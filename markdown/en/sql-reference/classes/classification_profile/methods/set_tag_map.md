# <classification\_profile\_name>!SET\_TAG\_MAP

[Enterprise Edition Feature](/user-guide/intro-editions)

Sensitive data classification requires Enterprise Edition or higher. To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Adds a JSON object to an instance of the CLASSIFICATION\_PROFILE class to map user-defined [tags](/user-guide/object-tagging/introduction) to the
SEMANTIC\_CATEGORY system tag.

## Syntax

Copy code

```
<classification_profile_name>!SET_TAG_MAP( <object> )
```

## Arguments

`object`
> An [OBJECT](/sql-reference/data-types-semistructured#label-data-type-object) that maps one or more user-defined tags to the SEMANTIC\_CATEGORY system tag.
>
> `'column_tag_map': [ ... ]`
> :   An array of objects that have the following key-value pairs:
>
>     `'tag_name': 'string'`
>     :   The fully qualified name of the tag.
>
>         For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).
>
>     `'tag_value':'string'`
>     :   The string value of the tag.
>
>         Optional: If not specified, you must also omit the `semantic_categories` key. If omitted, the `tag_name` tag is applied to
>         every column to which the SEMANTIC\_CATEGORY system tag is applied, and the value of the user-defined tag will match the value of the
>         SEMANTIC\_CATEGORY tag.
>
>     `'semantic_categories': [ 'category' [ , 'category' ... ] ]`
>     :   A comma-separated list of [native categories](/user-guide/classify-native). The `tag_name` user-defined tag is mapped to
>         instances where the value of the SEMANTIC\_CATEGORY tag is one of the specified native categories.
>
>         Optional: If not specified, you must also omit the `tag_value` key. If omitted, the `tag_name` tag is applied to every
>         column to which the system SEMANTIC\_CATEGORY tag is applied, and the value of the user-defined tag will match the value of the
>         SEMANTIC\_CATEGORY tag.

## Returns

Returns a successful status message or an error message. For more information, see [About tag mapping](/user-guide/classify-auto#label-classify-auto-map-tags).

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Instance role | Object | Notes |
| --- | --- | --- |
| `classification_profile`!PRIVACY\_USER | The classification profile instance. | The account role that calls this method must be granted this instance role on the classification profile. The role used to create the instance is automatically granted this instance role. |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

Calling this method does not return the object. Because of this, you can’t use method chaining to call another method on the
return value of this method. Instead, call each method in a separate SQL statement.

- If the same tag and semantic category is mapped to two different values, then the order of the objects in the `column_tag_map`
  determines the tag and string value to set on a column. Order the `column_tag_map` arrays from highest preference to lowest
  preference.

## Examples

Map a single tag and its value to the `my_classification_profile` instance:

Copy code

```
CALL my_classification_profile!SET_TAG_MAP(
  {
    'column_tag_map':[
      {
        'tag_name':'tag_db.sch.pii',
        'tag_value':'important',
        'semantic_categories':['NAME']
      }
    ]
  }
);
```
