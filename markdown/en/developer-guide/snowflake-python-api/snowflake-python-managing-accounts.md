# Managing Snowflake accounts and managed accounts with Python

You can use Python to manage accounts and managed accounts in Snowflake.

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

## Managing accounts

You can manage accounts in your Snowflake organization. For an overview of accounts in Snowflake, see
[Managing accounts in your organization](/user-guide/organizations-manage-accounts).

The Snowflake Python APIs represents accounts with two separate types:

- `Account`: Exposes an account’s properties such as its name identifier, the login name and password of its initial administrative
  user, and its Snowflake edition.
- `AccountResource`: Exposes methods you can use to drop and restore a corresponding `Account` object.

### Creating an account

To create an account, first create an `Account` object, and then create an `AccountCollection` object from the API `Root`
object. Using `AccountCollection.create`, add the new account to Snowflake.

Code in the following example creates an `Account` object that represents an account named `my_account1` with the specified
account properties:

Copy code

```
from snowflake.core.account import Account

my_account = Account(
  name="my_account1",
  admin_name="admin",
  admin_password="TestPassword1",
  first_name="Jane",
  last_name="Smith",
  email="myemail@myorg.org",
  edition="ENTERPRISE",
  region="aws_us_west_2",
  comment="creating my account",
)

root.accounts.create(my_account)
```

### Listing accounts

You can list accounts using the `AccountCollection.iter` method, which returns a `PagedIter` iterator of `Account`
objects.

Code in the following example lists accounts whose name starts with `my` and prints the name of each:

Copy code

```
account_iter = root.accounts.iter(like="my%")  # returns a PagedIter[Account]
for account_obj in account_iter:
  print(account_obj.name)
```

Code in the following example sets the optional parameter `history=True` to list a history of accounts including dropped accounts that
have not yet been deleted.

Copy code

```
account_iter = root.accounts.iter(history=True)  # returns a PagedIter[Account]
for account_obj in account_iter:
  print(account_obj.name)
```

### Performing account operations

You can perform common account operations—such as dropping and restoring an account—with an `AccountResource` object.

To demonstrate operations you can do with an account resource, code in the following example does the following:

1. Gets the `my_account1` account resource object.
2. Drops the account with the specified grace period, which is the number of days during which the account can be restored (“undropped”).
3. Restores the dropped account within the specified grace period (that is, before it’s permanently deleted).

Copy code

```
my_account_res = root.accounts["my_account1"]
my_account_res.drop(grace_period_in_days=4)
my_account_res.undrop()
```

## Managing managed accounts

You can manage Snowflake managed accounts, which are currently used by data providers to create reader accounts for their consumers. For
more information, see [Manage reader accounts](/user-guide/data-sharing-reader-create).

The Snowflake Python APIs represents managed accounts with two separate types:

- `ManagedAccount`: Exposes a managed account’s properties such as its name identifier, the login name and password of its initial
  administrative user, and its account type.
- `ManagedAccountResource`: Exposes methods you can use to drop a corresponding `ManagedAccount` object.

### Creating a managed account

To create a managed account, first create a `ManagedAccount` object, and then create a `ManagedAccountCollection` object from
the API `Root` object. Using `ManagedAccountCollection.create`, add the new managed account to Snowflake.

Code in the following example creates a `ManagedAccount` object that represents a managed account named `reader_acct1` with the
specified account properties:

Copy code

```
from snowflake.core.managed_account import ManagedAccount

my_managed_account = ManagedAccount(
  name="reader_acct1",
  admin_name="admin",
  admin_password="TestPassword1",
  type="READER",
  comment="creating my managed account",
)

root.managed_accounts.create(my_managed_account)
```

### Listing managed accounts

You can list managed accounts using the `ManagedAccountCollection.iter` method, which returns a `PagedIter` iterator of
`ManagedAccount` objects.

Code in the following example lists managed accounts whose name starts with `reader` and prints the name of each:

Copy code

```
account_iter = root.managed_accounts.iter(like="reader%")  # returns a PagedIter[ManagedAccount]
for account_obj in account_iter:
  print(account_obj.name)
```

### Dropping a managed account

You can drop a managed account with a `ManagedAccountResource` object.

Code in the following example gets the `reader_acct1` managed account resource object and then drops the account.

Copy code

```
my_managed_account_res = root.managed_accounts["reader_acct1"]
my_managed_account_res.drop()
```
