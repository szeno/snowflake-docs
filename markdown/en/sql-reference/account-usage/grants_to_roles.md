Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# GRANTS\_TO\_ROLES view

This Account Usage view can be used to query access control privileges that have been granted to an account role, application, application
role, database role, instance role, or user.

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| CREATED\_ON | TIMESTAMP\_LTZ | Date and time (in the UTC time zone) when the privilege is granted to the role. |
| MODIFIED\_ON | TIMESTAMP\_LTZ | Date and time (in the UTC time zone) when the privilege is updated. |
| PRIVILEGE | VARCHAR | Name of the privilege added to the role. |
| GRANTED\_ON | VARCHAR | Object kind, such as `TABLE` or `DATABASE`, on which the privilege is granted. |
| NAME | VARCHAR | Name of the object on which the privilege is granted. |
| TABLE\_CATALOG | VARCHAR | Name of the database for the current table or the name of the database that stores the instance of a class. |
| TABLE\_SCHEMA | VARCHAR | Name of the schema for the current table or the name of the schema that stores the instance of a class. |
| GRANTED\_TO | VARCHAR | `ACCOUNT ROLE`, `APPLICATION`, `APPLICATION_ROLE`, `DATABASE_ROLE`, `INSTANCE_ROLE`, or `USER`. |
| GRANTEE\_NAME | VARCHAR | Identifier for the recipient role, the role to which the privilege is granted, or the name of the Snowflake Native App object. |
| GRANT\_OPTION | BOOLEAN | `TRUE / FALSE`. If set to `TRUE`, the recipient role can grant the privilege to other roles. |
| GRANTED\_BY | VARCHAR | Indicates the role that authorized a privilege grant to the grantee. `GRANTED_BY` displays empty for privileges granted by the SNOWFLAKE system role. |
| DELETED\_ON | TIMESTAMP\_LTZ | Date and time (in the UTC time zone) when the privilege is revoked. |
| GRANTED\_BY\_ROLE\_TYPE | VARCHAR | Either `APPLICATION`, `ROLE` or `DATABASE_ROLE`. |
| OBJECT\_INSTANCE | VARCHAR | The fully-qualified name of the object that contains the instance role for a particular class in the format `database.schema.class`. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 120 minutes (2 hours).

- The GRANTS\_TO\_ROLES view shows a subset of all supported objects. The supported set is subject to change. The view is updated periodically
  to include support for new objects.
- The view does not contain grants to database roles from databases created from shares.
- The view does not contain grants on dropped objects.
- The `GRANTED_BY` column indicates the role that authorized a privilege grant to the grantee. The authorization role is known as the
  *grantor*.

  When you grant privileges on an object to a role using [GRANT <privileges> … TO ROLE](/sql-reference/sql/grant-privilege), the following authorization rules
  determine which role is listed as the grantor of the privilege:

  1. If an [active role](/user-guide/security-access-control-overview#label-access-control-overview-active-roles) is the object owner (i.e. has the OWNERSHIP privilege on the
     object), that role is the grantor.
  2. If an active role was given privileges on the object by a GRANT PRIVILEGE … WITH GRANT OPTION statement, then the active role is the
     grantor. If multiple active roles meet this criterion and one of these active roles is the primary role, then the primary role is the
     grantor. If there are multiple active roles, and none of them are the primary role, Snowflake randomly selects one of the roles as the
     grantor.
  3. If an active role holds the global MANAGE GRANTS privilege, the grantor role is the object owner, not the role that held the
     MANAGE GRANTS privilege. That is, the MANAGE GRANTS privilege allows a role to impersonate the object owner for the purposes of
     granting privileges on that object.

  The `GRANTED_BY` column displays empty for privileges granted by the Snowflake SYSTEM role. Certain internal operations are
  performed with this role. Grants of privileges authorized by the SYSTEM role cannot be modified by customers.
