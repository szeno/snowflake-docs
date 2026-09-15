# Supported formats for semi-structured data

This topic describes the supported formats for semi-structured data.

Snowflake natively supports the semi-structured data formats below. Specifically, Snowflake provides options in COPY commands to
load and unload data files in these formats.

## JSON

### About JSON

JSON (JavaScript Object Notation) is a lightweight, plain-text, data-interchange format based on a subset of the JavaScript Programming Language.

JSON data can be produced by any application. Some common examples include:

- JavaScript applications using native methods to generate JSON.
- Non-JavaScript applications using libraries (usually with extensions) to generate JSON data.
- Ad hoc JavaScript generators.
- Concatenation of JSON documents (which may or may not be line-separated).

Because there is no formal specification, there are significant differences between various implementations. These differences make import of JSON-like data sets impossible if the JSON parser is strict in
its language definition. To make import of JSON data sets as problem-free as possible, Snowflake follows the rule “be liberal in what you accept”. The intent is to accept the widest possible range of JSON
and JSON-like inputs that permit unambiguous interpretation.

This topic describes the syntax for JSON documents accepted by Snowflake.

For more information about JSON, see [json.org](http://www.json.org).

### Basic JSON syntax

JSON data is a hierarchical collection of name/value pairs grouped into objects and arrays:

- Colons `:` separate names and values in name/value pairs.
- Curly braces `{}` denote objects.
- Square brackets `[]` denote arrays.
- Commas `,` separate entities in objects and arrays.

### Name/value pairs

JSON name/value pairs consist of a field name (in double quotes), followed by a colon, then a value.

For example:

Copy code

```
{"firstName":"John", "empid":45611}
```

### Supported data types

A value in a name/value pair can be:

- A number (integer or floating point)
- A string (in double quotes)
- A Boolean (true or false)
- An array (in square brackets)
- An object (in curly braces)
- Null

### Objects

JSON objects are written inside curly braces. An object can contain multiple name/values pairs, separated by commas. For example:

Copy code

```
{"firstName":"John", "lastName":"Doe"}
```

### Arrays

JSON arrays are written inside square brackets. An array can contain multiple objects, separated by commas. For example:

Copy code

```
{"employees":[
    {"firstName":"John", "lastName":"Doe"},
    {"firstName":"Anna", "lastName":"Smith"},
    {"firstName":"Peter", "lastName":"Jones"}
  ]
}
```

### Examples of JSON documents

**FILE NAME:** `json_sample_data1`

Contains an array with 3 simple employee records (objects):

> Copy code
>
> ```
> {"root":[{"employees":[
>     {"firstName":"John", "lastName":"Doe"},
>     {"firstName":"Anna", "lastName":"Smith"},
>     {"firstName":"Peter", "lastName":"Jones"}
> ]}]}
> ```

**FILE NAME:** `json_sample_data2`

Contains an array with 3 employee records (objects) and their associated dependent data (children, the children’s names and ages, cities where the employee has lived, and the years that the employee has
lived in those cities):

> Copy code
>
> ```
> {"root":
>    [
>     { "kind": "person",
>       "fullName": "John Doe",
>       "age": 22,
>       "gender": "Male",
>       "phoneNumber":
>         {"areaCode": "206",
>          "number": "1234567"},
>       "children":
>          [
>            {
>              "name": "Jane",
>              "gender": "Female",
>              "age": "6"
>            },
>            {
>               "name": "John",
>               "gender": "Male",
>               "age": "15"
>            }
>          ],
>       "citiesLived":
>          [
>             {
>                "place": "Seattle",
>                "yearsLived": ["1995"]
>             },
>             {
>                "place": "Stockholm",
>                "yearsLived": ["2005"]
>             }
>          ]
>       },
>       {"kind": "person", "fullName": "Mike Jones", "age": 35, "gender": "Male", "phoneNumber": { "areaCode": "622", "number": "1567845"}, "children": [{ "name": "Earl", "gender": "Male", "age": "10"}, {"name": "Sam", "gender": "Male", "age": "6"}, { "name": "Kit", "gender": "Male", "age": "8"}], "citiesLived": [{"place": "Los Angeles", "yearsLived": ["1989", "1993", "1998", "2002"]}, {"place": "Washington DC", "yearsLived": ["1990", "1993", "1998", "2008"]}, {"place": "Portland", "yearsLived": ["1993", "1998", "2003", "2005"]}, {"place": "Austin", "yearsLived": ["1973", "1998", "2001", "2005"]}]},
>       {"kind": "person", "fullName": "Anna Karenina", "age": 45, "gender": "Female", "phoneNumber": { "areaCode": "425", "number": "1984783"}, "citiesLived": [{"place": "Stockholm", "yearsLived": ["1992", "1998", "2000", "2010"]}, {"place": "Russia", "yearsLived": ["1998", "2001", "2005"]}, {"place": "Austin", "yearsLived": ["1995", "1999"]}]}
>     ]
> }
> ```

## Avro

### About Avro

Avro is an open-source data serialization and RPC framework originally developed for use with Apache Hadoop. It utilizes schemas defined in JSON to produce serialized data in a compact binary format. The
serialized data can be sent to any destination (i.e. application or program) and can be easily deserialized at the destination because the schema is included in the data.

An Avro schema consists of a JSON string, object, or array that defines the type of schema and the data attributes (field names, data types, etc.) for the schema type. The attributes differ depending on
the schema type. Complex data types such as arrays and maps are supported.

Snowflake reads Avro data into a single VARIANT column. You can query the data in a VARIANT column just as you would JSON data, using similar commands and functions.

For more information, see [avro.apache.org](http://avro.apache.org).

### Example of an Avro schema

Copy code

```
{
 "type": "record",
 "name": "person",
 "namespace": "example.avro",
 "fields": [
     {"name": "fullName", "type": "string"},
     {"name": "age",  "type": ["int", "null"]},
     {"name": "gender", "type": ["string", "null"]}
     ]
}
```

## ORC

### About ORC

ORC (Optimized Row Columnar) is a binary format used to store Hive data. ORC was designed for efficient compression and improved
performance for reading, writing, and processing data over earlier Hive file formats. For more information about ORC, see [https://orc.apache.org/](https://orc.apache.org//).

Snowflake reads ORC data into a single VARIANT column. You can query the data in a VARIANT column just as you would JSON data, using similar commands and functions.

Alternatively, you can extract columns from a staged ORC file into separate table columns using a CREATE TABLE AS SELECT statement.

Note

- Map data is deserialized into an array of objects, e.g.:

  Copy code

  ```
  "map": [{"key": "chani", "value": {"int1": 5, "string1": "chani"}}, {"key": "mauddib", "value": {"int1": 1, "string1": "mauddib"}}]
  ```
- Union data is deserialized into a single object, e.g.:

  Copy code

  ```
  {"time": "1970-05-05 12:34:56.197", "union": {"tag": 0, "value": 3880900}, "decimal": 3863316326626557453.000000000000000000}
  ```

### Example of ORC data loaded into a VARIANT column

```
+--------------------------------------+
| SRC                                  |
|--------------------------------------|
| {                                    |
|   "boolean1": false,                 |
|   "byte1": 1,                        |
|   "bytes1": "0001020304",            |
|   "decimal1": 12345678.654745,       |
|   "double1": -1.500000000000000e+01, |
|   "float1": 1.000000000000000e+00,   |
|   "int1": 65536,                     |
|   "list": [                          |
|     {                                |
|       "int1": 3,                     |
|       "string1": "good"              |
|     },                               |
|     {                                |
|       "int1": 4,                     |
|       "string1": "bad"               |
|     }                                |
|   ]                                  |
| }                                    |
+--------------------------------------+
```

## Parquet

### About Parquet

Parquet is a compressed, efficient columnar data representation designed for projects in the Hadoop ecosystem. The file format supports complex nested data structures and uses Dremel record shredding and assembly algorithms. Parquet files can’t be opened in a text editor.
For more information, see [parquet.apache.org/docs/](https://parquet.apache.org/docs/).

Note

Snowflake supports Parquet files produced using the Parquet writer V2 for Apache Iceberg™ tables or when you use
a [vectorized scanner](/sql-reference/sql/copy-into-table#label-use-vectorized-scanner).

Depending on your loading use case, Snowflake either reads Parquet data into a single VARIANT column or directly into table columns
(such as when you [load data from Iceberg-compatible Parquet files](/user-guide/tables-iceberg-load#label-tables-iceberg-load-add-files-copy-example)).

You can query the data in a VARIANT column just as you would JSON data, using similar commands and functions.
Alternatively, you can extract select columns from a staged Parquet file into separate table columns using a CREATE TABLE AS SELECT statement.

### Example of Parquet data loaded into a VARIANT column

```
+------------------------------------------+
| SRC                                      |
|------------------------------------------|
| {                                        |
|   "continent": "Europe",                 |
|   "country": {                           |
|     "city": {                            |
|       "bag": [                           |
|         {                                |
|           "array_element": "Paris"       |
|         },                               |
|         {                                |
|           "array_element": "Nice"        |
|         },                               |
|         {                                |
|           "array_element": "Marseilles"  |
|         },                               |
|         {                                |
|           "array_element": "Cannes"      |
|         }                                |
|       ]                                  |
|     },                                   |
|     "name": "France"                     |
|   }                                      |
| }                                        |
+------------------------------------------+
```

## XML

### About XML

XML (eXtensible Markup Language) is a markup language that defines a set of rules for encoding documents. It was
originally based on SGML, another markup language developed for standardizing the structure and elements that comprise
a document.

Since its introduction, XML has grown beyond an initial focus on documents to encompass a wide range of uses, including
representation of arbitrary data structures and serving as the base language for communication protocols. Because of its
extensibility, versatility, and usability, it has become one of the most commonly-used standards for data interchange
on the Web.

An XML document consists primarily of the following constructs:

- Tags (identified by angle brackets, `<` and `>`)
- Elements

Elements typically consist of a “start” tag and matching “end” tag, with the text between the tags constituting the content
of the element. An element can also consist of an “empty-element” tag with no “end” tag. “start” and “empty-element” tags might
contain attributes, which help define the characteristics or metadata for the element.

When you query XML data, the dollar sign operator (`$`) returns the contents, as a VARIANT value, of the value it operates on.
For an element, the contents of that element are returned:

- If the element contains text, text is returned as a VARIANT value.
- If the element contains another element, the element is returned as a VARIANT value in XML format.
- If the element contains a series of elements, an array of the elements is returned as a VARIANT value in JSON format.

Use the following operators to access the VARIANT value in a query:

- `$` for the contents of the value.
- `@` for the name of the value. This operator is useful when you are iterating through elements with different names.

  Use `@attribute_name` for the contents of a named attribute. For example, for `@attr`, the attribute name is `attr`.
  The query returns the contents of the attribute with the name that directly follows the at sign. If no attribute is found,
  NULL is returned.

For examples that query XML data, see [Examples of querying XML data](#label-xml-examples-querying).

You can use the following functions to work with XML data:

- [CHECK\_XML](/sql-reference/functions/check_xml)
- [PARSE\_XML](/sql-reference/functions/parse_xml)
- [TO\_XML](/sql-reference/functions/to_xml)
- [XMLGET](/sql-reference/functions/xmlget)

### Examples of working with XML

The following examples show you how to load and query XML data.

#### Example of loading an XML document

This example shows you how to load the following XML document:

Copy code

```
<?xml version="1.0"?>
<!DOCTYPE parts system "parts.dtd">
<?xml-stylesheet type="text/css" href="xmlpartsstyle.css"?>
<parts>
   <part count="4">
      <item>Spark Plugs</item>
      <partnum>A3-400</partnum>
      <manufacturer>ABC company</manufacturer>
      <price units="dollar"> 27.00</price>
   </part>
   <part count="1">
      <item>Motor Oil</item>
      <partnum>B5-200</partnum>
      <source>XYZ company</source>
      <price units="dollar"> 14.00</price>
   </part>
   <part count="1">
      <item>Motor Oil</item>
      <partnum>B5-300</partnum>
      <source>XYZ company</source>
      <price units="dollar"> 16.75</price>
   </part>
   <part count="1">
      <item>Engine Coolant</item>
      <partnum>B6-120</partnum>
       <source>XYZ company</source>
      <price units="dollar"> 19.00</price>
   </part>
   <part count="1">
      <item>Engine Coolant</item>
      <partnum>B6-220</partnum>
      <source>XYZ company</source>
      <price units="dollar"> 18.25</price>
   </part>
</parts>
```

Complete the following steps to load the XML document:

1. Copy the content of the XML document into a file on your file system.

   This example assumes that the file is named `auto-parts.xml` in the `/examples/xml/` directory.
2. Stage the file in the internal staging location:

   Copy code

   ```
   PUT FILE:///examples/xml/auto-parts.xml @~/xml_stage;
   ```
3. Create a table for the XML document:

   Copy code

   ```
   CREATE OR REPLACE TABLE sample_xml_parts(src VARIANT);
   ```
4. Load the staged XML file into the table:

   Copy code

   ```
   COPY INTO sample_xml_parts
     FROM @~/xml_stage
     FILE_FORMAT=(TYPE=XML) ON_ERROR='CONTINUE';
   ```

#### Examples of querying XML data

These examples query XML data.

##### Query XML data directly

Query the column that contains the XML data to return the XML document.

This example queries the XML data loaded in [Example of loading an XML document](#label-xml-example-document) directly:

Copy code

```
SELECT src FROM sample_xml_parts;
```

```
+----------------------------------------------+
| SRC                                          |
|----------------------------------------------|
| <parts>                                      |
|   <part count="4">                           |
|     <item>Spark Plugs</item>                 |
|     <partnum>A3-400</partnum>                |
|     <manufacturer>ABC company</manufacturer> |
|     <price units="dollar">27.00</price>      |
|   </part>                                    |
|   <part count="1">                           |
|     <item>Motor Oil</item>                   |
|     <partnum>B5-200</partnum>                |
|     <source>XYZ company</source>             |
|     <price units="dollar">14.00</price>      |
|   </part>                                    |
|   <part count="1">                           |
|     <item>Motor Oil</item>                   |
|     <partnum>B5-300</partnum>                |
|     <source>XYZ company</source>             |
|     <price units="dollar">16.75</price>      |
|   </part>                                    |
|   <part count="1">                           |
|     <item>Engine Coolant</item>              |
|     <partnum>B6-120</partnum>                |
|     <source>XYZ company</source>             |
|     <price units="dollar">19.00</price>      |
|   </part>                                    |
|   <part count="1">                           |
|     <item>Engine Coolant</item>              |
|     <partnum>B6-220</partnum>                |
|     <source>XYZ company</source>             |
|     <price units="dollar">18.25</price>      |
|   </part>                                    |
| </parts>                                     |
+----------------------------------------------+
```

##### Query XML data using operators

Query the column that contains the XML data using the `$` and `@` operators.

This example queries the XML data loaded in [Example of loading an XML document](#label-xml-example-document) using the `$`
operator. The query shows metadata about the values (`$`) and names (`@`) of the elements.

Copy code

```
SELECT src:"$" FROM sample_xml_parts;
```

```
+--------------------------------+
| SRC:"$"                        |
|--------------------------------|
| [                              |
|   {                            |
|     "$": [                     |
|       {                        |
|         "$": "Spark Plugs",    |
|         "@": "item"            |
|       },                       |
|       {                        |
|         "$": "A3-400",         |
|         "@": "partnum"         |
|       },                       |
|       {                        |
|         "$": "ABC company",    |
|         "@": "manufacturer"    |
|       },                       |
|       {                        |
|         "$": 27,               |
|         "@": "price",          |
|         "@units": "dollar"     |
|       }                        |
|     ],                         |
|     "@": "part",               |
|     "@count": 4,               |
|     "item": 0,                 |
|     "manufacturer": 2,         |
|     "partnum": 1,              |
|     "price": 3                 |
|   },                           |
|   {                            |
|     "$": [                     |
|       {                        |
|         "$": "Motor Oil",      |
|         "@": "item"            |
|       },                       |
|       {                        |
|         "$": "B5-200",         |
|         "@": "partnum"         |
|       },                       |
|       {                        |
|         "$": "XYZ company",    |
|         "@": "source"          |
|       },                       |
|       {                        |
|         "$": 14,               |
|         "@": "price",          |
|         "@units": "dollar"     |
|       }                        |
|     ],                         |
|     "@": "part",               |
|     "@count": 1,               |
|     "item": 0,                 |
|     "partnum": 1,              |
|     "price": 3,                |
|     "source": 2                |
|   },                           |
|                                |
|              ...               |
|                                |
+--------------------------------+
```

This example queries the same XML data using the `@` operator. The query shows the name of the root element.

Copy code

```
SELECT src:"@" FROM sample_xml_parts;
```

```
+---------+
| SRC:"@" |
|---------|
| "parts" |
+---------+
```

This example queries the same XML data using `$` operator and the `@` operator. In the array of child
elements in the root element, the query shows the value of the `count` attribute for the element at the first (0)
and second (1) index.

Copy code

```
SELECT src:"$"[0]."@count", src:"$"[1]."@count" FROM sample_xml_parts;
```

```
+---------------------+---------------------+
| SRC:"$"[0]."@COUNT" | SRC:"$"[1]."@COUNT" |
|---------------------+---------------------|
| 4                   | 1                   |
+---------------------+---------------------+
```

##### Query XML data using the XMLGET function

Query the column that contains the XML data using the [XMLGET](/sql-reference/functions/xmlget) function.

This example queries the XML data loaded in [Example of loading an XML document](#label-xml-example-document) and returns the first
instance of an element in the root element of the XML data. The instance number is 0-based, not 1-based.
So, the following queries are equivalent:

Copy code

```
SELECT XMLGET(src, 'part') FROM sample_xml_parts;

SELECT XMLGET(src, 'part', 0) FROM sample_xml_parts;
```

```
+--------------------------------------------+
| XMLGET(SRC, 'PART')                        |
|--------------------------------------------|
| <part count="4">                           |
|   <item>Spark Plugs</item>                 |
|   <partnum>A3-400</partnum>                |
|   <manufacturer>ABC company</manufacturer> |
|   <price units="dollar">27.00</price>      |
| </part>                                    |
+--------------------------------------------+
```

This query returns the third element (0-based) in the root element of the XML data.

Copy code

```
SELECT XMLGET(src, 'part', 3) FROM sample_xml_parts;
```

```
+---------------------------------------+
| XMLGET(SRC, 'PART', 3)                |
|---------------------------------------|
| <part count="1">                      |
|   <item>Engine Coolant</item>         |
|   <partnum>B6-120</partnum>           |
|   <source>XYZ company</source>        |
|   <price units="dollar">19.00</price> |
| </part>                               |
+---------------------------------------+
```

##### Query XML data to extract element contents using multiple functions

This example uses the [FLATTEN](/sql-reference/functions/flatten) function with the [XMLGET](/sql-reference/functions/xmlget)
function to extract the contents of the elements in the XML data loaded in [Example of loading an XML document](#label-xml-example-document).

The example uses the [COALESCE](/sql-reference/functions/coalesce) function to return either the child element `manufacturer`
or `source` if it exists, cast to a VARCHAR value. The `SRC:"$"` passed to FLATTEN specifies the value in the root
element `parts`. The LATERAL FLATTEN iterates through all of the repeating elements that are passed in.

Copy code

```
SELECT XMLGET(VALUE, 'item'):"$"::VARCHAR AS item,
       XMLGET(VALUE, 'partnum'):"$"::VARCHAR AS partnum,
       COALESCE(XMLGET(VALUE, 'manufacturer'):"$"::VARCHAR,
                XMLGET(VALUE, 'source'):"$"::VARCHAR) AS manufacturer_or_source,
       XMLGET(VALUE, 'price'):"$"::VARCHAR AS price,
  FROM sample_xml_parts,
    LATERAL FLATTEN(INPUT => SRC:"$");
```

```
+----------------+---------+------------------------+-------+
| ITEM           | PARTNUM | MANUFACTURER_OR_SOURCE | PRICE |
|----------------+---------+------------------------+-------|
| Spark Plugs    | A3-400  | ABC company            | 27    |
| Motor Oil      | B5-200  | XYZ company            | 14    |
| Motor Oil      | B5-300  | XYZ company            | 16.75 |
| Engine Coolant | B6-120  | XYZ company            | 19    |
| Engine Coolant | B6-220  | XYZ company            | 18.25 |
+----------------+---------+------------------------+-------+
```
