# CREATE CUSTOM\_CLASSIFIER

*Fully qualified name:* SNOWFLAKE.DATA\_PRIVACY.CUSTOM\_CLASSIFIER

[Enterprise Edition Feature](/user-guide/intro-editions)

Sensitive data classification requires Enterprise Edition or higher. To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

See also:
:   [Using custom classifiers to implement custom semantic categories](/user-guide/classify-custom-using)

Creates a new custom classification instance or replaces an existing custom classification instance in the current or specified schema.

## Syntax

Copy code

```
CREATE [ OR REPLACE ] SNOWFLAKE.DATA_PRIVACY.CUSTOM_CLASSIFIER
[ IF NOT EXISTS ] <custom_classifier_name>()
```

## Parameters

`custom_classifier_name()`
:   Specifies the identifier (name) for the instance; the name must be unique for the schema in which the object is created. You must add the
    parentheses at the end of the identifier when creating the object.

    In addition, the identifier must start with an alphabetic character and cannot contain spaces or special characters unless the
    entire identifier string is enclosed in double quotes (for example, `"My object"`). Identifiers enclosed in double quotes are also
    case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

## Arguments

None.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Database role | Object | Notes |
| --- | --- | --- |
| CLASSIFICATION\_ADMIN | Database role | The account role that creates the object must be granted this database role.  This database role exists in the shared SNOWFLAKE database. |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Methods

You can call the following methods on the custom classification instance that you create:

- [<code className=”samp”><em>custom\_classifier</em></code>!ADD\_REGEX](/sql-reference/classes/custom_classifier/methods/add_regex)
- [<code className=”samp”><em>custom\_classifier</em></code>!DELETE\_CATEGORY](/sql-reference/classes/custom_classifier/methods/delete_category)
- [<code className=”samp”><em>custom\_classifier</em></code>!LIST](/sql-reference/classes/custom_classifier/methods/list)

## Usage notes

SNOWFLAKE.DATA\_PRIVACY.CUSTOM\_CLASSIFIER is a name that Snowflake defines and maintains. Use this object name every time you want to create
an instance of this class. Alternatively, update your [search path](/sql-reference/snowflake-db-classes#label-update-search-path) to make it easier to use the instance.

## Examples

Create a custom classifier named `medical_codes`:

Copy code

```
CREATE OR REPLACE SNOWFLAKE.DATA_PRIVACY.CUSTOM_CLASSIFIER internal_ids();
```
