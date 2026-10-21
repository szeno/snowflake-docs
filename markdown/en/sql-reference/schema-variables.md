# Schema variables

Schema variables are named, typed, persistent scalar values scoped to a schema. Unlike
[session variables](/sql-reference/session-variables), schema variables outlive sessions,
require no running warehouse to read or write, and are visible to all users whose roles have the
appropriate privileges on the schema.

A schema variable is a first-class catalog object. It has an owner, supports Time Travel
(UNDROP), appears in `INFORMATION_SCHEMA.VARIABLES` and `SHOW SCHEMA VARIABLES IN SCHEMA`,
and participates in Snowflake’s standard privilege model.

## When to use schema variables

| Use case | Example |
| --- | --- |
| Shared configuration | A `tax_rate` or `api_version` referenced by multiple stored procedures and views, without each session setting the value manually |
| Environment tagging | `$environment = 'production'` at the schema level; all procedures read it for conditional logic |
| ETL pipeline state | A cursor position or rate-limiting counter that one session writes and another reads across concurrent runs |
| Parameterized objects | A filter threshold or tenant ID referenced inside a view or masking policy, changeable by an admin without redefining the object |

Expand

Show lessSee more

## Creating and managing schema variables

### Create a variable

Use [CREATE VARIABLE](/sql-reference/sql/create-variable) to define a schema variable with a
declared type and an optional default:

Copy code

```
CREATE VARIABLE myschema.tax_rate FLOAT DEFAULT 0.08;
```

### Modify metadata

Use [ALTER VARIABLE](/sql-reference/sql/alter-variable) to update the default, rename, or
add a comment:

Copy code

```
ALTER VARIABLE myschema.tax_rate SET DEFAULT 0.10;
ALTER VARIABLE myschema.tax_rate SET COMMENT = 'Regional tax rate, updated annually';
ALTER VARIABLE myschema.old_name RENAME TO myschema.new_name;
```

### Drop and restore

Copy code

```
DROP VARIABLE myschema.tax_rate;

-- Restore within the Time Travel retention period:
UNDROP VARIABLE myschema.tax_rate;
```

## Reading and writing values

### Write a value

Use `SET` with a qualified name (schema-qualified or database-and-schema-qualified) to write
to a schema variable:

Copy code

```
SET myschema.tax_rate = 0.095;
SET mydb.myschema.tax_rate = 0.095;
```

To reset the variable to its declared default:

Copy code

```
SET myschema.tax_rate = DEFAULT;
```

Unqualified `SET name = value` always targets a **session variable**, never a schema variable.
This is intentional: a session variable created with `SET name = value` shadows the schema
variable of the same name for the duration of the session.

### Read a value

Use the `$` prefix to reference a schema variable in any expression where a literal constant
is allowed:

Copy code

```
SELECT price * (1 + $tax_rate) FROM orders;
```

Use a qualified name to reference the schema variable directly, bypassing any session shadow:

Copy code

```
SELECT $myschema.tax_rate;
SELECT $mydb.myschema.tax_rate;
```

### Resolution order for unqualified `$name`

When you write `$name` without qualification, Snowflake resolves it in this order:

1. **Session variable**: If a session variable named `name` exists for the current session,
   it takes precedence.
2. **Schema variable**: If no session variable exists, Snowflake looks for a schema variable
   named `name` in the current schema.
3. **Error**: If neither exists, a “variable does not exist” error is raised.

This mirrors how temporary tables shadow permanent tables. A session variable acts as a
per-session override. To remove the override and expose the schema variable again, use:

Copy code

```
UNSET name;
```

A qualified `$schema.name` reference always resolves to the schema variable, with no session
fallback.

## Access control

| Privilege | Granted on | Effect |
| --- | --- | --- |
| `CREATE VARIABLE` | Schema | Allows `CREATE VARIABLE` in that schema |
| `OWNERSHIP` | Variable | Full control: ALTER, DROP, DESCRIBE. Granted automatically to the creating role. |
| `READ` | Variable | Allows reading the value through `$name` or `$schema.name` |
| `WRITE` | Variable | Allows writing through `SET schema.name = value` |

Expand

Show lessSee more

`WRITE` does not imply `READ`. This enables write-only grants for audit logs, counters, and
append-style patterns.

Grant and revoke privileges using the standard GRANT and REVOKE commands:

Copy code

```
GRANT CREATE VARIABLE ON SCHEMA mydb.myschema TO ROLE sysadmin;
GRANT READ ON VARIABLE myschema.tax_rate TO ROLE analyst_role;
GRANT WRITE ON VARIABLE myschema.tax_rate TO ROLE etl_role;
```

## Performance

Reads and writes to schema variables are metadata-path operations, so no warehouse is
required. Read latency is sub-millisecond, the same as session variables.

Each `SET` increments a monotonic version number on the variable. Any query plan that
references the variable is recompiled on the next execution after a write.

## Constraints and limitations

| Constraint | Detail |
| --- | --- |
| Value size | Maximum 256 bytes |
| Concurrent writes | Last-writer-wins; no conflict detection |
| View bodies | Use a qualified reference (`$schema.name` or `$database.schema.name`); unqualified `$name` references aren’t supported |
| Cross-share access | Account-local only; not accessible across data sharing |
| Replication | Schema variables aren’t replicated across regions |
| Scope | Schema-level only; database-level and account-level variables aren’t supported |

Expand

Show lessSee more

## Discover schema variables

List all variables in a schema:

Copy code

```
SHOW SCHEMA VARIABLES IN SCHEMA myschema;
```

Describe a specific variable:

Copy code

```
DESCRIBE VARIABLE myschema.tax_rate;
```

Query the Information Schema:

Copy code

```
SELECT variable_name, data_type, value, default_value
  FROM mydb.information_schema.variables
  WHERE variable_schema = 'MYSCHEMA';
```

## Related topics

- [CREATE VARIABLE](/sql-reference/sql/create-variable)
- [ALTER VARIABLE](/sql-reference/sql/alter-variable)
- [DROP VARIABLE](/sql-reference/sql/drop-variable)
- [UNDROP VARIABLE](/sql-reference/sql/undrop-variable)
- [SHOW SCHEMA VARIABLES IN SCHEMA](/sql-reference/sql/show-schema-variables)
- [DESCRIBE VARIABLE](/sql-reference/sql/desc-variable)
- [VARIABLES view (Information Schema)](/sql-reference/info-schema/variables)
- [SQL variables (session variables)](/sql-reference/session-variables)
