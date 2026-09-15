# Aug 20, 2025: Distributed processing in Snowflake ML: Many Model Training and Distributed Partition Function

Snowflake ML now supports distributed processing capabilities for training multiple models and processing data across partitions.

You can use Many Model Training (MMT) to train multiple machine learning models efficiently across data partitions. MMT partitions your Snowpark DataFrame by a column that you specify and trains separate models on each partition in parallel.

You can use the Distributed Partition Function (DPF) to process data in parallel across one or more nodes in a compute pool. DPF partitions your Snowpark DataFrame by a column that you specify and executes your Python function on each partition in parallel.

Both features help you handle infrastructure complexity and scale automatically.

For more information, see [Train models across data partitions](/developer-guide/snowflake-ml/train-models-across-partitions) and [Process data with custom logic across partitions](/developer-guide/snowflake-ml/process-data-across-partitions).
