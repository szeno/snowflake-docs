# Add application logic to an application package

Feature — Generally Available

The Snowflake Native App Framework is generally available on supported cloud platforms. For additional information, see
[Support for private connectivity, VPS, and government regions](/developer-guide/native-apps/limitations#label-native-apps-supported-clouds).

This topic describes how to add application logic to the setup script of an application package. It
also describes how to use external code files in an application package.

See [Add a Streamlit app](/developer-guide/native-apps/adding-streamlit) for information about including a Streamlit in Snowflake app in an application package.

## Considerations for using stored procedures and functions

The Snowflake Native App Framework allows you to include stored procedures, user-defined functions
(UDFs), and external functions in an application package. These can be written in any of the
[languages Snowflake supports](/developer-guide/stored-procedures-vs-udfs#label-sp-udf-languages).

If you plan to publish your Snowflake Native App to the Snowflake Marketplace as a limited trial listing and want to limit the functionality
of your application that is available to those trial consumers, see [Preparing to offer a limited trial listing](https://other-docs.snowflake.com/collaboration/provider-listings-preparing#label-prepare-limited-trial-listing).

### Add application code securely

All stored procedures and UDFs within a Snowflake Native App run as the application and
have access to all objects within the installed Snowflake Native App. This can lead to SQL
injection attacks.

When developing procedures and functions for use within a Snowflake Native App, Snowflake recommends
that all SQL commands requiring input from users be run using bound parameters. This includes
input provided through procedure arguments.

See [Creating a stored procedure](/developer-guide/stored-procedure/stored-procedures-creating) for more information.

### About caller’s rights and owner’s rights

All procedures created by the setup script or that run
within the installed Snowflake Native App must be run with the rights of the owner (EXECUTE AS OWNER).

This restriction exists because if the Snowflake Native App were to run with caller’s rights (EXECUTE AS CALLER) in
a procedure that the Snowflake Native App does not own, the procedure would run as the Snowflake Native App
itself and allow a consumer to create code to view or modify the contents of the Snowflake Native App and shared data content.

See [Understanding caller’s rights and owner’s rights stored procedures](/developer-guide/stored-procedure/stored-procedures-rights) for more information.

### Limitations when calling context functions from the setup script

[Context functions](/sql-reference/functions-context) provide information about the context
in which a statement is run. Within the context of the Snowflake Native App Framework, some context
functions are not available. Context functions that are not available are either blocked and
return an error or always return a null value.

Use caution when using context functions in policies applied to shared data
content within a Snowflake Native App. Some functions, for example CURRENT\_IP\_ADDRESS, behave differently
in the context of a Snowflake Native App.

When using context functions that depend on the namespace within the client organization
there may be conflicts with functions in other namespaces. For example, a row access policy
using CURRENT\_USER should be aware that the same username can exist in multiple accounts.

When using a [Streamlit](https://streamlit.io/) app within a Snowflake Native App, context functions
have additional constraints. For example, CURRENT\_USER returns NULL when invoked from Streamlit in Snowflake.

The following table lists the context functions that are not supported by the Snowflake Native App Framework:

| Context Function | Blocked in shared content (returns null) | Blocked in setup scripts and stored procedure and UDFs owned by the Snowflake Native App (throws an exception) |
| --- | --- | --- |
| CURRENT\_ROLE | ✔ |  |
| CURRENT\_ROLE\_TYPE | ✔ |  |
| CURRENT\_USER | ✔ |  |
| CURRENT\_SESSION | ✔ |  |
| IS\_ROLE\_IN\_SESSION | ✔ |  |
| CURRENT\_IP\_ADDRESS | ✔ | ✔ |
| CURRENT\_AVAILABLE\_ROLES | ✔ | ✔ |
| CURRENT\_SECONDARY\_ROLES | ✔ | ✔ |
| ALL\_USER\_NAMES |  | ✔ |
| GET\_USERS\_FOR\_COLLABORATION |  | ✔ |
| CURRENT\_WAREHOUSE |  | ✔ |
| SYSTEM$ALLOWLIST |  | ✔ |

Expand

Show lessSee more

Note

CURRENT\_USER and CURRENT\_SESSION return NULL when invoked from Streamlit in Snowflake within a Snowflake Native App unless
permission is granted to the app with GRANT READ SESSION ON ACCOUNT TO APPLICATION.

## Supported versions of Python in a Snowflake Native App

For information on the versions of Python that Snowflake supports,
see [Snowflake Python Runtime Support](/developer-guide/python-runtime-support-policy).

Caution

Snowflake Native Apps do not support decommissioned versions of Python.

As a provider, you must ensure that your app uses supported versions of Python. Apps cannot create functions
that use decommissioned versions of Python. Additionally, you cannot create or publish new versions of an app that
attempt to create functions that use decommissioned versions of Python.

Existing published versions of an app that use decommissioned versions of Python cannot be installed.

## Use Snowpark functions and procedures in an app

The Snowflake Native App Framework supports the Snowpark libraries for creating stored procedures in Java, Scala, and Python.

### Reference external code files

There are two types of code files that you can include in an application package:

- Referenced files: include binaries, libraries and other code files. These files are specific
  to a version defined in the application package. These files must be located in the root directory of the stage
  when creating or adding a version.

  Referenced files are different from user-defined functions and stored procedures because they are not
  defined in the setup script of an application package. These files are referenced by import statements within the
  stored procedures and UDFs that are defined in the setup script.
- Resource files: include semi-structured data, structured data, and binaries, for example, a machine
  learning model. These files must be uploaded to a named stage that is accessible to
  the application package.

A stored procedure, user-defined function, or external function that references these types of
code files must be created within a versioned schema in the setup script. When creating stored
procedures or functions within a versioned schema, you must reference a code file relative
to the root directory of the named stage.

For example, if the root directory of the named stage is `/app_files/dev`, this directory would
contain the following files and directories:

- A manifest file.
- A directory containing the setup script, for example `scripts/setup_version.sql`.
- Referenced files that are imported when creating a stored procedure, UDF, or external function
  within the setup script, for example:
  - `libraries/jars/lookup.jar`
  - `libraries/jars/log4j.jar`
  - `libraries/python/evaluate.py`

In this scenario, the directory structure would be as follows:

Copy code

```
@DEV_DB.DEV_SCHEMA.DEV_STAGE/V1:
└── app_files/
    └── dev
        ├── manifest.yml
        └── scripts/
            ├── setup_script.sql
            └── libraries/
                └── jars/
                    ├── lookup.jar
                    └── log4j.jar
            └── python
                └── evaluation.py
```

To access the JAR files in this directory structure, a stored procedure defined in the setup
script would reference these files as shown in the following example:

Copy code

```
CREATE PROCEDURE PROGRAMS.LOOKUP(...)
  RETURNS STRING
  LANGUAGE JAVA
  PACKAGES = ('com.snowflake:snowpark:latest')
  IMPORTS = ('/scripts/libraries/jar/lookup.jar',
             '/scripts/libraries/jar/log4j.jar')
  HANDLER = 'com.acme.programs.Lookup';
```

In this example, the IMPORTS statement has a path relative to the root directory used to create the
version, for example, the location of the manifest file.

### Include Java and Scala code in an application package

The Snowflake Native App Framework supports using Java and Scala in stored procedures and in external
code files.

#### Create Java and Scala UDFs inline

The Snowflake Native App Framework supports creating stored procedures containing
[Java](/developer-guide/stored-procedure/java/procedure-java-overview) and
[Scala](/developer-guide/stored-procedure/scala/procedure-scala-overview). The code that defines the
stored procedure must be added to the setup script.

The following example shows a stored procedure containing a Java function:

Copy code

```
CREATE OR ALTER VERSIONED SCHEMA app_code;
CREATE STAGE app_code.app_jars;

CREATE FUNCTION app_code.add(x INT, y INT)
  RETURNS INTEGER
  LANGUAGE JAVA
  HANDLER = 'TestAddFunc.add'
  TARGET_PATH = '@app_code.app_jars/TestAddFunc.jar'
  AS
  $$
  class TestAddFunc {
    public static int add(int x, int y) {
      Return x + y;
    }
  }
  $$;
```

#### Import external Java and Scala UDFs

The syntax for creating pre-compiled UDFs requires that imported JARs be included as part
of a set of versioned artifacts. To refer to pre-compiled JARs, use the relative path instead
of specifying the full stage location in the IMPORT clause.

The path must be relative to the root directory containing the version starting with a single
forward slash, for example `IMPORTS = ('/path/to/JARs/from/version/root')`. See
[Reference external code files](#label-native-apps-reference-app-files) for
more information on relative paths.

The following shows an example directory structure for the code files.

Copy code

```
@DEV_DB.DEV_SCHEMA.DEV_STAGE/V1:
└── V1/
    ├── manifest.yml
    ├── setup_script.sql
    └── JARs/
        ├── Java/
        │   └── TestAddFunc.jar
        └── Scala/
            └── TestMulFunc.jar
```

The following example shows how to create a Java function using a JAR file:

Copy code

```
CREATE FUNCTION app_code.add(x INTEGER, y INTEGER)
  RETURNS INTEGER
  LANGUAGE JAVA
  HANDLER = 'TestAddFunc.add'
  IMPORTS = ('/JARs/Java/TestAddFunc.jar');
```

#### Restrictions on Java and Scala UDFs

The Snowflake Native App Framework imposes the following restrictions when using Java and Scala:

- Imports are only allowed for UDFs created in a versioned schema.
- Imports can only access the version artifacts using a relative path.
- UDFs created outside of versioned schemas can only be created inline.
- Relative paths are not supported for TARGET\_PATH.

### Add Python code to an application package

The Snowflake Native App Framework supports using Python in stored procedures and in external code
files.

#### Define a Python function in the setup script

The Snowflake Native App Framework supports creating stored procedures in
[Python](/developer-guide/stored-procedure/python/procedure-python-overview).

The following example shows a stored procedure containing a Python function:

Copy code

```
CREATE FUNCTION app_code.py_echo_func(str STRING)
  RETURNS STRING
  LANGUAGE PYTHON
  HANDLER = 'echo'
AS
$$
def echo(str):
  return "ECHO: " + str
$$;
```

#### Use external Python files

The following example shows how to include an external Python file in an application package:

Copy code

```
CREATE FUNCTION PY_PROCESS_DATA_FUNC()
  RETURNS STRING
  LANGUAGE PYTHON
  HANDLER = 'TestPythonFunc.process'
  IMPORTS = ('/python_modules/TestPythonFunc.py',
    '/python_modules/data.csv')
```

See to [Reference external code files](#label-native-apps-reference-app-files) for more information on relative paths.

#### Restrictions on Python UDFs

Snowflake Native App Framework imposes the following restrictions on Python UDFs:

- Imports are only allowed for UDFs created in a versioned schema.
- Imports can only access the version artifacts using a relative path.
- UDFs created outside of versioned schemas can only be created inline.

## Add JavaScript functions and procedures to an application package

The Snowflake Native App Framework supports using JavaScript in stored procedures and user-defined
functions using the [JavaScript API](/developer-guide/stored-procedure/stored-procedures-javascript).

### Handle JavaScript errors

When using JavaScript within an application package, Snowflake recommends that you catch and
handle errors. If not, the error message and stack trace that the
error returns are visible to the consumer. To ensure that data content and application logic
are kept private, use try/catch blocks in situations where sensitive objects or data is
being accessed.

The following example shows a JavaScript stored procedure that catches an error and returns
a message:

Copy code

```
CREATE OR REPLACE PROCEDURE APP_SCHEMA.ERROR_CATCH()
  RETURNS STRING
  LANGUAGE JAVASCRIPT
  EXECUTE AS OWNER
  AS $$
    try {
      let x = y.length;
    }
    catch(err){
      return "There is an error.";
    }
    return "Done";
  $$;
```

This example creates a JavaScript stored procedure that contains a try/catch block. If the
stored procedure encounters an error when running the statement in the `try` block, it
returns the message “There is an error” which is visible to the consumer.

Without the try/catch block, the stored procedure would return the original error message
and the full stack trace which would be visible to the consumer.

Note

Other languages supported by the Snowflake Native App Framework return redact error messages that occur in a Snowflake Native App.

## Add external functions to an application package

[External functions](/sql-reference/sql/create-external-function) allow a Snowflake Native App
to make calls to application code that is hosted outside of Snowflake. External functions
require you to create an API Integration object.

Because API integrations allow connectivity outside of the consumer environment, the consumer
must provide the method of integration to the Snowflake Native App.

The following example shows a stored procedure created by the setup script that accepts the integration
and creates an external function. This example shows how to create an external function in the setup script of the
application package:

Copy code

```
CREATE OR REPLACE PROCEDURE calculator.create_external_function(integration_name STRING)
  RETURNS STRING
  LANGUAGE SQL
  EXECUTE AS OWNER
  AS
  DECLARE
    CREATE_STATEMENT VARCHAR;
  BEGIN
    CREATE_STATEMENT := 'CREATE OR REPLACE EXTERNAL FUNCTION EXTERNAL_ADD(NUM1 FLOAT, NUM2 FLOAT)
        RETURNS FLOAT API_INTEGRATION = ? AS ''https://xyz.execute-api.us-west-2.amazonaws.com/production/sum'';' ;
    EXECUTE IMMEDIATE :CREATE_STATEMENT USING (INTEGRATION_NAME);
    RETURN 'EXTERNAL FUNCTION CREATED';
  END;

GRANT USAGE ON PROCEDURE calculator.create_external_function(string) TO APPLICATION ROLE app_public;
```

This example defines a stored procedure, written in SQL, and [creates an external function](/sql-reference/sql/create-external-function)
that references an application hosted on a system outside of Snowflake. The external function returns an
API integration.

This example also grants USAGE on the stored procedure to an application role. The consumer must grant this
privilege to the Snowflake Native App before invoking this procedure in the setup script.
