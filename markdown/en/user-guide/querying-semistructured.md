# Querying Semi-structured Data

This topic explains how to use special operators and functions to query complex hierarchical data stored in a VARIANT.

(For simple examples of how to extract values from ARRAYs and OBJECTs, see [Accessing elements of an array by index or by slice](/sql-reference/data-types-semistructured#label-accessing-array-by-index) and
[Accessing elements of an OBJECT value by key](/sql-reference/data-types-semistructured#label-accessing-object-by-key).)

Typically, hierarchical data has been imported into a VARIANT from one of the following supported data formats:

> - JSON
> - Avro
> - ORC
> - Parquet

For information about querying XML data (for example, data that originated in XML data format and was converted to an OBJECT
value by calling [PARSE\_XML](/sql-reference/functions/parse_xml)), see [Examples of querying XML data](/user-guide/semistructured-data-formats#label-xml-examples-querying) and
[XMLGET](/sql-reference/functions/xmlget).

Tip

You can use the search optimization service to improve query performance.
For details, see [Search optimization service](/user-guide/search-optimization-service).

## Sample Data Used in Examples

Except where noted, the examples in this topic refer to a table named `car_sales` that contains a single
[VARIANT](/sql-reference/data-types-semistructured#label-data-type-variant) column named `src`. This VARIANT contains nested [ARRAYs](/sql-reference/data-types-semistructured#label-data-type-array)
and [OBJECTs](/sql-reference/data-types-semistructured#label-data-type-object).

Create the table and load it:

Copy code

```
CREATE OR REPLACE TABLE car_sales
(
  src variant
)
AS
SELECT PARSE_JSON(column1) AS src
FROM VALUES
('{
    "date" : "2017-04-28",
    "dealership" : "Valley View Auto Sales",
    "salesperson" : {
      "id": "55",
      "name": "Frank Beasley"
    },
    "customer" : [
      {"name": "Joyce Ridgely", "phone": "16504378889", "address": "San Francisco, CA"}
    ],
    "vehicle" : [
      {"make": "Honda", "model": "Civic", "year": "2017", "price": "20275", "extras":["ext warranty", "paint protection"]}
    ]
}'),
('{
    "date" : "2017-04-28",
    "dealership" : "Tindel Toyota",
    "salesperson" : {
      "id": "274",
      "name": "Greg Northrup"
    },
    "customer" : [
      {"name": "Bradley Greenbloom", "phone": "12127593751", "address": "New York, NY"}
    ],
    "vehicle" : [
      {"make": "Toyota", "model": "Camry", "year": "2017", "price": "23500", "extras":["ext warranty", "rust proofing", "fabric protection"]}
    ]
}') v;
```

Select the data:

Copy code

```
SELECT * FROM car_sales;
+-------------------------------------------+
| SRC                                       |
|-------------------------------------------|
| {                                         |
|   "customer": [                           |
|     {                                     |
|       "address": "San Francisco, CA",     |
|       "name": "Joyce Ridgely",            |
|       "phone": "16504378889"              |
|     }                                     |
|   ],                                      |
|   "date": "2017-04-28",                   |
|   "dealership": "Valley View Auto Sales", |
|   "salesperson": {                        |
|     "id": "55",                           |
|     "name": "Frank Beasley"               |
|   },                                      |
|   "vehicle": [                            |
|     {                                     |
|       "extras": [                         |
|         "ext warranty",                   |
|         "paint protection"                |
|       ],                                  |
|       "make": "Honda",                    |
|       "model": "Civic",                   |
|       "price": "20275",                   |
|       "year": "2017"                      |
|     }                                     |
|   ]                                       |
| }                                         |
| {                                         |
|   "customer": [                           |
|     {                                     |
|       "address": "New York, NY",          |
|       "name": "Bradley Greenbloom",       |
|       "phone": "12127593751"              |
|     }                                     |
|   ],                                      |
|   "date": "2017-04-28",                   |
|   "dealership": "Tindel Toyota",          |
|   "salesperson": {                        |
|     "id": "274",                          |
|     "name": "Greg Northrup"               |
|   },                                      |
|   "vehicle": [                            |
|     {                                     |
|       "extras": [                         |
|         "ext warranty",                   |
|         "rust proofing",                  |
|         "fabric protection"               |
|       ],                                  |
|       "make": "Toyota",                   |
|       "model": "Camry",                   |
|       "price": "23500",                   |
|       "year": "2017"                      |
|     }                                     |
|   ]                                       |
| }                                         |
+-------------------------------------------+
```

## Traversing Semi-structured Data

Insert a colon `:` between the VARIANT column name and any first-level element: `<column>:<level1_element>`.

Note

In the following examples, the query output is enclosed in double quotes because the query output is
VARIANT, not VARCHAR. (The VARIANT values are not strings; the VARIANT values contain strings.) Operators `:` and subsequent `.` and `[]` always return VARIANT values containing strings.

For example, get a list of all dealership names:

Copy code

```
SELECT src:dealership
    FROM car_sales
    ORDER BY 1;
+--------------------------+
| SRC:DEALERSHIP           |
|--------------------------|
| "Tindel Toyota"          |
| "Valley View Auto Sales" |
+--------------------------+
```

There are two ways to access elements in a JSON object:

- [Dot Notation](#dot-notation) (in this topic).
- [Bracket Notation](#bracket-notation) (in this topic).

Important

Regardless of which notation you use, the column name is case-insensitive but element names are case-sensitive.
For example, in the following list, the first two paths are equivalent, but the third is not:

- src:salesperson.name
- SRC:salesperson.name
- SRC:Salesperson.Name

### Dot Notation

Use dot notation to traverse a path in a JSON object: `<column>:<level1_element>.<level2_element>.<level3_element>`. Optionally enclose element names in double quotes:
`<column>:"<level1_element>"."<level2_element>"."<level3_element>"`.

Note

The rules for JSON keys (element names) are different from the rules for
Snowflake SQL identifiers.

For more information about the rules for Snowflake SQL identifiers, see: [Identifier requirements](/sql-reference/identifiers-syntax).

For more information about JSON keys, see <http://json.org>, in particular the description of a “string”.

If an element name does not conform to Snowflake SQL identifier rules,
for example if it contains spaces, then you must enclose the
name in double quotes. Below are some examples (not all of which are
from the car\_sales example above) of valid JSON element names that are not valid Snowflake identifier names
unless they are surrounded by double quotes:

Copy code

```
-- This contains a blank.
SELECT src:"company name" FROM partners;

-- This does not start with a letter or underscore.
SELECT zipcode_info:"94987" FROM addresses;

-- This contains characters that are not letters, digits, or underscores, and
-- it does not start with a letter or underscore.
SELECT measurements:"#sPerSquareInch" FROM english_metrics;
```

Get the names of all salespeople who sold cars:

Copy code

```
_01
SELECT src:salesperson.name
    FROM car_sales
    ORDER BY 1;
+----------------------+
| SRC:SALESPERSON.NAME |
|----------------------|
| "Frank Beasley"      |
| "Greg Northrup"      |
+----------------------+
```

### Bracket Notation

Alternatively, use bracket notation to traverse the path in an object: `<column>['<level1_element>']['<level2_element>']`. Enclose element names in single quotes. Values are retrieved as strings.

Get the names of all salespeople who sold cars:

Copy code

```
_01
SELECT src['salesperson']['name']
    FROM car_sales
    ORDER BY 1;
+----------------------------+
| SRC['SALESPERSON']['NAME'] |
|----------------------------|
| "Frank Beasley"            |
| "Greg Northrup"            |
+----------------------------+
```

## Retrieving a Single Instance of a Repeating Element

Retrieve a specific numbered instance of a child element in a repeating array by adding a numbered predicate (starting from 0) to the array reference.

Note that to retrieve all instances of a child element in a repeating array, it is necessary to flatten the array. See an example in [Using the FLATTEN Function to Parse Arrays](#using-the-flatten-function-to-parse-arrays) in this topic.

Get the vehicle details for each sale:

Copy code

```
SELECT src:customer[0].name, src:vehicle[0]
    FROM car_sales
    ORDER BY 1;
+----------------------+-------------------------+
| SRC:CUSTOMER[0].NAME | SRC:VEHICLE[0]          |
|----------------------+-------------------------|
| "Bradley Greenbloom" | {                       |
|                      |   "extras": [           |
|                      |     "ext warranty",     |
|                      |     "rust proofing",    |
|                      |     "fabric protection" |
|                      |   ],                    |
|                      |   "make": "Toyota",     |
|                      |   "model": "Camry",     |
|                      |   "price": "23500",     |
|                      |   "year": "2017"        |
|                      | }                       |
| "Joyce Ridgely"      | {                       |
|                      |   "extras": [           |
|                      |     "ext warranty",     |
|                      |     "paint protection"  |
|                      |   ],                    |
|                      |   "make": "Honda",      |
|                      |   "model": "Civic",     |
|                      |   "price": "20275",     |
|                      |   "year": "2017"        |
|                      | }                       |
+----------------------+-------------------------+
```

Get the price of each car sold:

Copy code

```
SELECT src:customer[0].name, src:vehicle[0].price
    FROM car_sales
    ORDER BY 1;
+----------------------+----------------------+
| SRC:CUSTOMER[0].NAME | SRC:VEHICLE[0].PRICE |
|----------------------+----------------------|
| "Bradley Greenbloom" | "23500"              |
| "Joyce Ridgely"      | "20275"              |
+----------------------+----------------------+
```

## Explicitly Casting Values

When you extract values from a VARIANT, you can explicitly cast the values to the desired data type.
For example, you can extract the prices as numeric values and perform calculations on them:

Copy code

```
SELECT src:vehicle[0].price::NUMBER * 0.10 AS tax
    FROM car_sales
    ORDER BY tax;
+--------+
|    TAX |
|--------|
| 2027.5 |
| 2350.0 |
+--------+
```

By default, when VARCHARs, DATEs, TIMEs, and TIMESTAMPs are retrieved from a VARIANT column, the values are surrounded by double
quotes. You can eliminate the double quotes by explicitly casting the values. For example:

Copy code

```
SELECT src:dealership, src:dealership::VARCHAR
    FROM car_sales
    ORDER BY 2;
+--------------------------+-------------------------+
| SRC:DEALERSHIP           | SRC:DEALERSHIP::VARCHAR |
|--------------------------+-------------------------|
| "Tindel Toyota"          | Tindel Toyota           |
| "Valley View Auto Sales" | Valley View Auto Sales  |
+--------------------------+-------------------------+
```

For more information about casting VARIANT values, see [Inserting VARIANT data](/sql-reference/data-types-semistructured#label-using-values-in-a-variant).

For more information about casting in general, see [Data type conversion](/sql-reference/data-type-conversion).

## Using FLATTEN to Filter the Results in a WHERE Clause

The [FLATTEN](/sql-reference/functions/flatten) function explodes nested values into separate columns. You can use the function to filter query results in a [WHERE](/sql-reference/constructs/where) clause.

The following example returns key-value pairs that match a WHERE clause and displays them in separate columns:

Copy code

```
CREATE TABLE pets (v variant);

INSERT INTO pets SELECT PARSE_JSON ('{"species":"dog", "name":"Fido", "is_dog":"true"} ');
INSERT INTO pets SELECT PARSE_JSON ('{"species":"cat", "name":"Bubby", "is_dog":"false"}');
INSERT INTO pets SELECT PARSE_JSON ('{"species":"cat", "name":"dog terror", "is_dog":"false"}');

SELECT a.v, b.key, b.value FROM pets a,LATERAL FLATTEN(input => a.v) b
WHERE b.value LIKE '%dog%';

+-------------------------+---------+--------------+
| V                       | KEY     | VALUE        |
|-------------------------+---------+--------------|
| {                       | species | "dog"        |
|   "is_dog": "true",     |         |              |
|   "name": "Fido",       |         |              |
|   "species": "dog"      |         |              |
| }                       |         |              |
| {                       | name    | "dog terror" |
|   "is_dog": "false",    |         |              |
|   "name": "dog terror", |         |              |
|   "species": "cat"      |         |              |
| }                       |         |              |
+-------------------------+---------+--------------+
```

## Using FLATTEN to List Distinct Key Names

When working with unfamiliar semi-structured data, you might not know the key names in an OBJECT. You can use the FLATTEN function
with the RECURSIVE argument to return the list of distinct key names in all nested elements in an OBJECT:

Copy code

```
SELECT REGEXP_REPLACE(f.path, '\\[[0-9]+\\]', '[]') AS "Path",
  TYPEOF(f.value) AS "Type",
  COUNT(*) AS "Count"
FROM <table>,
LATERAL FLATTEN(<variant_column>, RECURSIVE=>true) f
GROUP BY 1, 2 ORDER BY 1, 2;
```

The [REGEXP\_REPLACE](/sql-reference/functions/regexp_replace) function removes the array index values (e.g. `[0]`) and replaces them with brackets (`[]`) to group array elements.

For example:

Copy code

```
{"a": 1, "b": 2, "special" : "data"}   <--- row 1 of VARIANT column
{"c": 3, "d": 4, "normal" : "data"}    <----row 2 of VARIANT column

Output from query:

+---------+---------+-------+
| Path    | Type    | Count |
|---------+---------+-------|
| a       | INTEGER |     1 |
| b       | INTEGER |     1 |
| c       | INTEGER |     1 |
| d       | INTEGER |     1 |
| normal  | VARCHAR |     1 |
| special | VARCHAR |     1 |
+---------+---------+-------+
```

## Using FLATTEN to List Paths in an OBJECT

Related to [Using FLATTEN to List Distinct Key Names](#using-flatten-to-list-distinct-key-names), you can use the FLATTEN function with the RECURSIVE argument to retrieve all keys and paths in an OBJECT.

The following query returns keys, paths, and values (including VARIANT “null” values) for all data types stored in a VARIANT
column. The code assumes that the VARIANT column contains an OBJECT in each row.

Copy code

```
SELECT
  t.<variant_column>,
  f.seq,
  f.key,
  f.path,
  REGEXP_COUNT(f.path,'\\.|\\[') +1 AS Level,
  TYPEOF(f.value) AS "Type",
  f.index,
  f.value AS "Current Level Value",
  f.this AS "Above Level Value"
FROM <table> t,
LATERAL FLATTEN(t.<variant_column>, recursive=>true) f;
```

The following query is similar to the first query, but excludes nested OBJECTs and ARRAYs:

Copy code

```
SELECT
  t.<variant_column>,
  f.seq,
  f.key,
  f.path,
  REGEXP_COUNT(f.path,'\\.|\\[') +1 AS Level,
  TYPEOF(f.value) AS "Type",
  f.value AS "Current Level Value",
  f.this AS "Above Level Value"
FROM <table> t,
LATERAL FLATTEN(t.<variant_column>, recursive=>true) f
WHERE "Type" NOT IN ('OBJECT','ARRAY');
```

The queries return the following values:

> *<variant\_column>*
> :   OBJECT stored as a row in the VARIANT column.
>
> Seq
> :   Unique sequence number associated with the data in the row.
>
> Key
> :   String associated with a value in the data structure.
>
> Path
> :   Path to the element within the data structure.
>
> Level
> :   Level of the key-value pair within the data structure.
>
> Type
> :   Data type for the value.
>
> Index
> :   Index of the element in the data structure. Applies to ARRAY values only; otherwise NULL.
>
> Current Level Value
> :   Value at the current level in the data structure.
>
> Above Level Value
> :   Value one level higher in the data structure.

## Using the FLATTEN Function to Parse Arrays

Parse an array using the [FLATTEN](/sql-reference/functions/flatten) function. FLATTEN is a table function that produces a lateral view of a VARIANT, OBJECT, or ARRAY column. The function returns a row for each object, and the LATERAL modifier joins the data with any information outside of the object.

Get the names and addresses of all customers. Cast the VARIANT output to string values:

Copy code

```
SELECT
  value:name::string as "Customer Name",
  value:address::string as "Address"
  FROM
    car_sales
  , LATERAL FLATTEN(INPUT => SRC:customer);

+--------------------+-------------------+
| Customer Name      | Address           |
|--------------------+-------------------|
| Joyce Ridgely      | San Francisco, CA |
| Bradley Greenbloom | New York, NY      |
+--------------------+-------------------+
```

## Using the FLATTEN Function to Parse Nested Arrays

The `extras` array is nested within the `vehicle` array in the sample data:

Copy code

```
"vehicle" : [
     {"make": "Honda", "model": "Civic", "year": "2017", "price": "20275", "extras":["ext warranty", "paint protection"]}
   ]
```

Add a second FLATTEN clause to flatten the `extras` array within the flattened `vehicle` array and retrieve the “extras” purchased for each car sold:

Copy code

```
SELECT
  vm.value:make::string as make,
  vm.value:model::string as model,
  ve.value::string as "Extras Purchased"
  FROM
    car_sales
    , LATERAL FLATTEN(INPUT => SRC:vehicle) vm
    , LATERAL FLATTEN(INPUT => vm.value:extras) ve
  ORDER BY make, model, "Extras Purchased";
+--------+-------+-------------------+
| MAKE   | MODEL | Extras Purchased  |
|--------+-------+-------------------|
| Honda  | Civic | ext warranty      |
| Honda  | Civic | paint protection  |
| Toyota | Camry | ext warranty      |
| Toyota | Camry | fabric protection |
| Toyota | Camry | rust proofing     |
+--------+-------+-------------------+
```

## Parsing Text as VARIANT Values Using the PARSE\_JSON Function

Parse text as a JSON document using the [PARSE\_JSON](/sql-reference/functions/parse_json) function.

If the input is NULL, the output will also be NULL. However, if the input string is `null`, it is interpreted as a VARIANT `null` value; that is, the result is not a SQL NULL but a real value used to represent a null value in semi-structured formats.

For an example, see [Sample Data Used in Examples](#sample-data-used-in-examples) in this topic.

## Extracting Values Using the GET Function

[GET](/sql-reference/functions/get) accepts a VARIANT, OBJECT, or ARRAY value as the first argument and extracts the VARIANT value of the element in the path provided as the second argument.

Compute and extract the last element of each array in a VARIANT column using the GET and [ARRAY\_SIZE](/sql-reference/functions/array_size) functions. ARRAY\_SIZE returns the size of the input array:

Note

This example departs from the `car_sales` table used elsewhere in this topic.

Copy code

```
CREATE OR replace TABLE colors (v variant);

INSERT INTO
   colors
   SELECT
      parse_json(column1) AS v
   FROM
   VALUES
     ('[{r:255,g:12,b:0},{r:0,g:255,b:0},{r:0,g:0,b:255}]'),
     ('[{c:0,m:1,y:1,k:0},{c:1,m:0,y:1,k:0},{c:1,m:1,y:0,k:0}]')
    v;

SELECT *, GET(v, ARRAY_SIZE(v)-1) FROM colors;

+---------------+-------------------------+
| V             | GET(V, ARRAY_SIZE(V)-1) |
|---------------+-------------------------|
| [             | {                       |
|   {           |   "b": 255,             |
|     "b": 0,   |   "g": 0,               |
|     "g": 12,  |   "r": 0                |
|     "r": 255  | }                       |
|   },          |                         |
|   {           |                         |
|     "b": 0,   |                         |
|     "g": 255, |                         |
|     "r": 0    |                         |
|   },          |                         |
|   {           |                         |
|     "b": 255, |                         |
|     "g": 0,   |                         |
|     "r": 0    |                         |
|   }           |                         |
| ]             |                         |
| [             | {                       |
|   {           |   "c": 1,               |
|     "c": 0,   |   "k": 0,               |
|     "k": 0,   |   "m": 1,               |
|     "m": 1,   |   "y": 0                |
|     "y": 1    | }                       |
|   },          |                         |
|   {           |                         |
|     "c": 1,   |                         |
|     "k": 0,   |                         |
|     "m": 0,   |                         |
|     "y": 1    |                         |
|   },          |                         |
|   {           |                         |
|     "c": 1,   |                         |
|     "k": 0,   |                         |
|     "m": 1,   |                         |
|     "y": 0    |                         |
|   }           |                         |
| ]             |                         |
+---------------+-------------------------+
```

## Extracting Values by Path Using the GET\_PATH Function

Extract a value from a VARIANT column using the [GET\_PATH , :](/sql-reference/functions/get_path) function. The function is a variation of [GET](/sql-reference/functions/get), used to extract a value using a path name. GET\_PATH is equivalent to a chain of GET functions.

Get the vehicle make for the car purchased by each customer:

Copy code

```
SELECT GET_PATH(src, 'vehicle[0]:make') FROM car_sales;

+----------------------------------+
| GET_PATH(SRC, 'VEHICLE[0]:MAKE') |
|----------------------------------|
| "Honda"                          |
| "Toyota"                         |
+----------------------------------+
```

[Traversing Semi-structured Data](#traversing-semi-structured-data) describes the path syntax used to retrieve elements in a VARIANT column. The syntax is shorthand for the GET or [GET\_PATH , :](/sql-reference/functions/get_path) function. Unlike the path syntax, these functions can handle irregular paths or path elements.

The following queries produce the same results:

Copy code

```
SELECT GET_PATH(src, 'vehicle[0].make') FROM car_sales;

SELECT src:vehicle[0].make FROM car_sales;
```

## Parsing Arrays Directly from a Staged Data File

Assume a staged file named `contacts.json.gz` contains the following data:

Copy code

```
{
    "root": [
        {
            "employees": [
                {
                    "firstName": "Anna",
                    "lastName": "Smith"
                },
                {
                    "firstName": "Peter",
                    "lastName": "Jones"
                }
            ]
        }
    ]
}
```

Also assume a file format named `my_json_format` includes `TYPE=JSON` in its definition.

Query the name of the first employee in the staged file. In this example, the file is located in the `customers` table stage, but it could be located in any internal (i.e. Snowflake) or external stage:

Copy code

```
SELECT 'The First Employee Record is '||
    S.$1:root[0].employees[0].firstName||
    ' '||S.$1:root[0].employees[0].lastName
FROM @%customers/contacts.json.gz (file_format => 'my_json_format') as S;

+----------------------------------------------+
| 'THE FIRST EMPLOYEE RECORD IS '||            |
|      S.$1:ROOT[0].EMPLOYEES[0].FIRSTNAME||   |
|      ' '||S.$1:ROOT[0].EMPLOYEES[0].LASTNAME |
|----------------------------------------------|
| The First Employee Record is Anna Smith      |
+----------------------------------------------+
```

## Use lambda functions on data with Snowflake higher-order functions

Snowflake higher-order functions enable you to use lambda functions to filter, reduce, and transform semi-structured
and structured data. When you call a Snowflake higher-order function, you use a lambda expression to create
the lambda function that operates on the data, which is specified in an [array](/sql-reference/data-types-semistructured#label-data-type-array).
Snowflake higher-order functions provide a concise, readable, and efficient way to perform data manipulation
and advanced analysis.

The following higher-order functions are available:

- [FILTER](/sql-reference/functions/filter)
- [REDUCE](/sql-reference/functions/reduce)
- [TRANSFORM](/sql-reference/functions/transform)

### Benefits of higher-order functions

When you use semi-structured data in data analytics, you typically need to loop over an array and perform actions
for each value in the array. You can perform these operations with a call to a Snowflake higher-order function.
Higher-order functions provide the following benefits:

- **Streamline advanced analytics** - By simplifying the iteration over array elements, the functions facilitate the implementation
  of custom logic for data filtering, reduction, and transformation, which streamlines analytical processes. Without higher-order functions,
  this type of manipulation requires LATERAL FLATTEN operations or user-defined functions (UDFs).
- **Enhance the developer experience** - Higher-order functions encapsulate the manipulation logic in lambda expressions, enabling
  more readable and maintainable SQL statements. By using higher-order functions, you can avoid writing verbose and convoluted
  SQL queries.
- **Avoid unnecessary UDFs** - With higher-order functions, there is less need to create, maintain, and manage access to
  UDFs for ad-hoc array manipulation logic. These functions can reduce overhead and simplify data manipulation processes.

### Lambda expressions

A lambda expression is a short block of code that takes an argument and returns a value. In the lambda expression,
you specify the argument on the left side of the lambda operator (`->`) and an expression on the right side. You
can use lambda expressions to complete a variety of operations.

For example, you can use a lambda expression to generate numeric output. The following lambda expression multiplies
elements by two:

Copy code

```
a -> a * 2
```

You can use a lambda expression to filter elements and return the elements for which the filter condition
returns TRUE. For example, the following lambda expression returns elements with a `value` greater than `50`:

Copy code

```
a -> a:value > 50
```

You can use a lambda expression to add text to elements. For example, the following lambda expression
adds the text `some string` to elements:

Copy code

```
a -> a || ' some string'
```

You can reference table columns in lambda expressions. For example, the following lambda expression
subtracts the value of `table1.col2` from elements:

Copy code

```
a -> a - table1.col2
```

When you reference columns in lambda expressions, you can specify unqualified or qualified column names.
You can also use aliases for column names in lambda expressions. The resolution of identifiers
prioritizes lambda arguments first, then column names (using the standard rules for object name resolution).
For more information, see [Object name resolution](/sql-reference/name-resolution).

You can specify the data types of lambda arguments. For example, the following lambda expression
specifies two INTEGER values and adds them:

Copy code

```
(x INT, y INT) -> (x + y)
```

You can use function calls in a lambda expression. For example, the following lambda expression
calls the [UPPER](/sql-reference/functions/upper) function:

Copy code

```
a -> UPPER(a)
```

You can execute an [uncorrelated scalar subquery](/user-guide/querying-subqueries) in a lambda
expression. For example, the following lambda expression includes such a subquery:

Copy code

```
a -> a + (SELECT MAX(c1) FROM mytable)
```

You can call a [user-defined SQL function](/developer-guide/udf/sql/udf-sql-introduction) in a lambda expression.
For example, the following lambda expression calls the function `mysqlfunction`:

Copy code

```
a -> mysqlfunction(5)
```

### Limitations

- Lambda expressions aren’t supported as standalone objects. They must be specified as arguments to Snowflake
  higher-order functions.
- Lambda expressions must be anonymous. Named functions can’t be passed in as lambda arguments to Snowflake
  higher-order functions.
- Lambda expressions only accept built-in functions (excluding aggregate and window functions), SQL user-defined functions,
  and uncorrelated scalar subqueries. They don’t support user-defined functions created in languages other than SQL,
  referencing nested context (such as Snowflake Scripting variables), CTE expressions, arguments in user-defined functions,
  or correlated subqueries.
