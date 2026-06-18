# Providers

## Supported adapters

| Adapter | Publish method | Atomic |
|---|---|---|
| Snowflake | `CLONE` | Yes — zero-copy |
| Databricks | `SHALLOW CLONE` | Yes — zero-copy (Delta Lake) |
| BigQuery | `CLONE` | Yes — zero-copy |
| DuckDB | `CREATE OR REPLACE TABLE AS SELECT *` | No — full copy |

## Snowflake

Uses Snowflake's native zero-copy cloning. The publish step is instantaneous and costs no additional storage until the cloned table diverges.

```sql
CREATE OR REPLACE TABLE prod.table_name
CLONE staging.table_name
```

## Databricks

Uses Delta Lake shallow cloning. Metadata is copied instantly; data files are shared until the clone is modified.

```sql
CREATE OR REPLACE TABLE catalog.prod_schema.table_name
SHALLOW CLONE staging.table_name
```

Requires the `catalog` variable to be set in `dbt_project.yml`.

## BigQuery

Use zero-copy cloning at table level via `CREATE OR REPLACE TABLE ... CLONE {{ item.relation }}`.

Requires `project_id` and `prod_dataset` variables.

## DuckDB

No native cloning. WAP uses `CREATE OR REPLACE TABLE AS SELECT *`. Recommended for local development and testing.
