# Snowflake in 20 minutes

## Introduction

This tutorial uses the Snowflake command-line client, [Snowflake CLI](/developer-guide/snowflake-cli/index), to introduce key concepts and tasks, including:

- Creating Snowflake objects—You create a database and a table for storing data.
- Loading data—We provide small sample CSV data files for you to load into the table.
- Querying—You explore sample queries.

Note

Snowflake bills a minimal amount for the on-disk storage used for any sample data in
this tutorial. The tutorial provides steps to drop objects and minimize storage
cost. Snowflake requires a [virtual warehouse](/user-guide/warehouses) to load the
data and execute queries. A running virtual warehouse consumes Snowflake credits.

If you are using a [30-day trial account](https://signup.snowflake.com/),
which provides free credits, you won’t incur any costs.

### What you’ll learn

In this tutorial you’ll learn how to:

- Create Snowflake objects—You create a database and a table for storing data.
- Install Snowflake CLI—You install and use Snowflake CLI, the Snowflake command-line client.

  Users of Visual Studio Code might consider using the [Snowflake Extension for Visual Studio Code](/user-guide/vscode-ext) instead of a command-line client.
- Load CSV data files—You use various mechanisms to load data into tables from CSV files.
- Write and execute sample queries—You write and execute a variety of queries against newly loaded data.

## Prerequisites

This tutorial requires a database, table, and virtual warehouse to load and query data.
Creating these Snowflake objects requires a Snowflake user with a role with the
necessary access control privileges. In addition, [Snowflake CLI](/developer-guide/snowflake-cli/index)
is required to execute the SQL statements in the tutorial. Lastly, the tutorial requires CSV files that contain sample data to load.

You can complete this tutorial using an existing Snowflake warehouse, database, and table, and your own local data files, but we recommend using the Snowflake objects and the set of
provided data.

To set up Snowflake for this tutorial, complete the following before continuing:

1. Create a user

   To create the database, table, and virtual warehouse, you must be logged in as a
   Snowflake user with a role that grants you the privileges to create these objects.

   - If you’re using a 30-day trial account, you can log in as the user that was created for the account.
     This user has the role with the privileges needed to create the objects.
   - If you don’t have a Snowflake user, you can’t perform this tutorial.
     If you don’t have a role that lets you create a user, ask someone who does to perform this step for you.
     Users with the ACCOUNTADMIN or SECURITYADMIN role can create users.
2. Install Snowflake CLI

   To install Snowflake CLI, see [Installing Snowflake CLI](/developer-guide/snowflake-cli/installation/installation).
3. Configure a connection

   Before you can run SQL, define a connection to your Snowflake account. See [Configuring Snowflake CLI and connecting to Snowflake](/developer-guide/snowflake-cli/connecting/connect).
4. Download sample data files

   For this tutorial you download sample employee data files in CSV format that Snowflake provides.

   To download and unzip the sample data files:

   1. Download the set of sample data files. Right-click the name of the archive
      file, [getting-started.zip](/static/samples/getting-started.zip), and save the link/file to your local file system.
   2. Unzip the sample files. The tutorial assumes you unpacked files into one of the following directories:
   - Linux/macOS: `/tmp`
   - Windows: `C:\\temp`

   Each file has five data records. The data uses a comma (,) character as field
   delimiter. The following is an example record:

   Copy code

   ```
   Althea,Featherstone,afeatherstona@sf_tuts.com,"8172 Browning Street, Apt B",Calatrava,7/12/2017
   ```

There are no blank spaces before or after the commas separating the
fields in each record. This is the default that Snowflake expects when loading CSV data.

## Run SQL with Snowflake CLI

After you have installed Snowflake CLI and [configured a connection](/developer-guide/snowflake-cli/connecting/connect), confirm the connection, then run SQL.

1. Open a command-line window.
2. Confirm the connection:

   Copy code

   ```
   snow connection test
   ```

   This command uses your default connection. To use a named connection, add `-c <connection_name>`. A successful test reports `Status` as `OK`.

   If you have not defined a connection yet, see [Managing Snowflake connections](/developer-guide/snowflake-cli/connecting/configure-connections).

   If your account uses an identity provider (IdP), configure the connection for browser-based authentication first. See [Use an external browser](/developer-guide/snowflake-cli/connecting/configure-connections#label-snowcli-externalbrowser).
3. When the client prompts you, complete any remaining authentication steps, such as entering your password or approving MFA.

You can run SQL statements in any of these ways:

- Pass a SQL string (`snow sql -q`)
- Run statements from a file (`snow sql -f`)
- Enter statements in interactive mode (`snow sql`)

This tutorial uses `snow sql -q` so you can copy each step and get a result.

### Pass a SQL string

Use `-q` to pass one or more statements as a string. End each statement with a semicolon (`;`):

Copy code

```
snow sql -q "SELECT CURRENT_USER();"
```

To run several statements in one command:

Copy code

```
snow sql -q "SELECT CURRENT_USER(); SELECT CURRENT_VERSION();"
```

### Run SQL from a file

Save one or more statements in a file, then pass the path with `-f`. For example, save the following statements in `queries.sql`:

Copy code

```
SELECT CURRENT_USER();
SELECT CURRENT_VERSION();
```

Copy code

```
snow sql -f queries.sql
```

### Interactive mode

To enter SQL one statement at a time, run `snow sql` with no `-q` or `-f`:

Copy code

```
snow sql
```

At the `>` prompt, enter a statement and press ENTER. End each statement with a semicolon (`;`). To leave interactive mode, enter `exit`, `quit`, or `CTRL-D`:

```
> SELECT CURRENT_USER();
> exit
```

Each `snow sql -q` or `snow sql -f` invocation is a new session. After you create the database and warehouse in the next step, later commands pass `--database sf_tuts` and `--warehouse sf_tuts_wh` so they use those objects. You can also set `database` and `warehouse` in your `connections.toml` file instead of passing those options on every command. For more information, see [Managing Snowflake connections](/developer-guide/snowflake-cli/connecting/configure-connections).

Interactive mode keeps one session until you exit.

Note

If you get locked out of the account and can’t obtain the account identifier, you can find it in the Welcome email that Snowflake sent to
you when you signed up for the trial account, or you can work with your
ORGADMIN to [get the account details](/sql-reference/sql/show-accounts).
You can also find the values for `locator`, `cloud`, and `region`
in the Welcome email.

For more information about executing SQL, including interactive mode, see [Executing SQL statements](/developer-guide/snowflake-cli/sql/execute-sql).

## Create Snowflake objects

During this step you create the following Snowflake objects:

- A database (`sf_tuts`) and a table (`emp_basic`). You load sample data into this table.
- A [virtual warehouse](/user-guide/warehouses-overview) (`sf_tuts_wh`).
  This warehouse provides the compute resources needed to load data into
  the table and query the table. For this tutorial, you create an X-Small warehouse.

At the completion of this tutorial, you will remove these objects.

### Create a database

Create the `sf_tuts` database using the [CREATE DATABASE](/sql-reference/sql/create-database) command. Both statements run in the same invocation, so the context functions see the database you just created:

Copy code

```
snow sql -q "CREATE OR REPLACE DATABASE sf_tuts; SELECT CURRENT_DATABASE(), CURRENT_SCHEMA();"
```

In this tutorial, you use the default schema (`public`) available for each database, rather than creating a new schema.

The following is an example result:

```
+--------------------+------------------+
| CURRENT_DATABASE() | CURRENT_SCHEMA() |
|--------------------+------------------|
| SF_TUTS            | PUBLIC           |
+--------------------+------------------+
```

### Create a table

Create a table named `emp_basic` in `sf_tuts.public` using the [CREATE TABLE](/sql-reference/sql/create-table) command. Pass `--database sf_tuts` so this new session uses that database:

Copy code

```
snow sql -q "CREATE OR REPLACE TABLE emp_basic (
   first_name STRING ,
   last_name STRING ,
   email STRING ,
   streetaddress STRING ,
   city STRING ,
   start_date DATE
   );" --database sf_tuts
```

Note that the number of columns in the table, their positions, and their data types correspond to the fields in the sample CSV data files that you stage in the next step in this tutorial.

### Create a virtual warehouse

Create an X-Small warehouse named `sf_tuts_wh` using the [CREATE WAREHOUSE](/sql-reference/sql/create-warehouse) command:

Copy code

```
snow sql -q "CREATE OR REPLACE WAREHOUSE sf_tuts_wh WITH
   WAREHOUSE_SIZE='X-SMALL'
   AUTO_SUSPEND = 180
   AUTO_RESUME = TRUE
   INITIALLY_SUSPENDED=TRUE;
SELECT CURRENT_WAREHOUSE();"
```

The `sf_tuts_wh` warehouse is initially suspended, but the DML statement also sets
`AUTO_RESUME = true`. The AUTO\_RESUME setting causes a warehouse to automatically start
when SQL statements that require compute resources are executed.

Later commands that need compute pass `--warehouse sf_tuts_wh`.

The following is an example result:

```
+---------------------+
| CURRENT_WAREHOUSE() |
|---------------------|
| SF_TUTS_WH          |
+---------------------+
```

## Stage data files

A Snowflake stage is a location in cloud storage that you use to load and
unload data from a table. Snowflake supports the following types of stages:

- **Internal stages**—Used to store data files internally within Snowflake. Each user and table in Snowflake gets an internal stage by default for staging data files.
- **External stages**—Used to store data files externally in Amazon S3, Google Cloud Storage, or Microsoft Azure.
  If your data is already stored in these cloud storage services, you can use an external stage to load data in Snowflake tables.

In this tutorial, we upload the sample data files
(downloaded in [Prerequisites](#label-tutorial-snowflake-in-20-mins-prerequisites))
to the internal stage for the `emp_basic` table that you created earlier. You use the [PUT](/sql-reference/sql/put) command
to upload the sample data files to that stage.

### Staging sample data files

Execute the [PUT](/sql-reference/sql/put) command with `snow sql -q` to upload local data files to the table stage
provided for the `emp_basic` table you created. Use `snow sql` for PUT, not `snow stage copy`. PUT compresses files with gzip by default, which matches the `PATTERN` in the next step.

Copy code

```
snow sql -q "PUT file://<file-path>[/\]employees0*.csv @sf_tuts.public.%emp_basic;" --database sf_tuts
```

For example:

- Linux or macOS

  Copy code

  ```
  snow sql -q "PUT file:///tmp/employees0*.csv @sf_tuts.public.%emp_basic;" --database sf_tuts
  ```
- Windows

  Copy code

  ```
  snow sql -q "PUT file://C:\temp\employees0*.csv @sf_tuts.public.%emp_basic;" --database sf_tuts
  ```

Let’s take a closer look at the command:

- `file://<file-path>[/]employees0*.csv` specifies the full directory path and
  names of the files on your local machine to stage. Note that file system wildcards are allowed, and if multiple files fit the pattern they are all displayed.
- `@<namespace>.%<table_name>` indicates to use the stage for the specified table, in this case the `emp_basic` table.

The command returns the following result, showing the staged files:

```
+-----------------+--------------------+-------------+-------------+--------------------+--------------------+----------+---------+
| source          | target             | source_size | target_size | source_compression | target_compression | status   | message |
|-----------------+--------------------+-------------+-------------+--------------------+--------------------+----------+---------|
| employees01.csv | employees01.csv.gz |         360 |         287 | NONE               | GZIP               | UPLOADED |         |
| employees02.csv | employees02.csv.gz |         355 |         274 | NONE               | GZIP               | UPLOADED |         |
| employees03.csv | employees03.csv.gz |         397 |         295 | NONE               | GZIP               | UPLOADED |         |
| employees04.csv | employees04.csv.gz |         366 |         288 | NONE               | GZIP               | UPLOADED |         |
| employees05.csv | employees05.csv.gz |         394 |         299 | NONE               | GZIP               | UPLOADED |         |
+-----------------+--------------------+-------------+-------------+--------------------+--------------------+----------+---------+
```

The PUT command compresses files by default using `gzip`, as indicated in the TARGET\_COMPRESSION column.

### Listing the staged files (Optional)

You can list the staged files using the [LIST](/sql-reference/sql/list) command.

Copy code

```
snow sql -q "LIST @sf_tuts.public.%emp_basic;" --database sf_tuts
```

The following is an example result:

```
+--------------------+------+----------------------------------+------------------------------+
| name               | size | md5                              | last_modified                |
|--------------------+------+----------------------------------+------------------------------|
| employees01.csv.gz |  288 | a851f2cc56138b0cd16cb603a97e74b1 | Tue, 9 Jan 2018 15:31:44 GMT |
| employees02.csv.gz |  288 | 125f5645ea500b0fde0cdd5f54029db9 | Tue, 9 Jan 2018 15:31:44 GMT |
| employees03.csv.gz |  304 | eafee33d3e62f079a054260503ddb921 | Tue, 9 Jan 2018 15:31:45 GMT |
| employees04.csv.gz |  304 | 9984ab077684fbcec93ae37479fa2f4d | Tue, 9 Jan 2018 15:31:44 GMT |
| employees05.csv.gz |  304 | 8ad4dc63a095332e158786cb6e8532d0 | Tue, 9 Jan 2018 15:31:44 GMT |
+--------------------+------+----------------------------------+------------------------------+
```

## Copy data into target tables

To load your staged data into the target table, execute [COPY INTO <table>](/sql-reference/sql/copy-into-table).

The [COPY INTO <table>](/sql-reference/sql/copy-into-table) command uses the virtual warehouse you created
in [Create Snowflake objects](#label-tutorial-snowflake-in-20-mins-create-snowflake-objects) to copy files.

Copy code

```
snow sql -q "COPY INTO emp_basic
  FROM @%emp_basic
  FILE_FORMAT = (type = csv field_optionally_enclosed_by='\"')
  PATTERN = '.*employees0[1-5].csv.gz'
  ON_ERROR = 'skip_file';" --database sf_tuts --warehouse sf_tuts_wh
```

Where:

- The FROM clause specifies the location containing the data files (the internal stage for the table).
- The FILE\_FORMAT clause specifies the file type as CSV, and specifies the double-quote
  character (`"`) as the character used to enclose strings. Snowflake supports
  diverse file types and options. These are described
  in [CREATE FILE FORMAT](/sql-reference/sql/create-file-format).
- The PATTERN clause specifies that the command should load data from the filenames matching
  this regular expression (`.*employees0[1-5].csv.gz`).
- The ON\_ERROR clause specifies what to do when the COPY command encounters errors in the files. By default, the command stops loading data
  when the first error is encountered. This example skips any file containing an error and moves on to loading
  the next file. (None of the files in this tutorial contain errors; this is included for illustration purposes.)

The COPY command also provides an option for validating files before they are loaded. For more information about additional error checking and validation instructions, see the [COPY INTO <table>](/sql-reference/sql/copy-into-table) topic and the other [data loading tutorials](/guides-overview-loading-data).

The COPY command returns a result showing the list of files copied and related information:

```
+--------------------+--------+-------------+-------------+-------------+-------------+-------------+------------------+-----------------------+-------------------------+
| file               | status | rows_parsed | rows_loaded | error_limit | errors_seen | first_error | first_error_line | first_error_character | first_error_column_name |
|--------------------+--------+-------------+-------------+-------------+-------------+-------------+------------------+-----------------------+-------------------------|
| employees02.csv.gz | LOADED |           5 |           5 |           1 |           0 | NULL        |             NULL |                  NULL | NULL                    |
| employees04.csv.gz | LOADED |           5 |           5 |           1 |           0 | NULL        |             NULL |                  NULL | NULL                    |
| employees05.csv.gz | LOADED |           5 |           5 |           1 |           0 | NULL        |             NULL |                  NULL | NULL                    |
| employees03.csv.gz | LOADED |           5 |           5 |           1 |           0 | NULL        |             NULL |                  NULL | NULL                    |
| employees01.csv.gz | LOADED |           5 |           5 |           1 |           0 | NULL        |             NULL |                  NULL | NULL                    |
+--------------------+--------+-------------+-------------+-------------+-------------+-------------+------------------+-----------------------+-------------------------+
```

## Query loaded data

You can query the data loaded in the `emp_basic` table using standard [SQL](/sql-reference/constructs) and any supported
[functions](/sql-reference-functions) and
[operators](/sql-reference/operators).

You can also manipulate the data, such as updating the loaded data or inserting more data, using standard [DML commands](/sql-reference/sql-dml).

### Retrieve all data

Return all rows and columns from the table:

Copy code

```
snow sql -q "SELECT * FROM emp_basic;" --database sf_tuts --warehouse sf_tuts_wh
```

The following is a partial result:

```
+------------+--------------+---------------------------+-----------------------------+--------------------+------------+
| FIRST_NAME | LAST_NAME    | EMAIL                     | STREETADDRESS               | CITY               | START_DATE |
|------------+--------------+---------------------------+-----------------------------+--------------------+------------|
| Arlene     | Davidovits   | adavidovitsk@sf_tuts.com  | 7571 New Castle Circle      | Meniko             | 2017-05-03 |
| Violette   | Shermore     | vshermorel@sf_tuts.com    | 899 Merchant Center         | Troitsk            | 2017-01-19 |
| Ron        | Mattys       | rmattysm@sf_tuts.com      | 423 Lien Pass               | Bayaguana          | 2017-11-15 |
 ...
 ...
 ...
| Carson     | Bedder       | cbedderh@sf_tuts.co.au    | 71 Clyde Gallagher Place    | Leninskoye         | 2017-03-29 |
| Dana       | Avory        | davoryi@sf_tuts.com       | 2 Holy Cross Pass           | Wenlin             | 2017-05-11 |
| Ronny      | Talmadge     | rtalmadgej@sf_tuts.co.uk  | 588 Chinook Street          | Yawata             | 2017-06-02 |
+------------+--------------+---------------------------+-----------------------------+--------------------+------------+
```

### Insert additional data rows

In addition to loading data from staged files into a table, you can insert rows directly into a table using the [INSERT](/sql-reference/sql/insert) DML command.

For example, to insert two additional rows into the table:

Copy code

```
snow sql -q "INSERT INTO emp_basic VALUES
   ('Clementine','Adamou','cadamou@sf_tuts.com','10510 Sachs Road','Klenak','2017-9-22') ,
   ('Marlowe','De Anesy','madamouc@sf_tuts.co.uk','36768 Northfield Plaza','Fangshan','2017-1-26');" --database sf_tuts --warehouse sf_tuts_wh
```

### Query rows based on email address

Return a list of email addresses with United Kingdom top-level domains using the [[ NOT ] LIKE](/sql-reference/functions/like) function:

Copy code

```
snow sql -q "SELECT email FROM emp_basic WHERE email LIKE '%.uk';" --database sf_tuts --warehouse sf_tuts_wh
```

The following is an example result:

```
+--------------------------+
| EMAIL                    |
|--------------------------|
| gbassfordo@sf_tuts.co.uk |
| rtalmadgej@sf_tuts.co.uk |
| madamouc@sf_tuts.co.uk   |
+--------------------------+
```

### Query rows based on start date

For example, to calculate when certain employee benefits might start, add 90 days to employee start
dates using the [DATEADD](/sql-reference/functions/dateadd) function. Filter the list by employees whose start date occurred earlier than January 1, 2017:

Copy code

```
snow sql -q "SELECT first_name, last_name, DATEADD('day',90,start_date) FROM emp_basic WHERE start_date <= '2017-01-01';" --database sf_tuts --warehouse sf_tuts_wh
```

The following is an example result:

```
+------------+-----------+------------------------------+
| FIRST_NAME | LAST_NAME | DATEADD('DAY',90,START_DATE) |
|------------+-----------+------------------------------|
| Granger    | Bassford  | 2017-03-30                   |
| Catherin   | Devereu   | 2017-03-17                   |
| Cesar      | Hovie     | 2017-03-21                   |
| Wallis     | Sizey     | 2017-03-30                   |
+------------+-----------+------------------------------+
```

## Summary, clean up, and additional resources

Congratulations! You’ve successfully completed this introductory tutorial.

Take a few minutes to review a short summary and the key points covered in the tutorial.
You might also want to consider cleaning up by dropping any objects you created in the tutorial.
Learn more by reviewing other topics in the Snowflake Documentation.

### Summary and key points

In summary, data loading is performed in two steps:

1. Stage the data files to load. The files can be staged internally (in Snowflake) or in an external location. In this tutorial, you stage files internally.
2. Copy data from the staged files into an existing target table. A running
   warehouse is required for this step.

Remember the following key points about loading CSV files:

- A CSV file consists of 1 or more records, with 1 or more fields in each record, and sometimes a header record.
- Records and fields in each file are separated by delimiters. The default delimiters are:

  Records:
  :   newline characters

  Fields:
  :   commas

  In other words, Snowflake expects each record in a CSV file to be separated by new lines and the fields (i.e. individual values) in each record to be separated by commas. If different
  characters are used as record and field delimiters, you must explicitly specify this as part of the file format when loading.
- There is a direct correlation between the fields in the files and the columns in the table you will be loading, in terms of:

  - Number of fields (in the file) and columns (in the target table).
  - Positions of the fields and columns within their respective file/table.
  - Data types, such as string, number, or date, for fields and columns.

  The records will not be loaded if the numbers, positions, and data types don’t align with the data.

  Note

  Snowflake supports loading files in which the fields don’t exactly align with the columns in the target table;
  however, this is a more advanced data loading topic (covered in
  [Transform data during a load](/user-guide/data-load-transform)).

### Tutorial cleanup (Optional)

If the objects you created in this tutorial are no longer needed,
you can remove them from the system with [DROP <object>](/sql-reference/sql/drop) statements.

Copy code

```
snow sql -q "DROP DATABASE IF EXISTS sf_tuts; DROP WAREHOUSE IF EXISTS sf_tuts_wh;"
```

### What’s next?

Continue learning about Snowflake using the following resources:

- Complete the other tutorials provided by Snowflake:

  - [Tutorials to get started with Snowflake](/learn-tutorials)
- Familiarize yourself with key Snowflake concepts and features, as well as the SQL commands to perform queries and insert/update data:

  - [Get started with Snowflake for users](/getting-started-for-users)
  - [Query syntax](/sql-reference/constructs)
  - [Data Manipulation Language (DML) commands](/sql-reference/sql-dml)
