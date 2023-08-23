Big Query

# opy the table for the new dbt database 
CREATE OR REPLACE TABLE `mindful-bivouac-395521.dbt_ntopel.table0` AS
SELECT DISTINCT
  adi,
  bos,
  dolu,
  sonBaglanti
FROM `mindful-bivouac-395521.db.table0`;

# Delete the null valus
DELETE FROM `mindful-bivouac-395521.dbt_ntopel.table0`
WHERE adi IS NULL
   OR dolu IS NULL
   OR bos IS NULL
   OR lon IS NULL
   OR lat IS NULL
   OR sonBaglanti IS NULL;