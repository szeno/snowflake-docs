Categories:
:   [Semi-structured and structured data functions](/sql-reference/functions-semistructured) (Extraction)

# XMLGET

Extracts an [XML](/user-guide/semistructured-data-formats#label-xml-format) element object (often referred to as simply a *tag*) from the content of
the outer XML element based on the name and instance number of the specified tag.

(Note that an XML tag is not the same as a Snowflake [data governance tag](/user-guide/object-tagging/introduction#label-what-is-a-tag).)

See also:
:   [CHECK\_XML](/sql-reference/functions/check_xml), [PARSE\_XML](/sql-reference/functions/parse_xml), [TO\_XML](/sql-reference/functions/to_xml)

## Syntax

Copy code

```
XMLGET( <expression> , <tag_name> [ , <instance_number> ] )
```

## Arguments

`expression`
:   The expression from which to extract the element.

    The expression must evaluate to an [OBJECT](/sql-reference/data-types-semistructured#label-data-type-object) (or a VARIANT containing an OBJECT). The OBJECT must contain
    valid XML in the internal format that Snowflake supports. Typically, that means that the OBJECT was produced by one of the
    following:

    - Calling the [PARSE\_XML](/sql-reference/functions/parse_xml) function.
    - Loading the data (e.g. via the [COPY INTO <table>](/sql-reference/sql/copy-into-table) command) and specifying that the data is in XML
      format.

    The XMLGET function does not operate directly on a VARCHAR expression even if that VARCHAR contains valid XML text.

`tag_name`
:   The name of an XML tag stored in the `expression`.

`instance_number`
:   If the XML contains multiple instances of `tag_name`, then use `instance_number` to specify which instance to
    retrieve. Like an array index, the `instance_number` is 0-based, not 1-based.

    `instance_number` can be omitted, in which case the default value 0 is used.

## Returns

The data type of the returned value is [OBJECT](/sql-reference/data-types-semistructured#label-data-type-object).

The function returns NULL in the following cases:

- If any argument of XMLGET is NULL.
- If the tag instance isn’t found.

See the Usage Notes for more details.

## Usage notes

- The result of XMLGET isn’t the content of the tag (that is, the text between the tags), but the entire element (the opening tag,
  content, and closing tag). From the returned OBJECT value, you can extract the tag name, the tag’s attribute values, and the contents
  of the element (including nested tags) by using the [GET](/sql-reference/functions/get) function:

  - To extract attribute values, use `GET(tag, '@attrname')`.
  - To extract the content, use `GET(tag, '$')`.
  - To extract the tag name, use `GET(tag, '@')`.
- You can extract nested tags by nesting XMLGET function calls. For example:

  Copy code

  ```
  SELECT XMLGET(XMLGET(my_xml_column, 'my_tag'), 'my_inner_tag') ...;
  ```
- Positions of the inner tags in the content can be obtained by using `GET(tag, 'inner-tag-name')`. If the content contains
  multiple elements, the positions are represented as an array.
- You can’t use XMLGET to extract the outermost element. To get the outermost element, select the `expression`
  itself.

## Examples

The following example creates a table with an OBJECT that contains XML, then uses the XMLGET function to extract elements from
that OBJECT.

Copy code

```
CREATE OR REPLACE TABLE xml_demo (id INTEGER, object_col OBJECT);

INSERT INTO xml_demo (id, object_col)
  SELECT 1001,
    PARSE_XML('<level1> 1 <level2> 2 <level3> 3A </level3> <level3> 3B </level3> </level2> </level1>');
```

Copy code

```
SELECT object_col,
       XMLGET(object_col, 'level2'),
       XMLGET(XMLGET(object_col, 'level2'), 'level3', 1)
  FROM xml_demo;
```

```
+-------------------------+------------------------------+---------------------------------------------------+
| OBJECT_COL              | XMLGET(OBJECT_COL, 'LEVEL2') | XMLGET(XMLGET(OBJECT_COL, 'LEVEL2'), 'LEVEL3', 1) |
|-------------------------+------------------------------+---------------------------------------------------|
| <level1>                | <level2>                     | <level3>3B</level3>                               |
|   1                     |   2                          |                                                   |
|   <level2>              |   <level3>3A</level3>        |                                                   |
|     2                   |   <level3>3B</level3>        |                                                   |
|     <level3>3A</level3> | </level2>                    |                                                   |
|     <level3>3B</level3> |                              |                                                   |
|   </level2>             |                              |                                                   |
| </level1>               |                              |                                                   |
+-------------------------+------------------------------+---------------------------------------------------+
```

This example shows how to use GET with XMLGET to retrieve the content of an element. In the example, the `level2` tag
contains three items (text and two nested tags), so GET returns these items in an [ARRAY](/sql-reference/data-types-semistructured#label-data-type-array). The
nested tags are represented by OBJECTs (key-value pairs). The `@` property contains the nested tag name and the `$` property
contains the nested tag contents.

Copy code

```
SELECT object_col,
       GET(XMLGET(object_col, 'level2'), '$') AS content_of_element
  FROM xml_demo;
```

```
+-------------------------+--------------------+
| OBJECT_COL              | CONTENT_OF_ELEMENT |
|-------------------------+--------------------|
| <level1>                | [                  |
|   1                     |   2,               |
|   <level2>              |   {                |
|     2                   |     "$": "3A",     |
|     <level3>3A</level3> |     "@": "level3"  |
|     <level3>3B</level3> |   },               |
|   </level2>             |   {                |
| </level1>               |     "$": "3B",     |
|                         |     "@": "level3"  |
|                         |   }                |
|                         | ]                  |
+-------------------------+--------------------+
```

This example shows how to use GET with XMLGET to retrieve an attribute of a tag.

Copy code

```
INSERT INTO xml_demo (id, object_col)
  SELECT 1002,
      PARSE_XML('<level1> 1 <level2 an_attribute="my attribute"> 2 </level2> </level1>');
```

Copy code

```
SELECT object_col,
       GET(XMLGET(object_col, 'level2'), '@an_attribute') AS attribute
  FROM xml_demo
  WHERE ID = 1002;
```

```
+--------------------------------------------------+----------------+
| OBJECT_COL                                       | ATTRIBUTE      |
|--------------------------------------------------+----------------|
| <level1>                                         | "my attribute" |
|   1                                              |                |
|   <level2 an_attribute="my attribute">2</level2> |                |
| </level1>                                        |                |
+--------------------------------------------------+----------------+
```

Note

For more examples of queries that use the XMLGET function, see [Examples of working with XML](/user-guide/semistructured-data-formats#label-xml-examples).
