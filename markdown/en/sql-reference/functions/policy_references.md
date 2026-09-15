Categories:
:   [Information Schema](/sql-reference/info-schema#label-info-schema-functions) , [Table functions](/sql-reference/functions-table)

# POLICY\_REFERENCES

Returns a row for each object that has the specified policy assigned to the object or returns a row for each policy assigned to the
specified object.

See also: [POLICY\_REFERENCES view](/sql-reference/account-usage/policy_references) (Account Usage View)

## Syntax

For network policy objects only:

> Copy code
>
> ```
> POLICY_REFERENCES(
>       POLICY_NAME => '<string>' ,
>       POLICY_KIND => 'NETWORK_POLICY'
>       )
> ```

For other policy objects:

> Copy code
>
> ```
> POLICY_REFERENCES(
>       POLICY_NAME => '<string>'
>       )
> ```

For all policy objects:

> Copy code
>
> ```
> POLICY_REFERENCES(
>     REF_ENTITY_NAME => '<string>' ,
>     REF_ENTITY_DOMAIN => '<string>'
>     )
> ```

## Arguments

`POLICY_NAME => 'string'`
:   Specifies the policy name.

    - The entire policy name must be enclosed in single quotes.
    - If the policy name is case-sensitive or includes any special characters or spaces, double quotes are required to process the
      case/characters. The double quotes must be enclosed within the single quotes (i.e. `'"<policy_name>"'`).

    Currently, Snowflake supports the following policies when specifying the policy name as an argument:

    - [aggregation policies](/user-guide/aggregation-policies)
    - [authentication policy](/user-guide/authentication-policies)
    - [feature policy](/user-guide/feature-policies)
    - [masking policy](/user-guide/security-column-intro)
    - [network policy](/user-guide/network-policies)
    - [packages policy](/developer-guide/udf/python/packages-policy)
    - [password policy](/user-guide/password-authentication#label-password-policies)
    - [projection policies](/user-guide/projection-policies)
    - [row access policy](/user-guide/security-row-intro)
    - [session policy](/user-guide/session-policies)
    - [storage lifecycle policies](/user-guide/storage-management/storage-lifecycle-policies)

`POLICY_KIND => 'NETWORK_POLICY'`
:   Use this argument only when the `POLICY_NAME` value is a network policy. Do not use this argument when you specify the name of
    other kinds of policies.

`REF_ENTITY_NAME => 'string'`
:   The name of the object, such as the table name, view name, external table name, or username, on which the policy is set.

    - The entire object name must be enclosed in single quotes.
    - If the object name is case-sensitive or includes any special characters or spaces, double quotes are required to process the
      case/characters. The double quotes must be enclosed within the single quotes (i.e. `'"<table_name>"'`).

`REF_ENTITY_DOMAIN => 'string'`
:   The object type on which the policy is set.

    If the object is an external table, use `'TABLE'` as the argument value.

    If the object is a materialized view, use `'VIEW'` as the argument value.

    The supported domains are:

    - `'ACCOUNT'`
    - `'INTEGRATION'`
    - `'TABLE'`
    - `'TAG'`
    - `'USER'`
    - `'VIEW'`

## Returns

The function returns the following columns:

| Column | Data Type | Description |
| --- | --- | --- |
| POLICY\_DB | VARCHAR | The database in which the policy is set. |
| POLICY\_SCHEMA | VARCHAR | The schema in which the policy is set. |
| POLICY\_NAME | VARCHAR | The name of the policy. |
| POLICY\_KIND | VARCHAR(17) | The type of policy in Snowflake. |
| REF\_DATABASE\_NAME | VARCHAR | The name of the database containing an object that the queried object references. |
| REF\_SCHEMA\_NAME | VARCHAR | The name of the schema containing an object that the queried object references. |
| REF\_ENTITY\_NAME | VARCHAR | The name of the object (i.e. table\_name, view\_name, external\_table\_name) on which the policy is set. |
| REF\_ENTITY\_DOMAIN | VARCHAR | The object type (i.e. table, view) on which the policy is set. |
| REF\_COLUMN\_NAME | VARCHAR | The column name on which the policy is set. |
| REF\_ARG\_COLUMN\_NAMES | VARCHAR | Returns NULL for rows in the query result in which a masking policy is set. |
| TAG\_DATABASE | VARCHAR | The name of the database containing the tag that has a policy assigned to the tag or NULL if a policy is not assigned to the tag. |
| TAG\_SCHEMA | VARCHAR | The name of the schema containing the tag that has a policy assigned to the tag or NULL if a policy is not assigned to the tag. |
| TAG\_NAME | VARCHAR | The name of the tag that has a policy assigned to it or NULL if a policy is not assigned to the tag. |
| POLICY\_STATUS | VARCHAR | Specifies the status of the policy, which can be one of four possible values: `ACTIVE`, `MULTIPLE_MASKING_POLICY_ASSIGNED_TO_THE_COLUMN`, `COLUMN_IS_MISSING_FOR_SECONDARY_ARG`, or `COLUMN_DATATYPE_MISMATCH_FOR_SECONDARY_ARG`. |

Expand

Show lessSee more

Note the following for the POLICY\_STATUS column:

> `ACTIVE`
> :   Specifies that the column (i.e. REF\_COLUMN\_NAME) is only associated with a single policy.
>
> `MULTIPLE_MASKING_POLICY_ASSIGNED_TO_THE_COLUMN`
> :   Specifies that multiple masking policies are assigned to the same column.
>
> `COLUMN_IS_MISSING_FOR_SECONDARY_ARG`
> :   Specifies that the policy (i.e. POLICY\_NAME) is a conditional masking policy and the table (i.e. REF\_ENTITY\_NAME) does not have a
>     column with the same name.
>
> `COLUMN_DATATYPE_MISMATCH_FOR_SECONDARY_ARG`
> :   Specifies that the policy is a conditional masking policy and the table has a column with the same name but a different data type than
>     the data type in the masking policy signature.

## Usage notes

- Results are returned based on the privileges granted to the role executing the query:

  - If the role has the global APPLY MASKING POLICY privilege, Snowflake returns all masking policy associations in the query result.
  - If the role has the global APPLY ROW ACCESS POLICY privilege, Snowflake returns all row access policy associations in the query result.
  - If the role has the APPLY privilege on a given policy (e.g. APPLY on MASKING POLICY), Snowflake returns associations of that policy
    only for objects that are owned by the role executing the query.
  - If the role has the APPLY or OWNERSHIP privilege on the policy, but not OWNERSHIP on the table or view, Snowflake does not show policy
    associations in the query result. Having the SELECT privilege on the table or view is not enough.
  - If the role does not have any policy permissions but has the OWNERSHIP privilege on the table, Snowflake returns an error message and
    does not show policy associations.
- When calling an Information Schema table function, the session must have an INFORMATION\_SCHEMA schema in use or the function must
  use the fully-qualified object name. For more details, see [Snowflake Information Schema](/sql-reference/info-schema).
- Choose one syntax variation to execute a query. Mixing arguments results in errors and query failure.

  The arguments `ref_entity_name` and `ref_entity_domain` must be included together otherwise the query fails.
- Snowflake returns errors if the specified object name does not exist or if the query operator is not authorized to view any policy on the
  object. Snowflake can return a result set of policy associations if the operator is allowed to view a subset of the policy
  associations. Unsupported object types listed as the `ref_entity_domain` (e.g. `'stream'`) also return errors.
- Snowflake does not return a result set if the query operator does not have either the APPLY or OWNERSHIP privileges on the policy.

## Examples

Return a row for each object, such as a table or view, that has the masking policy named `ssn_mask` set on column:

> Copy code
>
> ```
> use database my_db;
> use schema information_schema;
> select *
>   from table(information_schema.policy_references(policy_name => 'my_db.my_schema.ssn_mask'));
> ```

Return a row for each policy assigned to the table named `my_table`:

> Copy code
>
> ```
> use database my_db;
> use schema information_schema;
> select *
>   from table(information_schema.policy_references(ref_entity_name => 'my_db.my_schema.my_table', ref_entity_domain => 'table'));
> ```
