Schema:
:   [ORGANIZATION\_USAGE](/sql-reference/organization-usage)

    For guidance on query performance when using organization-wide usage views, see [Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance).

# TAG\_REFERENCES view

[Enterprise Edition Feature](/user-guide/intro-editions)

Available in the organization account, which requires Enterprise Edition or higher. To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Important

This view is only available in the organization account. For more information, see [Premium views in the organization account](/user-guide/organization-accounts-premium-views).

Organization Usage performance

When you query a specific view in the `SNOWFLAKE.ORGANIZATION_USAGE` schema, follow the organization-wide guidance in
[Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance): bound every scan on history views, list
columns explicitly, and use the time filter column table plus worked SQL and anti-patterns there.

This Organization Usage view can be used to identify the associations between objects and tags.

This view only records the direct relationship between the object and the tag. [Tag inheritance](/user-guide/object-tagging/inheritance) is not included in this view.

The view is complementary to the information schema table function [TAG\_REFERENCES](/sql-reference/functions/tag_references).

## Columns

**Organization-level columns**

| Column Name | Data Type | Description |
| --- | --- | --- |
| ORGANIZATION\_NAME | VARCHAR | Name of the organization. |
| ACCOUNT\_LOCATOR | VARCHAR | System-generated identifier for the account. |
| ACCOUNT\_NAME | VARCHAR | User-defined identifier for the account. |

Expand

Show lessSee more

**Additional columns**

| Column Name | Data Type | Description |
| --- | --- | --- |
| TAG\_DATABASE | VARCHAR | The database in which the tag is set. |
| TAG\_SCHEMA | VARCHAR | The schema in which the tag is set. |
| TAG\_ID | NUMBER | Internal/system-generated identifier for the tag. Note that for system tags this value is NULL. |
| TAG\_NAME | VARCHAR | The name of the tag. This is the `key` in the `key = 'value'` pair of the tag. |
| TAG\_VALUE | VARCHAR | The value of tag. This is the `'value'` in the `key = 'value'` pair of the tag. |
| OBJECT\_DATABASE | VARCHAR | Database name of the referenced object for database and schema objects. If the object is not a database or schema object, the value is empty. |
| OBJECT\_SCHEMA | VARCHAR | Schema name of the referenced object (for schema objects). If the referenced object is not a schema object (e.g. warehouse), this value is empty. |
| OBJECT\_ID | NUMBER | Internal identifier of the referenced object. |
| OBJECT\_NAME | VARCHAR | Name of the referenced object if the tag association is on the object. If the tag association is on a column, Snowflake returns the parent table name. |
| OBJECT\_DELETED | TIMESTAMP\_LTZ | Date and time when the associated or parent object was dropped. |
| DOMAIN | VARCHAR | Domain of the reference object (e.g. table, view) if the tag association is on the object. For columns, the domain is COLUMN if the tag association is on a column. For more information, see [supported domains](/sql-reference/functions/tag_references#label-tag-refs-function-arguments). |
| COLUMN\_ID | NUMBER | The local identifier of the reference column; not applicable if the tag association is not a column. |
| COLUMN\_NAME | VARCHAR | Name of the referenced column; not applicable if the tag association is not a column. |
| APPLY\_METHOD | VARCHAR | Specifies how the tag got assigned to the object.   - `CLASSIFIED`: The tag was automatically applied to a column that was classified as containing sensitive data. See [About tag mapping](/user-guide/classify-auto#label-classify-auto-map-tags). - `MANUAL`: Someone manually set the tag on the object using a CREATE <object> command or ALTER <object> command. See [Set a tag](/user-guide/object-tagging/work#label-object-tagging-set). - `PROPAGATED`: The tag was automatically propagated from one object to another. See [Automatic tag propagation with user-defined tags](/user-guide/object-tagging/propagation). - `NULL`: Legacy record. - `NONE`: Legacy record. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 180 minutes (3 hours).

- The view only displays objects for which the current role for the session has been granted access privileges.
- The view does not contain information about columns that have been deleted.
- The TAG\_DATABASE\_ID column is not included in this view. To obtain this value in your query result, perform a JOIN operation with the
  [TAGS view](/sql-reference/account-usage/tags).

## Examples

Return the tag references for your Snowflake account:

> Copy code
>
> ```
> select account_name, tag_name, tag_value, domain, object_id
> from snowflake.organization_usage.tag_references
> order by tag_name, domain, object_id;
> ```

Return the active objects that have tag associations in your Snowflake account. The addition of the specified WHERE clause filters the
objects that are deleted:

> Copy code
>
> ```
> select account_name, tag_name, tag_value, domain, object_id
> from snowflake.organization_usage.tag_references
> where object_deleted is null
> order by tag_name, domain, object_id;
> ```
