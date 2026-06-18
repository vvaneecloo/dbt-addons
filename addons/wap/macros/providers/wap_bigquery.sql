{% macro wap_deploy_bigquery(tables_to_copy, skipped_tables=[]) %}
    {% set project_id = var('dbt-addons')['project_id'] %}
    {% set prod_dataset = var('dbt-addons')['prod_dataset'] %}

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
