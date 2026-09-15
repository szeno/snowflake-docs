# November 15, 2024 — Apache Iceberg™ tables: Efficient bulk loading, continuous ingestion, and data streaming — *General Availability*

With this release, Snowflake is pleased to announce the general availability of the following features,
which support efficient bulk loading, continuous ingestion, and data streaming into Snowflake-managed Iceberg tables.

You can now use the same core Snowflake ingestion features like COPY INTO <table>, Snowpipe, and Snowpipe Streaming, to
load data into both standard Snowflake tables and Iceberg tables.

For more information, see [Load data into Apache Iceberg™ tables](/user-guide/tables-iceberg-load).

## COPY INTO <table> and Snowpipe continuous file ingestion

You can use the following `LOAD_MODE` options with the [COPY INTO <table>](/sql-reference/sql/copy-into-table) command
and [Snowpipe automated loading](/user-guide/data-load-snowpipe-auto) to load data from files into a Snowflake-managed Iceberg table:

- `FULL_INGEST`: Loads data from any supported file format, converts to validated Iceberg-compatible Parquet,
  and optionally lets you transform or filter the data before loading.
- `ADD_FILES_COPY`: Loads data from Iceberg-compatible Parquet data files by performing a server-side copy of the files
  into the table’s base location and fast registering the files to the table.

## Snowpipe Streaming

With Snowflake Ingest SDK versions 3.0.0 and later, Snowpipe Streaming can stream rows into Snowflake-managed Iceberg tables.
To enable this feature, set the property *ENABLE\_ICEBERG\_STREAMING=true* in the *profile.json* file.

For more information, see [Load data into Apache Iceberg™ tables](/user-guide/tables-iceberg-load).
