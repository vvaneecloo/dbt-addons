{% macro wap_deploy_databricks(tables_to_copy, skipped_tables=[]) %}
    {% set catalog = var('catalog') %}
    {% set prod_schema = var('dbt_prod_schema') %}

    {% set queries = [] %}
    {% for item in tables_to_copy %}
        {% set q %}
            CREATE OR REPLACE TABLE `{{ catalog }}`.`{{ prod_schema }}`.`{{ item.name }}`
            SHALLOW CLONE {{ item.relation }}
        {% endset %}
        {% do queries.append(q) %}
    {% endfor %}

    {{ deploy_wap(tables_to_copy, skipped_tables, queries) }}
{% endmacro %}
