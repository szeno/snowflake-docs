# Code Conversion - Function References for SQL-Server

## ISNUMERIC\_UDF

### Definition

This user-defined function (UDF) determines whether an expression is a valid numeric type.

Copy code

```
:force:
ISNUMERIC_UDF(EXPR VARCHAR)
```

### Parameters

`EXPR` VARCHAR

The expression to be evaluated.

### Returns

Returns 1 when the input expression evaluates to a valid numeric data type; otherwise, it returns 0.

### Usage example

Input:

Copy code

```
:force:
SELECT ISNUMERIC_UDF('5');
```

Output:

Copy code

```
:force:
1
```

## PATINDEX\_UDF

### Definition

This user-defined function (UDF) returns the starting position of the first occurrence of a pattern in a specified expression or zeros if the pattern is not found.

Copy code

```
:force:
PATINDEX_UDF(PATTERN VARCHAR, EXPRESSION VARCHAR)
```

### Parameters

`PATTERN` VARCHAR

The pattern to search for.

`EXPRESSION` VARCHAR

The expression that is being evaluated.

### Returns

Returns an integer with the starting position of the pattern.

### Usage example

Input:

Copy code

```
:force:
SELECT PATINDEX_UDF('an', 'banana');
```

Output:

Copy code

```
:force:
2
```

## ERROR\_SEVERITY\_UDF

### Definition

This user-defined function (UDF) gets a value indicating the severity of an error. The default value will always be 16.

Copy code

```
:force:
ERROR_SEVERITY_UDF()
```

### Parameters

No input parameters.

### Returns

Returns a `string` with the value associated with the SQL variable name `ERROR_SEVERITY`.

### Usage example

Input:

Copy code

```
:force:
SELECT ERROR_SEVERITY_UDF();
```

Output:

Copy code

```
:force:
null -- No information set.
```

## TRANSFORM\_SP\_EXECUTE\_SQL\_STRING\_UDF(STRING, STRING, ARRAY, ARRAY)

### Definition

This user-defined function (UDF) emulates the behavior of embedded parameters (Data Binding) in the SP\_EXECUTESQL system procedure by directly replacing their values in the SQL string.

Additionally, it removes the OUTPUT parameters from the string as this is done outside the EXECUTE IMMEDIATE to which the SP\_EXECUTESQL will be transformed.

For more information, check the SP\_EXECUTESQL translation specification.

Copy code

```
:force:
TRANSFORM_SP_EXECUTE_SQL_STRING_UDF(
    _SQL_STRING STRING,
    _PARAMS_DEFINITION STRING,
    _PARAMS_NAMES ARRAY,
    _PARAMS_VALUES ARRAY
)
```

### Parameters

`_SQL_STRING` STRING

The string to be transformed.

`_PARAMS_DEFINITION` STRING

The original parameters definition checks the order in which parameter values must be assigned.

`_PARAMS_NAMES` ARRAY

The array of parameter names to replace the values in the SQL string.

`_PARAMS_VALUES` ARRAY

The array of the parameter values to be replaced in the SQL string.

### Returns

Returns a STRING with the embedded parameters values replaced.

### Usage example

Input:

Copy code

```
:force:
SELECT TRANSFORM_SP_EXECUTE_SQL_STRING_UDF(
    'SELECT * FROM PERSONS WHERE NAME LIKE (@NAME) AND ID < @id AND AGE < @age;', '@age INT, @id INT, @name VARCHAR(25)',
    ARRAY_CONSTRUCT('', '', ''),
    ARRAY_CONSTRUCT(30, 100, 'John Smith'));
```

Output:

Copy code

```
:force:
SELECT * FROM PERSONS WHERE NAME LIKE ('John Smith') AND ID < 100 AND AGE < 30;
```

## TABLE\_OBJECT\_ID\_UDF (VARCHAR)

### Definition

This user-defined function (UDF) checks if a table with a specific name has been created before.

Copy code

```
:force:
TABLE_OBJECT_ID_UDF(NAME VARCHAR)
```

### Parameters

`NAME` VARCHAR

The table name to be evaluated.

### Returns

Returns a boolean expression depending on the existence of the table.

### Usage example

Input:

Copy code

```
:force:
SELECT TABLE_OBJECT_ID_UDF('Test');
```

Output:

Copy code

```
:force:
FALSE
```

## ERROR\_PROCEDURE\_UDF

### Definition

This user-defined function (UDF) returns the value associated with the SQL variable name `ERROR_PROCEDURE`.

Copy code

```
:force:
ERROR_PROCEDURE_UDF()
```

### Parameters

No input parameters.

### Returns

Returns a `string` with the value associated with the SQL variable name `ERROR_PROCEDURE`.

### Usage example

Input:

Copy code

```
:force:
SELECT ERROR_PROCEDURE_UDF();
```

Output:

Copy code

```
:force:
null -- No information set.
```

## DB\_ID\_UDF(STRING)

### Definition

This user-defined function (UDF) emulates the [DB\_ID](https://learn.microsoft.com/en-us/sql/t-sql/functions/db-id-transact-sql?view=sql-server-ver16) functionality.

Copy code

```
:force:
DB_ID_UDF(p_database_name STRING)
```

### Parameters

`p_database_name` STRING

The name of the database to obtain the id.

### Returns

Returns an id which corresponds to the number assigned to the database when it is created. This number is assigned consecutively.

### Usage example

Input:

Copy code

```
:force:
SELECT DB_ID_UDF('MY_DATABASE')
```

Output:

Copy code

```
:force:
6
```

Warning

If the database does not exist, it returns null.

## ERROR\_LINE\_UDF

### Definition

This user-defined function (UDF) returns the value associated with the SQL variable name `ERROR_LINE`.

Copy code

```
:force:
ERROR_LINE_UDF()
```

### Parameters

No input parameters.

### Returns

Returns a `string` with the value associated with the SQL variable name `ERROR_LINE`.

### Usage example

Input:

Copy code

```
:force:
SELECT ERROR_LINE_UDF();
```

Output:

Copy code

```
:force:
null -- No information set.
```

## FUNCTION\_OBJECT\_ID\_UDF (VARCHAR)

### Definition

This user-defined function (UDF) checks if a function with a specific name has been created before.

Copy code

```
:force:
FUNCTION_OBJECT_ID_UDF(NAME VARCHAR)
```

### Parameters

`NAME` VARCHAR

The function name to be evaluated.

### Returns

Returns a boolean expression depending on the existence of the function.

### Usage example

Input:

Copy code

```
:force:
SELECT FUNCTION_OBJECT_ID_UDF('Test');
```

Output:

Copy code

```
:force:
FALSE
```

## CONSTRAINT\_OBJECT\_ID\_UDF (VARCHAR)

### Definition

This user-defined function (UDF) checks if a constraint with a specific name has been created before.

Copy code

```
:force:
CONSTRAINT_OBJECT_ID_UDF(NAME VARCHAR)
```

### Parameters

`NAME` VARCHAR

The constraint name to be evaluated.

### Returns

Returns a boolean expression depending on the existence of the constraint.

### Usage example

Input:

Copy code

```
:force:
SELECT CONSTRAINT_OBJECT_ID_UDF('Test');
```

Output:

Copy code

```
:force:
FALSE
```

## FOR\_XML\_UDF (OBJECT, VARCHAR, VARCHAR)

### Definition

This user-defined function (UDF) converts an object to XML.

Copy code

```
:force:
FOR_XML_UDF(OBJ OBJECT, ELEMENT_NAME VARCHAR, ROOT_NAME VARCHAR)
```

### Parameters

`OBJ` OBJECT

Object to be converted.

`ELEMENT_NAME` VARCHAR

Element name to be given the object.

`ROOT_NAME` VARCHAR

The root name for XML.

### Returns

Returns a varchar in the format of XML.

### Usage example

Input:

Copy code

```
:force:
SELECT
FOR_XML_UDF(OBJECT_CONSTRUCT('id', 1, 'name', 'David'), 'employee', 'employees');
```

Output:

Copy code

```
<employees>
    <employee type="OBJECT">
        <id type="INTEGER">1</id>
        <name type="VARCHAR">David</name>
    </employee>
</employees>
```

## OBJECT\_ID\_UDF (VARCHAR)

### Definition

This user-defined function (UDF) checks if an object with a specific name has been created before.

Copy code

```
:force:
OBJECT_ID_UDF(NAME VARCHAR)
```

### Parameters

`NAME` VARCHAR

The object name to be evaluated.

### Returns

Returns a boolean expression depending on the existence of the object.

### Usage example

Input:

Copy code

```
:force:
SELECT OBJECT_ID_UDF('Test');
```

Output:

Copy code

```
:force:
FALSE
```

## PROCEDURE\_OBJECT\_ID\_UDF (VARCHAR)

### Definition

This user-defined function (UDF) checks if a procedure with a specific name has been created before.

Copy code

```
:force:
PROCEDURE_OBJECT_ID_UDF(NAME VARCHAR)
```

### Parameters

`NAME` VARCHAR

The procedure name to be evaluated.

### Returns

Returns a boolean expression depending on the existence of the procedure.

### Usage example

Input:

Copy code

```
:force:
SELECT PROCEDURE_OBJECT_ID_UDF('Test');
```

Output:

Copy code

```
:force:
FALSE
```

## ISDATE\_UDF

### Definition

This user-defined function (UDF) determines whether the input value is a valid date.

Copy code

```
:force:
ISDATE_UDF(DATE_VALUE STRING)
```

### Parameters

`DATE_VALUE` STRING

The date that is going to be evaluated.

### Returns

Returns 1 when the input expression evaluates to a valid date data type; otherwise, it returns 0.

### Usage example

Input:

Copy code

```
:force:
SELECT ISDATE_UDF('2024-01-26');
```

Output:

Copy code

```
:force:
1
```

## ERROR\_NUMBER\_UDF

### Definition

This user-defined function (UDF) returns the value associated with the SQL variable name `ERROR_NUMBER`.

Copy code

```
:force:
ERROR_NUMBER_UDF()
```

### Parameters

No input parameters.

### Returns

Returns a `string` with the value associated with the SQL variable name `ERROR_NUMBER`.

### Usage example

Input:

Copy code

```
:force:
SELECT ERROR_NUMBER_UDF();
```

Output:

Copy code

```
:force:
null -- No information set.
```

## OFFSET\_FORMATTER (VARCHAR)

### Definition

This user-defined function (UDF) is an **auxiliary function** to format the offset hour and its prefix operator.

Copy code

```
:force:
OFFSET_FORMATTER(offset_hrs VARCHAR)
```

### Parameters

`offset_hrs` VARCHAR

The value to be formatted.

### Returns

Returns a varchar value with the formatted output for the offset.

### Usage example

Input:

Copy code

```
:force:
 SELECT OFFSET_FORMATTER('2024-01-26 22:00:50.708 -0800');
```

Output:

Copy code

```
:force:
2024-01-26 22:00:50.708 -0800
```

## OPENXML\_UDF

### Definition

This user-defined function (UDF) generates a query from an XML reading.

Copy code

```
:force:
OPENXML_UDF(XML VARCHAR, PATH VARCHAR)
```

### Parameters

`XML` VARCHAR

The XML content as a `varchar`.

`PATH` VARCHAR

The path of the node to extract.

### Returns

Returns a table with the data generated by the XML reading.

### Usage example

Input:

Copy code

```
:force:
SELECT * FROM TABLE(OPENXML_UDF('<iceCreamOrders>
    <order>
        <customer customerID="CUST001" contactName="Test ABC">
            <iceCreamOrder orderID="ORD001" employeeID="101" orderDate="2023-05-15T14:30:00">
                <iceCreamDetail productID="001" quantity="2"/>
                <iceCreamDetail productID="003" quantity="1"/>
            </iceCreamOrder>
        </customer>
    </order>
    <order>
        <customer customerID="CUST002" contactName="Test XYZ">
            <iceCreamOrder orderID="ORD002" employeeID="102" orderDate="2023-06-20T12:45:00">
                <iceCreamDetail productID="005" quantity="3"/>
                <iceCreamDetail productID="007" quantity="2"/>
            </iceCreamOrder>
        </customer>
    </order>
</iceCreamOrders>
', 'iceCreamOrders:order'));
```

Output:

|  | Value |
| --- | --- |
| 1 | { “order”: { “$name”: “order”, “customer”: [ { “customer”: { “$name”: “customer”, “@contactName”: “Test ABC”, “@customerID”: “CUST001”, “iceCreamOrder”: [ { “iceCreamOrder”: { “$name”: “iceCreamOrder”, “@employeeID”: 101, “@orderDate”: “2023-05-15T14:30:00”, “@orderID”: “ORD001”, “iceCreamDetail”: [ { “iceCreamDetail”: { “$name”: “iceCreamDetail”, “@productID”: “001”, “@quantity”: 2 } }, { “iceCreamDetail”: { “$name”: “iceCreamDetail”, “@productID”: “003”, “@quantity”: 1 } } ] } } ] } } ] } } |
| 2 | { “order”: { “$name”: “order”, “customer”: [ { “customer”: { “$name”: “customer”, “@contactName”: “Test XYZ”, “@customerID”: “CUST002”, “iceCreamOrder”: [ { “iceCreamOrder”: { “$name”: “iceCreamOrder”, “@employeeID”: 102, “@orderDate”: “2023-06-20T12:45:00”, “@orderID”: “ORD002”, “iceCreamDetail”: [ { “iceCreamDetail”: { “$name”: “iceCreamDetail”, “@productID”: “005”, “@quantity”: 3 } }, { “iceCreamDetail”: { “$name”: “iceCreamDetail”, “@productID”: “007”, “@quantity”: 2 } } ] } } ] } } ] } } |

## QUOTENAME\_UDF (VARCHAR, VARCHAR)

### Definition

This user-defined function (UDF) creates a valid SQL Server delimited identifier by returning a Unicode string with the delimiters added.

Copy code

```
:force:
QUOTENAME_UDF(STR VARCHAR, QUOTECHAR VARCHAR)
```

### Parameters

`STR` VARCHAR

The string to be transformed.

`QUOTECHAR` VARCHAR

The delimiter to add to the first parameter.

### Returns

Returns a varchar with the second parameter identifier added as delimiter.

### Usage example

Input:

Copy code

```
:force:
SELECT QUOTENAME_UDF('test', '?');
```

Output:

Copy code

```
:force:
?test?
```

## UPDATE\_ERROR\_VARS\_UDF (STRING, STRING, STRING)

### Definition

This user-defined function (UDF) updates the error variables in an environment in order to know when the procedure throws an error.

Copy code

```
:force:
UPDATE_ERROR_VARS_UDF(MESSAGE STRING, SEVERITY STRING, STATE STRING)
```

### Parameters

`STATE` STRING

The state of the error message.

`MESSAGE` STRING

The message to be shown in the error.

`SEVERITY` STRING

The severity of the error.

### Returns

Returns a `string` value with the new error message information.

### Usage example

Input:

Copy code

```
:force:
  SELECT UPDATE_ERROR_VARS_UDF('Message', '1', '1');
```

Output:

Copy code

```
:force:
1ABC1
```

## ROUND\_MILLISECONDS\_UDF (TIMESTAMP\_TZ)

### Definition

This user-defined function (UDF) is a function that rounds milliseconds to increments of 0, 3, or 7 milliseconds. Transact automatically rounds the milliseconds of datetime values.

Copy code

```
:force:
ROUND_MILLISECONDS_UDF(INPUT TIMESTAMP_TZ)
```

### Parameters

`INPUT` TIMESTAMP\_TZ

The input time to be rounded.

### Returns

Returns the same input `TIMESTAMP_TZ` value but with the milliseconds rounded.

### Usage example

Input:

Copy code

```
:force:
SELECT PUBLIC.ROUND_MILLISECONDS_UDF('1900-01-01 00:00:00.995 +0100')
```

Output:

Copy code

```
:force:
'1900-01-01 00:00:00.997 +0100'
```

## CAST\_NUMERIC\_TO\_TIMESTAMP\_TZ\_UDF (NUMBER)

### Definition

This user-defined function (UDF) is used to cast a numeric value to `timestamp_tz`.

Copy code

```
:force:
CAST_NUMERIC_TO_TIMESTAMP_TZ_UDF(INPUT NUMBER)
```

### Parameters

`INPUT` NUMBER

The number to be cast.

### Returns

Returns a `timestamp_tz` with the current timezone.

### Usage example

Input:

Copy code

```
:force:
SELECT PUBLIC.CAST_NUMERIC_TO_TIMESTAMP_TZ_UDF(0)
```

Output:

Copy code

```
:force:
1900-01-01 01:00:00.000 +0100
```

## IDENTITY\_UDF

### Definition

This user-defined function (UDF) returns a sequential integer expression to replicate the behavior of an IDENTITY column.

Copy code

```
:force:
IDENTITY_UDF()
```

### Parameters

No input parameters.

### Returns

Returns an integer expression.

### Usage example

Warning

A sequence is generated to support the logic.

Input:

Copy code

```
:force:
IDENTITY_UDF()
```

Output:

Copy code

```
:force:
1
```

## FOR\_XML\_UDF (OBJECT, VARCHAR)

### Definition

This user-defined function (UDF) converts an object to XML.

Copy code

```
:force:
FOR_XML_UDF(OBJ OBJECT, ELEMENT_NAME VARCHAR)
```

### Parameters

`OBJ` OBJECT

Object to be converted.

`ELEMENT_NAME` VARCHAR

Element name to be given the object.

### Returns

Returns a varchar in the format of XML.

### Usage example

Input:

Copy code

```
:force:
SELECT
FOR_XML_UDF(OBJECT_CONSTRUCT('id', 1, 'name', 'David'), 'employee');
```

Output:

Copy code

```
<employee type="OBJECT">
    <id type="INTEGER">1</id>
    <name type="VARCHAR">David</name>
</employee>
```

## QUOTENAME\_UDF (VARCHAR)

### Definition

This user-defined function (UDF) creates a valid SQL Server delimited identifier by returning a Unicode string with the delimiters added.

Copy code

```
:force:
QUOTENAME_UDF(STR VARCHAR)
```

### Parameters

`STR` VARCHAR

The string to be transformed.

### Returns

Returns a varchar with the delimited identifier added.

### Usage example

Input:

Copy code

```
:force:
SELECT QUOTENAME_UDF('test');
```

Output:

Copy code

```
:force:
"test"
```

## VIEW\_OBJECT\_ID\_UDF (VARCHAR)

### Definition

This user-defined function (UDF) checks if a view with a specific name has been created before.

Copy code

```
:force:
VIEW_OBJECT_ID_UDF(NAME VARCHAR)
```

### Parameters

`NAME` VARCHAR

The view name to be evaluated.

### Returns

Returns a boolean expression depending on the existence of the view.

### Usage example

Input:

Copy code

```
:force:
SELECT VIEW_OBJECT_ID_UDF('Test');
```

Output:

Copy code

```
:force:
FALSE
```

## SUBTRACT\_TIMESTAMP\_TZ\_UDF (TIMESTAMP\_TZ, TIMESTAMP\_TZ)

### Definition

This user-defined function (UDF) converts both inputs to the system session timezone and subtracts the dates (`FIRST_DATE` - `SECOND_DATE`) taking 1900-01-01 00:00:00.000 as the zero value. If any value does not include the timezone, the current session timezone is used.

Copy code

```
:force:
PUBLIC.SUBTRACT_TIMESTAMP_TZ_UDF(FIRST_DATE TIMESTAMP_TZ, SECOND_DATE TIMESTAMP_TZ)
```

### Parameters

`FIRST_DATE` TIMESTAMP\_TZ

The first date to be subtracted from.

`SECOND_DATE` TIMESTAMP\_TZ

The second date to be subtracted from.

### Returns

Returns the difference between the two input dates.

### Usage example

Input:

Copy code

```
:force:
SELECT SUBTRACT_TIMESTAMP_TZ_UDF('1900-01-01 00:00:00.000 +0100', '1900-01-01 00:00:00.003 -0100')
```

Output:

Copy code

```
:force:
1899-12-31 13:59:59.997 -0800
```

## STR\_UDF (FLOAT, VARCHAR)

### Definition

This user-defined function (UDF) is a template for translating the functionality of SQL Server STR() to Snowflake when it’s used with one or two optional parameters

Copy code

```
:force:
STR_UDF(FLOAT_EXPR FLOAT, FORMAT VARCHAR)
```

### Parameters

`FLOAT_EXPR` FLOAT

The expression to be processed.

`FORMAT` VARCHAR

The format to apply.

### Returns

Returns a varchar with the formatted expression.

### Usage example

Input:

Copy code

```
:force:
SELECT STR_UDF(1.5, '99');
```

Output:

Copy code

```
:force:
2
```

## XML\_JSON\_SIMPLE

### Definition

This user-defined function (UDF) generates an object with the information from executing a reading from an XML value.

Copy code

```
:force:
XML_JSON_SIMPLE(XML VARIANT)
```

### Parameters

`XML` VARIANT

The XML to be read.

### Returns

Returns an object with the processed information from the XML.

### Usage example

Input:

Copy code

```
:force:
SELECT XML_JSON_SIMPLE(TO_VARIANT(PARSE_XML('<iceCreamOrders>
    <order>
        <customer customerID="CUST001" contactName="Test ABC">
            <iceCreamOrder orderID="ORD001" employeeID="101" orderDate="2023-05-15T14:30:00">
                <iceCreamDetail productID="001" quantity="2"/>
                <iceCreamDetail productID="003" quantity="1"/>
            </iceCreamOrder>
        </customer>
    </order>
    <order>
        <customer customerID="CUST002" contactName="Test XYZ">
            <iceCreamOrder orderID="ORD002" employeeID="102" orderDate="2023-06-20T12:45:00">
                <iceCreamDetail productID="005" quantity="3"/>
                <iceCreamDetail productID="007" quantity="2"/>
            </iceCreamOrder>
        </customer>
    </order>
</iceCreamOrders>
')));
```

Output:

Copy code

```
:force:
{
  "iceCreamOrders": {
    "$name": "iceCreamOrders",
    "order": [
      {
        "order": {
          "$name": "order",
          "customer": [
            {
              "customer": {
                "$name": "customer",
                "@contactName": "Test ABC",
                "@customerID": "CUST001",
                "iceCreamOrder": [
                  {
                    "iceCreamOrder": {
                      "$name": "iceCreamOrder",
                      "@employeeID": 101,
                      "@orderDate": "2023-05-15T14:30:00",
                      "@orderID": "ORD001",
                      "iceCreamDetail": [
                        {
                          "iceCreamDetail": {
                            "$name": "iceCreamDetail",
                            "@productID": "001",
                            "@quantity": 2
                          }
                        },
                        {
                          "iceCreamDetail": {
                            "$name": "iceCreamDetail",
                            "@productID": "003",
                            "@quantity": 1
                          }
                        }
                      ]
                    }
                  }
                ]
              }
            }
          ]
        }
      },
      {
        "order": {
          "$name": "order",
          "customer": [
            {
              "customer": {
                "$name": "customer",
                "@contactName": "Test XYZ",
                "@customerID": "CUST002",
                "iceCreamOrder": [
                  {
                    "iceCreamOrder": {
                      "$name": "iceCreamOrder",
                      "@employeeID": 102,
                      "@orderDate": "2023-06-20T12:45:00",
                      "@orderID": "ORD002",
                      "iceCreamDetail": [
                        {
                          "iceCreamDetail": {
                            "$name": "iceCreamDetail",
                            "@productID": "005",
                            "@quantity": 3
                          }
                        },
                        {
                          "iceCreamDetail": {
                            "$name": "iceCreamDetail",
                            "@productID": "007",
                            "@quantity": 2
                          }
                        }
                      ]
                    }
                  }
                ]
              }
            }
          ]
        }
      }
    ]
  }
}
```

## FORMATMESSAGE\_UDF

### Definition

This user-defined function (UDF) provides the functionality of the SQL Server FORMATMESSAGE function. It constructs a message from an existing message from a provided string.

Copy code

```
:force:
FORMATMESSAGE_UDF(MESSAGE STRING, ARGS ARRAY)
```

### Parameters

`MESSAGE` STRING

The existing message string.

`ARGS` ARRAY

The arguments to be added on the first message string.

### Returns

Returns a string with the corresponding concatenated message related to the argument’s positions.

### Usage example

Input:

Copy code

```
:force:
SELECT FORMATMESSAGE_UDF('Test %s!', TO_ARRAY('a'));
```

Output:

Copy code

```
:force:
Test a!
```

## IS\_MEMBER\_UDF

### Definition

This user-defined function (UDF) determines the Windows group membership by examining an access token.

Copy code

```
:force:
IS_MEMBER_UDF(ROLE STRING)
```

### Parameters

`ROLE` STRING

The role name to be checked.

### Returns

Returns a boolean expression that is true when the current user is a member of the role; otherwise returns false.

### Usage example

Input:

Copy code

```
:force:
SELECT IS_MEMBER_UDF('TEST');
```

Output:

Copy code

```
:force:
FALSE
```

## RAISERROR\_UDF (DOUBLE, DOUBLE, DOUBLE, ARRAY)

### Definition

This user-defined function (UDF) throws an exception with a specific message.

Copy code

```
:force:
RAISERROR_UDF(MSG_ID DOUBLE, SEVERITY DOUBLE, STATE DOUBLE, PARAMS ARRAY)
```

### Parameters

`MSG_ID` DOUBLE

The message ID of the error message.

`SEVERITY` DOUBLE

The severity number for the error.

`STATE` DOUBLE

The state number for the error message.

`PARAMS` ARRAY

The additional information of the error message.

### Returns

Returns a varchar with an error message.

### Usage example

Input:

Copy code

```
:force:
SELECT RAISERROR_UDF(2.1, 1.6, 1.0, array_construct('More information'));
```

Output:

Copy code

```
:force:
MESSAGE: 2.1, LEVEL: 1.6, STATE: 1
```

## STR\_UDF(FLOAT)

### Definition

This user-defined function (UDF) is a template for translating the functionality of SQL Server STR() to Snowflake when it’s used with one or two optional parameters

Copy code

```
:force:
STR_UDF(FLOAT_EXPR FLOAT)
```

### Parameters

`FLOAT_EXPR` FLOAT

The expression to be processed.

### Returns

Returns a varchar with the formatted expression.

### Usage example

Input:

Copy code

```
:force:
SELECT STR_UDF(1.5);
```

Output:

Copy code

```
:force:
2
```

## SWITCHOFFSET\_UDF (TIMESTAMP\_TZ, VARCHAR)

### Definition

This user-defined function (UDF) returns a new timestamp\_tz with the adjusted time taken for parameter target\_tz.

Copy code

```
:force:
SWITCHOFFSET_UDF(source_timestamp TIMESTAMP_TZ, target_tz varchar)
```

### Parameters

`source_timestamp` TIMESTAMP\_TZ

The source timestamp to adjust.

`target_tz` varchar

The target time to take.

### Returns

Returns the formatted target time as TIMESTAMP\_TZ.

### Usage example

Input:

Copy code

```
:force:
SELECT SWITCHOFFSET_UDF(time_in_paris, '-0600') as time_in_costa_rica;
```

Output:

| time\_in\_paris | time\_in\_costa\_rica |
| --- | --- |
| 2022-10-05 22:00:24.467 +02:00 | 2022-10-05 14:00:24.467 -06:00 |

Expand

Show lessSee more

## GET\_CURRENT\_TIMEZONE\_UDF

### Definition

This user-defined function (UDF) gets the current session or system timezone as a literal.

Copy code

```
:force:
GET_CURRENT_TIMEZONE_UDF()
```

### Parameters

No parameters.

### Returns

Returns a literal value with the current session or system timezone as a literal.

### Usage example

Input:

Copy code

```
:force:
SELECT PUBLIC.GET_CURRENT_TIMEZONE_UDF();
```

Output:

Copy code

```
:force:
'Europe/London'
```

## UPDATE\_ERROR\_VARS\_UDF (STRING, STRING, STRING, STRING, STRING, STRING)

### Definition

This user-defined function (UDF) updates the error variables in an environment in order to know when the procedure throws an error.

Copy code

```
:force:
UPDATE_ERROR_VARS_UDF(LINE STRING,CODE STRING, STATE STRING, MESSAGE STRING, PROC_NAME STRING, SEVERITY STRING)
```

### Parameters

`LINE` STRING

The line related to the error.

`CODE` STRING

The error code associated with the error message.

`STATE` STRING

The state of the error message.

`MESSAGE` STRING

The message to be shown in the error.

`PROC_NAME` STRING

The procedure name.

`SEVERITY` STRING

The severity of the error.

### Returns

Returns a `string` value with the new error message information.

### Usage example

Input:

Copy code

```
:force:
  SELECT UPDATE_ERROR_VARS_UDF('1', '1', '1', 'ABC', 'TEST', '1');
```

Output:

Copy code

```
:force:
111ABCTEST1
```

## SEQUENCE\_OBJECT\_ID\_UDF (VARCHAR)

### Definition

This user-defined function (UDF) checks if a sequence with a specific name has been created before.

Copy code

```
:force:
SEQUENCE_OBJECT_ID_UDF(NAME VARCHAR)
```

### Parameters

`NAME` VARCHAR

The sequence name to be evaluated.

### Returns

Returns a boolean expression depending on the existence of the sequence.

### Usage example

Input:

Copy code

```
:force:
SELECT SEQUENCE_OBJECT_ID_UDF('Test');
```

Output:

Copy code

```
:force:
FALSE
```

## CAST\_TIMESTAMP\_TZ\_TO\_NUMERIC\_UDF (TIMESTAMP\_TZ)

### Definition

This user-defined function (UDF) is used to cast `timestamp_tz` to numeric. It converts the current timezone to UTC because the numeric value cannot save the `timestamp` information.

Copy code

```
:force:
CAST_TIMESTAMP_TZ_TO_NUMERIC_UDF(INPUT TIMESTAMP_TZ)
```

### Parameters

`INPUT` TIMESTAMP\_TZ

The `timestamp` input that is going to be cast.

### Returns

Returns a numeric with a decimal point. The integer part represents the number of days from 1900-01-01 and the decimal part is the percentage of milliseconds in 24 hours.

### Usage example

Input:

Copy code

```
:force:
SELECT PUBLIC.CAST_TIMESTAMP_TZ_TO_NUMERIC_UDF('1900-01-01 01:00:00.000 +0100')
```

Output:

Copy code

```
:force:
0
```

## RAISERROR\_UDF (VARCHAR, DOUBLE, DOUBLE, ARRAY)

### Definition

This user-defined function (UDF) throws an exception with a specific message.

Copy code

```
:force:
RAISERROR_UDF(MSG_TEXT VARCHAR, SEVERITY DOUBLE, STATE DOUBLE, PARAMS ARRAY)
```

### Parameters

`MSG_TEXT` VARCHAR

The message text of the error message.

`SEVERITY` DOUBLE

The severity number for the error.

`STATE` DOUBLE

The state number for the error message.

`PARAMS` ARRAY

The additional information of the error message.

### Returns

Returns a varchar with an error message.

### Usage example

Input:

Copy code

```
:force:
SELECT RAISERROR_UDF('<\<%*.*s>> TEST', 1.0, 1, array_construct());
```

Output:

Copy code

```
:force:
MESSAGE: <<undefined>> TEST, LEVEL: 1, STATE: 1
```

## PARSENAME\_UDF

### Definition

This user-defined function (UDF) gets the PART\_NUMBER index of a `string` separated by `'.'`.

Copy code

```
:force:
PARSENAME_UDF(STR VARCHAR, PART_NUMBER INT)
```

### Parameters

`STR` VARCHAR

The object name as a `string`.

`PART_NUMBER` INT

The part of the object name to be checked.

### Returns

Returns the specified part of an object name.

### Usage example

Input:

Copy code

```
:force:
SELECT PARSENAME_UDF('Test_A.Test_B.Test_C', 2);
```

Output:

Copy code

```
:force:
Test_B
```

## ERROR\_STATE\_UDF

### Definition

This user-defined function (UDF) gets the error state regardless of how many times it is run, or where it is run within the scope of the `CATCH` block.

Copy code

```
:force:
ERROR_STATE_UDF()
```

### Parameters

No input parameters.

### Returns

Returns the `string` with the error state regardless of how many times it is run, or where it is run within the scope of the `CATCH` block.

### Usage example

Input:

Copy code

```
:force:
SELECT ERROR_STATE_UDF();
```

Output:

Copy code

```
:force:
null -- No information set.
```

## CAST\_TIME\_TO\_TIMESTAMP\_TZ\_UDF (TIME)

### Definition

This user-defined function (UDF) casts `time` to `timestamp_tz`.

Copy code

```
:force:
CAST_TIME_TO_TIMESTAMP_TZ_UDF(INPUT TIME)
```

### Parameters

`INPUT` TIME

The input time to be cast to `timestamp_tz`.

### Returns

Returns a `timestamp_tz` with the date as 1900-01-01 and the same time as the input.

### Usage example

Input:

Copy code

```
:force:
SELECT PUBLIC.CAST_TIME_TO_TIMESTAMP_TZ_UDF('00:00:00.995')
```

Output:

Copy code

```
:force:
1900-01-01 00:00:00.997
```

## SUM\_TIMESTAMP\_TZ\_UDF (TIMESTAMP\_TZ, TIMESTAMP\_TZ)

### Definition

This user-defined function (UDF) converts both inputs to the system or session timezone and sums the dates taking 1900-01-01 00:00:00.000 as the zero value. If any value does not include the timezone, the current session timezone is used.

Copy code

```
:force:
SUM_TIMESTAMP_TZ_UDF(FIRST_DATE TIMESTAMP_TZ, SECOND_DATE TIMESTAMP_TZ)
```

### Parameters

`FIRST_DATE` TIMESTAMP\_TZ

The first date to sum to.

`SECOND_DATE` TIMESTAMP\_TZ

The second date to sum to.

### Returns

Returns the sum between the two input dates.

### Usage example

Input:

Copy code

```
:force:
SELECT SUM_TIMESTAMP_TZ_UDF('1900-01-01 00:00:00.000 +0100', '1900-01-01 00:00:00.003 -0100')
```

Output:

Copy code

```
:force:
1900-01-01 00:00:00.003 +0000
```

## GET\_WEEK\_START\_UDF

### Definition

This user-defined function (UDF) retrieves the WEEK\_START configuration, which is equivalent to the @@DATEFIRST function. To maintain consistency across platforms, ensure the [WEEK\_START](https://docs.snowflake.com/en/sql-reference/parameters#week-start) parameter matches the DATEFIRST setting in Transact-SQL.

Copy code

```
:force:
GET_WEEK_START_UDF()
```

### Returns

Returns a number representing the first day of the week.

### Usage example

Snowflake’s default value for WEEK\_START is `0`. However, this function returns `7` to align with the default DATEFIRST value in Transact-SQL, ensuring consistent behavior.

Input:

Copy code

```
:force:
SELECT GET_WEEK_START_UDF();
```

Output:

Copy code

```
:force:
7
```

## DATE\_PART\_WEEK\_DAY\_UDF

### Definition

This user-defined function (UDF) gets the day of the week as a number (1-7). To ensure consistency across platforms, please set the [WEEK\_START](https://docs.snowflake.com/en/sql-reference/parameters#week-start) parameter to the same value as the DATEFIRST setting in Transact-SQL.

Copy code

```
:force:
DATE_PART_WEEK_DAY_UDF(INPUT DATE)
```

### Parameters

`INPUT` DATE

Date to get the day.

### Returns

Returns a number representing the day of the week where Monday=1, Tuesday=2, …, Sunday=7.

### Usage example

The WEEK\_START parameter is 0, which causes the DATE\_PART\_WEEK\_DAY\_UDF to return a value of 1.

Input:

Copy code

```
:force:
SELECT PUBLIC.DATE_PART_WEEK_DAY_UDF('2025-08-17') AS "Sunday";
```

Output:

Copy code

```
:force:
1
```

## SCOPE\_IDENTITY()

### Definition

The `SCOPE_IDENTITY()` function in SQL Server returns the last identity value inserted into an identity column in the same scope. This function is transformed into a time-travel query using `AT(STATEMENT =>)` to retrieve the identity value from the most recent INSERT statement.

### Transformation Pattern

**SQL Server:**

Copy code

```
:force:
INSERT INTO TableName (Column1) VALUES (Value1);
SET @VariableName = SCOPE_IDENTITY();
```

**Snowflake:**

Copy code

```
:force:
INSERT INTO TableName (Column1) VALUES (Value1);
LET _scope_identity_query_id VARCHAR := LAST_QUERY_ID();
VariableName := (SELECT MAX(IdentityColumn) FROM TableName AT(STATEMENT => _scope_identity_query_id));
```

### Requirements

- Only works within **procedural contexts** (stored procedures, functions) that are transformed to SnowScript
- Requires an **identity column** defined on the target table using `IDENTITY(seed, increment)`
- The preceding INSERT statement must target a table with a resolvable identity column in the symbol table

### Usage Example

#### Input (SQL Server):

Copy code

```
:force:

CREATE TABLE Orders (OrderID INT IDENTITY(1,1), CustomerID INT);
GO

CREATE PROCEDURE InsertOrder @CustomerID INT
AS
BEGIN
    DECLARE @OrderID INT;
    INSERT INTO Orders (CustomerID) VALUES (@CustomerID);
    SET @OrderID = SCOPE_IDENTITY();
    SELECT @OrderID;
END;
```

#### Output (Snowflake):

Copy code

```
:force:

CREATE OR REPLACE TABLE Orders (
  OrderID INT IDENTITY(1, 1) ORDER,
  CustomerID INT
)
;

CREATE OR REPLACE PROCEDURE InsertOrder (CUSTOMERID INT)
RETURNS TABLE()
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
  DECLARE
    ORDERID INT;
    ProcedureResultSet RESULTSET;
  BEGIN

    INSERT INTO Orders (CustomerID) VALUES (:CUSTOMERID);
    LET _scope_identity_query_id VARCHAR := LAST_QUERY_ID();
    ORDERID :=
      SELECT
        MAX(OrderID)
      FROM
        Orders AT (STATEMENT => _scope_identity_query_id);
    ProcedureResultSet := (SELECT
      :ORDERID);
    RETURN TABLE(ProcedureResultSet);
  END;
$$;
```

### Known Limitations

#### Nested Scope Edge Case

When `SCOPE_IDENTITY()` is used inside a nested `BEGIN...END` block while the INSERT statement is in the outer procedure body, the transformation may not detect the INSERT correctly:

Copy code

```
:force:

CREATE PROCEDURE Example
AS
BEGIN
    INSERT INTO Orders (CustomerID) VALUES (@CustomerID);  -- outer scope
    BEGIN
        DECLARE @OrderID INT;
        SET @OrderID = SCOPE_IDENTITY();  -- inner scope
    END;
END;
```

In this case, [SSC-EWI-TS0095](../issues-and-troubleshooting/conversion-issues/sqlServerEWI#ssc-ewi-ts0095) may be generated indicating that no preceding INSERT was found, even though one exists at a different nesting level. This is a known limitation tracked for future enhancement.

**Workaround:** Refactor the code to keep `SCOPE_IDENTITY()` in the same block as the INSERT statement.

#### Batch Context

`SCOPE_IDENTITY()` is **not transformed** in batch contexts (scripts outside of procedures/functions). In such cases, the original function call is preserved with [SSC-EWI-0073](../issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0073).

### Related Issues

When `SCOPE_IDENTITY()` cannot be transformed, one of these EWI codes is generated:

- **[SSC-EWI-TS0095](../issues-and-troubleshooting/conversion-issues/sqlServerEWI#ssc-ewi-ts0095)** - No preceding INSERT statement found
- **[SSC-EWI-TS0096](../issues-and-troubleshooting/conversion-issues/sqlServerEWI#ssc-ewi-ts0096)** - Target table cannot be resolved
- **[SSC-EWI-TS0097](../issues-and-troubleshooting/conversion-issues/sqlServerEWI#ssc-ewi-ts0097)** - Table has no identity column

### Additional Notes

- The `AT(STATEMENT =>)` time-travel clause may return incorrect results under high-concurrency scenarios where multiple sessions insert into the same table simultaneously
- For more information about time-travel queries, see the [Snowflake documentation](https://docs.snowflake.com/en/user-guide/querying-time-travel)
