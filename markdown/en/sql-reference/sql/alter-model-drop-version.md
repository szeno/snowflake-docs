# ALTER MODEL … DROP VERSION

Removes a version from the specified machine learning model.

See also:
:   [ALTER MODEL … ADD VERSION](/sql-reference/sql/alter-model-add-version), [ALTER MODEL … MODIFY VERSION](/sql-reference/sql/alter-model-modify-version)

## Syntax

Copy code

```
ALTER MODEL [ IF EXISTS ] <name> DROP VERSION <version_name>
```

## Parameters

`name`
:   Specifies the identifier of the model. If the identifier contains spaces, special characters, or mixed-case
    characters, the entire identifier must be enclosed in double quotes. Identifiers enclosed in double quotes are also
    case-sensitive. For information on identifier syntax, see [Identifier requirements](/sql-reference/identifiers-syntax).

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

`version_name`
:   Specifies the identifier of the version to be removed.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

## Usage notes

Aliases are alternative names for model versions. In addition to aliases you create, the following three system aliases are available.

- `DEFAULT` refers to the default version of the model.
- `FIRST` refers to the oldest version of the model by creation time.
- `LAST` refers to the newest version of the model by creation time.

When you drop the first or last model version, the corresponding system alias, `FIRST` or `LAST`, adjusts to point
to the new first or last alias.

You cannot drop the default version of a model. Change the default to a different version, if there is one, using
[ALTER MODEL … SET DEFAULT VERSION](/sql-reference/sql/alter-model), then drop the unneeded version. If there is no other version to
select as the default, because the model has only one version, [drop the entire model](/sql-reference/sql/drop-model).
