# Configuration

## Schema name generation

By default dbt prepends the target schema to custom schemas (e.g. `main_staging`). Add this macro to your project so schemas are used as-is:

```sql title="macros/generate_schema_name.sql"
{% macro generate_schema_name(custom_schema_name, node) -%}
    {%- if custom_schema_name is none -%}
        {{ target.schema }}
    {%- else -%}
        {{ custom_schema_name | trim }}
    {%- endif -%}
{%- endmacro %}
```

## Variables

### Common (all adapters)

| Variable | Description |
|---|---|
| `dbt_staging_schema` | Schema where dbt builds models |
| `dbt_prod_schema` | Schema where WAP publishes passing models |

### BigQuery only

| Variable | Description |
|---|---|
| `project_id` | GCP project ID |
| `prod_dataset` | BigQuery dataset for prod |

### Databricks only

| Variable | Description |
|---|---|
| `catalog` | Unity Catalog name |

```yaml title="dbt_project.yml"
vars:
  dbt_staging_schema: staging
  dbt_prod_schema: prod
```
