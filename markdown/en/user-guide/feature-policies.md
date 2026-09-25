# Feature policies

A feature policy controls which object types can be created in a given context. You can apply
a feature policy to all native apps in an account, to a specific native app, to all personal
databases in an account, to all regular databases in an account, or to a specific database.

You can block every creation of a listed object type with
`BLOCKED_OBJECT_TYPES_FOR_CREATION`, or attach a YAML policy body with
[conditional creation rules](#label-feature-policy-rules) that fire only when a SQL expression
you supply evaluates to `TRUE`. For example, a feature policy can permit tables in general but
block temporary tables, or permit tasks but block serverless (no-warehouse) tasks.

Feature policies are schema-level objects. Before creating one, create a dedicated database and
schema to store it.

For details on using feature policies with native apps, see
[Use feature policies to limit the objects an app can create](/developer-guide/native-apps/ui-consumer-feature-policies).

For details on using feature policies with personal databases, see
[Use feature policies with personal databases](/user-guide/personal-databases#label-personal-databases-feature-policies).

## Blockable object types

### Account-level objects (native apps only)

When a native app is installed with
[automated granting of privileges](/developer-guide/native-apps/requesting-auto-privs#privileges-granted-by-automated-granting-of-privileges),
the app can receive privileges that let it create account-level objects such as warehouses,
compute pools, and databases. Once granted, these privileges can’t be directly revoked by the
consumer. A feature policy lets administrators prevent apps from exercising those privileges
to create specific object types, without revoking the underlying privilege.

The following account-level object types can be blocked:

- COMPUTE\_POOLS
- DATABASES
- WAREHOUSES

Note

Account-level object types have no effect when a feature policy is bound to personal databases.
They apply only in a native app context.

### Other blockable types

The following object types can be blocked in any context to which the policy is attached,
whether that is native apps or personal databases:

- AGENTS
- APPLICATION\_SERVICE
- ARTIFACT\_REPOSITORY
- GIT\_REPOSITORY
- MCP\_SERVERS
- SCHEMA
- SECRET
- TASKS
- WORKSPACE

For the broader set of object types that [conditional creation rules](#label-feature-policy-rules)
can reference, see [Supported object types](#label-feature-policy-rules-object-types).

## Privileges required to use feature policies

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| CREATE FEATURE POLICY | SCHEMA | Required to create a feature policy. This privilege must be granted on the schema containing the feature policy. |
| APPLY FEATURE POLICY | ACCOUNT |  |
| APPLY or OWNERSHIP | FEATURE POLICY |  |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Create a feature policy

Use the [CREATE FEATURE POLICY](/sql-reference/sql/create-feature-policy) command to create a
feature policy. The following example creates a policy that blocks task creation:

Copy code

```
CREATE DATABASE feature_policy_db;
CREATE SCHEMA sch;
CREATE FEATURE POLICY feature_policy_db.sch.block_create_task_policy
  BLOCKED_OBJECT_TYPES_FOR_CREATION = (TASKS);
```

Note

Feature policies must be created within a schema.

You can also create a policy that doesn’t restrict any object types. This is useful for
overriding a more general account-level policy on a specific app:

Copy code

```
CREATE FEATURE POLICY feature_policy_db.sch.block_nothing_policy
  BLOCKED_OBJECT_TYPES_FOR_CREATION = ();
```

To create a policy with conditional creation rules, see
[Feature policy rules](#label-feature-policy-rules).

## Apply a feature policy

### To all native apps

To apply a feature policy to all native apps in the account, use the
[ALTER ACCOUNT](/sql-reference/sql/alter-account) command:

Copy code

```
ALTER ACCOUNT
  SET FEATURE POLICY feature_policy_db.sch.block_create_task_policy
  FOR ALL APPLICATIONS;
```

To replace an existing account-level policy without unsetting it first, use `FORCE`:

Copy code

```
ALTER ACCOUNT
  SET FEATURE POLICY feature_policy_db.sch.new_policy
  FOR ALL APPLICATIONS
  FORCE;
```

To unapply the policy from all native apps:

Copy code

```
ALTER ACCOUNT UNSET FEATURE POLICY FOR ALL APPLICATIONS;
```

### To a specific application

To apply a feature policy when installing an application, use the `WITH FEATURE POLICY` clause of
the [CREATE APPLICATION](/sql-reference/sql/create-application) command:

Copy code

```
CREATE APPLICATION hello_snowflake_app
  WITH FEATURE POLICY = feature_policy_db.sch.block_create_db_policy;
```

To apply a feature policy to an existing application, use the
[ALTER APPLICATION](/sql-reference/sql/alter-application) command:

Copy code

```
ALTER APPLICATION hello_snowflake_app
  SET FEATURE POLICY feature_policy_db.sch.block_create_db_policy;
```

To unapply the policy from a specific application:

Copy code

```
ALTER APPLICATION hello_snowflake_app UNSET FEATURE POLICY;
```

A per-application policy overrides the account-level `FOR ALL APPLICATIONS` policy for that
application. See [Feature policy precedence](#label-feature-policy-precedence) for details.

### To all databases

To apply a feature policy to all regular databases in the account, use the
[ALTER ACCOUNT](/sql-reference/sql/alter-account) command with `FOR ALL DATABASES`:

Copy code

```
ALTER ACCOUNT
  SET FEATURE POLICY feature_policy_db.sch.block_create_task_policy
  FOR ALL DATABASES;
```

This policy also applies to personal databases as a fallback when no `FOR ALL PERSONAL DATABASES`
policy is set. It does not apply to native apps (application instances or application packages).

To replace an existing `FOR ALL DATABASES` policy without unsetting it first, use `FORCE`:

Copy code

```
ALTER ACCOUNT
  SET FEATURE POLICY feature_policy_db.sch.new_policy
  FOR ALL DATABASES
  FORCE;
```

To unapply the policy from all databases:

Copy code

```
ALTER ACCOUNT UNSET FEATURE POLICY FOR ALL DATABASES;
```

### To a specific database

To apply a feature policy to a specific database, use the
[ALTER DATABASE](/sql-reference/sql/alter-database) command:

Copy code

```
ALTER DATABASE my_db
  SET FEATURE POLICY feature_policy_db.sch.block_create_task_policy;
```

To replace an existing database-level policy without unsetting it first, use `FORCE`:

Copy code

```
ALTER DATABASE my_db
  SET FEATURE POLICY feature_policy_db.sch.new_policy
  FORCE;
```

To unapply the policy from the database:

Copy code

```
ALTER DATABASE my_db UNSET FEATURE POLICY;
```

A policy applied directly to a database overrides any account-level policy for that database.
See [Feature policy precedence](#label-feature-policy-precedence) for details.

### To all personal databases

To apply a feature policy to all personal databases in the account, use the
[ALTER ACCOUNT](/sql-reference/sql/alter-account) command with `FOR ALL PERSONAL DATABASES`:

Copy code

```
ALTER ACCOUNT
  SET FEATURE POLICY feature_policy_db.sch.block_app_services_policy
  FOR ALL PERSONAL DATABASES;
```

To unapply the policy from all personal databases:

Copy code

```
ALTER ACCOUNT UNSET FEATURE POLICY FOR ALL PERSONAL DATABASES;
```

Note

The `FOR ALL APPLICATIONS`, `FOR ALL PERSONAL DATABASES`, and `FOR ALL DATABASES` bindings are
independent. Setting or unsetting one has no effect on the others.

## Feature policy precedence

When an object is created, Snowflake walks the following hierarchy and enforces the first matching
policy it finds. A more specific policy always wins over a more general one.

### Regular databases

For objects created inside a regular database (not a personal database or application instance):

1. A policy applied directly to the database (`ALTER DATABASE ... SET FEATURE POLICY`)
2. The account-level `FOR ALL DATABASES` policy
3. No policy applies: the creation is allowed.

### Personal databases

For objects created inside a personal database:

1. A policy applied directly to the database (`ALTER DATABASE ... SET FEATURE POLICY`)
2. The account-level `FOR ALL PERSONAL DATABASES` policy
3. The account-level `FOR ALL DATABASES` policy (personal databases fall under this context when no
   `FOR ALL PERSONAL DATABASES` policy is set)
4. No policy applies: the creation is allowed.

### Native apps (application instances)

For objects created inside a native app:

1. A policy applied directly to the app (`ALTER APPLICATION ... SET FEATURE POLICY` or
   `CREATE APPLICATION ... WITH FEATURE POLICY`)
2. The account-level `FOR ALL APPLICATIONS` policy
3. No policy applies: the creation is allowed.

`FOR ALL DATABASES` does not apply to native apps (application instances or application packages).

### Using an empty policy to lift restrictions

A policy with no blocked object types can be applied at any specific level to explicitly allow
creation of all types, overriding a more general policy. For example, you can block a type for
all databases at the account level while exempting a specific database from that restriction:

Copy code

```
-- Block task creation for all databases.
ALTER ACCOUNT
  SET FEATURE POLICY feature_policy_db.sch.block_tasks
  FOR ALL DATABASES;

-- Exempt my_db from the restriction.
ALTER DATABASE my_db
  SET FEATURE POLICY feature_policy_db.sch.block_nothing;
```

## Feature policy rules

A feature policy can carry a YAML body that conditionally blocks the creation of
specific object types based on attributes of the request. This extends the
existing `BLOCKED_OBJECT_TYPES_FOR_CREATION` clause, which blocks every attempt
to create an object of a given type, with rules that fire only when a SQL
expression you supply evaluates to `TRUE`.

### Policy body syntax

The body is a YAML document attached to the policy with an `AS` clause:

Copy code

```
CREATE FEATURE POLICY <name>
  [ BLOCKED_OBJECT_TYPES_FOR_CREATION = ( <type> [ , ... ] ) ]
  [ COMMENT = '<string-literal>' ]
  [ AS $$
      <yaml-body>
    $$ ]
```

The YAML supports two top-level keys:

Copy code

```
conditions:
  - name: <condition-name>
    expression: "<sql-expression>"

blocked_creation_rules:
  - object_type: <OBJECT_TYPE>
    block_when: "<sql-expression>"
    # or, referencing one or more named conditions:
    block_when_any:
      - <condition-name>
```

`blocked_creation_rules`:
:   A list of rules, each scoped to a single `object_type` (for example, `TABLE`,
    `TASK`, `WAREHOUSE`) or to the `ALL` wildcard. A rule blocks creation when its
    `block_when` expression evaluates to `TRUE`, or when any of the conditions named
    in `block_when_any` evaluates to `TRUE`. If both `block_when` and
    `block_when_any` are omitted, every creation of that `object_type` is blocked
    (this isn’t allowed for `ALL`; see [Supported object types](#label-feature-policy-rules-object-types)).
    A rule can specify `block_when` or `block_when_any`, but not both.

`conditions`:
:   An optional list of named, reusable expressions that rules can reference by
    name through `block_when_any`. Use this when the same predicate appears in
    multiple rules. A rule that uses `block_when_any` requires at least one matching
    entry in `conditions`.

### Supported object types

A rule’s `object_type` can name any of the following types, in either singular
or plural form (for example, both `TABLE` and `TABLES` are accepted):

| Category | Object types |
| --- | --- |
| Account-level | `COMPUTE_POOL`, `DATABASE`, `WAREHOUSE` |
| Schema-level | `TABLE`, `ICEBERG_TABLE`, `DYNAMIC_TABLE`, `MATERIALIZED_VIEW`, `VIEW`, `STAGE`, `FILE_FORMAT`, `FUNCTION`, `PROCEDURE`, `SECRET`, `SCHEMA`, `TASK`, `AGENT`, `MCP_SERVER` |
| Personal database | `WORKSPACE`, `GIT_REPOSITORY`, `APPLICATION_SERVICE`, `ARTIFACT_REPOSITORY` |

Expand

Show lessSee more

Account-level types apply only in a native app context. Personal database types apply only
when the policy is bound to personal databases, either with `FOR ALL PERSONAL DATABASES` or
directly to a personal database. The `ALL` wildcard covers only the types applicable in the
current policy binding context.

A rule can also use the `ALL` wildcard in place of a specific `object_type` to
apply a single `block_when` or `block_when_any` to every supported type. An
`ALL` rule must carry a `block_when` or `block_when_any`: an unconditional `ALL`
rule (one that blocks every object type outright) isn’t allowed. To block every
creation of a specific type unconditionally, list that type in
`BLOCKED_OBJECT_TYPES_FOR_CREATION` instead.

### Supported object types for personal databases

Within a personal-database policy, `blocked_creation_rules` can reference the following
entity types:

| Category | Object types |
| --- | --- |
| Account-level | *(none; account-level types have no effect in personal database context)* |
| Entity types | `WORKSPACE`, `SCHEMA`, `SECRET`, `GIT_REPOSITORY`, `APPLICATION_SERVICE`, `ARTIFACT_REPOSITORY` |

Expand

Show lessSee more

Account-level types (`COMPUTE_POOL`, `DATABASE`, `WAREHOUSE`) are ignored when a policy
is bound to personal databases. List them in `BLOCKED_OBJECT_TYPES_FOR_CREATION` or
`blocked_creation_rules` only when the policy is bound to native apps. For how Snowflake
chooses between a per-database policy and an account-level policy, see
[Feature policy precedence](#label-feature-policy-precedence).

### block\_when expressions

A `block_when` (or `conditions[].expression`) value is a SQL Boolean expression
written as a quoted string. The expression is validated when the policy is
created or altered.

#### Available context

Access attributes of the object being created using either the `$` variable shorthand or the `SYS_CONTEXT` function:

- **`$<PROPERTY>`**: a shorthand that resolves the property directly. Boolean properties (`$IS_TEMPORARY`, `$IS_TRANSIENT`) evaluate to an actual boolean, so write `"$IS_TRANSIENT"` rather than `"... = 'TRUE'"`. Using a name that isn’t a recognized property, or a property inapplicable to the rule’s `object_type`, causes a compilation error when the policy is created or altered.
- **`SYS_CONTEXT('SNOWFLAKE$REQUEST', 'GET_OBJECT_PROPERTY', '<property>')`**: the full form. Always returns a string, so Boolean comparisons require `= 'TRUE'`. A property inapplicable to the domain returns `NULL` at runtime rather than an error at create time.

| Property | $ shorthand | Type | Returns |
| --- | --- | --- | --- |
| `IS_TEMPORARY` | `$IS_TEMPORARY` | Boolean | `'TRUE'` for `CREATE TEMPORARY ...` of `TABLE`, `VIEW`, `STAGE`, `FILE_FORMAT`, `FUNCTION`, `PROCEDURE`, `SECRET`, `AGENT`; `'FALSE'` otherwise. |
| `IS_TRANSIENT` | `$IS_TRANSIENT` | Boolean | `'TRUE'` for `CREATE TRANSIENT ...` of `TABLE`, `ICEBERG_TABLE`, `DYNAMIC_TABLE`, `MATERIALIZED_VIEW`, `SCHEMA`, `DATABASE`, `APPLICATION_PACKAGE`; `'FALSE'` otherwise. |
| `WAREHOUSE` | `$WAREHOUSE` | String | For `TASK`: the warehouse named in the request, or `NULL` if none (serverless task). `NULL` for other object types. |
| `EXTERNAL_VOLUME` | `$EXTERNAL_VOLUME` | String | For `ICEBERG_TABLE`: the external volume resolved for the request (table, schema, database, or account level), or `NULL` if none. `NULL` for other object types. |
| `DATABASE` | `$DATABASE` | String | The name of the database containing the object being created. `NULL` for account-level object types. |
| `SCHEMA` | `$SCHEMA` | String | The name of the schema containing the object being created. `NULL` for account-level and database-level object types (those not contained in a schema, including `SCHEMA` itself). |

Expand

Show lessSee more

Boolean properties (`$IS_TEMPORARY`, `$IS_TRANSIENT`) always evaluate to `TRUE` or
`FALSE` for every object type, so a single rule applied across mixed object types
behaves predictably: the property is `FALSE` for types that don’t support that
creation option (for example, `$IS_TRANSIENT` is `FALSE` for `STAGE`). When accessed
with `SYS_CONTEXT`, the same properties return the strings `'TRUE'` or `'FALSE'`.

String properties return `NULL` when the rule’s `object_type` doesn’t carry
that property. A comparison against `NULL` is itself `NULL`, and a rule whose
`block_when` evaluates to `NULL` fails closed and blocks the operation (see
[NULL handling](#label-feature-policy-rules-null-handling)). Guard string-property
comparisons so they evaluate to `TRUE` or `FALSE` for every `object_type` the
rule covers. With the `$` shorthand, a string property that doesn’t apply to the
rule’s `object_type` is instead rejected as a compilation error at create time.

#### Validation rules

The following expressions are rejected at CREATE or ALTER time:

- Expressions that don’t evaluate to a Boolean type (for example, a numeric
  literal or a string literal).
- Expressions that reference tables or other database objects (for example,
  `(SELECT COUNT(*) FROM t) > 0`).
- Expressions that call functions with side effects (for example,
  `SYSTEM$RUN_QUERY_SYNC`).
- Expressions that name an unsupported `object_type` or call a function that
  doesn’t exist.
- Expressions that use `$<NAME>` where `<NAME>` is not a recognized property, or
  where the property doesn’t apply to the rule’s `object_type` (for example,
  `$WAREHOUSE` in a `TABLE` rule).

#### NULL handling

If `block_when` evaluates to `NULL` at runtime (for example, because
`SYS_CONTEXT(...) = 'TRUE'` is compared against a property the request didn’t
supply), the rule fails closed: the operation is blocked. Write expressions
that always evaluate to `TRUE` or `FALSE` for every `object_type` a rule
covers, for example by guarding a property comparison with a test that is
never `NULL`.

### Examples

The following examples assume the feature policy is attached to an account, an
application, or a database after creation. For attachment syntax, see
[Apply a feature policy](#label-feature-policy-apply).

#### Block all temporary tables

Copy code

```
-- Using the $ variable shorthand:
CREATE FEATURE POLICY block_temp_tables
  AS $$
    blocked_creation_rules:
      - object_type: TABLE
        block_when: "$IS_TEMPORARY"
  $$;

-- Equivalent using SYS_CONTEXT:
CREATE FEATURE POLICY block_temp_tables_sys_context
  AS $$
    blocked_creation_rules:
      - object_type: TABLE
        block_when: "SYS_CONTEXT('SNOWFLAKE$REQUEST', 'GET_OBJECT_PROPERTY', 'IS_TEMPORARY') = 'TRUE'"
  $$;
```

#### Block all transient tables

Transient tables don’t carry the same Time Travel and Fail-safe protections as
permanent tables. A policy that requires only permanent tables can block
creations of `CREATE TRANSIENT TABLE`:

Copy code

```
-- Using the $ variable shorthand:
CREATE FEATURE POLICY block_transient_tables
  AS $$
    blocked_creation_rules:
      - object_type: TABLE
        block_when: "$IS_TRANSIENT"
  $$;

-- Equivalent using SYS_CONTEXT:
CREATE FEATURE POLICY block_transient_tables_sys_context
  AS $$
    blocked_creation_rules:
      - object_type: TABLE
        block_when: "SYS_CONTEXT('SNOWFLAKE$REQUEST', 'GET_OBJECT_PROPERTY', 'IS_TRANSIENT') = 'TRUE'"
  $$;
```

To require permanent tables outright, block both temporary and transient
creations in the same rule:

Copy code

```
-- Using the $ variable shorthand:
CREATE FEATURE POLICY require_permanent_tables
  AS $$
    blocked_creation_rules:
      - object_type: TABLE
        block_when: "$IS_TEMPORARY OR $IS_TRANSIENT"
  $$;

-- Equivalent using SYS_CONTEXT:
CREATE FEATURE POLICY require_permanent_tables_sys_context
  AS $$
    blocked_creation_rules:
      - object_type: TABLE
        block_when: "SYS_CONTEXT('SNOWFLAKE$REQUEST', 'GET_OBJECT_PROPERTY', 'IS_TEMPORARY') = 'TRUE' OR SYS_CONTEXT('SNOWFLAKE$REQUEST', 'GET_OBJECT_PROPERTY', 'IS_TRANSIENT') = 'TRUE'"
  $$;
```

#### Block transient and temporary objects across multiple object types

A single named condition can be reused across object types, including object
types that don’t support `TRANSIENT` (such as `STAGE`, `VIEW`, `FUNCTION`,
`PROCEDURE`). For those types, `$IS_TRANSIENT` is `FALSE`, so the rule fires
only on temporary creations:

Copy code

```
CREATE FEATURE POLICY block_transient_and_temp_objects
  AS $$
    conditions:
      - name: is_transient
        expression: "$IS_TRANSIENT"
      - name: is_temporary
        expression: "$IS_TEMPORARY"
    blocked_creation_rules:
      - object_type: TABLE
        block_when_any: [is_transient, is_temporary]
      - object_type: DYNAMIC_TABLE
        block_when_any: [is_transient, is_temporary]
      - object_type: ICEBERG_TABLE
        block_when_any: [is_transient, is_temporary]
      - object_type: STAGE
        block_when_any: [is_transient, is_temporary]
      - object_type: VIEW
        block_when_any: [is_transient, is_temporary]
      - object_type: FUNCTION
        block_when_any: [is_transient, is_temporary]
      - object_type: PROCEDURE
        block_when_any: [is_transient, is_temporary]
  $$;
```

#### Block serverless tasks

Serverless tasks are tasks created without a `WAREHOUSE`. The following policy
permits warehouse-attached tasks but blocks serverless ones:

Copy code

```
CREATE FEATURE POLICY block_serverless_tasks
  AS $$
    blocked_creation_rules:
      - object_type: TASK
        block_when: "$WAREHOUSE IS NULL"
  $$;
```

#### Block a property across every object type with ALL

Use the `ALL` wildcard to apply one rule to every supported object type without
listing each one. Because Boolean properties such as `$IS_TEMPORARY` are `FALSE`
for object types that can’t be temporary, the following policy blocks every
temporary creation across all types and permits everything else:

Copy code

```
CREATE FEATURE POLICY block_temp_everywhere
  AS $$
    blocked_creation_rules:
      - object_type: ALL
        block_when: "$IS_TEMPORARY"
  $$;
```

An `ALL` rule must include a `block_when` or `block_when_any`. To block every
creation of a type unconditionally, list it in
`BLOCKED_OBJECT_TYPES_FOR_CREATION` instead.

#### Restrict object creation to a specific schema

Use the `$SCHEMA` variable to block creations outside an approved schema.
A schema-level object such as a table always carries a `SCHEMA` value, so the
comparison never evaluates to `NULL`:

Copy code

```
CREATE FEATURE POLICY tables_only_in_staging
  AS $$
    blocked_creation_rules:
      - object_type: TABLE
        block_when: "$SCHEMA <> 'STAGING'"
  $$;
```

The `$SCHEMA` variable returns the schema name as stored in the catalog (uppercase
unless the schema was created with a quoted, case-sensitive identifier). The
companion `$DATABASE` variable restricts by containing database in the same way.

#### Block every table

Omit `block_when` to block every creation of an object type, regardless of
request attributes:

Copy code

```
CREATE FEATURE POLICY block_all_tables
  AS $$
    blocked_creation_rules:
      - object_type: TABLE
  $$;
```

#### Reuse a condition across rules

Copy code

```
CREATE FEATURE POLICY block_temp_objects
  AS $$
    conditions:
      - name: is_temp
        expression: "$IS_TEMPORARY"
    blocked_creation_rules:
      - object_type: TABLE
        block_when_any:
          - is_temp
      - object_type: VIEW
        block_when_any:
          - is_temp
  $$;
```

#### Combine type-level blocks and rules

`BLOCKED_OBJECT_TYPES_FOR_CREATION` and `blocked_creation_rules` can be used
together in a single policy. Listing an object type in
`BLOCKED_OBJECT_TYPES_FOR_CREATION` blocks every creation of that type
regardless of any rule. Rules covering different object types are evaluated
independently. The following policy blocks every warehouse creation and also
blocks temporary tables:

Copy code

```
CREATE FEATURE POLICY combined_policy
  BLOCKED_OBJECT_TYPES_FOR_CREATION = (WAREHOUSES)
  AS $$
    blocked_creation_rules:
      - object_type: TABLE
        block_when: "$IS_TEMPORARY"
  $$;
```

### Modify or remove a policy body

Use [ALTER FEATURE POLICY](/sql-reference/sql/alter-feature-policy) to set, replace, or clear the
body of an existing policy.

To replace the body, use the `AS` clause, with or without other `SET` clauses:

Copy code

```
ALTER FEATURE POLICY my_policy AS $$
  blocked_creation_rules:
    - object_type: TABLE
      block_when: "true"
$$;

ALTER FEATURE POLICY my_policy SET COMMENT = 'updated' AS $$
  blocked_creation_rules:
    - object_type: TABLE
      block_when: "true"
$$;
```

To remove the body but keep any `BLOCKED_OBJECT_TYPES_FOR_CREATION` clause:

Copy code

```
ALTER FEATURE POLICY my_policy UNSET POLICY_DEFINITION;
```

To inspect the current body, use
[DESCRIBE FEATURE POLICY](/sql-reference/sql/desc-feature-policy). The body appears as the
`policy_definition` property in the result.

## Delete a feature policy

Use the [DROP FEATURE POLICY](/sql-reference/sql/drop-feature-policy) command:

Copy code

```
DROP FEATURE POLICY feature_policy_db.sch.block_create_task_policy;
```

A feature policy can’t be dropped if it’s currently applied to an object. Unapply it first using
[ALTER ACCOUNT](/sql-reference/sql/alter-account), [ALTER APPLICATION](/sql-reference/sql/alter-application),
or [ALTER DATABASE](/sql-reference/sql/alter-database), then drop it.

## View feature policies

To list the feature policies in the account that you have access to:

Copy code

```
SHOW FEATURE POLICIES ON ACCOUNT;
```

To list the feature policies applied to a specific application:

Copy code

```
SHOW FEATURE POLICIES ON APPLICATION hello_snowflake_app;
```

To list the feature policies applied to a specific database:

Copy code

```
SHOW FEATURE POLICIES ON DATABASE my_db;
```

To view the details of a specific feature policy:

Copy code

```
DESCRIBE FEATURE POLICY feature_policy_db.sch.block_create_task_policy;
```

## Identify feature policy references

The [POLICY\_REFERENCES](/sql-reference/functions/policy_references) Information Schema table function can identify feature policy references. There
are two different syntax options:

1. Return a row for each object that has the specified feature policy assigned to it:

   Copy code

   ```
   USE DATABASE my_db;
   USE SCHEMA information_schema;
   SELECT policy_name,
       policy_kind,
       ref_entity_name,
       ref_entity_domain,
       policy_status
   FROM TABLE(information_schema.policy_references(policy_name => 'feature_policy_db.sch.block_create_task_policy'));
   ```
2. Return each feature policy assigned to the account:

   Copy code

   ```
   USE DATABASE my_db;
   USE SCHEMA information_schema;
   SELECT policy_name,
       policy_kind,
       ref_entity_name,
       ref_entity_domain,
       policy_status
   FROM TABLE(information_schema.policy_references(ref_entity_name => 'my_account', ref_entity_domain => 'account'));
   ```

## Replication considerations

Feature policy references at the account level are replicated when the database containing the
policy is included in the replication group, for example by setting
`ALLOWED_DATABASES = feature_policy_db`.

If the account has already been replicated to a target account, do the following:

1. Update the replication or failover group in the source account to include the databases and
   object types required to replicate the feature policy.
2. Execute a refresh operation to update the target account.

Note

The feature policy must be in the same account as the account-level policy assignment.

If you don’t include the policy database in the replication group, Snowflake creates a dangling
reference in the target account. The fully qualified policy name points to the source account’s
database, which doesn’t exist in the target account, so the policy isn’t enforced there.

For more information, see [Replication considerations](/user-guide/account-replication-considerations).
