# Creating Python UDFs

This topic shows how to create and install a Python UDF (user-defined function).

## Writing the Python code

### Writing the Python module and function

Write a module that follows the specifications below:

- Define the module. A module is a file containing Python definitions and statements.
- Define a function inside the module.
- If the function accepts arguments, each argument must be one of the data types specified in the `Python Data Type` column of the
  [SQL-Python Type Mappings table](/developer-guide/udf-stored-procedure-data-type-mapping#label-sql-python-data-type-mappings).

  Function arguments are bound by position, not name. The first argument passed to the
  UDF is the first argument received by the Python function.
- Specify an appropriate return value. Because a Python UDF must be a scalar function, it must return one value each
  time that it is invoked. The type of the return value must be one of the data types specified in the
  `Python Data Type` column of the [SQL-Python Type Mappings table](/developer-guide/udf-stored-procedure-data-type-mapping#label-sql-python-data-type-mappings).
  The type of the return value must be
  compatible with the SQL data type specified in the `RETURNS` clause of the [CREATE FUNCTION](/sql-reference/sql/create-function) statement.
- Your module can contain more than one function. The function that is called by Snowflake can call other functions in the same module, or in
  other modules.
- Your function (and any functions called by your function) must comply with the
  [Snowflake-imposed constraints for Python UDFs](/developer-guide/udf/python/udf-python-designing#label-udf-python-limitations).

Note

Vectorized Python UDFs let you define Python functions that receive batches of input rows
as [Pandas DataFrames](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html) and
return batches of results as [Pandas arrays](https://pandas.pydata.org/docs/reference/api/pandas.array.html)
or [Series](https://pandas.pydata.org/docs/reference/series.html). For more information, see [Vectorized Python UDFs](/developer-guide/udf/python/udf-python-batch).

## Creating the function in Snowflake

You must execute a [CREATE FUNCTION](/sql-reference/sql/create-function) statement to specify:

- The name to use for the UDF.
- The name of the Python function to call when the Python UDF is called.

The name of the UDF does not need to match the name of the handler function written in Python. The HANDLER clause in the CREATE
FUNCTION statement associates the UDF name with the Python function.

When choosing a name for the UDF, refer to [Naming and overloading procedures and UDFs](/developer-guide/udf-stored-procedure-naming-conventions).

Within the body of the CREATE FUNCTION statement, function arguments are bound by position, not name. The first argument declared
in the CREATE FUNCTION statement is the first argument passed to the Python function.

For information about the data types of arguments, see [SQL-Python Data Type Mappings](/developer-guide/udf-stored-procedure-data-type-mapping#label-sql-python-data-type-mappings).

Set `runtime_version` to the version of the Python runtime that your code requires. The supported versions of Python are:

> Generally available versions:
>
> - 3.9 (deprecated)
> - 3.10
> - 3.11
> - 3.12
> - 3.13
> - 3.14

## UDFs with in-line code vs. UDFs with code uploaded from a stage

The code for a Python UDF can be specified either of the following ways:

- Uploaded from a stage: The CREATE FUNCTION statement specifies the location of an existing Python source
  code in a [stage](/sql-reference/sql/create-stage).
- In-line: The CREATE FUNCTION statement specifies the Python source code.

### Creating an in-line Python UDF

For an in-line UDF, you supply the Python source code as part of the CREATE FUNCTION statement.

For example, the following statement creates an in-line Python UDF that adds one to a given integer:

Copy code

```
CREATE OR REPLACE FUNCTION addone(i INT)
  RETURNS INT
  LANGUAGE PYTHON
  RUNTIME_VERSION = '3.12'
  HANDLER = 'addone_py'
AS $$
def addone_py(i):
 return i+1
$$;
```

The Python source code is specified in the `AS` clause. The source code can be surrounded by either single quotes or by a pair of
dollar signs (`$$`). Using the double dollar signs is usually easier if the source code contains embedded single quotes.

Call the UDF:

Copy code

```
SELECT addone(10);
```

Here is the output:

```
+------------+
| ADDONE(10) |
|------------|
|         11 |
+------------+
```

The Python source code can contain more than one module, and more than one function in a module, so the `HANDLER` clause specifies
the module and function to call.

An in-line Python UDF can call code in modules that are included in the `IMPORTS` clause.

For more details about the syntax of the CREATE FUNCTION statement, see [CREATE FUNCTION](/sql-reference/sql/create-function).

For more examples, see [in-line Python UDF examples](/developer-guide/udf/python/udf-python-examples#label-udf-python-in-line-examples).

### Creating a Python UDF with code uploaded from a stage

The following statements create a simple Python UDF using code uploaded from a [stage](/sql-reference/sql/create-stage).
The stage hosting the file must be readable by the owner
of the UDF. Also, ZIP files must be self-contained and not rely on any additional setup scripts to be executed.

Create a Python file named `sleepy.py` that contains your source code:

Copy code

```
def snore(n):   # return a series of n snores
  result = []
  for a in range(n):
    result.append("Zzz")
  return result
```

Launch the [SnowSQL (CLI client)](/user-guide/snowsql) and use the [PUT](/sql-reference/sql/put) command to copy the file from
the local file system to the default user stage, named `@~`. (The `PUT` command cannot be executed through the Snowflake GUI.)

Copy code

```
put
file:///Users/Me/sleepy.py
@~/
auto_compress = false
overwrite = true
;
```

If you delete or rename the file, you can no longer call the UDF.
If you need to update your file, then update it while no calls to the UDF can be made.
If the old file is still in the stage, the `PUT` command should include the clause `OVERWRITE=TRUE`.

Create the UDF. The handler specifies the module and the function.

Copy code

```
CREATE OR REPLACE FUNCTION dream(i INT)
  RETURNS VARIANT
  LANGUAGE PYTHON
  RUNTIME_VERSION = '3.12'
  HANDLER = 'sleepy.snore'
  IMPORTS = ('@~/sleepy.py')
```

Call the UDF:

Copy code

```
SELECT dream(3);
```

```
+----------+
| DREAM(3) |
|----------|
| [        |
|   "Zzz", |
|   "Zzz", |
|   "Zzz"  |
| ]        |
+----------+
```

#### Specifying multiple import files

Here is an example of how to specify multiple import files.

Copy code

```
CREATE OR REPLACE FUNCTION multiple_import_files(s STRING)
  RETURNS STRING
  LANGUAGE PYTHON
  RUNTIME_VERSION = 3.12
  IMPORTS = ('@python_udf_dep/bar/python_imports_a.zip', '@python_udf_dep/foo/python_imports_b.zip')
  HANDLER = 'compute'
AS $$
def compute(s):
  return s
$$;
```

Note

The import file names specified must be different.
For example, this will not work:
`imports=('@python_udf_dep/bar/python_imports.zip', '@python_udf_dep/foo/python_imports.zip')`.

## Granting privileges on the function

For any role other than the owner of the function to call the function, the owner must grant the appropriate
privileges to the role.

The [GRANT](/sql-reference/sql/grant-privilege) statements for a Python UDF are essentially identical to
the GRANT statements for other UDFs, such as JavaScript UDFs.

For example:

Copy code

```
GRANT USAGE ON FUNCTION my_python_udf(number, number) TO my_role;
```
