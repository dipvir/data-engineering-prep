-- Databricks notebook source
SELECT * from delta_catalog.delta_db.invoices_se;
-- DELETE FROM delta_catalog.delta_db.invoices_sv WHERE customer_id in (200,199,198,197,196)
ALTER TABLE delta_catalog.delta_db.invoices_se DROP COLUMN purchase_details.staff_id;

-- COMMAND ----------


