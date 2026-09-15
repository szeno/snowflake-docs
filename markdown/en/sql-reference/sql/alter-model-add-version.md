# ALTER MODEL … ADD VERSION

Adds a new version to an existing model from an existing model version. Versions are the actual model code that contains
methods that can be called to perform inference and other functions.

Note

Use the [Snowflake Model Registry](/developer-guide/snowflake-ml/model-registry/overview) Python API
to create model versions from scratch. In SQL, you can only create model versions from existing model versions.

Some version properties can be modified (see [ALTER MODEL … MODIFY VERSION](/sql-reference/sql/alter-model-modify-version)), but the actual model implementation
contained in a version is immutable.

This command also supports the following variant:

- ALTER MODEL .. ADD VERSION … FROM internalStage (creates a model version from an internal stage)

See also:
:   [ALTER MODEL … MODIFY VERSION](/sql-reference/sql/alter-model-modify-version), [ALTER MODEL … DROP VERSION](/sql-reference/sql/alter-model-drop-version)

## Syntax

Copy code

```
ALTER MODEL [ IF EXISTS ] <name> ADD VERSION <version_name>
  FROM MODEL <source_model_name> [ VERSION <source_version_name> ]
```

## Variant Syntax

This variant is used by the [Snowflake Model Registry](/developer-guide/snowflake-ml/model-registry/overview) Python API.
It is not possible to create model versions from scratch in SQL.

Copy code

```
ALTER MODEL [ IF EXISTS ] <name> ADD VERSION <version_name> FROM internalStage
```

Where:

Copy code

```
internalStage ::=
    @[<namespace>.]<int_stage_name>[/<path>]
| @[<namespace>.]%<table_name>[/<path>]
| @~[/<path>]
```

For additional internal stage details, see [Choosing an internal stage for local files](/user-guide/data-load-local-file-system-create-stage).

## Parameters

`name`
:   Specifies the identifier of the model. If the identifier contains spaces, special characters, or mixed-case
    characters, the entire identifier must be enclosed in double quotes. Identifiers enclosed in double quotes are also
    case-sensitive. For information on identifier syntax, see [Identifier requirements](/sql-reference/identifiers-syntax).

`ADD VERSION version_name`
:   Specifies the identifier of the version, which must be unique within the model. If the identifier contains
    spaces, special characters, or mixed-case characters, the entire identifier must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive. For information on identifier syntax, see
    [Identifier requirements](/sql-reference/identifiers-syntax).

`FROM MODEL source_model_name [ VERSION source_version_or_alias_name ]`
:   Required if not using FROM internalStage variant
    :   Specifies the name of the model from which the version will be obtained.

        To obtain a specific version of that model, specify the `VERSION source_version_or_alias_name` clause. If
        you omit this clause, the command obtains the default version of the source model.

`FROM internalStage`
:   Required if using FROM internalStage variant
    :   Specifies the internal stage that contains the version’s files.
