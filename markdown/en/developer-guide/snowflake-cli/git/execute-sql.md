# Executing files from a repository

Note

Snowflake CLI does not support executing Python files for Python versions 3.12 and above.

You can use the `snow git execute` command for all `.sql` and `.py` files in a repository path. The command searches for all SQL and Python files and then executes the [EXECUTE IMMEDIATE](/sql-reference/sql/execute-immediate) command on each of them.

Copy code

```
snow git execute <REPO_PATH> [--silent]
```

where:

- `<REPO_PATH>` can be any of the following:

  - A repository stage, such as `@snowcli_git/branches/main/`, to execute commands from all `.sql` files in the stage.
  - A glob-like pattern, such as `@snowcli_git/branches/main/scripts/*`, to execute commands from all `.sql` files in the `scripts` directory.
  - A specific `.sql` file, such as `@snowcli_git/branches/main/scripts/script.sql`, to execute commands contained only the `script.sql` file.
- `--silent` hides intermediate messages with file execution results.

Note

The `snow git execute` command does not display the output of any of the SQL commands it processes.

The following example shows how to execute SQL commands in all files within the `project` directory that match a regular expression.

Copy code

```
snow git execute "@git_test/branches/main/projects/script?.sql"
```

```
SUCCESS - git_test/branches/main/projects/script1.sql
SUCCESS - git_test/branches/main/projects/script2.sql
SUCCESS - git_test/branches/main/projects/script3.sql
+---------------------------------------------------------------+
| File                                        | Status  | Error |
|---------------------------------------------+---------+-------|
| git_test/branches/main/projects/script1.sql | SUCCESS | None  |
| git_test/branches/main/projects/script2.sql | SUCCESS | None  |
| git_test/branches/main/projects/script3.sql | SUCCESS | None  |
+---------------------------------------------------------------+
```

Adding the `--silent` option to the same command hides the intermediate messages showing the progression of the files processed.

Copy code

```
snow git execute "@git_test/branches/main/projects/script?.sql" --silent
```

```
+---------------------------------------------------------------+
| File                                        | Status  | Error |
|---------------------------------------------+---------+-------|
| git_test/branches/main/projects/script1.sql | SUCCESS | None  |
| git_test/branches/main/projects/script2.sql | SUCCESS | None  |
| git_test/branches/main/projects/script3.sql | SUCCESS | None  |
+---------------------------------------------------------------+
```
