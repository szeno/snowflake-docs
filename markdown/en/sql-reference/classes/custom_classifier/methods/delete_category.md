# <code className=”samp”><em>custom\_classifier</em></code>!DELETE\_CATEGORY

[Enterprise Edition Feature](/user-guide/intro-editions)

Sensitive data classification requires Enterprise Edition or higher. To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

See also:
:   [Using custom classifiers to implement custom semantic categories](/user-guide/classify-custom-using)

Deletes the specified semantic category with its associated privacy category, regular expression, and comment from the instance.

## Syntax

Copy code

```
<custom_classifier>!DELETE_CATEGORY( '<semantic_category>' )
```

## Arguments

`semantic_category`
:   Specifies the identifier (name) for the semantic category that you added to the instance when calling the
    [<code className=”samp”><em>custom\_classifier</em></code>!ADD\_REGEX](/sql-reference/classes/custom_classifier/methods/add_regex) method.

## Output

Returns a status message indicating the deletion of the specified semantic category.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Instance role | Object | Notes |
| --- | --- | --- |
| `custom_classifier`!PRIVACY\_USER | The custom classification instance. | The account role that calls this method must be granted this instance role on the custom classifier.  By default, the account role used to create the instance can call this method. |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

Call the method in a separate SQL statement (no method chaining).

## Examples

Delete a category from the `medical_codes` instance:

Copy code

```
CALL medical_codes!DELETE_CATEGORY('IC_10_CODES');
```

Returns:

```
+------------------------------+
|       DELETE_CATEGORY        |
+------------------------------+
| Deleted category IC_10_CODES |
+------------------------------+
```
