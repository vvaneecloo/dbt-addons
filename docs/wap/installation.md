# Installation

## 2 ways of installing this addon

1. You want WAP logic in the same environment/dataset (`exposition` for instance):
  - dbta build objects in `exposition` with a suffix (for instance `__audit`) e.g. `exposition.fct_customers__audit`
  - then dbta zero copy clone them without suffix e.g. `exposition.fct_customers`
  - your business users only point to the no-audit table e.g. `exposition.fct_customers`

2. You want WAP logic in 2 separate environments (`audit` & `exposition` for instance)
  - dbta build objects in `audit` **without a suffix** e.g. `audit.fct_customers`
  - then dbta zero copy clone them on your exposition environment e.g. `exposition.fct_customers`
  - your business users only point to the exposition table e.g. `exposition.fct_customers`

## You want WAP logic in the same environment

1. Add this to your `dbt_project.yml`:

```yaml
vars:
  dbt-addons:
    wap_staging_suffix: __staging # the suffix your audit table will use
    prod_target: prod # the prod target you need dbta to work on (avoid running wap in dev / preprod / ci)
    addons:
      - wap
```

2. Install the required dbt macros with `dbta install`.

## You want WAP logic in 2 separate environments

1. Add this to your `dbt_project.yml`:

```yaml
vars:
  dbt-addons:
    # when you run in prod, dbta will automatically run in `audit` env first and then clone in `prod`
    prod_target: prod
    audit_target: audit
    addons:
      - wap
```

2. Install the required dbt macros with `dbta install`.