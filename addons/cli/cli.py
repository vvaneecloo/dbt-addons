import sys
import subprocess
import json
import shutil
import yaml
from pathlib import Path
from .logger import log
from ..wap.wap import get_executed_tables, read_wap_config
from ..install import install_from_project, install_addon


def get_real_dbt_path():
    dbt_path = shutil.which('dbt')

    if not dbt_path:
        log.error("dbt not found in PATH")
        sys.exit(1)

    real_path = Path(dbt_path).resolve()

    if real_path == Path(__file__).resolve():
        import os
        path_dirs = os.environ['PATH'].split(os.pathsep)
        current_dir = str(Path(__file__).parent.resolve())
        filtered_path = os.pathsep.join([d for d in path_dirs if d != current_dir])

        old_path = os.environ['PATH']
        os.environ['PATH'] = filtered_path
        dbt_path = shutil.which('dbt')
        os.environ['PATH'] = old_path

        if not dbt_path:
            log.error("Real dbt executable not found")
            sys.exit(1)

    return dbt_path


def _read_profile_outputs() -> dict:
    project_file = Path('dbt_project.yml')
    profiles_file = Path('profiles.yml')
    if not project_file.exists() or not profiles_file.exists():
        return {}
    with open(project_file) as f:
        profile_name = yaml.safe_load(f).get('profile', '')
    with open(profiles_file) as f:
        profiles = yaml.safe_load(f)
    return profiles.get(profile_name, {}).get('outputs', {})


def _active_target(dbt_args: list) -> str:
    for i, arg in enumerate(dbt_args):
        if arg in ('--target', '-t') and i + 1 < len(dbt_args):
            return dbt_args[i + 1]
    project_file = Path('dbt_project.yml')
    profiles_file = Path('profiles.yml')
    if not project_file.exists() or not profiles_file.exists():
        return ''
    with open(project_file) as f:
        profile_name = yaml.safe_load(f).get('profile', '')
    with open(profiles_file) as f:
        profiles = yaml.safe_load(f)
    return profiles.get(profile_name, {}).get('target', '')


def _target_schema(target_name: str) -> str:
    return _read_profile_outputs().get(target_name, {}).get('schema', '')


def _set_target(dbt_args: list, target_name: str) -> list:
    """Return a copy of dbt_args with --target set to target_name."""
    args = list(dbt_args)
    for flag in ('--target', '-t'):
        if flag in args:
            args[args.index(flag) + 1] = target_name
            return args
    return args + ['--target', target_name]


def _merge_wap_vars(args: list, extra: dict) -> list:
    args = list(args)
    if '--vars' in args:
        idx = args.index('--vars')
        try:
            existing = yaml.safe_load(args[idx + 1]) or {}
        except Exception:
            existing = {}
        existing.update(extra)
        args[idx + 1] = json.dumps(existing)
    else:
        args += ['--vars', json.dumps(extra)]
    return args


def main():
    real_dbt = get_real_dbt_path()
    args = sys.argv[1:]

    if args[:1] == ['install']:
        return install_from_project()

    if args[:2] == ['wap', 'install']:
        return install_addon('wap')

    if '--wap' not in args:
        return subprocess.run([real_dbt] + args).returncode

    args.remove('--wap')
    dbt_command = args[0] if args else None

    if dbt_command not in ['run', 'build']:
        log.error("--wap only works with 'run' or 'build'")
        return 1

    dbt_args = list(args[1:])
    wap_config = read_wap_config()

    prod_target = wap_config.get('prod_target')
    if prod_target and _active_target(dbt_args) != prod_target:
        log.warning(f"[dbt-addon WAP] prod_target is '{prod_target}' — running plain dbt {dbt_command}")
        return subprocess.run([real_dbt, dbt_command] + dbt_args).returncode

    suffix = wap_config.get('wap_staging_suffix')
    if suffix:
        dbt_args = _merge_wap_vars(dbt_args, {'dbt_wap_staging_suffix': suffix})

    audit_target = wap_config.get('audit_target')
    if audit_target:
        dbt_args = _set_target(dbt_args, audit_target)

    log.info(f"Running dbt {dbt_command} on target '{_active_target(dbt_args)}'...")
    subprocess.run([real_dbt, dbt_command] + dbt_args)
    log.info("")

    tables_to_copy, skipped = get_executed_tables()

    if not tables_to_copy:
        log.warning("No tables to copy")
        return 0

    log.info(f"[dbt-addon WAP] Publishing {len(tables_to_copy)} tables to prod...")
    tables_json = json.dumps(tables_to_copy)
    skipped_json = json.dumps(skipped)

    # In rename mode the schema is derived from the relation — no injection needed.
    # In cross-schema mode the prod schema comes from the prod_target profile.
    suffix = wap_config.get('wap_staging_suffix')
    if not suffix and prod_target:
        prod_schema = _target_schema(prod_target)
        deploy_vars = json.dumps({'dbt_wap_prod_schema': prod_schema}) if prod_schema else '{}'
    else:
        deploy_vars = '{}'

    deploy_result = subprocess.run([
        real_dbt, 'run-operation', 'wap_deploy',
        '--vars', deploy_vars,
        '--args', f'{{tables_to_copy: {tables_json}, skipped_tables: {skipped_json}}}'
    ])
    log.info("")

    return deploy_result.returncode


if __name__ == '__main__':
    sys.exit(main())
