# Use secure objects to control data access

Provider sharing not enabled for all accounts

Provider sharing is enabled by default for most, but not all accounts.

If you encounter errors when attempting to share data with consumers, the feature may not be enabled for your account. To inquire about
enabling it, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

To ensure sensitive data in a shared database is not exposed to users in consumer accounts, Snowflake strongly recommends sharing
[secure views](/user-guide/views-secure) and/or [secure UDFs](/developer-guide/secure-udf-procedure) instead of directly
sharing tables.

In addition, for optimal performance, especially when sharing data in extremely large tables, we recommend defining
[clustering keys](/user-guide/tables-clustering-keys#label-clustering-keys) on the base table(s) for your secure objects.

This topic describes using clustering keys in base tables for shared secure objects and provides step-by-step instructions for sharing
a secure view with a consumer account. It provides sample scripts for both data providers and consumers.

Note

The instructions for sharing a secure object are essentially the same as sharing a table, with the addition of the following objects:

- A “private” schema containing the base table and a “public” schema containing the secure object. Only the public schema and secure
  object are shared.
- A “mapping table” (also in the “private” schema), which is only required if you wish to share the data in the base table with multiple
  consumer accounts and share specific rows in the table with specific accounts.

## Using clustering keys for shared data

On very large (i.e. multi-terabyte) tables, clustering keys provide significant query performance benefits. By defining one or more
clustering keys on the base tables used in shared secure views or secure UDFs, you ensure users in your consumer accounts are not negatively
impacted when using these objects.

When choosing the columns to use as the clustering key for a table, please note some
[important considerations](/user-guide/tables-clustering-keys#label-clustering-keys-strategies).

## Sample setup and tasks

These sample instructions assume a database named `mydb` exists in the data provider account and has two schemas, `private`
and `public`. If the database and schemas do not exist, you should create them before proceeding.

### Step 1: Create data and mapping tables in private schema

Create the following two tables in the `mydb.private` schema and populate them with data:

`sensitive_data` — contains the data to share, and an `access_id` column for controlling data access by account.
`sharing_access` — uses the `access_id` column to map the shared data and the accounts that can access the data.

### Step 2: Create secure view in public schema

Create the following secure view in the `mydb.public` schema:

`paid_sensitive_data` — displays data based on account.

Note that the `access_id` column from the base table (`sensitive_data`) does not need to be included in the view.

### Step 3: Validate tables and secure view

Validate the tables and secure view to ensure the data is filtered properly by account.

To enable validating secure views that will be shared with other accounts, Snowflake provides a session parameter,
[SIMULATED\_DATA\_SHARING\_CONSUMER](/sql-reference/parameters#label-simulated-data-sharing-consumer). Set this session parameter to the name of the consumer account you wish to simulate
access for. You can then query the view and see the results that a user in the consumer account will see.

### Step 4: Create a share

1. Create a [share](/user-guide/data-sharing-provider#label-share-create).

   To create a share, you must use the ACCOUNTADMIN role or a role granted the global CREATE SHARE privilege.
   The role must also have one of the following to grant objects to the share:

   - A role with the OWNERSHIP privilege on the shared database.
   - A role with the [USAGE privilege on the database WITH GRANT OPTION](/sql-reference/sql/grant-privilege). For example:

     Copy code

     ```
     GRANT USAGE ON <database-name> TO ROLE <role-name> WITH GRANT OPTION;
     ```
2. Add the database (`mydb`), schema (`public`), and secure view (`paid_sensitive_data`) to the share. You can choose
   to either add privileges on these objects to a share via a database role, or grant privileges on the objects directly to the
   share. For more information on these options, see [How to share database objects](/user-guide/data-sharing-gs#label-data-sharing-share-options).
3. Confirm the contents of the share. At the most basic level, you should use the [SHOW GRANTS](/sql-reference/sql/show-grants) command to confirm
   the objects in the share have the necessary privileges.

   Note that the secure view `paid_sensitive_data` is displayed in the command output as a table.
4. Add one or more accounts to the share.

## Sample script

The following script illustrates performing all the tasks described in the previous section:

1. Create two tables in the ‘private’ schema and populate the first one with stock data from three different companies (Apple, Microsoft,
   and IBM). You will then populate the second one with data that maps the stock data to individual accounts:

   Copy code

   ```
   use role sysadmin;

   create or replace table mydb.private.sensitive_data (
    name string,
    date date,
    time time(9),
    bid_price float,
    ask_price float,
    bid_size int,
    ask_size int,
    access_id string /* granularity for access */ )
    cluster by (date);

   insert into mydb.private.sensitive_data
    values('AAPL',dateadd(day,  -1,current_date()), '10:00:00', 116.5, 116.6, 10, 10, 'STOCK_GROUP_1'),
          ('AAPL',dateadd(month,-2,current_date()), '10:00:00', 116.5, 116.6, 10, 10, 'STOCK_GROUP_1'),
          ('MSFT',dateadd(day,  -1,current_date()), '10:00:00',  58.0,  58.9, 20, 25, 'STOCK_GROUP_1'),
          ('MSFT',dateadd(month,-2,current_date()), '10:00:00',  58.0,  58.9, 20, 25, 'STOCK_GROUP_1'),
          ('IBM', dateadd(day,  -1,current_date()), '11:00:00', 175.2, 175.4, 30, 15, 'STOCK_GROUP_2'),
          ('IBM', dateadd(month,-2,current_date()), '11:00:00', 175.2, 175.4, 30, 15, 'STOCK_GROUP_2');

   create or replace table mydb.private.sharing_access (
     access_id string,
     snowflake_account string
   );

   /* In the first insert, CURRENT_ACCOUNT() gives your account access to the AAPL and MSFT data.       */

   insert into mydb.private.sharing_access values('STOCK_GROUP_1', CURRENT_ACCOUNT());

   /* In the second insert, replace <consumer_account> with an account name; this account will have     */
   /* access to IBM data only. Note that account names are case-sensitive and must be in uppercase      */
   /* enclosed in single-quotes, e.g.                                                                   */
   /*                                                                                                   */
   /*      insert into mydb.private.sharing_access values('STOCK_GROUP_2', 'ACCT1')                */
   /*                                                                                                   */
   /* To share the IBM data with multiple accounts, repeat the second insert for each account.          */

   insert into mydb.private.sharing_access values('STOCK_GROUP_2', '<consumer_account>');
   ```
2. Create a secure view in the ‘public’ schema. This view filters the stock data from the first table by account, using the mapping
   information in the second table:

   Copy code

   ```
   create or replace secure view mydb.public.paid_sensitive_data as
    select name, date, time, bid_price, ask_price, bid_size, ask_size
    from mydb.private.sensitive_data sd
    join mydb.private.sharing_access sa on sd.access_id = sa.access_id
    and sa.snowflake_account = current_account();

   grant select on mydb.public.paid_sensitive_data to public;

   /* Test the table and secure view by first querying the data as the provider account. */

   select count(*) from mydb.private.sensitive_data;

   select * from mydb.private.sensitive_data;

   select count(*) from mydb.public.paid_sensitive_data;

   select * from mydb.public.paid_sensitive_data;

   select * from mydb.public.paid_sensitive_data where name = 'AAPL';

   /* Next, test the secure view by querying the data as a simulated consumer account. You specify the  */
   /* account to simulate using the SIMULATED_DATA_SHARING_CONSUMER session parameter.                  */
   /*                                                                                                   */
   /* In the ALTER command, replace <consumer_account> with one of the accounts you specified in the    */
   /* mapping table. Note that the account name is not case-sensitive and does not need to be enclosed  */
   /* in single-quotes, e.g.                                                                            */
   /*                                                                                                   */
   /*      alter session set simulated_data_sharing_consumer=acct1;                                     */

   alter session set simulated_data_sharing_consumer=<account_name>;

   select * from mydb.public.paid_sensitive_data;
   ```
3. Create a share using the ACCOUNTADMIN role.

   Copy code

   ```
   use role accountadmin;

   create or replace share mydb_shared
     comment = 'Example of using Secure Data Sharing with secure views';

   show shares;
   ```
4. Add the objects to the share. You can choose to either add privileges on these objects to a share via a database role
   (Option 1), or grant privileges on the objects directly to the share (Option 2):

   Copy code

   ```
   /* Option 1: Create a database role, grant privileges on the objects to the database role, and then grant the database role to the share */

   create database role mydb.dr1;

   grant usage on database mydb to database role mydb.dr1;

   grant usage on schema mydb.public to database role mydb.dr1;

   grant select on mydb.public.paid_sensitive_data to database role mydb.dr1;

   grant usage on database mydb to share mydb_shared;

   grant database role mydb.dr1 to share mydb_shared;

   /* Option 2: Grant privileges on the database objects to include in the share.  */

   grant usage on database mydb to share mydb_shared;

   grant usage on schema mydb.public to share mydb_shared;

   grant select on mydb.public.paid_sensitive_data to share mydb_shared;

   /*  Confirm the contents of the share. */

   show grants to share mydb_shared;
   ```
5. Add accounts to the share.

   Copy code

   ```
   /* In the alter statement, replace <consumer_accounts> with the  */
   /* consumer account(s) you assigned to STOCK_GROUP2 earlier,     */
   /* with each account name separated by commas, e.g.              */
   /*                                                               */
   /*    alter share mydb_shared set accounts = acct1, acct2;       */

   alter share mydb_shared set accounts = <consumer_accounts>;
   ```

## Sample script (for consumers)

The following script can be used by consumers to create a database (from the share created in the above script) and query the secure view
in the resulting database:

1. Bring the shared database into your account by creating a database from the share.

   Copy code

   ```
   /* In the following commands, the share name must be fully qualified by replacing     */
   /* <provider_account> with the name of the account that provided the share, e.g.      */
   /*                                                                                    */
   /*    desc prvdr1.mydb_shared;                                                        */

   use role accountadmin;

   show shares;

   desc share <provider_account>.mydb_shared;

   create database mydb_shared1 from share <provider_account>.mydb_shared;
   ```
2. Grant privileges on the database to other roles in your account (e.g. CUSTOM\_ROLE1). The GRANT statement differs depending on whether
   the data consumer added objects to the share using database roles (Option 1) or by granting privileges on the objects directly to the
   share (Option 2):

   Copy code

   ```
   /* Option 1 */
   grant database role mydb_shared1.db1 to role custom_role1;

   /* Option 2 */
   grant imported privileges on database mydb_shared1 to custom_role1;
   ```
3. Use the CUSTOM\_ROLE1 role to query the view in the database you created. Note that there must be an active warehouse in use in the
   session to perform queries. In the USE WAREHOUSE command, replace <warehouse\_name> with the name of one of the warehouses in your
   account. The CUSTOM\_ROLE1 role must have the USAGE privilege on the warehouse:

   Copy code

   ```
   use role custom_role1;

   show views;

   use warehouse <warehouse_name>;

   select * from paid_sensitive_data;
   ```
