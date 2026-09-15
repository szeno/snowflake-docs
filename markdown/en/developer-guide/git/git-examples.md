# Examples of using Git with Snowflake

Examples in this topic describe how to use files from a remote Git repository when developing Snowflake applications and how to execute SQL
scripts in a Git repository clone.

Be sure to see the following, which describe other ways to interact with a Git repository clone.

- [Sync Streamlit in Snowflake apps with a Git repository](/developer-guide/streamlit/features/git-integration)
- [Sync notebooks with a Git repository](/user-guide/ui-snowsight/notebooks-snowgit)

## Use a Git repository file as a stored procedure handler

After you’ve [set up integration between Snowflake and your remote Git repository](/developer-guide/git/git-setting-up),
you can use files from the repository as handler code in stored procedures and UDFs. Note that,
[as with staged handlers](/developer-guide/inline-or-staged#label-inline-stage-using-staged), you must qualify the handler function name with the name of its containing
class or module.

This example describes how to use Python handler code from the repository in a stored procedure.

### Code required by this example

The handler in this example depends on a database created with SQL code similar to the following:

Copy code

```
CREATE DATABASE example_db;
USE DATABASE example_db;
CREATE SCHEMA example_schema;
USE SCHEMA example_schema;

CREATE OR REPLACE TABLE employees(id NUMBER, name VARCHAR, role VARCHAR);
INSERT INTO employees (id, name, role) VALUES (1, 'Alice', 'op'), (2, 'Bob', 'dev'), (3, 'Cindy', 'dev');
```

The example uses the following Python handler code contained in `filter.py`:

Copy code

```
from snowflake.snowpark.functions import col

def filter_by_role(session, table_name, role):
  df = session.table(table_name)
  return df.filter(col("role") == role)
```

### Commit the file and refresh the Git repository clone

1. From your Git client, add the code to the remote repository.

   Code in the following example uses the git command-line tool to add and commit the handler file to the local repository, then push it
   to the remote repository referenced by the Git repository clone in Snowflake:

   Copy code

   ```
   $ git add python-handlers/filter.py
   $ git commit -m "Adding code to filter by role"
   $ git push
   ```
2. In Snowflake, refresh the Git repository clone.

   Assuming you’ve [set up integration between Snowflake and your remote Git repository](/developer-guide/git/git-setting-up),
   resulting in a Git repository clone in Snowflake, you can refresh the Git repository clone by fetching from the remote repository.

   Using Snowflake to refresh from your remote repository is similar to working with other Git client tools, where you fetch from the remote
   repository before beginning work to ensure that you have the latest changes.

   Code in the following example executes the [ALTER GIT REPOSITORY](/sql-reference/sql/alter-git-repository) command to
   retrieve the latest changes from the remote repository. The code generates a full clone that includes branches, tags, and commits.

   Copy code

   ```
   ALTER GIT REPOSITORY snowflake_extensions FETCH;
   ```

### Create and execute a procedure that uses the file in the Git repository clone

1. In Snowflake, write the procedure.

   When you write a procedure, you can reference its handler code at the code file’s location in the Git repository clone in Snowflake.
   For example, to refer to a file `python-handlers/filter.py` in the main branch of a remote repository synchronized to a Git repository
   clone called `snowflake_extensions`, you would use syntax similar to the following:

   Copy code

   ```
   @snowflake_extensions/branches/main/python-handlers/filter.py
   ```

   Code in the following example creates a procedure called `filter_by_role`, specifying handler code stored in the Git repository clone:

   Copy code

   ```
   CREATE OR REPLACE PROCEDURE filter_by_role(tableName VARCHAR, role VARCHAR)
     RETURNS TABLE(id NUMBER, name VARCHAR, role VARCHAR)
     LANGUAGE PYTHON
     RUNTIME_VERSION = '3.12'
     PACKAGES = ('snowflake-snowpark-python')
     IMPORTS = ('@example_db.example_schema.snowflake_extensions/branches/main/python-handlers/filter.py')
     HANDLER = 'filter.filter_by_role';
   ```
2. Execute the procedure.

   The following code executes the procedure.

   Copy code

   ```
   CALL filter_by_role('employees', 'dev');
   ```

   The following is an example of output from the procedure.

   ```
   ---------------------
   | ID | NAME  | ROLE |
   ---------------------
   | 2  | Bob   | dev  |
   ---------------------
   | 3  | Cindy | dev  |
   ---------------------
   ```

## Use a Git repository clone file to configure new accounts

This example describes how to execute a SQL script contained in a Git repository clone in Snowflake. The script in the example creates a
user and role.

This example uses the [EXECUTE IMMEDIATE FROM](/sql-reference/sql/execute-immediate-from) command to execute the SQL statements contained in a file in
the Git repository clone.

With EXECUTE IMMEDIATE FROM, you can execute (from any Snowflake session) scripts you manage in your remote Git repository. For
example, you might have a script that sets up every new Snowflake account in your organization. The script might contain statements
to create users, roles, objects, and grant privileges on the account and objects.

1. Create the file `setup.sql` with the following contents:

   Copy code

   ```
   CREATE ROLE analyst;

   CREATE USER gladys;

   GRANT ROLE analyst TO USER gladys;

   SHOW GRANTS TO USER gladys;
   ```
2. Commit your SQL file to your remote Git repository.

   Use the git command-line tool to commit the file to your remote Git repository:

   Copy code

   ```
   git add scripts/setup.sql
   git commit -m "Adding code to set up new accounts"
   git push
   ```

   For detailed instructions, see [Commit the file and refresh the Git repository clone](#label-commit-file-and-refresh-repo-stage).
3. Refresh the Git repository clone.

   Refresh the Git repository clone `configuration_repo`:

   Copy code

   ```
   ALTER GIT REPOSITORY configuration_repo FETCH;
   ```

   For detailed instructions, see [Commit the file and refresh the Git repository clone](#label-commit-file-and-refresh-repo-stage).
4. In Snowflake, execute the file in your Git repository clone:

   Note

   The user executing the following statement must use a role that has the required privileges to execute all statements in the file.
   For more information, see [Access control requirements](/sql-reference/sql/execute-immediate-from#label-execute-immediate-from-access-control-requirements).

   Copy code

   ```
   EXECUTE IMMEDIATE FROM @configuration_repo/branches/main/scripts/setup.sql;
   ```

   The EXECUTE IMMEDIATE FROM commands [returns](/sql-reference/sql/execute-immediate-from#label-execute-immediate-from-returns) the results of the last SQL statement
   in the file:

   ```
   +-------------------------------+---------+------------+--------------+--------------+
   | created_on                    | role    | granted_to | grantee_name | granted_by   |
   |-------------------------------+---------+------------+--------------+--------------|
   | 2023-07-24 22:07:04.354 -0700 | ANALYST | USER       | GLADYS       | ACCOUNTADMIN |
   +-------------------------------+---------+------------+--------------+--------------+
   ```
