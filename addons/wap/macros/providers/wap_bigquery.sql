{% macro wap_deploy_bigquery(tables_to_copy, skipped_tables=[]) %}
    {% set project_id = target.database %}
    {% set prod_dataset = var('dbt_wap_prod_schema') %}

    {% set queries = [] %}
    {% for item in tables_to_copy %}
        {% set q %}
            CREATE OR REPLACE TABLE `{{ project_id }}.{{ prod_dataset }}.{{ item.name }}`
            CLONE {{ item.relation }}
        {% endset %}
        {% do queries.append(q) %}
    {% endfor %}

    {{ deploy_wap(tables_to_copy, skipped_tables, queries) }}
{% endmacro %}
