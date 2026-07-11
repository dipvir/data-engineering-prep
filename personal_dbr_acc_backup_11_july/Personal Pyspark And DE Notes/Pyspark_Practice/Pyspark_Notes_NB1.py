# Databricks notebook source
print(type(spark))
print(type(sc))
# https://github.com/rangareddy

# required imports
from pyspark.sql.types import *
from pyspark.sql.functions import *

# COMMAND ----------

# MAGIC %md
# MAGIC ### Ways To Create DataFrames In PySpark

# COMMAND ----------

# DBTITLE 1,Create DataFrame from Python List of Tuples
data = [("Alice", 25), ("Bob", 30), ("Charlie", 29)]
columns = ["name", "age"]
df = spark.createDataFrame(data, columns)
display(df)

# COMMAND ----------

# DBTITLE 1,Create DataFrame from Python Dictionaries
data = [{"name": "Alice", "age": 25}, {"name": "Bob", "age": 30}]
df = spark.createDataFrame(data)
display(df)

# COMMAND ----------

# DBTITLE 1,Load DataFrame from CSV File
file_path = "/Volumes/dbacademy/default/sample_files/employee.csv"
df = spark.read.csv(file_path, header=True, inferSchema=True)
df.printSchema()
display(df)

# COMMAND ----------

# DBTITLE 1,Load DataFrame from Parquet
file_path = "/Volumes/dbacademy/default/sample_files/employees.parquet"
df = spark.read.parquet(file_path)
df.printSchema()
display(df)

# COMMAND ----------

# DBTITLE 1,Load DataFrame from JSON File
file_path = "/Volumes/dbacademy/default/sample_files/employee.json"
# Read JSON file
# multiline = true → tells Spark the JSON spans multiple lines (array or formatted JSON)
df = spark.read.option("multiline", "true").json(file_path)
df.printSchema()
display(df)

# COMMAND ----------

# DBTITLE 1,Create Empty DataFrame with Schema
schema = StructType([
    StructField("name", StringType(), True),
    StructField("age", IntegerType(), True)
])
df = spark.createDataFrame([], schema)
df.printSchema()
display(df)

# COMMAND ----------

# DBTITLE 1,Load DataFrame From MYSQL Database Table
# Force the serverless Spark session to pull the driver from Maven dynamically
spark.conf.set("spark.jars.packages", "mysql:mysql-connector-java:8.0.33")

# 2. Read the data from your local MySQL instance
df = spark.read.format("jdbc").options(
    url="jdbc:mysql://localhost:3306/store",  # Changed protocol & default port
    driver="com.mysql.cj.jdbc.Driver",                     # Changed to MySQL Driver class
    dbtable="customers",                                    # Your MySQL table name
    user="root",                                           # Your MySQL username (default is root)
    password="Iloveudip@123"                         # Your MySQL password
).load()
display(df)

# Code throwing error here locally working but not working on databricks.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Exploring DataFrames

# COMMAND ----------

# DBTITLE 1,Loading bank_additional_csv File With InferSchema
bank_additional_csv_df = spark.read.csv(
    "/Volumes/dbacademy/default/tutorials/bank-additional.csv",
    header=True,
    sep=";",
    inferSchema=True
)

bank_additional_csv_df.printSchema()
display(bank_additional_csv_df)

# COMMAND ----------

# DBTITLE 1,Loading bank_additional_csv File With Explicit Schema
schema = StructType(
    [
        StructField("age", IntegerType(), True),
        StructField("job", StringType(), True),
        StructField("marital", StringType(), True),
        StructField("education", StringType(), True),
        StructField("default", StringType(), True),
        StructField("housing", StringType(), True),
        StructField("loan", StringType(), True),
        StructField("contact", StringType(), True),
        StructField("month", StringType(), True),
        StructField("day_of_week", StringType(), True),
        StructField("duration", IntegerType(), True),
        StructField("campaign", IntegerType(), True),
        StructField("pdays", IntegerType(), True),
        StructField("previous", IntegerType(), True),
        StructField("poutcome", StringType(), True),
        StructField("emp_var_rate", DoubleType(), True),
        StructField("cons_price_idx", DoubleType(), True),
        StructField("cons_conf_idx", DoubleType(), True),
        StructField("euribor3m", DoubleType(), True),
        StructField("nr_employed", DoubleType(), True),
        StructField("y", StringType(), True),
    ]
)
bank_additional_csv_df = spark.read.csv(
    "/Volumes/dbacademy/default/tutorials/bank-additional.csv",
    header=True,
    sep=";",
    schema=schema,
)

bank_additional_csv_df = bank_additional_csv_df.withColumn(
    "job", when(col("job") == "unknown", None).otherwise(col("job"))
)

bank_additional_csv_df.printSchema()
display(bank_additional_csv_df)

# COMMAND ----------

# DBTITLE 1,Displaying Data, Inspecting Schema, Summary Statistics
# bank_additional_csv_df.show() # Displays the first 20 rows.
# bank_additional_csv_df.show(50)# Show more rows:
# bank_additional_csv_df.show(truncate=False) # Show full column values:

print(bank_additional_csv_df.head(), end="\n\n")
print(bank_additional_csv_df.head(3), end="\n\n")
bank_additional_csv_df.printSchema()
print(bank_additional_csv_df.take(3), end="\n\n")
print(bank_additional_csv_df.first() ,end = "\n\n")
print(bank_additional_csv_df.columns, end="\n\n")
print(bank_additional_csv_df.dtypes, end="\n\n")
print(bank_additional_csv_df.schema, end="\n\n")
print(bank_additional_csv_df.count(), end="\n\n")
display(bank_additional_csv_df.describe())
display(bank_additional_csv_df.summary())

# COMMAND ----------

# DBTITLE 1,Selecting Columns, Filtering Data, Sorting Data, Removing Duplicates, Distinct and Null Values
display(bank_additional_csv_df.select("age", "job").limit(5))
display(bank_additional_csv_df.select(col("age") + 5).limit(5))
display(bank_additional_csv_df.filter(col("age") > 80))
# display(bank_additional_csv_df.filter(bank_additional_csv_df.age > 80)) # alternate option to above loc.
# display(bank_additional_csv_df.where(col("age") > 80)) # alternate option to above loc.
# display(bank_additional_csv_df.where(bank_additional_csv_df.age > 80)) # alternate option to above loc.
display(bank_additional_csv_df.orderBy("age").limit(200))
display(bank_additional_csv_df.orderBy(col("age").desc()).limit(200))
display(bank_additional_csv_df.dropDuplicates())
display(bank_additional_csv_df.select("age").dropDuplicates())
display(bank_additional_csv_df.dropDuplicates(["age"]))
display(bank_additional_csv_df.select("job").distinct())
print(bank_additional_csv_df.select("age", "job").distinct().count())
display(bank_additional_csv_df.filter(col("job").isNull()))

# COMMAND ----------

# DBTITLE 1,Checking Metadata:-partitions, DF columns, explain(), toPandas()
# print("Number of Partitions:", bank_additional_csv_df.rdd.getNumPartitions()) # Doesnt work onserverless

# alternate approach
from pyspark.sql.functions import spark_partition_id
# display(bank_additional_csv_df.select(spark_partition_id()).distinct())
# Count the distinct partition IDs present in the actual DataFrame rows
num_partitions = bank_additional_csv_df.select(spark_partition_id()).distinct().count()
print("Number of Active Partitions:", num_partitions)

print("Number of Columns:", len(bank_additional_csv_df.columns))
# Gets Spark Execution Plan
bank_additional_csv_df.filter(bank_additional_csv_df.age > 25).explain(True)
# Converting to Pandas
pd_df = bank_additional_csv_df.toPandas()
print(pd_df)

# COMMAND ----------

# DBTITLE 1,Casting and Updating Column
display(bank_additional_csv_df.limit(10))
bank_additional_csv_df.printSchema()
bank_additional_csv_df = bank_additional_csv_df.withColumn("age", col("age").cast("float"))
bank_additional_csv_df.printSchema()
display(bank_additional_csv_df.withColumn("age", col("age") + lit(5)).limit(10))

# COMMAND ----------

# MAGIC %md
# MAGIC **Nested Schema (Struct, Array, Map)**
# MAGIC
# MAGIC Spark’s schema system supports complex nested types. These are especially common in JSON and semi‑structured data.
# MAGIC
# MAGIC Spark supports:
# MAGIC
# MAGIC - **Struct (nested objects)**
# MAGIC - **Array (list of values)**
# MAGIC - **Map (key-value pairs)**
# MAGIC
# MAGIC This is why Spark is powerful — it handles **complex data structures**.

# COMMAND ----------

# DBTITLE 1,Example — StructType (Nested Object)
from pyspark.sql.types import StructField, StructType, StringType, IntegerType
schema = StructType([
    StructField("name", StringType(), True),
    StructField("address", StructType([
        StructField("city", StringType(), True),
        StructField("pincode", IntegerType(), True)
    ]))
])
data = [("Alice", ("Delhi", 110001))]
df_ex_struct = spark.createDataFrame(data, schema)
display(df_ex_struct)
df_ex_struct.printSchema()

# COMMAND ----------

# DBTITLE 1,Example — ArrayType (Lists)
from pyspark.sql.types import ArrayType, StringType
schema = StructType([
    StructField("name", StringType(), True),
    StructField("skills", ArrayType(StringType()), True)
])
data = [("Megha", ["Python", "Spark", "AWS"])]
df_ex_array = spark.createDataFrame(data, schema)
df_ex_array.printSchema()
display(df_ex_array)

# COMMAND ----------

# DBTITLE 1,Example — MapType (Key-Value)
# 1. CRITICAL: We must import MapType!
from pyspark.sql.types import StructType, StructField, StringType, MapType 
# 2. SCHEMA: MapType requires TWO parameters: MapType(KeyType, ValueType)
schema = StructType([
    StructField("name", StringType(), True),
    StructField("skills_years", MapType(StringType(), StringType()), True) 
])
# 3. DATA: We must pass a Python DICTIONARY instead of a list
data = [("Megha", {"Python": "3 Years", "Spark": "2 Years", "AWS": "1 Year"})]
df_ex_map = spark.createDataFrame(data, schema)
df_ex_map.printSchema()
display(df_ex_map)

# COMMAND ----------

bank_additional_csv_df = bank_additional_csv_df.withColumnRenamed("job", "Occupation")
bank_additional_csv_df = bank_additional_csv_df.withColumn("duration_new", col("duration") + 10)
bank_additional_csv_df = bank_additional_csv_df.drop("nr_employed" ,"euribor3m")
display(bank_additional_csv_df.limit(4))

# Real-World Practical Examples: Combining column expressions with filters or actions:
display(bank_additional_csv_df.select("Occupation", col("age") + 1)) #increase age of all rows
bank_additional_csv_df = bank_additional_csv_df.filter(col("age") > 80)#filter old people
display(bank_additional_csv_df)
result = bank_additional_csv_df.collect() #convert entire data frame to python list
print(type(result) , len(result ), result[0] , type(result[0]) , result[0]["age"] ,sep = "\n")
