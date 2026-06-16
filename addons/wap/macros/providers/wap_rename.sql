{% macro wap_rename_snowflake(tables_to_copy, skipped_tables, suffix) %}
    {% set queries = [] %}
    {% for item in tables_to_copy %}
        {% set staging_name = item.name ~ suffix %}
        {% set target = item.relation
            | replace(staging_name | upper, item.name | upper)
            | replace(staging_name, item.name) %}
        {% set q %}
            CREATE OR REPLACE TABLE {{ target }} CLONE {{ item.relation }}
        {% endset %}
        {% do queries.append(q) %}
    {% endfor %}

    {{ deploy_wap(tables_to_copy, skipped_tables, queries) }}
{% endmacro %}


{% macro wap_rename_databricks(tables_to_copy, skipped_tables, suffix) %}
    {% set queries = [] %}
    {% for item in tables_to_copy %}
        {% set staging_name = item.name ~ suffix %}
        {% set target = item.relation
            | replace(staging_name | upper, item.name | upper)
            | replace(staging_name, item.name) %}
        {% set q %}
            CREATE OR REPLACE TABLE {{ target }} SHALLOW CLONE {{ item.relation }}
        {% endset %}
        {% do queries.append(q) %}
    {% endfor %}

    {{ deploy_wap(tables_to_copy, skipped_tables, queries) }}
{% endmacro %}


{% macro wap_rename_bigquery(tables_to_copy, skipped_tables, suffix) %}
    {% set queries = [] %}
    {% for item in tables_to_copy %}
        {% set staging_name = item.name ~ suffix %}
        {% set target = item.relation
            | replace(staging_name | upper, item.name | upper)
            | replace(staging_name, item.name) %}
        {% set q %}
            CREATE OR REPLACE TABLE {{ target }} AS
            SELECT * FROM {{ item.relation }}
        {% endset %}
        {% do queries.append(q) %}
    {% endfor %}

    {{ deploy_wap(tables_to_copy, skipped_tables, queries) }}
{% endmacro %}


{% macro wap_rename_duckdb(tables_to_copy, skipped_tables, suffix) %}
    {% set queries = [] %}
    {% for item in tables_to_copy %}
        {% set staging_name = item.name ~ suffix %}
        {% set target = item.relation
            | replace(staging_name | upper, item.name | upper)
            | replace(staging_name, item.name) %}
        {% set q %}
            CREATE OR REPLACE TABLE {{ target }} AS
            SELECT * FROM {{ item.relation }}
        {% endset %}
        {% do queries.append(q) %}
    {% endfor %}

    {{ deploy_wap(tables_to_copy, skipped_tables, queries) }}
{% endmacro %}
