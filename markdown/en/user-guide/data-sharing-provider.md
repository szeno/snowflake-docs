# Create and configure shares

Provider sharing not enabled for all accounts

Provider sharing is enabled by default for most, but not all, accounts.

If you encounter errors when attempting to share data with consumers, the feature may not be enabled for your account.
To inquire about enabling it, contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

This topic describes the tasks associated with a data provider account creating and configuring shares, sharing the shares with other
consumer accounts, and performing ongoing maintenance of the shares.

Attention

Snowflake is not responsible for ensuring that HIPAA (and HITRUST) accounts who engage in data sharing have a signed BAA with each other;
this is at the discretion of the accounts that are sharing data. Failure to have a signed BAA might impact the HIPAA (and HITRUST)
compliance of both accounts, particularly the provider account.

If you have a Business Critical account, consider the following to maintain the expected level of data protection before requesting
Snowflake to enable Secure Data Sharing with non-Business Critical accounts:

- Do not share sensitive data with non-Business Critical accounts.
- Consider creating a non-Business Critical account to store less sensitive data and then sharing this data with non-Business
  Critical accounts.

- If you are using [Tri-Secret Secure](/user-guide/security-encryption-tss) with your Business Critical account and you share data with other accounts, Snowflake
  treats the data access from these accounts as if the access occurred from within your own account. Specifically, granting access to
  the consumer account may require Snowflake to access the key management service in the cloud platform that hosts your Snowflake account.

These are only recommendations and are not enforced by Snowflake. The decision to share data is always at the discretion of the data
provider. Snowflake does not assume any responsibility for data that is improperly shared.

## General data sharing considerations and usage

Note the following important usage details for creating and maintaining shares:

- You can share data across regions and cloud platforms. For more information,
  see [Share data securely across regions and cloud platforms](/user-guide/secure-data-sharing-across-regions-platforms).
- A share can include data from multiple databases. For more information, see [Share data from multiple databases](/user-guide/data-sharing-multiple-db).
- A share is available immediately to a consumer when you add that consumer’s account to the share.
- New and modified rows are available immediately to consumers who have created a database from the share.
  This only happens when the consumer already has access.
- A new object created or recreated in a database granted to a share is not automatically available to consumers. For example,
  if you drop and then recreate an object, it is still considered a new object, even if the name is the same.
  To make a new object available to consumers, you must use the [GRANT <privilege> … TO SHARE](/sql-reference/sql/grant-privilege-share) command to
  explicitly add the object to the share.
- For data security and privacy reasons, only [secure views](/user-guide/views-secure) are supported in shares at this time.
  If a standard view is added to a share, Snowflake returns an error.
- Creating secure views on streams in your database and then sharing those views with consumers is not recommended.
  This scenario requires the ability to modify a stream in another account, which is not a supported operation and is therefore
  an anti-pattern. Instead, allow consumers to create their own streams on the tables and secure views that you share.
  For more information, see [Streams on shared objects](#label-data-sharing-streams) (in this topic).
- [Storage lifecycle policies](/user-guide/storage-management/storage-lifecycle-policies) aren’t supported on shared tables. If you need to manage data retention
  for shared data, consider implementing retention logic in your application or using other data management strategies before sharing.
- A direct share is enabled for resharing within the consumer’s organization only.

## Using SQL with data shares

Preparing objects to share can be performed using any role. Other data sharing tasks, such as creating a share or adding consumer
accounts to the share, require the ACCOUNTADMIN role or a role granted the global CREATE SHARE privilege.
For more details about the CREATE SHARE privilege, see [Enable non-ACCOUNTADMIN roles to perform data sharing tasks](/user-guide/security-access-privileges-shares).

If you want to use DDL to create and manage database roles, use the commands listed here:

- [CREATE DATABASE ROLE](/sql-reference/sql/create-database-role)
- [ALTER DATABASE ROLE](/sql-reference/sql/alter-database-role)
- [DROP DATABASE ROLE](/sql-reference/sql/drop-database-role)
- [SHOW DATABASE ROLES](/sql-reference/sql/show-database-roles)
- A shared database role does not support future grants on objects. For details, see [GRANT DATABASE ROLE … TO SHARE](/sql-reference/sql/grant-database-role-share).

If you want to use DDL to view, grant, or revoke access to database objects in a share, use the commands listed here:

- [GRANT DATABASE ROLE … TO SHARE](/sql-reference/sql/grant-database-role-share)
- [REVOKE DATABASE ROLE … FROM SHARE](/sql-reference/sql/revoke-database-role-share)
- [GRANT <privilege> … TO SHARE](/sql-reference/sql/grant-privilege-share)
- [REVOKE <privilege> … FROM SHARE](/sql-reference/sql/revoke-privilege-share)
- [SHOW GRANTS TO SHARE …](/sql-reference/sql/show-grants) — lists all object privileges that have been granted to a share
- [SHOW GRANTS OF SHARE …](/sql-reference/sql/show-grants) — lists all accounts for the share and indicates the accounts
  that are using the share

## Preparing to create a share

Before creating a share, Snowflake recommends identifying the Snowflake objects you plan to share:

- Databases
- Tables
- Dynamic tables
- External tables
- Externally managed and managed Apache Iceberg™ tables
- Externally managed Delta Lake tables (with Delta Direct and catalog-linked databases)
- Views

  - Regular views
  - Secure views
  - Secure materialized views
  - Semantic views
- Cortex Search services
- User-defined functions (UDFs) (secure and non-secure)
- Models of type USER\_MODEL, CORTEX\_FINETUNED, or DOC\_AI

This might require some additional planning and administrative tasks, particularly if you decide to share only a subset of data in
any of your tables.

### Database and tables

If you plan to share a database, little or no preparation is required.

If you plan to share entire tables, no preparation is required.

However, if you decide to filter the data in a table (or set of tables), either based on certain conditions, or by consumer account,
you must create one or more secure views on the table(s).

### Secure objects (views, materialized views and UDFs)

To provide strict control of access to data in a shared database, you must
use [secure views](/user-guide/views-secure), [secure materialized views](/user-guide/views-materialized)
and/or [secure UDFs](/developer-guide/secure-udf-procedure). For example,
you can choose to filter data by date or some other condition, or you can decide to use a single share
to partition shared data for different consumer accounts. Secure objects enable you to dictate
the level of granularity you wish to apply to your data while ensuring that the base tables and
business logic are protected from exposure.

Secure objects are defined similarly to standard objects, using either the corresponding [CREATE <object>](/sql-reference/sql/create)
or [ALTER <object>](/sql-reference/sql/alter) commands. However, note the following important
usage information:

- Secure objects that reference tables by their fully-qualified names (that is, `<db_name>.<schema_name>.<table_name>`)
  can be included in a share; however, you must ensure that the referenced database
  name matches the database for the share.
- Do not include secure objects that use the [CURRENT\_USER](/sql-reference/functions/current_user)
  or [CURRENT\_ROLE](/sql-reference/functions/current_role) functions in their definition. The contextual values
  returned by these functions have no relevance in a consumer’s account and will cause the object to fail when queried/used.
- When defining a secure object to share with consumer accounts, a key/vital additional step to perform
  is validating that the object is configured correctly to display only the data you wish to display.
  This is particularly important if you wish to limit data access based on the account the data is shared with. To facilitate performing
  this validation, Snowflake provides the [SIMULATED\_DATA\_SHARING\_CONSUMER](/sql-reference/parameters#label-simulated-data-sharing-consumer) session parameter.
  The SIMULATED\_DATA\_SHARING\_CONSUMER session parameter only supports secure views and
  secure materialized views, but does not support secure UDFs. Setting this parameter in a session enables you to
  simulate querying a secure view as a user in any of the consumer account(s) you plan to share the view with.

  For example, for consumer account `xy12345`:

  Copy code

  ```
  ALTER SESSION SET SIMULATED_DATA_SHARING_CONSUMER = xy12345;
  ```

For a detailed example, see [Use secure objects to control data access](/user-guide/data-sharing-secure-views).

### Streams on shared objects

Data consumers can create streams in their own databases that record data manipulation language (DML) changes made to the source tables or
views.

Note

The operations listed here are not supported:

- Creating append-only streams on shares of secondary source objects is not supported.
- Modifying a stream in another account is not supported.

You can allow consumers to create streams on shared tables or secure views. Before you do this, you need to extend the data
retention period for the tables, and you also need to enable change tracking on the shared tables or the
underlying tables for a shared view. You set the CHANGE\_TRACKING and DATA\_RETENTION\_TIME\_IN\_DAYS parameters when
creating or altering a table, using
[CREATE TABLE](/sql-reference/sql/create-table) or [ALTER TABLE](/sql-reference/sql/alter-table).

Enable change tracking:
:   Currently, when the first stream for a local table is created, a pair of hidden columns is automatically added to the table and begins
    storing change tracking metadata. This change is not possible for shared tables, because a consumer of a share cannot modify the source
    database. Instead, to enable change tracking for tables intended for sharing, execute
    [ALTER TABLE](/sql-reference/sql/alter-table) … CHANGE\_TRACKING = TRUE on each of the tables.

Extend the data retention period for the table:
:   When a stream on a local table is not consumed regularly, Snowflake temporarily extends the data retention period for the source table
    to help avoid staleness.

    A stream on a shared table does not extend the data retention period for the table. Likewise, a stream on a shared view does not
    extend the data retention period for the underlying tables. To manually specify a longer data retention period
    for any shared table, or any underlying table for a shared view, set the [DATA\_RETENTION\_TIME\_IN\_DAYS](/sql-reference/parameters#label-data-retention-time-in-days) parameter for
    the table.

### Shared tag references

A data sharing provider can set a tag on an object and share both the tag and the tagged object with the data sharing consumer.
Additionally, the tag references of the shared object are available to the consumer. Sharing the tag references allows the provider to
share additional context regarding the shared object, such as the data sensitivity of a table or column based on the tag string value.

The consumer can use SQL to view the tag assignments on shared objects and determine the tag references of the shared objects. By viewing
the tag assignments and references of shared objects, data stewards in the consumer account can provide a more comprehensive assessment of
where data originates from and how the data is being used. These new insights can facilitate regulatory compliance requirements.

The provider must create the tag in the same database as the tagged objects and share this database. After sharing the database, if the
provider unsets a tag from a shared object, the change in tag assignment also occurs in the consumer account. The consumer cannot track the
shared object using the tag once that tag is unset. By unsetting the tag, the provider can maintain data discretion in cases when an object
was tagged inadvertently.

[Tag inheritance](/user-guide/object-tagging/inheritance#label-object-tagging-lineage) applies to tagged objects in the shared database. For example, if a provider sets a tag
on a schema in the shared database, the objects and columns in that schema are also tagged. However, the consumer cannot use the
Information Schema [TAG\_REFERENCES](/sql-reference/functions/tag_references) table function to determine where the provider initially set the tag.
Snowflake hides the values in the LEVEL column in the table function output to protect the data provider by not revealing where
the tag was initially set.

Important

Shared tags are read only. The consumer cannot set a shared tag on an object in their account.

Provider options
:   To share a tag, the provider has these options:

    - Use SQL to allow the share to access the tag and allow the consumer to view the assignments of the shared tag on the shared objects.

      The provider must grant the READ privilege on each tag to make the tag available to a consumer.

      Copy code

      ```
      GRANT READ ON TAG mydb.tags.tag1 TO SHARE my_share;

      GRANT USAGE ON DATABASE mydb TO SHARE my_share;
      GRANT USAGE ON SCHEMA mydb.tags TO SHARE my_share;
      ```
    - [Create a database role](/sql-reference/sql/create-database-role), grant the READ privilege on the tag to the database role, and
      [grant the database role to the share](/sql-reference/sql/grant-database-role-share). The database role also needs the USAGE
      privilege on the schema that stores the tag.

      Copy code

      ```
      GRANT READ ON TAG mydb.tags.tag1 TO DATABASE ROLE my_db_role;
      GRANT USAGE ON SCHEMA mydb.tags TO DATABASE ROLE my_db_role;
      GRANT DATABASE ROLE my_db_role TO SHARE my_share;
      ```

Consumer options
:   To view shared tags in the consumer account, the consumer has these options:

    - Use the ACCOUNTADMIN role. Consumer account administrators can view the shared tags the provider makes available.
    - Use a role with IMPORTED PRIVILEGES. An account role that is granted or inherits a role with IMPORTED PRIVILEGES on the database
      created from the share can view the shared tag the provider makes available.

      Copy code

      ```
      GRANT IMPORTED PRIVILEGES ON DATABASE db_share TO ROLE db_share_role;
      ```
    - Use a shared database role. If the provider grants the READ privilege on a tag to the database role and shares the database role, the
      consumer can grant the shared database role to an account role in their account.

      Copy code

      ```
      GRANT DATABASE ROLE my_db_role TO ROLE consumer_analyst_role;
      ```

    In the consumer account, you can use SQL to view tags, tag references, and tagged objects that the provider shares:

    - Command: [SHOW TAGS](/sql-reference/sql/show-tags)
    - Functions:
      - [SYSTEM$GET\_TAG](/sql-reference/functions/system_get_tag)
      - [TAG\_REFERENCES](/sql-reference/functions/tag_references)
      - [TAG\_REFERENCES\_ALL\_COLUMNS](/sql-reference/functions/tag_references_all_columns)

    Currently, you cannot use the following options in the consumer account to view tags, tag references, and tagged objects the provider
    shares:

    - Snowsight.
    - The Account Usage [TAG\_REFERENCES](/sql-reference/account-usage/tag_references) view.
    - The Account Usage [TAG\_REFERENCES\_WITH\_LINEAGE](/sql-reference/functions/tag_references_with_lineage) table function.

## Creating a share

You must use the ACCOUNTADMIN role or a role that has been granted the CREATE SHARE global privilege to create shares.

### Using Snowsight to create a share

There are several ways to share data in Snowsight:

> - Provide a listing to specific consumers or publicly on the Snowflake Marketplace using **Provider Studio**.
>   See [Create and publish a listing](/collaboration/provider-listings-creating-publishing).
> - Publish a listing in a [data exchange](/user-guide/data-exchange-managing-data-listings).
> - Create a direct share to share data with consumer accounts in your region.

If you are creating a share where you need to add a secure view that references objects in other databases,
you must create your share using SQL. For more information, see [Share data from multiple databases](/user-guide/data-sharing-multiple-db).

To create a direct share:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Data sharing** » **External sharing**.
3. Select the **Shared by your account** tab.
4. Select **Share** » **Create a Direct Share**.
5. In the Share Data dialog, select **+ Select Data** and then:
   1. Select a source database.
   2. Select a target object or objects from the source database.
   3. Optionally, update the **Secure Share Identifier** created for your share.
   4. Optionally, enter a **Description**.
   5. In the remaining text box, enter an account locator. Entering a partial account locator lists all accounts that match the entered text.
      Repeat as required to add additional accounts. You can only add accounts within the same region to the share.
   6. Select **Create Share**.

If you want to convert a direct share with active consumers to a listing, see [Convert a direct share to a listing](https://other-docs.snowflake.com/en/collaboration/provider-listings-creating-publishing#convert-a-direct-share-to-a-private-listing).

### Using SQL to create a share

To create a share using SQL:

1. Use the [CREATE SHARE](/sql-reference/sql/create-share) command to create an empty share.
2. Use the [GRANT <privilege> … TO SHARE](/sql-reference/sql/grant-privilege-share) command to add a database to the share and then selectively grant access to
   specific database objects (schemas, tables and secure views) to the share.
3. Use the [ALTER SHARE](/sql-reference/sql/alter-share) command to add one or more accounts access to the share.

Note

The following steps assume a provider account, `prvdr1`, is sharing data with two consumer accounts, `xy12345` and `yz23456`.

### Using DDL to create and manage shares

To create and manage shares, you use the DDL commands listed here:

- [CREATE SHARE](/sql-reference/sql/create-share)
- [ALTER SHARE](/sql-reference/sql/alter-share)
- [DROP SHARE](/sql-reference/sql/drop-share)
- [DESCRIBE SHARE](/sql-reference/sql/desc-share) — describes all the objects in a share
- [SHOW SHARES](/sql-reference/sql/show-shares) — lists all shares, as well as the consumer accounts specified for each share

#### Step 1: Create the empty share

The following example creates an empty share named `sales_s`:

> Copy code
>
> ```
> CREATE SHARE sales_s;
> ```

#### Step 2: Grant privileges for a database and objects to the share

Add objects (database, schema, tables, secure views, etc.) to the share. You can choose to either add privileges on these objects
to a share via a database role, or grant privileges on the objects directly to the share. For more information on these options, see
[How to share database objects](/user-guide/data-sharing-gs#label-data-sharing-share-options).

Option 1:
:   The following example illustrates creating a database role, granting privileges on the following objects to the database role, and then
    granting the database role to the `sales_s` share created in the previous step:

    > - `sales_db` (database)
    > - `aggregates_eula` (schema)
    > - `aggregate_1` (table)
    >
    > Copy code
    >
    > ```
    > CREATE DATABASE ROLE sales_db.dr1;
    >
    > GRANT USAGE ON DATABASE sales_db TO DATABASE ROLE sales_db.dr1;
    >
    > GRANT USAGE ON SCHEMA sales_db.aggregates_eula TO DATABASE ROLE sales_db.dr1;
    >
    > GRANT SELECT ON TABLE sales_db.aggregates_eula.aggregate_1 TO DATABASE ROLE sales_db.dr1;
    >
    > GRANT USAGE ON DATABASE sales_db TO SHARE sales_s;
    >
    > GRANT DATABASE ROLE sales_db.dr1 TO SHARE sales_s;
    > ```

Option 2:
:   To include objects in the share, grant privileges on each object. When granting privileges, first grant usage on any container
    objects before granting usage on the objects in the container. For example, grant usage on a database before granting usage on any
    schemas contained in the database.

    Note

    Perform this task before adding accounts to the share. Attempting to add an account before granting usage on a
    database results in an error.

    The following example illustrates granting privileges on the following objects to the `sales_s` share created in the previous step:

    > - `sales_db` (database)
    > - `aggregates_eula` (schema)
    > - `aggregate_1` (table)
    >
    > Copy code
    >
    > ```
    > GRANT USAGE ON DATABASE sales_db TO SHARE sales_s;
    >
    > GRANT USAGE ON SCHEMA sales_db.aggregates_eula TO SHARE sales_s;
    >
    > GRANT SELECT ON TABLE sales_db.aggregates_eula.aggregate_1 TO SHARE sales_s;
    > ```

To confirm the contents of the share:

> Copy code
>
> ```
> SHOW GRANTS TO SHARE sales_s;
>
> +-------------------------------+-----------+------------+--------------------------------------+------------+----------------+--------------+--------------+
> | created_on                    | privilege | granted_on | name                                 | granted_to | grantee_name   | grant_option | granted_by   |
> |-------------------------------+-----------+------------+--------------------------------------+------------+----------------+--------------+--------------|
> | 2017-06-15 16:45:07.307 -0700 | USAGE     | DATABASE   | SALES_DB                             | SHARE      | PRVDR1.SALES_S | false        | ACCOUNTADMIN |
> | 2017-06-15 16:45:10.310 -0700 | USAGE     | SCHEMA     | SALES_DB.AGGREGATES_EULA             | SHARE      | PRVDR1.SALES_S | false        | ACCOUNTADMIN |
> | 2017-06-15 16:45:12.312 -0700 | SELECT    | TABLE      | SALES_DB.AGGREGATES_EULA.AGGREGATE_1 | SHARE      | PRVDR1.SALES_S | false        | ACCOUNTADMIN |
> +-------------------------------+-----------+------------+--------------------------------------+------------+----------------+--------------+--------------+
> ```

This ensures that the share is correctly configured before making it available to other accounts to consume.

#### Step 3: Add accounts to the share

Attention

If you have a Business Critical account and are sharing data with consumer accounts:

- Snowflake supports sharing sensitive data with non-Business Critical accounts (disabled by default), but does not
  encourage doing so.
- To ensure compliance with HIPAA and HITRUST requirements, Snowflake does not allow HIPAA accounts to share data
  with non-HIPAA accounts.

- If you are using Tri-Secret Secure, Snowflake treats data access from consumer accounts as if the access occurred from within your
  own account.

The following example adds two accounts to the `sales_s` share:

> Copy code
>
> ```
> ALTER SHARE sales_s ADD ACCOUNTS=xy12345, yz23456;
> ```

Accounts `xy12345` and `yz23456` are now able to see the share and create a database from it.

> Note
>
> When adding accounts to a share, if the accounts do not exist, the command completes successfully,
> but no updates are made to the share. To ensure the share is properly updated, verify that the accounts
> exist and you’ve entered the names correctly.

Use [SHOW SHARES](/sql-reference/sql/show-shares) to confirm the share. The output of the command lists the `sales_s` share.
The `kind` column indicates that the share is OUTBOUND, meaning this share is sharing a database with other
Snowflake accounts. The `to` column lists all accounts to which the share has been made available:

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

## Maintaining shares

You must use a role with the OWNERSHIP privilege on a share and the CREATE SHARE global privilege to manage shares.

### Adding objects to a share

You can add objects to an existing share at any time. Objects that you add to a share are instantly available to the consumer
accounts that have created databases from the share. For example, if you add a table to a share, users in consumer accounts can query the
data in the table as soon as the table is added to the share.

Important

If you plan to securely share data with data consumers across different [regions](/user-guide/intro-regions) or
[cloud platforms](/user-guide/intro-cloud-platforms), note that replicating a primary database is blocked if the database
contains some types of objects. For a full list of objects that cause refresh operations to fail, see
[Current limitations of replication](/user-guide/account-replication-intro#label-replication-limitations).

#### Using Snowsight to add objects to a share

To modify the data associated with a share using Snowsight:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Data sharing** » **External sharing**.
3. Select the **Shared by your account** tab.
4. Locate and select the share you want to modify.
5. In the **Data** section, select **Edit**.
6. Select the data that you want to add.
7. Select **Done**.

Note

The web interface does not currently support adding or removing external tables, secure materialized views, or secure UDFs to/from
shares. All management of these objects in shares must be performed using SQL.

You cannot add a secure view that references objects in other databases to a share using the web interface. You must
create your share using SQL. See [Share data from multiple databases](/user-guide/data-sharing-multiple-db).

#### Using SQL to add objects to a share

Use the [GRANT <privilege> … TO SHARE](/sql-reference/sql/grant-privilege-share) command.

Note

- If the schema for the object is already in the share, you only need to add the object.
- If the schema for the object is not already in the share, you need to first add the schema and then the object.

The following example adds a secure view named `agg_secure` in the `aggregates_eula` schema to the `sales_s` share:

> Copy code
>
> ```
> SHOW GRANTS TO SHARE sales_s;
>
> +-------------------------------+-----------+------------+--------------------------------------+------------+----------------+--------------+--------------+
> | created_on                    | privilege | granted_on | name                                 | granted_to | grantee_name   | grant_option | granted_by   |
> |-------------------------------+-----------+------------+--------------------------------------+------------+----------------+--------------+--------------|
> | 2017-06-15 16:45:07.307 -0700 | USAGE     | DATABASE   | SALES_DB                             | SHARE      | PRVDR1.SALES_S | false        | ACCOUNTADMIN |
> | 2017-06-15 16:45:10.310 -0700 | USAGE     | SCHEMA     | SALES_DB.AGGREGATES_EULA             | SHARE      | PRVDR1.SALES_S | false        | ACCOUNTADMIN |
> | 2017-06-15 16:45:12.312 -0700 | SELECT    | TABLE      | SALES_DB.AGGREGATES_EULA.AGGREGATE_1 | SHARE      | PRVDR1.SALES_S | false        | ACCOUNTADMIN |
> +-------------------------------+-----------+------------+--------------------------------------+------------+----------------+--------------+--------------+
>
> GRANT SELECT ON VIEW sales_db.aggregates_eula.agg_secure TO SHARE sales_s;
>
> SHOW GRANTS TO SHARE sales_s;
>
> +-------------------------------+-----------+------------+--------------------------------------+------------+----------------+--------------+--------------+
> | created_on                    | privilege | granted_on | name                                 | granted_to | grantee_name   | grant_option | granted_by   |
> |-------------------------------+-----------+------------+--------------------------------------+------------+----------------+--------------+--------------|
> | 2017-06-15 16:45:07.307 -0700 | USAGE     | DATABASE   | SALES_DB                             | SHARE      | PRVDR1.SALES_S | false        | ACCOUNTADMIN |
> | 2017-06-15 16:45:10.310 -0700 | USAGE     | SCHEMA     | SALES_DB.AGGREGATES_EULA             | SHARE      | PRVDR1.SALES_S | false        | ACCOUNTADMIN |
> | 2017-06-15 16:45:12.312 -0700 | SELECT    | TABLE      | SALES_DB.AGGREGATES_EULA.AGGREGATE_1 | SHARE      | PRVDR1.SALES_S | false        | ACCOUNTADMIN |
> | 2017-06-17 12:33:15.310 -0700 | SELECT    | TABLE      | SALES_DB.AGGREGATES_EULA.AGG_SECURE  | SHARE      | PRVDR1.SALES_S | false        | ACCOUNTADMIN |
> +-------------------------------+-----------+------------+--------------------------------------+------------+----------------+--------------+--------------+
> ```

### Removing objects from a share

You can remove objects from an existing share at any time.
Any objects that you remove from a share are instantly unavailable to the consumer accounts who have created databases from the share.

For example, if you remove a table from a share, users in consumer accounts can no longer query the data in the table as soon as the table
is removed from the share.

Note

The web interface does not currently support adding or removing external tables, secure materialized views, or
secure UDFs to/from shares. All management of these objects in shares must be performed using SQL.

#### Using Snowsight to remove objects from a share

To remove the data associated with a share using Snowsight:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Data sharing** » **External sharing**.
3. Select the **Shared by your account** tab.
4. Locate and select the share you want to modify.
5. In the **Data** section, select **Edit**.
6. Select the data in the share and deselect the checkboxes for the data that you want to remove from the share.
7. Select **Done**.

#### Using SQL to remove objects from a share

Remove objects from an existing share at any time using the [REVOKE <privilege> … FROM SHARE](/sql-reference/sql/revoke-privilege-share) command.

The following example removes the secure view named `agg_secure` in the `aggregates_eula` schema from the `sales_s` share:

> Copy code
>
> ```
> SHOW GRANTS TO SHARE sales_s;
>
> +-------------------------------+-----------+------------+--------------------------------------+------------+----------------+--------------+--------------+
> | created_on                    | privilege | granted_on | name                                 | granted_to | grantee_name   | grant_option | granted_by   |
> |-------------------------------+-----------+------------+--------------------------------------+------------+----------------+--------------+--------------|
> | 2017-06-15 16:45:07.307 -0700 | USAGE     | DATABASE   | SALES_DB                             | SHARE      | PRVDR1.SALES_S | false        | ACCOUNTADMIN |
> | 2017-06-15 16:45:10.310 -0700 | USAGE     | SCHEMA     | SALES_DB.AGGREGATES_EULA             | SHARE      | PRVDR1.SALES_S | false        | ACCOUNTADMIN |
> | 2017-06-15 16:45:12.312 -0700 | SELECT    | TABLE      | SALES_DB.AGGREGATES_EULA.AGGREGATE_1 | SHARE      | PRVDR1.SALES_S | false        | ACCOUNTADMIN |
> | 2017-06-17 12:33:15.310 -0700 | SELECT    | TABLE      | SALES_DB.AGGREGATES_EULA.AGG_SECURE  | SHARE      | PRVDR1.SALES_S | false        | ACCOUNTADMIN |
> +-------------------------------+-----------+------------+--------------------------------------+------------+----------------+--------------+--------------+
>
> REVOKE SELECT ON VIEW sales_db.aggregates_eula.agg_secure FROM SHARE sales_s;
>
> +-------------------------------+-----------+------------+--------------------------------------+------------+----------------+--------------+--------------+
> | created_on                    | privilege | granted_on | name                                 | granted_to | grantee_name   | grant_option | granted_by   |
> |-------------------------------+-----------+------------+--------------------------------------+------------+----------------+--------------+--------------|
> | 2017-06-15 16:45:07.307 -0700 | USAGE     | DATABASE   | SALES_DB                             | SHARE      | PRVDR1.SALES_S | false        | ACCOUNTADMIN |
> | 2017-06-15 16:45:10.310 -0700 | USAGE     | SCHEMA     | SALES_DB.AGGREGATES_EULA             | SHARE      | PRVDR1.SALES_S | false        | ACCOUNTADMIN |
> | 2017-06-15 16:45:12.312 -0700 | SELECT    | TABLE      | SALES_DB.AGGREGATES_EULA.AGGREGATE_1 | SHARE      | PRVDR1.SALES_S | false        | ACCOUNTADMIN |
> +-------------------------------+-----------+------------+--------------------------------------+------------+----------------+--------------+--------------+
> ```

### Adding accounts to a share

You can add accounts to an existing share at any time. After an account is added to the share, the share is immediately “visible”
to the account and the account can create a database from the share and start querying the Snowflake objects in the database.

#### Using Snowsight to add accounts to a share

To add consumers to an existing share using Snowsight:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Data sharing** » **External sharing**.
3. Select the **Shared by your account** tab.
4. Locate the share you want to modify.
5. In the **Shared With** section, select **Add Consumers**.
6. For **Share With Snowflake Accounts**, enter one or more account locators. Entering part of an account locator lists all accounts that match.
7. Select **Add**.

#### Using SQL to add accounts to a share

To add consumers to an existing share using SQL, use the [ALTER SHARE](/sql-reference/sql/alter-share) command.

### Removing accounts from a share

You can remove accounts from an existing share at any time. Removing an account from a share instantly invalidates the database they
created from the share. All queries and other operations that users in the account perform on the database will no longer work.

After removing an account from a share, you can add it back again to the share; however, this does not restore the database
they created earlier from the share. They must create a new database from the share.

Note

Before removing an account from a share, consider the downstream impact it will have on the account.
Because the database is instantly invalidated, all queries and other operations that users (in the account)
perform on the database will stop working, which could have a significant impact on the business operations of the account.

#### Using Snowsight to remove accounts from a share

To remove consumers from an existing share using Snowsight:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Data sharing** » **External sharing**.
3. Select the **Shared by your account** tab.
4. Locate and select the share you want to modify.
5. In the **Shared With** section, select **…** » **Remove**.
6. In the confirmation dialog, select **Remove**.

#### Using SQL to remove accounts from a share

Remove accounts from an existing share using the [ALTER SHARE](/sql-reference/sql/alter-share) command.

You remove an account from a share by setting a new list of accounts for the share and leaving the desired account off the list.

### Dropping a share

You can drop (remove) a share at any time. Dropping a share instantly invalidates all databases created from the share by consumer accounts.
All queries and other operations performed on these databases no longer work.

After dropping a share, you can recreate it with the same name; however, this does not restore any of the databases created from the share
by consumer accounts. The recreated share is treated as a new share and all consumer accounts must create a new database from the new share.

Note

Before dropping a share, consider the downstream impact it will have on all consumer accounts using the share.

Instead, you might want to consider removing individual objects from the share. Removed objects can be added back to a share without
requiring any additional tasks on the part of the consumer accounts.

#### Using Snowsight to drop a share

To drop a share using Snowsight:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Data sharing** » **External sharing**.
3. Select the **Shared by your account** tab.
4. Locate and select the share you want to drop.
5. Select **…** » **Drop**.
6. In the confirmation dialog, select **Drop**.

#### Using SQL to drop a share

Drop a share using the [DROP SHARE](/sql-reference/sql/drop-share) command.

## Viewing consumers who have created databases from shares

To see the accounts that have created databases from a share, use the SHOW GRANTS OF SHARE command. The output from this command is
different from the list of accounts returned by SHOW SHARES in the following ways:

- SHOW SHARES lists all shares that are available to accounts, as well as the accounts that are able to access each share.
- SHOW GRANTS OF SHARE lists all accounts that have created a database from the share. If no accounts have created a database from the
  share, the results are empty.

For example, the following shows:

> - Two shares, `sales_s` and `sales_s2` have been made available to accounts `xy12345` and `yz23456`
>   by the owner account `SNOW.PRVDR1`.
> - Account `xy12345` has created a database from the `prvdr1.sales_s` share.
> - No accounts have created databases from the `sales_s2` share.
>
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
> | 2017-06-15 17:02:29.625 -0700 | OUTBOUND | SNOW.PRVDR1          | SALES_S       | SALES_DB              | XY12345, YZ23456 | ACCOUNTADMIN |                                        |
> | 2017-06-15 17:02:29.625 -0700 | OUTBOUND | SNOW.PRVDR1          | SALES_S2      | SALES_DB              | XY12345, YZ23456 | ACCOUNTADMIN |                                        |                     |
> +-------------------------------+----------+----------------------+---------------+-----------------------+------------------+--------------+----------------------------------------+---------------------+
> ```
>
> Copy code
>
> ```
> SHOW GRANTS OF SHARE sales_s;
> ```
>
> ```
> +-------------------------------+----------------+------------+----------+
> | created_on                    | share          | granted_to | account  |
> |-------------------------------+----------------+------------+----------|
> | 2017-06-15 18:00:03.803 -0700 | PRVDR1.SALES_S | ACCOUNT    | XY12345  |
> +-------------------------------+----------------+------------+----------+
> ```
>
> Copy code
>
> ```
> SHOW GRANTS OF SHARE sales_s2;
> ```
>
> ```
> +------------+-------+------------+---------+
> | created_on | share | granted_to | account |
> |------------+-------+------------+---------|
> +------------+-------+------------+---------+
> ```

## Viewing shares and data

Using Snowsight, you can view data that was shared by your account using a listing, a direct share, or as part of a data exchange.

To view the data shared by your account, do the following:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Data sharing** » **External sharing**.
3. Select the **Shared by your account** tab.

On this page, you can do the following:

- View the shares that you have created or have access privileges to. This includes information such as the database for the share,
  the consumer accounts, if any, added to the share, creation date of the share, and the shared objects.
- Explore shares associated with listings offered specifically to certain consumers or available to any consumer on the Snowflake Marketplace.
- Access shares that are shared within private data exchanges.

You can use the following filters to selectively display shared data:

- Filter by type with the **All Types** drop-down list. Choose to display only secure shares or listings shared within a data exchange.
  Some secure shares are shares associated with listings.
- Filter by consumer account or data exchange with the **Shared With** drop-down list. Select one or more specific consumers or data
  exchanges to see all shares or listings associated with your selection or selections.

## Managing shares and data

Select a share to manage the share, revoke access for individual consumer accounts, or add a description to the share.
To manage secure shares that are offered as listings, or to manage your listings on the Snowflake Marketplace, use **Provider Studio**.
