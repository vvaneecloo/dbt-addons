{{
  config(
    materialized="table"
  )
}}

SELECT
  customer_id,
  customer_name,
  email,
  country,
  created_date,
  dbt_loaded_at
FROM {{ ref('stg_customers') }}