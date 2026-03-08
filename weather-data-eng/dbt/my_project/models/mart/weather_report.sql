{{ config(
    materialized='table',
    unique_key='id'
)}}

select city,temperatue, weather_descriptions, wind_speed, weather_time_local from {{ ref('staging') }}
