{% macro wap_deploy(tables_to_copy, skipped_tables=[]) %}
  {% set provider = adapter.type() %}
  {% set cfg = var('dbt-addons', {}) %}
  {% set wap_staging_suffix = cfg.get('wap_staging_suffix') %}

  {% if wap_staging_suffix %}
    {# Rename mode: models built with suffix, promoted within the same schema #}
    {% if provider == 'snowflake' %}
      {{ wap_rename_snowflake(tables_to_copy, skipped_tables, wap_staging_suffix) }}
    {% elif provider == 'bigquery' %}
      {{ wap_rename_bigquery(tables_to_copy, skipped_tables, wap_staging_suffix) }}
    {% elif provider == 'databricks' %}
      {{ wap_rename_databricks(tables_to_copy, skipped_tables, wap_staging_suffix) }}
    {% elif provider == 'duckdb' %}
      {{ wap_rename_duckdb(tables_to_copy, skipped_tables, wap_staging_suffix) }}
    {% else %}
      {% do exceptions.raise_compiler_error("WAP rename mode not supported for provider: " ~ provider) %}
    {% endif %}

  {% else %}
    {# Cross-schema mode: copy from staging schema to prod schema #}
    {% if not all_required_variables_are_setup() %}
      {% do exceptions.raise_compiler_error("All the variables needed for WAP are not setup.") %}
    {% endif %}

    {% if provider == 'snowflake' %}
      {{ wap_deploy_snowflake(tables_to_copy) }}
    {% elif provider == 'bigquery' %}
      {{ wap_deploy_bigquery(tables_to_copy) }}
    {% elif provider == 'databricks' %}
      {{ wap_deploy_databricks(tables_to_copy) }}
    {% elif provider == 'duckdb' %}
      {{ wap_deploy_duckdb(tables_to_copy, skipped_tables) }}
    {% else %}
      {% do log("WAP not supported for provider: " ~ provider, info=true) %}
      {% do exceptions.raise_compiler_error("Unsupported provider for WAP") %}
    {% endif %}

  {% endif %}

{% endmacro %}
