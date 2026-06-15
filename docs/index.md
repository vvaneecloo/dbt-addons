# dbt-addons

A CLI built on top of dbt that adds features to your dbt workflows.

## Features

- Drop-in wrapper around `dbt run` and `dbt build`
- Promotes tables to prod via zero-copy clone on Snowflake and Databricks
- Automatically skips models with failing tests
- dbt-style log output with coloured status indicators
- Supports DuckDB, Snowflake, Databricks, and BigQuery
