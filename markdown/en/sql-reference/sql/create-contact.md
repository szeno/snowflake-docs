# CREATE CONTACT

Creates a new [contact](/user-guide/contacts-using) or replaces an existing contact.

See also:
:   [ALTER CONTACT](/sql-reference/sql/alter-contact) , [DROP CONTACT](/sql-reference/sql/drop-contact) , [SHOW CONTACTS](/sql-reference/sql/show-contacts)

## Syntax

Copy code

```
CREATE [ OR REPLACE ] CONTACT [ IF NOT EXISTS ] <name>
  [ {
    USERS = ( '<user_name>' [ , '<user_name>' ... ] )
    | EMAIL_DISTRIBUTION_LIST = '<email>'
    | URL = '<url>'
    } ]
  [ COMMENT = '<string_literal>' ]
```

## Required parameters

`name`
:   Specifies the name of the new contact.

    In addition, the identifier must start with an alphabetic character and cannot contain spaces or special characters unless the
    entire identifier string is enclosed in double quotes (for example, `"My object"`). Identifiers enclosed in double quotes are also
    case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

## Optional parameters

`USERS = ( 'user_name' [ , 'user_name' ... ] )`
:   Comma-delimited list of Snowflake users who can be contacted, specified by the name of their user objects.

    If the user name is case-sensitive or includes any special characters or spaces, double quotes are required. The double quotes must be
    enclosed within the single quotes. For example, if the user is `joe@example.com`, you must specify `'"joe@example.com"'`.

`EMAIL_DISTRIBUTION_LIST = 'email'`
:   A valid email address, which can be a distribution list.

`URL = 'url'`
:   A URL that can be used to contact people about an object.

`COMMENT`
:   A user-defined string. Specifies a comment for the contact.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| CREATE CONTACT | Schema |  |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).
- CREATE OR REPLACE *<object>* statements are atomic. That is, when an object is replaced, the old object is deleted and the new object is created in a single transaction.

## Examples

Copy code

```
CREATE CONTACT my_contact
  EMAIL_DISTRIBUTION_LIST = 'support@example.com';
```
