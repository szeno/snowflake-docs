# DROP FILE FORMAT

Removes the specified file format from the current/specified schema.

See also:
:   [CREATE FILE FORMAT](/sql-reference/sql/create-file-format) , [ALTER FILE FORMAT](/sql-reference/sql/alter-file-format) , [SHOW FILE FORMATS](/sql-reference/sql/show-file-formats) , [DESCRIBE FILE FORMAT](/sql-reference/sql/desc-file-format)

## Syntax

Copy code

```
DROP FILE FORMAT [ IF EXISTS ] <name>
```

## Parameters

`name`
:   Specifies the identifier for the file format to drop. If the identifier contains spaces, special characters, or mixed-case characters,
    the entire string must be enclosed in double quotes. Identifiers enclosed in double quotes are also case-sensitive.

## Usage notes

- Dropped file formats cannot be recovered; they must be recreated.
- Dropping a file format that is referenced in another object (e.g. named stage) does not cause errors because the object uses the
  file format defaults in place of the dropped file format.

- When the IF EXISTS clause is specified and the target object doesn’t exist, the command completes successfully
  without returning an error.

## Examples

> Copy code
>
> ```
> DROP FILE FORMAT my_format;
>
> ---------------------------------+
>            status                |
> ---------------------------------+
> MY_FORMAT successfully dropped.  |
> ---------------------------------+
> ```
