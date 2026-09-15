Categories:
:   [Semi-structured and structured data functions](/sql-reference/functions-semistructured) (Parsing)

# CHECK\_XML

Checks the validity of an [XML](/user-guide/semistructured-data-formats#label-xml-format) document. If the input string is NULL or a valid XML document,
the output is NULL. In case of an XML parsing error, the output string contains the error message.

See also:
:   [PARSE\_XML](/sql-reference/functions/parse_xml), [TO\_XML](/sql-reference/functions/to_xml), [XMLGET](/sql-reference/functions/xmlget)

## Syntax

Copy code

```
CHECK_XML( <string_containing_xml> [ , <disable_auto_convert> ] )
```

Copy code

```
CHECK_XML( STR => <string_containing_xml>
  [ , DISABLE_AUTO_CONVERT => <disable_auto_convert> ] )
```

## Arguments

**Required:**

`string_containing_xml` OR `STR => string_containing_xml`
:   Specify an expression that evaluates to a VARCHAR value that contains valid XML.

**Optional:**

`disable_auto_convert` OR `DISABLE_AUTO_CONVERT => disable_auto_convert`
:   Specify the same value that you pass to the [PARSE\_XML](/sql-reference/functions/parse_xml) function.

    Default: `FALSE`

## Returns

The data type of the returned value is VARCHAR.

## Usage notes

- When you mix arguments by position and by name, all of the positional arguments must come before
  all of the named arguments.
- When you specify an argument by name, you can’t use double quotes around the argument name.

## Examples

The following examples use the CHECK\_XML function.

### Show the output of the function when the XML is valid

Copy code

```
SELECT CHECK_XML('<name> Valid </name>');
```

```
+-----------------------------------+
| CHECK_XML('<NAME> VALID </NAME>') |
|-----------------------------------|
| NULL                              |
+-----------------------------------+
```

### Show the output of the function when the XML is invalid

Copy code

```
SELECT CHECK_XML('<name> Invalid </WRONG_CLOSING_TAG>');
```

```
+--------------------------------------------------+
| CHECK_XML('<NAME> INVALID </WRONG_CLOSING_TAG>') |
|--------------------------------------------------|
| no opening tag for </WRONG_CLOSING_TAG>, pos 35  |
+--------------------------------------------------+
```

### Locate records with invalid XML

Copy code

```
SELECT xml_str, CHECK_XML(xml_str)
  FROM my_table
  WHERE CHECK_XML(xml_str) IS NOT NULL;
```
