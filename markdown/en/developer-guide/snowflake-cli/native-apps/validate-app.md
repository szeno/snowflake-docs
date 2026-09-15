# Validating an application package

## Prerequisites

- You must have an existing connection in your `config.toml` file.
- You must have a `snowflake.yml` file in your Snowflake Native App project.

Snowflake CLI automatically validates a Snowflake Native App setup script, along with any other SQL files included using the SQL [EXECUTE IMMEDIATE](/sql-reference/sql/execute-immediate) statement, when you run (`snow app run`) or deploy (`snow app deploy`) an application. It uses the script most recently uploaded by one of the commands. Validation checks for SQL syntax errors, invalid object references, and best practices. If the script validation fails, the executed command aborts but does not automatically roll back the staged files.

For more information about Snowflake Native App setup scripts, see [Create the setup script](/developer-guide/native-apps/creating-setup-script) in the Snowflake Native App Framework documentation.

## How to validate a setup script manually

Occasionally, you might want to validate a setup script before deploying an application to avoid potential impacts that could occur if validation fails during the deployment process. The `snow app validate` command validates a setup script without needing to run or deploy an application. It uploads source files to a separate scratch stage that drops automatically after the command completes to avoid disturbing files in the application’s source stage.

1. [Create a connection](/developer-guide/snowflake-cli/connecting/connect), if necessary.
2. Execute the `snow app validate` command from within your project, similar to the following:

   Copy code

   ```
   snow app validate --connection="dev"
   ```

   When successful, the command returns the following message:

   ```
   Snowflake Native App validation succeeded.
   ```

   If validation fails, the following error message, along with any error messages, is displayed:

   ```
   Snowflake Native App setup script failed validation.
   ```

If you want to see the raw validation output as JSON, you can execute `snow app validate --format json`, as shown:

Copy code

```
snow app validate --format json
```

```
{
    "errors": [],
    "warnings": [],
    "status": "SUCCESS"
}
```

where:

- **errors** shows a list of errors, if they exist. Errors cause validation to fail.
- **warnings** shows a list of warnings, if they exist.
- **status** shows the result of the validation: SUCCESS or FAILURE.

If validation encounters any errors, which cause validation to fail, or warnings, which lets is succeed, the command displays the following information for the error or warning:

- `message`: Human-readable message for the error or warning.
- `cause`: Reason why the SQL construct is considered an error or warning.
- `errorCode`: Numeric code associated with the error or warning.
- `fileName`: Name of the file containing the error or warning, relative the stage root.
- `line`: Line number in the file identifying the location of the error or warning.
- `column`: Column number in the line where the error or warning occurred.

The following example shows a failed validation that contained both warnings and errors:

Copy code

```
snow app validate --format json
```

```
{
    "errors": [
        {
            "message": "Error in file '@STAGE_SNOWFLAKE_CLI_SCRATCH/empty.sql': Empty SQL statement.",
            "cause": "Empty SQL statement.",
            "errorCode": "000900",
            "fileName": "@STAGE_SNOWFLAKE_CLI_SCRATCH/empty.sql",
            "line": -1,
            "column": -1
        },
        {
            "message": "Error in file '@STAGE_SNOWFLAKE_CLI_SCRATCH/second.sql': Unsupported feature 'CREATE VERSIONED SCHEMA without OR ALTER'.",
            "cause": "Unsupported feature 'CREATE VERSIONED SCHEMA without OR ALTER'.",
            "errorCode": "000002",
            "fileName": "@STAGE_SNOWFLAKE_CLI_SCRATCH/second.sql",
            "line": -1,
            "column": -1
        },
        {
            "message": "Error in file '@STAGE_SNOWFLAKE_CLI_SCRATCH/setup_script.sql': File '/does-not-exist.sql' cannot be found in the same stage as the setup script is located.",
            "cause": "File '/does-not-exist.sql' cannot be found in the same stage as the setup script is located.",
            "errorCode": "093159",
            "fileName": "@STAGE_SNOWFLAKE_CLI_SCRATCH/setup_script.sql",
            "line": -1,
            "column": -1
        }
    ],
    "warnings": [
        {
            "message": "Warning in file '@STAGE_SNOWFLAKE_CLI_SCRATCH/setup_script.sql' on line 11 at position 35: APPLICATION ROLE should be created with IF NOT EXISTS.",
            "cause": "APPLICATION ROLE should be created with IF NOT EXISTS.",
            "errorCode": "093352",
            "fileName": "@STAGE_SNOWFLAKE_CLI_SCRATCH/setup_script.sql",
            "line": 11,
            "column": 35
        },
        {
            "message": "Warning in file '@STAGE_SNOWFLAKE_CLI_SCRATCH/setup_script.sql' on line 15 at position 13: CREATE Table statement in the setup script should have \"IF NOT EXISTS\", \"OR REPLACE\", or \"OR ALTER\".",
            "cause": "CREATE Table statement in the setup script should have \"IF NOT EXISTS\", \"OR REPLACE\", or \"OR ALTER\".",
            "errorCode": "093351",
            "fileName": "@STAGE_SNOWFLAKE_CLI_SCRATCH/setup_script.sql",
            "line": 15,
            "column": 13
        },
        {
            "message": "Warning in file '@STAGE_SNOWFLAKE_CLI_SCRATCH/setup_script.sql' on line 15 at position 13: Table identifier 'MY_TABLE' should include its parent schema name.",
            "cause": "Table identifier 'MY_TABLE' should include its parent schema name.",
            "errorCode": "093353",
            "fileName": "@STAGE_SNOWFLAKE_CLI_SCRATCH/setup_script.sql",
            "line": 15,
            "column": 13
        }
    ],
    "status": "FAIL"
}
```
