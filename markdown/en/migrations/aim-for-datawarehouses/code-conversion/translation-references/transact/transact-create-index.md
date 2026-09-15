# SQL Server-Azure Synapse - CREATE INDEX

Translation reference to convert CREATE INDEX statement to Snowflake

Applies to

- SQL Server
- Azure Synapse Analytics

Warning

Currently, ***Create Index*** statement is not being converted but it is being parsed. Also, if your source code has Create `index` statements, these are going to be accounted for in the ***Assessment Report.***

**Example of Create Index**

## SQLServer

Copy code

```
CREATE INDEX my_index_name ON my_table (column1, column2);

CREATE TABLE table_1(
   date_time DATETIME,
   INDEX ix_PatientBaseEpisodes_Version NONCLUSTERED (VersionStamp)
) ON [PRIMARY]
```

## Snowflake

Copy code

```
 ----** SSC-FDM-0021 - CREATE INDEX IS NOT SUPPORTED BY SNOWFLAKE **
--CREATE INDEX my_index_name ON my_table (column1, column2)

CREATE OR REPLACE TABLE table_1 (
  date_time TIMESTAMP_NTZ(3)
--                            ,
--  --** SSC-FDM-0021 - CREATE INDEX IS NOT SUPPORTED BY SNOWFLAKE **
--   INDEX ix_PatientBaseEpisodes_Version NONCLUSTERED (VersionStamp)
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "transact",  "convertedOn": "06/06/2025",  "domain": "no-domain-provided" }}'
;
```

Note

Due to architectural reasons, Snowflake does not support indexes so, all the code related to the creation of indexes will be removed. Snowflake automatically creates micro-partitions for every table that help speed up the performance of DML operations, the user does not have to worry about creating or managing these micro-partitions.

Usually, this is enough to have a very good query performance however, there are ways to improve it by creating data clustering keys. [Snowflake’s official page](https://docs.snowflake.com/en/user-guide/tables-clustering-micropartitions.html) provides more information about micro-partitions and data clustering.
