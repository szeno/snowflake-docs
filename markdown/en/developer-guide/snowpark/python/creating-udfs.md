# Creating User-Defined Functions (UDFs) for DataFrames in Python

The Snowpark API provides methods that you can use to create a user-defined function from a lambda or function in Python.
This topic explains how to create these types of functions.

## Introduction

With Snowpark, you can create user-defined functions (UDFs) for your custom lambdas and functions, and you can call these
UDFs to process the data in your DataFrame.

When you use the Snowpark API to create a UDF, the Snowpark library uploads the code for your function to an internal stage.
When you call the UDF, the Snowpark library executes your function on the server, where the data is. As a result, the data
doesn’t need to be transferred to the client in order for the function to process the data.

In your custom code, you can also import modules from Python files or third-party packages.

You can create a UDF for your custom code in one of two ways:

- You can [create an anonymous UDF](#label-snowpark-python-udf-inline-anonymous) and assign the function to a variable. As long as
  this variable is in scope, you can use this variable to call the UDF.
- You can [create a named UDF](#label-snowpark-python-udf-inline-named) and call the UDF by name. You can use this if, for example,
  you need to call a UDF by name or use the UDF in a subsequent session.

The next sections explain how to create these UDFs using a local development environment or using a
[Python worksheet](/developer-guide/snowpark/python/python-worksheets).

Note that if you defined a UDF by running the `CREATE FUNCTION` command, you can call that UDF in Snowpark. For details, see
[Calling User-Defined Functions (UDFs)](/developer-guide/snowpark/python/calling-functions#label-snowpark-python-udfs-calling).

Note

Vectorized Python UDFs let you define Python functions that receive batches of input rows as Pandas DataFrames.
This results in much better performance with machine learning inference scenarios.
For more information, see [Using Vectorized UDFs](#label-snowpark-python-udf-vectorized).

Note

If you are working with a Python worksheet, use these examples within the handler function:

Copy code

```
import snowflake.snowpark as snowpark
from snowflake.snowpark.functions import col

def main(session: snowpark.Session):
  df_table = session.table("sample_product_data")
```

If the examples return something other than a DataFrame, such as a `list` of `Row` objects,
[change the return type](/developer-guide/snowpark/python/python-worksheets#label-snowsight-py-worksheets-return) to match the return type of the example.

After you run a code example, use the **Results** tab to view any output returned.
Refer to [Running Python Worksheets](/developer-guide/snowpark/python/python-worksheets#label-snowsight-py-worksheets-run) for more details.

## Specifying Dependencies for a UDF

To define a UDF using the Snowpark API, you must import the files that contain any modules that your UDF depends on, such as Python files,
zip files, resource files, etc.

- To do this using Python worksheets, refer to [Add a Python File from a Stage to a Worksheet](/developer-guide/snowpark/python/python-worksheets#label-snowsight-py-worksheets-add-py-file).
- To do this using your local development environment, you must call `Session.add_import()` in your code.

You can also specify a directory and the Snowpark library automatically compresses the directory and uploads it as a zip file.
(For details on reading resources from a UDF, see [Reading Files with a UDF](#label-snowpark-python-udf-read-files).)

When you call `Session.add_import()`, the Snowpark library uploads the specified files to an internal stage and imports the
files when executing your UDF.

The following example demonstrates how to add a zip file in a stage as a dependency to your code:

Copy code

```
# Add a zip file that you uploaded to a stage.
session.add_import("@my_stage/<path>/my_library.zip")
```

The following examples demonstrate how to add a Python file from your local machine:

Copy code

```
# Import a Python file from your local machine.
session.add_import("/<path>/my_module.py")

# Import a Python file from your local machine and specify a relative Python import path.
session.add_import("/<path>/my_module.py", import_path="my_dir.my_module")
```

The following examples demonstrate how to add other types of dependencies:

Copy code

```
# Add a directory of resource files.
session.add_import("/<path>/my-resource-dir/")

# Add a resource file.
session.add_import("/<path>/my-resource.xml")
```

Note

The Python Snowpark library is not uploaded automatically.

You do not need to specify the following dependencies:

- **Your Python built-in libraries.**

  These libraries are already available in the runtime environment on the server where your UDFs are executed.

## Using Artifact Repository packages in a UDF

For more information, see [Artifact Repository overview](/developer-guide/udf/python/udf-python-packages#label-python-udfs-pypi).

## Using Third-Party Packages from Anaconda in a UDF

You can use third-party packages from the Snowflake Anaconda channel in a UDF.

- If you create a Python UDF in a Python worksheet, the Anaconda packages are already available to your worksheet.
  Refer to [Add a Python File from a Stage to a Worksheet](/developer-guide/snowpark/python/python-worksheets#label-snowsight-py-worksheets-add-py-file).
- If you create a Python UDF in your local development environment, you can specify which Anaconda packages to install.

When queries that call Python UDFs are executed inside a Snowflake warehouse, Anaconda packages
are installed seamlessly and cached on the virtual warehouse on your behalf.

For more information about best practices, how to view the available packages, and how to
set up a local development environment, see [Using third-party packages](/developer-guide/udf/python/udf-python-packages).

If you write a Python UDF in your local development environment, use `session.add_packages` to add packages at the session level.

This code example shows how to import packages and return their versions.

Copy code

```
import numpy as np
import pandas as pd
import xgboost as xgb
from snowflake.snowpark.functions import udf

session.add_packages("numpy", "pandas", "xgboost==1.5.0")

@udf
def compute() -> list:
  return [np.__version__, pd.__version__, xgb.__version__]
```

You can also use `session.add_requirements` to specify packages with a
[requirements file](https://pip.pypa.io/en/stable/user_guide/#requirements-files).

Copy code

```
session.add_requirements("mydir/requirements.txt")
```

You can add the UDF-level packages to overwrite the session-level packages you might have added previously.

Copy code

```
import numpy as np
import pandas as pd
import xgboost as xgb
from snowflake.snowpark.functions import udf

@udf(packages=["numpy", "pandas", "xgboost==1.5.0"])
def compute() -> list:
  return [np.__version__, pd.__version__, xgb.__version__]
```

Important

If you don’t specify a package version, Snowflake uses the latest version when resolving dependencies. When you deploy the UDF to
production, you might want to ensure that your code always uses the same dependency versions. You can do that for both permanent
and temporary UDFs.

- When you create a permanent UDF, the UDF is created and registered only once. This resolves dependencies once and the selected version
  is used for production workloads. When the UDF executes, it always uses the same dependency versions.
- When you create a temporary UDF, specify dependency versions as part of the version spec. That way, when the UDF is registered, package
  resolution uses the specified version. If you don’t specify the version, the dependency might be updated when a new version becomes
  available.

## Creating an Anonymous UDF

To create an anonymous UDF, you can either:

- Call the `udf` function in the `snowflake.snowpark.functions` module, passing in the definition of the anonymous
  function.
- Call the `register` method in the `UDFRegistration` class, passing in the definition of the anonymous
  function.

Here is an example of an anonymous UDF:

Copy code

```
from snowflake.snowpark.types import IntegerType
from snowflake.snowpark.functions import udf

add_one = udf(lambda x: x+1, return_type=IntegerType(), input_types=[IntegerType()])
```

Note

When writing code that might execute in multiple sessions, use the `register` method to register
UDFs, rather than using the `udf` function. This can prevent errors in which the default Snowflake `Session` object
cannot be found.

## Creating and Registering a Named UDF

If you want to call a UDF by name (e.g. by using the `call_udf` function in the `functions` module), you can create and register a named UDF. To do this, use one of the following:

- The `register` method, in the `UDFRegistration` class, with the `name` argument.
- The `udf` function, in the `snowflake.snowpark.functions` module, with the `name` argument.

To access an attribute or method of the `UDFRegistration` class, call the `udf` property of the `Session` class.

Calling `register` or `udf` will create a temporary UDF that you can use in the current session.

To create a permanent UDF, call the `register` method or the `udf` function and set
the `is_permanent` argument to `True`. When you create a permanent UDF, you must also set the `stage_location`
argument to the stage location where the Python file for the UDF and its dependencies are uploaded.

Here is an example of how to register a named temporary UDF:

Copy code

```
from snowflake.snowpark.types import IntegerType
from snowflake.snowpark.functions import udf

add_one = udf(lambda x: x+1, return_type=IntegerType(), input_types=[IntegerType()], name="my_udf", replace=True)
```

Here is an example of how to register a named permanent UDF by setting the `is_permanent` argument to `True`:

Copy code

```
@udf(name="minus_one", is_permanent=True, stage_location="@my_stage", replace=True)
def minus_one(x: int) -> int:
  return x-1
```

Here is an example of these UDFs being called:

Copy code

```
df = session.create_dataframe([[1, 2], [3, 4]]).to_df("a", "b")
df.select(add_one("a"), minus_one("b")).collect()
```

```
[Row(MY_UDF("A")=2, MINUS_ONE("B")=1), Row(MY_UDF("A")=4, MINUS_ONE("B")=3)]
```

You can also call the UDF using SQL:

Copy code

```
session.sql("select minus_one(1)").collect()
```

```
[Row(MINUS_ONE(1)=0)]
```

## Creating a UDF from a Python source file

If you create your UDF in your local development environment, you can define your UDF handler in a Python file and then use the
`register_from_file` method in the `UDFRegistration` class to create a UDF.

Note

You cannot use this method in a Python worksheet.

Here are examples of using `register_from_file`.

Suppose you have a Python file `test_udf_file.py` that contains:

Copy code

```
def mod5(x: int) -> int:
  return x % 5
```

Then you can create a UDF from this function of file `test_udf_file.py`.

Copy code

```
# mod5() in that file has type hints
mod5_udf = session.udf.register_from_file(
  file_path="tests/resources/test_udf_dir/test_udf_file.py",
  func_name="mod5",
)
session.range(1, 8, 2).select(mod5_udf("id")).to_df("col1").collect()
```

```
[Row(COL1=1), Row(COL1=3), Row(COL1=0), Row(COL1=2)]
```

You can also upload the file to a stage location, then use it to create the UDF.

Copy code

```
from snowflake.snowpark.types import IntegerType
# suppose you have uploaded test_udf_file.py to stage location @mystage.
mod5_udf = session.udf.register_from_file(
  file_path="@mystage/test_udf_file.py",
  func_name="mod5",
  return_type=IntegerType(),
  input_types=[IntegerType()],
)
session.range(1, 8, 2).select(mod5_udf("id")).to_df("col1").collect()
```

```
[Row(COL1=1), Row(COL1=3), Row(COL1=0), Row(COL1=2)]
```

## Reading Files with a UDF

To read the contents of a file, your Python code can:

- [Read a statically-specified file](#label-snowpark-python-udf-read-files-import) by importing a file and then reading it from the UDF’s home directory.
- [Read a dynamically-specified file with SnowflakeFile](#label-snowpark-python-udf-read-files-snowflakefile). You might do this if you need to access a file during computation.

### Reading Statically-Specified Files

The Snowpark library uploads and executes UDFs on the server. If your UDF needs to read data from a file,
you must ensure that the file is uploaded with the UDF.

Note

If you write your UDF in a Python worksheet, the UDF can only read files from a stage.

To set up a UDF to read a file:

1. Specify that the file is a dependency, which uploads the file to the server. For more information, see
   [Specifying Dependencies for a UDF](#label-snowpark-python-udf-inline-dependencies).

   For example:

   Copy code

   ```
   # Import a file from your local machine as a dependency.
   session.add_import("/<path>/my_file.txt")

   # Or import a file that you uploaded to a stage as a dependency.
   session.add_import("@my_stage/<path>/my_file.txt")
   ```
2. In the UDF, read the file. In the following example, the file will only be read once during UDF creation, and will not
   be read again during UDF execution. This is achieved with a third-party library
   [cachetools](https://pypi.org/project/cachetools/).

   Copy code

   ```
   import sys
   import os
   import cachetools
   from snowflake.snowpark.types import StringType
   @cachetools.cached(cache={})
   def read_file(filename):
   import_dir = sys._xoptions.get("snowflake_import_directory")
      if import_dir:
         with open(os.path.join(import_dir, filename), "r") as f:
            return f.read()

   # create a temporary text file for test
   temp_file_name = "/tmp/temp.txt"
   with open(temp_file_name, "w") as t:
   _ = t.write("snowpark")
   session.add_import(temp_file_name)
   session.add_packages("cachetools")

   def add_suffix(s):
   return f"{read_file(os.path.basename(temp_file_name))}-{s}"

   concat_file_content_with_str_udf = session.udf.register(
      add_suffix,
      return_type=StringType(),
      input_types=[StringType()]
   )

   df = session.create_dataframe(["snowflake", "python"], schema=["a"])
   df.select(concat_file_content_with_str_udf("a")).to_df("col1").collect()
   ```

   ```
   [Row(COL1='snowpark-snowflake'), Row(COL1='snowpark-python')]
   ```

   Copy code

   ```
   os.remove(temp_file_name)
   session.clear_imports()
   ```

### Reading Dynamically-Specified Files with `SnowflakeFile`

You can read a file from a stage using the `SnowflakeFile` class in the Snowpark `snowflake.snowpark.files` module.
The `SnowflakeFile` class provides dynamic file access, which lets you stream files of any size. Dynamic file access is also useful when you want to iterate over multiple files. For example, see [Processing multiple files](/developer-guide/udf/python/udf-python-examples#label-reading-file-from-python-udf-multiple-files).

For more information about and examples of reading files using `SnowflakeFile`, see [Reading a File Using the SnowflakeFile Class in a Python UDF Handler](/developer-guide/udf/python/udf-python-examples#label-reading-file-from-python-udf-snowflakefile).

The following example registers a temporary UDF that reads a text file from a stage using `SnowflakeFile` and returns the file length.

Register the UDF:

Copy code

```
import snowflake.snowpark as snowpark
from snowflake.snowpark.functions import udf
from snowflake.snowpark.files import SnowflakeFile
from snowflake.snowpark.types import StringType, IntegerType

@udf(name="get_file_length", replace=True, input_types=[StringType()], return_type=IntegerType(), packages=['snowflake-snowpark-python'])
def get_file_length(file_path):
  with SnowflakeFile.open(file_path) as f:
    s = f.read()
  return len(s);
```

Call the UDF:

Copy code

```
session.sql("select get_file_length(build_scoped_file_url(@my_stage, 'example-file.txt'));")
```

## Writing files from Snowpark Python UDFs and UDTFs

With Snowpark Python, you can write files to stages with user-defined functions (UDFs), vectorized UDFs, user-defined table functions
(UDTFs), and vectorized UDTFs. In the function handler, you use the
[SnowflakeFile API](https://docs.snowflake.com/developer-guide/snowpark/reference/python/latest/snowpark/api/snowflake.snowpark.files.SnowflakeFile#snowflake.snowpark.files.SnowflakeFile)
to open and write files. When you return the file from the function, the file is written alongside the query results.

A simple UDF to write a file might look like this:

Copy code

```
CREATE OR REPLACE FUNCTION write_file()
RETURNS STRING
LANGUAGE PYTHON
VOLATILE
RUNTIME_VERSION = 3.12
PACKAGES = ('snowflake-snowpark-python')
HANDLER = 'write_file'
AS
$$
from snowflake.snowpark.files import SnowflakeFile

def write_file():
  file = SnowflakeFile.open_new_result("w") # Open a new result file
  file.write("Hello world")                 # Write data
  return file               # File must be returned
$$;
```

Executing this UDF will then give you a scoped URL referencing the result file.

### Accessing the result files

A file handler is returned as a scoped URL to the query calling the UDF. You can use this particular scoped URL to access files from within
Snowflake (through another UDF or the COPY FILES command), but not from outside of Snowflake as a pre-signed URL. The scoped URL is valid
for 24 hours.

After a file is returned by a UDF, you can access it using any of the following storage tools, depending on your use case:

- [COPY FILES](/sql-reference/sql/copy-files): Copy the file to another stage location. After the file is copied, you can use it like a typical
  staged file, such as by using the following tools:

  - [Directory tables](/user-guide/data-load-dirtables): Query a list of files on a stage using a WHERE clause to filter if necessary.
  - [GET\_PRESIGNED\_URL](/sql-reference/functions/get_presigned_url): Generate a URL to the @stage/file.
  - [External stages](/user-guide/data-load-overview#label-data-load-overview-external-stages): Access the file outside of Snowflake through cloud provider APIs.
- [UDF](/developer-guide/udf/udf-overview): Read the file in another query.

For more information, see [COPY FILES](/sql-reference/sql/copy-files).

### Limitations

- This feature is not available for Java or Scala.
- Stored procedures also support file writes, but cannot be easily chained with a COPY FILES command. Therefore, for file writes using
  stored procedures, we recommend using the file staging [PUT](/sql-reference/sql/put) command.

### Examples

This section includes code examples that show how to write files to stages for different use cases.

> - [File transformation](#label-udf-python-file-writes-examples-transformation)
> - [Create a PDF from a partition of table data and copy it to a final location](#label-udf-python-file-writes-examples-pdf-report)
> - [Split files and unload them into multiple tables](#label-udf-python-file-writes-examples-split-files)

#### File transformation

The following is a UDF handler example that transforms a file. You can modify this example to do different types of file
transformation, such as:

- Convert from one file format to another format.
- Re-size an image.
- Transform files into a “golden state” in a time-stamped format folder in the same or different bucket.

Copy code

```
CREATE OR REPLACE FUNCTION convert_to_foo(filename string)
RETURNS STRING
LANGUAGE PYTHON
VOLATILE
RUNTIME_VERSION = 3.12
PACKAGES = ('snowflake-snowpark-python')
HANDLER = 'convert_to_foo'
AS
$$
from snowflake.snowpark.files import SnowflakeFile

def convert_to_foo(filename):
  input_file = SnowflakeFile.open(filename, "r")
  converted_file = SnowflakeFile.open_new_result("w")

  # Foo-type is just adding foo at the end of every line
  for line in input_file.readlines():
    converted_file.write(line[:-1] + 'foo' + '\n')
  return converted_file
$$;
```

You can call this UDF in a query and then access the `converted_file` result file written by the UDF.

The following SQL examples show what you can do with result files returned by UDFs, such as copying them to a stage or consuming them in a
subsequent query or another UDF. These basic SQL patterns are applicable to any UDF file write examples included in this topic. For example,
you can use the pre-signed URL query for any of the following UDF examples by using it in place of another SQL statement.

##### Example 1: Convert a single file and copy it to a final stage

Copy code

```
COPY FILES INTO @output_stage FROM
  (SELECT convert_to_foo(BUILD_SCOPED_FILE_URL(@input_stage, 'in.txt')), 'out.foo.txt');
```

##### Example 2: Convert a table of files and copy them to a final stage

Copy code

```
CREATE TABLE files_to_convert(file string);
-- Populate files_to_convert with input files:
INSERT INTO files_to_convert VALUES ('file1.txt');
INSERT INTO files_to_convert VALUES ('file2.txt');

COPY FILES INTO @output_stage FROM
  (SELECT convert_to_foo(BUILD_SCOPED_FILE_URL(@input_stage, file)),
      REPLACE(file, '.txt', '.foo.txt') FROM files_to_convert);
```

##### Example 3: Convert all files in a stage and copy them to a final stage

Copy code

```
COPY FILES INTO @output_stage FROM
  (SELECT convert_to_foo(BUILD_SCOPED_FILE_URL(@input_stage, RELATIVE_PATH)),
      REPLACE(RELATIVE_PATH, 'format1', 'format2') FROM DIRECTORY(@input_stage));
```

##### Example 4: Convert all files from a table and read them without copying

Copy code

```
-- A basic UDF to read a file:
CREATE OR REPLACE FUNCTION read_udf(filename string)
RETURNS STRING
LANGUAGE PYTHON
VOLATILE
RUNTIME_VERSION = 3.12
PACKAGES = ('snowflake-snowpark-python')
HANDLER = 'read'
AS
'
from snowflake.snowpark.files import SnowflakeFile

def read(filename):
  return SnowflakeFile.open(filename, "r").read()
';
```

Copy code

```
-- Create files_to_convert as in Example 2.

SELECT convert_to_foo(BUILD_SCOPED_FILE_URL(@input_stage, file)) as new_file
  FROM files_to_convert;
-- The following query must be run within 24 hours from the prior one
SELECT read_udf(new_file) FROM TABLE(RESULT_SCAN(LAST_QUERY_ID()));
```

##### Example 5: Convert all files from a table and read them immediately via a UDF

Copy code

```
-- Set up files_to_convert as in Example 2.
-- Set up read_udf as in Example 4.

SELECT read_udf(
    convert_to_foo(BUILD_SCOPED_FILE_URL(@input_stage, file))) FROM files_to_convert;
```

##### Example 6: Read using pre-signed URLs

This example is only for stages with server-side encryption. Internal stages have client-side encryption by default.

Copy code

```
COPY FILES INTO @output_stage FROM
  (SELECT convert_to_foo(BUILD_SCOPED_FILE_URL(@input_stage, file)) FROM files_to_convert);

-- Refresh the directory to get new files in output_stage.
ALTER STAGE output_stage REFRESH;
```

#### Create a PDF from a partition of table data and copy it to a final location

The following UDF handler example partitions input data and writes a PDF report for each partition of the data. This example partitions
reports by the `location` string.

You can also modify this example to write other types of files such as ML models and other custom formats for each partition.

Copy code

```
-- Create a stage that includes the font (for PDF creation)

CREATE OR REPLACE STAGE fonts
URL = 's3://sfquickstarts/misc/';

-- UDF to write the data
CREATE OR REPLACE FUNCTION create_report_pdf(data string)
RETURNS TABLE (file string)
LANGUAGE PYTHON
RUNTIME_VERSION = 3.12
HANDLER='CreateReport'
PACKAGES = ('snowflake-snowpark-python', 'fpdf')
IMPORTS  = ('@fonts/DejaVuSans.ttf')
AS $$
from snowflake.snowpark.files import SnowflakeFile
from fpdf import FPDF
import shutil
import sys
import uuid
import_dir = sys._xoptions["snowflake_import_directory"]

class CreateReport:
  def __init__(self):
      self.pdf = None

  def process(self, data):
      if self.pdf == None:
        # PDF library edits this file, make sure it's unique.
        font_file = f'/tmp/DejaVuSans-{uuid.uuid4()}.ttf'
        shutil.copy(f'{import_dir}/DejaVuSans.ttf', font_file)
        self.pdf = FPDF()
        self.pdf.add_page()
        self.pdf.add_font('DejaVu', '', font_file, uni=True)
        self.pdf.set_font('DejaVu', '', 14)
      self.pdf.write(8, data)
      self.pdf.ln(8)

  def end_partition(self):
      f = SnowflakeFile.open_new_result("wb")
      f.write(self.pdf.output(dest='S').encode('latin-1'))
      yield f,
$$;
```

The following SQL example first sets up the `reportData` table with fictitious data and creates the `output_stage` stage. Then it calls
the `create_report_pdf` UDF to create a PDF file using data that it queries from the `reportData` table. In the same SQL statement, the
COPY FILES command copies the result file from the UDF to `output_stage`.

Note

We use a server-side-encrypted (SSE) output stage because the pre-signed URL
to a file on an SSE stage will download an unencrypted file. In general, we
recommend the default stage encryption on stages as the file is client-side
encrypted and it’s more secure. Files on normal stages can still be read
through UDFs or GET/PUT - just not via pre-signed URLs. Ensure you understand
the security implications before using an SSE stage in a production environment.

Copy code

```
 -- Fictitious data
 CREATE OR REPLACE TABLE reportData(location string, item string);
 INSERT INTO reportData VALUES ('SanMateo' ,'Item A');
 INSERT INTO reportData VALUES ('SanMateo' ,'Item Z');
 INSERT INTO reportData VALUES ('SanMateo' ,'Item X');
 INSERT INTO reportData VALUES ('Bellevue' ,'Item B');
 INSERT INTO reportData VALUES ('Bellevue' ,'Item Q');

 -- Presigned URLs only work with SSE stages, see note above.
 CREATE OR REPLACE STAGE output_stage ENCRYPTION = (TYPE = 'SNOWFLAKE_SSE');

 COPY FILES INTO @output_stage
   FROM (SELECT reports.file, location || '.pdf'
           FROM reportData, TABLE(create_report_pdf(item)
           OVER (partition BY location)) AS reports);

 -- Check the results
LIST @output_stage;
SELECT GET_PRESIGNED_URL(@output_stage, 'SanMateo.pdf');
```

#### Split files and unload them into multiple tables

The following UDF handler example splits a CSV file by line based on the first character of each line. The UDF then unloads the split files
into multiple tables.

Copy code

```
CREATE OR REPLACE FUNCTION split_file(path string)
RETURNS TABLE(file string, name string)
LANGUAGE PYTHON
VOLATILE
PACKAGES = ('snowflake-snowpark-python')
RUNTIME_VERSION = 3.12
HANDLER = 'SplitCsvFile'
AS $$
import csv
from snowflake.snowpark.files import SnowflakeFile

class SplitCsvFile:
    def process(self, file):
      toTable1 = SnowflakeFile.open_new_result("w")
      toTable1Csv = csv.writer(toTable1)
      toTable2 = SnowflakeFile.open_new_result("w")
      toTable2Csv = csv.writer(toTable2)
      toTable3 = SnowflakeFile.open_new_result("w")
      toTable3Csv = csv.writer(toTable3)
      with SnowflakeFile.open(file, 'r') as file:
        # File is of the format 1:itemA \n 2:itemB \n [...]
        for line in file.readlines():
          forTable = line[0]
          if (forTable == "1"):
            toTable1Csv.writerow([line[2:-1]])
          if (forTable == "2"):
            toTable2Csv.writerow([line[2:-1]])
          if (forTable == "3"):
            toTable3Csv.writerow([line[2:-1]])
      yield toTable1, 'table1.csv'
      yield toTable2, 'table2.csv'
      yield toTable3, 'table3.csv'
$$;
-- Create a stage with access to an import file.
CREATE OR REPLACE STAGE staged_files url="s3://sfquickstarts/misc/";

-- Add the files to be split into a table - we just add one.
CREATE OR REPLACE TABLE filesToSplit(path string);
INSERT INTO filesToSplit VALUES ( 'items.txt');

-- Create output tables
CREATE OR REPLACE TABLE table1(item string);
CREATE OR REPLACE TABLE table2(item string);
CREATE OR REPLACE TABLE table3(item string);

-- Create output stage
CREATE OR REPLACE stage output_stage;

-- Creates files named path-tableX.csv
COPY FILES INTO @output_stage FROM
  (SELECT file, path || '-' || name FROM filesToSplit, TABLE(split_file(build_scoped_file_url(@staged_files, path))));

-- We use pattern and COPY INTO (not COPY FILES INTO) to upload to a final table.
COPY INTO table1 FROM @output_stage PATTERN = '.*.table1.csv';
COPY INTO table2 FROM @output_stage PATTERN = '.*.table2.csv';
COPY INTO table3 FROM @output_stage PATTERN = '.*.table3.csv';

-- See results
SELECT * from table1;
SELECT * from table2;
SELECT * from table3;
```

## Using Vectorized UDFs

Vectorized Python UDFs let you define Python functions that receive batches of input rows
as [Pandas DataFrames](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html) and
return batches of results as [Pandas arrays](https://pandas.pydata.org/docs/reference/api/pandas.array.html)
or [Series](https://pandas.pydata.org/docs/reference/series.html).
The column in the Snowpark `dataframe` will be vectorized as a Pandas Series inside the UDF.

Here is an example of how to use the batch interface:

Copy code

```
from sklearn.linear_model import LinearRegression
model = LinearRegression()
model.fit(X, y)

@udf(packages=['pandas', 'scikit-learn','xgboost'])
def predict(df: PandasDataFrame[float, float, float, float]) -> PandasSeries[float]:
    # The input pandas DataFrame doesn't include column names. Specify the column names explicitly when needed.
    df.columns = ["col1", "col2", "col3", "col4"]
    return model.predict(df)
```

You call vectorized Python UDFs the same way you call other Python UDFs.
For more information, see [Vectorized Python UDFs](/developer-guide/udf/python/udf-python-batch), which explains how to create a vectorized UDF by using a SQL statement.
For example, you can use the `vectorized` decorator when you specify the Python code in the SQL statement.
By using the Snowpark Python API described in this document, you don’t use a SQL statement to create a vectorized UDF.
So you don’t use the `vectorized` decorator.

It is possible to limit the number of rows per batch. For more information, see [Setting a target batch size](/developer-guide/udf/python/udf-python-batch#label-udf-python-batch-size).

For more explanations and examples of using the Snowpark Python API to create vectorized UDFs, refer to
the [UDFs section of the Snowpark API Reference](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/api/snowflake.snowpark.udf.UDFRegistration).
