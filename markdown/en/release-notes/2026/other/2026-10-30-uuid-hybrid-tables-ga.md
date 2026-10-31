# Oct 30, 2026: UUID data type in hybrid tables (*General availability*)

With this release, you can use the [UUID](/sql-reference/data-types-uuid) data type in
[hybrid tables](/user-guide/tables-hybrid). A UUID column can be a primary key, a foreign key, or a
secondary index.

Copy code

```
CREATE OR REPLACE HYBRID TABLE application_users (
  user_id UUID PRIMARY KEY,
  email VARCHAR
  );
```

For more information, see [UUID data type](/sql-reference/data-types-uuid).
