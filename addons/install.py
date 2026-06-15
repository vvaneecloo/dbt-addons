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


def install_from_project() -> int:
    project_file = Path('dbt_project.yml')
    if not project_file.exists():
        log.error("dbt_project.yml not found — run this from your dbt project root")
        return 1

    with open(project_file) as f:
        project = yaml.safe_load(f)

    addons: List[str] = (
        project.get('meta', {})
               .get('dbt-addons', {})
               .get('addons', [])
    )

    if not addons:
        log.warning("No addons configured under meta.dbt-addons.addons in dbt_project.yml")
        return 0

    log.info(f"Installing {len(addons)} addon(s): {', '.join(addons)}")
    for name in addons:
        _install_addon(name)

    return 0


def install_addon(name: str) -> int:
    return 0 if _install_addon(name) else 1
