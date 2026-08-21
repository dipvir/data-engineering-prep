# Databricks notebook source
# /// script
# [tool.databricks.environment]
# environment_version = "5"
# ///
# DBTITLE 1,Imports
import  pyspark.sql.functions as F

# COMMAND ----------

# DBTITLE 1,Create Dataframe
df=spark.read.table("samples.bakehouse.sales_transactions")
display(df)

# COMMAND ----------

# DBTITLE 1,PySpark -Count
df.count()

# COMMAND ----------

# DBTITLE 1,PySpark - First and Last
print(df.first())
print(df.tail(1)[0])

# COMMAND ----------

# DBTITLE 1,PySpark - Min - Max
# df2=df.select(F.min("quantity"), F.max("quantity"))
# or
df2=df.select(F.min("quantity").alias("min_quantity") , F.max("quantity").alias("max_quantity"))
display(df2)

# COMMAND ----------

# DBTITLE 1,PySpark - Sum and Average
# df2=df.select(F.sum("quantity"), F.avg("quantity"))
# or
df2=df.selectExpr("sum(quantity) as sum_quantity", "avg(quantity) as avg_quantity")
display(df2)

# COMMAND ----------

# DBTITLE 1,SQL - Count, Min, Max, Average, Sum
# MAGIC %sql
# MAGIC select 
# MAGIC   count(*),
# MAGIC   min(quantity),
# MAGIC   max(quantity),
# MAGIC   avg(quantity),
# MAGIC   sum(quantity)
# MAGIC from samples.bakehouse.sales_transactions

# COMMAND ----------

# DBTITLE 1,PySpark - Group By
df2=df.groupBy("paymentMethod").count()
display(df2)

# COMMAND ----------

# DBTITLE 1,SQL Group by
# MAGIC %sql
# MAGIC select
# MAGIC   paymentMethod,
# MAGIC   count(*) as count,
# MAGIC   avg(quantity) as avg_quantity
# MAGIC from
# MAGIC   samples.bakehouse.sales_transactions
# MAGIC group by
# MAGIC   paymentMethod
# MAGIC -- having
# MAGIC --   count > 1100

# COMMAND ----------

# DBTITLE 1,PySpark - Group by - Having
df2 = df.groupBy("paymentMethod").count().filter(F.col("count") > 1100)
display(df2)

# COMMAND ----------

# DBTITLE 1,PySpark - Collect Set and List
df2=df.groupBy("paymentMethod").agg(F.collect_set("product"), F.collect_list("product"))
display(df2)

# COMMAND ----------

# DBTITLE 1,SQL - Collect Set and List
# MAGIC %sql
# MAGIC select 
# MAGIC   paymentMethod,
# MAGIC   collect_set(product),
# MAGIC   collect_list(product)
# MAGIC from samples.bakehouse.sales_transactions
# MAGIC group by paymentMethod

# COMMAND ----------

# DBTITLE 1,PySpark - Window Function - Row Number
from pyspark.sql.window import Window

window_spec = Window.partitionBy("product").orderBy(F.col("quantity").desc())

df2 = df.withColumn("row_number_over_product", F.row_number().over(window_spec))

df3=df2.select("product","customerID","quantity","row_number_over_product")

display(df3)

# COMMAND ----------

# DBTITLE 1,Filter Product With Highest Quantity
df4=df3.filter(df3["row_number_over_product"]==1)
display(df4)

# COMMAND ----------

# DBTITLE 1,PySpark - Window Function - Rank, Dense Rank
window_spec = Window.partitionBy("product").orderBy(F.col("quantity").desc())

df2 = df.withColumn("rank_over_product", F.rank().over(window_spec)) \
    .withColumn("dense_rank_over_product", F.dense_rank().over(window_spec)) 

df3 = df2.select(
    "product",
    "customerID",
    "quantity",
    "rank_over_product",
    "dense_rank_over_product"
)
display(df3)

# COMMAND ----------

# DBTITLE 1,SQL - Window Function - Row Number, Rank, Dense Rank
# MAGIC %sql
# MAGIC SELECT
# MAGIC   product,
# MAGIC   customerID,
# MAGIC   quantity,
# MAGIC   ROW_NUMBER() OVER (PARTITION BY product ORDER BY quantity DESC) AS row_number_over_product,
# MAGIC   RANK() OVER (PARTITION BY product ORDER BY quantity DESC) AS rank_over_product,
# MAGIC   DENSE_RANK() OVER (PARTITION BY product ORDER BY quantity DESC) AS dense_rank_over_product
# MAGIC FROM samples.bakehouse.sales_transactions
