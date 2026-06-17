# Installation

## 2 ways of installing this addon

1. You want WAP logic in the same environment (`exposition` for instance)

2. You want WAP logic in 2 separate environments (`staging` & `exposition` for instance)

## You want WAP logic in the same environment

1. Add this to your `dbt_project.yml`:

```yaml
vars:
  dbt-addons:
    wap_staging_suffix: __staging # the suffix your audit table will use
    addons:
      - wap
```

2. Install the required dbt macros with `dbta install`.

## You want WAP logic in 2 separate environments

1. Add this to your `dbt_project.yml`:

```yaml
vars:
  dbt-addons:
    dbt_staging_schema: staging
    dbt_prod_schema: prod
    addons:
      - wap
```

2. Install the required dbt macros with `dbta install`.