-- Databricks notebook source
SELECT * from delta_catalog.delta_db.invoices_se;
-- DELETE FROM delta_catalog.delta_db.invoices_sv WHERE customer_id in (200,199,198,197,196)
ALTER TABLE delta_catalog.delta_db.invoices_se DROP COLUMN purchase_details.staff_id;

-- COMMAND ----------

part-00000-9c4e2750-2eeb-4014-8b28-6b2219ef8910-c000.zstd.parquet
deletion_vector_6c3dce3c-b847-4b9b-9fa4-1f9703295a3c.bin
deletion_vector_e07992a7-b262-4f2a-9b27-f11eec60e71d.bin
part-00000-04d26777-f1aa-4506-87e1-f892c775a31c-c000.zstd.parquet
part-00000-cb6f5953-2c67-40ea-9046-4753497c5f0f-c000.zstd.parquet

-- COMMAND ----------


