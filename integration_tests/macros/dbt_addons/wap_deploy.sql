{% macro wap_deploy(tables_to_copy, skipped_tables=[]) %}
  {# Main WAP orchestration macro - routes to provider-specific implementations #}
  
  {% set provider = adapter.type() %}
  
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
  
{% endmacro %}