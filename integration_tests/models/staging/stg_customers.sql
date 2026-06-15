SELECT
  customer_id,
  customer_name,
  email,
  country,
  created_date,
  CURRENT_TIMESTAMP as dbt_loaded_at
FROM {{ source('staging', 'customers_raw') }}