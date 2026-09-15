# Creating Stored Procedures for DataFrames in Python

The Snowpark API provides methods that you can use to create a stored procedure in Python.
This topic explains how to create stored procedures.

## Introduction

With Snowpark, you can create stored procedures for your custom lambdas and functions, and you can call these
stored procedures to process the data in your DataFrame.

You can create stored procedures that only exist within the current session (temporary stored procedures)
as well as stored procedures that you can use in other sessions (permanent stored procedures).

## Using Artifact Repository packages in a Stored Procedure

For more information, see [Artifact Repository overview](/developer-guide/udf/python/udf-python-packages#label-python-udfs-pypi).

## Using Third-Party Packages from Anaconda in a Stored Procedure

You can specify Anaconda packages to install when you create Python stored procedures.
When calling the Python stored procedure inside a Snowflake warehouse, Anaconda packages
are installed seamlessly and cached on the virtual warehouse on your behalf.
For more information about best practices, how to view the available packages, and how to
set up a local development environment, see [Using third-party packages](/developer-guide/udf/python/udf-python-packages).

Use `session.add_packages` to add packages at the session level.

This code example shows how to import packages and return their versions.

Copy code

```
import pandas as pd
import snowflake.snowpark
import xgboost as xgb
from snowflake.snowpark.functions import sproc

session.add_packages("snowflake-snowpark-python", "pandas", "xgboost==1.5.0")

@sproc
def compute(session: snowflake.snowpark.Session) -> list:
  return [pd.__version__, xgb.__version__]
```

You can also use `session.add_requirements` to specify packages with a
[requirements file](https://pip.pypa.io/en/stable/user_guide/#requirements-files).

Copy code

```
session.add_requirements("mydir/requirements.txt")
```

You can add the stored-procedure-level packages to overwrite the session-level packages you might have added previously.

Copy code

```
import pandas as pd
import snowflake.snowpark
import xgboost as xgb
from snowflake.snowpark.functions import sproc

@sproc(packages=["snowflake-snowpark-python", "pandas", "xgboost==1.5.0"])
def compute(session: snowflake.snowpark.Session) -> list:
  return [pd.__version__, xgb.__version__]
```

Important

If you don’t specify a package version, Snowflake will use the latest version when resolving dependencies.
When deploying the stored procedure to production, however, you may want to ensure that your code always
uses the same dependency versions. You can do that for both permanent and temporary stored procedures.

- When you create a permanent stored procedure, the stored procedure is created and registered only once.
  This resolves dependencies once and the selected version is used for production workloads. When the stored procedure executes,
  it will always use the same dependency versions.
- When you create a temporary stored procedure, specify dependency versions as part of the version spec.
  That way, when the stored procedure is registered, package resolution will use the specified version.
  If you don’t specify the version, the dependency might be updated when a new version becomes available.

## Creating an Anonymous Stored Procedure

To create an anonymous stored procedure, you can either:

- Call the `sproc` function in the `snowflake.snowpark.functions` module, passing in the definition of the anonymous function.
- Call the `register` method in the `StoredProcedureRegistration` class, passing in the definition of the anonymous function.
  To access an attribute or method of the `StoredProcedureRegistration` class, call the `sproc` property of the `Session` class.

Here is an example of an anonymous stored procedure:

Copy code

```
from snowflake.snowpark.functions import sproc
from snowflake.snowpark.types import IntegerType

add_one = sproc(lambda session, x: session.sql(f"select {x} + 1").collect()[0][0], return_type=IntegerType(), input_types=[IntegerType()], packages=["snowflake-snowpark-python"])
```

Note

When writing code that might execute in multiple sessions, use the `register` method to register stored procedures,
rather than using the `sproc` function. This can prevent errors in which the default Snowflake `Session` object
cannot be found.

## Creating and registering a named stored procedure

If you want to call a stored procedure by name (e.g. by using the `call` function in the `Session` object),
you can create and register a named stored procedure. To do this, you can either:

- Call the `sproc` function in the `snowflake.snowpark.functions` module, passing in the `name` argument
  and the definition of the anonymous function.
- Call the `register` method in the `StoredProcedureRegistration` class, passing in the `name` argument
  and the definition of the anonymous function.
  To access an attribute or method of the `StoredProcedureRegistration` class, call the `sproc` property of the `Session` class.

Calling `register` or `sproc` will create a temporary stored procedure that you can use in the current session.

To create a permanent stored procedure, call the `register` method or the `sproc` function and set
the `is_permanent` argument to `True`. When you create a permanent stored procedure, you must also set the `stage_location`
argument to the stage location where the Python connector used by Snowpark uploads the Python file for the stored procedure and its dependencies.

Here is an example of how to register a named temporary stored procedure:

Copy code

```
from snowflake.snowpark.functions import sproc
from snowflake.snowpark.types import IntegerType

add_one = sproc(lambda session, x: session.sql(f"select {x} + 1").collect()[0][0], return_type=IntegerType(), input_types=[IntegerType()], name="my_sproc", replace=True, packages=["snowflake-snowpark-python"])
```

Here is an example of how to register a named permanent stored procedure by setting the `is_permanent` argument to `True`:

Copy code

```
import snowflake.snowpark
from snowflake.snowpark.functions import sproc

@sproc(name="minus_one", is_permanent=True, stage_location="@my_stage", replace=True, packages=["snowflake-snowpark-python"])
def minus_one(session: snowflake.snowpark.Session, x: int) -> int:
  return session.sql(f"select {x} - 1").collect()[0][0]
```

Here is an example of these stored procedures being called:

Copy code

```
add_one(1)
```

```
2
```

Copy code

```
session.call("minus_one", 1)
```

```
0
```

Copy code

```
session.sql("call minus_one(1)").collect()
```

```
[Row(MINUS_ONE(1)=0)]
```

## Reading Files with a Stored Procedure

To read the contents of a file with a stored procedure, you can:

- [Read a statically-specified file](#label-snowpark-python-sprocs-read-files-import) by importing a file and then reading it from the stored procedure’s home directory.
- [Read a dynamically-specified file with SnowflakeFile](#label-snowpark-python-sprocs-read-files-snowflakefile). You might do this if you need to access a file during computation.

### Reading Statically-Specified Files

1. Specify that the file is a dependency, which uploads the file to the server. This is done the same way as for UDFs.
   For more information, see [Specifying Dependencies for a UDF](/developer-guide/snowpark/python/creating-udfs#label-snowpark-python-udf-inline-dependencies).

   For example:

   Copy code

   ```
   # Import a file from your local machine as a dependency.
   session.add_import("/<path>/my_file.txt")

   # Or import a file that you uploaded to a stage as a dependency.
   session.add_import("@my_stage/<path>/my_file.txt")
   ```
2. In the stored procedure, read the file.

   Copy code

   ```
   def read_file(name: str) -> str:
     import sys
     IMPORT_DIRECTORY_NAME = "snowflake_import_directory"
     import_dir = sys._xoptions[IMPORT_DIRECTORY_NAME]

     with open(import_dir + 'my_file.txt', 'r') as file:
       return file.read()
   ```

### Reading Dynamically-Specified Files with `SnowflakeFile`

You can read a file from a stage using the `SnowflakeFile` class in the Snowpark `snowflake.snowpark.files` module.
The `SnowflakeFile` class provides dynamic file access, which lets you stream files of any size. Dynamic file access is also useful when you want to iterate over multiple files. For example, see [Processing multiple files](/developer-guide/udf/python/udf-python-examples#label-reading-file-from-python-udf-multiple-files).

For more information about and examples of reading files using `SnowflakeFile`, see [Reading a File Using the SnowflakeFile Class in a Python UDF Handler](/developer-guide/udf/python/udf-python-examples#label-reading-file-from-python-udf-snowflakefile).

The following example creates a permanent stored procedure that reads a file from a stage using `SnowflakeFile` and returns the file length.

Create the stored procedure:

Copy code

```
import snowflake.snowpark as snowpark
from snowflake.snowpark.functions import sproc
from snowflake.snowpark.files import SnowflakeFile
from snowflake.snowpark.types import StringType, IntegerType

@sproc(name="calc_size", is_permanent=True, stage_location="@my_procedures", replace=True, packages=["snowflake-snowpark-python"])
def calc_size(ignored_session: snowpark.Session, file_path: str) -> int:
  with SnowflakeFile.open(file_path) as f:
    s = f.read()
  return len(s);
```

Call the stored procedure:

Copy code

```
file_size = session.sql("call calc_size(build_scoped_file_url('@my_stage', 'my_file.csv'))")
```
