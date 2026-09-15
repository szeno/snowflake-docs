Categories:
:   [System functions](/sql-reference/functions-system) (System Information)

# SYSTEM$GET\_TAG\_ALLOWED\_VALUES

Returns a comma-separated list of string values that can be set on a [supported object](/user-guide/object-tagging/introduction#label-object-tag-supported-objects), or NULL
to indicate the tag key does not have any specified string values and accepts all [possible](/user-guide/object-tagging/introduction) string
values.

See also:
:   [Set a list of allowed tag values](/user-guide/object-tagging/work#label-object-tagging-specify-tag-values) , [TAGS view](/sql-reference/account-usage/tags)

## Syntax

Copy code

```
SYSTEM$GET_TAG_ALLOWED_VALUES('<name>')
```

## Arguments

`name`
:   The fully-qualified name of the tag key as a string.

## Usage notes

- The role that calls this function must have USAGE or any other privilege on the parent database and schema of the tag, or the global APPLY
  TAG on ACCOUNT privilege.
- Snowflake returns NULL when you pass the SNOWFLAKE.CORE.SEMANTIC\_CATEGORY system tag as an argument in the function because there is not
  an allowed values constraint with this tag.

## Examples

Query the allowed tag values for the tag key named `cost_center`, which resides in the database named `governance` and the schema named
`tags`:

> Copy code
>
> ```
> select system$get_tag_allowed_values('governance.tags.cost_center');
> ```
