# Python UDF handler examples

This topic includes simple examples of UDF handler code written in Python.

For information on using Python to create a UDF handler, refer to [Creating Python UDFs](/developer-guide/udf/python/udf-python-creating).

Set `runtime_version` to the version of the Python runtime that your code requires. The supported versions of Python are:

> Generally available versions:
>
> - 3.9 (deprecated)
> - 3.10
> - 3.11
> - 3.12
> - 3.13
> - 3.14

## Importing a package in an in-line handler

A curated list of third-party packages from Anaconda is available.
For more information, see [Using third-party packages](/developer-guide/udf/python/udf-python-packages).

The following code shows how to import packages and return their versions.

Create the UDF:

Copy code

```
CREATE OR REPLACE FUNCTION py_udf()
  RETURNS VARIANT
  LANGUAGE PYTHON
  RUNTIME_VERSION = 3.12
  PACKAGES = ('numpy','pandas','xgboost==1.5.0')
  HANDLER = 'udf'
AS $$
import numpy as np
import pandas as pd
import xgboost as xgb
def udf():
  return [np.__version__, pd.__version__, xgb.__version__]
$$;
```

Call the UDF:

Copy code

```
SELECT py_udf();
```

```
+-------------+
| PY_UDF()    |
|-------------|
| [           |
|   "1.19.2", |
|   "1.4.0",  |
|   "1.5.0"   |
| ]           |
+-------------+
```

You can use the PACKAGES keyword to specify package versions as follows:

- Without a version (e.g `numpy`)
- Pinned to an exact version (e.g. `numpy==1.25.2`)
- Constrained to a version prefix by using wildcards (e.g. `numpy==1.*`)
- Constrained to a version range (e.g. `numpy>=1.25`)
- Constrained by multiple version specifiers (e.g. `numpy>=1.25,<2`) so that a package that satisfies all version specifiers will be selected.

Note

Using multiple range operators (e.g. `numpy>=1.25,<2`) is not supported in package policies but you can use them when creating Python UDF, UDTF, and stored procedures.

Here is an example of how to use the wildcard `*` to constrain a package to a version prefix.

Copy code

```
CREATE OR REPLACE FUNCTION my_udf()
  RETURNS STRING
  LANGUAGE PYTHON
  PACKAGES = ('numpy==1.*')
  RUNTIME_VERSION = 3.10
  HANDLER = 'echo'
AS $$
def echo():
  return 'hi'
$$;
```

This example shows how to constrain a package to be greater than or equal to a specified version.

Copy code

```
CREATE OR REPLACE FUNCTION my_udf()
  RETURNS STRING
  LANGUAGE PYTHON
  PACKAGES = ('numpy>=1.2')
  RUNTIME_VERSION = 3.10
  HANDLER = 'echo'
AS $$
def echo():
  return 'hi'
$$;
```

This example shows how to use multiple package version specifiers.

Copy code

```
CREATE OR REPLACE FUNCTION my_udf()
  RETURNS STRING
  LANGUAGE PYTHON
  PACKAGES = ('numpy>=1.2,<2')
  RUNTIME_VERSION = 3.10
  HANDLER = 'echo'
AS $$
def echo():
  return 'hi'
$$;
```

## Reading files and assets

### Reading a file

You can read the contents of a file with Python UDF handler code. For example, you might want to read a file to process unstructured data.

To read the contents of a file, you can:

- [Statically specify the file path and name with the IMPORTS clause](#label-reading-file-from-python-udf), then read it from the UDF’s home
  directory. This can be useful when a file name is static, consistent within the function, and you know the file name in advance.
- [Dynamically specify the file and read its contents with SnowflakeFile](#label-reading-file-from-python-udf-snowflakefile). You might do this if you need to access a file during computation.

#### Reading a statically-specified file using IMPORTS

You can read a file by specifying the file name and stage name in the IMPORTS clause of the
[CREATE FUNCTION](/sql-reference/sql/create-function) command.

When you specify a file in the IMPORTS clause, Snowflake copies that file from the stage to the UDF’s
*home directory* (also called the *import directory*), which is the directory from which the UDF reads the file.

Snowflake copies imported files to a single directory. All files in that directory must have unique names, so each file in your
IMPORTS clause must have a distinct name. This applies even if the files start out in different stages or different subdirectories within a
stage.

The following example uses an in-line Python handler that reads a file called `file.txt` from a stage named `my_stage`.
The handler retrieves the location of the UDF’s home directory using
the Python `sys._xoptions` method with the `snowflake_import_directory` system option.

Snowflake reads the file only once during UDF creation,
and will not read it again during UDF execution if reading the file happens outside of the target handler.

Create the UDF with an in-line handler:

Copy code

```
CREATE OR REPLACE FUNCTION my_udf()
  RETURNS STRING
  LANGUAGE PYTHON
  RUNTIME_VERSION = 3.12
  IMPORTS = ('@my_stage/file.txt')
  HANDLER = 'compute'
AS $$
import sys
import os

with open(os.path.join(sys._xoptions["snowflake_import_directory"], 'file.txt'), "r") as f:
  s = f.read()

def compute():
  return s
$$;
```

#### Reading a dynamically-specified file with `SnowflakeFile`

You can read a file from a stage using the `SnowflakeFile` class in the Snowpark `snowflake.snowpark.files` module.
The `SnowflakeFile` class provides dynamic file access, which lets you stream files of any size. Dynamic file access is also useful when you want to iterate over multiple files. For example, see [Processing multiple files](#label-reading-file-from-python-udf-multiple-files).

The `SnowflakeFile` class has one method for opening a file: `open`. The `open` method returns a `SnowflakeFile` object that extends Python’s `IOBase` file objects.

The `SnowflakeFile` object supports the following `IOBase`, `BufferedIOBase`, and `RawIOBase` methods:

> - `IOBase.fileno`
> - `IOBase.isatty`
> - `IOBase.readable`
> - `IOBase.readinto`
> - `IOBase.readline`
> - `IOBase.readlines`
> - `IOBase.seek`
> - `IOBase.seekable`
> - `IOBase.tell`
> - `BufferedIOBase.readinto1`
> - `RawIOBase.read`
> - `RawIOBase.readall`

For more information, see the [Python 3.12 documentation on IOBase](https://docs.python.org/3.12/library/io.html).
Calling unsupported methods in a Snowflake server, such as the method `fileno`, will return an error.

Note

By default, file access with `SnowflakeFile` requires scoped URLs in order to make your code resilient to file injection attacks. You can create a scoped URL in SQL using the built-in function [BUILD\_SCOPED\_FILE\_URL](/sql-reference/functions/build_scoped_file_url). For more information about scoped URLs, see [Types of URLs available to access files](/user-guide/unstructured-intro#label-unstructured-data-urls). Only users with access to the file can create a scoped URL.

The examples in this section use `SnowflakeFile` to read one or more files from a specified stage location.

- [Prerequisites](#prerequisites)
- [Calculating the perceptual hash of an image with an in-line Python handler](#calculating-the-perceptual-hash-of-an-image-with-an-in-line-python-handler)
- [Processing a CSV file with a UDTF](#processing-a-csv-file-with-a-udtf)
- [Processing multiple files](#processing-multiple-files)
- [Reading files with stage URIs and URLs](#reading-files-with-stage-uris-and-urls)

##### Prerequisites

Before your Python handler code can read a file on a stage, you must do the following to make the file available to the code:

1. Create a stage that is available to your handler.

   You can use an external stage or internal stage. If you use an internal stage, it can be a user stage when you plan to create a caller’s rights stored procedure.
   Otherwise, you must use a named stage. Snowflake does not currently support using a table stage for UDF dependencies.

   For more on creating a stage, see
   [CREATE STAGE](/sql-reference/sql/create-stage). For more on choosing an internal stage type, see
   [Choosing an internal stage for local files](/user-guide/data-load-local-file-system-create-stage).

   Adequate privileges on the stage must be assigned to the following role, depending on your use case:

   > | Use case | Role |
   > | --- | --- |
   > | UDF or owner’s rights stored procedure | The role that owns the executing UDF or stored procedure. |
   > | Caller’s rights stored procedure | The user role. |
   >
   > Expand
   >
   > Show lessSee more

   For more information, see [Granting privileges for user-defined functions](/developer-guide/udf/udf-access-control).
2. Copy the file that your code will read to the stage.

   You can copy the file from a local drive to an internal stage using the [PUT](/sql-reference/sql/put) command.
   For information on staging files with PUT, see [Staging data files from a local file system](/user-guide/data-load-local-file-system-stage).

   You can copy the file from a local drive to an external stage location using any of the tools provided by your cloud storage service.
   For help, see the documentation for your cloud storage service.

##### Calculating the perceptual hash of an image with an in-line Python handler

This example uses `SnowflakeFile` to read a pair of staged image files and use the [perceptual hash](https://www.phash.org/)
(pHash) of each file to determine how similar the images are to each other.

Create a UDF that returns the phash value of an image, specifying the input mode as binary by passing `rb` for the `mode` argument:

Copy code

```
CREATE OR REPLACE FUNCTION calc_phash(file_path STRING)
  RETURNS STRING
  LANGUAGE PYTHON
  RUNTIME_VERSION = '3.12'
  PACKAGES = ('snowflake-snowpark-python','imagehash','pillow')
  HANDLER = 'run'
AS $$
from PIL import Image
import imagehash
from snowflake.snowpark.files import SnowflakeFile

def run(file_path):
  with SnowflakeFile.open(file_path, 'rb') as f:
  return imagehash.average_hash(Image.open(f))
$$;
```

Create a second UDF that calculates the distance between the phash values of two images:

Copy code

```
CREATE OR REPLACE FUNCTION calc_phash_distance(h1 STRING, h2 STRING)
  RETURNS INT
  LANGUAGE PYTHON
  RUNTIME_VERSION = '3.12'
  PACKAGES = ('imagehash')
  HANDLER = 'run'
AS $$
import imagehash

def run(h1, h2):
  return imagehash.hex_to_hash(h1) - imagehash.hex_to_hash(h2)
$$;
```

Stage the image files and refresh the directory table:

Copy code

```
PUT file:///tmp/image1.jpg @images AUTO_COMPRESS=FALSE;
PUT file:///tmp/image2.jpg @images AUTO_COMPRESS=FALSE;

ALTER STAGE images REFRESH;
```

Call the UDFs:

Copy code

```
SELECT
  calc_phash_distance(
    calc_phash(build_scoped_file_url(@images, 'image1.jpg')),
    calc_phash(build_scoped_file_url(@images, 'image2.jpg'))
  ) ;
```

##### Processing a CSV file with a UDTF

This example uses `SnowflakeFile` to create a UDTF that extracts the contents
of a CSV file and returns the rows in a table.

Create the UDTF with an in-line handler:

Copy code

```
CREATE FUNCTION parse_csv(file_path STRING)
  RETURNS TABLE (col1 STRING, col2 STRING, col3 STRING)
  LANGUAGE PYTHON
  RUNTIME_VERSION = '3.12'
  PACKAGES = ('snowflake-snowpark-python')
  HANDLER = 'csvparser'
AS $$
from snowflake.snowpark.files import SnowflakeFile

class csvparser:
  def process(self, stagefile):
    with SnowflakeFile.open(stagefile) as f:
      for line in f.readlines():
        lineStr = line.strip()
        row = lineStr.split(",")
        try:
          # Read the columns from the line.
          yield (row[1], row[0], row[2], )
        except:
          pass
$$;
```

Stage the CSV file and refresh the directory table:

Copy code

```
PUT file:///tmp/sample.csv @data_stage AUTO_COMPRESS=FALSE;

ALTER STAGE data_stage REFRESH;
```

Call the UDTF, passing a file URL:

Copy code

```
SELECT * FROM TABLE(PARSE_CSV(build_scoped_file_url(@data_stage, 'sample.csv')));
```

##### Processing multiple files

You can read and process multiple files by passing the RELATIVE\_PATH column of a directory table to your handler. For more information on the RELATIVE\_PATH column, see [the output from a directory table query](/user-guide/data-load-dirtables-query#label-data-load-dirtables-query-output).

Note

Depending on your file size and compute needs, you might want to use [ALTER WAREHOUSE](/sql-reference/sql/alter-warehouse) to scale your warehouse up before you execute a statement that reads and processes multiple files.

Call a UDF to process multiple files:
:   The following example calls a UDF within a CREATE TABLE statement to process each file on a stage and then store the results in a new table.

    For demonstration purposes, the example assumes the following:

    - There are multiple text files on a stage named `my_stage`.
    - There is an existing UDF named `get_sentiment` that performs sentiment analysis on unstructured text. The UDF takes a path to a text file as input and returns a value that represents sentiment.

    Copy code

    ```
    CREATE OR REPLACE TABLE sentiment_results AS
    SELECT
      relative_path
      , get_sentiment(build_scoped_file_url(@my_stage, relative_path)) AS sentiment
    FROM directory(@my_stage);
    ```

Call a UDTF to process multiple files:
:   This next example calls a UDTF named `parse_excel_udtf`. The example passes the `relative_path` from the directory table on the stage named `my_excel_stage`.

    Copy code

    ```
    SELECT t.*
    FROM directory(@my_stage) d,
    TABLE(parse_excel_udtf(build_scoped_file_url(@my_excel_stage, relative_path)) t;
    ```

##### Reading files with stage URIs and URLs

File access with `SnowflakeFile` requires scoped URLs by default. This makes your code resilient to file injection attacks. However, you can refer to a file location using a stage URI or a stage URL instead. To do so, you must call the `SnowflakeFile.open` method with the keyword argument `require_scoped_url = False`.

This option is useful when you want to let a caller provide a URI that is accessible only to the UDF owner. For example, you might use a stage URI for file access if you own a UDF and you want to read in your configuration files or machine learning models. We do not recommend this option when you work with files that have unpredictable names, such as files that are created based on user input.

This example reads a machine learning model from a file and uses the model in a function to perform natural language processing for sentiment analysis. The example calls the `open` with `require_scoped_url = False`. In both file location formats (stage URI and stage URL), the UDF owner must have access to the model file.

Create the UDF with an in-line handler:

Copy code

```
CREATE OR REPLACE FUNCTION extract_sentiment(input_data STRING)
  RETURNS STRING
  LANGUAGE PYTHON
  RUNTIME_VERSION = '3.12'
  PACKAGES = ('snowflake-snowpark-python','scikit-learn')
  HANDLER = 'run'
AS $$
from snowflake.snowpark.files import SnowflakeFile
from sklearn.linear_model import SGDClassifier
import pickle

def run(input_data):
  model_file = '@models/NLP_model.pickle'
  # Specify 'mode = rb' to open the file in binary mode.
  with SnowflakeFile.open(model_file, 'rb', require_scoped_url = False) as f:
    model = pickle.load(f)
    return model.predict([input_data])[0]
$$;
```

Stage the model file and refresh the directory table:

Copy code

```
PUT file:///tmp/NLP_model.pickle @models AUTO_COMPRESS=FALSE;

ALTER STAGE models REFRESH;
```

Alternatively, you can specify the UDF with the model’s stage URL to extract the sentiment.

For example, create a UDF with an in-line handler that specifies a file using a stage URL:

Copy code

```
CREATE OR REPLACE FUNCTION extract_sentiment(input_data STRING)
  RETURNS STRING
  LANGUAGE PYTHON
  RUNTIME_VERSION = '3.12'
  PACKAGES = ('snowflake-snowpark-python','scikit-learn')
  HANDLER = 'run'
AS $$
from snowflake.snowpark.files import SnowflakeFile
from sklearn.linear_model import SGDClassifier
import pickle

def run(input_data):
  model_file = 'https://my_account/api/files/my_db/my_schema/models/NLP_model.pickle'
  # Specify 'rb' to open the file in binary mode.
  with SnowflakeFile.open(model_file, 'rb', require_scoped_url = False) as f:
    model = pickle.load(f)
    return model.predict([input_data])[0]
$$;
```

Call the UDF with the input data:

Copy code

```
SELECT extract_sentiment('I am writing to express my interest in a recent posting made.');
```

### Importing directories and repositories

You can use the IMPORTS clause to import entire directories or Git repositories, in addition to individual files.

Note

- The import path for a directory must end with a trailing slash (`/`). For example, `IMPORTS = ('@my_stage/my_dir/')`.
- To rename a directory on import, append `/=custom_name/` to the stage path. The custom name must be a single directory name, not a path. For example, `IMPORTS = ('@my_stage/my_dir/=custom_name/')`.
- Directory imports are not supported in Native Apps.

#### Importing a directory using IMPORTS

You can import a directory using the IMPORTS clause of the [CREATE FUNCTION](/sql-reference/sql/create-function) command.

The following example imports a directory called `my_dir` from a stage named `my_stage` and lists the files it contains.

Copy code

```
CREATE OR REPLACE FUNCTION my_directory_import_list_udf()
  RETURNS STRING
  LANGUAGE PYTHON
  IMPORTS = ('@my_stage/my_dir/')
  PACKAGES = ('snowflake-snowpark-python')
  RUNTIME_VERSION = 3.12
  HANDLER = 'run'
AS $$
import os
import sys
def list_files(directory):
  files = []
  # Walk through the directory and its subdirectories
  for dirpath, _, filenames in os.walk(directory):
    for filename in filenames:
      # Append the relative path to each file to the list
      full_path = os.path.join(dirpath, filename)
      files.append(os.path.relpath(full_path, directory))
  return files
def run():
    directory_path = sys._xoptions["snowflake_import_directory"]
    file_list = list_files(directory_path)
    file_list_str = ' '.join(file_list)
    return file_list_str
$$;
select my_directory_import_list_udf();
```

#### Importing from the root of a stage using IMPORTS

You can import from the root of a stage using the IMPORTS clause of the [CREATE FUNCTION](/sql-reference/sql/create-function) command.

The following example imports from the root of a stage named `my_stage`. The directory is renamed to `customer_dir` to access and read the files within it.

Copy code

```
CREATE OR REPLACE FUNCTION my_directory_import_read_udf()
  RETURNS STRING
  LANGUAGE PYTHON
  RUNTIME_VERSION = 3.12
  IMPORTS = ('@my_stage/=customer_dir/')
  HANDLER = 'run'
AS $$
import sys
import os

with open(os.path.join(sys._xoptions["snowflake_import_directory"], 'customer_dir', 'my_dir', 'file.txt'), "r") as f:
  s = f.read()

def run():
  return s
$$;
select my_directory_import_read_udf();
```

#### Importing from a Git repo using IMPORTS

You can point imports at a Git repo stored in Snowflake (SnowGit), enabling a cleaner deployment workflow.
For more information, see [CREATE GIT REPOSITORY](/sql-reference/sql/create-git-repository).

Copy code

```
CREATE OR REPLACE FUNCTION run_adapter(x STRING)
  RETURNS STRING
LANGUAGE PYTHON
RUNTIME_VERSION = '3.13'
IMPORTS = ('@my_snow_git/branches/main/src/adapter/')
HANDLER = 'run'
AS $$
from adapter.core import transform

def run(x: str) -> str:
  return transform(x)
$$;
```

## Writing files

A UDF handler can write files to a `/tmp` directory created for the query calling the UDF.

Keep in mind that a `/tmp` directory is set aside for a single calling query, yet multiple Python worker processes might be running at the
same time. To prevent collisions, you must ensure either that access to the /tmp directory is synchronized with other Python worker
processes or that the names of files written to /tmp are unique.

For example code, see [Unzipping a staged file](#label-udf-python-unzipping-file-from-stage) in this topic.

Code in the following example writes the input `text` to the `/tmp` directory. It also appends the function’s process ID to ensure the
file location’s uniqueness.

Copy code

```
def func(text):
  # Append the function's process ID to ensure the file name's uniqueness.
  file_path = '/tmp/content' + str(os.getpid())
  with open(file_path, "w") as file:
    file.write(text)
```

For information on writing files, see [Writing files from Snowpark Python UDFs and UDTFs](/developer-guide/snowpark/python/creating-udfs#label-snowpark-python-udf-write-files).

## Unzipping a staged file

You can store a .zip file on a stage, then unzip it in a UDF by using the Python zipfile module.

For example, you can upload a .zip file to a stage, then reference the .zip file at its staged location in the IMPORTS clause when you
create the UDF. At run time, Snowflake will copy the staged file into an import directory from which your code can access it.

For more about reading and writing files, see [Reading files and assets](#label-udf-python-read-files) and [Writing files](#label-udf-python-write-files).

In the following example, the UDF code uses an NLP model to discover entities in text. The code returns an array of these entities.
To set up the NLP model for processing the text, the code first uses the zipfile module to extract the file for the model
(en\_core\_web\_sm-2.3.1) from a .zip file. The code then uses the spaCy module to load the model from the file.

Note that the code writes extracted file contents to the /tmp directory created for the query calling this function. The code uses file
locks to ensure that the extraction is synchronized across Python worker processes; this way, contents are unzipped only once. For more about
writing files, see [Writing files](#label-udf-python-write-files).

For more about the zipfile module, see the [zipfile reference](https://docs.python.org/3/library/zipfile.html). For more about the spaCy
module, see the [spaCy API documentation](https://spacy.io/api).

Create the UDF with an in-line handler:

Copy code

```
CREATE OR REPLACE FUNCTION py_spacy(str STRING)
  RETURNS ARRAY
  LANGUAGE PYTHON
  RUNTIME_VERSION = 3.12
  HANDLER = 'func'
  PACKAGES = ('spacy')
  IMPORTS = ('@spacy_stage/spacy_en_core_web_sm.zip')
AS $$
import fcntl
import os
import spacy
import sys
import threading
import zipfile

 # File lock class for synchronizing write access to /tmp.
 class FileLock:
   def __enter__(self):
       self._lock = threading.Lock()
       self._lock.acquire()
       self._fd = open('/tmp/lockfile.LOCK', 'w+')
       fcntl.lockf(self._fd, fcntl.LOCK_EX)

    def __exit__(self, type, value, traceback):
       self._fd.close()
       self._lock.release()

 # Get the location of the import directory. Snowflake sets the import
 # directory location so code can retrieve the location via sys._xoptions.
 IMPORT_DIRECTORY_NAME = "snowflake_import_directory"
 import_dir = sys._xoptions[IMPORT_DIRECTORY_NAME]

 # Get the path to the ZIP file and set the location to extract to.
 zip_file_path = import_dir + "spacy_en_core_web_sm.zip"
 extracted = '/tmp/en_core_web_sm'

 # Extract the contents of the ZIP. This is done under the file lock
 # to ensure that only one worker process unzips the contents.
 with FileLock():
    if not os.path.isdir(extracted + '/en_core_web_sm/en_core_web_sm-2.3.1'):
       with zipfile.ZipFile(zip_file_path, 'r') as myzip:
          myzip.extractall(extracted)

 # Load the model from the extracted file.
 nlp = spacy.load(extracted + "/en_core_web_sm/en_core_web_sm-2.3.1")

 def func(text):
    doc = nlp(text)
    result = []

    for ent in doc.ents:
       result.append((ent.text, ent.start_char, ent.end_char, ent.label_))
    return result
 $$;
```

## Handling NULL values

The following code shows how NULL values are handled.
For more information, see [NULL values](/developer-guide/udf/python/udf-python-designing#label-udf-python-null-values).

Create the UDF:

Copy code

```
CREATE OR REPLACE FUNCTION py_udf_null(a VARIANT)
  RETURNS STRING
  LANGUAGE PYTHON
  RUNTIME_VERSION = 3.12
  HANDLER = 'udf'
AS $$

def udf(a):
   if not a:
       return 'JSON null'
   elif getattr(a, "is_sql_null", False):
       return 'SQL null'
   else:
       return 'not null'
$$;
```

Call the UDF:

Copy code

```
SELECT py_udf_null(null);
```

```
+-------------------+
| PY_UDF_NULL(NULL) |
|-------------------|
| SQL null          |
+-------------------+
```

Copy code

```
SELECT py_udf_null(parse_json('null'));
```

```
+---------------------------------+
| PY_UDF_NULL(PARSE_JSON('NULL')) |
|---------------------------------|
| JSON null                       |
+---------------------------------+
```

Copy code

```
SELECT py_udf_null(10);
```

```
+-----------------+
| PY_UDF_NULL(10) |
|-----------------|
| not null        |
+-----------------+
```
