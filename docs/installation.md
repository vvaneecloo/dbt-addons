# Installation

## 1. Install the package

```bash
pip install dbt-wap-addon
```

## 2. Install the WAP macros into your dbt project

Run this from your dbt project root:

```bash
dbt-addons wap install
```

This copies the WAP macros into `macros/dbt_addons/` in your project. Re-run it after upgrading the package to get the latest macros.

## 3. Add the required variables to `dbt_project.yml`

```yaml
vars:
  dbt_staging_schema: staging
  dbt_prod_schema: prod
```

See [Configuration](configuration.md) for the full list of variables per adapter.
