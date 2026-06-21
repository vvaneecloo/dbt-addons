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
    {% set prod_schema = var('dbt_wap_prod_schema', none) %}
    {% if prod_schema is none %}
      {% do exceptions.raise_compiler_error("WAP: prod_target is not set in vars.dbt-addons or its schema could not be found in profiles.yml") %}
    {% else %}
      {% do log("[WAP] staging schema (target.schema): " ~ target.schema, info=true) %}
      {% do log("[WAP] prod schema (prod_target):       " ~ prod_schema, info=true) %}
    {% endif %}
  {% endif %}
{% endmacro %}
