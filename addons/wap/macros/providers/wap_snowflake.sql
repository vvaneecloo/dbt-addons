{% macro wap_deploy_snowflake(tables_to_copy, skipped_tables=[]) %}
    {% set prod_schema = var('dbt-addons')['dbt_prod_schema'] %}

    {% set queries = [] %}
    {% for item in tables_to_copy %}
        {% set q %}
            CREATE OR REPLACE TABLE {{ prod_schema }}.{{ item.name }}
            CLONE {{ item.relation }}
        {% endset %}
        {% do queries.append(q) %}
    {% endfor %}

    {{ deploy_wap(tables_to_copy, skipped_tables, queries) }}
{% endmacro %}
