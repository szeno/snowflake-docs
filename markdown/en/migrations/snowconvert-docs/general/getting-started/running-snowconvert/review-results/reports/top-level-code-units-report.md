# SnowConvert AI - Top-Level Code Units Report

## What is a Top-Level Code Unit?

A Code Unit, as the name suggests, is the most atomic, standalone executable element. In most cases, these are statements, but they also include script files as well because those are executed as a single element.

Some Code Units can be nested inside other Code Units. When there is no other Code Unit above it in a hierarchy of Units, it’s called a Top-Level Code Unit.

## What is an out-of-scope Code Unit?

Out-of-scope Top-Level Code Units are Code Units that are out of the conversion scope of SnowConvert AI. Because of this, these code units are not considered when calculating the conversion rate. Each of these code units will not have a conversion rate (it will appear as `N/A`).

If the input code includes only out-of-scope Code Units, then the Lines of Code conversion rate of the entire migration will be 0%.

The following `CREATE TRIGGER` is considered an out-of-scope Code Unit.

Copy code

```
:force:
CREATE OR REPLACE TRIGGER my_trigger
    AFTER
    UPDATE
    ON my_table
    FOR EACH ROW
BEGIN
   NULL;
END;
```

## Examples of Top-Level Code Units

In the following section, we can see some examples of Top-Level Code Units.

### Queries

In the following example, we have here a single SELECT statement. This statement is a single Top-Level Code Unit.

Copy code

```
:force:
SELECT * FROM table1;
```

In this example, we have a nested `SELECT` statement nested inside another `SELECT` statement. The entire query counts as a single Top-Level Code Unit.

Copy code

```
SELECT * FROM (SELECT * FROM table1);
```

### Objects

Objects created with a DDL count as a single Top-Level Code Unit, even if it contains other Code Units inside it.

The following statement creates a view with a query. In this case, the entire `CREATE VIEW` counts as a single Top-Level Code Unit.

Copy code

```
CREATE VIEW view1 AS SELECT * FROM table1;
```

The following `CREATE PROCEDURE` statement counts as a single Top-Level Code Unit even if it contains multiple statements inside it.

Copy code

```
CREATE PROCEDURE procedure1
AS
BEGIN
    DELETE FROM table1;
END;
```

### Commands

Independent commands in an SQL file are considered Top-Level Code Units.

A `COMMIT` statement counts as a single Top-Level Code Unit.

Copy code

```
COMMIT;
```

### Package Bodies in Oracle

A package can define multiple elements inside its body. The package body is considered the Top-Level Code Unit because those elements cannot be created individually without creating the entire package body. Elements or code units inside a package body will not count as Top-Level Code Units.

The following code will be reported as a single `CREATE PACKAGE BODY` Code Unit.

Copy code

```
:force:
CREATE PACKAGE package_body1 IS
    FUNCTION function1
    RETURN VARCHAR
    IS
    BEGIN
        RETURN 'HELLO'';
    END;
END;
```

### Teradata Script files

Teradata Script files like BTEQ or TPUMP are executed as standalone code units. Because of this, the entire file is considered a single Top-Level Code Unit. Other possible code units inside these files will not count as Top-Level Code Units.

The following BTEQ script file will be reported as a single BTEQ Top-Level Code Unit.

Copy code

```
:force:
.LOGON e/fml,notebook
.COMPILE FILE = example.spl;
COMMIT;
CALL samplesp1 (8888, pAmount);
.LOGOFF
```

### Transact SQL batches with GOTO

Each statement of Transact-SQL can be executed independently. In most cases, each of these statements is considered a Top-Level Code Unit. However, when there is a batch that contains a GOTO statement to a label inside the same batch, the statements of the batch cannot be executed independently without ensuring that they work properly. Because of this, statements that are in a batch with a GOTO statement will not count as Top-Level Code Units, only the batch.

The following code example will be reported as a single GOTO/LABEL Code Unit:

Copy code

```
DECLARE @Counter int;
SET @Counter = 1;
WHILE @Counter < 10
BEGIN
    SELECT @Counter
    SET @Counter = @Counter + 1
    IF @Counter = 4 GOTO Branch_One
    IF @Counter = 5 GOTO Branch_Two
END
Branch_One:
    SELECT 'Jumping To Branch One.'
    GOTO Branch_Three;
Branch_Two:
    SELECT 'Jumping To Branch Two.'
Branch_Three:
    SELECT 'Jumping To Branch Three.';
GO
```

## How is the Code Unit methodology represented in other reports?

The Code Unit methodology is also represented in other reports. This section explains how these values are shown or are related to other reports.

### Issues Report

[issues-report.md](issues-report)

Each row of the Issues Report has some information about the Code Unit that is being impacted by the issue. The columns related to Code Units are the following:

- **Code Unit Database:** This is the Database of the Top-Level Code Unit where the issue was found. It only applies to Code Units that are objects.
- **Code Unit Schema:** This is the Schema of the Top-Level Code Unit where the issue was found. It only applies to Code Units that are objects.
- **Code Unit Package:** This is the Package of the Top-Level Code Unit where the issue was found. It only applies to Code Units that are objects.
- **Code Unit Name:** This is the name Top-Level Code Unit where the issue was found. It only applies to named Code Units like objects. This name is not qualified by database, schema, or package.
- **Code Unit ID:** This is the ID of the Top-Level Code Unit where the issue was found. This name has the name qualified and will add a number for code units with repeated names.
- **Code Unit:** This is the type of the Top-Level Code Unit where the issue was found.
- **Code Unit Size:** This is the size of the Top-Level Code Unit where the issue was found.

### Object References Report and Missing Objects Report

[object-references-report.md](object-references-report)

[missing-objects-report.md](missing-objects-report)

Each row of the Object References report has information about the Top-Level Code Unit that was referencing another element. These referenced elements may not be Top-Level, so those other values may not be included in the Top-Level Code Units report.

Similarly to the Object References report, the Missing Objects Report has information about the Top-Level Code Unit that was referencing an element that could not be found in the code.

- **Caller Code Unit:** This is the type of the Top-Level Code Unit that is referencing another element.
- **Caller Code Unit Database:** This is the database of the Top-Level Code Unit that is referencing another element.
- **Caller Code Unit Schema:** This is the schema of the Top-Level Code Unit that is referencing another element.
- **Caller Code Unit Name:** This is the name of the Top-Level Code Unit that is referencing another element.
- **Caller Code Unit Full Name:** This is the full name of the Top-Level Code Unit that is referencing another element.

## Information in the Top-Level Code Units Report

| Column | Description |
| --- | --- |
| Partition Key | The unique identifier of the conversion. |
| File Type | The type of the file that the Code Unit is in. (SQL, BTEQ, etc…) |
| Category | The broader class or type each code unit belongs to. |
| Code Unit | The type of Code Unit that this element belongs to. |
| Source Database | The database where the source code unit is located. |
| Source Schema | The schema where the source code unit is located. |
| Source Name | The original name of the source code unit as it appears in the source system. |
| Code Unit Id | The unique identifier of the Code Unit with qualified name and numbering for code units with repeated names. |
| File Name | The name of the file in which the object is located. Uses the relative path starting from the input directory. |
| Line Number | The line number inside the file where the code unit is located. |
| Lines of Code | The total lines of code that the code unit has. |
| EWI Count | The amount of EWIs found within the code unit. You can learn more about EWIs [here](../../../../technical-documentation/issues-and-troubleshooting/conversion-issues/README). |
| FDM Count | The amount of FDMs found within the code unit. You can learn more about FDMs [here](../../../../technical-documentation/issues-and-troubleshooting/functional-difference/README). |
| PRF Count | The amount of PRFs found within the code unit. You can learn more about PRFs [here](../../../../technical-documentation/issues-and-troubleshooting/performance-review/README). |
| Highest EWI Severity | The highest EWI severity found within the code unit. The severity order is the following:   - N/A (when there are not any EWIs) - Low - Medium - High - Critical |
| UDFs Used | The names of all the user defined functions found within the code unit. The name of the UDFs used are separated by a pipe if there is more than one. |
| EWI | The codes of all the EWIs found within the code unit. These codes are separated by pipes and do not include repeated codes. |
| FDM | The codes of all the FDMs found within the code unit. These codes are separated by pipes and do not include repeated codes. |
| PRF | The codes of all the PRFs found within the code unit. These codes are separated by pipes and do not include repeated codes. |
| Conversion Status | The final status of the conversion of the code unit.  The possible conversion statuses are:   - NotSupported: When the Code Unit has a 0% conversion rate. - Partial: When the conversion rate of the Code Unit is between 0% and 100%. - Success: When the Code Unit conversion rate is 100%. |
| LoC Conversion Percentage | The conversion percentage is based on Lines of Code. A single line of code may have supported and unsupported fragments depending on how the input code was formatted. In these cases, the entire line is considered as not supported. |
| Deployment Order | The deployment order is the topological level of each code unit based on its dependencies. It shows the right order in which the code units should be deployed to avoid missing dependencies during the deployment phase. |
| Language | The programming language or SQL dialect of the source code unit. |

Expand

Show lessSee more

## Example

Assume that the following `CREATE TABLE` in ORACLE SQL is located in its file called table\_example.sql.

Copy code

```
CREATE TABLE my_table (
  my_column DATE DEFAULT TO_DATE(CURRENT_DATE, 'J'),
  NOT A VALID COLUMN
);
```

Copy code

```
CREATE OR REPLACE TABLE my_table (
   my_column TIMESTAMP /*** SSC-FDM-OR0042 - DATE TYPE COLUMN HAS A DIFFERENT BEHAVIOR IN SNOWFLAKE. ***/ DEFAULT PUBLIC.JULIAN_TO_GREGORIAN_DATE_UDF(CURRENT_DATE(), 'J')
--                                                                                                                                                                          ,
-- ** SSC-EWI-0001 - UNRECOGNIZED TOKEN ON LINE '3' COLUMN '3' OF THE SOURCE CODE STARTING AT 'NOT'. EXPECTED 'Column Definition' GRAMMAR. LAST MATCHING TOKEN WAS ',' ON LINE '2' COLUMN '52'. FAILED TOKEN WAS 'NOT' ON LINE '3' COLUMN '3'. CODE '15'. **
--  NOT A VALID COLUMN
 )
 COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"oracle"}}'
 ;
```

The Top-Level Code Units report will have a single entry of the previously shown table.

Here are all the values that would be reported in the entry of this `CREATE TABLE` statement:

- The **Partition Key** value will depend on migration so the value here will vary.
- The **File Type** will be SQL because it was migrated on a file with the .sql extension.
- The **Category** will be TABLE because the `CREATE TABLE` statement is part of the TABLE Code Unit Category.
- The **Code Unit** itself will be `CREATE TABLE`.
- The **File Name** where this code unit was found would be table\_example.sql.
- Assuming that the `CREATE TABLE` statement is at the beginning of the file, the **Line Number** will be 1.
- The **Lines of Code** number would be 4.
- The **EWI Count** column will report 1 because the output code has one parsing EWI.
- The **FDM Count** column will report 1 because the output code has an FDM issue related to data types.
- The **PRF Count** will report 0 because there are no PRF issues present in the output code.
- The **Highest EWI Severity** in this case would be “Critical” because this is the severity of the parsing EWI of the example. The other one has a “Low” severity.
- The **UDFs Used** column will be `JULIAN_TO_GREGORIAN_DATE_UDF` because this custom User Defined Function was added to convert the `TO_DATE` function of the input code.
- The **EWI** column will report “SSC-EWI-0001” because this was one of EWIs added in the output code.
- The **FDM** column will report “SSC-FDM-OR0042” because this was one of FDMs added in the output code.
- The **PRF** column will report “N/A” because there are no PRF issues present in the output code.
- The **Conversion Status** will be “Partial” because only some fragments of this Code Unit were able to be migrated without EWIs.
- The **LoC Conversion Percentage** is 50% because out of 4 lines, only 2 were converted successfully.

## Deployment Order

The deployment order column represents the correct order to deploy each code unit into Snowflake.

The following code exemplifies in depth how the deployment order is calculated.

Copy code

```
CREATE TABLE TABLE1 ( -- level 0, no dependencies
   COL1 INT
);

CREATE TABLE TABLE2 ( -- level 0, no dependencies
   COL1 INT
);

CREATE VIEW VIEW1 -- level 4, depends on level-3 objects
AS SELECT * FROM VIEW2, VIEW3;

CREATE VIEW VIEW2 -- level 3, depends on level-2 objects
AS SELECT * FROM VIEW4, VIEW5, VIEW3;

CREATE VIEW VIEW4 -- level 1, depends on level-0 objects
AS SELECT * FROM TABLE1, TABLE2;

CREATE VIEW VIEW5 -- level 1, depends on level-0 objects
AS SELECT * FROM TABLE1;

CREATE VIEW VIEW3 -- level 2, depends on level-1 objects
AS SELECT * FROM VIEW6;

CREATE VIEW VIEW6 -- level 1, depends on level-0 objects
AS SELECT * FROM TABLE2;
```

The deployment order starts with `0`, so code units without any dependencies will start at this level. In the example above, `TABLE1` and `TABLE2` will have a level `0` .

For the next level, we will focus on code units that depend on code units of level `0`. `VIEW4`, `VIEW5`, and `VIEW6` depend directly on `TABLE1` and `TABLE2`, so their level will be `1`.

After identifying all the code units of level `1` , we will focus on code units of level `2`. In that particular scenario, just `VIEW3` depends on `VIEW6` , so `VIEW3` will be level `2`.

Once we identify all code units of level `2`, we will focus on level 3. In the example above, `VIEW2` depends on `VIEW4`, `VIEW5` and `VIEW3`, however, the highest dependency level is `2`, so, `VIEW2` will be of level `3`.

Finally, we got `VIEW1`, which depends on `VIEW2` and `VIEW3`. Since `VIEW2` is the dependency with higher level, `VIEW1` will get level `4`.

After making all the calculations, the top-level code units report will look something like the following table.

| Code Unit Id | Deployment Order |
| --- | --- |
| VIEW1 | 4 |
| VIEW2 | 3 |
| VIEW3 | 2 |
| VIEW4 | 1 |
| VIEW5 | 1 |
| VIEW6 | 1 |
| TABLE1 | 0 |
| TABLE2 | 0 |

Expand

Show lessSee more

### Limitations

There are some scenarios where the deployment order may not calculate the right level for a specific code unit.

#### Code Units with Missing Dependencies

Deployment of code units that depend (directly or indirectly) on missing objects is not possible. Although SnowConvert AI calculates the deployment order as best it can, a missing dependency will cause deployment errors. For code units with missing dependencies, SnowConvert AI adds an asterisk (\*) alongside the deployment order. E.g.

Copy code

```
CREATE TABLE TABLE1 ( -- level 0, no dependencies
  COL1 INT
);

CREATE VIEW VIEW1 -- level 1*, depends on level-0 objects and has a missing dependency
AS SELECT * FROM TABLE1, TABLE2;

CREATE VIEW VIEW2 -- level 2*, depends on level-1* objects
AS SELECT * FROM VIEW1;
```

The example above shows `VIEW1` referencing a missing `TABLE2` and `VIEW2` referencing ,`VIEW1` which indirectly refers `TABLE2` . `VIEW1` has a direct missing reference and `VIEW2` an indirect missing reference. The top-level code units report will look something like the following table.

| Code Unit Id | Deployment Order |
| --- | --- |
| TABLE1 | 0 |
| VIEW1 | 1\* |
| VIEW2 | 2\* |

Expand

Show lessSee more

#### Code Units referencing Database Links (Oracle)

While SnowConvert AI can identify references to Database Links, it cannot get more information about the objects being referenced through the database link. This kind of reference may cause trouble during deployment as well, so it will be handled the same way as missing object references. E.g.

Copy code

```
CREATE DATABASE LINK DBLINK1
CONNECT TO PUBLIC IDENTIFIED BY VALUES ':1'
USING 'TEST';

CREATE MATERIALIZED VIEW VIEW1 REFRESH WITH ROWID
AS SELECT * FROM TABLE1@DBLINK1;
```

`VIEW1` is referencing `TABLE1` through the database link `DBLINK1`. Since we don’t know where `TABLE1` is located, the deployment order of `VIEW1` will be handled like a deployment order with missing dependencies (\*).

| Code Unit Id | Deployment Order |
| --- | --- |
| DBLINK1 | 0 |
| VIEW1 | 1\* |

Expand

Show lessSee more

#### Code Units referencing DDLs defined inside Stored Procedures, Anonymous Blocks, etc

In some scenarios, the deployment order may not be correct because the referenced element was defined inside another code unit. E.g.

Copy code

```
CREATE TABLE TABLE1 (
  COL1 INT
);

CREATE OR REPLACE PROCEDURE PROC1 (param1 NUMBER)
IS
BEGIN
    CREATE VIEW VIEW1
    AS
    SELECT * FROM TABLE1;
END;

CREATE VIEW VIEW2
AS SELECT * FROM VIEW1;
```

In the code above, `VIEW2` references `VIEW1`, which will be created after executing the stored procedure. `VIEW1` references `TABLE1`, so the procedure should be executed after creating the table. In that particular scenario, `VIEW1` will not be included in the top-level code units report since it is contained by the stored procedure. In that case, for `VIEW2` is not possible to know that `VIEW1` depends on PROC1 to be created, and the deployment order may not be correct because of that. The following table shows the deployment order for the code above.

| Code Unit Id | Deployment Order |
| --- | --- |
| TABLE1 | 0 |
| PROC1 | 1 |
| VIEW2 | 1 |

Expand

Show lessSee more

Despite `VIEW1` and `PROC1` having the same deployment order, `VIEW1` will fail if the procedure was not executed first.

Warning

Deployment Order support for Sequences is going to be delivered in a future version. By default, Code Units referencing sequences are not considering them to calculate the deployment order.
