# Managing Snowflake functions and stored procedures with Python

You can use Python to manage user-defined functions (UDFs) and stored procedures in Snowflake. When you create a UDF or procedure, you
write its logic in one of the supported handler languages, then create it using the Snowflake Python APIs. For more information about UDFs and
procedures, see [Extending Snowflake with Functions and Procedures](/developer-guide/extensibility).

## Prerequisites

The examples in this topic assume that you’ve added code to connect with Snowflake and to create a `Root` object from which to use the
Snowflake Python APIs.

For example, the following code uses connection parameters defined in a configuration file to create a connection to Snowflake:

Copy code

```
from snowflake.core import Root
from snowflake.snowpark import Session

session = Session.builder.config("connection_name", "myconnection").create()
root = Root(session)
```

Using the resulting `Session` object, the code creates a `Root` object to use the API’s types and methods. For more information,
see [Connect to Snowflake with the Snowflake Python APIs](/developer-guide/snowflake-python-api/snowflake-python-connecting-snowflake).

## Managing user-defined functions (UDFs)

You can manage user-defined functions (UDFs), which you can write to extend the system to perform operations that are not available through
the built-in system-defined functions provided by Snowflake. After you create a UDF, you can reuse it multiple times. For more information,
see [User-defined functions overview](/developer-guide/udf/udf-overview).

Note

Calling UDFs by using the API is currently not supported.

The Snowflake Python APIs represents UDFs with two separate types:

- `UserDefinedFunction`: Exposes a UDF’s properties such as its name, list of arguments, return type, and function definition.
- `UserDefinedFunctionResource`: Exposes methods you can use to fetch a corresponding `UserDefinedFunction` object, rename the
  UDF, and drop the UDF.

### Creating a UDF

To create a UDF, first create a `UserDefinedFunction` object, and then create a `UserDefinedFunctionCollection` object from the
API `Root` object. Using `UserDefinedFunctionCollection.create`, add the new UDF to Snowflake.

When you create a UDF, you specify a handler whose code is written in one of the following supported languages.

#### Python

Code in the following example creates a `UserDefinedFunction` object that represents a UDF named `my_python_function` in the
`my_db` database and the `my_schema` schema, with the specified arguments, return type, language, and UDF Python definition:

Copy code

```
from snowflake.core.user_defined_function import (
    PythonFunction,
    ReturnDataType,
    UserDefinedFunction
)

function_of_python = UserDefinedFunction(
    "my_python_function",
    arguments=[],
    return_type=ReturnDataType(datatype="VARIANT"),
    language_config=PythonFunction(runtime_version="3.12", packages=[], handler="udf"),
    body="""
def udf():
    return {"key": "value"}
    """,
)

root.databases["my_db"].schemas["my_schema"].user_defined_functions.create(function_of_python)
```

#### Java

Code in the following example creates a `UserDefinedFunction` object that represents a UDF named `my_java_function` in the
`my_db` database and the `my_schema` schema, with the specified arguments, return type, language, and UDF Java definition:

Copy code

```
from snowflake.core.user_defined_function import (
    Argument,
    JavaFunction,
    ReturnDataType,
    UserDefinedFunction
)

function_body = """
    class TestFunc {
        public static String echoVarchar(String x) {
            return x;
        }
    }
"""

function_of_java = UserDefinedFunction(
    name="my_java_function",
    arguments=[Argument(name="x", datatype="STRING")],
    return_type=ReturnDataType(datatype="VARCHAR", nullable=True),
    language_config=JavaFunction(
        handler="TestFunc.echoVarchar",
        runtime_version="11",
        target_path=target_path,
        packages=[],
        called_on_null_input=True,
        is_volatile=True,
    ),
    body=function_body,
    comment="test_comment",
)

root.databases["my_db"].schemas["my_schema"].user_defined_functions.create(function_of_java)
```

#### JavaScript

Code in the following example creates a `UserDefinedFunction` object that represents a UDF named `my_javascript_function` in the
`my_db` database and the `my_schema` schema, with the specified arguments, return type, language, and UDF JavaScript definition:

Copy code

```
from snowflake.core.user_defined_function import (
    Argument,
    ReturnDataType,
    JavaScriptFunction,
    UserDefinedFunction
)

function_body = """
    if (D <= 0) {
        return 1;
    } else {
        var result = 1;
        for (var i = 2; i <= D; i++) {
            result = result * i;
        }
        return result;
    }
"""

function_of_javascript = UserDefinedFunction(
    name="my_javascript_function",
    arguments=[Argument(name="d", datatype="DOUBLE")],
    return_type=ReturnDataType(datatype="DOUBLE"),
    language_config=JavaScriptFunction(),
    body=function_body,
)

root.databases["my_db"].schemas["my_schema"].user_defined_functions.create(function_of_javascript)
```

#### Scala

Code in the following example creates a `UserDefinedFunction` object that represents a UDF named `my_scala_function` in the
`my_db` database and the `my_schema` schema, with the specified arguments, return type, language, and UDF Scala definition:

Copy code

```
from snowflake.core.user_defined_function import (
    Argument,
    ReturnDataType,
    ScalaFunction,
    UserDefinedFunction
)

function_body = """
    class Echo {
        def echoVarchar(x : String): String = {
            return x
        }
    }
"""

function_of_scala = UserDefinedFunction(
    name="my_scala_function",
    arguments=[Argument(name="x", datatype="VARCHAR")],
    return_type=ReturnDataType(datatype="VARCHAR"),
    language_config=ScalaFunction(
        runtime_version="2.12", handler="Echo.echoVarchar", target_path=target_path, packages=[]
    ),
    body=function_body,
    comment="test_comment",
)

root.databases["my_db"].schemas["my_schema"].user_defined_functions.create(function_of_scala)
```

#### SQL

Code in the following example creates a `UserDefinedFunction` object that represents a UDF named `my_sql_function` in the
`my_db` database and the `my_schema` schema, with the specified arguments, return type, language, and UDF SQL definition:

Copy code

```
from snowflake.core.user_defined_function import (
    ReturnDataType,
    SQLFunction,
    UserDefinedFunction
)

function_body = """3.141592654::FLOAT"""

function_of_sql = UserDefinedFunction(
    name="my_sql_function",
    arguments=[],
    return_type=ReturnDataType(datatype="FLOAT"),
    language_config=SQLFunction(),
    body=function_body,
)

root.databases["my_db"].schemas["my_schema"].user_defined_functions.create(function_of_sql)
```

### Getting UDF details

You can get information about a UDF by calling the `UserDefinedFunctionResource.fetch` method, which returns a
`UserDefinedFunction` object.

Code in the following example fetches information about the `my_javascript_function(DOUBLE)` UDF in the `my_db` database and the
`my_schema` schema:

Note

When getting a UDF resource object, you must specify the full signature (the UDF name and its parameter data types) because UDFs can be
overloaded.

Copy code

```
my_udf = root.databases["my_db"].schemas["my_schema"].user_defined_functions["my_javascript_function(DOUBLE)"].fetch()
print(my_udf.to_dict())
```

### Listing UDFs

You can list UDFs using the `UserDefinedFunctionCollection.iter` method, which returns a `PagedIter` iterator of
`UserDefinedFunction` objects.

Code in the following example lists UDFs whose name starts with `my_java` in the `my_db` database and the `my_schema` schema, and
then prints the name of each:

Copy code

```
udf_iter = root.databases["my_db"].schemas["my_schema"].user_defined_functions.iter(like="my_java%")
for udf_obj in udf_iter:
    print(udf_obj.name)
```

### Renaming a UDF

You can rename a UDF with a `UserDefinedFunctionResource` object.

Code in the following example gets the `my_javascript_function(DOUBLE)` UDF resource object in the `my_db` database and the
`my_schema` schema, and then renames the UDF to `my_other_js_function` while also moving it to the `my_other_db` database and the
`my_other_schema` schema:

Copy code

```
root.databases["my_db"].schemas["my_schema"].user_defined_functions["my_javascript_function(DOUBLE)"].rename(
    "my_other_js_function",
    target_database = "my_other_database",
    target_schema = "my_other_schema"
)
```

### Dropping a UDF

You can drop a UDF with a `UserDefinedFunctionResource` object.

Code in the following example gets the `my_javascript_function(DOUBLE)` UDF resource object and then drops the UDF:

Copy code

```
my_udf_res = root.databases["my_db"].schemas["my_schema"].user_defined_functions["my_javascript_function(DOUBLE)"]
my_udf_res.drop()
```

## Managing stored procedures

You can manage stored procedures, which you can write to extend the system with procedural code that executes SQL. In a stored procedure,
you can use programmatic constructs to perform branching and looping. After you create a stored procedure, you can reuse it multiple times.
For more information, see [Stored procedures overview](/developer-guide/stored-procedure/stored-procedures-overview).

The Snowflake Python APIs represents procedures with two separate types:

- `Procedure`: Exposes a procedure’s properties such as its name, list of arguments, return type, and procedure definition.
- `ProcedureResource`: Exposes methods you can use to fetch a corresponding `Procedure` object, call the procedure, and drop
  the procedure.

### Creating a procedure

To create a procedure, first create a `Procedure` object, and then create a `ProcedureCollection` object from the API
`Root` object. Using `ProcedureCollection.create`, add the new procedure to Snowflake.

Code in the following example creates a `Procedure` object that represents a procedure named `my_procedure` in the `my_db`
database and the `my_schema` schema, with the specified arguments, return type, and SQL procedure definition:

Copy code

```
from snowflake.core.procedure import Argument, ColumnType, Procedure, ReturnTable, SQLFunction

procedure = Procedure(
    name="my_procedure",
    arguments=[Argument(name="id", datatype="VARCHAR")],
    return_type=ReturnTable(
        column_list=[
            ColumnType(name="id", datatype="NUMBER"),
            ColumnType(name="price", datatype="NUMBER"),
        ]
    ),
    language_config=SQLFunction(),
    body="""
        DECLARE
            res RESULTSET DEFAULT (SELECT * FROM invoices WHERE id = :id);
        BEGIN
            RETURN TABLE(res);
        END;
    """,
)

procedures = root.databases["my_db"].schemas["my_schema"].procedures
procedures.create(procedure)
```

### Calling a procedure

You can call a procedure with a `ProcedureResource` object.

Code in the following example gets the `my_procedure(VARCHAR)` procedure resource object, creates a `CallArgumentList` object, and
then calls the procedure using that list of arguments.

Note

When getting a procedure resource object, you must specify the full signature (the procedure name and its parameter data types) because
procedures can be overloaded.

Copy code

```
from snowflake.core.procedure import CallArgument, CallArgumentList

procedure_reference = root.databases["my_db"].schemas["my_schema"].procedures["my_procedure(VARCHAR)"]
call_argument_list = CallArgumentList(call_arguments=[
    CallArgument(name="id", datatype="VARCHAR", value="1"),
])
procedure_reference.call(call_argument_list=call_argument_list, extract=False)
```

### Getting procedure details

You can get information about a procedure by calling the `ProcedureResource.fetch` method, which returns a `Procedure` object.

Code in the following example fetches information about the `my_procedure(VARCHAR)` procedure in the `my_db` database and the
`my_schema` schema:

Copy code

```
my_procedure = root.databases["my_db"].schemas["my_schema"].procedures["my_procedure(VARCHAR)"].fetch()
print(my_procedure.to_dict())
```

### Listing procedures

You can list procedures using the `ProcedureCollection.iter` method, which returns a `PagedIter` iterator of `Procedure`
objects.

Code in the following example lists procedures whose name starts with `my` in the `my_db` database and the `my_schema` schema, and
then prints the name of each:

Copy code

```
procedure_iter = root.databases["my_db"].schemas["my_schema"].procedures.iter(like="my%")
for procedure_obj in procedure_iter:
    print(procedure_obj.name)
```

### Dropping a procedure

You can drop a procedure with a `ProcedureResource` object.

Code in the following example gets the `my_procedure(VARCHAR)` procedure resource object in the `my_db` database and the `my_schema`
schema, and then drops the procedure.

Copy code

```
my_procedure_res = root.databases["my_db"].schemas["my_schema"].procedures["my_procedure(VARCHAR)"]
my_procedure_res.drop()
```
