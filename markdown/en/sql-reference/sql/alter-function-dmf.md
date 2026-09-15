# ALTER FUNCTION (DMF)

[Enterprise Edition Feature](/user-guide/intro-editions)

Data Quality Monitoring requires Enterprise Edition. To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Modifies the properties of an existing data metric function (DMF).

To make any other changes to a DMF, you must drop the function using a [DROP FUNCTION](/sql-reference/sql/drop-function) command and
recreate the DMF.

## Syntax

Copy code

```
ALTER FUNCTION [ IF EXISTS ] <name> ( TABLE(  <arg_data_type> [ , ... ] ) [ , TABLE( <arg_data_type> [ , ... ] ) ] )
  RENAME TO <new_name>

ALTER FUNCTION [ IF EXISTS ] <name> ( TABLE(  <arg_data_type> [ , ... ] ) [ , TABLE( <arg_data_type> [ , ... ] ) ] )
  SET SECURE

ALTER FUNCTION [ IF EXISTS ] <name> ( TABLE(  <arg_data_type> [ , ... ] ) [ , TABLE( <arg_data_type> [ , ... ] ) ] )
  UNSET SECURE

ALTER FUNCTION [ IF EXISTS ] <name> ( TABLE(  <arg_data_type> [ , ... ] ) [ , TABLE( <arg_data_type> [ , ... ] ) ] )
  SET COMMENT = '<string_literal>'

ALTER FUNCTION [ IF EXISTS ] <name> ( TABLE(  <arg_data_type> [ , ... ] ) [ , TABLE( <arg_data_type> [ , ... ] ) ] )
  UNSET COMMENT

ALTER FUNCTION [ IF EXISTS ] <name> ( TABLE(  <arg_data_type> [ , ... ] ) [ , TABLE( <arg_data_type> [ , ... ] ) ] )
  SET TAG <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' ... ]

ALTER FUNCTION [ IF EXISTS ] <name> ( TABLE(  <arg_data_type> [ , ... ] ) [ , TABLE( <arg_data_type> [ , ... ] ) ] )
  UNSET TAG <tag_name> [ , <tag_name> ... ]
```

## Parameters

`name`
:   Specifies the identifier for the DMF to alter.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

`TABLE( arg_data_type [ , ... ] ) [ , TABLE( <arg_data_type> [ , ... ] ) ]`
:   Specifies the data type of the column arguments for the DMF. The data types are necessary because DMFs support name
    overloading, where two DMFs in the same schema can have the same name. The data types of the arguments are used to identify the DMF you
    want to alter.

`RENAME TO new_name`
:   Specifies the new identifier for the DMF; the combination of the identifier and existing argument data types must be unique for the
    schema.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

    Note

    When specifying the new name for the UDF, don’t specify argument data types or parentheses; specify only the new name.

    You can move the object to a different database and/or schema while optionally renaming the object. To do so, specify
    a qualified `new_name` value that includes the new database and/or schema name in the form
    `db_name.schema_name.object_name` or `schema_name.object_name`, respectively.

    Note

    - The destination database and/or schema must already exist. In addition, an object with the same name cannot already
      exist in the new location; otherwise, the statement returns an error.
    - Moving an object to a managed access schema is prohibited unless the object owner (that is, the role that has
      the OWNERSHIP privilege on the object) also owns the target schema.

    When an object is renamed, other objects that reference it must be updated with the new name.

`SET ...`
:   Specifies the properties to set for the DMF:

    `SECURE`
    :   Specifies whether a function is secure. For more information, see [Protecting Sensitive Information with Secure UDFs and Stored Procedures](/developer-guide/secure-udf-procedure).

    `COMMENT = 'string_literal'`
    :   Adds a comment or overwrites the existing comment for the function. The value you specify is displayed in the `DESCRIPTION`
        column in the [SHOW FUNCTIONS](/sql-reference/sql/show-functions) and [SHOW USER FUNCTIONS](/sql-reference/sql/show-user-functions) output.

    `TAG tag_name = 'tag_value' [ , tag_name = 'tag_value' , ... ]`
    :   Specifies the [tag](/user-guide/object-tagging/introduction) name and the tag string value.

        The tag value is always a string, and the maximum number of characters for the tag value is 256.

        For information about specifying tags in a statement, see [Tag quotas](/user-guide/object-tagging/introduction#label-object-tagging-quota).

`UNSET ...`
:   Specifies the properties to unset for the function, which resets them to the defaults.

    - `SECURE`
    - `COMMENT`
    - `TAG tag_name [ , tag_name ... ]`

## Access control requirements

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP | Data metric function |  |
| APPLY | Tag | Enables setting a tag on the DMF. |

Expand

Show lessSee more

## Usage notes

- If you want to update an existing data metric function and need to see the current definition of the function, run the
  [DESCRIBE FUNCTION (DMF)](/sql-reference/sql/desc-function-dmf) command or call the [GET\_DDL](/sql-reference/functions/get_ddl) function.
- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

## Example

You can use the ALTER FUNCTION command to make a DMF secure. For more information about what it means for a function to be secure, see
[Protecting Sensitive Information with Secure UDFs and Stored Procedures](/developer-guide/secure-udf-procedure).

Copy code

```
ALTER FUNCTION governance.dmfs.count_positive_numbers(
 TABLE(
   NUMBER,
   NUMBER,
   NUMBER
))
SET SECURE;
```
