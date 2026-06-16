import json
import fnmatch
from pathlib import Path
from typing import List, Optional

import yaml


def read_wap_config() -> dict:
    project_path = Path('dbt_project.yml')
    if not project_path.exists():
        return {}
    with open(project_path) as f:
        project = yaml.safe_load(f)
    return project.get('vars', {}).get('dbt-addons', {})


def _matches_wap_paths(model_path: str, wap_paths: List[str]) -> bool:
    """Return True if model_path (e.g. 'marts/fct_customers.sql') matches any pattern."""
    for pattern in wap_paths:
        norm = pattern.rstrip('/')
        # Folder prefix: 'marts' matches 'marts/fct_customers.sql'
        if model_path.startswith(norm + '/') or model_path == norm:
            return True
        # Glob pattern: 'marts/*.sql' or 'core/fct_*'
        if fnmatch.fnmatch(model_path, pattern):
            return True
    return False


def get_executed_tables() -> List[str]:
    """Extract successfully built models whose tests all passed from run_results.json."""
    run_results_path = Path('target/run_results.json')
    manifest_path = Path('target/manifest.json')

    if not run_results_path.exists():
        return [], []

    with open(run_results_path) as f:
        run_results = json.load(f)

    results = run_results.get('results', [])

    manifest = {}
    if manifest_path.exists():
        with open(manifest_path) as f:
            manifest = json.load(f)

    wap_config = read_wap_config()
    wap_paths: Optional[List[str]] = wap_config.get('wap_paths')  # None = all models

    # Find models blocked by a failing test via manifest dependency graph
    failed_model_ids: set = set()
    for result in results:
        if result.get('status') not in ('fail', 'error'):
            continue
        uid = result.get('unique_id', '')
        if not uid.startswith('test.'):
            continue
        test_node = manifest.get('nodes', {}).get(uid, {})
        for dep in test_node.get('depends_on', {}).get('nodes', []):
            if dep.startswith('model.'):
                failed_model_ids.add(dep)

    promoted = []
    skipped = []
    for result in results:
        if result.get('status') != 'success':
            continue
        uid = result.get('unique_id', '')
        if not uid.startswith('model.'):
            continue

        node = manifest.get('nodes', {}).get(uid, {})

        if wap_paths is not None:
            model_path = node.get('path', '')
            if not _matches_wap_paths(model_path, wap_paths):
                continue

        table_name = uid.split('.')[-1]
        if uid in failed_model_ids:
            skipped.append(table_name)
            continue
        relation_name = result.get('relation_name')
        if relation_name:
            promoted.append({"name": table_name, "relation": relation_name})

    return sorted(promoted, key=lambda t: t["name"]), sorted(skipped)



def run_with_wap(args: List[str]) -> int:
    """Run dbt run with WAP deployment."""
    import subprocess
    
    return subprocess.run(['dbt', 'run'] + args).returncode


def build_with_wap(args: List[str]) -> int:
    """Run dbt build with WAP deployment."""
    import subprocess
    
    return subprocess.run(['dbt', 'build'] + args).returncode