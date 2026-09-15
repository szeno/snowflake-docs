description:
:   Error, Warning, and Issue (EWI) for the DBX elements.

# Snowpark Migration Accelerator: Issue codes for DBX

## SPRKDBX1000

Message: < ***Magic Name*** > is not supported in Snowsight. It is necessary to rewrite code.

Category: Conversion Error.

### Description

This issue appears when the SMA detects a magic command in a DBX notebook, Snowsight does not support magic commands.

### Scenario

**Input**

The following is an example of a magic command in a DBX notebook.

Copy code

```
val df = spark.read.format("csv").load("path/to/file.csv")
df.show()
```

**Output**

The SMA adds the EWI `SPRKDBX1000` to the output code to let you know that this magic is not supported.

Copy code

```
# EWI: SPRKDBX1000 => Then %alias magic command is not supported in Snowsight. It is necessary to rewrite code.
# %alias myalias echo \"This is an alias\"
```

**Recommended fix**

This issue has no direct fix. You must rewrite the code.

## SPRKDBX1001

Message: The `%run` command has a partial mapping, because it has different behavior in Snowpark.

Category: Conversion Error.

### Description

This issue appears when the SMA detects a use of the `%run` command that does not have a direct equivalent in Snowpark.

The way the `%run` command works in DBX is similar to an import, meaning it includes the code
from another notebook into the current one in that it shares variables, functions, and states with the notebook
where the command was executed.

### Scenario

**Input**

Below is an example of the `%run` command.

Copy code

```
%run /Workspace/Users/path/to/Notebook/notebookName
```

**Output**

The SMA adds the EWI `SPRKDBX1001` on the output code to let you know that this element has a different behavior in Snowpark.

Copy code

```
EWI: SPRKDBX1001 => The %run command has a partial mapping, because it has a different behavior in Snowpark.
spark.sql("EXECUTE NOTEBOOK <DATABASE>.<SCHEMA>.notebookName()")
```

**Recommended fix**

Identify the used elements (functions, variables) from the executed notebook and encapsulate them into a file. Import that file into the executing notebook.

This fix would emulate the behavior of the original `%run` command.

## SPRKDBX1002

Message: Scala cells are not supported in Snowsight.

Category: Conversion Error.

### Description

This issue appears when the SMA detects a cell with Scala code in a DBX notebook; Snowsight does not support Scala cells. Only SQL, Python, and Markdown are available in Snowsight.

### Scenarios

The following scenarios are not supported.

#### Scenario 1

Scala cell in a DBX notebook.

**Input**

Below is an example of a Scala cell in a DBX notebook.

Copy code

```
val df = spark.read.format("csv").load("path/to/file.csv")
df.show()
```

**Output**

The SMA adds the EWI `SPRKDBX1002` on the output code to let you know that this cell is not supported.

Copy code

```
# EWI: SPRKDBX1002 => Scala cells are not supported in Snowpark. It is necessary to rewrite the Scala code in Python.
#val df = spark.read.format("csv").load("path/to/file.csv")
#df.show()
```

**Recommended fix**

This issue has no direct fix. You must rewrite the Scala code in Python.

#### Scenario 2

The `%scala` command in a DBX notebook.

**Input**

Below is an example of a `%scala` command cell in a DBX notebook.

Copy code

```
%scala
val df = spark.read.format("csv").load("path/to/file.csv")
df.show()
```

**Output**

The SMA adds the EWI `SPRKDBX1002` on the output code to let you know that this cell is not supported.

Copy code

```
# EWI: SPRKDBX1002 => Scala cells are not supported in Snowpark. It is necessary to rewrite the Scala code in Python.
#val df = spark.read.format("csv").load("path/to/file.csv")
#df.show()
```

**Recommended fix**

This issue has no direct fix. It is necessary to rewrite the Scala code in Python.

## SPRKDBX1003

Message: R cells are not supported in Snowsight.

Category: Conversion Error.

### Description

This issue appears when the SMA detects a cell with R code in a DBX notebook; Snowsight does not support R cells. Only SQL, Python, and Markdown are available in Snowsight.

### Scenario

**Input**

Below is an example of %r command.

Copy code

```
%r
my_vector <- c(1, 2, 3, 4, 5)
```

**Output**

The SMA adds the EWI `SPRKDBX1003` on the output code to let you know that this cell is not supported.

Copy code

```
# EWI: SPRKDBX1003 => R cells are not supported in Snowpark. It is necessary to rewrite the R code in Python.
# my_vector <- c(1, 2, 3, 4, 5)
```

**Recommended fix**

This issue has no direct fix. You must rewrite the R code in Python.

## SPRKDBX1004

Message: The method ‘< ***element*** >’ has no equivalence on Snowflake/Snowsight.

Category: Conversion Error.

### Description

This issue appears when the SMA detects the use of a DBX method that has no equivalent in Snowsight, and does not have its own error code associated with it. SMA uses this generic error code for an unsupported DBX element.

### Scenario

**Input**

Below is an example of DBX utility element.

Copy code

```
dbutils.data.summarize(df)
```

**Output**

The SMA adds the EWI `SPRKDBX1004` on the output code to let you know that the method has no equivalent in Snowsight.

Copy code

```
# EWI: SPRKPY1004 => The method 'dbutils.data.summarize ' has no equivalence on Snowflake/Snowsight.
dbutils.data.summarize(df)
```

**Recommended fix**

Because this is a generic error code that applies to a range of unsupported functions, there is not a single and specific fix. The appropriate action will depend on the particular element in use.

Please note that even though the element is not supported, it does not necessarily mean that a solution or workaround cannot be found. It means only that the SMA itself cannot find the solution.

## SPRKDBX1005

Message: The method <***element***> has an equivalent in Snowflake/Snowsight; however, the element’s parameter, a URL path, is not supported.

Category: Warning.

### Description

This issue appears when the SMA identifies the use of a DBX method that has an equivalent in Snowsight; however, the element has a URL path as a parameter, which is not supported in Snowflake and Snowsight.

### Scenario

**Input**

The following example shows a `dbutils` method called with a URL path as a parameter:

Copy code

```
dbutils.fs.cp("s3://example.com/data.csv", "/mnt/data/")
```

**Output**

The SMA adds the EWI `SPRKDBX1005` on the output code to let you know that the method has URL as a parameter and is not supported.

Copy code

```
# EWI: SPRKDBX1005 => The method 'dbutils.fs.cp' has an equivalent in Snowflake/Snowsight; however, the element's parameter, a URL path, is not supported.
sfutils.fs.cp("s3://example.com/data.csv", "/mnt/data/")
```

**Recommended fix**

This generic warning is used for functions with URL path parameters, so there is no single recommended fix. Review the specific method and its usage to determine if an alternative approach or workaround is possible in Snowflake or Snowsight. Consider refactoring the code to avoid using URL paths. You can also implement custom logic to handle the data transfer outside the method.

Please note that even though the URL paths are not supported, it does not necessarily mean that a solution or workaround cannot be found. It only means that the SMA itself cannot find the solution.

Snowflake offers the ability to map URL-type paths by using an external stage, which facilitates the integration and access to external data. Consult the Snowflake documentation on [External Stage](/user-guide/data-load-s3-create-stage) for more information.

For this, you must have a storage integration ([STORAGE\_INTEGRATION](/sql-reference/sql/create-storage-integration)) configured. Subsequently, you will need to copy your files to a table. You can find more details on how to copy data from an [S3 stage](/user-guide/data-load-s3-copy) in the Snowflake documentation.
