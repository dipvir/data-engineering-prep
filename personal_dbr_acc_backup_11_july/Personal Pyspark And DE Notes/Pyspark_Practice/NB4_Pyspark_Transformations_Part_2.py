# Databricks notebook source
# /// script
# [tool.databricks.environment]
# environment_version = "5"
# ///
# DBTITLE 1,Imports
import pyspark.sql.functions as F

# COMMAND ----------

# DBTITLE 1,Create Dataframe
df=spark.read.table("samples.bakehouse.sales_transactions")
display(df)

# COMMAND ----------

# DBTITLE 1,Boolean - PySpark
# df2=df.filter("paymentMethod =='mastercard'")
df2=df.where(F.col("paymentMethod") !='mastercard')
display(df2)

# COMMAND ----------

# DBTITLE 1,Boolean - SQL
# MAGIC %sql
# MAGIC select * from samples.bakehouse.sales_transactions where paymentMethod ='mastercard'
# MAGIC -- select * from samples.bakehouse.sales_transactions where paymentMethod !='mastercard'

# COMMAND ----------

# DBTITLE 1,Numbers - PySpark
df2 = (
    df.withColumn("myCol_1",F.pow("quantity",2)/6)
        .withColumn("myCol_2",F.round(F.pow("quantity",2)/6,2))
      )
display(df2)

# COMMAND ----------

# DBTITLE 1,Numbers - SQL
# MAGIC %sql
# MAGIC select *,round(pow(quantity,2)/6,2) from samples.bakehouse.sales_transactions 

# COMMAND ----------

# DBTITLE 1,String Manipulations and Splitting Functions - PySpark
df2 = df.select("product").\
            withColumn("lower_product",F.expr("lower(product)")).\
            withColumn("upper_product",F.expr("upper(product)")).\
            withColumn("trim_product",F.expr("trim(product)")).\
            withColumn("substr_product",F.expr("substr(product,0,4)")).\
            withColumn("split_product",F.expr("split(product,' ')"))
display(df2)

# COMMAND ----------

# DBTITLE 1,String Manipulations and Splitting Functions - SQL
# MAGIC %sql
# MAGIC SELECT 
# MAGIC         product,
# MAGIC         lower(product) AS lower_product,
# MAGIC         upper(product) AS upper_product,
# MAGIC         trim(product) AS trim_product,
# MAGIC         substr(product, 0, 4) AS substr_product,
# MAGIC         split(product, ' ') AS split_product
# MAGIC     FROM samples.bakehouse.sales_transactions

# COMMAND ----------

# DBTITLE 1,RegEx - PySpark
df2=df.select("product").\
withColumn("regexp_extract_product", F.expr("regexp_extract(product, r'^\S+\s+(\S+)\s+\S+$', 1)")).\
withColumn("regexp_replace_product", F.expr("regexp_replace(product, r'^\S+\s+(\S+)\s+\S+$', 'AAAA')"))
display(df2)

# COMMAND ----------

# DBTITLE 1,RegEx - SQL
# MAGIC %sql
# MAGIC SELECT 
# MAGIC     product,
# MAGIC     regexp_extract(product, r'^\S+\s+(\S+)\s+\S+$', 1) AS regexp_extract_product,
# MAGIC     regexp_replace(product, r'^\S+\s+(\S+)\s+\S+$', 'AAAA') AS regexp_replace_product
# MAGIC   FROM samples.bakehouse.sales_transactions

# COMMAND ----------

# DBTITLE 1,Date Manipulations and Custom Timestamps - PySpark
df2 = df.select("dateTime")\
.withColumn("today", F.current_date())\
.withColumn("now", F.current_timestamp())\
.withColumn("dateTime_date", F.to_date("dateTime"))\
.withColumn("dateTime_date_add", F.date_add(F.to_date("dateTime"),5))\
.withColumn("dateTime_date_sub", F.date_sub(F.to_date("dateTime"),5))\
.withColumn("custom_date", F.to_date(F.lit("20251014"),'yyyyMMdd'))\
.withColumn("custom_timestamp", F.to_timestamp(F.lit("20251014112233"),'yyyyMMddHHmmss'))
display(df2)

# COMMAND ----------

# DBTITLE 1,Date Manipulations and Custom Timestamps - SQL
# MAGIC %sql
# MAGIC SELECT 
# MAGIC   dateTime,
# MAGIC   current_date() AS today,
# MAGIC   current_timestamp() AS now,
# MAGIC   to_date(dateTime) AS dateTime_date,
# MAGIC   date_add(to_date(dateTime), 5) AS dateTime_date_add,
# MAGIC   date_sub(to_date(dateTime), 5) AS dateTime_date_sub,
# MAGIC   to_date('20251014', 'yyyyMMdd') AS custom_date,
# MAGIC   to_timestamp('20251014112233', 'yyyyMMddHHmmss') AS custom_timestamp
# MAGIC FROM samples.bakehouse.sales_transactions

# COMMAND ----------

# DBTITLE 1,Null Handling and Conditional Columns PySpark
# Select transactionID and customerID columns
# coalesce returns first non-null value between from given cols
# Uses CASE WHEN to choose transactionID if not null, else customerID

df2 = df.select("transactionID","customerID")\
    .withColumn("coalesce_id", F.coalesce("transactionID", "customerID"))\
    .withColumn("if_else", F.expr("CASE WHEN transactionID IS NOT NULL THEN transactionID ELSE customerID END"))\
    .na.drop(subset=["transactionID"])  # Drop rows where transactionID is null
    # .na.drop('all')  # Would drop rows only if ALL columns are null
    # .na.fill('myvalue')  # Would fill null values with 'myvalue'

# Display the resulting dataframe
display(df2)

# COMMAND ----------

# DBTITLE 1,Null Handling and Conditional Columns - SQL
# MAGIC %sql
# MAGIC SELECT 
# MAGIC         transactionID,
# MAGIC         customerID,
# MAGIC         coalesce(transactionID, customerID) AS coalesce_id,
# MAGIC         CASE WHEN transactionID IS NOT NULL THEN transactionID ELSE customerID END AS if_else
# MAGIC     FROM samples.bakehouse.sales_transactions
