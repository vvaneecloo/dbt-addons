# Usage

## Commands

### Install macros

```bash
dbta wap install
```

Copies the WAP macros into `macros/dbt_addons/` in your current dbt project. Re-run after upgrading the package.

### Run with WAP

```bash
dbta run --wap
dbta build --wap
```

The `--wap` flag activates the full Write-Audit-Publish flow. Without it, `dbta` behaves exactly like `dbt`.

All standard dbt flags are supported:

```bash
dbta build --wap --select stg_customers fct_customers
dbta build --wap -s stg_customers fct_customers
dbta run --wap --target prod
```

## What happens

1. `dbt run` / `dbt build` runs normally — models are built in the staging schema
2. `run_results.json` is parsed to find which models succeeded and which tests failed
3. Models with failing tests are excluded from the publish step
4. `wap_deploy` is called — tables are promoted to prod via clone or copy
5. A summary is printed

## Log output

```
14:01:03  Running dbt build...
14:01:03  Running with dbt=1.9.3
...
14:01:05  [dbt-addon WAP] Publishing 1 tables to prod...
14:01:05  1 of 2 START copying stg_customers ......................... [RUN]
14:01:05  1 of 2 OK stg_customers ................................... [OK]
14:01:05  2 of 2 FAIL fct_customers ................................. [FAIL]

14:01:05  [PARTIAL] PASS=1 FAIL=1 TOTAL=2
```
