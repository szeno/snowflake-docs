# Managing Snowflake users, roles, and grants with Python

You can use Python to manage Snowflake users, roles, and grants. For more information about managing users and their privileges in
Snowflake, see [User management](/user-guide/admin-user-management).

## Prerequisites

The examples in this topic assume that you’ve added code to connect with Snowflake and to create a `Root` object from which to use the
Snowflake Python APIs.

For example, the following code uses connection parameters defined in a configuration file to create a connection to Snowflake:

Copy code

```
from snowflake.core import Root
from snowflake.snowpark import Session

session = Session.builder.config("connection_name", "myconnection").create()
root = Root(session)
```

Using the resulting `Session` object, the code creates a `Root` object to use the API’s types and methods. For more information,
see [Connect to Snowflake with the Snowflake Python APIs](/developer-guide/snowflake-python-api/snowflake-python-connecting-snowflake).

## Managing users

You can manage users in Snowflake. A user is an account-level object in Snowflake. The Snowflake Python APIs represents users with two
separate types:

- `User`: Exposes a user’s properties, such as its name.
- `UserResource`: Exposes methods you can use to fetch a corresponding `User` object and to drop the user.

### Creating a user

You can create a user by calling the `UserCollection.create` method and passing a `User` object that represents the user you
want to create. To create a user, first create a `User` object that specifies the user name.

Code in the following example creates a `User` object representing a user named `my_user` and then creates the user by passing
the `User` object to the `UserCollection.create` method:

Copy code

```
from snowflake.core.user import User

my_user = User(name="my_user")
root.users.create(my_user)
```

### Getting user details

You can get information about a user by calling the `UserResource.fetch` method, which returns a `User` object.

Code in the following example gets information about a user named `my_user`:

Copy code

```
my_user = root.users["my_user"].fetch()
print(my_user.to_dict())
```

### Creating or altering a user

You can set properties of a `User` object and pass it to the `UserResource.create_or_alter` method to create a user if it
doesn’t exist, or alter it according to the user definition if it does exist. The behavior of `create_or_alter` is intended to be
idempotent, which means that the resulting user object will be the same regardless of whether the user exists before you call the method.

`create_or_alter` uses default values for any [User](/developer-guide/snowflake-python-api/reference/latest/_autosummary/snowflake.core.user.User)
properties that you don’t explicitly define. For example, if you don’t set `snowflake_support`, its value defaults to `False` even
if the user previously existed with a different value.

Note

The `create_or_alter` method currently does not support changing the `password` for an existing user. You can only set the
password when creating a new user.

Code in the following example updates the first name, last name, and `must_change_password` properties of the `my_user` user, and
then alters the user on Snowflake:

Copy code

```
user_parameters = root.users["my_user"].fetch()
user_parameters.first_name="Snowy"
user_parameters.last_name="User"
user_parameters.must_change_password=False
root.users["my_user"].create_or_alter(user_parameters)
```

### Listing users

You can list users using the `iter` method, which returns a `PagedIter` iterator.

Code in the following example lists users whose name begins with `my`:

Copy code

```
users = root.users.iter(like="my%")
for user in users:
  print(user.name)
```

### Dropping a user

You can drop a user using the `UserResource.drop` method.

Code in the following example drops the `my_user` user:

Copy code

```
my_user_res = root.users["my_user"]
my_user_res.drop()
```

## Managing roles

You can manage roles in Snowflake. A role is an account-level object. The Snowflake Python APIs represents roles with two separate types:

- `Role`: Exposes a role’s properties, such as its name.
- `RoleResource`: Exposes methods you can use to grant and manage privileges on a corresponding `Role` object, and to drop the role.

### Creating a role

To create a role, first create a `Role` object that specifies the role name.

Code in the following example creates a `Role` object representing a role named `my_role`:

Copy code

```
from snowflake.core.role import Role

my_role = Role(name="my_role")
root.roles.create(my_role)
```

The code then creates the role by passing the `Role` object to the `RoleCollection.create` method.

### Using a role in a session

Code in the following example applies the role `my_role` in the current session.

Copy code

```
root.session.use_role("my_role")
```

### Listing roles

You can list the roles in an account using the `iter` method. The method returns a `PagedIter` iterator of `Role` objects.

Code in the following example lists all role names in an account:

Copy code

```
role_list = root.roles.iter()
for role_obj in role_list:
  print(role_obj.name)
```

### Dropping a role

You can drop a role using the `RoleResource.drop` method.

Code in the following example drops the `my_role` role:

Copy code

```
my_role_res = root.roles["my_role"]
my_role_res.drop()
```

## Managing database roles

You can manage [database roles](/user-guide/security-access-control-considerations#label-access-control-considerations-database-roles) in Snowflake. A database role is a database-level
object. The Snowflake Python APIs represents database roles with two separate types:

- `DatabaseRole`: Exposes a database role’s properties, such as its name and a comment.
- `DatabaseRoleResource`: Exposes methods you can use to grant and manage privileges on a corresponding `DatabaseRole` object,
  and to drop the database role.

### Creating a database role

To create a database role, first create a `DatabaseRole` object that specifies the role name.

Code in the following example creates a `DatabaseRole` object representing a database role named `my_db_role`:

Copy code

```
from snowflake.core.database_role import DatabaseRole

my_db_role = DatabaseRole(
  name="my_db_role",
  comment="sample comment"
)

my_db_role_ref = root.databases['my_db'].database_roles.create(my_db_role)
```

The code then creates the database role by passing the `DatabaseRole` object to the `DatabaseRoleCollection.create` method.

#### Cloning a database role

Code in the following example creates a database role named `dr2` in the `my_db_2` target database as a copy of the existing `dr1`
database role in the `my_db` database.

Copy code

```
database_role_ref = root.databases['my_db'].database_roles['dr1'].clone(target_database_role='dr2', target_database='my_db_2')
```

### Listing database roles

You can list the database roles in an account using the `iter` method. The method returns a `PagedIter` iterator of
`DatabaseRole` objects.

Code in the following example lists the database role named `my_db_role` in the `my_db` database, limiting the number of results to `1`:

Copy code

```
db_role_list = root.databases['my_db'].database_roles.iter(limit=1, from_name='my_db_role')
for db_role_obj in db_role_list:
  print(db_role_obj.name)
```

### Dropping a database role

You can drop a database role using the `DatabaseRoleResource.drop` method.

Code in the following example drops the `my_db_role` database role:

Copy code

```
root.databases['my_db'].database_roles['my_db_role'].drop()
```

## Managing access privileges

You can use the API to manage access privileges on a securable Snowflake object to an account role, database role, or user. For more
information about roles, securable objects, and the access control framework in Snowflake, see [Overview of Access Control](/user-guide/security-access-control-overview).

### For account roles

The following code examples demonstrate the API operations to grant privileges, revoke privileges, and list grants for
[account roles](/user-guide/security-access-control-overview#label-access-control-overview-role-types).

#### Grant privileges

Copy code

```
from snowflake.core.role import Securable

root.roles['my_role'].grant_privileges(
    privileges=["OPERATE"], securable_type="WAREHOUSE", securable=Securable(name='my_wh')
)
```

#### Grant role

Copy code

```
from snowflake.core.role import Securable

root.roles['my_role'].grant_role(role_type="ROLE", role=Securable(name='my_role_1'))
```

#### Grant privileges on all

Copy code

```
from snowflake.core.role import ContainingScope

root.roles['my_role'].grant_privileges_on_all(
    privileges=["SELECT"],
    securable_type="TABLE",
    containing_scope=ContainingScope(database='my_db', schema='my_schema'),
)
```

#### Grant future privileges

Copy code

```
from snowflake.core.role import ContainingScope

root.roles['my_role'].grant_future_privileges(
    privileges=["SELECT", "INSERT"],
    securable_type="TABLE",
    containing_scope=ContainingScope(database='my_db', schema='my_schema'),
)
```

#### Revoke privileges

Copy code

```
from snowflake.core.role import Securable

root.roles['my_role'].revoke_privileges(
    privileges=["OPERATE"], securable_type="WAREHOUSE", securable=Securable(name='my_wh')
)
```

#### Revoke role

Copy code

```
from snowflake.core.role import Securable

root.roles['my_role'].revoke_role(role_type="ROLE", role=Securable(name='my_role_1'))
```

#### Revoke privileges on all

Copy code

```
from snowflake.core.role import ContainingScope

root.roles['my_role'].revoke_privileges_on_all(
    privileges=["SELECT"],
    securable_type="TABLE",
    containing_scope=ContainingScope(database='my_db', schema='my_schema'),
)
```

#### Revoke future privileges

Copy code

```
from snowflake.core.role import ContainingScope

root.roles['my_role'].revoke_future_privileges(
    privileges=["SELECT", "INSERT"],
    securable_type="TABLE",
    containing_scope=ContainingScope(database='my_db', schema='my_schema'),
)
```

#### Revoke grant option for privileges

Copy code

```
from snowflake.core.role import Securable

 root.roles['my_role'].revoke_grant_option_for_privileges(
    privileges=["OPERATE"], securable_type="WAREHOUSE", securable=Securable(name='my_wh')
)
```

#### Revoke grant option for privileges on all

Copy code

```
from snowflake.core.role import ContainingScope

root.roles['my_role'].revoke_grant_option_for_privileges_on_all(
    privileges=["SELECT"],
    securable_type="TABLE",
    containing_scope=ContainingScope(database='my_db', schema='my_schema'),
)
```

#### Revoke grant option for future privileges

Copy code

```
from snowflake.core.role import ContainingScope

root.roles['my_role'].revoke_grant_option_for_future_privileges(
    privileges=["SELECT", "INSERT"],
    securable_type="TABLE",
    containing_scope=ContainingScope(database='my_db', schema='my_schema'),
)
```

#### List grants to the role

Copy code

```
root.roles['my_role'].iter_grants_to()
```

#### List grants on the role

Copy code

```
root.roles['my_role'].iter_grants_on()
```

#### List grants of the role

Copy code

```
root.roles['my_role'].iter_grants_of()
```

#### List future grants to the role

Copy code

```
root.roles['my_role'].iter_future_grants_to()
```

### For users

The following code examples demonstrate the API operations to grant a role, revoke a role, and list roles for users.

#### Grant role to a user

Copy code

```
from snowflake.core.user import Securable

root.users['my_user'].grant_role(role_type="ROLE", role=Securable(name='my_role'))
```

#### Revoke role from a user

Copy code

```
from snowflake.core.user import Securable

root.users['my_user'].revoke_role(role_type="ROLE", role=Securable(name='my_role'))
```

#### List roles granted to a user

Copy code

```
root.users['my_user'].iter_grants_to()
```

### For database roles

The following code examples demonstrate the API operations to grant privileges, revoke privileges, and list grants for
[database roles](/user-guide/security-access-control-overview#label-access-control-overview-role-types).

#### Grant privileges

Copy code

```
from snowflake.core.database_role import Securable

root.databases['my_db'].database_roles['my_db_role'].grant_privileges(
    privileges=["MODIFY"], securable_type="DATABASE", securable=Securable(name='my_db')
)
```

#### Grant role

Copy code

```
from snowflake.core.database_role import Securable

root.databases['my_db'].database_roles['my_db_role'].grant_role(role_type="DATABASE ROLE", role=Securable(name='my_db_role_1'))
```

#### Grant privileges on all

Copy code

```
from snowflake.core.database_role import ContainingScope

root.databases['my_db'].database_roles['my_db_role'].grant_privileges_on_all(
    privileges=["SELECT"],
    securable_type="TABLE",
    containing_scope=ContainingScope(database='my_db', schema='my_schema'),
)
```

#### Grant future privileges

Copy code

```
from snowflake.core.database_role import ContainingScope

root.databases['my_db'].database_roles['my_db_role'].grant_future_privileges(
    privileges=["SELECT", "INSERT"],
    securable_type="TABLE",
    containing_scope=ContainingScope(database='my_db', schema='my_schema'),
)
```

#### Revoke privileges

Copy code

```
from snowflake.core.database_role import Securable

root.databases['my_db'].database_roles['my_db_role'].revoke_privileges(
    privileges=["MODIFY"], securable_type="DATABASE", securable=Securable(name='my_db')
)
```

#### Revoke role

Copy code

```
from snowflake.core.database_role import Securable

root.databases['my_db'].database_roles['my_db_role'].revoke_role(role_type="DATABASE ROLE", role=Securable(name='my_db_role_1'))
```

#### Revoke all privileges

Copy code

```
from snowflake.core.database_role import ContainingScope

root.databases['my_db'].database_roles['my_db_role'].revoke_privileges_on_all(
    privileges=["SELECT"],
    securable_type="TABLE",
    containing_scope=ContainingScope(database='my_db', schema='my_schema'),
)
```

#### Revoke future privileges

Copy code

```
from snowflake.core.database_role import ContainingScope

root.databases['my_db'].database_roles['my_db_role'].revoke_future_privileges(
    privileges=["SELECT", "INSERT"],
    securable_type="TABLE",
    containing_scope=ContainingScope(database='my_db', schema='my_schema'),
)
```

#### Revoke grant option for privileges

Copy code

```
from snowflake.core.database_role import Securable

root.databases['my_db'].database_roles['my_db_role'].revoke_grant_option_for_privileges(
    privileges=["MODIFY"], securable_type="DATABASE", securable=Securable(name='my_db')
)
```

#### Revoke grant option for privileges on all

Copy code

```
from snowflake.core.database_role import ContainingScope

root.databases['my_db'].database_roles['my_db_role'].revoke_grant_option_for_privileges_on_all(
    privileges=["SELECT"],
    securable_type="TABLE",
    containing_scope=ContainingScope(database='my_db', schema='my_schema'),
)
```

#### Revoke grant option for future privileges

Copy code

```
from snowflake.core.database_role import ContainingScope

root.databases['my_db'].database_roles['my_db_role'].revoke_grant_option_for_future_privileges(
    privileges=["SELECT", "INSERT"],
    securable_type="TABLE",
    containing_scope=ContainingScope(database='my_db', schema='my_schema'),
)
```

#### List grants to the role

Copy code

```
root.databases['my_db'].database_roles['my_db_role'].iter_grants_to()
```

#### List future grants to the role

Copy code

```
root.databases['my_db'].database_roles['my_db_role'].iter_future_grants_to()
```

## Managing grants using the `Grant` resource — *Deprecated*

Deprecated API

Using the `Grant` resource API to manage grants, as shown in the following code examples, is now deprecated. Version 0.13.1 of the
API introduces new grant methods in the `User`, `Role`, and `DatabaseRole` resources that you can use to
[manage access privileges](#label-snowflake-python-privileges).

You can execute [GRANT <privileges> … TO ROLE](/sql-reference/sql/grant-privilege) operations to grant access privileges on a securable Snowflake object to a role.

### Granting privileges

To grant privileges on a Snowflake object, you first create a `Grant` object that specifies the following attributes:

- `grantee`: The role or user that is being granted the privileges.
- `securable`: The Snowflake object that is being secured by the privileges.
- `privileges`: The privileges that are being granted to a role.

#### Granting CREATE privileges in an account to a role

Code in the following example creates a `Grant` object representing a grant operation that grants the privileges `create_database`
and `create_warehouse` to the role `my_role` in the current Snowflake account. The code executes the operation using the
`root.grants.grant` method.

Copy code

```
from snowflake.core.grant import Grant
from snowflake.core.grant._grantee import Grantees
from snowflake.core.grant._privileges import Privileges
from snowflake.core.grant._securables import Securables

root.grants.grant(
  Grant(
    grantee=Grantees.role(name='my_role'),
    securable=Securables.current_account,
    privileges=[Privileges.create_database,
                Privileges.create_warehouse],
  )
)
```

#### Granting privileges on a database to a role

Code in the following example grants [imported privileges](/user-guide/data-share-consumers#label-granting-privileges-on-shared-database) on the database `my_db`
to the role `my_role`:

Copy code

```
from snowflake.core.grant import Grant
from snowflake.core.grant._grantee import Grantees
from snowflake.core.grant._privileges import Privileges
from snowflake.core.grant._securables import Securables

root.grants.grant(
  Grant(
    grantee=Grantees.role('my_role'),
    securable=Securables.database('my_db'),
    privileges=[Privileges.imported_privileges],
  )
)
```

### Granting a role to another role

You can assign a role to another role to create a “parent-child” relationship between the roles (also referred to as a *role hierarchy*).

Code in the following example grants the `my_role` user role to the `ACCOUNTADMIN` system role:

Copy code

```
from snowflake.core.grant import Grant
from snowflake.core.grant._grantee import Grantees
from snowflake.core.grant._securables import Securables

root.grants.grant(
  Grant(
    grantee=Grantees.role('ACCOUNTADMIN'),
    securable=Securables.role('my_role'),
  )
)
```
