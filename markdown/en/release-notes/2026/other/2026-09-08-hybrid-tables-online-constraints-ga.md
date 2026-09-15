# Sep 08, 2026: Add and drop hybrid table constraints online (*General availability*)

With this release, you can add and drop UNIQUE and FOREIGN KEY constraints on an existing
[hybrid table](/user-guide/tables-hybrid) by using [ALTER TABLE](/sql-reference/sql/alter-table). Previously, you had to define
these constraints when you created the table, so adding a foreign key to a table that was already serving a workload
meant recreating and reloading the table.

The change is an online operation. Snowflake builds the index that backs the constraint in the background, and the table
stays available for SELECT and DML statements while the build runs:

Copy code

```
ALTER TABLE player ADD CONSTRAINT fk_player_team
  FOREIGN KEY (team_id) REFERENCES team (team_id);
```

Because the build runs in the background, the ALTER TABLE statement returns before the constraint is fully in place. Use
[SHOW INDEXES](/sql-reference/sql/show-indexes) to track the build. The `status` column reports `BUILD IN PROGRESS` while the index
is building and `ACTIVE` when the constraint is ready.

Adding a constraint also validates the rows that are already in the table. If some of them violate the new constraint,
the ALTER TABLE statement still succeeds and the background build reports a status of `BUILD VALIDATION FAILURE`. A
constraint in that state still enforces every new write. Only the rows that were already in the table remain
unvalidated. To recover, drop the constraint, correct the offending rows, and add the constraint again.

For more information, see
[Add and drop constraints on an existing hybrid table](/sql-reference/sql/create-hybrid-table#label-hybrid-table-online-constraints).
