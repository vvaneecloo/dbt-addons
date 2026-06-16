import shutil
from pathlib import Path
from typing import List

import yaml

from .cli.logger import log

ADDONS_ROOT = Path(__file__).parent


def _install_addon(name: str) -> bool:
    src = ADDONS_ROOT / name / 'macros'
    if not src.exists():
        log.warning(f"No macros found for addon '{name}' — skipping")
        return False

    dest = Path('macros/dbt_addons') / name
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(src, dest)
    log.info(f"Installed addon '{name}' → {dest}/")
    return True


def _active_adapter() -> str:
    """Return the adapter type from profiles.yml for the active profile, or '' if unknown."""
    project_file = Path('dbt_project.yml')
    profiles_file = Path('profiles.yml')
    if not project_file.exists() or not profiles_file.exists():
        return ''
    with open(project_file) as f:
        profile_name = yaml.safe_load(f).get('profile', '')
    with open(profiles_file) as f:
        profiles = yaml.safe_load(f)
    profile = profiles.get(profile_name, {})
    target = profile.get('target', '')
    return profile.get('outputs', {}).get(target, {}).get('type', '')


def _install_wap_root_macro(cfg: dict) -> None:
    """Install the root macros required for the configured WAP strategy."""
    rename_mode = bool(cfg.get('wap_staging_suffix'))
    Path('macros').mkdir(exist_ok=True)

    # generate_schema_name is only needed for DuckDB — other adapters manage it themselves
    if _active_adapter() == 'duckdb':
        src = ADDONS_ROOT / 'wap' / 'root_macros' / 'generate_schema_name.sql'
        shutil.copy(src, Path('macros') / 'generate_schema_name.sql')
        log.info("  Added macros/generate_schema_name.sql (duckdb)")

    if rename_mode:
        src = ADDONS_ROOT / 'wap' / 'root_macros' / 'generate_alias_name.sql'
        shutil.copy(src, Path('macros') / 'generate_alias_name.sql')
        log.info("  Added macros/generate_alias_name.sql (rename mode)")
    else:
        dest = Path('macros') / 'generate_alias_name.sql'
        if dest.exists():
            dest.unlink()
            log.info("  Removed macros/generate_alias_name.sql")


def _read_project_cfg() -> dict:
    project_file = Path('dbt_project.yml')
    if not project_file.exists():
        return {}
    with open(project_file) as f:
        project = yaml.safe_load(f)
    return project.get('vars', {}).get('dbt-addons', {})


def install_from_project() -> int:
    project_file = Path('dbt_project.yml')
    if not project_file.exists():
        log.error("dbt_project.yml not found — run this from your dbt project root")
        return 1

    with open(project_file) as f:
        project = yaml.safe_load(f)

    cfg = project.get('vars', {}).get('dbt-addons', {})
    addons: List[str] = cfg.get('addons', [])

    if not addons:
        log.warning("No addons configured under vars.dbt-addons.addons in dbt_project.yml")
        return 0

    log.info(f"Installing {len(addons)} addon(s): {', '.join(addons)}")
    for name in addons:
        _install_addon(name)
        if name == 'wap':
            _install_wap_root_macro(cfg)

    return 0


def install_addon(name: str) -> int:
    if not _install_addon(name):
        return 1
    if name == 'wap':
        _install_wap_root_macro(_read_project_cfg())
    return 0
