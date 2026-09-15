# ALTER STREAM

Modifies the properties, columns, or constraints for an existing [stream](/user-guide/streams-intro).

See also:
:   [CREATE STREAM](/sql-reference/sql/create-stream) , [DROP STREAM](/sql-reference/sql/drop-stream) , [SHOW STREAMS](/sql-reference/sql/show-streams) , [DESCRIBE STREAM](/sql-reference/sql/desc-stream)

## Syntax

Copy code

```
ALTER STREAM [ IF EXISTS ] <name> SET COMMENT = '<string_literal>'

ALTER STREAM [ IF EXISTS ] <name> SET TAG <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' ... ]

ALTER STREAM <name> UNSET TAG <tag_name> [ , <tag_name> ... ]

ALTER STREAM [ IF EXISTS ] <name> UNSET COMMENT
```

## Parameters

`name`
:   Identifier for the stream to alter. If the identifier contains spaces or special characters, the entire string must be enclosed in double
    quotes. Identifiers enclosed in double quotes are also case-sensitive.

`SET ...`
:   Specifies the properties to set for the stream:

    `TAG tag_name = 'tag_value' [ , tag_name = 'tag_value' , ... ]`
    :   Specifies the [tag](/user-guide/object-tagging/introduction) name and the tag string value.

        The tag value is always a string, and the maximum number of characters for the tag value is 256.

        For information about specifying tags in a statement, see [Tag quotas](/user-guide/object-tagging/introduction#label-object-tagging-quota).

    `COMMENT = 'string'`
    :   Adds a comment or overwrites an existing comment for the stream.

`UNSET ...`
:   Specifies one or more properties/parameters to unset for the stream, which resets them back to their defaults:

    - `TAG tag_key [ , tag_key ... ]`
    - `COMMENT`

## Usage notes

Regarding metadata:

> Attention
>
> Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

## Examples

Add a comment for a stream:

> Copy code
>
> ```
> ALTER STREAM mystream SET COMMENT = 'New comment for stream';
> ```
