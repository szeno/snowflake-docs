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

The following object types can be blocked in any context the policy is bound to (native
apps, regular databases, or personal databases) that supports creating that object type:

- AGENTS
- APPLICATION\_SERVICE
- ARTIFACT\_REPOSITORY
- CORTEX\_SEARCH\_SERVICES
- DYNAMIC\_TABLES
- FILE\_FORMATS
- FUNCTIONS
- GIT\_REPOSITORY
- ICEBERG\_TABLES
- MATERIALIZED\_VIEWS
- MCP\_SERVERS
- PROCEDURES
- SCHEMA
- SECRET
- STAGES
- TABLES
- TASKS
- VIEWS
- WORKSPACE

Each type is accepted in either singular or plural form (for example, both `TABLE` and
`TABLES`). [Conditional creation rules](#label-feature-policy-rules) can reference the
same object types; see [Supported object types](#label-feature-policy-rules-object-types).

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

With `blocked_creation_rules`, a feature policy can stop users from creating
objects in ways you don’t allow. Each rule applies to an object type and blocks
a `CREATE` statement only when a condition you define is true. This lets you allow
users to create objects of a type in general but block specific uses, such as a
particular creation option or a property value you don’t permit.

For example, a feature policy can:

- Block temporary or transient tables.
- Require request logging on Cortex Search Services.
- Restrict object creation to a specific schema.

To block every creation of an object type, regardless of the statement, list the
type in `BLOCKED_OBJECT_TYPES_FOR_CREATION` instead.

Attention

`blocked_creation_rules` apply only to statements that create an object,
including `CREATE OR ALTER`. They don’t prevent a later standalone `ALTER`
statement from modifying the properties of an existing object, including
properties that a rule required at creation. For example, a rule that requires
`REQUEST_LOGGING = TRUE` when a Cortex Search Service is created doesn’t stop a
user from later running
`ALTER CORTEX SEARCH SERVICE ... SET REQUEST_LOGGING = FALSE`.

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

The YAML body has the following structure:

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
    error_message: "<text>"   # optional
```

The policy body supports the following top-level keys:

- `conditions`: Optional. A list of named, reusable expressions that rules
  reference through `block_when_any`. See
  [Condition properties](#label-feature-policy-rules-condition-properties).
- `blocked_creation_rules`: Optional. A list of rules that block matching `CREATE`
  statements. See [Rule properties](#label-feature-policy-rules-rule-properties).

#### Condition properties

The `conditions` list is optional. Each condition gives a name to a SQL Boolean
expression, so you can define the expression once and reuse it across multiple
rules instead of repeating it in each rule’s `block_when`. A rule references
conditions by name in its `block_when_any` list.

Each entry in `conditions` supports these properties:

- `name`: Required. The name that rules use to reference the condition in
  `block_when_any`. Must be unique within `conditions`.
- `expression`: Required. A SQL Boolean expression. See
  [Blocking expressions](#label-feature-policy-rules-blocking-expressions).

#### Rule properties

Each entry in `blocked_creation_rules` supports these properties:

- `object_type`: Required. The object type that the rule applies to, such as
  `TABLE`, `TASK`, or `CORTEX_SEARCH_SERVICE`, or the `ALL` wildcard. Snowflake
  rejects an unsupported type when the policy is created or altered. See
  [Supported object types](#label-feature-policy-rules-object-types).
- `block_when`: Optional. A SQL Boolean expression. The rule blocks the
  statement when the expression evaluates to `TRUE`. Can’t be an empty string.
- `block_when_any`: Optional. A list of condition names. The rule blocks the
  statement when any of the named conditions evaluates to `TRUE`. Must contain
  at least one name, and each name must match an entry in `conditions`.
- `error_message`: Optional. Text that Snowflake appends to the error for a
  blocked `CREATE`. See
  [Custom error messages](#label-feature-policy-rules-error-message).

A rule can specify `block_when` or `block_when_any`, but not both. If a rule
specifies neither, it blocks every `CREATE` of its `object_type`. An `ALL` rule
must specify one of them.

An `ALL` rule applies to every supported object type, not to every object type
in Snowflake. For the list of supported types, see
[Supported object types](#label-feature-policy-rules-object-types).
The expression in an `ALL` rule can use only the following properties:

- `TYPE`
- `REQUEST_OPERATION`
- `IS_TEMPORARY`
- `IS_TRANSIENT`
- `DATABASE`
- `SCHEMA`

To use a property that applies only to specific object types, such as
`WAREHOUSE` on `TASK`, write a rule for that object type instead.

### Supported object types

A rule’s `object_type` can name any of the following types, in either singular
or plural form (for example, both `TABLE` and `TABLES` are accepted):

| Category | Object types |
| --- | --- |
| Account-level | `DATABASE` |
| Database-level | `SCHEMA` |
| Schema-level | `TABLE`, `ICEBERG_TABLE`, `DYNAMIC_TABLE`, `VIEW`, `STAGE`, `FILE_FORMAT`, `FUNCTION`, `PROCEDURE`, `SECRET`, `TASK`, `AGENT`, `CORTEX_SEARCH_SERVICE` |

Expand

Show lessSee more

Each of these types has at least one object property that a blocking expression
can test. For the properties that apply to each type, see
[Object properties](#label-feature-policy-rules-available-context). The `ALL`
wildcard covers every supported type.

To block every creation of other object types, list them in
`BLOCKED_OBJECT_TYPES_FOR_CREATION`. See [Blockable object types](#label-feature-policy-blockable-object-types).

### Blocking expressions

This section applies to both a rule’s `block_when` expression and a
condition’s `expression`. Each is a SQL Boolean expression written as a quoted
string. Snowflake validates the expression when the policy is created or
altered.

#### Object properties

A blocking expression can refer to properties of the object that the `CREATE`
statement creates, such as the values that the statement sets. It can also
refer to properties of the request itself, such as the type of object. Refer to
a property in either of the following ways:

- **`$<PROPERTY>`**: Resolves the property directly. The variable has the same
  type as the property. For example, `$IS_TRANSIENT` is a Boolean, so use it
  directly or compare it with an unquoted `TRUE` or `FALSE` (for example,
  `$IS_TRANSIENT` or `NOT $IS_TRANSIENT`). `$SCHEMA` is a string, so compare it
  with a string literal (for example, `$SCHEMA = 'STAGING'`). Using an
  unrecognized name, or a property that doesn’t apply to the rule’s
  `object_type`, is a compilation error when the policy is created or altered.
- **`SYS_CONTEXT('SNOWFLAKE$REQUEST', 'GET_OBJECT_PROPERTY', '<property>')`**:
  The full form. Always returns a string, so Boolean comparisons require
  `= 'TRUE'`. A property that doesn’t apply to the rule’s `object_type` returns
  `NULL` at runtime instead of causing an error when the policy is created.

For example, the following two rules are equivalent:

Copy code

```
blocked_creation_rules:
  - object_type: TABLE
    block_when: "$IS_TEMPORARY"
    error_message: "Temporary tables aren't allowed. Create a permanent table."
  - object_type: TABLE
    block_when: "SYS_CONTEXT('SNOWFLAKE$REQUEST', 'GET_OBJECT_PROPERTY', 'IS_TEMPORARY') = 'TRUE'"
    error_message: "Temporary tables aren't allowed. Create a permanent table."
```

The following properties describe the request itself. They apply to every
object type:

| Property | $ shorthand | Returns |
| --- | --- | --- |
| `TYPE` | `$TYPE` | The type of the object being created, using the same name as a rule’s `object_type`, for example `TABLE`, `AGENT`, or `TASK`. Useful in `ALL` rules and in shared conditions. |
| `REQUEST_OPERATION` | `$REQUEST_OPERATION` | The kind of statement being evaluated. Always `CREATE` in `blocked_creation_rules`, including for `CREATE OR ALTER`. |

Expand

Show lessSee more

The following properties describe the object being created:

| Property | $ shorthand | Type | Returns |
| --- | --- | --- | --- |
| `IS_TEMPORARY` | `$IS_TEMPORARY` | Boolean | `TRUE` for `CREATE TEMPORARY ...` of `TABLE`, `VIEW`, `STAGE`, `FILE_FORMAT`, `FUNCTION`, `PROCEDURE`, `SECRET`, `AGENT`. `FALSE` otherwise. |
| `IS_TRANSIENT` | `$IS_TRANSIENT` | Boolean | `TRUE` for `CREATE TRANSIENT ...` of `TABLE`, `ICEBERG_TABLE`, `DYNAMIC_TABLE`, `SCHEMA`, `DATABASE`. `FALSE` otherwise. |
| `REQUEST_LOGGING` | `$REQUEST_LOGGING` | Boolean | For `CORTEX_SEARCH_SERVICE`: `TRUE` when the statement sets `REQUEST_LOGGING = TRUE`. `FALSE` when it sets `FALSE` or omits the property. `FALSE` for other object types. |
| `WAREHOUSE` | `$WAREHOUSE` | String | For `TASK`: the warehouse named in the request, or `NULL` if none (serverless task). `NULL` for other object types. |
| `EXTERNAL_VOLUME` | `$EXTERNAL_VOLUME` | String | For `ICEBERG_TABLE`: the external volume resolved for the request (table, schema, database, or account level), or `NULL` if none. `NULL` for other object types. |
| `DATABASE` | `$DATABASE` | String | The name of the database containing the object being created. `NULL` for account-level object types. |
| `SCHEMA` | `$SCHEMA` | String | The name of the schema containing the object being created. `NULL` for account-level and database-level object types (those not contained in a schema, including `SCHEMA` itself). |

Expand

Show lessSee more

Boolean properties are `FALSE` for object types that don’t support that
creation option, so a single rule applied across mixed object types behaves
predictably. For example, `$IS_TRANSIENT` is `FALSE` for `STAGE`.

#### Properties on CREATE and CREATE OR ALTER

A blocking expression can read the properties that the statement explicitly
sets. It can also read properties that the statement doesn’t set but that have
a default or a resolved value for the object type. Those properties report that
value.

- Boolean properties are always present. If the statement omits one, the value
  is that property’s default. `IS_OBJECT_PROPERTY_PRESENT` returns `TRUE`.
- Other properties that have a default or a resolved value for the object type,
  such as `EXTERNAL_VOLUME` on `ICEBERG_TABLE`, are present at that value when
  the statement omits them. `IS_OBJECT_PROPERTY_PRESENT` returns `TRUE`.
- Properties without a default are `NULL` when the statement omits them or sets
  them to `NULL`. `IS_OBJECT_PROPERTY_PRESENT` returns `TRUE` only when the
  statement supplies a value.
- `TYPE`, `REQUEST_OPERATION`, `DATABASE`, and `SCHEMA` are always present when
  they apply to the object type.

#### Safely handling missing properties

A string property can be `NULL`, for example `WAREHOUSE` on a serverless task.
A comparison against `NULL` is itself `NULL`, and a rule whose expression
evaluates to `NULL` blocks the statement. For example,
`$WAREHOUSE NOT IN ('CORP_M', 'CORP_XL')` is `NULL` for a serverless task, so
the rule blocks every serverless task, even if you intended to allow them.

To write a rule that behaves predictably for every statement, use one of the
following approaches instead of comparing the property directly.

##### Using NULL checks

Test whether a property is `NULL` before comparing its value. An `IS NOT NULL`
check makes the expression `FALSE` instead of `NULL` when the property has no
value.

The following rule requires that a task’s warehouse, when set, is `CORP_M` or
`CORP_XL`. A task without a warehouse is allowed:

Copy code

```
blocked_creation_rules:
  - object_type: TASK
    block_when: "$WAREHOUSE IS NOT NULL AND $WAREHOUSE NOT IN ('CORP_M', 'CORP_XL')"
    error_message: "Tasks must use the CORP_M or CORP_XL warehouse, or run as serverless tasks."
```

The rule handles each statement as follows:

- `CREATE TASK` with `WAREHOUSE = CORP_M` or `WAREHOUSE = CORP_XL`: allowed.
- `CREATE TASK` with a different warehouse: blocked.
- `CREATE TASK` with no warehouse (a serverless task): allowed.

##### Using IS\_OBJECT\_PROPERTY\_SET\_TO

Use `IS_OBJECT_PROPERTY_SET_TO` to require that a property has a specific value
whenever a statement supplies it. The function returns `TRUE` when the
statement sets the property to the value, or when the statement doesn’t supply
the property at all. The value is compared case-insensitively, and an explicit
`NULL` doesn’t match any value. An omitted Boolean is present at its default,
so the function compares that default. The function returns `NULL` for an
unrecognized property name.

The following rule requires that a task that names a warehouse uses
`CORP_M`:

Copy code

```
blocked_creation_rules:
  - object_type: TASK
    block_when: "NOT SYS_CONTEXT('SNOWFLAKE$REQUEST', 'IS_OBJECT_PROPERTY_SET_TO', 'WAREHOUSE', 'CORP_M')"
    error_message: "Tasks must use the CORP_M warehouse, or run as serverless tasks."
```

The rule handles each statement as follows:

- `CREATE TASK` with `WAREHOUSE = CORP_M`: allowed.
- `CREATE TASK` with a different warehouse: blocked.
- `CREATE TASK` with no warehouse (a serverless task): allowed.

##### Using IS\_OBJECT\_PROPERTY\_PRESENT

Use `IS_OBJECT_PROPERTY_PRESENT` to block a statement based on whether a
property is present, regardless of its value. The function returns `TRUE` when
the property is present and `FALSE` when it isn’t. For the properties that
count as present, see
[Properties on CREATE and CREATE OR ALTER](#label-feature-policy-rules-properties-on-create).
The function returns `NULL` for an unrecognized property name.

The following rule allows only serverless tasks:

Copy code

```
blocked_creation_rules:
  - object_type: TASK
    block_when: "SYS_CONTEXT('SNOWFLAKE$REQUEST', 'IS_OBJECT_PROPERTY_PRESENT', 'WAREHOUSE')"
    error_message: "Only serverless tasks are allowed. Create the task without a WAREHOUSE."
```

The rule handles each statement as follows:

- `CREATE TASK` with any `WAREHOUSE`: blocked.
- `CREATE TASK` with no warehouse (a serverless task): allowed.

Each of these expressions evaluates to `TRUE` or `FALSE` for every statement,
so a missing property never causes it to block the statement.

#### Validation rules

Snowflake rejects the following expressions when the policy is created or
altered:

- Expressions that don’t evaluate to a Boolean type (for example, a numeric
  literal or a string literal).
- Expressions that reference tables or other database objects (for example,
  `(SELECT COUNT(*) FROM t) > 0`).
- Expressions that call functions with side effects (for example,
  `SYSTEM$RUN_QUERY_SYNC`).
- Expressions that call functions that must run in a warehouse.
- Expressions that call a function that doesn’t exist.
- Expressions that use `$<NAME>` where `<NAME>` isn’t a recognized object
  property, or where the property doesn’t apply to the rule’s `object_type`
  (for example, `$WAREHOUSE` in a `TABLE` rule).

Attention

An expression that compares a property can evaluate to `NULL` at runtime, and
a rule whose expression evaluates to `NULL` blocks the statement. Validation
doesn’t catch the following cases:

- The property has no value for the statement, for example `WAREHOUSE` on a
  serverless task.
- The expression uses `SYS_CONTEXT` to read a property that doesn’t apply to
  the rule’s `object_type`, or a misspelled property name.
- The statement explicitly sets the property to `NULL`.

To avoid these failures, check for `NULL` before comparing a property’s value.
See [Using NULL checks](#label-feature-policy-rules-null-checks).

### Custom error messages

When a rule blocks the statement, the statement is denied. By default, the
error names the object type and points to the effective feature policy, for
example:

```
Create TABLE denied due to feature policy restriction for the account. Consult your internal policy administrator to review the effective feature policy by running 'SHOW FEATURE POLICIES ON ACCOUNT'.
```

Add an `error_message` to a rule to tell the user why the statement was blocked
and what to do instead:

Copy code

```
CREATE FEATURE POLICY require_permanent_tables
  AS $$
    blocked_creation_rules:
      - object_type: TABLE
        block_when: "$IS_TEMPORARY OR $IS_TRANSIENT"
        error_message: "Temporary and transient tables aren't allowed. Create a permanent table."
  $$;
```

When this policy is applied to the account, a `CREATE TRANSIENT TABLE` statement
fails with an error that includes the rule’s text after `Your policy:`:

```
Create TABLE denied due to feature policy restriction for the account. Your policy: Temporary and transient tables aren't allowed. Create a permanent table. Consult your internal policy administrator to review the effective feature policy by running 'SHOW FEATURE POLICIES ON ACCOUNT'.
```

The following rules apply to `error_message`:

- The value is trimmed of leading and trailing whitespace. The trimmed text must be
  1 to 512 characters long.
- The value must be a single line. Newlines, tabs, and other control characters
  aren’t allowed.
- The sequence `${`, followed later by `}`, is reserved and isn’t allowed.
- Snowflake validates the value when the policy is created or altered. An invalid
  value causes the statement to fail.

Snowflake shows the message from the first rule in the list that blocks the
statement. If a statement is blocked because its object type is listed in
`BLOCKED_OBJECT_TYPES_FOR_CREATION`, Snowflake shows the generic error without any
rule’s `error_message`, even if a rule for the same object type also matches.

### Examples

The following examples assume the feature policy is attached to an account, an
application, or a database after creation. For attachment syntax, see
[Apply a feature policy](#label-feature-policy-apply).

Each example includes an `error_message`. Adding one to every rule is
recommended, so that users who are blocked understand why and know what to do
instead. For more information, see
[Custom error messages](#label-feature-policy-rules-error-message).

#### Block all temporary tables

Copy code

```
CREATE FEATURE POLICY block_temp_tables
  AS $$
    blocked_creation_rules:
      - object_type: TABLE
        block_when: "$IS_TEMPORARY"
        error_message: "Temporary tables aren't allowed. Create a permanent or transient table."
  $$;
```

#### Block all transient tables

Transient tables don’t carry the same Time Travel and Fail-safe protections as
permanent tables. A policy that requires only permanent tables can block
`CREATE TRANSIENT TABLE` statements:

Copy code

```
CREATE FEATURE POLICY block_transient_tables
  AS $$
    blocked_creation_rules:
      - object_type: TABLE
        block_when: "$IS_TRANSIENT"
        error_message: "Transient tables aren't allowed. Create a permanent table."
  $$;
```

To block both temporary and transient tables in one rule, see the example in
[Custom error messages](#label-feature-policy-rules-error-message).

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
        error_message: "Temporary and transient tables aren't allowed. Create a permanent table."
      - object_type: DYNAMIC_TABLE
        block_when_any: [is_transient, is_temporary]
        error_message: "Transient dynamic tables aren't allowed. Create a permanent dynamic table."
      - object_type: ICEBERG_TABLE
        block_when_any: [is_transient, is_temporary]
        error_message: "Transient Iceberg tables aren't allowed. Create a permanent Iceberg table."
      - object_type: STAGE
        block_when_any: [is_transient, is_temporary]
        error_message: "Temporary stages aren't allowed. Create a permanent stage."
      - object_type: VIEW
        block_when_any: [is_transient, is_temporary]
        error_message: "Temporary views aren't allowed. Create a permanent view."
      - object_type: FUNCTION
        block_when_any: [is_transient, is_temporary]
        error_message: "Temporary functions aren't allowed. Create a permanent function."
      - object_type: PROCEDURE
        block_when_any: [is_transient, is_temporary]
        error_message: "Temporary procedures aren't allowed. Create a permanent procedure."
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
        error_message: "Serverless tasks aren't allowed. Specify a WAREHOUSE when you create the task."
  $$;
```

#### Require request logging for Cortex Search Services

The following policy blocks creating a Cortex Search Service unless the statement
sets `REQUEST_LOGGING = TRUE`. Because `REQUEST_LOGGING` defaults to `FALSE`, a
statement that omits the property is also blocked. For more information about
request logging, see
[Enable request logging](/user-guide/snowflake-cortex/cortex-search/cortex-search-monitor#label-cortex-search-request-logging).

Copy code

```
CREATE FEATURE POLICY require_search_request_logging
  AS $$
    blocked_creation_rules:
      - object_type: CORTEX_SEARCH_SERVICE
        block_when: "NOT $REQUEST_LOGGING"
        error_message: "Create Cortex Search Services with REQUEST_LOGGING = TRUE."
  $$;
```

This rule applies only when a service is created. It doesn’t block an
`ALTER CORTEX SEARCH SERVICE` statement that later disables request logging.

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
        error_message: "Temporary objects aren't allowed. Create a permanent object."
  $$;
```

To exempt specific types from an `ALL` rule, test `$TYPE`. The following policy
blocks every temporary creation except temporary tables:

Copy code

```
CREATE FEATURE POLICY block_temp_except_tables
  AS $$
    blocked_creation_rules:
      - object_type: ALL
        block_when: "$IS_TEMPORARY AND $TYPE <> 'TABLE'"
        error_message: "Only temporary tables are allowed. Create other objects as permanent objects."
  $$;
```

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
        error_message: "Tables can be created only in the STAGING schema."
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
        error_message: "Creating tables isn't allowed here. Contact your administrator to request a table."
  $$;
```

Unlike listing `TABLE` in `BLOCKED_OBJECT_TYPES_FOR_CREATION`, this rule shows
its `error_message` when it blocks a statement.

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
        error_message: "Temporary tables aren't allowed. Create a permanent table."
      - object_type: VIEW
        block_when_any:
          - is_temp
        error_message: "Temporary views aren't allowed. Create a permanent view."
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
        error_message: "Temporary tables aren't allowed. Create a permanent table."
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
   FROM TABLE(policy_references(policy_name => 'feature_policy_db.sch.block_create_task_policy'));
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
   FROM TABLE(policy_references(ref_entity_name => 'my_account', ref_entity_domain => 'account'));
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
