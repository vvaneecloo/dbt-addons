import json
from pathlib import Path
from typing import List

def get_executed_tables() -> List[str]:
    """Extract successfully built models whose tests all passed from run_results.json."""
    run_results_path = Path('target/run_results.json')
    manifest_path = Path('target/manifest.json')

    if not run_results_path.exists():
        return []

    with open(run_results_path) as f:
        run_results = json.load(f)

    results = run_results.get('results', [])

    # Find models blocked by a failing test via manifest dependency graph
    failed_model_ids: set = set()
    if manifest_path.exists():
        with open(manifest_path) as f:
            manifest = json.load(f)
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