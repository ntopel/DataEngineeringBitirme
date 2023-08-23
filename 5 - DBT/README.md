DBT 

# table0.sql 

{{ config(
    materialized='table'
) }}

SELECT * FROM dbt_ntopel.table0 WHERE dolu > 0


# create-model.sql 

{{ config(
    materialized='table'
) }}

WITH bike_degisimler AS (
    SELECT
        adi,
        dolu,
        sonBaglanti,
        lon,
        lat,
        LAG(dolu) OVER(PARTITION BY adi ORDER BY sonBaglanti) AS prev_dolu,
        LAG(sonBaglanti) OVER(PARTITION BY adi ORDER BY sonBaglanti) AS prev_sonBaglanti
    FROM
        {{ ref('table0') }}  -- Reference to the table1 model
),
 
kullanim_suresi AS (
    SELECT
        adi,
        dolu,
        sonBaglanti,
        lon,
        lat,
        prev_dolu,
        prev_sonBaglanti,
        TIMESTAMP_DIFF(sonBaglanti, prev_sonBaglanti, SECOND) AS zaman_farki,
        IFNULL(ABS(dolu - prev_dolu), 0) AS bike_degisim
    FROM
        bike_degisimler
)

SELECT
    adi,
    lon,
    lat,
    SUM(bike_degisim * zaman_farki) AS total_kullanim_saniye,
    CASE WHEN SUM(zaman_farki) = 0 THEN NULL
         ELSE SUM(bike_degisim * zaman_farki) / SUM(zaman_farki)
    END AS activity_degisim
FROM
    kullanim_suresi
GROUP BY
    adi, lon, lat
ORDER BY
    total_kullanim_saniye DESC


# dbt_project.yml 


name: 'my_new_project'
version: '1.0.0'
config-version: 2

profile: 'default'


model-paths: ["models"]
analysis-paths: ["analyses"]
test-paths: ["tests"]
seed-paths: ["seeds"]
macro-paths: ["macros"]
snapshot-paths: ["snapshots"]

target-path: "target"  # directory which will store compiled SQL files
clean-targets:         # directories to be removed by `dbt clean`
  - "target"
  - "dbt_packages"




models:
  my_new_project:
    table1:
      materialized: table
    create_model:
      materialized: table
