# Code Conversion - Function References for Oracle

## DATEDIFF\_UDF(TIMESTAMP, NUMBER)

### Definition

This user-defined function (UDF) is used to subtract a `number` (which is a number of days) from a `timestamp`.

Copy code

```
:force:
PUBLIC.DATEDIFF_UDF(FIRST_PARAM TIMESTAMP, SECOND_PARAM NUMBER)
```

### Parameters

`FIRST_PARAM` TIMESTAMP

The `timestamp` that represents the minuend.

`SECOND_PARAM` NUMBER

The number of days that represents the subtrahend.

### Returns

Returns a timestamp with the difference between the `timestamp` and the `number`.

### Usage example

Input:

Copy code

```
:force:
SELECT PUBLIC.DATEDIFF_UDF('2024-01-26 22:00:50.708 -0800', 3);
```

Output:

Copy code

```
:force:
2024-01-23
```

## DATEDIFF\_UDF(TIMESTAMP, DATE)

### Definition

This user-defined function (UDF) is used to subtract a `date` from a `timestamp`.

Copy code

```
:force:
PUBLIC.DATEDIFF_UDF(FIRST_PARAM TIMESTAMP, SECOND_PARAM DATE)
```

### Parameters

`FIRST_PARAM` TIMESTAMP

The `timestamp` that represents the minuend.

`SECOND_PARAM` DATE

The `date` that represents the subtrahend.

### Returns

Returns an integer with the difference between the `timestamp` and the `date`.

### Usage example

Input:

Copy code

```
:force:
SELECT PUBLIC.DATEDIFF_UDF('2024-01-26 22:00:50.708 -0800', TO_DATE('2023-01-26'));
```

Output:

Copy code

```
:force:
365
```

## DATE\_TO\_JULIAN\_DAYS\_UDF

### Definition

This user-defined function (UDF) transforms from Gregorian date to Julian date (the number of days since January 1, 4712 BC).

Copy code

```
:force:
PUBLIC.DATE_TO_JULIAN_DAYS_UDF(INPUT_DATE DATE)
```

### Parameters

`INPUT_DATE` DATE

The Gregorian date to transform.

### Returns

Returns the date representation of the Julian date.

### Migration example

Input:

Copy code

```
:force:
Select TO_CHAR(SYSDATE, 'J') as A from DUAL;
```

Output:

Copy code

```
:force:
Select
PUBLIC.DATE_TO_JULIAN_DAYS_UDF(CURRENT_TIMESTAMP()) as A from DUAL;
```

### Usage example

Input:

Copy code

```
:force:
SELECT PUBLIC.DATE_TO_JULIAN_DAYS_UDF(DATE '1998-12-25');
```

Output:

Copy code

```
:force:
2451173
```

## UTL\_FILE.PUT\_LINE\_UDF

### Definition

This user-defined function (UDF) is used to replicate the functionality of the Oracle UTL\_FILE\_PUT\_LINE procedure.

Copy code

```
:force:
UTL_FILE.PUT_LINE_UDF(FILE VARCHAR,BUFFER VARCHAR)
```

### Parameters

`FILE` VARCHAR

The file to open and save the new buffer.

`BUFFER` VARCHAR

The buffer to be saved on the defined file.

### Returns

Returns a varchar with the result.

### Usage example

Warning

To review the lines in the file, there are two ways: Downloading the file from the Snowflake CLI or briefly reviewing the information with `SELECT * FROM UTL_FILE.FOPEN_TABLES_LINES;` but only if the file has not been closed.

Input:

Copy code

```
:force:
CREATE OR REPLACE PROCEDURE PROC()
RETURNS VARCHAR
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
   DECLARE
    file_data  VARIANT;
   BEGIN

    CALL UTL_FILE.FOPEN_UDF('test2.csv','a');

    SELECT
      *
    INTO
      file_data
    FROM
      TABLE(RESULT_SCAN(LAST_QUERY_ID()));

    CALL UTL_FILE.PUT_LINE_UDF(:file_data,'New line');

    CALL UTL_FILE.FCLOSE_UDF(:file_data);

   END
$$;

CALL PROC();
```

Output:

Copy code

```
:force:
null
```

## UTL\_FILE.FOPEN\_UDF (VARCHAR,VARCHAR)

### Definition

This user-defined function (UDF) is used to replicate the functionality of the Oracle `UTL_FILE_FOPEN` procedure.

Copy code

```
:force:
UTL_FILE.FOPEN_UDF(FILENAME VARCHAR,OPEN_MODE VARCHAR)
```

### Parameters

`FILENAME` VARCHAR

The file to be opened.

`OPEN_MODE` VARCHAR

Indicates the mode on which the file will be available.

### Returns

Returns a varchar with the result.

### Usage example

Warning

The `UTL_FILE.FOPEN_UDF` allows you to open a .csv file. To access the file it is required to create a `stage` for the file and use the Snowflake CLI to upload it.

Input:

Copy code

```
:force:
CREATE OR REPLACE PROCEDURE PROC()
RETURNS VARCHAR
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
   DECLARE
    file_data  VARIANT;
   BEGIN

    CALL UTL_FILE.FOPEN_UDF('test2.csv','a');

    SELECT
      *
    INTO
      file_data
    FROM
      TABLE(RESULT_SCAN(LAST_QUERY_ID()));

   END
$$;

CALL PROC();
```

Output:

Copy code

```
:force:
null
```

## JSON\_VALUE\_UDF

### Definition

This user-defined function (UDF) reproduces the JSON\_VALUE function to extract a single result out of a JSON variable.

Copy code

```
:force:
JSON_VALUE_UDF(JSON_OBJECT VARIANT, JSON_PATH STRING, RETURNING_TYPE STRING, ON_ERROR_MESSAGE VARIANT, ON_EMPTY_MESSAGE VARIANT)
```

### Parameters

`JSON_OBJECT` VARIANT

The JSON variable from which to extract the values.

`JSON_PATH` STRING

The JSON path that indicates where the values are located inside the JSON\_OBJECT.

`RETURNING_TYPE` STRING

The type to return.

`ON_ERROR_MESSAGE` VARIANT

The error message to add if needed.

`ON_EMPTY_MESSAGE` VARIANT

The error message to add in case of empty message.

### Returns

Returns a single value specified by the JSON\_PATH inside the JSON\_OBJECT. If the result is not a single value, returns a default error message or an error message defined in the input parameters.

### Usage example

Input:

Copy code

```
:force:
   SELECT
     JSON_VALUE_UDF(

     PARSE_JSON('{
  "iceCreamOrders": [
    {
      "customerID": "CUST001",
      "orderID": "ORD001",
      "productID": "PROD001",
      "quantity": 2
    }
  ]
}'),

JSON_EXTRACT_PATH_TEXT('{
  "iceCreamOrders": [
    {
      "customerID": "CUST001",
      "orderID": "ORD001",
      "productID": "PROD001",
      "quantity": 2
    }
  ]
}', 'iceCreamOrders'), 'VARIANT', TO_VARIANT('There was an error'), TO_VARIANT('Empty message'));
```

Output:

Copy code

```
:force:
"Empty message"
```

## DATEADD\_UDF (FLOAT, TIMESTAMP)

### Definition

This user-defined function (UDF) is used in cases when there is an addition between a `float` number and a `timestamp`.

Copy code

```
:force:
PUBLIC.DATEADD_UDF(FIRST_PARAM FLOAT, SECOND_PARAM TIMESTAMP)
```

### Parameters

`FIRST_PARAM` FLOAT

The timestamp number that is going to be added with the second float parameter.

`SECOND_PARAM` TIMESTAMP

The float number to be added with the timestamp in the first parameter.

### Returns

Returns a timestamp with the addition between the timestamp and the float number specified.

### Usage example

Input:

Copy code

```
:force:
SELECT DATEADD_UDF(1, current_timestamp);
```

Output:

Copy code

```
:force:
2024-01-30 18:47:16.988
```

## FETCH\_BULK\_COLLECTIONS\_UDF (OBJECT)

### Definition

This user-defined function (UDF) is used to replicate the functionality of fetching bulk for collections in Oracle. This function version receives the cursor only.

Copy code

```
:force:
FETCH_BULK_COLLECTIONS_UDF(CURSOR OBJECT)
```

### Parameters

`CURSOR` OBJECT

The cursor that is processed and filled with the data in the `fetch bulk collection`.

### Returns

Returns an object with information related to the logic of fetching bulk collections.

### Usage example

Input:

Copy code

```
:force:

CREATE OR REPLACE TABLE MY_TABLE (test VARCHAR(100));
INSERT INTO MY_TABLE VALUES ('TEST_A');

CREATE OR REPLACE PROCEDURE MY_PROCEDURE ()
RETURNS OBJECT
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
    DECLARE
        MY_CURSOR OBJECT := INIT_CURSOR_UDF('MY_CURSOR', '   SELECT * FROM
      MY_TABLE');

    BEGIN
        MY_CURSOR := (
            CALL OPEN_BULK_CURSOR_UDF(:MY_CURSOR)
        );
        MY_CURSOR := (
            CALL FETCH_BULK_COLLECTIONS_UDF(:MY_CURSOR)
        );

        Return MY_CURSOR;
    END;
$$;

CALL MY_PROCEDURE();
```

Output:

Copy code

```
:force:
{
  "FOUND": true,
  "ISOPEN": true,
  "NAME": "MY_CURSOR",
  "NOTFOUND": false,
  "QUERY": "   SELECT * FROM\n      MY_TABLE",
  "RESULT": [
    [
      "TEST_A"
    ]
  ],
  "ROWCOUNT": 1
}
```

## DATEADD\_UDF (DATE, FLOAT)

### Definition

This user-defined function (UDF) is used in cases when there is an addition between a date and a type as `float` or `timestamp`.

Copy code

```
:force:
PUBLIC.DATEADD_UDF(FIRST_PARAM DATE, SECOND_PARAM FLOAT)
```

### Parameters

`FIRST_PARAM` DATE

The date to be added with the number in the second parameter.

`SECOND_PARAM` FLOAT

The float number that is going to be added with the first date parameter.

### Returns

Returns the addition between the date and the float number specified.

### Migration example

Input:

Copy code

```
:force:
SELECT TO_DATE('05/11/21', 'dd/mm/yy') + 3.4 from dual;
```

Output:

Copy code

```
:force:
SELECT
PUBLIC.DATEADD_UDF( TO_DATE('05/11/21', 'dd/mm/yy'), 3.4) from dual;
```

### Usage example

Input:

Copy code

```
:force:
SELECT DATEADD_UDF('2022-02-14',6);
```

Output:

Copy code

```
:force:
2022-02-20
```

## DATEDIFF\_UDF(DATE, TIMESTAMP)

### Definition

This user-defined function (UDF) is used to subtract a `timestamp` from a `date`.

Copy code

```
:force:
PUBLIC.DATEDIFF_UDF(FIRST_PARAM DATE, SECOND_PARAM TIMESTAMP)
```

### Parameters

`FIRST_PARAM` DATE

The date on which the subtraction is performed.

`SECOND_PARAM` TIMESTAMP

The `timestamp` to subtract from the first parameter.

### Returns

Returns an integer with the days between the first and the second parameter.

### Usage example

Input:

Copy code

```
:force:
SELECT PUBLIC.DATEDIFF_UDF(TO_DATE('2024-01-26'), '2022-02-14 15:31:00');
```

Output:

Copy code

```
:force:
711
```

## DBMS\_RANDOM.VALUE\_UDF

### Definition

This user-defined function (UDF) is to replicate the functionality of the Oracle DBMS\_RANDOM.VALUE function.

Copy code

```
:force:
DBMS_RANDOM.VALUE_UDF()
```

### Parameters

No input parameters.

### Returns

Returns a `double` number with a random number.

### Usage example

Input:

Copy code

```
:force:
SELECT DBMS_RANDOM.VALUE_UDF();
```

Output:

Copy code

```
:force:
0.6666235896
```

## DBMS\_RANDOM.VALUE\_UDF (DOUBLE, DOUBLE)

### Definition

This user-defined function (UDF) is to replicate the functionality of the Oracle DBMS\_RANDOM.VALUE function.

Copy code

```
:force:
DBMS_RANDOM.VALUE_UDF(low DOUBLE, high DOUBLE)
```

### Parameters

`low` DOUBLE

The initial limit to be considered.

`high` DOUBLE

The delimiting limit that coordinates with the first parameter.

### Returns

Returns a `double` number with a random number between the limits specified.

### Usage example

Input:

Copy code

```
:force:
SELECT DBMS_RANDOM.VALUE_UDF(1.1, 2.2);
```

Output:

Copy code

```
:force:
1.637802374
```

## FETCH\_BULK\_RECORD\_COLLECTIONS\_UDF (OBJECT, ARRAY)

### Definition

This user-defined function (UDF) is used to cover the functionality of `fetch bulk records` with different input parameters that determine the information added or the behavior of the cursor.

Copy code

```
:force:
FETCH_BULK_RECORD_COLLECTIONS_UDF(CURSOR OBJECT, COLUMN_NAMES ARRAY)
```

### Parameters

`CURSOR` OBJECT

The cursor that is being processed.

`COLUMN_NAMES` ARRAY

The column names that are associated with the cursor.

### Returns

Returns an object with the processed information.

### Usage example

Input:

Copy code

```
:force:

CREATE OR REPLACE TABLE BULKCOLLECTTABLE(test VARCHAR(100));
INSERT INTO BULKCOLLECTTABLE VALUES ('TEST_A');

CREATE OR REPLACE PROCEDURE MY_PROCEDURE ()
RETURNS OBJECT
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
    DECLARE
        MY_CURSOR OBJECT := INIT_CURSOR_UDF('MY_CURSOR', '   SELECT * FROM
      BULKCOLLECTTABLE');

    BEGIN
        MY_CURSOR := (
            CALL OPEN_BULK_CURSOR_UDF(:MY_CURSOR)
        );
        MY_CURSOR := (
            CALL FETCH_BULK_RECORD_COLLECTIONS_UDF(:MY_CURSOR, NULL)
        );

        Return MY_CURSOR;
    END;
$$;

CALL MY_PROCEDURE();
```

Output:

Copy code

```
:force:
{
  "FOUND": true,
  "ISOPEN": true,
  "NAME": "MY_CURSOR",
  "NOTFOUND": false,
  "QUERY": "   SELECT * FROM\n      BULKCOLLECTTABLE",
  "RESULT": {
    "TEST": [
      "TEST_A"
    ]
  },
  "ROWCOUNT": 1
}
```

## FETCH\_BULK\_COLLECTION\_RECORDS\_UDF (OBJECT, ARRAY)

### Definition

This user-defined function (UDF) is used to replicate the functionality of FETCH in Oracle. This is the variation where it receives the cursor and the column names.

Copy code

```
:force:
FETCH_BULK_COLLECTION_RECORDS_UDF(CURSOR OBJECT, COLUMN_NAMES ARRAY)
```

### Parameters

`CURSOR` OBJECT

The cursor that is processed and filled with the data in the `fetch bulk`.

`COLUMN_NAMES` ARRAY

The name associated with the column is not the initial name.

### Returns

Returns an object with the records from the `fetch bulk`.

### Usage example

Input:

Copy code

```
:force:

CREATE OR REPLACE TABLE MY_TABLE (test VARCHAR(100));
INSERT INTO MY_TABLE VALUES ('TEST_A');

CREATE OR REPLACE PROCEDURE MY_PROCEDURE ()
RETURNS OBJECT
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
    DECLARE
        MY_CURSOR OBJECT := INIT_CURSOR_UDF('MY_CURSOR', '   SELECT * FROM
      MY_TABLE');

    BEGIN
        MY_CURSOR := (
            CALL OPEN_BULK_CURSOR_UDF(:MY_CURSOR)
        );
        MY_CURSOR := (
            CALL FETCH_BULK_COLLECTION_RECORDS_UDF(:MY_CURSOR, NULL)
        );

        Return MY_CURSOR;
    END;
$$;

CALL MY_PROCEDURE();
```

Output:

Copy code

```
:force:
{
  "FOUND": true,
  "ISOPEN": true,
  "NAME": "MY_CURSOR",
  "NOTFOUND": false,
  "QUERY": "   SELECT * FROM\n      MY_TABLE",
  "RESULT": [
    {
      "TEST": "TEST_A"
    }
  ],
  "ROWCOUNT": 1
}
```

## JULIAN\_TO\_GREGORIAN\_DATE\_UDF

### Definition

This user-defined function (UDF) is used to transform a Julian date into the formats: JD Edwards, YYYYDDD (astronomical), and YYYYDDD (ordinal).

Copy code

```
:force:
JULIAN_TO_GREGORIAN_DATE_UDF(JULIAN_DATE CHAR(7), FORMAT_SELECTED CHAR(1))
```

### Parameters

`JULIAN_DATE` CHAR

The Julian date to transform.

`FORMAT_SELECTED` CHAR

The format required for the logic. E.g. `'E'`, `'J'`, `'R'`. Astronomy standardized or `'J'` is the default format.

### Returns

Returns a variant with the date representation of the Julian date.

### Usage example

Input:

Copy code

```
:force:
SELECT JULIAN_TO_GREGORIAN_DATE_UDF('098185');
```

Output:

Copy code

```
:force:
'1998-07-04' --(a.k.a Sat Jul 04 1998)
```

## TIMESTAMP\_DIFF\_UDF

### Definition

This user-defined function (UDF) is used for the timestamps arithmetic operations and the equivalence functionality in Snowflake.

Copy code

```
:force:
TIMESTAMP_DIFF_UDF(LEFT_TS TIMESTAMP, RIGHT_TS TIMESTAMP )
```

### Parameters

LEFT\_TS TIMESTAMP

The minuend value.

RIGHT\_TS TIMESTAMP

The subtrahend value.

### Returns

Returns a varchar with the resulting difference between timestamps.

### Usage example

Input:

Copy code

```
:force:
SELECT TIMESTAMP_DIFF_UDF(TO_TIMESTAMP('2024-01-31 11:47:20.532 -0800'), TO_TIMESTAMP('2024-01-31 11:47:20.532 -0800'));
```

Output:

Copy code

```
:force:
-000000000  00:00:00.00000000
```

## REGEXP\_LIKE\_UDF (STRING, STRING, STRING)

### Definition

This user-defined function (UDF) is used to support the Oracle `REGEXP_LIKE` functionality with a match parameter for case sensitivity.

Copy code

```
:force:
REGEXP_LIKE_UDF(COL STRING, PATTERN STRING, MATCHPARAM STRING)
```

### Parameters

COL STRING

The string to be evaluated with the pattern.

PATTERN STRING

The pattern to be checked.

MATCHPARAM STRING

The match parameter that will determine whether the match is case-sensitive or not.

### Returns

Returns a boolean expression. True if the pattern matches the string; otherwise, false.

### Usage example

Input:

Copy code

```
:force:
SELECT REGEXP_LIKE_UDF('san Francisco', 'San* [fF].*', 'i');
```

Output:

Copy code

```
:force:
TRUE
```

## FETCH\_BULK\_COLLECTIONS\_UDF (OBJECT, FLOAT)

### Definition

This user-defined function (UDF) is used to replicate the functionality of fetching bulk for collections in Oracle. This function version receives the cursor and the limit value for the row count.

Copy code

```
:force:
FETCH_BULK_COLLECTIONS_UDF(CURSOR OBJECT, LIMIT FLOAT)
```

### Parameters

`CURSOR` OBJECT

The cursor that is processed and filled with the data in the `fetch bulk collection`.

`LIMIT` FLOAT

The limit for the records to call.

### Returns

Returns an object with information related to the logic of fetching bulk collections.

### Usage example

Input:

Copy code

```
:force:

CREATE OR REPLACE TABLE MY_TABLE (test VARCHAR(100));
INSERT INTO MY_TABLE VALUES ('TEST_A');

CREATE OR REPLACE PROCEDURE MY_PROCEDURE ()
RETURNS OBJECT
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
    DECLARE
        MY_CURSOR OBJECT := INIT_CURSOR_UDF('MY_CURSOR', '   SELECT * FROM
      MY_TABLE');

    BEGIN
        MY_CURSOR := (
            CALL OPEN_BULK_CURSOR_UDF(:MY_CURSOR)
        );
        MY_CURSOR := (
            CALL FETCH_BULK_COLLECTIONS_UDF(:MY_CURSOR, 1.0)
        );

        Return MY_CURSOR;
    END;
$$;

CALL MY_PROCEDURE();
```

Output:

Copy code

```
:force:
{
  "FOUND": true,
  "ISOPEN": true,
  "NAME": "MY_CURSOR",
  "NOTFOUND": false,
  "QUERY": "   SELECT * FROM\n      MY_TABLE",
  "RESULT": [
    [
      "TEST_A"
    ]
  ],
  "ROWCOUNT": 1
}
```

## INIT\_CURSOR\_UDF

### Definition

This user-defined function (UDF) is to initialize a cursor object with the equivalent functionality.

Copy code

```
:force:
INIT_CURSOR_UDF(NAME VARCHAR, QUERY VARCHAR)
```

### Parameters

`NAME` VARCHAR

The name of the cursor.

`QUERY` VARCHAR

The query that is associated with the cursor.

### Returns

Returns an object with the cursor information.

### Usage example

Input:

Copy code

```
:force:
CREATE OR REPLACE TABLE BULKCOLLECTTABLE(test VARCHAR(100));

CREATE OR REPLACE PROCEDURE MY_PROCEDURE ()
RETURNS OBJECT
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
    DECLARE
        MY_CURSOR OBJECT := INIT_CURSOR_UDF('MY_CURSOR', '   SELECT * FROM
      BULKCOLLECTTABLE');

    BEGIN
        Return MY_CURSOR;
    END;
$$;

CALL MY_PROCEDURE();
```

Output:

Copy code

```
:force:
{
  "ISOPEN": false,
  "NAME": "MY_CURSOR",
  "QUERY": "   SELECT * FROM\n      BULKCOLLECTTABLE",
  "ROWCOUNT": -1
}
```

## UPDATE\_PACKAGE\_VARIABLE\_STATE\_UDF

### Definition

This user-defined function (UDF) updates the given package variable values. It is a wrapper for the Snowflake SETVARIABLE() function.

Copy code

```
:force:
UPDATE_PACKAGE_VARIABLE_STATE_UDF (VARIABLE VARCHAR, NEW_VALUE VARCHAR)
```

### Parameters

`VARIABLE` VARCHAR

The variable name to set the value.

`NEW_VALUE` VARCHAR

The value that will be stored.

### Returns

Returns a varchar with the information of the updated variable.

### Usage example

Warning

Please, review the existence of the variable.

Input:

Copy code

```
:force:
CALL PUBLIC.UPDATE_PACKAGE_VARIABLE_STATE_UDF('MY_LOCAL_VARIABLE', '1');
```

Output:

Copy code

```
:force:
1
```

## OPEN\_BULK\_CURSOR\_UDF (OBJECT)

### Definition

This user-defined function (UDF) is used to open a cursor without bindings.

Copy code

```
:force:
OPEN_BULK_CURSOR_UDF(CURSOR OBJECT)
```

### Parameters

`CURSOR` OBJECT

The cursor to process as open.

### Returns

Returns an object with the current information of the cursor.

### Usage example

Input:

Copy code

```
:force:

CREATE OR REPLACE TABLE BULKCOLLECTTABLE(test VARCHAR(100));

CREATE OR REPLACE PROCEDURE MY_PROCEDURE ()
RETURNS OBJECT
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
    DECLARE
        MY_CURSOR OBJECT := INIT_CURSOR_UDF('MY_CURSOR', '   SELECT * FROM
      BULKCOLLECTTABLE');

    BEGIN
        MY_CURSOR := (
            CALL OPEN_BULK_CURSOR_UDF(:MY_CURSOR)
        );
        Return MY_CURSOR;
    END;
$$;

CALL MY_PROCEDURE();
```

Output:

Copy code

```
:force:
{
  "ISOPEN": true,
  "NAME": "MY_CURSOR",
  "QUERY": "   SELECT * FROM\n      BULKCOLLECTTABLE",
  "ROWCOUNT": 0
}
```

## DATEADD\_UDF (TIMESTAMP, FLOAT)

### Definition

This user-defined function (UDF) is used in cases when there is an addition between a `timestamp` and a `float` number.

Copy code

```
:force:
PUBLIC.DATEADD_UDF(FIRST_PARAM TIMESTAMP, SECOND_PARAM FLOAT)
```

### Parameters

`FIRST_PARAM` TIMESTAMP

The timestamp number that is going to be added with the second float parameter.

`SECOND_PARAM` FLOAT

The float number to be added with the timestamp in the first parameter.

### Returns

Returns a timestamp with the addition between the timestamp and the float number specified.

### Usage example

Input:

Copy code

```
:force:
SELECT DATEADD_UDF(current_timestamp, 1);
```

Output:

Copy code

```
:force:
2024-01-26 13:22:49.354
```

## DATEDIFF\_UDF(TIMESTAMP, TIMESTAMP)

### Definition

This user-defined function (UDF) subtracts a `timestamp` from another `timestamp`.

Copy code

```
:force:
PUBLIC.DATEDIFF_UDF(FIRST_PARAM TIMESTAMP, SECOND_PARAM TIMESTAMP)
```

### Parameters

`FIRST_PARAM` TIMESTAMP

The `timestamp` that represents the minuend.

`SECOND_PARAM` TIMESTAMP

The `timestamp` that represents the subtrahend.

### Returns

Returns an integer with the difference of days between the first and the second timestamps.

### Usage example

Input:

Copy code

```
:force:
SELECT PUBLIC.DATEDIFF_UDF('2024-01-26 22:00:50.708 -0800','2023-01-26 22:00:50.708 -0800');
```

Output:

Copy code

```
:force:
365
```

## UTL\_FILE.FCLOSE\_UDF

### Definition

This user-defined function (UDF) is used to replicate the functionality of the Oracle `UTL_FILE_FCLOSE` procedure.

Copy code

```
:force:
UTL_FILE.FCLOSE_UDF(FILE VARCHAR)
```

### Parameters

`FILE` VARCHAR

The file to process and close.

### Returns

Returns a varchar with the result.

### Usage example

Warning

The `UTL_FILE.FCLOSE_UDF` closes the file that is being processed. To review the result or handle files, it is required to use the Snowflake CLI console. The Snowflake CLI console allows the upload or download of a file.

Input:

Copy code

```
:force:
CREATE OR REPLACE PROCEDURE PROC()
RETURNS VARCHAR
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
   DECLARE
    file_data  VARIANT;
   BEGIN

    CALL UTL_FILE.FOPEN_UDF('test2.csv','a');

    SELECT
      *
    INTO
      file_data
    FROM
      TABLE(RESULT_SCAN(LAST_QUERY_ID()));

    CALL UTL_FILE.PUT_LINE_UDF(:file_data,'New line');

    CALL UTL_FILE.FCLOSE_UDF(:file_data);

   END
$$;

CALL PROC();
```

Output:

Copy code

```
:force:
null
```

## FETCH\_BULK\_RECORD\_COLLECTIONS\_UDF (OBJECT)

### Definition

This user-defined function (UDF) is used to cover the functionality of `fetch bulk records` with different input parameters that determine the information added or the behavior of the cursor.

Copy code

```
:force:
FETCH_BULK_RECORD_COLLECTIONS_UDF(CURSOR OBJECT)
```

### Parameters

`CURSOR` OBJECT

The cursor that is being processed.

### Returns

Returns an object with the processed information.

### Usage example

Input:

Copy code

```
:force:
CREATE OR REPLACE TABLE BULKCOLLECTTABLE(test VARCHAR(100));
INSERT INTO BULKCOLLECTTABLE VALUES ('TEST_A');

CREATE OR REPLACE PROCEDURE MY_PROCEDURE ()
RETURNS OBJECT
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
    DECLARE
        MY_CURSOR OBJECT := INIT_CURSOR_UDF('MY_CURSOR', '   SELECT * FROM
      BULKCOLLECTTABLE');

    BEGIN
        MY_CURSOR := (
            CALL OPEN_BULK_CURSOR_UDF(:MY_CURSOR)
        );
        MY_CURSOR := (
            CALL FETCH_BULK_RECORD_COLLECTIONS_UDF(:MY_CURSOR)
        );

        Return MY_CURSOR;
    END;
$$;

CALL MY_PROCEDURE();
```

Output:

Copy code

```
:force:
{
  "FOUND": true,
  "ISOPEN": true,
  "NAME": "MY_CURSOR",
  "NOTFOUND": false,
  "QUERY": "   SELECT * FROM\n      BULKCOLLECTTABLE",
  "RESULT": {
    "TEST": [
      "TEST_A"
    ]
  },
  "ROWCOUNT": 1
}
```

## CAST\_DATE\_UDF

### Definition

The function processes a timestamp in string format to a date. It returns a date with the specified format.

Copy code

```
:force:
PUBLIC.CAST_DATE_UDF(DATESTR STRING)
```

### Parameters

`DATESTR` STRING

The date as a `string` to be formatted. The format should be `'YYYY-MM-DD"T"HH24:MI:SS.FF'` e.g. `'2024-01-25T23:25:11.120'`.

Please review the following information about formatting [here](https://docs.snowflake.com/en/sql-reference/date-time-input-output#timestamp-formats).

### Returns

Returns a `date` with the new format applied.

### Usage example

Input:

Copy code

```
:force:
SELECT PUBLIC.CAST_DATE_UDF('2024-01-25T23:25:11.120');
```

Output:

Copy code

```
:force:
2024-01-25
```

## FETCH\_BULK\_COLLECTION\_RECORDS\_UDF (OBJECT, FLOAT, ARRAY)

### Definition

This user-defined function (UDF) is used to replicate the functionality of FETCH in Oracle. This is the variation where it receives the cursor, the limit, and the column names.

Copy code

```
:force:
FETCH_BULK_COLLECTION_RECORDS_UDF(CURSOR OBJECT, LIMIT FLOAT, COLUMN_NAMES ARRAY)
```

### Parameters

`CURSOR` OBJECT

The cursor that is processed and filled with the data in the `fetch bulk`.

`LIMIT` FLOAT

The limit for the records to call.

`COLUMN_NAMES` ARRAY

The name associated with the column is not the initial name.

### Returns

Returns an object with the records from the `fetch bulk`.

### Usage example

Input:

Copy code

```
:force:
CREATE OR REPLACE TABLE MY_TABLE (test VARCHAR(100));
INSERT INTO MY_TABLE VALUES ('TEST_A');

CREATE OR REPLACE PROCEDURE MY_PROCEDURE ()
RETURNS OBJECT
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
    DECLARE
        MY_CURSOR OBJECT := INIT_CURSOR_UDF('MY_CURSOR', '   SELECT * FROM
      MY_TABLE');

    BEGIN
        MY_CURSOR := (
            CALL OPEN_BULK_CURSOR_UDF(:MY_CURSOR)
        );
        MY_CURSOR := (
            CALL FETCH_BULK_COLLECTION_RECORDS_UDF(:MY_CURSOR, 1.0, NULL)
        );

        Return MY_CURSOR;
    END;
$$;

CALL MY_PROCEDURE();
```

Output:

Copy code

```
:force:
{
  "FOUND": true,
  "ISOPEN": true,
  "NAME": "MY_CURSOR",
  "NOTFOUND": false,
  "QUERY": "   SELECT * FROM\n      MY_TABLE",
  "RESULT": [
    {
      "TEST": "TEST_A"
    }
  ],
  "ROWCOUNT": 1
}
```

## DATEDIFF\_UDF(DATE, INTEGER)

### Definition

This user-defined function (UDF) applies a subtraction of days over a date.

Copy code

```
:force:
PUBLIC.DATEDIFF_UDF(FIRST_PARAM DATE, SECOND_PARAM INTEGER)
```

### Parameters

`FIRST_PARAM` DATE

The initial date to apply the subtraction.

`SECOND_PARAM` INTEGER

The number of days to be subtracted from the first date parameter.

### Returns

Returns the date after subtracting the indicated number of days.

### Usage example

Input:

Copy code

```
:force:
SELECT PUBLIC.DATEDIFF_UDF(TO_DATE('2024-01-26'), 365);
```

Output:

Copy code

```
:force:
2023-01-26
```

## DATE\_TO\_RR\_FORMAT\_UDF

### Definition

This user-defined function (UDF) transforms from date to Oracle RR datetime format

Copy code

```
:force:
PUBLIC.DATE_TO_RR_FORMAT_UDF(INPUT_DATE DATE)
```

### Parameters

`INPUT_DATE` DATE

The date to transform.

### Returns

The input date with years adjusted to RR format.

### Migration example

Input:

Copy code

```
:force:
Select TO_DATE('17-NOV-30','DD-MON-RR') as A from DUAL;
```

Output:

Copy code

```
:force:
Select
PUBLIC.DATE_TO_RR_FORMAT_UDF( TO_DATE('17-NOV-30', 'DD-MON-YY')) as A from DUAL;
```

### Usage example

Input:

Copy code

```
:force:
PUBLIC.DATE_TO_RR_FORMAT_UDF(TO_DATE('17-NOV-30','DD-MON-YY')) as A from DUAL;
```

Output:

Copy code

```
:force:
2030-11-17
```

## FETCH\_BULK\_RECORD\_COLLECTIONS\_UDF (OBJECT, INTEGER)

### Definition

This user-defined function (UDF) is used to cover the functionality of `fetch bulk records` with different input parameters that determine the information added or the behavior of the cursor.

Copy code

```
:force:
FETCH_BULK_RECORD_COLLECTIONS_UDF(CURSOR OBJECT, LIMIT INTEGER)
```

### Parameters

`CURSOR` OBJECT

The cursor that is being processed.

`LIMIT` INTEGER

The limit of the row count.

### Returns

Returns an object with the processed information.

### Usage example

Input:

Copy code

```
:force:
CREATE OR REPLACE TABLE BULKCOLLECTTABLE(test VARCHAR(100));
INSERT INTO BULKCOLLECTTABLE VALUES ('TEST_A');

CREATE OR REPLACE PROCEDURE MY_PROCEDURE ()
RETURNS OBJECT
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
    DECLARE
        MY_CURSOR OBJECT := INIT_CURSOR_UDF('MY_CURSOR', '   SELECT * FROM
      BULKCOLLECTTABLE');

    BEGIN
        MY_CURSOR := (
            CALL OPEN_BULK_CURSOR_UDF(:MY_CURSOR)
        );
        MY_CURSOR := (
            CALL FETCH_BULK_RECORD_COLLECTIONS_UDF(:MY_CURSOR, 0)
        );

        Return MY_CURSOR;
    END;
$$;

CALL MY_PROCEDURE();
```

Output:

Copy code

```
:force:
{
  "FOUND": false,
  "ISOPEN": true,
  "NAME": "MY_CURSOR",
  "NOTFOUND": true,
  "QUERY": "   SELECT * FROM\n      BULKCOLLECTTABLE",
  "RESULT": {
    "TEST": []
  },
  "ROWCOUNT": 0
}
```

## DBMS\_OUTPUT.PUT\_LINE\_UDF

### Definition

This user-defined function (UDF) is used to replicate the functionality of the Oracle DBMS\_OUTPUT\_PUT\_LINE function.

Copy code

```
:force:
DBMS_OUTPUT.PUT_LINE_UDF(LOG VARCHAR)
```

Warning

Notice that performance may be affected by using this UDF. To start logging information uncomment the implementation inside the function.

### Parameters

`LOG` VARCHAR

The information to be shown in the command line.

### Returns

Returns a `varchar` with the information logged.

### Usage example

Input:

Copy code

```
:force:
SELECT DBMS_OUTPUT.PUT_LINE_UDF(to_varchar(123));
```

Output:

Copy code

```
:force:
123
```

## DATEDIFF\_UDF(DATE, DATE)

### Definition

This user-defined function (UDF) is used when there is a subtraction between two dates.

Copy code

```
:force:
PUBLIC.DATEDIFF_UDF(FIRST_PARAM DATE, SECOND_PARAM DATE)
```

### Parameters

`FIRST_PARAM` DATE

The date that represents the minuend in the subtraction.

`SECOND_PARAM` DATE

The date that represents the subtrahend in the subtraction.

### Returns

Returns an integer with the number of days between the dates.

### Usage example

Input:

Copy code

```
:force:
SELECT PUBLIC.DATEDIFF_UDF(TO_DATE('2024-01-26'), TO_DATE('2023-01-26'));
```

Output:

Copy code

```
:force:
365
```

## OPEN\_BULK\_CURSOR\_UDF (OBJECT, ARRAY)

### Definition

This user-defined function (UDF) is used to open a cursor with bindings.

Copy code

```
:force:
OPEN_BULK_CURSOR_UDF(CURSOR OBJECT, BINDINGS ARRAY)
```

### Parameters

`CURSOR` OBJECT

The cursor to process as open.

`BINDINGS` ARRAY

The binding that is related to the cursor.

### Returns

Returns an object with the current information of the cursor.

### Usage example

Input:

Copy code

```
:force:

CREATE OR REPLACE TABLE BULKCOLLECTTABLE(test VARCHAR(100));

CREATE OR REPLACE PROCEDURE MY_PROCEDURE ()
RETURNS OBJECT
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
    DECLARE
        MY_CURSOR OBJECT := INIT_CURSOR_UDF('MY_CURSOR', '   SELECT * FROM
      BULKCOLLECTTABLE');

    BEGIN
        MY_CURSOR := (
            CALL OPEN_BULK_CURSOR_UDF(:MY_CURSOR, NULL)
        );
        Return MY_CURSOR;
    END;
$$;

CALL MY_PROCEDURE();
```

Output:

Copy code

```
:force:
{
  "ISOPEN": true,
  "NAME": "MY_CURSOR",
  "QUERY": "   SELECT * FROM\n      BULKCOLLECTTABLE",
  "ROWCOUNT": 0
}
```

## CLOSE\_BULK\_CURSOR\_UDF

### Definition

This user-defined function (UDF) deletes the temporary table that stores the result set of the cursor and resets the cursor properties to their initial state.

Copy code

```
:force:
CLOSE_BULK_CURSOR_UDF(CURSOR OBJECT)
```

### Parameters

`CURSOR` OBJECT

The cursor that is checked and closed.

### Returns

Returns an object with the cursor properties reset.

### Migration example

Input:

Copy code

```
:force:
-- [procedure initial logic]
CLOSE C1;
-- [procedure ending logic]
```

Output:

Copy code

```
:force:
C1 := (
            CALL CLOSE_BULK_CURSOR_UDF(:C1)
        );
```

### Usage example

Input:

Copy code

```
:force:
CREATE OR REPLACE TABLE BULKCOLLECTTABLE(test VARCHAR(100));

CREATE OR REPLACE PROCEDURE MY_PROCEDURE ()
RETURNS OBJECT
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
    DECLARE
        MY_CURSOR OBJECT := INIT_CURSOR_UDF('MY_CURSOR', '   SELECT * FROM
      BULKCOLLECTTABLE');

    BEGIN
        MY_CURSOR := (
            CALL OPEN_BULK_CURSOR_UDF(:MY_CURSOR)
        );
        MY_CURSOR := (
            CALL CLOSE_BULK_CURSOR_UDF(:MY_CURSOR)
        );

        RETURN MY_CURSOR;
    END;
$$;
```

Output:

Copy code

```
:force:
{
  "FOUND": null,
  "ISOPEN": false,
  "NAME": "MY_CURSOR",
  "NOTFOUND": null,
  "QUERY": "   SELECT * FROM\n      BULKCOLLECTTABLE",
  "ROWCOUNT": -1
}
```

## DATEADD\_UDF (FLOAT, DATE)

### Definition

This user-defined function (UDF) is used in cases when there is an addition between a type as `float` or `timestamp` and a `date`.

Copy code

```
:force:
PUBLIC.DATEADD_UDF(FIRST_PARAM FLOAT, SECOND_PARAM DATE)
```

### Parameters

`FIRST_PARAM` FLOAT

The float number that is going to be added with the second date parameter.

`SECOND_PARAM` DATE

The date to be added with the number in the first parameter.

### Returns

Returns the addition between the float number and the date specified.

### Usage example

Input:

Copy code

```
:force:
SELECT DATEADD_UDF(6, '2022-02-14');
```

Output:

Copy code

```
:force:
2022-02-20
```

## BFILENAME\_UDF

### Definition

The function takes the directory name and the filename parameter as a `string`. Then, it returns a concatenation using the `'\'.`

Warning

The character `'\'` must be changed to match the Operating System file concatenation character.

Copy code

```
:force:
PUBLIC.BFILENAME_UDF (DIRECTORYNAME STRING, FILENAME STRING);
```

### Parameters

`DIRECTORYNAME` STRING

The directory name to be processed as a `string`.

`FILENAME` STRING

The filename to be concatenated.

### Returns

Returns a `string` that contains the directory name and filename concatenated by a `'\'`.

### Migration example

Input:

Copy code

```
:force:
SELECT BFILENAME ('directory', 'filename.jpg') FROM DUAL;
```

Output:

Copy code

```
:force:
SELECT
PUBLIC.BFILENAME_UDF('directory', 'filename.jpg') FROM DUAL;
```

### Usage example

Input:

Copy code

```
:force:
SELECT PUBLIC.BFILENAME_UDF('directory', 'filename.jpg');
```

Output:

Copy code

```
:force:
directory\filename.jpg
```

## REGEXP\_LIKE\_UDF (STRING, STRING)

### Definition

This user-defined function (UDF) is used to support the Oracle `REGEXP_LIKE` functionality.

Copy code

```
:force:
REGEXP_LIKE_UDF(COL STRING, PATTERN STRING)
```

### Parameters

COL STRING

The string to be evaluated with the pattern.

PATTERN STRING

The pattern to be checked.

### Returns

Returns a boolean expression. True if the pattern matches the string; otherwise, false.

### Usage example

Input:

Copy code

```
:force:
SELECT REGEXP_LIKE_UDF('San Francisco', 'San* [fF].*');
```

Output:

Copy code

```
:force:
TRUE
```

## UTL\_FILE.FOPEN\_UDF (VARCHAR, VARCHAR, VARCHAR)

### Definition

This user-defined function (UDF) is used to replicate the functionality of the Oracle `UTL_FILE_FOPEN` procedure.

Copy code

```
:force:
UTL_FILE.FOPEN_UDF(PACKAGE_VARIABLE VARCHAR, FILENAME VARCHAR, OPEN_MODE VARCHAR)
```

### Parameters

`PACKAGE_VARIABLE` VARCHAR

The variable related to the file opening.

`FILENAME` VARCHAR

The file to be opened.

`OPEN_MODE` VARCHAR

Indicates the mode on which the file will be available.

### Returns

Returns a varchar with the result.

### Usage example

Warning

The `UTL_FILE.FOPEN_UDF` allows you to open a .csv file. To access the file it is required to create a `stage` for the file and use the Snowflake CLI to upload it.

Input:

Copy code

```
:force:

CREATE OR REPLACE PROCEDURE PROC()
RETURNS VARCHAR
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
   DECLARE
    file_data  VARIANT;
   BEGIN

    CALL UTL_FILE.FOPEN_UDF(NULL, 'test2.csv','a');

    SELECT
      *
    INTO
      file_data
    FROM
      TABLE(RESULT_SCAN(LAST_QUERY_ID()));

    CALL UTL_FILE.PUT_LINE_UDF(:file_data,'New line');

    CALL UTL_FILE.FCLOSE_UDF(:file_data);

   END
$$;

CALL PROC();
```

Output:

Copy code

```
:force:
null
```

## FETCH\_BULK\_COLLECTION\_RECORDS\_UDF (OBJECT)

### Definition

This user-defined function (UDF) is used to replicate the functionality of FETCH in Oracle. This is the variation where it receives the cursor only.

Copy code

```
:force:
FETCH_BULK_COLLECTION_RECORDS_UDF(CURSOR OBJECT)
```

### Parameters

`CURSOR` OBJECT

The cursor that is processed and filled with the data in the `fetch bulk`.

### Returns

Returns an object with the records from the `fetch bulk`.

### Usage example

Input:

Copy code

```
:force:
CREATE OR REPLACE TABLE MY_TABLE (test VARCHAR(100));
INSERT INTO MY_TABLE VALUES ('TEST_A');

CREATE OR REPLACE PROCEDURE MY_PROCEDURE ()
RETURNS OBJECT
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
    DECLARE
        MY_CURSOR OBJECT := INIT_CURSOR_UDF('MY_CURSOR', '   SELECT * FROM
      MY_TABLE');

    BEGIN
        MY_CURSOR := (
            CALL OPEN_BULK_CURSOR_UDF(:MY_CURSOR)
        );
        MY_CURSOR := (
            CALL FETCH_BULK_COLLECTION_RECORDS_UDF(:MY_CURSOR)
        );

        Return MY_CURSOR;
    END;
$$;

CALL MY_PROCEDURE();
```

Output:

Copy code

```
:force:
{
  "FOUND": true,
  "ISOPEN": true,
  "NAME": "MY_CURSOR",
  "NOTFOUND": false,
  "QUERY": "   SELECT * FROM\n      MY_TABLE",
  "RESULT": [
    {
      "TEST": "TEST_A"
    }
  ],
  "ROWCOUNT": 1
}
```

## FETCH\_BULK\_RECORD\_COLLECTIONS\_UDF (OBJECT, FLOAT, ARRAY)

### Definition

This user-defined function (UDF) is used to cover the functionality of `fetch bulk records` with different input parameters that determine the information added or the behavior of the cursor.

Copy code

```
:force:
FETCH_BULK_RECORD_COLLECTIONS_UDF(CURSOR OBJECT, LIMIT FLOAT, COLUMN_NAMES ARRAY)
```

### Parameters

`CURSOR` OBJECT

The cursor that is being processed.

`LIMIT` FLOAT

The limit of the row count.

`COLUMN_NAMES` ARRAY

The column names that are associated with the cursor.

### Returns

Returns an object with the processed information.

### Usage example

Input:

Copy code

```
:force:
CREATE OR REPLACE TABLE BULKCOLLECTTABLE(test VARCHAR(100));
INSERT INTO BULKCOLLECTTABLE VALUES ('TEST_A');

CREATE OR REPLACE PROCEDURE MY_PROCEDURE ()
RETURNS OBJECT
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
    DECLARE
        MY_CURSOR OBJECT := INIT_CURSOR_UDF('MY_CURSOR', '   SELECT * FROM
      BULKCOLLECTTABLE');

    BEGIN
        MY_CURSOR := (
            CALL OPEN_BULK_CURSOR_UDF(:MY_CURSOR)
        );
        MY_CURSOR := (
            CALL FETCH_BULK_RECORD_COLLECTIONS_UDF(:MY_CURSOR, 1.0, NULL)
        );

        RETURN MY_CURSOR;
    END;
$$;

CALL MY_PROCEDURE();
```

Output:

Copy code

```
:force:
{
  "FOUND": true,
  "ISOPEN": true,
  "NAME": "MY_CURSOR",
  "NOTFOUND": false,
  "QUERY": "   SELECT * FROM\n      BULKCOLLECTTABLE",
  "RESULT": {
    "TEST": [
      "TEST_A"
    ]
  },
  "ROWCOUNT": 1
}
```

## FETCH\_BULK\_COLLECTION\_RECORDS\_UDF (OBJECT, INTEGER)

### Definition

This user-defined function (UDF) is used to replicate the functionality of FETCH in Oracle. This is the variation where it receives the cursor and the limit.

Copy code

```
:force:
FETCH_BULK_COLLECTION_RECORDS_UDF(CURSOR OBJECT, LIMIT INTEGER)
```

### Parameters

`CURSOR` OBJECT

The cursor that is processed and filled with the data in the `fetch bulk`.

`LIMIT` FLOAT

The limit for the records to call.

### Returns

Returns an object with the records from the `fetch bulk`.

### Usage example

Input:

Copy code

```
:force:

CREATE OR REPLACE TABLE MY_TABLE (test VARCHAR(100));
INSERT INTO MY_TABLE VALUES ('TEST_A');

CREATE OR REPLACE PROCEDURE MY_PROCEDURE ()
RETURNS OBJECT
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
    DECLARE
        MY_CURSOR OBJECT := INIT_CURSOR_UDF('MY_CURSOR', '   SELECT * FROM
      MY_TABLE');

    BEGIN
        MY_CURSOR := (
            CALL OPEN_BULK_CURSOR_UDF(:MY_CURSOR)
        );
        MY_CURSOR := (
            CALL FETCH_BULK_COLLECTION_RECORDS_UDF(:MY_CURSOR, 0)
        );

        Return MY_CURSOR;
    END;
$$;

CALL MY_PROCEDURE();
```

Output:

Copy code

```
:force:
{
  "FOUND": false,
  "ISOPEN": true,
  "NAME": "MY_CURSOR",
  "NOTFOUND": true,
  "QUERY": "   SELECT * FROM\n      MY_TABLE",
  "RESULT": [],
  "ROWCOUNT": 0
}
```
