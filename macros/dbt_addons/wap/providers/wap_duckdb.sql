{% macro wap_deploy_duckdb(tables_to_copy, skipped_tables=[]) %}
    {% set prod_schema = var('dbt_prod_schema') %}

    {% do run_query("CREATE SCHEMA IF NOT EXISTS " ~ prod_schema) %}
    {% do log("", info=true) %}

    {% set queries = [] %}
    {% for item in tables_to_copy %}
        {% set q %}
            CREATE OR REPLACE TABLE {{ prod_schema }}.{{ item.name }} AS
            SELECT * FROM {{ item.relation }}
        {% endset %}
        {% do queries.append(q) %}
    {% endfor %}

    {{ deploy_wap(tables_to_copy, skipped_tables, queries) }}
{% endmacro %}
