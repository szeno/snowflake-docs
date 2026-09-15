# July 20, 2026: DML into frozen regions of dynamic tables (*General availability*)

You can now use DML statements (INSERT, UPDATE, MERGE, DELETE) to modify rows directly in the frozen
region of a dynamic table. This enables use cases such as GDPR-required row deletions or correcting
specific records without triggering a full refresh of the active region.

For more information, see [DML into a frozen region](/user-guide/dynamic-tables/frozen-regions#label-dynamic-tables-frozen-dml).
