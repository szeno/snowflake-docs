# Nov 2, 2026: SECRET object tagging

With this release, you can assign tags to secrets when you create or alter a secret. You can use tags on secrets to track
sensitive objects, manage governance workflows, and organize secrets consistently with other tagged Snowflake objects.

This release adds support for:

- [CREATE SECRET](/sql-reference/sql/create-secret) with `WITH TAG`.
- [ALTER SECRET](/sql-reference/sql/alter-secret) with `SET TAG` and `UNSET TAG`.
- The `SECRET` object domain in [SYSTEM$GET\_TAG](/sql-reference/functions/system_get_tag), the [TAG\_REFERENCES](/sql-reference/functions/tag_references)
  Information Schema table function, [TAG\_REFERENCES view](/sql-reference/account-usage/tag_references),
  [TAG\_REFERENCES view](/sql-reference/organization-usage/tag_references), and [TAG\_REFERENCES\_WITH\_LINEAGE](/sql-reference/functions/tag_references_with_lineage).

For more information, see [Introduction to object tagging](/user-guide/object-tagging/introduction).
