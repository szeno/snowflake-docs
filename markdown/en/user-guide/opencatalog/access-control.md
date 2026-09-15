# Access control

Feature — Generally Available

Not available in government regions.

This section provides information about how access control works for Snowflake Open Catalog.

Open Catalog uses a role-based access control (RBAC) model in which the Open Catalog administrator assigns access privileges to catalog roles
and then grants access to resources to service principals by assigning catalog roles to principal roles.

These are the key concepts to understanding access control in Open Catalog:

- **Securable object**
- **Principal role**
- **Custom role**
- **Catalog role**
- **Privilege**

## Securable object

A securable object is an object to which access can be granted. Open Catalog
has the following securable objects:

- Catalog
- Namespace
- Iceberg table
- View

The RBAC model for Open Catalog is fine-grained; that is, you can grant privileges on the entire catalog or on a namespace, table, or view
within the catalog. If you’re granting privileges on a namespace, you can also secure the tables grouped under it and any
child namespaces or tables nested under it.

## Principal role

A principal role is a resource in Open Catalog that you can use to logically group Open Catalog service principals together and grant privileges on
securable objects.

Open Catalog supports a many-to-one relationship between service principals and principal roles. For example, to grant the same privileges to
multiple service principals, you can grant a single principal role to those service principals. A service principal can be granted only one
principal role. When registering a service connection, the Open Catalog administrator specifies the principal role that is granted to the
service principal.

You don’t grant privileges directly to a principal role. Instead, you configure object permissions at the catalog role level, and then grant
catalog roles to a principal role.

The following table shows examples of principal roles that you might configure in Open Catalog:

| Principal role name | Description |
| --- | --- |
| Data\_engineer | A role that is granted to multiple service principals for running data engineering jobs. |
| Data\_scientist | A role that is granted to multiple service principals for running data science or AI jobs. |

Expand

Show lessSee more

## Custom role

A custom role is similar to a principal role but with a few differences. A custom role is also a resource in Open Catalog. You can
use a custom role for the following purposes:

- Logically group Open Catalog service principals together that you create through the Snowflake CLI. Open Catalog supports a many-to-one
  relationship between these service principals and custom roles. You use these service principals to
  [connect to Open Catalog with External OAuth](external-oauth-overview).
- Logically group Open Catalog users together that you create through the Snowflake CLI for key pair authentication. Open Catalog
  supports a many-to-one relationship between these users and custom roles. You use these service principals to
  [connect to Open Catalog with key pair authentication](key-pair-auth-overview).

To create a custom role, you must use the Snowflake CLI.

As with principal roles, you don’t grant privileges directly to a custom role. Instead, you configure object permissions at the catalog role level, and
then grant catalog roles to a custom role.

You can’t grant a custom role to a service principal that is created through the Open Catalog UI. In other words, when you
[configure a service connection](configure-service-connection), you can’t grant a custom role to the service principal for the service
connection. However, when you grant a catalog role to a custom role, the custom role appears in the **ASSIGNED TO PRINCIPAL ROLES** column
in the Open Catalog UI.

## Catalog role

A catalog role belongs to a particular catalog resource in Open Catalog and specifies a set of permissions for actions on the catalog or objects
in the catalog, such as catalog namespaces or tables. You can create one or more catalog roles for a catalog.

You grant privileges to a catalog role and then grant the catalog role to a principal role to bestow the privileges to one or more service
principals.

**Note**

> If you update the privileges bestowed to a service principal, the updates won’t take effect for up to one hour. This means that if you
> revoke or grant some privileges for a catalog, the updated privileges won’t take effect on any service principal with access to that catalog
> for up to one hour.

Open Catalog also supports a many-to-many relationship between catalog roles and principal roles. You can grant the same catalog role to one or more
principal roles. Likewise, a principal role can be granted one or more catalog roles.

The following table displays examples of catalog roles that you might
configure in Open Catalog:

| Example Catalog role | Description |
| --- | --- |
| Catalog administrators | A role that has been granted multiple privileges to emulate full access to the catalog.  Principal roles that have been granted this role are permitted to create, alter, read, write, and drop tables in the catalog. |
| Catalog readers | A role that has been granted read-only privileges to tables in the catalog.  Principal roles that have been granted this role are allowed to read from tables in the catalog. |
| Catalog contributor | A role that has been granted read and write access privileges to all tables that belong to the catalog.  Principal roles that have been granted this role are allowed to perform read and write operations on tables in the catalog. |

Expand

Show lessSee more

## User roles

A user is someone who signs in to the Open Catalog web interface to manage the Open Catalog account. However, before a user can manage the
account, they must be granted at least one user role. The user roles available to grant to a user are service admin and catalog admin.

### Service admin role

The service admin role allows a user to manage the entire account, with a few exceptions.

#### Allowed permissions

A user with service admin privileges is a service admin. A service admin can perform the following tasks in the account:

- Create service connections.
- Use network policies.
- Manage users: Create and drop users, grant roles to users, and revoke roles from users.
- Create catalogs and manage the catalogs that they create.

When a service admin creates a catalog, they are also automatically granted the catalog admin role on the catalog. The service admin can do
the following to a catalog they that have catalog admin privileges on:

- Grant to another user the catalog admin role to the catalog. As a result, both users can access the catalog.
- Revoke their own catalog admin privileges to the catalog, thereby losing access to the catalog. However, before revoking their catalog
  admin privileges, they must first grant to another user catalog admin privileges to that catalog.

#### Disallowed permissions

A user with service admin privileges can’t perform the following tasks in the account:

- Access or manage a catalog that they didn’t create.
- Grant catalog admin privileges to a catalog that the service admin didn’t create.

### Catalog admin role

The catalog admin role allows a user to manage a catalog in the account. The catalog admin role must be granted to each individual catalog.

#### Allowed permissions

The catalog admin role grants to a user the permissions to access and manage a catalog, as follows:

- Access the catalog.
- Create namespaces in the catalog.
- Create a catalog role in the catalog and grant privileges to it.
- Grant a catalog role to a principal role, which bestows the service principal with the privileges that are granted to the catalog role.

#### Disallowed permissions

A user with only catalog admin privileges can’t perform the following tasks in the account:

- Create a service connection.
- Access or manage catalogs for which they haven’t been granted the catalog admin role.
- Create or remove a catalog.
- Use network policies.
- Manage users.

## RBAC model

The following diagram illustrates the RBAC model used by Open Catalog. For each catalog, the Open Catalog catalog admin assigns access
privileges to catalog roles and then grants service principals access to resources by assigning catalog roles to principal roles. Open Catalog
supports a many-to-one relationship between service principals and principal roles.

Note

- For [External OAuth](external-oauth-overview) and [key pair authentication](key-pair-auth-overview), a [custom role](#custom-role) is used instead of a **principal role**.
- For key pair authentication, a key pair authentication user is used instead of a **service principal**. This type of user connects to Open Catalog
  programmatically through an access token. It’s not a human user that signs in to the Open Catalog UI by using a username and password.

[![Diagram that shows the RBAC model for Open Catalog.](/static/images/user-guide/opencatalog/img/rbac-model.svg "Open Catalog RBAC model")](/static/images/user-guide/opencatalog/img/rbac-model.svg)

You can also grant access control privileges at the table or namespace level. For example, the following diagram depicts granting privileges
on a namespace and table within the catalog.

[![Diagram that shows the RBAC model for Open Catalog at table, namespace level.](/static/images/user-guide/opencatalog/img/rbac-model-namespace-table.svg "Open Catalog RBAC model at table, namespace level")](/static/images/user-guide/opencatalog/img/rbac-model-namespace-table.svg)

## Access control privileges

This section describes the privileges that are available in the Open Catalog access control model. Privileges are granted to catalog roles, catalog roles are granted to principal roles, and principal roles are granted to service principals to specify the operations that service principals can perform on objects in Open Catalog.

To grant the full set of privileges (drop, list, read, write, etc.) on an object, you can use the *full privilege* option.

For more information, see:

- [Catalog privileges](#catalog-privileges)
- [Namespace privileges](#namespace-privileges)
- [Table privileges](#table-privileges)

Note

For privilege sets for common catalog roles, such as Table Reader, see [Privilege sets for common catalog roles](#privilege-sets-for-common-catalog-roles).

### Catalog privileges

| Privilege | Description |
| --- | --- |
| CATALOG\_MANAGE\_CONTENT | Enables full management of content for the catalog. This privilege encompasses the following privileges:  - CATALOG\_MANAGE\_METADATA - TABLE\_FULL\_METADATA - NAMESPACE\_FULL\_METADATA - VIEW\_FULL\_METADATA - TABLE\_WRITE\_DATA - TABLE\_READ\_DATA - CATALOG\_READ\_PROPERTIES - CATALOG\_WRITE\_PROPERTIES |
| CATALOG\_MANAGE\_METADATA | Enables full management of the catalog, catalog roles, namespaces, and tables. |
| CATALOG\_READ\_PROPERTIES | Enables listing catalogs and reading properties of the catalog. |
| CATALOG\_WRITE\_PROPERTIES | Enables configuring catalog properties. |
| NAMESPACE\_CREATE | Enables creating a namespace in a catalog. |
| NAMESPACE\_DROP | Enables dropping the namespace from the catalog. |
| NAMESPACE\_FULL\_METADATA | Grants all namespace privileges. |
| NAMESPACE\_LIST | Enables listing any object in the namespace, including nested namespaces and tables. |
| NAMESPACE\_READ\_PROPERTIES | Enables reading all the namespace properties. |
| NAMESPACE\_WRITE\_PROPERTIES | Enables configuring namespace properties. |
| TABLE\_CREATE | Enables registering a table with the catalog. |
| TABLE\_DROP | Enables dropping a table from the catalog. |
| TABLE\_FULL\_METADATA | Grants all table privileges, except TABLE\_READ\_DATA and TABLE\_WRITE\_DATA, which need to be granted individually. |
| TABLE\_LIST | Enables listing any tables in the catalog. |
| TABLE\_READ\_DATA | Enables reading data from the table by receiving short-lived read-only storage credentials from the catalog. |
| TABLE\_READ\_PROPERTIES | Enables reading [properties](https://iceberg.apache.org/docs/nightly/configuration/#table-properties) of the table. |
| TABLE\_WRITE\_DATA | Enables writing data to the table by receiving short-lived read+write storage credentials from the catalog. |
| TABLE\_WRITE\_PROPERTIES | Enables configuring [properties](https://iceberg.apache.org/docs/nightly/configuration/#table-properties) for the table. |
| VIEW\_CREATE | Enables registering a view with the catalog. |
| VIEW\_DROP | Enables dropping a view from the catalog. |
| VIEW\_FULL\_METADATA | Grants all view privileges. |
| VIEW\_LIST | Enables listing any views in the catalog. |
| VIEW\_READ\_PROPERTIES | Enables reading all the view properties. |

Expand

Show lessSee more

### Namespace privileges

| Privilege | Description |
| --- | --- |
| CATALOG\_MANAGE\_CONTENT | Enables full management of content for the namespace, any tables grouped under it, and any namespaces and tables nested under the namespace, if applicable. The privilege is not granted to the entire catalog. This privilege encompasses the following privileges:  - CATALOG\_MANAGE\_METADATA - TABLE\_FULL\_METADATA - NAMESPACE\_FULL\_METADATA - VIEW\_FULL\_METADATA - TABLE\_WRITE\_DATA - TABLE\_READ\_DATA - CATALOG\_READ\_PROPERTIES - CATALOG\_WRITE\_PROPERTIES |
| CATALOG\_MANAGE\_METADATA | Enables full management of the namespace, catalog roles, and any tables grouped under it or any child namespaces or tables nested under it. |
| NAMESPACE\_CREATE | Enables creating a child namespace off the namespace. |
| NAMESPACE\_DROP | Enables dropping the namespace from the catalog. |
| NAMESPACE\_FULL\_METADATA | Grants all namespace privileges on the namespace. |
| NAMESPACE\_LIST | Enables listing any object in the namespace, including nested namespaces and tables. |
| NAMESPACE\_READ\_PROPERTIES | Enables reading all the namespace properties. |
| NAMESPACE\_WRITE\_PROPERTIES | Enables configuring namespace properties. |
| TABLE\_CREATE | Enables registering a table with the namespace. |
| TABLE\_DROP | Enables dropping a table from the namespace. |
| TABLE\_FULL\_METADATA | Grants all table privileges for tables grouped on the namespace, except TABLE\_READ\_DATA and TABLE\_WRITE\_DATA, which need to be granted individually. |
| TABLE\_LIST | Enables listing any tables in the namespace. |
| TABLE\_READ\_DATA | Enables reading data from any table grouped under the namespace by receiving short-lived read-only storage credentials from the catalog. |
| TABLE\_READ\_PROPERTIES | Enables reading [properties](https://iceberg.apache.org/docs/nightly/configuration/#table-properties) of any table grouped under the namespace. |
| TABLE\_WRITE\_DATA | Enables writing data to any table grouped on the namespace by receiving short-lived read+write storage credentials from the catalog. |
| TABLE\_WRITE\_PROPERTIES | Enables configuring [properties](https://iceberg.apache.org/docs/nightly/configuration/#table-properties) for any table grouped under the namespace. |
| VIEW\_CREATE | Enables registering a view with the namespace. |
| VIEW\_DROP | Enables dropping a view from the namespace. |
| VIEW\_FULL\_METADATA | Grants all view privileges for all views in the namespace. |
| VIEW\_LIST | Enables listing any views in the namespace. |
| VIEW\_READ\_PROPERTIES | Enables reading all the view properties for all view in the namespace. |
| VIEW\_WRITE\_PROPERTIES | Enables configuring view properties for any view in the namespace. |

Expand

Show lessSee more

### Table privileges

| Privilege | Description |
| --- | --- |
| TABLE\_DROP | Enables dropping the table from the catalog. |
| TABLE\_FULL\_METADATA | Grants all table privileges, except TABLE\_READ\_DATA and TABLE\_WRITE\_DATA, which need to be granted individually. |
| TABLE\_LIST | Enables listing any tables in the catalog. |
| TABLE\_READ\_DATA | Enables reading data from the table by receiving short-lived read-only storage credentials from the catalog. |
| TABLE\_READ\_PROPERTIES | Enables reading [properties](https://iceberg.apache.org/docs/nightly/configuration/#table-properties) of the table. |
| TABLE\_WRITE\_DATA | Enables writing data to the table by receiving short-lived read+write storage credentials from the catalog. |
| TABLE\_WRITE\_PROPERTIES | Enables configuring [properties](https://iceberg.apache.org/docs/nightly/configuration/#table-properties) for the table. |
| VIEW\_READ\_PROPERTIES | Enables reading all the view properties. |

Expand

Show lessSee more

### View privileges

| Privilege | Description |
| --- | --- |
| VIEW\_CREATE | Enables registering a view with the catalog. |
| VIEW\_DROP | Enables dropping a view from the catalog. |
| VIEW\_LIST | Enables listing any views in the catalog. |
| VIEW\_READ\_PROPERTIES | Enables reading all the view properties. |
| VIEW\_WRITE\_PROPERTIES | Enables configuring view properties. |
| VIEW\_FULL\_METADATA | Grants all view privileges. |

Expand

Show lessSee more

### Privilege sets for common catalog roles

| Catalog role | Description | Privileges |
| --- | --- | --- |
| table\_reader | Read the table information and query the tables. | - TABLE\_LIST - TABLE\_READ\_PROPERTIES - TABLE\_READ\_DATA - TABLE\_FULL\_METADATA |
| catalog\_writer | Create and drop tables. | - TABLE\_CREATE - TABLE\_DROP - TABLE\_LIST - TABLE\_READ\_PROPERTIES - TABLE\_WRITER\_PROPERTIES - TABLE\_READ\_METADATA - TABLE\_WRITE\_METADATA - TABLE\_FULL\_METADATA |
| catalog\_metadata\_reader | Read catalog metadata. | - NAMESPACE\_LIST - NAMESPACE\_READ\_PROPERTIES - NAMESPACE\_FULL\_METADATA - CATALOG\_READ\_PROPERTIES |

Expand

Show lessSee more

## RBAC example

The following diagram illustrates how RBAC works in Open Catalog at the catalog level and includes the following users:

- **Alice:** A service admin who signs up for Open Catalog. Alice can create service principals. She can also create catalogs and namespaces and
  configure access control for Open Catalog resources.

  > **Note**

  > The service principal for Alice is not visible in the Open Catalog user interface.
- **Bob:** A data engineer who uses Snowpipe Streaming (in Snowflake) and Apache Spark™ connections to interact with Open Catalog.

  - Alice has created a service principal for Bob. It has been granted the Data\_engineer principal role, which in turn has been granted
    the following catalog roles: Catalog contributor and Data administrator (for both the Silver and Gold zone catalogs in the following
    diagram).
    - The Catalog contributor role grants permission to create namespaces and tables in the Bronze zone catalog.
    - The Data administrator roles grant full administrative rights to the Silver zone catalog and Gold zone catalog.
- **Mark:** A data scientist who uses Snowflake AI services to interact with Open Catalog.

  - Alice has created a service principal for Mark. It has been granted the Data\_scientist principal role, which in turn has been granted
    the catalog role named Catalog reader.
    - The Catalog reader role grants read-only access for a catalog named Gold zone catalog.

[![Diagram that shows an example of how RBAC works in Open Catalog.](/static/images/user-guide/opencatalog/img/rbac-example.svg "Open Catalog RBAC example")](/static/images/user-guide/opencatalog/img/rbac-example.svg)
