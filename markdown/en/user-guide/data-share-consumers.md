# Consume imported data

This topic describes the tasks associated with creating databases from shares made available by data providers and then using the databases
for queries and other operations.

You must use the ACCOUNTADMIN role (or a role granted the IMPORT SHARE global privilege) to perform these tasks. For more details about the
IMPORT SHARE privilege, see [Enable non-ACCOUNTADMIN roles to perform data sharing tasks](/user-guide/security-access-privileges-shares).

Note

The tasks described in this topic do not apply to reader accounts. If you are using a reader account to consume imported data, you do not
need to perform any of these tasks because they have already been completed by an administrator from the provider account.

## General limitations for imported databases

Imported databases have the following limitations for consumers:

- Imported databases are read-only. Users in a consumer account can view/query data, but cannot insert or update data, or create any objects
  in the database.
- The following actions are not supported:

  - Creating a clone of an imported database or any schemas/tables in the database.
  - Time Travel for an imported database or any schemas/tables in the database.
  - Editing the comments for an imported database.
  - Attaching [storage lifecycle policies](/user-guide/storage-management/storage-lifecycle-policies) to tables in an imported database.
- You can reshare an imported database only when resharing is allowed. Run [SHOW DATABASES](/sql-reference/sql/show-databases)
  and check the `resharing_settings` column for the imported database. For the resharing workflow,
  see [Resharing shares](#resharing-shares).
- Imported databases cannot be replicated.

## Viewing available shares

You can view the shares that are available to consume in your account using either the web interface or SQL:

SnowsightSQL

To view shares that have been shared with you, in the navigation menu, select **Data sharing** » **Internal sharing**, then select **Shared With You**.

> From this page, you can view the following:
>
> - **Privately Shared Listings** that have been shared with you. You can also view **Data exchange** listings that you have access to.
> - **Direct shares** that have been shared with you. Depending on the share status, shares are grouped into two sections:
>   - Direct shares that are ready to get (that is, a database has not been created from the share).
>   - Direct shares that have been imported into a database and are ready to query.

To view Snowflake Marketplace listings that have been imported to a database and are ready to query, do the following steps:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Marketplace** » **Snowflake Marketplace**.

Execute a [SHOW SHARES](/sql-reference/sql/show-shares) or [DESCRIBE SHARE](/sql-reference/sql/desc-share) statement.

For example, using SQL:

Copy code

```
SHOW SHARES;
```

The output shows the following:

- Two shares, `sales_s` and `sales_s2` are available. `INBOUND` in the `kind` column specifies that a data provider made the
  share available to your account to consume.
- The `name` column displays the name of each share, in the form of `share_name` (for example, `SALES_S`).
- The `owner_account` column displays the account name that provided each share, in the form of `orgname.account_name`.
- If the `database_name` column is empty, a database has not yet been created from the share in your account.

```
+-------------------------------+----------+----------------------+---------------+-----------------------+------------------+--------------+----------------------------------------+---------------------+
| created_on                    | kind     | owner_account        | name          | database_name         | to               | owner        | comment                                | listing_global_name |                  |
|-------------------------------+----------+----------------------+---------------+-----------------------+------------------+--------------+----------------------------------------|---------------------|
| 2017-07-09 19:18:09.821 -0700 | INBOUND  | SNOW.XY12345         | SALES_S2      | UPDATED_SALES_DB      |                  |              | Transformed and updated sales data     |                     |
| 2017-06-15 17:02:29.625 -0700 | OUTBOUND | SNOW.MY_TEST_ACCOUNT | SALES_S       | SALES_DB              | XY12345, YZ23456 | ACCOUNTADMIN |                                        |                     |
+-------------------------------+----------+----------------------+---------------+-----------------------+----------------- -+--------------+----------------------------------------+---------------------+
```

### DESCRIBE SHARE example

The following example uses the [DESCRIBE SHARE](/sql-reference/sql/desc-share) command to show the objects (database, schemas, and tables) that are in
the `sales_s` share:

> Copy code
>
> ```
> DESC SHARE xy12345.sales_s;
>
> +----------+------------------------------------+---------------------------------+
> | kind     | name                               | shared_on                       |
> |----------+------------------------------------+---------------------------------|
> | DATABASE | <DB>                               | Thu, 15 Jun 2017 17:03:16 -0700 |
> | SCHEMA   | <DB>.AGGREGATES_EULA               | Thu, 15 Jun 2017 17:03:16 -0700 |
> | TABLE    | <DB>.AGGREGATES_EULA.AGGREGATE_1   | Thu, 15 Jun 2017 17:03:16 -0700 |
> | VIEW     | <DB>.AGGREGATES_EULA.AGGREGATE_1_v | Thu, 15 Jun 2017 17:03:16 -0700 |
> +----------+------------------------------------+---------------------------------+
> ```
>
> The share consists of one schema, `aggregates_eula`, with one table, `aggregate_1`. Each object name, including the database
> itself, is prefixed with `<DB>`. This indicates a database has not been created yet (in your account) from the share.

## Creating a database from a share

You can create a database from a share using the web interface or SQL:

SnowsightSQL

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Data sharing** » **External sharing**.
3. Select the **Shared with you** tab.
4. In the **Ready to Get** section, select the share that you want to create a database for.
5. Set a database name and the roles that are permitted to access the database.
6. Select **Get Data**.

Execute a [CREATE DATABASE](/sql-reference/sql/create-database) statement with the following data sharing-specific syntax:

Copy code

```
CREATE DATABASE <name> FROM SHARE <provider_account>.<share_name>
```

Where `provider_account` is the name of the account that provided the share and `share_name` is the name of the share
from which to create the database.

Note

- A share can only be consumed once per account.
- To see the objects that are being imported before creating a database, use the [DESCRIBE SHARE](/sql-reference/sql/desc-share) command.
- When a database is created from a share, only the role used to create the database can access objects in the database by default.
  For instructions on granting access to other roles, see [Granting Privileges on an Imported Database](#granting-privileges-on-an-imported-database) (in this topic).

### SQL examples

The following example creates a new database named `snow_sales` in your account from the `sales_s` share:

> Copy code
>
> ```
> CREATE DATABASE snow_sales FROM SHARE xy12345.sales_s;
> ```

List the new `snow_sales` database:

> Copy code
>
> ```
> SHOW DATABASES LIKE 'snow%';
>
> +---------------------------------+-----------------------+------------+------------+-------------------------+--------------+---------+---------+----------------+
> | created_on                      | name                  | is_default | is_current | origin                  | owner        | comment | options | retention_time |
> |---------------------------------+-----------------------+------------+------------+-------------------------+--------------+---------+---------+----------------|
> | Sun, 10 Jul 2016 23:28:50 -0700 | SNOWFLAKE_SAMPLE_DATA | N          | N          | SFC_SAMPLES.SAMPLE_DATA | ACCOUNTADMIN |         |         | 1              |
> | Thu, 15 Jun 2017 18:30:08 -0700 | SNOW_SALES            | N          | Y          | xy12345.SALES_S         | ACCOUNTADMIN |         |         | 1              |
> +---------------------------------+-----------------------+------------+------------+-------------------------+--------------+---------+---------+----------------+
> ```
>
> In this example, the `origin` column indicates the fully-qualified name of the share from which the database was created.

Similarly, the output of SHOW SHARES and DESC SHARE includes the name of the database that was created from the share:

> Copy code
>
> ```
> SHOW SHARES;
> ```
>
> ```
> +-------------------------------+----------+----------------------+---------------+-----------------------+------------------+--------------+----------------------------------------+---------------------+
> | created_on                    | kind     | owner_account        | name          | database_name         | to               | owner        | comment                                | listing_global_name |
> |-------------------------------+----------+----------------------+---------------+-----------------------+------------------+--------------+----------------------------------------|---------------------|
> | 2017-07-09 19:18:09.821 -0700 | INBOUND  | SNOW.XY12345         | SALES_S2      | UPDATED_SALES_DB      |                  |              | Transformed and updated sales data     |                     |
> | 2017-06-15 17:02:29.625 -0700 | OUTBOUND | SNOW.MY_TEST_ACCOUNT | SALES_S       | SALES_DB              | XY12345, YZ23456 | ACCOUNTADMIN |                                        |                     |
> +-------------------------------+----------+----------------------+---------------+-----------------------+------------------+--------------+----------------------------------------+---------------------+
> ```
>
> Copy code
>
> ```
> DESC SHARE xy12345.sales_s;
>
> +----------+------------------------------------------+---------------------------------+
> | kind     | name                                     | shared_on                       |
> |----------+------------------------------------------+---------------------------------|
> | DATABASE | SNOW_SALES                               | Thu, 15 Jun 2017 17:03:16 -0700 |
> | SCHEMA   | SNOW_SALES.AGGREGATES_EULA               | Thu, 15 Jun 2017 17:03:16 -0700 |
> | TABLE    | SNOW_SALES.AGGREGATES_EULA.AGGREGATE_1   | Thu, 15 Jun 2017 17:03:16 -0700 |
> | VIEW     | SNOW_SALES.AGGREGATES_EULA.AGGREGATE_1_v | Thu, 15 Jun 2017 17:03:16 -0700 |
> +----------+------------------------------------------+---------------------------------+
> ```

## Resharing shares

As a consumer, when resharing is allowed, you can reshare data that you imported from a provider’s direct share with other Snowflake
accounts in your own organization. You can’t reshare a direct share with accounts outside your organization.

Before you reshare, run [SHOW DATABASES](/sql-reference/sql/show-databases) and inspect the `resharing_settings` column for the imported
database. When resharing is allowed, `resharing_settings` contains a JSON object similar to the following:

Copy code

```
{
  "enabled": true,
  "only_within_organization": true
}
```

### Resharing workflow

To reshare data from a direct share, do the following:

- Create a database from the provider’s direct share, then run SHOW DATABASES and confirm that the `resharing_settings` column shows
  resharing is enabled.
- Create a secure view in your own database that references the imported data. You can’t attach objects from an imported database
  directly to a share.
- Create a share, grant the SELECT privilege on the secure view to the share, and add one or more consumer accounts in your organization
  to the share.

The following example imports the `snow_sales` database from the `xy12345.sales_s` direct share, exposes the data through a secure view,
and reshares that view with the `yz23456` account in the same organization:

Copy code

```
-- Create a database from the provider's direct share
CREATE DATABASE snow_sales FROM SHARE xy12345.sales_s;

-- Confirm the imported database is enabled for resharing
SHOW DATABASES LIKE 'snow_sales';

-- Create a secure view in your own database over the imported data
CREATE DATABASE sales_reshare;
CREATE SCHEMA sales_reshare.aggregates;
CREATE SECURE VIEW sales_reshare.aggregates.aggregate_1_v
  AS SELECT * FROM snow_sales.aggregates_eula.aggregate_1;

-- Create a share, grant access to the secure view, and add a consumer account in your organization
CREATE SHARE sales_reshare_s;
GRANT USAGE ON DATABASE sales_reshare TO SHARE sales_reshare_s;
GRANT USAGE ON SCHEMA sales_reshare.aggregates TO SHARE sales_reshare_s;
GRANT SELECT ON VIEW sales_reshare.aggregates.aggregate_1_v TO SHARE sales_reshare_s;
ALTER SHARE sales_reshare_s ADD ACCOUNTS = yz23456;
```

Resharing can extend across multiple accounts (multi-level resharing), as long as every account in the chain belongs to the same
organization as the resharer.

Resharing a direct share has the following limitations:

- You can’t attach objects from an imported database directly to a share. Create a secure view over the imported database and share that
  view instead.
- Resharing is restricted to accounts in your own organization.
- Cross-region resharing of direct shares isn’t supported. To reshare across regions, use listings. See [Reshare incoming data as a resharer](/collaboration/resharing-as-resharer).
- To reshare data that you have access to, the reshared view must be owned by the role that creates the outgoing share from your account.
  When a data provider adds governance policies and the view owner role and the share owner role are different, “what you access from the
  provider is what you reshare” doesn’t hold true. If you receive a reshared view from another role, you can always create a new secure view
  before you create another outgoing share.

## Granting privileges on an imported database

The instructions to grant access to objects in a share differ depending on whether the provider segmented the objects in a share using
database roles. This option associates different objects in the share with different database roles.

Note that a single share can include both objects that are accessible via database roles and objects that are not associated with a
database role.

### Option 1: Objects in a share aren’t associated with a database role

Allow users to access objects in a share by granting the IMPORTED PRIVILEGES privilege on an imported database to one or more roles in your
account.

A role can grant IMPORTED PRIVILEGES on an imported database only when it either:

- Owns the imported database (that is, has the OWNERSHIP privilege on the database).
- Was granted the MANAGE GRANTS global privilege.

#### Assigning IMPORTED PRIVILEGES to other roles

You can assign this role to other roles using either Snowsight or SQL:

SnowsightSQL

1. Select **Catalog** » **Database Explorer**.
2. Select the database that you want to grant privileges to.
3. In the **Privileges** section, select **+ Privileges**.
4. Select a role and privilege to grant to that role.
5. Select **Grant Privileges**.

Execute a [GRANT <privileges> … TO ROLE](/sql-reference/sql/grant-privilege) statement.

To see the roles that have USAGE privileges on an imported database, use Snowsight or the [SHOW GRANTS](/sql-reference/sql/show-grants) command.

#### SQL examples

1. Role `r1` creates database `snow_sales` from share `xy12345.sales_s`:

   Copy code

   ```
   use role r1;
   create database snow_sales from share xy12345.sales_s;
   ```
2. Role `r1` grants IMPORTED PRIVILEGES on database `snow_sales` to role `r2`:

   Copy code

   ```
   grant imported privileges on database snow_sales to role r2;
   ```
3. Since `r2` does not have the OWNERSHIP privilege on the database, to be able to perform either of the following grant or revoke
   operations, role `r2` must hold the MANAGE GRANTS privilege on the account:

   Copy code

   ```
   use role r2;
   grant imported privileges on database snow_sales to role r3;
   revoke imported privileges on database snow_sales from role r3;
   ```

### Option 2: Objects in a share associated with a database role

Allow users to access objects in a share by granting the appropriate database role in the imported database to one or more roles in your
account.

#### Step 1: Create a database from the share

Create a database from the share using [CREATE DATABASE … FROM SHARE](/sql-reference/sql/create-database).

Executing this command requires a role with the global CREATE DATABASE and IMPORT SHARE privileges.

For example, create databases `c1` from provider `provider1` and share `share1`:

Copy code

```
CREATE DATABASE c1 FROM SHARE provider1.share1;
```

#### Step 2: Grant database roles to your account-level roles

Grant database roles to roles in your account to allow users with those roles to access database objects in the share.

Use the role that you used to create the database from the share.

For example, see the database roles available, then grant database role `c1.r1` to the `analyst` role in your account:

Copy code

```
SHOW DATABASE ROLES in DATABASE c1;
GRANT DATABASE ROLE c1.r1 TO ROLE analyst;
```

## Creating streams on shared views or tables

Creating streams on shared objects (secure views or tables) enables you to track data manipulation language (DML) changes made in those
objects. This functionality is similar to creating and using streams on “local” objects (that is, in the same account as the stream).

The role used to execute the SQL statements in this section must have the required grants on the shared table or secure view. For information,
see [Granting privileges on an imported database](#label-granting-privileges-on-shared-database) (in this topic).

- To create streams on shared views:

  Copy code

  ```
  CREATE STREAM <name> ON VIEW <shared_db>.<schema>.<view>;
  ```

  For example, create a stream on the shared `aggregate_1_v` view in the `snow_sales.aggregates_eula` database and schema:

  Copy code

  ```
  CREATE STREAM aggregate_1_v_stream ON VIEW snow_sales.aggregates_eula.aggregate_1_v;
  ```
- To create streams on shared tables:

  Copy code

  ```
  CREATE STREAM <name> ON TABLE <shared_db>.<schema>.<table>;
  ```

  For example, create a table stream on the shared `aggregate_1` table in the `snow_sales.aggregates_eula` database and schema:

  Copy code

  ```
  CREATE STREAM aggregate_1_stream ON TABLE snow_sales.aggregates_eula.aggregate_1;
  ```

For more information on creating streams, see [CREATE STREAM](/sql-reference/sql/create-stream).

Note

- The data provider must enable change tracking on views or tables before you can create streams on these objects. If you cannot
  create streams on a desired shared object, contact the data provider to consider enabling change tracking on the object.
- To avoid allowing a stream to become stale, consume the stream records within a transaction during the retention period for the table.
  Contact the data provider to determine the data retention period for the table.

  To determine whether a stream has become stale, execute the [DESCRIBE STREAM](/sql-reference/sql/desc-stream) or [SHOW STREAMS](/sql-reference/sql/show-streams)
  command. In the command output, when the STALE column value is TRUE, the stream may be stale. In practice, reading from the stream may
  succeed for some time after the expected STALE\_AFTER. However, the stream may become stale at any time during this period.

## Querying an imported database

Querying an imported database is the same as querying any other database in your account.

For example:

> Copy code
>
> ```
> USE ROLE r1;
>
> USE DATABASE snow_sales;
>
> SELECT * FROM aggregates_1;
> ```
