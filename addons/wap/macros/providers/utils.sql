{% macro deploy_wap(tables_to_copy, skipped_tables, queries) %}
  {% if execute %}
    {% set total = (tables_to_copy | length) + (skipped_tables | length) %}
    {% set width = 80 %}

    {% for item in tables_to_copy %}
      {% set start_label = loop.index ~ " of " ~ total ~ " START copying " ~ item.name %}
      {% set start_dots = "." * ([width - start_label | length, 1] | max) %}
      {% do log(start_label ~ " " ~ start_dots ~ " [RUN]", info=true) %}

      {% do run_query(queries[loop.index - 1]) %}

      {% set ok_label = loop.index ~ " of " ~ total ~ " OK " ~ item.name %}
      {% set ok_dots = "." * ([width - ok_label | length, 1] | max) %}
      {% do log(ok_label ~ " " ~ ok_dots ~ " [\x1b[32mOK\x1b[0m]", info=true) %}
    {% endfor %}

    {% for name in skipped_tables %}
      {% set idx = (tables_to_copy | length) + loop.index %}
      {% set fail_label = idx ~ " of " ~ total ~ " FAIL " ~ name %}
      {% set fail_dots = "." * ([width - fail_label | length, 1] | max) %}
      {% do log(fail_label ~ " " ~ fail_dots ~ " [\x1b[31mFAIL\x1b[0m]", info=true) %}
    {% endfor %}

    {% set n_copied = tables_to_copy | length %}
    {% set n_failed = skipped_tables | length %}
    {% set summary = "PASS=" ~ n_copied ~ " FAIL=" ~ n_failed ~ " TOTAL=" ~ total %}

    {% do log("", info=true) %}
    {% if n_copied == 0 %}
      {% do log("[\x1b[31mNO TABLES\x1b[0m] " ~ summary, info=true) %}
    {% elif n_copied < total %}
      {% do log("[\x1b[33mPARTIAL\x1b[0m] " ~ summary, info=true) %}
    {% else %}
      {% do log("[\x1b[32mOK\x1b[0m] " ~ summary, info=true) %}
    {% endif %}
  {% endif %}
{% endmacro %}

{% macro all_required_variables_are_setup() %}
  {% if execute %}
    {% set adapter_type = adapter.type() %}
    {% set cfg = var('dbt-addons', {}) %}
    {% set required_vars = {} %}

    {% set common_vars = {
      'dbt_staging_schema': cfg.get('dbt_staging_schema'),
      'dbt_prod_schema': cfg.get('dbt_prod_schema')
    } %}

    {% if adapter_type == 'snowflake' %}
      {% set required_vars = common_vars %}

    {% elif adapter_type == 'bigquery' %}
      {% set required_vars = common_vars | combine({
        'project_id': cfg.get('project_id'),
        'prod_dataset': cfg.get('prod_dataset'),
        'staging_dataset': cfg.get('staging_dataset')
      }) %}

    {% elif adapter_type == 'duckdb' %}
      {% set required_vars = common_vars %}

    {% else %}
      {% do log("Unknown adapter: " ~ adapter_type, info=true) %}
      {% set required_vars = common_vars %}
    {% endif %}

    {% set missing_vars = [] %}
    {% for var_name, var_value in required_vars.items() %}
      {% if var_value is none %}
        {% do missing_vars.append(var_name) %}
      {% endif %}
    {% endfor %}

    {% if missing_vars | length > 0 %}
      {% do log("[" ~ adapter_type ~ "] Missing required variables: " ~ missing_vars | join(', '), info=true) %}
      {% do exceptions.raise_compiler_error("Setup incomplete for " ~ adapter_type ~ ". Define: " ~ missing_vars | join(', ')) %}
    {% else %}
      {% do log("[" ~ adapter_type ~ "] All required variables configured", info=true) %}
      {% for var_name, var_value in required_vars.items() %}
        {% do log("   • " ~ var_name ~ ": " ~ var_value, info=true) %}
      {% endfor %}
    {% endif %}
  {% endif %}
{% endmacro %}
