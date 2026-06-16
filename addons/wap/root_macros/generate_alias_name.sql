{% macro generate_alias_name(custom_alias_name=none, node=none) -%}
    {%- set suffix = var('dbt_wap_staging_suffix', '') if node.resource_type == 'model' else '' -%}
    {%- if custom_alias_name is none -%}
        {{ node.name }}{{ suffix }}
    {%- else -%}
        {{ custom_alias_name }}{{ suffix }}
    {%- endif -%}
{%- endmacro %}
