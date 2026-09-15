Categories:
:   [System functions](/sql-reference/functions-system) (System Information)

# EXPLAIN\_GRANTABLE\_PRIVILEGES

Returns a JSON string representing all grantable privileges for each object type in Snowflake.
This function provides comprehensive information about which privileges can be granted on different
object types, including the available grant types for each privilege.

See also:
:   [GRANT <privileges> … TO ROLE](/sql-reference/sql/grant-privilege) , [GRANT CALLER](/sql-reference/sql/grant-caller) ,

## Syntax

Copy code

```
EXPLAIN_GRANTABLE_PRIVILEGES(
  [ grantee => '<grantee_type>' ]
  [, object_type => '<object_type_name>' ]
  [, grant_type => '<grant_type_name>' ])
```

## Arguments

All arguments are optional and use named parameter syntax:

`grantee => 'grantee_type'`
:   Filter results by grantee type. Valid values:

    - `ROLE`
    - `APPLICATION`

    Default: `ROLE`

    The grantee type determines which privileges are available. For example, applications cannot
    have individual ownership of objects.

`object_type => 'object_type_name'`
:   Filter results to a single object type. Accepts the singular form of the object type name
    (for example, `'DATABASE'`, `'TABLE'`, `'SCHEMA'`). The text is case-insensitive.

`grant_type => 'grant_type_name'`
:   Filter results to privileges that support a specific grant type. Valid values:

    - `'INDIVIDUAL'` — Grants on individual objects. See [GRANT <privileges> … TO ROLE](/sql-reference/sql/grant-privilege).
    - `'ALL'` — Bulk grants on all current objects (for example, `GRANT ... ON ALL TABLES IN SCHEMA`).
      See [GRANT <privileges> … TO ROLE](/sql-reference/sql/grant-privilege).
    - `'FUTURE'` — Bulk grants on future objects (for example, `GRANT ... ON FUTURE TABLES IN SCHEMA`).
      See [Future grants on database or schema objects](/sql-reference/sql/grant-privilege#label-grant-privilege-schema-future-grants).
    - `'INHERITED'` — Bulk grants on both current and future objects in a container (combines `ALL` and `FUTURE`).
      See [GRANT <privileges> … TO ROLE](/sql-reference/sql/grant-privilege).
    - `'CALLER'` — [Caller grants](/developer-guide/restricted-callers-rights) on individual objects.
      See [GRANT CALLER](/sql-reference/sql/grant-caller).
    - `'INHERITED_CALLER'` — Bulk caller grants on all current and future objects in a container
      (for example, `GRANT INHERITED CALLER ... ON ALL TABLES IN SCHEMA`).
      See [GRANT CALLER](/sql-reference/sql/grant-caller).

    The text is case-insensitive.

## Returns

The function returns a VARCHAR containing a JSON array. Each element in the array is a JSON object that represents
an object type and has the following structure:

Copy code

```
{
  "parent": "<parent_object_type>",
  "singular": "<singular_name>",
  "plural": "<plural_name>",
  "privileges": {
    "<privilege_name>": ["<grant_type>", /* ... additional grant types */],
    /* ... additional privileges */
  }
}
```

**JSON Fields:**

- `parent` — The parent object type in the object hierarchy (for example, SCHEMA is the parent of TABLE).
  The string is empty for top-level objects like ACCOUNT.
- `singular` — The singular form of the object type name (for example, DATABASE). Used for individual grants.
- `plural` — The plural form of the object type name (for example, DATABASES). Used for bulk grants.
- `privileges` — A map where each key is a privilege name and each value is an array of grant type
  names indicating how that privilege can be granted.

## Usage notes

- All arguments must be constant expressions. You cannot pass column values or other non-constant expressions.
- If no arguments are provided, the function returns all grantable privileges for roles across all object types.

## Examples

The following examples call the EXPLAIN\_GRANTABLE\_PRIVILEGES function:

- [Get all grantable privileges for roles](#get-all-grantable-privileges-for-roles)
- [Get privileges for a specific object type](#get-privileges-for-a-specific-object-type)
- [Filter by grantee type](#filter-by-grantee-type)

### Get all grantable privileges for roles

Return all object types and their grantable privileges for roles:

Copy code

```
CALL EXPLAIN_GRANTABLE_PRIVILEGES();
```

### Get privileges for a specific object type

Return only the privileges for the `'DATABASE'` object type:

Copy code

```
CALL EXPLAIN_GRANTABLE_PRIVILEGES(object_type => 'DATABASE');
```

Example output:

Copy code

```
[
  {
    "parent": "ACCOUNT",
    "singular": "DATABASE",
    "plural": "DATABASES",
    "privileges": {
      "APPLYBUDGET": ["ALL", "FUTURE", "INDIVIDUAL", "INHERITED"],
      "CREATE SCHEMA": ["INDIVIDUAL"],
      "IMPORTED PRIVILEGES": ["INDIVIDUAL"],
      "MODIFY": ["ALL", "FUTURE", "INDIVIDUAL", "INHERITED"],
      "MONITOR": ["ALL", "FUTURE", "INDIVIDUAL", "INHERITED"],
      "OWNERSHIP": ["INDIVIDUAL"],
      "REFERENCE_USAGE": ["ALL", "FUTURE", "INDIVIDUAL", "INHERITED"],
      "USAGE": ["ALL", "FUTURE", "INDIVIDUAL", "INHERITED"]
    }
  }
]
```

### Filter by grantee type

Return privileges available for applications:

Copy code

```
CALL EXPLAIN_GRANTABLE_PRIVILEGES(grantee => 'APPLICATION');
```

Applications can’t have individual ownership, so `OWNERSHIP` only shows grant types
such as `'ALL'`, `'FUTURE'`, and `'INHERITED'`.
