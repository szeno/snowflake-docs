# ALTER MASKING POLICY

[Enterprise Edition Feature](/user-guide/intro-editions)

This feature requires Enterprise Edition (or higher). To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Replaces the existing masking policy rules with new rules or a new comment and allows the renaming of a masking policy.

Any changes made to the policy rules go into effect when the next SQL query that uses the masking policy runs.

See also:
:   [Masking policy DDL](/user-guide/security-column-intro#label-security-column-intro-ddl)

## Syntax

Copy code

```
ALTER MASKING POLICY [ IF EXISTS ] <name> RENAME TO <new_name>

ALTER MASKING POLICY [ IF EXISTS ] <name> SET BODY -> <expression_on_arg_name_to_mask>

ALTER MASKING POLICY [ IF EXISTS ] <name> SET TAG <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' ... ]

ALTER MASKING POLICY [ IF EXISTS ] <name> UNSET TAG <tag_name> [ , <tag_name> ... ]

ALTER MASKING POLICY [ IF EXISTS ] <name> SET COMMENT = '<string_literal>'

ALTER MASKING POLICY [ IF EXISTS ] <name> UNSET COMMENT
```

## Parameters

`name`
:   Identifier for the masking policy; must be unique in the parent schema of the policy.

    The identifier value must start with an alphabetic character and cannot contain spaces or special characters unless the entire identifier
    string is enclosed in double quotes (e.g. `"My object"`). Identifiers enclosed in double quotes are also case-sensitive.

    For more details, see [Identifier requirements](/sql-reference/identifiers-syntax).

`RENAME TO new_name`
:   Specifies the new identifier for the masking policy; must be unique for your schema. The new identifier cannot be used if the identifier
    is already in place for a different masking policy.

    For more details, see [Identifier requirements](/sql-reference/identifiers-syntax).

    You can move the object to a different database and/or schema while optionally renaming the object. To do so, specify
    a qualified `new_name` value that includes the new database and/or schema name in the form
    `db_name.schema_name.object_name` or `schema_name.object_name`, respectively.

    Note

    - The destination database and/or schema must already exist. In addition, an object with the same name cannot already
      exist in the new location; otherwise, the statement returns an error.
    - Moving an object to a managed access schema is prohibited unless the object owner (that is, the role that has
      the OWNERSHIP privilege on the object) also owns the target schema.

`SET ...`
:   Specifies one (or more) properties to set for the masking policy:

    `BODY -> expression_on_arg_name_to_mask`
    :   SQL expression that transforms the data in the column designated by `arg_name_mask`.

        The expression can include [Conditional expression functions](/sql-reference/expressions-conditional) to represent conditional logic, built-in functions, or UDFs to
        transform the data.

        If a UDF or external function is used inside the masking policy body, the policy owner must have the USAGE privilege on the UDF or
        external function. Users querying a column that has a masking policy applied to it do not need to have USAGE on the UDF or external
        function.

        If a UDF or external function is used inside the conditional masking policy body, the policy owner must have the OWNERSHIP privilege on
        the UDF or external function. Users querying a column that has a conditional masking policy applied to it do not need to have USAGE on
        the UDF or external function.

    `TAG tag_name = 'tag_value' [ , tag_name = 'tag_value' , ... ]`
    :   Specifies the [tag](/user-guide/object-tagging/introduction) name and the tag string value.

        The tag value is always a string, and the maximum number of characters for the tag value is 256.

        For information about specifying tags in a statement, see [Tag quotas](/user-guide/object-tagging/introduction#label-object-tagging-quota).

    `COMMENT = 'string_literal'`
    :   Adds a comment or overwrites the existing comment for the masking policy.

        Default: No value

`UNSET ...`
:   Specifies one or more properties and/or parameters to unset for the masking policy, which resets them to the defaults:

    - `TAG tag_name [ , tag_name ... ]`
    - `COMMENT`

    When resetting a property/parameter, specify only the name; specifying a value for the property will return an error.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP | Masking policy | OWNERSHIP is a special privilege on an object that is automatically granted to the role that created the object, but can also be transferred using the [GRANT OWNERSHIP](/sql-reference/sql/grant-ownership) command to a different role by the owning role (or any role with the MANAGE GRANTS privilege). |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

For additional details on masking policy DDL and privileges, see [Managing Column-level Security](/user-guide/security-column-intro#label-security-column-manage).

## Usage notes

- If you want to update an existing masking policy and need to see the current definition of the policy, call the
  [GET\_DDL](/sql-reference/functions/get_ddl) function or run the [DESCRIBE MASKING POLICY](/sql-reference/sql/desc-masking-policy) command.
- You cannot change the policy signature (i.e. argument name or input/output data type). If you need to change the signature, execute a
  [DROP MASKING POLICY](/sql-reference/sql/drop-masking-policy) statement on the policy and create a new one.
- Before executing an ALTER statement, you can execute a [DESCRIBE MASKING POLICY](/sql-reference/sql/desc-masking-policy) statement to determine the argument name to use for
  updating the policy.
- For masking policies that include a subquery in the masking policy body, use [EXISTS](/sql-reference/operators-subquery) in the
  WHEN clause. For a representative example, see the custom entitlement table example in the Examples section in
  [CREATE MASKING POLICY](/sql-reference/sql/create-masking-policy).
- If the policy `body` contains a mapping table lookup, create a centralized mapping table and store the mapping table
  in the same database as the protected table. This is particularly important if the `body` calls the
  [IS\_DATABASE\_ROLE\_IN\_SESSION](/sql-reference/functions/is_database_role_in_session) function. For details, see the function usage notes.
- Adding a masking policy to a column fails if the column is referenced by a row access policy. For more information, see
  [ALTER ROW ACCESS POLICY](/sql-reference/sql/alter-row-access-policy).
- If using a [UDF](/developer-guide/udf/udf-overview) in a masking policy, ensure the data type of the column, UDF, and masking
  policy match. For more information, see [User-defined functions in a masking policy](/user-guide/security-column-intro#label-security-column-intro-udf-policy).
- Once you create a dynamic table, you can’t make changes to the masking policy.
- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

## Examples

The following example updates the masking policy to use a SHA-512 hash. Users without the ANALYST role see the value as a SHA-512 hash,
while users with the ANALYST role see the plain-text value.

Copy code

```
DESCRIBE MASKING POLICY email_mask;
```

```
+-----+------------+---------------+-------------------+-----------------------------------------------------------------------+
| Row | name       | signature     | return_type       | body                                                                  |
+-----+------------+---------------+-------------------+-----------------------------------------------------------------------+
| 1   | EMAIL_MASK | (VAL VARCHAR) | VARCHAR(16777216) | case when current_role() in ('ANALYST') then val else '*********' end |
+-----+------------+---------------+-------------------+-----------------------------------------------------------------------+
```

Copy code

```
ALTER MASKING POLICY email_mask SET BODY ->
  CASE
    WHEN current_role() IN ('ANALYST') THEN VAL
    ELSE sha2(val, 512)
  END;
```
