# Using Contacts

Contacts are schema-level objects that contain details about which user or group of users can be contacted for a specific purpose. For
example, one contact named `data_stewards` might include an email distribution list while another named `support_department` might
include the URL of the department’s website.

Contacts can be associated with other objects such as databases and tables so the right person can be contacted for assistance with those
objects. For example, there might be a contact on a table that contains the users who can help gain access to the table. The purpose of the
contact is not a property of the contact, but rather the association between a contact and a specific object.
For example, the same contact might provide general support for one table while providing access approval for another.

An object can have more than one contact as long as the purpose of each contact is unique for the object. For example, a table might have
one contact that grants access to the table and another contact that provides general support for the table. When a user views the contacts
associated with an object, they see the purpose of each contact along with a communication method, so they know who to communicate with for
a specific reason and how to reach them.

Data users see these contacts when they are using the **Database Explorer** in Snowsight to navigate their databases, schemas, and
table-like objects. Snowflake features that send notifications to users can use the contact associated with an object to communicate
with the users.

## Inheriting and overriding contacts

Contacts are inherited by descendant objects. If you associate a contact with an object that is the parent of another object, the child,
grandchild, and so on inherit the contact. For example, if you associate a contact with a schema, all of the tables in the schema inherit
the contact by default.

Contact inheritance is overridden if a child object has a contact with the same purpose. For example, suppose someone associates the
following two contacts with the `ac_sch` schema, which contains the table `t1`:

| Contact | Purpose |
| --- | --- |
| `data_stewards` | Steward |
| `business_unit1` | Approver |

Expand

Show lessSee more

Now suppose someone associates the contact `finance_dept` with `t1` for the purpose of access approval. The contacts associated with
`t1` are now the following:

| Contact | Purpose |
| --- | --- |
| `data_stewards` | Steward |
| `finance_dept` | Approver |

Expand

Show lessSee more

The contact responsible for access approval on the `ac_sch` has been replaced with a contact directly associated with `t1`, but
`t1` continues to inherit the `data_stewards` contact from the schema.

All objects inherit contacts set on the account unless overridden by an association further down in the inheritance hierarchy.

## Supported objects

You can associate a contact with the following objects:

- Database
- Dynamic table
- Event table
- External table
- Iceberg table
- Materialized view
- Schema
- Table
- Task
- View

## Create a contact

When you create a contact, you specify the name of the contact and how the contact can be reached. Communication methods include the
following:

- The URL of a website.
- An email address, which can be a distribution list.
- A list of Snowflake users.

You can create a contact using Snowsight or SQL.

Tip

Creating all contacts in a dedicated schema can be helpful.

Snowsight:
:   1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
    2. In the navigation menu, select **Catalog** » **Database Explorer**.
    3. Navigate to the schema where you want to create the contact.
    4. Select **Create** » **Contact**.
    5. Specify the name of the contact.
    6. Choose a communication method, then specify the email address, users, or URL of the people who can be contacted for assistance with an
       object.
    7. Select the roles that will have the ability to associate the contact with objects. These roles are granted the APPLY privilege on the
       contact.
    8. Select **Create**.

SQL:
:   You can execute the [CREATE CONTACT](/sql-reference/sql/create-contact) command to create a new contact.

    **Examples**

    Create a contact for the support team that is reached through their website.

    Copy code

    ```
    CREATE CONTACT support_dept URL = 'http://internalsupport.example.com';
    ```

    Create a contact for the finance team that is reached via an email address, which acts as a distribution list.

    Copy code

    ```
    CREATE CONTACT finance_dept EMAIL_DISTRIBUTION_LIST = 'fd_dl@example.com';
    ```

    Create a contact for database administrators, as identified by the name of their Snowflake user objects.

    Copy code

    ```
    CREATE CONTACT db_admins USERS = ('ex_admin1', 'ex_admin2');
    ```

## Associate a contact with an object

When you associate a contact with an object, you specify the name of the contact along with the purpose of the association between the
contact and the object. When users view all of the contacts associated with an object, they’ll be able to decide who to communicate with based
on the purpose of each contact. If a Snowflake feature uses the contact to reach people, it will be able to select the right contacts based
on the purpose.

The purpose of having a contact associated with an object can be one of the following:

| Purpose | Description | SQL value |
| --- | --- | --- |
| Approver | Approves or rejects requests to access data. | `ACCESS_APPROVAL` |
| Security and compliance | Receives security and compliance updates. | `SECURITY_COMPLIANCE` |
| Data steward | Provides information about the accuracy, consistency, and reliability of data. | `STEWARD` |
| Support | Provides technical support related to a dataset. | `SUPPORT` |

Expand

Show lessSee more

You can associate a contact and define its purpose when modifying an existing object or creating a new object.

### Associate a contact with an existing object

Snowsight:
:   1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
    2. In the navigation menu, select **Catalog** » **Database Explorer**.
    3. Navigate to one of the [supported objects](#label-contacts-supported-objects).
    4. Select the **Details** tab.
    5. Find the **Assigned Contacts** section and select the **Edit** icon.
    6. Select a contact for one or more of the purposes. For example, if you select a contact from the **Approver** drop-down list, data
       users will reach out to that contact when they need access to the object.
    7. Select **Save**.

SQL:
:   The ALTER … SET CONTACT command for an existing object lets you associate a contact and specify the purpose of the contact for that
    object. The syntax to associate the contact is the same for all objects that can be associated with a contact:

    Copy code

    ```
    ALTER <object_type> <object_name>
      SET CONTACT <purpose> = <contact_name> [ , <purpose> = <contact_name> ... ]
    ```

    The `purpose` must be one of the [predefined purposes](/user-guide/contacts-using#label-contacts-associate-purposes), which describe the contact’s
    relationship to the object. When users view the contacts of an object, they use the purpose to determine which of the contacts to
    communicate with.

    **Examples**

    Associate the `finance_dept` contact with a table so users know who to communicate with when they need access to the table:

    Copy code

    ```
    ALTER TABLE t1 SET CONTACT ACCESS_APPROVAL = finance_dept;
    ```

    Associate the `security_officers` contact with the account so Snowflake features can send updates related to security and compliance:

    Copy code

    ```
    ALTER ACCOUNT SET CONTACT SECURITY_COMPLIANCE = security_officers;
    ```

    Associate the `data_stewards` contact with a schema so users know who to communicate with regarding object tagging of tables in the schema:

    Copy code

    ```
    ALTER SCHEMA sch1 SET CONTACT STEWARD = data_stewards;
    ```

    Note

    If you want to set a contact on an existing Iceberg table, external table, or dynamic table, you must use the ALTER TABLE
    command.

### Associate a contact when creating a new object

The CREATE … WITH CONTACT command lets you associate a contact with a new object. The syntax for the WITH CONTACT clause is the same for all
objects that can be associated with a contact:

Copy code

```
WITH CONTACT ( <purpose> = <contact_name> [ , <purpose> = <contact_name> ... ] )
```

The `purpose` must be one of the [predefined purposes](/user-guide/contacts-using#label-contacts-associate-purposes), which describe the contact’s
relationship to the object. When users view the contacts of an object, they use the purpose to determine which of the contacts to
communicate with.

For tables and table-like objects, the WITH CONTACT clause is specified after the column definitions.

The organization administrator can’t associate a contact when creating an account.

#### Examples

Associate the `finance_dept` contact with a new table so users know who to communicate with when they need access to the table:

Copy code

```
CREATE TABLE t1 (col1 VARCHAR, col2 INT) WITH CONTACT (ACCESS_APPROVAL = finance_dept);
```

Associate the `data_stewards` contact with a new schema so users know who to communicate with regarding object tagging of tables in the
schema and the `finance_dept` contact so users know who to communicate with when they need access:

Copy code

```
CREATE SCHEMA sch1 WITH CONTACT (STEWARD = data_stewards, ACCESS_APPROVAL = finance_dept);
```

## Detach a contact from an object

Snowsight:
:   1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
    2. In the navigation menu, select **Catalog** » **Database Explorer**.
    3. Navigate to the object.
    4. Select the **Details** tab.
    5. Find the **Assigned Contacts** section and select the **Edit** icon.
    6. Find the purpose (for example, **Approver**) that has the contact that you want to detach, and use the drop-down list to select **None**.
    7. Select **Save**.

SQL:
:   ALTER … UNSET CONTACT command lets you detach a contact from an object. The syntax to detach the contact is the same for all
    objects that can be associated with a contact:

    Copy code

    ```
    ALTER <object_type> <object_name>
      UNSET CONTACT <purpose>
    ```

    You identify the contact to detach by specifying the purpose of the association between the contact and the object, not by the contact
    name. For a list of possible purposes that can be specified to detach a contact, see
    [predefined purposes](/user-guide/contacts-using#label-contacts-associate-purposes).

    For example, to detach the contact that was added as the STEWARD of a table, run:

    > Copy code
    >
    > ```
    > ALTER TABLE t1 UNSET CONTACT STEWARD;
    > ```

    Note

    If you want to unset a contact on an existing Iceberg table, external table, or dynamic table, you must use the ALTER TABLE
    command.

## View contacts for an object

Snowsight:
:   When you navigate to an object in Snowsight, the contacts that are associated with the object appear on the **Details** tab.

SQL:
:   Users with at least one privilege on an object can use the [GET\_CONTACTS](/sql-reference/functions/get_contacts) table function to view the
    contacts associated with that object. The function returns a row for each contact associated with the object.

    For example, to list the contacts on the table `t1`, a user with at least one privilege can execute the following:

    Copy code

    ```
    SELECT *
      FROM TABLE(SNOWFLAKE.CORE.GET_CONTACTS('t1', 'TABLE'));
    ```

    For each contact, the function lists the following:

    - Purpose of the contact.
    - Method of communication for the contact.
    - Whether the contact was associated with the object directly or inherited from a parent object.

## Governing contacts and their associations

Snowsight:
:   To list the contacts that have been created in a schema and drill down into the details for a specific contact:

    1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
    2. In the navigation menu, select **Catalog** » **Database Explorer**, and then select the schema.
    3. Select the **Contacts** tab.
    4. Select a contact if you want to view details about it, including the objects with which it is associated.

SQL:
:   The ACCOUNT\_USAGE schema provides the following views to help manage contacts:

    - [CONTACTS view](/sql-reference/account-usage/contacts) - Lists all contacts in the account.
    - [CONTACT\_REFERENCES view](/sql-reference/account-usage/contact_references) - Lists the objects with which a contact has been associated.

## Access control privileges

The following summarizes the privileges a user needs to work with contacts.

| Task | Required privileges |
| --- | --- |
| [Create a contact](#label-contacts-create) | Both of the following:   - CREATE CONTACT on the schema - USAGE on the schema and database |
| [Associate a contact with an object](#label-contacts-associate) | Either of the following:   - APPLY CONTACT on the account - APPLY privilege on the contact and OWNERSHIP on the object |
| [List the contacts for an object](#label-contacts-view-for-object) | Any privilege on the object. |
| [Detach a contact from an object](#label-contacts-associate) | Either of the following:   - APPLY CONTACT on the account - APPLY privilege on the contact and OWNERSHIP on the object |
| [Modify an existing contact](/sql-reference/sql/alter-contact) | Either of the following:   - OWNERSHIP on the contact - MODIFY on the contact |
| [Drop a contact](/sql-reference/sql/drop-contact) | OWNERSHIP on the contact |

Expand

Show lessSee more
