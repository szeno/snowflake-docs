# PIPES view

This Information Schema view displays a row for each pipe defined in the specified (or current) database.

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| PIPE\_CATALOG | VARCHAR | Database that the pipe belongs to |
| PIPE\_SCHEMA | VARCHAR | Schema that the pipe belongs to |
| PIPE\_NAME | VARCHAR | Name of the pipe |
| PIPE\_OWNER | VARCHAR | Name of the role that owns the pipe |
| DEFINITION | VARCHAR | COPY statement used to load data from queued files into a Snowflake table. |
| IS\_AUTOINGEST\_ENABLED | VARCHAR | Whether AUTO-INGEST is enabled for the pipe. Represents future functionality. |
| NOTIFICATION\_CHANNEL\_NAME | VARCHAR | Amazon Resource Name of the Amazon SQS queue for the stage named in the DEFINITION column. Represents future functionality. |
| CREATED | TIMESTAMP\_LTZ | Creation time of the pipe |
| LAST\_ALTERED | TIMESTAMP\_LTZ | Date and time the object was last altered by a DML, DDL, or background metadata operation. See [Usage Notes](#usage-notes). |
| COMMENT | VARCHAR | Comment for this pipe |
| PATTERN | VARCHAR | PATTERN copy option value in the [COPY INTO <table>](/sql-reference/sql/copy-into-table) statement in the pipe definition, if the copy option was specified. |

Expand

Show lessSee more

## Usage notes

- Returns results only for the pipe owner (i.e. the role with the OWNERSHIP privilege on the pipe) or a role with the MONITOR privilege on
  the pipe.
- To determine the current status of a pipe, query the [SYSTEM$PIPE\_STATUS](/sql-reference/functions/system_pipe_status) function.
- The LAST\_ALTERED column is updated when the following operations are performed on an object:

  - DDL operations.
  - DML operations (for tables only). This column is updated even when no rows are affected by the DML statement.
  - Background maintenance operations on metadata performed by Snowflake.
