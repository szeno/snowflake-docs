# ALTER MODEL … MODIFY VERSION

Modifies a version of a model, changing the version’s comment or metadata.

See also:
:   [ALTER MODEL … ADD VERSION](/sql-reference/sql/alter-model-add-version), [ALTER MODEL … DROP VERSION](/sql-reference/sql/alter-model-drop-version)

## Syntax

Copy code

```
ALTER MODEL [ IF EXISTS ] <name> MODIFY VERSION <version_or_alias_name> SET
  [ COMMENT = '<string_literal>' ]
  [ METADATA = '<json_metadata>']
```

## Parameters

`name`
:   Specifies the identifier of the model.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

`version_or_alias_name`
:   Specifies the identifier of the version, either its version name or its alias. Version names that contain spaces or
    that are case sensitive must be enclosed in double quotes. For information on identifier syntax, see
    [Identifier requirements](/sql-reference/identifiers-syntax).

    Aliases must be valid identifiers without double quotes.

    See [Usage Notes](#usage-notes) for more information on aliases.

`SET ...`
:   Specifies one or more model version properties to be set.

    `COMMENT = 'string_literal'`
    :   Sets the comment of the version.

    `METADATA = 'json_metadata'`
    :   Sets the metadata of the version. Metadata is a JSON object that stores key-value pairs of your choosing.

## Usage notes

Aliases are alternative names for model versions. In addition to aliases you create, the following three system aliases are available.

- `DEFAULT` refers to the default version of the model.
- `FIRST` refers to the oldest version of the model by creation time.
- `LAST` refers to the newest version of the model by creation time.
