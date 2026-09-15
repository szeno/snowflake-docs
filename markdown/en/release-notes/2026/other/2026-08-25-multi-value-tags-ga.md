# Aug 25, 2026: Multi-value tags (*General availability*)

With this release, multi-value tags are generally available. You can assign more than one string value to the same tag.

Multi-value tags are useful when an object needs multiple classifications that aren’t mutually exclusive, such as more than one
data source or compliance requirement. You create a tag with `MULTI_VALUE = TRUE`, then add and remove values with
`ADD VALUE` and `DROP VALUE`. For tag propagation, `ON_CONFLICT = MERGE` is available only on multi-value tags.

To check whether a tag includes a specific value, use [SYSTEM$TAG\_VALUE\_CONTAINS](/sql-reference/functions/system_tag_value_contains).

For more information, see [Multi-value tags](/user-guide/object-tagging/multi-value-tags).
