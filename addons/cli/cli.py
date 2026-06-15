import sys
import subprocess
import json
import shutil
from pathlib import Path
from .logger import log
from ..wap.wap import get_executed_tables
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

    log.info(f"Running dbt {' '.join([dbt_command] + args[1:])}...")
    result = subprocess.run([real_dbt, dbt_command] + args[1:])
    log.info("")

    tables_to_copy, skipped = get_executed_tables()

    if not tables_to_copy:
        log.warning("No tables to copy")
        return 0

    log.info(f"[dbt-addon WAP] Publishing {len(tables_to_copy)} tables to prod...")
    tables_json = json.dumps(tables_to_copy)
    skipped_json = json.dumps(skipped)

    deploy_result = subprocess.run([
        real_dbt, 'run-operation', 'wap_deploy',
        '--args', f'{{tables_to_copy: {tables_json}, skipped_tables: {skipped_json}}}'
    ])
    log.info("")

    return deploy_result.returncode


if __name__ == '__main__':
    sys.exit(main())
