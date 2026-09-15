# <code className=”samp”><em>custom\_classifier</em></code>!LIST

[Enterprise Edition Feature](/user-guide/intro-editions)

Sensitive data classification requires Enterprise Edition or higher. To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Lists each custom classification semantic category system tag with its associated regular expressions for the column name and values in the
column, the description, and the privacy category tag.

See also:
:   [Using custom classifiers to implement custom semantic categories](/user-guide/classify-custom-using)

## Syntax

Copy code

```
<custom_classifier>!LIST()
```

## Arguments

None.

## Output

Returns a JSON object with the following structure:

Copy code

```
{
  "semantic_category_name": {
    "col_name_regex": "string",
    "description": "string",
    "privacy_category": "string",
    "threshold": number,
    "value_regex": "string"
   }
}
```

Each field value corresponds to the value that you specify when calling the
[<code className=”samp”><em>custom\_classifier</em></code>!ADD\_REGEX](/sql-reference/classes/custom_classifier/methods/add_regex) method.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Instance role | Object | Notes |
| --- | --- | --- |
| `custom_classifier`!PRIVACY\_USER | The custom classifier instance. | The role that calls this method must be granted the instance role.  By default, the account role used to create the instance can call this method. |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

Call each method in a separate SQL statement (no method chaining).

## Examples

Copy code

```
SELECT internal_ids!LIST();
```

Returns:

```
+--------------------------------------------------------------------------------+
| INTERNAL_IDS!LIST()                                                            |
+--------------------------------------------------------------------------------+
| {                                                                              |
|   "EMPLOYEE_ID": {                                                             |
|     "col_name_regex": "EMP.*ID.*",                                             |
|     "description": "Add a regex to identify employee IDs in a column",         |
|     "privacy_category": "IDENTIFIER",                                          |
|     "threshold": 0.8,                                                          |
|     "value_regex": "^[0-9]{6}$"                                                |
|   }                                                                            |
| }                                                                              |
+--------------------------------------------------------------------------------+
```
