# CREATE ROW ACCESS POLICY

[Enterprise Edition Feature](/user-guide/intro-editions)

This feature requires Enterprise Edition (or higher). To inquire about upgrading,
please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Creates a new row access policy in the current/specified schema or replaces an existing row access policy.

After creating a row access policy, add the policy to a table using an [ALTER TABLE](/sql-reference/sql/alter-table) command or a view using an [ALTER VIEW](/sql-reference/sql/alter-view)
command.

This command supports the following variants:

- [CREATE OR ALTER ROW ACCESS POLICY](#label-create-or-alter-row-access-policy-syntax): Creates a row access policy if it doesn’t exist or alters an existing row access policy.

See also:
:   [Row access policy DDL](/user-guide/security-row-intro#label-security-row-ddl)

## Syntax

Snowflake supports the following syntax to create a row access policy.

Copy code

```
CREATE [ OR REPLACE ] ROW ACCESS POLICY [ IF NOT EXISTS ] <name> AS
( <arg_name> <arg_type> [ , ... ] ) RETURNS BOOLEAN -> <body>
[ COMMENT = '<string_literal>' ]
```

## Variant syntax

### CREATE OR ALTER ROW ACCESS POLICY

Creates a new row access policy if it doesn’t already exist, or transforms an existing row access policy into the row access policy defined in the statement.
A CREATE OR ALTER ROW ACCESS POLICY statement follows the syntax rules of a CREATE ROW ACCESS POLICY statement and has the same limitations as an
[ALTER ROW ACCESS POLICY](/sql-reference/sql/alter-row-access-policy) statement.

The following modifications are supported when altering a row access policy:

- Replacing the policy body expression.
- Adding, updating, or removing a COMMENT.

For more information, see [CREATE OR ALTER <object>](/sql-reference/sql/create-or-alter).

Copy code

```
CREATE OR ALTER ROW ACCESS POLICY <name> AS
( <arg_name> <arg_type> [ , ... ] ) RETURNS BOOLEAN -> <body>
[ COMMENT = '<string_literal>' ]
```

## Required parameters

`name`
:   Identifier for the row access policy; must be unique for your schema.

    The identifier value must start with an alphabetic character and cannot contain spaces or special characters unless the entire
    identifier string is enclosed in double quotes (for example, “My object”). Identifiers enclosed in double quotes are also case-sensitive.

    For more details, see [Identifier requirements](/sql-reference/identifiers-syntax).

`{AS ( <arg_name> <arg_type> [ , ... ] )}`
:   The signature for the row access policy.

    A signature specifies a set of attributes that must be considered to determine whether the row is accessible. The attribute values come
    from the database object (for example, a table or view) to be protected by the row access policy.

`RETURNS BOOLEAN`
:   A row access policy must evaluate to true or false. A user that queries a table protected by a row access policy sees rows in the output
    based on how the `body` is written.

`body`
:   SQL expression that operates on the argument values in the signature to determine which rows to return for a query on a table that is
    protected by a row access policy.

    The `body` can be any boolean-valued SQL expression. Snowflake supports expressions that invoke
    [User-defined functions overview](/developer-guide/udf/udf-overview), [Writing external functions](/sql-reference/external-functions), and expressions that use sub-queries.

## Optional parameters

`COMMENT = 'string_literal'`
:   Specifies a comment for the row access policy.

    Default: No value

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| CREATE ROW ACCESS POLICY | Schema |  |
| OWNERSHIP | Row Access Policy | Required to execute a [CREATE OR ALTER ROW ACCESS POLICY](#label-create-or-alter-row-access-policy-syntax) statement for an *existing* row access policy. |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

For additional details on masking policy DDL and privileges, see [Managing Column-level Security](/user-guide/security-column-intro#label-security-column-manage).

## Usage notes

- Including one or more [subqueries](/user-guide/querying-subqueries) in the policy body may cause errors. When possible, limit the
  number of subqueries, limit the number of JOIN operations, and simplify WHERE clause conditions.
- If a database object has both a row access policy and one or more [masking policies](/user-guide/security-column-intro), the row access
  policy is evaluated first.

  For more information on row access policies during query runtime, see [Understanding row access policies](/user-guide/security-row-intro).
- A given table or view column can be specified in either a masking policy signature or a row access policy signature. In other words, the
  same column cannot be specified in both a masking policy signature and a row access policy signature at the same time.

  For more information, see [CREATE MASKING POLICY](/sql-reference/sql/create-masking-policy).
- You cannot change the policy signature (that is, argument name or input/output data type) using
  CREATE OR REPLACE ROW ACCESS POLICY if the policy is attached to a table or view, or using
  [ALTER ROW ACCESS POLICY](/sql-reference/sql/alter-row-access-policy). If you need to change the signature, execute a
  [DROP ROW ACCESS POLICY](/sql-reference/sql/drop-row-access-policy) statement on the policy and create a new row access policy.
- If the policy `body` contains a mapping table lookup, create a centralized mapping table and store the mapping table
  in the same database as the protected table. This is particularly important if the `body` calls the
  [IS\_DATABASE\_ROLE\_IN\_SESSION](/sql-reference/functions/is_database_role_in_session) function. For details, see the function usage notes.
- A data sharing provider cannot create a row access policy in a [reader account](/user-guide/data-sharing-reader-create).
- If you specify the [CURRENT\_DATABASE](/sql-reference/functions/current_database) or [CURRENT\_SCHEMA](/sql-reference/functions/current_schema) function in the
  body of a masking or row access policy, the function returns the database or schema that contains the protected table, not the database or
  schema in use for the session.
- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

- The OR REPLACE and IF NOT EXISTS clauses are mutually exclusive. They can’t both be used in the same statement.
- CREATE OR REPLACE *<object>* statements are atomic. That is, when an object is replaced, the old object is deleted and the new object is created in a single transaction.

### CREATE OR ALTER ROW ACCESS POLICY

- All limitations of the [ALTER ROW ACCESS POLICY](/sql-reference/sql/alter-row-access-policy) command apply.
- The row access policy signature (argument names and data types) can’t be changed for an existing policy. If you need to change the
  signature, drop the existing policy and create a new one.
- Renaming a row access policy is not supported.
- Setting or unsetting a tag is not supported.

## Examples

These examples use the [CURRENT\_ROLE](/sql-reference/functions/current_role) context function. If role activation and role hierarchy are
necessary in the policy conditions, use [IS\_ROLE\_IN\_SESSION](/sql-reference/functions/is_role_in_session).

The following row access policy allows users whose CURRENT\_ROLE is the `it_admin` custom role to see rows that contain the
employee ID number (that is, `empl_id`) in the query result.

> Copy code
>
> ```
> create or replace row access policy rap_it as (empl_id varchar) returns boolean ->
>   case
>       when 'it_admin' = current_role() then true
>       else false
>   end
> ;
> ```

The following row access policy allows users to view rows in the query result if either of the following two conditions are true:

1. The current role is the `sales_executive_role` custom role. Call the [CURRENT\_ROLE](/sql-reference/functions/current_role) function to
   determine the current role.
2. The current role is the `sales_manager` custom role and the query specifies a `sales_region` that corresponds to the
   `salesmanagerregions` mapping table.

> Copy code
>
> ```
> use role securityadmin;
>
> create or replace row access policy rap_sales_manager_regions_1 as (sales_region varchar) returns boolean ->
>   'sales_executive_role' = current_role()
>       or exists (
>             select 1 from salesmanagerregions
>               where sales_manager = current_role()
>                 and region = sales_region
>           )
> ;
> ```
>
> Where:
>
> > `rap_sales_manager_regions_1`
> > :   The name of the row access policy.
> >
> > `as (sales_region varchar)`
> > :   The signature for the row access policy.
> >
> >     A signature specifies a set of attributes that must be considered to determine whether the row is accessible. The attribute values
> >     come from the table to be protected by the row access policy.
> >
> > `returns boolean ->`
> > :   Specifies the application of the row access policy.
> >
> >     Note that the `<expression>` of the row access policy immediately follows the right-arrow (that is, `->`).
> >
> >     The expression can be any boolean-valued SQL expression. Snowflake supports expressions that invoke UDFs, External Functions, and
> >     expressions that use subqueries.
> >
> > `'sales_executive_role' = current_role()`
> > :   The first condition of the row access policy expression that allows users with the sales\_executive\_role custom role to view data.
> >
> > `or exists (select 1 from salesmanagerregions where sales_manager = current_role() and region = sales_region)`
> > :   The second condition of the row access policy expression that uses a subquery.
> >
> >     The subquery requires the [CURRENT\_ROLE](/sql-reference/functions/current_role) to be the sales\_manager custom role with the executed query on
> >     the data to specify a region listed in the `salesmanagerregions` mapping table.

The following row access policy specifies two attributes in the policy signature:

> Copy code
>
> ```
> create or replace row access policy rap_test2 as (n number, v varchar)
>   returns boolean -> true;
> ```
>
> Where:
>
> > `rap_test2`
> > :   The name of the row access policy.
> >
> > `(n number, v varchar)`
> > :   The signature for the row access policy.
> >
> >     A signature specifies a set of attributes that must be considered to determine whether the row is accessible. The attribute values
> >     come from the table to be protected by the row access policy.
> >
> > `returns boolean -> true`
> > :   Determines the application of the row access policy.
> >
> >     The returned value determines whether the user has access to a given row on the database object to which the row access policy is
> >     added.

For additional examples, see [Use row access policies](/user-guide/security-row-using).

### CREATE OR ALTER ROW ACCESS POLICY

Create a new row access policy or replace the body of an existing policy:

Copy code

```
CREATE OR ALTER ROW ACCESS POLICY rap_it AS (empl_id varchar) RETURNS BOOLEAN ->
  CASE
    WHEN 'it_admin' = current_role() THEN true
    ELSE false
  END
COMMENT = 'Restrict row access to IT admin role';
```
