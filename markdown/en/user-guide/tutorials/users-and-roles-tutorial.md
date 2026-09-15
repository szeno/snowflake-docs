# Create users and grant roles

## Introduction

This tutorial shows you how to create a user and grant a role to it by using SQL commands.
You can access a pre-loaded [Snowsight template](/user-guide/ui-snowsight/snowsight-templates)
worksheet to complete these tasks.

Note

Snowflake bills a minimal amount for the on-disk storage used for any sample data in
this tutorial. The tutorial provides steps to drop objects and minimize storage
cost. Snowflake requires a [virtual warehouse](/user-guide/warehouses) to load the
data and execute queries. A running virtual warehouse consumes Snowflake credits.

If you are using a [30-day trial account](https://signup.snowflake.com/),
which provides free credits, you won’t incur any costs.

### What you will learn

In this tutorial you will learn how to:

- Use a role that has the privileges to create and use the Snowflake objects required by this tutorial.
- Create a user.
- Grant a role to the user and grant access to a warehouse.
- Explore the users and roles in your account.
- Drop the user you created.

## Prerequisites

This tutorial assumes the following:

- You have a [supported browser](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-supported-browsers).
- You have access to a Snowflake account and can log in as a user who has been granted
  the ACCOUNTADMIN, USERADMIN, and SECURITYADMIN
  [system-defined roles](/user-guide/security-access-control-overview#label-access-control-overview-roles-system).

  If you don’t have an account, you can sign up for a [free trial](https://signup.snowflake.com/)
  and choose any [Snowflake Cloud Region](/user-guide/intro-regions).

# Step 1. Sign in using Snowsight

To access Snowsight over the public Internet, do the following:

1. In a supported web browser, navigate to <https://app.snowflake.com>.
2. Provide your [account identifier](/user-guide/admin-account-identifier) or account URL.
   If you’ve previously signed in to Snowsight, you might see an account name that you can select.
3. Sign in using your Snowflake account credentials.

## Step 2. Open the SQL worksheet for adding a user and granting roles

You can use worksheets to write and run SQL commands on your database.
You can access a pre-loaded template worksheet for this tutorial.
The worksheet contains the SQL commands that you will run to set the role context,
create a user, and grant role privileges. Because it is a template worksheet, you
will be invited to enter your own values for certain SQL parameters.

For more information about worksheets, see [Getting started with worksheets](/user-guide/ui-snowsight-worksheets-gs).

To open the pre-loaded template worksheet, follow these steps:

1. In the navigation menu, select **Projects** » **Templates**.
2. Find and open **Create users in a SQL worksheet**.

   The beginning of your worksheet looks similar to the following image:

> ![SQL users worksheet, which contains the SQL commands for this tutorial, along with descriptive comments.](/static/images/screens/create-user-tutorial.png)

## Step 3. Set the role to use

The role you use determines the privileges you have. In this tutorial, use the
USERADMIN system role so that you can create and manage users and roles in your
account. For more information, see [Overview of Access Control](/user-guide/security-access-control-overview).

To set the role to use, do the following:

1. In the open worksheet, place your cursor in the [USE ROLE](/sql-reference/sql/use-role) line.

   Copy code

   ```
   USE ROLE USERADMIN;
   ```
2. At the top of the worksheet, select **Run**.

   Note

   In this tutorial, run SQL statements one at a time. Don’t select **Run all**.

## Step 4. Create a user

A Snowflake user has login credentials. When a user is granted a role, the user can
perform all the operations that the role allows, through the privileges that were
granted to the role. For more information, see [User management](/user-guide/admin-user-management).

In this step of the tutorial, you create a user with a name, a password, and some
other properties.

In the open worksheet, place your cursor in the [CREATE USER](/sql-reference/sql/create-user) line,
insert a username and other parameter values of your choice (an example is shown below), and
select **Run**.

For MUST\_CHANGE\_PASSWORD, set the value to `true`, which ensures that a password
reset is requested on first login. For DEFAULT\_WAREHOUSE, use `COMPUTE_WH`.

Copy code

```
CREATE OR REPLACE USER snowman
PASSWORD = 'sn0wf@ll'
LOGIN_NAME = 'snowstorm'
FIRST_NAME = 'Snow'
LAST_NAME = 'Storm'
EMAIL = 'snow.storm@snowflake.com'
MUST_CHANGE_PASSWORD = true
DEFAULT_WAREHOUSE = COMPUTE_WH;
```

This command returns the following output:

> ```
> User SNOWMAN successfully created.
> ```

If you were creating a real user in a real Snowflake account, you would now send the
following information in a secure manner to the person who would need to access
this new account:

- Snowflake Account URL: The Snowflake account link where the user will log in.
  You can find this link at the top of your browser
  (for example: <https://app.snowflake.com/myorg/myaccount/>,
  where `myorg` is the Snowflake organization ID, and `myaccount` is the account ID).
- LOGIN\_NAME, as specified in the CREATE USER command.
- PASSWORD, as specified in the CREATE USER command.

## Step 5. Grant a system role and warehouse access to the user

Now that you have created a user, you can use the SECURITYADMIN role to grant the
SYSADMIN role to the user, and grant USAGE on the COMPUTE\_WH warehouse.

Granting a role to another role creates a parent-child relationship between the roles
(also referred to as a role hierarchy). Granting a role to a user enables the user to perform
all operations allowed by the role (through the access privileges granted to the role).

The SYSADMIN role has privileges to create warehouses, databases, and database objects
in an account and grant those privileges to other roles. Only grant this role to users who should
have these privileges. For more information about other system-defined roles, see
[Overview of Access Control](/user-guide/security-access-control-overview).

To grant the user access to a role and a warehouse, do the following:

1. In the open worksheet, place your cursor in the [USE ROLE](/sql-reference/sql/use-role) line,
   then select **Run**.

   Copy code

   ```
   USE ROLE SECURITYADMIN;
   ```
2. Place your cursor in the [GRANT ROLE](/sql-reference/sql/grant-role) line, enter the name of the user you created,
   then select **Run**.

   Copy code

   ```
   GRANT ROLE SYSADMIN TO USER snowman;
   ```
3. Place your cursor in the GRANT USAGE line, then select **Run**.

   Copy code

   ```
   GRANT USAGE ON WAREHOUSE COMPUTE_WH TO ROLE SYSADMIN;
   ```

## Step 6. Explore the users and roles in your account

Now you can explore all the users and roles in your account by using the ACCOUNTADMIN role.

To explore users and roles, do the following:

1. In the open worksheet, place your cursor in the [USE ROLE](/sql-reference/sql/use-role) line,
   then select **Run**.

   Copy code

   ```
   USE ROLE ACCOUNTADMIN;
   ```
2. Place your cursor in the [SHOW USERS](/sql-reference/sql/show-users) line, then select **Run**.

   Copy code

   ```
   SHOW USERS;
   ```

   Your output looks similar to the following image:

   ![Show all the users in the account. Table output with the following columns: name, created_on, login_name, display_name, first_name.](/static/images/screens/create-user-tutorial-show-users.png)
3. Place your cursor in the [SHOW ROLES](/sql-reference/sql/show-roles) line, then select **Run**.

   Copy code

   ```
   SHOW ROLES;
   ```

   Your output looks similar to the following image:

   ![Show all the roles in the account. Table output with the following columns: created_on, name, is_default, is_current, is_inherited.](/static/images/screens/create-user-tutorial-show-roles.png)

## Step 7. Drop the user and review key points

Congratulations! You have successfully completed this tutorial.
Take a few minutes to review the key points that were covered.
Learn more by reviewing other topics in the Snowflake Documentation.

### Drop the user

Assuming that it is no longer needed, you can now drop the user you created.

In the open worksheet, place your cursor in the [DROP USER](/sql-reference/sql/drop-user) line,
enter the name of the user you created, then select **Run**.

Copy code

```
DROP USER snowman;
```

### Review key points

In summary, you used a pre-loaded worksheet in Snowsight to complete the following steps:

1. Set the role to use.
2. Create a new user.
3. Grant the user role privileges and access to a warehouse.
4. Explore the users and roles in the account.
5. Drop the user you created.

Here are some key points to remember about users and roles:

- You need the required permissions to create and manage objects in your account. In this tutorial,
  you used the USERADMIN, SECURITYADMIN, SYSADMIN, and ACCOUNTADMIN system roles for different purposes.
- The ACCOUNTADMIN role isn’t normally used to create objects. Instead, we recommend creating a
  hierarchy of roles aligned with business functions in your organization. For more information, see
  [Using the ACCOUNTADMIN Role](/user-guide/security-access-control-considerations#label-security-accountadmin-role).
- A warehouse provides the compute resources that you need to execute DML operations, load data,
  and run queries. This tutorial uses the `compute_wh` warehouse that is included with your account.

### What’s next?

Continue learning about Snowflake using the following resources:

- Complete the other tutorials provided by Snowflake:

  - [Tutorials to get started with Snowflake](/learn-tutorials)
- Familiarize yourself with key Snowflake concepts and features, and the SQL commands used to
  create users and grant role privileges:

  - [Get started with Snowflake for users](/getting-started-for-users)
  - [User, role, & privilege commands](/sql-reference/commands-user-role)
- Try the Tasty Bytes Quickstarts provided by Snowflake:

  - [Tasty Bytes Quickstarts](https://www.snowflake.com/en/developers/guides/?searchTerm=tasty+bytes)
