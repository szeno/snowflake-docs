# BigQuery - CREATE VIEW

## Description

Creates a new view. ([BigQuery SQL Language Reference Create view statement](https://cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=en#create_view_statement))

Note

:class: tip
This syntax is fully supported in [Snowflake](https://docs.snowflake.com/en/sql-reference/sql/create-view).

## Grammar Syntax

Copy code

```
CREATE [ OR REPLACE ] VIEW [ IF NOT EXISTS ] view_name
[(view_column_name_list)]
[OPTIONS(view_option_list)]
AS query_expression

view_column_name_list :=
  view_column[, ...]

view_column :=
  column_name [OPTIONS(view_column_option_list)]
```

### Sample Source Patterns

#### BigQuery

Copy code

```
CREATE VIEW myuser
AS
SELECT lastname FROM users;

CREATE OR REPLACE VIEW myuser2
AS
SELECT lastname FROM users2;

CREATE VIEW IF NOT EXISTS myuser2
AS
SELECT lastname FROM users2;
```

#### Snowflake

Copy code

```
CREATE VIEW myuser
AS
SELECT lastname FROM
users;

CREATE OR REPLACE VIEW myuser2
AS
SELECT lastname FROM
users2;

CREATE VIEW myuser3
AS
SELECT lastname FROM
users3;
```

### Known Issues

There are no known Issues.

### Related EWIs

There are no related EWIs.

## View column name list

### Description

The view’s column name list is optional. The names must be unique but do not have to be the same as the column names of the underlying SQL query. ([BigQuery SQL Language Reference View column name list](https://cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=en#view_column_name_list))

Note

:class: tip
This syntax is fully supported in [Snowflake](https://docs.snowflake.com/en/sql-reference/sql/create-view).

### Grammar Syntax

Copy code

```
view_column_name_list :=
  view_column [OPTIONS(view_column_option_list)] [, ...]

view_column_option_list :=
  DESCRIPTION = value
```

### Sample Source Patterns

#### BigQuery

Copy code

```
CREATE VIEW `myproject.mydataset.newview` (
  column_1_new_name OPTIONS (DESCRIPTION='Description of the column 1 contents'),
  column_2_new_name OPTIONS (DESCRIPTION='Description of the column 2 contents'),
  column_3_new_name OPTIONS (DESCRIPTION='Description of the column 3 contents')
)
AS SELECT column_1, column_2, column_3 FROM `myproject.mydataset.mytable`
```

#### Snowflake

Copy code

```
 CREATE VIEW myproject.mydataset.newview
(
  column_1_new_name COMMENT 'Description of the column 1 contents',
  column_2_new_name COMMENT 'Description of the column 2 contents',
  column_3_new_name COMMENT 'Description of the column 3 contents'
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "bigquery",  "convertedOn": "03/25/2025",  "domain": "test" }}'
AS SELECT column_1, column_2, column_3 FROM
  myproject.mydataset.mytable
```

### Known Issues

There are no known Issues.

### Related EWIs

There are no related EWIs.

## View Options

### Description

> The option list allows you to set view options such as a label and an expiration time. You can include multiple options using a comma-separated list. ([BigQuery SQL Language Reference View Options](https://cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=en#view_option_list))

Warning

This syntax is partially supported in [Snowflake](https://docs.snowflake.com/en/sql-reference/sql/create-view).

### Grammar Syntax

Copy code

```
OPTIONS(view_option_list [,...])

view_option_list :=
  NAME = value
```

| NAME | Value | Supported |
| --- | --- | --- |
| expiration\_timestamp | TIMESTAMP | false |
| friendly\_name | STRING | true |
| description | STRING | true |
| labels | ARRAY<STRUCT<STRING, STRING>> | true |
| privacy\_policy | JSON-formatted STRING | false |

### Sample Source Patterns

#### Description & Friendly\_name:

The description and friendly\_name options are included in the generated Comment Clause.

##### BigQuery

Copy code

```
CREATE VIEW my_view
OPTIONS (
  description="This is a view description",
  friendly_name="my_friendly_view") AS
SELECT column1, column2
FROM my_table;
```

##### Snowflake

Copy code

```
CREATE VIEW my_view
COMMENT = '{ "description": "This is a view description", "friendly_name": "my_friendly_view", "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "bigquery",  "convertedOn": "03/25/2025",  "domain": "test" }}'
AS
SELECT column1, column2
FROM
 my_table;
```

#### Labels:

In BigQuery the labels associated with a view can be used to organize and group tables in the database administrative environment, in Snowflake the Tags can be used for the same functionality. But to ensure that the tag exists, The corresponding CREATE TAG will be added before the CREATE VIEW if it contains labels. It is important to know that the `CREATE TAG` feature requires Enterprise Edition or higher

##### BigQuery

Copy code

```
CREATE VIEW my_view
OPTIONS(
    labels=[("label1", "value1"), ("label2", "value2")]
)
AS
SELECT column1, column2
FROM table1;
```

##### Snowflake

Copy code

```
CREATE TAG IF NOT EXISTS "label1";
CREATE TAG IF NOT EXISTS "label2";

CREATE VIEW my_view
WITH TAG( "label1" = "value1","label2" = "value2" )
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "bigquery",  "convertedOn": "03/26/2025",  "domain": "test" }}'
AS
SELECT column1, column2
FROM
  table1;
```

#### Unsupported Options:

When an option clause includes elements not supported by Snowflake, An EWI will be added.

##### BigQuery

Copy code

```
CREATE VIEW my_view
OPTIONS (
  expiration_timestamp=TIMESTAMP "2026-01-01 00:00:00 UTC",
  privacy_policy='{"aggregation_threshold_policy": {"threshold": 50, "privacy_unit_columns": "ID"}}'
) AS
SELECT column1, column2
FROM my_table;
```

##### Snowflake

Copy code

```
CREATE VIEW my_view10
!!!RESOLVE EWI!!! /*** SSC-EWI-BQ0001 - SNOWFLAKE DOES NOT SUPPORT THE OPTIONS: EXPIRATION_TIMESTAMP, PRIVACY_POLICY ***/!!!
OPTIONS(
  expiration_timestamp=TIMESTAMP "2026-01-01 00:00:00 UTC",
  privacy_policy='{"aggregation_threshold_policy": {"threshold": 50, "privacy_unit_columns": "ID"}}'
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "bigquery",  "convertedOn": "03/26/2025",  "domain": "test" }}'
AS
SELECT column1, column2
FROM
  my_table;
```

#### Known Issues

- The label-to-tag transformation could lead to errors if the Snowflake account is not Enterprise Edition or higher.

#### Related EWIs

1. [SSC-EWI-BQ0001](../../issues-and-troubleshooting/conversion-issues/bigqueryEWI#ssc-ewi-bq0001): The OPTIONS clause within View is not supported in Snowflake.
