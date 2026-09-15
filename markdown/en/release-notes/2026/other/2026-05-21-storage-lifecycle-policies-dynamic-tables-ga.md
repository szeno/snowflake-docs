# May 21, 2026: Storage lifecycle policies for dynamic tables (*General availability*)

Attaching a storage lifecycle policy to a dynamic table is now generally available. You can attach a
storage lifecycle policy directly to a dynamic table to delete or archive rows that match a predicate, on a
schedule that runs independently of dynamic table refresh.

To attach a policy at create time, use the `WITH STORAGE LIFECYCLE POLICY <policy> ON (<column>)` clause in
[CREATE DYNAMIC TABLE](/sql-reference/sql/create-dynamic-table). To attach a policy to an existing dynamic
table, use the `ADD STORAGE LIFECYCLE POLICY <policy> ON (<column>)` clause in
[ALTER DYNAMIC TABLE](/sql-reference/sql/alter-dynamic-table). Rows that match the policy predicate form
the dynamic table’s expired region, which refresh treats as frozen. The policy runs asynchronously on its
own schedule to delete or archive those rows.

For more information, see [Use storage lifecycle policies with dynamic tables](/user-guide/dynamic-tables/storage-lifecycle-policies).
