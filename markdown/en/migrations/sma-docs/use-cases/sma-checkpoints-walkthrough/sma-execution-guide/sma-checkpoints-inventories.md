# Snowpark Migration Accelerator: SMA-Checkpoints inventories

The SMA-Checkpoints feature introduces two new inventory files: `CheckpointsInventory.csv` and `DataFramesInventory.csv`. These files are generated regardless of whether the feature is enabled.

[![SMA-Checkpoints feature related inventories.](/static/images/migrations/sma-assets/image(571).png)](/static/images/migrations/sma-assets/image(571).png)

**Checkpoints Inventory Sample**

Copy code

```
Name: sample$BBVOC7$df1$1
FileId: sample.py
CellId: 0
Line: 6
Column: 1
Type: Collection
DataFrameName: df1
Location: 1
Enabled: True
Mode: Schema
Sample: 1
EntryPoint: sample.py
ExecutionId: 00000000-0000-0000-0000-000000000000
```

**DataFrames Inventory Sample**

Copy code

```
FullName: TestingCheckpoints.sample.df1
Name: df1
FileId: sample.py
CellId: 0
Line: 6
Column: 1
AssignmentNumber: 1
RelevantFunction: pyspark.sql.session.SparkSession.createDataFrame
RelatedDataFrames:
EntryPoints: sample.py
ExecutionId: 00000000-0000-0000-0000-000000000000
```
