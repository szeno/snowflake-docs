# Notational conventions

The following notational conventions are used in Snowflake documentation.

Important

In syntax and code descriptions, angle brackets (`< >`), square brackets (`[ ]`), curly braces (`{ }`), and vertical bars (`|`) are used for notational purposes only. To
avoid syntax errors, do not include them when entering a command or writing code.

However, brackets and braces have specific meanings in JSON and XML, and therefore must be included when working with JSON or XML documents/data.

## Syntax, examples, and text

| Notation | Description |
| --- | --- |
| ITEM , `ITEM` | All-uppercase indicates a Snowflake SQL command, keyword, parameter name, or function name. |
| item , `item` | All-lowercase indicates a user-supplied value for an identifier, parameter, or argument. |
| *<item>* , `item` | Angle brackets and italics indicate identifiers, parameters, or arguments that are provided by users. |
| `( item1 item2 ... )` | Parentheses are used in SQL to group parameters or arguments.  They are required when entering a command (i.e. they must be typed exactly as they appear). |
| `{ item1 item2 ... }` | Curly braces indicate groupings of identifiers, parameters, or arguments.  Curly braces are also used with vertical bars to delimit choices when more than one choice is available.  In both of those cases, the curly braces should not be entered. |
| `[ ITEM ]` , `[ item1 item2 ... ]` | Square brackets indicate optional parts of a statement. They should not be entered.  In many cases, items in the square brackets are optional because default values are provided. |
| `|` | A vertical bar indicates a choice between two or more items or values, usually within square brackets or curly braces. The square brackets or curly braces should not be entered. |
| `...` (ellipsis) | The previous item can be repeated an indefinite number of times. |

Expand

Show lessSee more

### Examples

In the following, the keyword `WORK` is optional:

Copy code

```
BEGIN [ WORK ]
```

Therefore, either of the following are valid:

Copy code

```
BEGIN;
BEGIN WORK;
```

In the following, you can use either the keyword `WORK` or the keyword `TRANSACTION`. You must not use both. You can omit both.

Copy code

```
BEGIN [ { WORK | TRANSACTION } ]
```

Therefore, any of the following are valid:

Copy code

```
BEGIN;
BEGIN WORK;
BEGIN TRANSACTION;
```

The following shows the syntax of a function call that accepts one argument. The parentheses are required.
The `<function_name>`, `<argument_name>`, and `<data_type>` should be replaced with the actual names:

Copy code

```
create function <function_name>( <argument_name> <data_type> )
```

Therefore, the following is valid:

Copy code

```
create function my_function(my_argument integer)
```

The following shows a function that requires at least one argument and accepts optional additional arguments.

Copy code

```
<function_name>( <argument_name> <data_type> [ , <argument_name> data_type ] ... )
```

Therefore, the following are valid:

Copy code

```
my_function(argument_1 integer)
my_function(argument_1 integer, argument_2 integer)
my_function(argument_1 integer, argument_2 integer, argument_3 varchar)
```

In this case, additional arguments are also allowed.

## JSON data

| Notation | Description |
| --- | --- |
| `[ item1 ... ]` | Square brackets are JSON array delimiters. |
| `{ item1 item2 ... }` | Curly braces are JSON object delimiters. |

Expand

Show lessSee more

## XML data

| Notation | Description |
| --- | --- |
| `<item> ... </item>` | Angle brackets indicate the start or end of an XML element. |

Expand

Show lessSee more
