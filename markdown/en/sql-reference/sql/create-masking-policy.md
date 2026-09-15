# CREATE MASKING POLICY

[Enterprise Edition Feature](/user-guide/intro-editions)

This feature requires Enterprise Edition (or higher). To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Creates a new masking policy in the current/specified schema or replaces an existing masking policy.

After creating a masking policy, apply the masking policy to a column in a table using an [ALTER TABLE … ALTER COLUMN](/sql-reference/sql/alter-table-column) command or a view using
an [ALTER VIEW](/sql-reference/sql/alter-view) command.

This command supports the following variants:

- [CREATE OR ALTER MASKING POLICY](#label-create-or-alter-masking-policy-syntax): Creates a masking policy if it doesn’t exist or alters an existing masking policy.

See also:
:   [Choosing a centralized, hybrid, or decentralized approach](/user-guide/security-column-intro#label-security-column-mgmt-approach), [Advanced Column-level Security topics](/user-guide/security-column-advanced)

    [Masking policy DDL](/user-guide/security-column-intro#label-security-column-intro-ddl)

## Syntax

Copy code

```
CREATE [ OR REPLACE ] MASKING POLICY [ IF NOT EXISTS ] <name> AS
( <arg_name_to_mask> <arg_type_to_mask> [ , <arg_1> <arg_type_1> ... ] )
RETURNS <arg_type_to_mask> -> <body>
[ COMMENT = '<string_literal>' ]
[ EXEMPT_OTHER_POLICIES = { TRUE | FALSE } ]
```

## Variant syntax

### CREATE OR ALTER MASKING POLICY

Creates a new masking policy if it doesn’t already exist, or transforms an existing masking policy into the masking policy defined in the statement.
A CREATE OR ALTER MASKING POLICY statement follows the syntax rules of a CREATE MASKING POLICY statement and has the same limitations as an
[ALTER MASKING POLICY](/sql-reference/sql/alter-masking-policy) statement.

The following modifications are supported when altering a masking policy:

- Replacing the policy body expression.
- Adding, updating, or removing a COMMENT.
- Setting or unsetting EXEMPT\_OTHER\_POLICIES.

For more information, see [CREATE OR ALTER <object>](/sql-reference/sql/create-or-alter).

Copy code

```
CREATE OR ALTER MASKING POLICY <name> AS
( <arg_name_to_mask> <arg_type_to_mask> [ , <arg_1> <arg_type_1> ... ] )
RETURNS <arg_type_to_mask> -> <body>
[ COMMENT = '<string_literal>' ]
[ EXEMPT_OTHER_POLICIES = { TRUE | FALSE } ]
```

## Required parameters

`name`
:   Identifier for the masking policy; must be unique for your schema.

    The identifier value must start with an alphabetic character and cannot contain spaces or special characters unless the entire identifier
    string is enclosed in double quotes (e.g. `"My object"`). Identifiers enclosed in double quotes are also case-sensitive.

    For more details, see [Identifier requirements](/sql-reference/identifiers-syntax).

`AS ( arg_name_to_mask arg_type_to_mask [ , arg_1 arg_type_1 ... ] )`
:   The signature for the masking policy; specifies the input columns and data types to evaluate at query runtime.

    For more details, see [SQL data types reference](/sql-reference-data-types).

    `arg_name_to_mask arg_type_to_mask`
    :   The first column and its data type always indicate the column data type values to mask or tokenize in the subsequent
        policy conditions.

        Note that you can not specify a virtual column as the first column argument in a conditional masking policy.

    `[ , arg_1 arg_type_1 ... ]`
    :   Specifies the conditional columns and their data types to evaluate to determine whether the policy conditions should mask or tokenize
        the data in the first column in each row of the query result.

        If these additional columns and data types are not specified, Snowflake evaluates the policy as a normal masking policy.

`RETURNS arg_type_to_mask`
:   The return data type must match the input data type of the first column that is specified as an input column.

`body`
:   SQL expression that transforms the data in the column designated by `arg_name_to_mask`.

    The expression can include [Conditional expression functions](/sql-reference/expressions-conditional) to represent conditional logic, built-in functions, or UDFs to
    transform the data.

    If a UDF or external function is used inside the masking policy body, the policy owner must have USAGE on the UDF or external function.
    The USAGE privilege on the UDF or external function is not required for the role used to query a column that has a masking policy applied
    to it.

    If a UDF or external function is used inside the conditional masking policy body, the policy owner must have OWNERSHIP on the UDF or
    external function. Users querying a column that has a conditional masking policy applied to it do not need to have USAGE on the UDF or
    external function.

## Optional parameters

`COMMENT = 'string_literal'`
:   Adds a comment or overwrites an existing comment for the masking policy.

`EXEMPT_OTHER_POLICIES = { TRUE | FALSE }`
:   One of the following depending on the usage:

    - Specifies whether a row access policy or conditional masking policy can reference a column that is already protected by this masking
      policy.
    - Specifies whether a masking policy assigned to a virtual column overrides the masking policy that the virtual column inherits from the
      VALUE column. When working with external tables, specify this property in the masking policy that protects the VALUE column.

    `TRUE`
    :   Allows a different policy to reference the masked column or allows the masking policy set on a virtual column to override the masking
        policy the virtual column inherits from the VALUE column in an external table.

    `FALSE`
    :   Does not allow a different policy to reference the masked column or allow the masking policy set on a virtual column to override the masking policy the virtual column inherits from the VALUE column in an external table.

    Note the following:

    - The value of this property in the masking policy cannot change after setting the masking policy on a table or view. To update
      the value of this property setting, execute a CREATE OR REPLACE MASKING POLICY statement on the masking policy.
    - When the property is set to true it is included in the output of calling the [GET\_DDL](/sql-reference/functions/get_ddl) function on the
      policy.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| CREATE MASKING POLICY | Schema |  |
| OWNERSHIP | Masking Policy | Required to execute a [CREATE OR ALTER MASKING POLICY](#label-create-or-alter-masking-policy-syntax) statement for an *existing* masking policy. |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

When specifying the `EXEMPT_OTHER_POLICIES` property in a masking policy, the role that owns the masking policy
(i.e. the role with OWNERSHIP privilege on the policy) must be in the role hierarchy of the role that owns the row access
policy or the conditional masking policy.

For example, the policy administrator custom roles can form a [role hierarchy](/user-guide/security-access-control-overview#label-role-hierarchy-and-privilege-inheritance) as
follows:

> `masking_admin` » `rap_admin` » SYSADMIN
>
> `masking_admin` » `cond_masking_admin` » SYSADMIN

Where:

`masking_admin`
:   Specifies the custom role that owns the masking policy that is set on the column that will be specified in the signature of a row access
    policy or a conditional masking policy.

`rap_admin`
:   Specifies the custom role that owns the row access policy.

`cond_masking_admin`
:   Specifies the custom role that owns the conditional masking policy.

For additional details on masking policy DDL and privileges, see [Managing Column-level Security](/user-guide/security-column-intro#label-security-column-manage).

## Usage notes

- If you want to replace an existing masking policy and need to see the current definition of the policy, call the
  [GET\_DDL](/sql-reference/functions/get_ddl) function or run the [DESCRIBE MASKING POLICY](/sql-reference/sql/desc-masking-policy) command.
- For masking policies that include a subquery in the masking policy body, use [EXISTS](/sql-reference/operators-subquery) in the
  WHEN branch of the CASE function. For a representative example, refer to the custom entitlement table example in the
  [Normal Masking Policy](#label-create-masking-policy-normal) section (in this topic).
- If the policy `body` contains a mapping table lookup, create a centralized mapping table and store the mapping table
  in the same database as the protected table. This is particularly important if the `body` calls the
  [IS\_DATABASE\_ROLE\_IN\_SESSION](/sql-reference/functions/is_database_role_in_session) function. For details, see the function usage notes.
- A given table or view column can be specified in either a masking policy signature or a row access policy signature. In other words, the
  same column cannot be specified in both a masking policy signature and a row access policy signature at the same time.

  For more information, see [CREATE ROW ACCESS POLICY](/sql-reference/sql/create-row-access-policy).
- A data sharing provider cannot create a masking policy in a [reader account](/user-guide/data-sharing-reader-create).
- If using a [UDF](/developer-guide/udf/udf-overview) in a masking policy, ensure the data type of the column, UDF, and masking
  policy match. For more information, see [User-defined functions in a masking policy](/user-guide/security-column-intro#label-security-column-intro-udf-policy).
- If you specify the [CURRENT\_DATABASE](/sql-reference/functions/current_database) or [CURRENT\_SCHEMA](/sql-reference/functions/current_schema) function in the
  body of a masking or row access policy, the function returns the database or schema that contains the protected table, not the database or
  schema in use for the session.
- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

- The OR REPLACE and IF NOT EXISTS clauses are mutually exclusive. They can’t both be used in the same statement.
- CREATE OR REPLACE *<object>* statements are atomic. That is, when an object is replaced, the old object is deleted and the new object is created in a single transaction.

### CREATE OR ALTER MASKING POLICY

- All limitations of the [ALTER MASKING POLICY](/sql-reference/sql/alter-masking-policy) command apply.
- The masking policy signature (argument names and data types) can’t be changed for an existing masking policy. If you need to change the
  signature, drop the existing policy and create a new one.
- Renaming a masking policy is not supported.
- Setting or unsetting a tag is not supported.

## Example: Normal masking policy

You can use [Conditional expression functions](/sql-reference/expressions-conditional), [Context functions](/sql-reference/functions-context), and UDFs to write the SQL expression.

The following are representative examples of the policy body to show how to create masking policy conditions using different SQL
expressions, functions, and data types.

These examples mostly use the [CURRENT\_ROLE](/sql-reference/functions/current_role) context function. If role activation and role hierarchy is
necessary in the policy conditions, use [IS\_ROLE\_IN\_SESSION](/sql-reference/functions/is_role_in_session).

Full mask:

> The `analyst` custom role can see the plain-text value. Users without the `analyst` custom role see a full mask.
>
> Copy code
>
> ```
> CREATE OR REPLACE MASKING POLICY email_mask AS (val string) returns string ->
>   CASE
>     WHEN current_role() IN ('ANALYST') THEN VAL
>     ELSE '*********'
>   END;
> ```

Allow a production [account](/user-guide/admin-account-identifier) to see unmasked values and all other accounts
(e.g. development, test) to see masked values.

> Copy code
>
> ```
> case
>   when current_account() in ('<prod_account_identifier>') then val
>   else '*********'
> end;
> ```

Return NULL for unauthorized users:

> Copy code
>
> ```
> case
>   when current_role() IN ('ANALYST') then val
>   else NULL
> end;
> ```

Return a static masked value for unauthorized users:

> Copy code
>
> ```
> CASE
>   WHEN current_role() IN ('ANALYST') THEN val
>   ELSE '********'
> END;
> ```

Return a hash value using [SHA2 , SHA2\_HEX](/sql-reference/functions/sha2) for unauthorized users. Using a hashing function in a masking policy may result in collisions; therefore, exercise caution with this approach. For more information, see [Advanced Column-level Security topics](/user-guide/security-column-advanced).

> Copy code
>
> ```
> CASE
>   WHEN current_role() IN ('ANALYST') THEN val
>   ELSE sha2(val) -- return hash of the column value
> END;
> ```

Apply a partial mask or full mask:

> Copy code
>
> ```
> CASE
>   WHEN current_role() IN ('ANALYST') THEN val
>   WHEN current_role() IN ('SUPPORT') THEN regexp_replace(val,'.+\@','*****@') -- leave email domain unmasked
>   ELSE '********'
> END;
> ```

Using timestamps.

> Copy code
>
> ```
> case
>   WHEN current_role() in ('SUPPORT') THEN val
>   else date_from_parts(0001, 01, 01)::timestamp_ntz -- returns 0001-01-01 00:00:00.000
> end;
> ```
>
> Important
>
> Currently, Snowflake does not support different input and output data types in a masking policy, such as defining the masking policy to target a timestamp and return a string (e.g. `***MASKED***`); the input and output data types must match.
>
> A workaround is to cast the actual timestamp value with a fabricated timestamp value. For more information, see [DATE\_FROM\_PARTS](/sql-reference/functions/date_from_parts) and [CAST , `::`](/sql-reference/functions/cast).

Using a UDF:

> Copy code
>
> ```
> CASE
>   WHEN current_role() IN ('ANALYST') THEN val
>   ELSE mask_udf(val) -- custom masking function
> END;
> ```

On variant data:

> Copy code
>
> ```
> CASE
>    WHEN current_role() IN ('ANALYST') THEN val
>    ELSE OBJECT_INSERT(val, 'USER_IPADDRESS', '****', true)
> END;
> ```

Using a custom entitlement table. Note the use of [EXISTS](/sql-reference/operators-subquery) in the WHEN clause. Always use EXISTS when including a subquery in the masking policy body. For more information on subqueries that Snowflake supports, see [Working with Subqueries](/user-guide/querying-subqueries).

> Copy code
>
> ```
> CASE
>   WHEN EXISTS
>     (SELECT role FROM <db>.<schema>.entitlement WHERE mask_method='unmask' AND role = current_role()) THEN val
>   ELSE '********'
> END;
> ```

Detecting when an agent is active. Use [IS\_AGENT\_ACTIVATED](/sql-reference/functions/is_agent_activated) in a masking policy to identify when an AI agent is active in the current execution context and apply data governance policies accordingly. For example, you can mask sensitive column values when an agent is present in the context, even if the user’s role would otherwise allow viewing unmasked data.

> Copy code
>
> ```
> CASE
>   WHEN SYS_CONTEXT('SNOWFLAKE$CURRENT', 'IS_AGENT_ACTIVATED')::BOOLEAN = TRUE THEN '********'
>   WHEN CURRENT_ROLE() IN ('ANALYST') THEN val
>   ELSE '********'
> END;
> ```

Using [DECRYPT](/sql-reference/functions/decrypt) on previously encrypted data with either [ENCRYPT](/sql-reference/functions/encrypt) or [ENCRYPT\_RAW](/sql-reference/functions/encrypt_raw), with a passphrase on the encrypted data:

> Copy code
>
> ```
> case
>   when current_role() in ('ANALYST') then DECRYPT(val, $passphrase)
>   else val -- shows encrypted value
> end;
> ```

Using a [<JavaScript UDF](/developer-guide/udf/javascript/udf-javascript-introduction) on JSON (VARIANT):

> In this example, a JavaScript UDF masks location data in a JSON string. It is important to set the data type as VARIANT in the UDF and
> the masking policy. If the data type in the table column, UDF, and masking policy signature do not match, Snowflake returns an error
> message because it cannot resolve the SQL.
>
> Copy code
>
> ```
> -- Flatten the JSON data
>
> create or replace table <table_name> (v variant) as
> select value::variant
> from @<table_name>,
>   table(flatten(input => parse_json($1):stationLocation));
>
> -- JavaScript UDF to mask latitude, longitude, and location data
>
> CREATE OR REPLACE FUNCTION full_location_masking(v variant)
>   RETURNS variant
>   LANGUAGE JAVASCRIPT
>   AS
>   $$
>     if ("latitude" in V) {
>       V["latitude"] = "**latitudeMask**";
>     }
>     if ("longitude" in V) {
>       V["longitude"] = "**longitudeMask**";
>     }
>     if ("location" in V) {
>       V["location"] = "**locationMask**";
>     }
>
>     return V;
>   $$;
>
>   -- Grant UDF usage to ACCOUNTADMIN
>
>   grant ownership on function FULL_LOCATION_MASKING(variant) to role accountadmin;
>
>   -- Create a masking policy using JavaScript UDF
>
>   create or replace masking policy json_location_mask as (val variant) returns variant ->
>     CASE
>       WHEN current_role() IN ('ANALYST') THEN val
>       else full_location_masking(val)
>       -- else object_insert(val, 'latitude', '**locationMask**', true) -- limited to one value at a time
>     END;
> ```

Using the [GEOGRAPHY](/sql-reference/data-types-geospatial) data type:

> In this example, a masking policy uses the [TO\_GEOGRAPHY](/sql-reference/functions/to_geography) function to convert all GEOGRAPHY data in a
> column to a fixed point, the longitude and latitude for Snowflake in San Mateo, California, for users whose CURRENT\_ROLE is not
> `ANALYST`.
>
> > Copy code
> >
> > ```
> > create masking policy mask_geo_point as (val geography) returns geography ->
> >   case
> >     when current_role() IN ('ANALYST') then val
> >     else to_geography('POINT(-122.35 37.55)')
> >   end;
> > ```
>
> Set the masking policy on a column with the GEOGRAPHY data type and set the [GEOGRAPHY\_OUTPUT\_FORMAT](/sql-reference/parameters#label-geography-output-format) value for the session to
> `GeoJSON`:
>
> > Copy code
> >
> > ```
> > alter table mydb.myschema.geography modify column b set masking policy mask_geo_point;
> > alter session set geography_output_format = 'GeoJSON';
> > use role public;
> > select * from mydb.myschema.geography;
> > ```
>
> Snowflake returns the following:
>
> > Copy code
> >
> > ```
> > ---+--------------------+
> >  A |         B          |
> > ---+--------------------+
> >  1 | {                  |
> >    |   "coordinates": [ |
> >    |     -122.35,       |
> >    |     37.55          |
> >    |   ],               |
> >    |   "type": "Point"  |
> >    | }                  |
> >  2 | {                  |
> >    |   "coordinates": [ |
> >    |     -122.35,       |
> >    |     37.55          |
> >    |   ],               |
> >    |   "type": "Point"  |
> >    | }                  |
> > ---+--------------------+
> > ```
>
> The query result values in column B depend on the GEOGRAPHY\_OUTPUT\_FORMAT parameter value for the session. For example, if the parameter
> value is set to `WKT`, Snowflake returns the following:
>
> > Copy code
> >
> > ```
> > alter session set geography_output_format = 'WKT';
> > select * from mydb.myschema.geography;
> >
> > ---+----------------------+
> >  A |         B            |
> > ---+----------------------+
> >  1 | POINT(-122.35 37.55) |
> >  2 | POINT(-122.35 37.55) |
> > ---+----------------------+
> > ```

For examples using other context functions and role hierarchy, see [Advanced Column-level Security topics](/user-guide/security-column-advanced).

## Example: Conditional masking policy

The following example returns unmasked data for users whose [CURRENT\_ROLE](/sql-reference/functions/current_role) is the `admin` custom role, or
whose value in the visibility column is `Public`. All other conditions result in a fixed masked value.

> Copy code
>
> ```
> -- Conditional Masking
>
> create masking policy email_visibility as
> (email varchar, visibility string) returns varchar ->
>   case
>     when current_role() = 'ADMIN' then email
>     when visibility = 'Public' then email
>     else '***MASKED***'
>   end;
> ```

The following example returns detokenized data for users whose [CURRENT\_ROLE](/sql-reference/functions/current_role) is the `admin` custom role,
and whose value in a different column is `Public`. All other conditions result in a tokenized value.

> Copy code
>
> ```
> -- Conditional Tokenization
>
> create masking policy de_email_visibility as
>  (email varchar, visibility string) returns varchar ->
>    case
>      when current_role() = 'ADMIN' and visibility = 'Public' then de_email(email)
>      else email -- sees tokenized data
>    end;
> ```

## Example: Allow a masked column in a row access policy or conditional masking policy

Replace a masking policy that either allows viewing the email address, viewing only the email address domain, or a fixed masked value:

> Copy code
>
> ```
> create or replace masking policy governance.policies.email_mask
> as (val string) returns string ->
> case
>   when current_role() in ('ANALYST') then val
>   when current_role() in ('SUPPORT') then regexp_replace(val,'.+\@','*****@')
>   else '********'
> end
> comment = 'specify in row access policy'
> exempt_other_policies = true
> ;
> ```

This policy can now be set on a column and a row access policy or a conditional masking policy can reference the column protected by this
masking policy as needed.

### CREATE OR ALTER MASKING POLICY

Create a new masking policy or replace the body of an existing policy:

Copy code

```
CREATE OR ALTER MASKING POLICY email_mask AS (val string) RETURNS string ->
  CASE
    WHEN current_role() IN ('ANALYST') THEN val
    ELSE '*********'
  END
COMMENT = 'Mask email addresses from non-analyst roles';
```
