# Databricks notebook source
# MAGIC %md
# MAGIC ### THE EVOLUTION OF BIG DATA ARCHITECTURE
# MAGIC ### CHAPTER 1: THE GOOGLE ORIGINS & INTERNET EXPLOSION (2003 - 2004)
# MAGIC #### 🚨 The Physical Bottleneck: Vertical vs. Horizontal Scaling
# MAGIC In the early 2000s, Google faced a crisis: the World Wide Web was expanding exponentially, and the volume of incoming data outgrew the storage capacity and processing limits of single computing units. 
# MAGIC * **Vertical Scaling (Scaling UP):** Buying a larger, faster, and more expensive enterprise server. Google hit a physical wall here—manufacturers simply could not build components fast enough or large enough to host a copy of the entire internet.
# MAGIC * **Horizontal Scaling (Scaling OUT):** Connecting thousands of cheap, standard, consumer-grade computers ("commodity hardware") together across a local network to act as a single cooperative machine. Google chose this path.
# MAGIC
# MAGIC #### 🛠️ The Core Architectural Solutions
# MAGIC Because cheap computers crash and fail frequently, Google had to design software that was inherently **fault-tolerant**. They solved this by publishing two historic research papers:
# MAGIC
# MAGIC ![image_1780131604660.png](./image_1780131604660.png "image_1780131604660.png")
# MAGIC
# MAGIC #### A. GFS (Google File System) — The Storage Blueprint (2003)
# MAGIC * **The Mechanism:** GFS takes a massive dataset file (e.g., a 10 Terabyte search log) and cuts it up into uniform blocks (typically 64MB or 128MB). It distributes these individual blocks across separate storage units in the cluster network.
# MAGIC * **Fault Tolerance via Replication:** GFS automatically makes a minimum of **3 copies (replicas)** of every single data block and saves them on completely separate hardware racks. If a hard drive chokes, catches fire, or disconnects, the central controller instantly redirects traffic to a backup replica without the user ever noticing a delay.
# MAGIC
# MAGIC #### B. MapReduce (MR) — The Processing Blueprint (2004)
# MAGIC Before MapReduce, analyzing data required pulling files over the network wire into a central processing unit—a tactic that completely chokes network bandwidth. MapReduce flipped this model by **bringing the computation code directly to where the data physically sits.**
# MAGIC * **The Map Phase:** The master node sends the script down to all worker computers simultaneously. Each worker processes its own local block of data in parallel, producing temporary, intermediate key-value results.
# MAGIC * **The Shuffle & Sort Phase:** The system organizes the intermediate results, routing identical keys from different machines to the same processing bucket.
# MAGIC * **The Reduce Phase:** The workers aggregate, sum, or summarize the shuffled values into a single, clean final output dataset.
# MAGIC
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### CHAPTER 2: THE OPEN-SOURCE REBIRTH: THE HADOOP ECOSYSTEM
# MAGIC Google utilized GFS and MapReduce to dominate the search landscape but kept their internal proprietary source code locked away. In response, open-source engineers Doug Cutting and Mike Cafarella used Google's theoretical papers as an exact blueprint to build a free, public clone named **Hadoop**.
# MAGIC
# MAGIC ![image_1780131666672.png](./image_1780131666672.png "image_1780131666672.png")
# MAGIC ![image_1780131895549.png](./image_1780131895549.png "image_1780131895549.png")
# MAGIC ![image_1780131885892.png](./image_1780131885892.png "image_1780131885892.png")
# MAGIC
# MAGIC Hadoop split Google's architecture into two core open-source frameworks:
# MAGIC
# MAGIC | Google Layer (Proprietary) | Hadoop Layer (Open-Source Clone) | Operational Responsibility |
# MAGIC | :--- | :--- | :--- |
# MAGIC | **GFS** | **HDFS** (Hadoop Distributed File System) | **The Storage Master:** Splitting, scattering, and replicating physical file blocks across cluster hard drives. |
# MAGIC | **MapReduce** | **MapReduce (YARN Engine)** | **The Execution Engine:** Scheduling, tracking, and executing parallel Map and Reduce code sequences across nodes. |
# MAGIC
# MAGIC #### 🛑 Hadoop's Fatal Architectural Bottleneck: Disk I/O
# MAGIC While Hadoop was a massive success, its execution architecture had a severe design flaw: **it was completely bound to physical hard drives (Disk I/O).**
# MAGIC * MapReduce cannot hold moving data in active memory. When the **Map Phase** finishes, the worker must write its entire intermediate result down onto a local physical hard drive.
# MAGIC * The system must then read that data back off the hard drive, send it over the network wires for the Shuffle phase, run the **Reduce Phase**, and write the final result back down to the hard drive once more.
# MAGIC * Because reading and writing to physical disk storage is orders of magnitude slower than reading from RAM, Hadoop pipelines spent more time waiting for hard drives to spin than actually computing data.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### CHAPTER 3: THE BIRTH & DEMOCRATIZATION OF APACHE HIVE
# MAGIC When Hadoop first arrived, it was a massive breakthrough for storing petabytes of data via HDFS. However, running data transformations or calculating metrics was an absolute nightmare for average data teams.
# MAGIC * **The Language Wall:** Early Hadoop MapReduce was written strictly in **Java**. 
# MAGIC * **The Code Complexity:** To run a simple data aggregation (like a basic `COUNT` or `SUM` group-by query), a data engineer had to write over 50 to 100 lines of complex, low-level Java boilerplate code just to compile a single MapReduce job.
# MAGIC * **The Talent Gap:** Most data analysts and business teams already knew **SQL** perfectly, but they did not know Java. This meant data locked inside Hadoop was inaccessible to the people who needed it most.
# MAGIC
# MAGIC To bridge this gap, Facebook's engineering team invented **Apache Hive** to act as a translation layer directly on top of the Hadoop platform.
# MAGIC
# MAGIC
# MAGIC
# MAGIC #### 🛠️ How Hive Works Under the Hood
# MAGIC Hive allowed engineers to write standard, familiar SQL queries (called **HiveQL**). 
# MAGIC 1. **The Query:** You write a clean SQL statement: `SELECT country, COUNT(*) FROM users GROUP BY country;`
# MAGIC 2. **The Translation:** The Hive Engine takes that SQL statement, compiles it, and automatically translates it into complex **Java MapReduce code** behind the scenes.
# MAGIC 3. **The Execution:** Hive sends that generated Java code down to the Hadoop cluster to process the data stored in HDFS.
# MAGIC
# MAGIC ### 🌟 Core Capabilities Hive Offered on the Hadoop Platform:
# MAGIC * Create **Databases**
# MAGIC * Create **Tables**
# MAGIC * Create **Views**
# MAGIC * Run **SQL Queries**
# MAGIC * Bringing together Hadoop as a platform and Hive as a database became very popular because it **democratized** big data access.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### CHAPTER 4: THE LIMITATIONS OF THE HADOOP + HIVE COMBINATION
# MAGIC While combining Hadoop and Hive was widely adopted, as companies collected more data, this specific architecture left a massive scope for improvement due to five core limitations:
# MAGIC
# MAGIC * **🛑 1. Performance (The Speed Disaster):** Hive SQL queries performed significantly slower than traditional relational database (RDBMS) SQL queries. Why? Because Hive was still ultimately generating Hadoop MapReduce jobs under the hood. It was forced to constantly read and write intermediate data to slow physical hard drives (Disk I/O), killing query performance.
# MAGIC * **🛑 2. Ease of Development (The Black Box Problem):** Writing raw MapReduce programs was incredibly difficult, and debugging complex data pipelines was a nightmare. If a Hive query failed or ran slowly, engineers had to dig through thousands of lines of compiled Java logs to find out where the processing logic broke.
# MAGIC * **🛑 3. Language Support:** MapReduce processing logic was primarily available and confined to **JAVA**. It completely lacked native flexibility for engineers who wanted to use other language ecosystems like Python or R for advanced data work.
# MAGIC * **🛑 4. Storage Costs:** Maintaining dedicated, on-premises physical Hadoop cluster infrastructures became dramatically more expensive and rigid compared to modern public cloud object storage models.
# MAGIC * **🛑 5. Resource Management:** Hadoop was deeply tied to its own engine layer, providing **only YARN container support**. It was entirely unable to use other modern container orchestration systems like **Mesos, Docker, or Kubernetes**.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### CHAPTER 5: THE NEXT GENERATION — THE APACHE SPARK REVOLUTION
# MAGIC Because of the gaps left by the Hadoop and Hive setup, **Apache Spark** came into existence to fix these issues completely.
# MAGIC
# MAGIC
# MAGIC
# MAGIC #### ⚡ The Core Breakthrough: In-Memory Processing
# MAGIC Instead of dropping data down to hard drives between processing stages, Apache Spark loads data fragments directly into the **RAM memory** of the cluster workers. It keeps the data alive in memory across the entire duration of your transformation pipeline.
# MAGIC * **The Performance Jump:** By eliminating physical disk read/write cycles, Apache Spark can process complex data pipelines **up to 10 to 100 times faster** than traditional Hadoop MapReduce or Hive.
# MAGIC
# MAGIC #### 🤝 The Modern Data Engineering Reality
# MAGIC * **Spark replaces the Processing Layer:** Data engineers almost never write old-fashioned MapReduce or raw Hive execution steps anymore. We use Spark (or PySpark) to handle all computational work because it is blazing fast.
# MAGIC * **Spark still leverages Distributed Storage:** Spark does not have a permanent native storage layer. It relies entirely on distributed storage systems to hold its raw files. It plugs seamlessly into **Hadoop's HDFS**, or modern cloud equivalents like **Azure Data Lake Storage Gen2 (ADLS Gen2)**, AWS S3, or Databricks' own **DBFS/Delta Lake** frameworks.
# MAGIC
# MAGIC ### CHAPTER 6: THE APACHE SPARK ECOSYSTEM & COMPONENTS
# MAGIC #### ⚡ What is Apache Spark?
# MAGIC Apache Spark is a unified, open-source analytics engine explicitly designed for large-scale distributed data processing and machine learning. It is an open-source cluster computing framework which handles both batch data and streaming data. 
# MAGIC
# MAGIC Built directly on top of the theoretical lessons learned from Hadoop MapReduce, Spark provides **in-memory storage** for intermediate computations whereas alternative approaches like Hadoop's MapReduce write data to and from computer hard drives. By eliminating physical disk read/write cycles, Apache Spark processes data much faster than other alternatives.
# MAGIC
# MAGIC #### 📜 History of Spark:
# MAGIC * **2009:** Initiated by Matei Zaharia at UC Berkeley's AMPLab.
# MAGIC * **2010:** Released open-source to the global developer community under a BSD license.
# MAGIC * **2013:** Project was acquired by the Apache Software Foundation.
# MAGIC * **2014:** Emerged as a Top-Level, flagship Apache Project.
# MAGIC
# MAGIC #### 🌟 Key Features of Apache Spark:
# MAGIC * **Fault Tolerance:** Automatically recomputes missing or failed data fragments using lineage chains if a worker node crashes mid-job.
# MAGIC * **Dynamic in Nature:** Dynamically adapts resource utilization based on workload requirements.
# MAGIC * **Lazy Evaluation:** Postpones execution until an action is explicitly called, allowing Spark to optimize the full query execution plan.
# MAGIC * **Real-Time Stream Processing:** Handles high-velocity, continuous streaming data pipelines natively.
# MAGIC * **Reusability:** Allows you to reuse code across batch processing, interactive queries, and streaming apps.
# MAGIC * **Speed:** Delivers blazing fast data execution by operating directly in memory.
# MAGIC * **Advanced Analytics:** Supports sophisticated analytical processing beyond standard SQL aggregates.
# MAGIC * **In-Memory Computing:** Eliminates physical disk bottlenecks by caching calculations directly inside worker RAM nodes.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### 🎨 The Architectural Blueprint of Spark Ecosystem
# MAGIC Apache Spark was intentionally designed to be **decoupled**. It focuses entirely on execution logic and memory processing, deliberately leaving permanent storage and base infrastructure management to specialized third-party technologies.
# MAGIC
# MAGIC The entire Apache Spark ecosystem is divided into three functional architectural tiers as indicated below:
# MAGIC
# MAGIC #### 🧱 1. Storage and Cluster Manager (The Foundation)
# MAGIC Apache Spark is a distributed processing engine. However, it doesn't come with an inbuilt cluster resource manager and a distributed storage system. 
# MAGIC
# MAGIC There is a good reason behind that design decision. Apache Spark tried to decouple the functionality of a cluster resource manager, distributed storage, and a distributed computing engine from the beginning. This design allows us to use Apache Spark with any compatible cluster manager and storage solution. Hence, the storage and the cluster manager are part of the ecosystem, however, they are not part of Apache Spark. You can plugin a cluster manager and a storage system of your choice.
# MAGIC
# MAGIC * **The Cluster Manager Layer:** Schedulers that manage and allocate resources across your server hardware. Sourced via options like **Standalone**, **Hadoop YARN**, **Apache Mesos**, or **Kubernetes**.
# MAGIC * **The Storage Layer:** Systems where the raw bytes sit at rest. Sourced via options like **Hadoop HDFS**, **Amazon S3**, **Azure Data Lake Storage (ADLS)**, or **Apache Cassandra**.
# MAGIC
# MAGIC #### ⚙️ 2. Spark Core
# MAGIC Apache Spark core contains two main components:
# MAGIC 1. **Spark Compute Engine**
# MAGIC 2. **Spark Core APIs**
# MAGIC
# MAGIC #### Spark Compute Engine:
# MAGIC The low-level background coordinator responsible for:
# MAGIC * Memory management.
# MAGIC * Task scheduling and job tracking.
# MAGIC * Fault recovery.
# MAGIC * Crucially, communication with your chosen cluster manager and storage system.
# MAGIC To give the user a smooth experience, the Spark compute engine manages and executes our Spark jobs. Simply submit your job to Spark, and the core of Spark does the rest.
# MAGIC
# MAGIC #### Spark Core APIs:
# MAGIC These core APIs deliver distributed processing capabilities and are written and made available in four core languages: **Scala, Python, Java, and R**. They are split into two computational layers:
# MAGIC * **Structured APIs:** Consist of **DataFrames** and **DataSets**. They are explicitly designed and heavily optimized to work with structured, tabular data.
# MAGIC * **Unstructured APIs:** The lower-level raw APIs including **RDDs** (Resilient Distributed Datasets), **Accumulators**, and **Broadcast variables**.
# MAGIC
# MAGIC #### 📚 3. Set of Libraries
# MAGIC Apache Spark has different sets of libraries and packages that make it a powerful big data processing framework. These libraries provide different functionalities for data processing, analysis, and machine learning tasks. They offer us APIs, DSLs, and algorithms in multiple languages and directly depend on Spark Core APIs to achieve distributed processing.
# MAGIC
# MAGIC * **📊 Spark SQL:** Allows you to use standard SQL queries for structured data processing and DataFrame manipulation.
# MAGIC * **🌊 Structured Streaming:** Helps you to seamlessly consume, process, and analyze continuous live data streams.
# MAGIC * **🤖 MLlib (Machine Learning):** A high-performance machine learning library that delivers high-quality, distributed algorithmic frameworks.
# MAGIC * **🕸️ GraphX:** Comes packed with a library of typical graph processing structures and network relation algorithms.

# COMMAND ----------

# MAGIC %md
# MAGIC ### What is a Data Lake, why was it created, and what are its core limitations?
# MAGIC
# MAGIC #### 📌 1. The Core Definition
# MAGIC
# MAGIC A **Data Lake** is a centralized, highly scalable repository designed to store vast amounts of raw data in its **native, unformatted state**. Unlike a traditional Data Warehouse that strictly requires structured relational tables, a Data Lake can ingest and hold data regardless of its variety.
# MAGIC
# MAGIC * **Storage Layer Type:** Object Storage (e.g., Azure ADLS Gen2, AWS S3, Google Cloud Storage).
# MAGIC * **Data Typologies Supported:**
# MAGIC     * **Structured:** `.csv`, `.tsv`, database dumps.
# MAGIC     * **Semi-Structured:** `.json`, `.xml`, `.avro`, `.parquet`.
# MAGIC     * **Unstructured:** Images, PDFs, audio files, video streams, log transcripts.
# MAGIC
# MAGIC
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### 🚀 2. The Shift: Traditional Data Warehouse vs. Data Lake
# MAGIC
# MAGIC To understand why companies migrated to Data Lakes, you have to understand the operational shift from **Schema-on-Write** to **Schema-on-Read**:
# MAGIC
# MAGIC | Feature | Traditional Data Warehouse (RDBMS) | Modern Data Lake (Object Storage) |
# MAGIC | --- | --- | --- |
# MAGIC | **Design Philosophy** | **Schema-on-Write:** You must define the table structure and data types *before* you can load any data into it. | **Schema-on-Read:** You dump raw data immediately. The structure is applied only when a processing engine (like Spark) reads it. |
# MAGIC | **Processing Paradigm** | **ETL** (Extract, Transform, Load) | **ELT** (Extract, Load, Transform) |
# MAGIC | **Cost Scale** | **Expensive:** Highly specialized compute and storage are tightly coupled together. | **Incredibly Cheap:** Decoupled architecture. Storage is separated from compute, costing pennies per gigabyte. |
# MAGIC | **Data Flexibility** | Relational tables only (Strict structures). | Highly flexible (Raw logs, binary files, JSON, Parquet side-by-side). |
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### 💥 3. The Critical Flaws of a Traditional Data Lake (The Nightmare Scenarios)
# MAGIC
# MAGIC While Data Lakes completely solved the problem of cheap, infinite storage, they introduced massive operational engineering problems. In production, a raw Data Lake lacks an enterprise governance layer, which leads to these core issues:
# MAGIC
# MAGIC ##### **A. The "Data Swamp" Phenomenon**
# MAGIC
# MAGIC Because anyone can dump files into a data lake without structural validation, directories quickly turn into a chaotic mess of messy schemas, corrupted files, and duplicate directories. Without indexing or a centralized catalog, finding trustworthy data becomes impossible.
# MAGIC
# MAGIC ##### **B. Lack of ACID Transaction Support**
# MAGIC
# MAGIC Raw object storage systems (like S3 or ADLS Gen2) do not natively understand database transactions. They only understand file-level operations (Create, Read, Update, Delete). This causes massive production synchronization bugs:
# MAGIC
# MAGIC * **Dirty Reads:** If a PySpark job is actively writing a massive batch of 500 partition files to a folder, and a business analyst runs a reporting query at the exact same time, the report will read a partial, corrupted, half-written state of the data.
# MAGIC * **No Rollbacks:** If your data pipeline fails 90% of the way through a massive write operation due to a cluster timeout, the data lake is left in a corrupted state. There is no `ROLLBACK` command to undo the partial files already written to storage.
# MAGIC
# MAGIC ##### **C. The "Small Files" Problem**
# MAGIC
# MAGIC Streaming engines or frequent micro-batch jobs write thousands of tiny, separate files (kilobytes each) into storage directories over time. Because object stores struggle with metadata overhead when opening and closing millions of individual files, read operations stall out completely, slowing down your Spark processing cluster to a crawl.
# MAGIC
# MAGIC ##### **D. Lack of Schema Enforcement and Evolution**
# MAGIC
# MAGIC If an upstream source suddenly changes a column data type from an `Integer` to a `String` inside a new JSON payload, the raw Data Lake will blindly accept it. The next time a downstream application attempts to read that historical directory, the Spark schema validation will fail and completely crash your production pipelines.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### 💡 The Key Takeaway for your Notes.
# MAGIC
# MAGIC  Data Lakes perfectly solved the problem of **cheap storage flexibility**, but they completely failed at **data reliability and transaction safety**. This exact structural gap is why Databricks created **Delta Lake**—an open-source storage layer that sits directly *on top* of your existing Data Lake storage to bring ACID reliability, schema validation, and database performance directly to your raw object files.
# MAGIC
# MAGIC ---

# COMMAND ----------

# MAGIC %md
# MAGIC ### What are ACID properties in Data Engineering, and what happens to a Data Lake if they fail?
# MAGIC
# MAGIC #### 📌 The Core Definitions (ACID)
# MAGIC
# MAGIC * **Atomicity:** "All or nothing." If a pipeline write operation fails halfway through, the entire transaction is rolled back so no partial or corrupted data is left behind.
# MAGIC * **Consistency:** Data must always move from one valid state to another, strictly adhering to defined rules, schemas, and constraints.
# MAGIC * **Isolation:** Concurrent transactions cannot interfere with one another. Multiple pipelines or users can read and write to the same data space simultaneously without seeing partial states.
# MAGIC * **Durability:** Once a transaction is successfully committed, the data is permanently written to non-volatile storage (disk) and will survive any subsequent cluster or system crashes.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### 🎬 Production Example Scenario: Daily Sales Ingestion Pipeline
# MAGIC
# MAGIC Imagine a daily PySpark ETL job that updates a massive corporate `sales_data` folder stored in your Data Lake (**ADLS Gen2**).
# MAGIC
# MAGIC * The job reads raw files, processes them, and attempts to write **100 new partition files** (Parquet) into the main folder.
# MAGIC * At the exact same time, a financial analyst is running an automated PowerBI dashboard query against that very same `sales_data` folder to generate a daily revenue report.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### 💥 The Nightmare: How a Raw Data Lake Fails ACID
# MAGIC
# MAGIC If you are using a traditional, raw Data Lake without a storage layer like Delta Lake, look at how the lack of ACID properties breaks your data reliability:
# MAGIC
# MAGIC ##### **1. Atomicity Failure (The "Half-Baked" Write)**
# MAGIC
# MAGIC * **What happens:** The PySpark job successfully writes 60 out of the 100 new partition files, but suddenly the Spark cluster hits a spot instance termination or out-of-memory error and crashes.
# MAGIC * **The Result:** Because raw object storage (S3/ADLS) does not have Atomicity, those 60 files stay in the directory permanently. Your data lake is now left in a corrupted, semi-updated state with no native way to roll them back automatically.
# MAGIC
# MAGIC ##### **2. Isolation Failure (The "Dirty Read")**
# MAGIC
# MAGIC * **What happens:** While the PySpark job is actively writing those 100 new partition files, the financial analyst's PowerBI report kicks off its read operation.
# MAGIC * **The Result:** Because there is no Isolation layer, the report reads the first 40 files that were successfully written, completely misses the remaining 60 files still in flight, and calculates completely incorrect, incomplete financial numbers for the company.
# MAGIC
# MAGIC ##### **3. Consistency Failure (The Schema Corruption)**
# MAGIC
# MAGIC * **What happens:** An upstream software update accidentally changes the data type of the `amount` column from a `Decimal` to a `String` inside a few of the files being ingested.
# MAGIC * **The Result:** The raw Data Lake blindly accepts the mismatched files. The next day, when your downstream aggregate jobs try to mathematically sum up the `amount` column, they crash with a type-mismatch exception, breaking your production analytics.
# MAGIC
# MAGIC ##### **4. Durability Failure (The Phantom Acknowledgement)**
# MAGIC
# MAGIC * **What happens:** The distributed storage engine acknowledges to Spark that a file batch write is "successful," but a massive cloud-provider hardware failure or metadata sync drop happens at the storage tier milliseconds later before the changes are fully flushed out across copies.
# MAGIC * **The Result:** Because raw, legacy network file layers don't enforce absolute write-ahead logs, the data can vanish or become unreadable. Your pipeline assumes the data is safely landed, but downstream systems hit missing file exceptions.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### 💡 Why Delta Lake is the Solution (The Complete Picture)
# MAGIC
# MAGIC > **Notebook Note:** This is exactly why Delta Lake is called an **ACID Storage Layer**. It sits as an absolute truth boundary over your raw Parquet files by utilizing a centralized, JSON-backed **Transaction Log (`_delta_log/`)**.
# MAGIC > * **Atomicity:** Until all 100 files are successfully written, the transaction log doesn't append the new JSON commit file. If a crash occurs at file 99, the log ignores all 99 files completely. It’s "all or nothing."
# MAGIC > * **Isolation:** Readers (like PowerBI) are strictly isolated to reading only the paths explicitly committed in the last valid transaction log file. They completely ignore any raw Parquet files actively being streamed or dumped in flight.
# MAGIC > * **Consistency:** Delta Lake implements **Schema Enforcement**. If an upstream system tries to append a `String` into a `Decimal` column, Delta intercepts the write *before* it touches disk and instantly kills the Spark job, protecting your lakehouse from schema corruption.
# MAGIC > * **Durability:** Every commit is written as an `atomic(All-or-Nothing)` transaction directly to the cloud storage log directory (`_delta_log/000000.json`). Because cloud object stores (like ADLS Gen2) are highly replicated, once that JSON log file commits, the transaction state is permanently durable and guaranteed to survive any cluster drop.
# MAGIC
# MAGIC ---
