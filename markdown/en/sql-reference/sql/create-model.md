# CREATE MODEL

Creates a new machine learning model in the current/specified schema or replaces an existing model.

Note

Use the [Snowflake Model Registry](/developer-guide/snowflake-ml/model-registry/overview) Python API
to create models from scratch. In SQL, you can only create models from other models.

Models are versioned. All models must have at least one version, and one version must be designated as the default. To add
a version to a model, use [ALTER MODEL … ADD VERSION](/sql-reference/sql/alter-model-add-version).

Some properties of a model can be modified (see [ALTER MODEL](/sql-reference/sql/alter-model)), and multiple versions can be added.

This command also supports the following variant:

- CREATE MODEL … FROM internalStage (creates a model from files in an external stage)

See also:
:   [ALTER MODEL](/sql-reference/sql/alter-model) , [ALTER MODEL … ADD VERSION](/sql-reference/sql/alter-model-add-version) , [DROP MODEL](/sql-reference/sql/drop-model) , [SHOW MODELS](/sql-reference/sql/show-models)

## Syntax

Copy code

```
CREATE [ OR REPLACE ] MODEL [ IF NOT EXISTS ] <name> [ WITH VERSION <version_name> ]
    FROM MODEL <source_model_name> [ VERSION <source_version_or_alias_name> ]
```

## Variant Syntax

This variant is used by the [Snowflake Model Registry](/developer-guide/snowflake-ml/model-registry/overview) Python API.
It is not possible to create models from scratch in SQL.

Copy code

```
CREATE [ OR REPLACE ] MODEL [ IF NOT EXISTS ] <name> [ WITH VERSION <version_name> ]
  FROM internalStage
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

## Required parameters

`name`
:   String that specifies the identifier (i.e. name) for the new model; must be unique for the schema in which the model
    is created.

    In addition, the identifier must start with an alphabetic character and cannot contain spaces or special characters unless the
    entire identifier string is enclosed in double quotes (for example, `"My object"`). Identifiers enclosed in double quotes are also
    case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

`FROM MODEL source_model_name`
:   Required if not using FROM internalStage variant
    :   Specifies the name of the model from which to create the new model.

`FROM internalStage`
:   Required if using FROM internalStage variant
    :   Specifies the internal stage that contains the model’s files. The required layout of these files is not currently
        documented.

## Optional parameters

`WITH VERSION version_name`
:   For use with FROM MODEL variant
    :   Specifies the name of the version to create in the new model.

`VERSION source_version_or_alias_name`
:   For use with FROM MODEL variant
    :   Specifies the name or alias of the version to be copied from the source model. If not specified, uses the default version
        from the source model.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| CREATE MODEL | Schema | Implied by OWNERSHIP on schema |
| OWNERSHIP | Model | A role must be granted or inherit the OWNERSHIP privilege on the object to create a temporary object that has the same name as the object that already exists in the schema. |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- The OR REPLACE and IF NOT EXISTS clauses are mutually exclusive. They can’t both be used in the same statement.
- CREATE OR REPLACE *<object>* statements are atomic. That is, when an object is replaced, the old object is deleted and the new object is created in a single transaction.
