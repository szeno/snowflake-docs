# Share data protected by a policy

Data sharing consumers can use a shared database role to access shared data protected by a masking policy or a row access policy.

## Overview

A data sharing provider can share a database role to enable a data sharing consumer to access policy protected data. The provider defines
the policy to call the [IS\_DATABASE\_ROLE\_IN\_SESSION](/sql-reference/functions/is_database_role_in_session) function to evaluate the shared database role or
a mapping table column that contains the database role. This provides more options to the provider to share data and allows the consumer to
access sensitive data that the provider makes available.

When the policies and protected tables are in different databases, the provider must:

- Create the database role in the same database as the protected table.
- Grant the database role to the share containing the protected table.
- Share the database that contains the protected table to the consumer account.

When the consumer creates a database from the share, the database roles in the share are granted to the role that creates the database from
the share. This allows the account role in the consumer account to meet the policy conditions that specify the database role and access the
shared data.

To access the shared data protected by the policy, the consumer must specify the database containing the shared database role to make the
shared database role active in the current session. In this context, making the database role active means that the database role is
available in the role hierarchy of the current role for the user. If you do not specify this shared database, users in the consumer account
cannot access shared data that is protected by a policy. You can specify this database using either of the following options:

- Activate the database in the session with the [USE <object>](/sql-reference/sql/use) command or select the database in the worksheet. For example:

  Copy code

  ```
  USE DATABASE mounted_db;
  ```

  Where `mounted_db` is the name of the database the consumer creates from the share.
- For a specific query, use the fully qualified name of the object that is in the same database as the database role. For example:

  Copy code

  ```
  SELECT * FROM mounted_db.myschema.mytable;
  ```

### Call the function

There are two different ways to specify arguments in the IS\_DATABASE\_ROLE\_IN\_SESSION function: a string literal or a nonliteral
(that is, column name).

- When you specify a database role as a string in the IS\_DATABASE\_ROLE\_IN\_SESSION function, the result of calling the
  function depends on how the function is called. For example:

  - In a worksheet, Snowflake looks at the database that is in use for the session or the database that is specified in the query. This
    applies to both the provider account and the consumer account.
  - With a policy, UDF, or view, Snowflake looks at the database that contains the protected object. When these objects are not
    shared and the database role is defined in a different database, the function evaluates to `False`.
- When you specify a column name as the argument in the IS\_DATABASE\_ROLE\_IN\_SESSION function:

  - If a table query calls the function, the column maps to the table identifier of the table containing the column. Snowflake then looks
    at the database roles in the database containing the table. For example, to specify the AUTHZ\_ROLE (that is, authorized role) column as the
    argument:

    Copy code

    ```
    SELECT * FROM mydb.myschema.t WHERE IS_DATABASE_ROLE_IN_SESSION(AUTHZ_ROLE);
    ```
  - If a masking policy, row access policy, or UDF calls the function, the lookup occurs in the database that contains the protected table.

## General workflow

Sharing policy-protected data with the IS\_DATABASE\_ROLE\_IN\_SESSION function in the policy requires the same steps to create a policy to
call the function and share data. To summarize:

1. The provider creates an account role.
2. The provider creates a policy and sets the policy on a table or column.
3. The provider tests the policy with the account role.
4. The provider creates a database role and tests the policy with the database role.
5. The provider creates a share and grants privileges to the share, including granting the database role to the share.
6. The consumer creates a database from the share (the *mounted database*).
7. The consumer queries the shared object that is protected by the policy.

## Example: All objects in the same database

In this example, the database roles, masking policy, and the protected table are all in the same database named `mydb`.

For reference:

- The database roles are `analyst_dbrole` and `support_dbrole`.
- The masking policy is defined as follows:

  Copy code

  ```
  CREATE OR REPLACE MASKING POLICY mydb.policies.email_mask
    AS (val string) RETURNS string ->
    CASE
   WHEN IS_DATABASE_ROLE_IN_SESSION('ANALYST_DBROLE')
     THEN val
   WHEN IS_DATABASE_ROLE_IN_SESSION('SUPPORT_DBROLE')
     THEN REGEXP_REPLACE(val,'.+\@','*****@')
   ELSE '********'
    END
    COMMENT = 'use database role for shared data'
    ;
  ```
- The EMAIL column is in a table named `mydb.tables.empl_info` and the masking policy is set on this column.

Complete the following steps to share the database `mydb` and allow the consumer to use the shared database role to query the shared data
protected by the shared masking policy. These steps assume the provider has already tested the masking policy on the EMAIL column with
their account roles and database roles.

1. In the provider account, execute the [CREATE SHARE](/sql-reference/sql/create-share) command to create a share for the analyst database role:

   Copy code

   ```
   USE ROLE r1;
   CREATE SHARE analyst_share;
   ```
2. Grant privileges to the share. The same privileges are required for each share:

   Copy code

   ```
   USE ROLE r1;
   GRANT USAGE ON DATABASE mydb TO SHARE analyst_share;
   GRANT USAGE ON SCHEMA mydb.tables TO SHARE analyst_share;
   GRANT SELECT ON TABLE mydb.tables.empl_info TO SHARE analyst_share;
   GRANT DATABASE ROLE analyst_dbrole TO SHARE analyst_share;
   ```
3. Add the consumer account to the share:

   Copy code

   ```
   ALTER SHARE analyst_share ADD ACCOUNTS = consumer_account;
   ```
4. In the consumer account, create the account role `r1` and grant privileges to this role to import the share:

   Copy code

   ```
   USE ROLE ACCOUNTADMIN;
   CREATE ROLE r1;

   GRANT USAGE ON WAREHOUSE my_warehouse TO ROLE r1;
   GRANT CREATE DATABASE ON ACCOUNT TO ROLE r1;
   GRANT IMPORT SHARE ON ACCOUNT TO ROLE r1;
   GRANT ROLE r1 TO ROLE ACCOUNTADMIN;
   ```
5. Import the share:

   Copy code

   ```
   USE ROLE r1;
   CREATE DATABASE mounted_db FROM SHARE provider_account.analyst_share;
   ```
6. Verify the database role is in session:

   Copy code

   ```
   USE DATABASE mounted_db;
   USE SCHEMA mounted_db.tables;

   SELECT IS_DATABASE_ROLE_IN_SESSION('ANALYST_DBROLE');
   ```

   The SELECT statement should return `True`.
7. Query the protected table:

   Copy code

   ```
   SELECT * FROM empl_info;
   ```

   The SELECT statement should return the unmasked email addresses.
8. Grant the database roles to account roles so that users with these roles can query the protected table and view data based on the
   masking policy definition.

   After repeating the previous two steps, a user that is granted the `support_dbrole` database role should see a partially masked email
   address.

## Example: Masking policy and protected data in different databases

When the policy and the protected table are in different databases, share the database that contains the protected table with the consumer.

For example:

- `mydb1` contains the masking policy.
- `mydb2` contains the table named `mydb2.tables.empl_info`, which contains the EMAIL column. The masking policy is set on this column.

  You must group the table and the database role, `analyst_dbrole`, in the same database.

The provider follows the same procedure as the previous example in terms of creating a share, granting privileges to the share, and
granting the database role to the share.

The consumer follows the same procedure as the previous example in terms of creating a database from the share. However, the consumer must
have the database containing the protected table in use to activate the database role. Then the consumer can query the protected table by
specifying the fully qualified name of the table.

1. In the provider account, execute the [CREATE SHARE](/sql-reference/sql/create-share) command to create a share for each database:

   Copy code

   ```
   USE ROLE r1;
   CREATE SHARE analyst_policy_share;
   CREATE SHARE analyst_table_share;
   ```
2. Grant privileges to the share named `analyst_table_share`:

   Copy code

   ```
   USE ROLE r1;
   GRANT USAGE ON SCHEMA mydb2.tables TO SHARE analyst_table_share;
   GRANT SELECT ON TABLE mydb2.tables.empl_info TO SHARE analyst_table_share;
   GRANT DATABASE ROLE mydb2.analyst_dbrole TO SHARE analyst_table_share;
   ```
3. Add the consumer account to the share:

   Copy code

   ```
   ALTER SHARE analyst_table_share ADD ACCOUNTS = consumer_account;
   ```
4. In the consumer account, create the account role `r1` and grant privileges to this role to import the share:

   Copy code

   ```
   USE ROLE ACCOUNTADMIN;
   CREATE ROLE r1;

   GRANT USAGE ON WAREHOUSE my_warehouse TO ROLE r1;
   GRANT CREATE DATABASE ON ACCOUNT TO ROLE r1;
   GRANT IMPORT SHARE ON ACCOUNT TO ROLE r1;
   GRANT ROLE r1 TO ROLE ACCOUNTADMIN;
   ```
5. Import the share that contains the protected table and the database role:

   Copy code

   ```
   USE ROLE r1;
   CREATE DATABASE mounted_db2 FROM SHARE provider_account.analyst_table_share;
   ```
6. Verify the database role is in session:

   Copy code

   ```
   USE DATABASE mounted_db2;
   USE SCHEMA mounted_db2.tables;

   SELECT IS_DATABASE_ROLE_IN_SESSION('ANALYST_DBROLE');
   ```

   The SELECT statement should return `True`.
7. Query the protected table:

   Copy code

   ```
   SELECT * FROM mounted_db2.tables.empl_info;
   ```

   The SELECT statement should return the unmasked email addresses.

## Example: Row access policy without mapping table

In this example, the row access policy calls the IS\_DATABASE\_ROLE\_IN\_SESSION function to lookup the role name in the `authz_role`
(authorized role) column. The nonliteral syntax and that function lookup occurs in the database that contains the protected table.

Create the policy:

> Copy code
>
> ```
> CREATE OR REPLACE ROW ACCESS POLICY rap_authz_role AS (authz_role string)
> RETURNS boolean ->
> IS_DATABASE_ROLE_IN_SESSION(authz_role);
> ```

Add the policy to a table:

> Copy code
>
> ```
> ALTER TABLE allowed_roles
>   ADD ROW ACCESS POLICY rap_authz_role ON (authz_role);
> ```

The provider can choose to share objects in a single database or in multiple databases as shown in the masking policy examples. The
consumer follows the same procedure to create a database from a share for each database that the provider makes available.

## Example: Row access policy with mapping table

In this example, the row access policy calls the IS\_DATABASE\_ROLE\_IN\_SESSION function to look up the authorized role from a mapping table
column called `role_name`. The nonliteral syntax and that function lookup occurs in the database that contains the protected
table. In this scenario, the mapping table must be in the same database as the protected table. After creating the policy, add the policy
to the table containing the `authz_role` column.

> Create the policy:
>
> > Copy code
> >
> > ```
> > CREATE OR REPLACE ROW ACCESS POLICY rap_authz_role_map AS (authz_role string)
> > RETURNS boolean ->
> > EXISTS (
> >   SELECT 1 FROM mapping_table m
> >   WHERE authz_role = m.key AND IS_DATABASE_ROLE_IN_SESSION(m.role_name)
> > );
> > ```
>
> Add the policy to a table:
>
> > Copy code
> >
> > ```
> > ALTER TABLE allowed_roles
> >   ADD ROW ACCESS POLICY rap_authz_role_map ON (authz_role);
> > ```

The provider can choose to share objects in a single database or in multiple databases as shown in the masking policy examples. The
consumer follows the same procedure to create a database from a share for each database that the provider makes available.
