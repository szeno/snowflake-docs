# Tutorial: Loading JSON data into a relational table

## Introduction

When uploading JSON data into a table, you have these options:

- Store JSON objects natively in a VARIANT type column (as shown in [Tutorial: Bulk loading from a local file system using COPY](/user-guide/tutorials/data-load-internal-tutorial)).
- Store JSON objects natively in an intermediate table and then use the FLATTEN function to extract JSON elements into separate columns in a table (as shown in [Tutorial: JSON basics for Snowflake](/user-guide/tutorials/json-basics-tutorial)).
- Transform JSON elements directly into table columns as shown in this tutorial.

The COPY command in this tutorial uses a SELECT statement to query for individual elements in a staged JSON file.

Run the SQL in one interactive [Snowflake CLI](/developer-guide/snowflake-cli/sql/execute-sql#label-snowcli-sql-interactive-mode) session (`snow sql`). Upload the sample file with [`snow stage copy`](/developer-guide/snowflake-cli/command-reference/stage-commands/copy) from a second terminal so the SQL session stays open.

## Prerequisites

For this tutorial you need to:

- [Install Snowflake CLI](/developer-guide/snowflake-cli/installation/installation).
- Download a Snowflake provided JSON data file.
- Create a database, a table, and a virtual warehouse for this tutorial.

Database, table, and virtual warehouse are basic Snowflake objects required for
most Snowflake activities.

### Data file for loading

To download the sample JSON data file, click [sales.json](/static/samples/sales.json).
If clicking the link does not download the file, right-click the link and save the
link/file to your local file system.

The tutorial assumes you unpacked the JSON data file into the following directories:

> - Linux/macOS: `/tmp/load`
> - Windows: `C:\temp\load`

The data file includes sample home sales JSON data. An example JSON object is shown:

Copy code

```
{
   "location": {
      "state_city": "MA-Lexington",
      "zip": "40503"
   },
   "sale_date": "2017-3-5",
   "price": "275836"
}
```

### Open one Snowflake CLI session

Start an interactive `snow sql` session and run every SQL statement in this tutorial at that prompt. Keep the session open until you finish the tutorial, including the clean-up commands. The temporary table lasts only for this session, and the `USE` statements apply only here.

Copy code

```
snow sql
```

End each SQL statement with a semicolon (`;`). To leave the session after the tutorial, enter `exit`.

The file upload later in this tutorial uses `snow stage copy` in a second terminal. Leave this `snow sql` session running while you upload, then return to it for the `COPY INTO` statement.

### Creating the database, table, and virtual warehouse

In the `snow sql` session, run the following commands to create objects for this tutorial.
When you have completed the tutorial, you can drop the objects.

Copy code

```
CREATE OR REPLACE DATABASE mydatabase;

CREATE OR REPLACE WAREHOUSE mywarehouse WITH
  WAREHOUSE_SIZE='X-SMALL'
  AUTO_SUSPEND = 120
  AUTO_RESUME = TRUE
  INITIALLY_SUSPENDED=TRUE;

USE DATABASE mydatabase;
USE SCHEMA public;
USE WAREHOUSE mywarehouse;

CREATE OR REPLACE TEMPORARY TABLE home_sales (
  city STRING,
  zip STRING,
  state STRING,
  type STRING DEFAULT 'Residential',
  sale_date timestamp_ntz,
  price STRING
  );
```

The `USE` statements set the database, schema, and warehouse for the rest of this session.
The `CREATE TABLE` statement creates a temporary table. Temporary tables persist only for
the duration of the user session and are not visible to other users.

## Create file format object

Execute the [CREATE FILE FORMAT](/sql-reference/sql/create-file-format) command
to create the `sf_tut_json_format` file format.

Copy code

```
CREATE OR REPLACE FILE FORMAT sf_tut_json_format
  TYPE = JSON;
```

`TYPE = 'JSON'` indicates the source file format type. CSV is the default file format type.

## Create stage object

Execute [CREATE STAGE](/sql-reference/sql/create-stage) to create the
internal `sf_tut_stage` stage.

> Copy code
>
> ```
> CREATE OR REPLACE STAGE sf_tut_stage
>  FILE_FORMAT = sf_tut_json_format;
> ```

Create this stage without `TEMPORARY` so the upload command in the other terminal can write to `mydatabase.public.sf_tut_stage`. The `DROP DATABASE` command at the end of the tutorial removes the stage.

## Stage the data file

In a second terminal, upload the JSON file from your local file system to the named stage.
Leave the `snow sql` session open.

`snow stage copy` gzips a file only when you pass `--auto-compress`. The COPY INTO step
later in this tutorial loads `sales.json.gz`, so include that option.

- Linux or macOS

  Copy code

  ```
  snow stage copy "/tmp/load/sales.json" @mydatabase.public.sf_tut_stage --auto-compress
  ```
- Windows

  Copy code

  ```
  snow stage copy "C:\temp\load\sales.json" @mydatabase.public.sf_tut_stage --auto-compress
  ```

## Copy data into the target table

Load the `sales.json.gz` staged data file into the `home_sales` table.

Copy code

```
COPY INTO home_sales(city, state, zip, sale_date, price)
   FROM (SELECT SUBSTR($1:location.state_city,4),
                SUBSTR($1:location.state_city,1,2),
                $1:location.zip,
                to_timestamp_ntz($1:sale_date),
                $1:price
         FROM @sf_tut_stage/sales.json.gz t)
   ON_ERROR = 'continue';
```

Note the $1 in the SELECT query refers to the single column where the JSON is stored.
The query also uses the following functions:

- The [SUBSTR , SUBSTRING](/sql-reference/functions/substr) function to extract city and state values from the state\_city JSON key.
- The [TO\_TIMESTAMP / TO\_TIMESTAMP\_\*](/sql-reference/functions/to_timestamp) function to cast the sale\_date JSON key value to a timestamp.

Execute the following query to verify data is copied.

Copy code

```
SELECT * from home_sales;
```

## Remove the successfully copied data files

After you verify that you successfully copied data from your stage into the tables,
you can remove data files from the internal stage using the [REMOVE](/sql-reference/sql/remove)
command to save on [data storage](/user-guide/cost-understanding-compute).

> Copy code
>
> ```
> REMOVE @sf_tut_stage/sales.json.gz;
> ```

## Clean up

Execute the following [DROP <object>](/sql-reference/sql/drop) commands to return your system to its state before you began the tutorial:

> Copy code
>
> ```
> DROP DATABASE IF EXISTS mydatabase;
> DROP WAREHOUSE IF EXISTS mywarehouse;
> ```

Dropping the database automatically removes all child database objects such as tables.
