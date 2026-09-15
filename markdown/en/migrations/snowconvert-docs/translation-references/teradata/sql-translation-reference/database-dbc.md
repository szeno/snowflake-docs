# Teradata - Database DBC

Equivalents for DBC objects and columns

Note

The DBC database contains critical system tables that define the user databases in the Analytics Database / Teradata Database. In the next segments, you can see the **supported** objects and columns of DBC database, the ones missing are **not supported** yet.

## DBC database

| Teradata | Snowflake | Notes |
| --- | --- | --- |
| DBC | INFORMATION\_SCHEMA |  |

Expand

Show lessSee more

> See [DBC database](https://docs.teradata.com/r/Teradata-DSA-User-Guide/November-2022/Database-DBC-Info/Database-DBC)

## DBC tables

| Teradata | Snowflake | Notes |
| --- | --- | --- |
| COLUMNS | COLUMNS |  |
| COLUMNSV | COLUMNS |  |
| DATABASES | DATABASES |  |
| DBQLOGTBL | TABLE(INFORMATION\_SCHEMA.QUERY\_HISTORY()) |  |
| TABLES | TABLES |  |

Expand

Show lessSee more

## DBC columns

| Teradata | Snowflake | Notes |
| --- | --- | --- |
| ALLRIGHTS | APPLICABLE\_ROLES |  |
| COLUMNNAME | COLUMN\_NAME |  |
| COLUMNUDTNAME | UDT\_NAME |  |
| COMMENT\_STRING | COMMENT |  |
| CREATETIMESTAMP | CREATED |  |
| COLUMNTYPE | DATA\_TYPE |  |
| COLUMNLENGTH | CHARACTER\_MAXIMUM\_LENGTH |  |
| CONSTRAINTNAME | CONSTRAINT\_NAME |  |
| CONSTRAINTTEXT | CONSTRAINT\_TYPE |  |
| DATABASENAME | TABLE\_SCHEMA |  |
| FINALWDNAME | SESSION\_ID |  |
| FIRSTSTEPTIME | DATEADD(MILLISECOND, TOTAL\_ELAPSED\_TIME - EXECUTION\_TIME, START\_TIME) |  |
| LASTALTERTIMESTAMP | LAST\_ALTERED |  |
| NULLABLE | IS\_NULLABLE |  |
| STARTTIME | START\_TIME |  |
| TABLEKIND | TABLE\_TYPE |  |
| TABLE\_LEVELCONSTRAINTS | TABLE\_CONSTRAINTS |  |
| TABLENAME | TABLE\_NAME |  |
| USER\_NAME | GRANTEE |  |

Expand

Show lessSee more

> For more information about DBC tables and columns see the [Teradata documentation.](https://docs.teradata.com/r/hNI_rA5LqqKLxP~Y8vJPQg/jwOyftGqfH5vIH1ZRVNW6A)
