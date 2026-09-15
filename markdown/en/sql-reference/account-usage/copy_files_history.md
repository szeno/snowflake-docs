Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# COPY\_FILES\_HISTORY view

This Account Usage view includes information about compute credit usage, number of bytes copied, and number of files copied for the
following operations:

- Using [COPY FILES](/sql-reference/sql/copy-files) to copy files from a source stage to an output stage.
- Cloning named internal stages.

See also:
:   [COPY FILES](/sql-reference/sql/copy-files) , [CREATE <object> … CLONE](/sql-reference/sql/create-clone)

## Columns

| Column name | Data type | Description |
| --- | --- | --- |
| DATABASE\_ID | NUMBER | ID of the database from which the files are copied. You can map this to the ENTITY\_ID in the [METERING\_HISTORY view](/sql-reference/account-usage/metering_history) view. |
| DATABASE\_NAME | VARCHAR | Name of the database from which the staged files are copied. |
| SUB\_SERVICE\_TYPE | VARCHAR | Type of service that is copying files, which can be one of the following:   - `COPY STAGE FILES`: See [COPY FILES](/sql-reference/sql/copy-files). - `SCHEMA CLONE`: See [CREATE <object> … CLONE](/sql-reference/sql/create-clone). - `DATABASE CLONE`: See [CREATE <object> … CLONE](/sql-reference/sql/create-clone). |
| JOB\_ROOT\_ENTITY\_ID | NUMBER | Entity ID for the root job; varies by SUB\_SERVICE\_TYPE. For COPY STAGE FILES, indicates the ID of the stage from which files are copied. For SCHEMA CLONE, indicates the schema ID. For DATABASE CLONE, indicates the database ID. |
| START\_TIME | TIMESTAMP\_LTZ | The date and beginning of the hour (in the local time zone) in which the copy operation took place. |
| END\_TIME | TIMESTAMP\_LTZ | The date and end of the hour (in the local time zone) in which the copy operation took place. |
| CREDITS\_USED | NUMBER | Number of compute credits used by warehouses and serverless compute resources between the START\_TIME and END\_TIME. |
| BYTES\_COPIED | NUMBER | Number of bytes copied from the root entity (stage, schema, or database) between the START\_TIME and END\_TIME. |
| FILES\_COPIED | NUMBER | Number of files copied from the root entity (stage, schema, or database) between the START\_TIME and END\_TIME. |

Expand

Show lessSee more
