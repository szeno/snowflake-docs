# Teradata - SnowConvert AI Scripts Helpers

SnowConvert AI Helpers is a set of classes with functions designed to facilitate the conversion of Teradata script files to Python files that Snowflake can interpret.

SnowConvert AI for Teradata can take in any Teradata SQL or scripts (BTEQ, FastLoad, MultiLoad, and TPump) and convert them to functionally equivalent Snowflake SQL, JavaScript embedded in Snowflake SQL, and Python. Any output Python code from SnowConvert AI will call functions from these helper classes to complete the conversion and create a functionally equivalent output in Snowflake.

The [Snowflake Connector for Python](https://pypi.org/project/snowflake-connector-python/) will also be called to connect to your Snowflake account and run the output Python code created by SnowConvert.

For the latest version information, see the [snowconvert-helpers PyPI page](https://pypi.org/project/snowconvert-helpers/).

Note

The Python package`snowconvert-helpers` supports Python versions 3.6, 3.7, 3.8, and 3.9.

## Script Migration

### Source

Suppose you have the following BTEQ code to be migrated.

Copy code

```
 insert into table1 values(1, 2);
insert into table1 values(3, 4);
insert into table1 values(5, 6);
```

### Output

You should get an output like the one below.

Note

The `log_on`function parameters (‘user’, ‘password’, ‘account’, ‘database’, ‘warehouse’, ‘role’, ‘token’) should be defined by the user.

Copy code

```
 #*** Generated code is based on the SnowConvert AI Python Helpers version 2.0.6 ***

import os
import sys
import snowconvert.helpers
from snowconvert.helpers import Export
from snowconvert.helpers import exec
from snowconvert.helpers import BeginLoading
con = None
def main():
  snowconvert.helpers.configure_log()
  con = snowconvert.helpers.log_on()
  exec("""
    INSERT INTO table1
    VALUES (1, 2)
    """)
  exec("""
    INSERT INTO table1
    VALUES (3, 4)
    """)
  exec("""
    INSERT INTO table1
    VALUES (5, 6)
    """)
  snowconvert.helpers.quit_application()

if __name__ == "__main__":
  main()
```

## Getting Started

To install the package, you should run the following command in your python environment. If you’re not familiar with installing packages in Python, visit the following page on python packages (<https://packaging.python.org/tutorials/installing-packages/>).

Copy code

```
 pip install snowconvert-helpers
```

Once your package is installed, you will be able to run the script migrated code in Python.

## Run the code

To run the migrated code, you just have to open the `Command Prompt` or the `Terminal` and execute the following command.

Copy code

```
 python sample_BTEQ.py
```

If the script has no errors, you will get in your console an output like the one below.

Copy code

```
 Executing: INSERT INTO PUBLIC.table1 VALUES (1, 2).
Printing Result Set:
number of rows inserted
1

Executing: INSERT INTO PUBLIC.table1 VALUES (3, 4).
Printing Result Set:
number of rows inserted
1

Executing: INSERT INTO PUBLIC.table1 VALUES (5, 6).
Printing Result Set:
number of rows inserted
1

Error Code 0
Script done >>>>>>>>>>>>>>>>>>>>
Error Code 0
```

### Passing connection parameters

There are several ways to pass the connection parameters to the connection of the database:

- As parameters in the function call snowconvert.helpers.log\_on inside the python file.
- As positional parameters with the specific order of user, password, account, database, warehouse, and role when the python is being executed from the command line.
- As named parameters with no order restriction of SNOW\_USER, SNOW\_PASSWORD, SNOW\_ACCOUNT, SNOW\_DATABASE, SNOW\_WAREHOUSE, SNOW\_ROLE, SNOW\_QUERYTAG, SNOWAUTHENTICATOR and SNOWTOKEN when the python is being executed from the command line and any of them are passed like –param-VARNAME=VALUE.
- As environment variables named SNOW\_USER, SNOW\_PASSWORD, SNOW\_ACCOUNT, SNOW\_DATABASE, SNOW\_WAREHOUSE, SNOW\_ROLE, SNOW\_QUERYTAG, SNOWAUTHENTICATOR and SNOWTOKEN before python execution.

The previous order specified is the way to determine the precedence.

#### Parameters in the function call

They can be set as positional parameters in the function call as follows.

Copy code

```
    .....
   con = snowconvert.helpers.log_on(
     'myuser',
     'mypassword',
     'myaccount',
     'mydatabase',
     'mywarehouse',
     'myrole',
     5,
     'myauthenticator',
     'mytoken')
   .....
```

Or they can be set any of the named parameters in any order in the function call as follows.

Copy code

```
    .....
   con = snowconvert.helpers.log_on(
     account:'myaccount',
     password:'mypassword',
     user:'myuser',
     warehouse:'mywarehouse',
     login_timeout:5,
     authenticator:'myauthenticator',
     token:'mytoken')
   .....
```

#### Positional parameters

They need to be set in the specific order in the command line as follows.

Copy code

```
 python sample_BTEQ.py myuser mypassword myaccount mydatabase mywarehouse myrole myauthenticator mytokenr
```

Or they can be set only some of the parameters but always starting with the user parameter as follows.

Copy code

```
 python sample_BTEQ.py myuser mypassword myaccount
```

#### Named parameters

They can be set any of the named parameters in any order in the command line as follows (use a single line, multiline shown for readability reasons).

Copy code

```
python sample_BTEQ.py --param-SNOW_WAREHOUSE=mywarehouse
  --param-SNOW_ROLE=myrole
  --param-SNOW_PASSWORD=mypassword
  --param-SNOW_USER=myuser
  --param-SNOW_QUERYTAG=mytag
  --param-SNOW_ACCOUNT=myaccount
  --param-SNOW_DATABASE=mydatabase
  --param-SNOW_AUTHENTICATOR=myauthenticator
  --param-SNOW_TOKEN=mytoken
  --param-PRIVATE_KEY_PATH=myprivatekey
  --param-PRIVATE_KEY_PASSWORD=myprivatekeypassword
```

#### Environment variables

Before calling the python script, any of the following environment variables can be set:

- SNOW\_USER
- SNOW\_PASSWORD
- SNOW\_ACCOUNT
- SNOW\_DATABASE
- SNOW\_WAREHOUSE
- SNOW\_ROLE
- SNOW\_QUERYTAG
- SNOW\_AUTHENTICATOR
- SNOW\_TOKEN
- PRIVATE\_KEY\_PATH
- PRIVATE\_KEY\_PASSWORD

#### Key Pair Authentication

The `log_on` function can also support the key pair authentication process. Review the following [Snowflake documentation](https://docs.snowflake.com/en/user-guide/key-pair-auth) for more information about the key creation . Please notice the required parameters:

`log_on(`

`user='YOUR_USER',`

`account='YOUR_ACCOUNT',`

`role = 'YOUR_ROLE',`

`warehouse = 'YOUR_WAREHOUSE',`

`database = 'YOUR_DATABASE',`

`private_key_path='/YOUR_PATH/rsa_key.p8',`

`private_key_password='YOUR_PASSWORD')`

### Example of passing environment variables

Here is an example of using SNOW\_AUTHENTICATOR, SNOW\_USER and SNOW\_PASSWORD. They must be defined before running the output python file and then run the python generated file.

#### Windows

Copy code

```
 SET SNOW_AUTHENTICATOR=VALUE
SET SNOW_USER=myuser
SET SNOW_PASSWORD=mypassword
python sample_BTEQ.py
```

##### Linux/Mac

Copy code

```
 export SNOW_AUTHENTICATOR=VALUE
export SNOW_USER=myuser
export SNOW_PASSWORD=mypassword
python3 sample_BTEQ.py
```

### Enabling Logging

To enable logging, you should enable an environment variable called SNOW\_LOGGING set as true.

Then, if you want to customize the logging configuration you can pass a parameter to the `snowconvert.helpers.configure_log()` method like this:

Copy code

```
 snowconvert.helpers.configure_log("SOMEPATH.conf")
```

The configuration file should contain the next structure. For more information, see the [Python logging configuration documentation](https://docs.python.org/es/3/library/logging.config.html)

Copy code

```
[loggers] keys=root [handlers] keys=consoleHandler [formatters]
keys=simpleFormatter [logger_root] level=DEBUG handlers=consoleHandler
[logger_simpleExample] level=DEBUG handlers=consoleHandler
qualname=simpleExample propagate=0 [handler_consoleHandler] class=FileHandler
level=DEBUG formatter=simpleFormatter args=('python2.log', 'w')
[formatter_simpleFormatter] format=%(asctime)s -%(levelname)s - %(message)s
```

## Snowflake

Once any migrated code you have been executed, you can go to Snowflake and check your changes or deployments.

Copy code

```
 select * from PUBLIC.table1;
```

You will be able to see the rows you have inserted in the example above.

[![Query result](/static/images/migrations/sc-assets/result.png)](/static/images/migrations/sc-assets/result.png)

## Local Helpers Documentation

First of all, it is required to install the python package named pydoc (Available since version 2.0.2 of snowconvert-helpers).

Copy code

```
 pip install pydoc
```

Then to display the python documentation of the package snowconvert-helpers, you should go to a folder where you have the converted output code and you have a python output.

Copy code

```
D:\bteq\Output>dir

 Volume in drive D is Storage
 Volume Serial Number is 203C-168C

 Directory of D:\bteq\Output

05/25/2021  03:55 PM    <DIR>          .
05/25/2021  03:55 PM    <DIR>          ..
05/25/2021  03:55 PM               630 input_BTEQ.py
               1 File(s)            630 bytes
               2 Dir(s)  1,510,686,502,912 bytes free
```

Located in this directory you need to run:

Copy code

```
 python -m pydoc -b
```

The console will open your preferred browser with the HTML help of the documentation for all the installed packages.

Copy code

```
D:\bteq\Output>python -m pydoc -b
Server ready at http://localhost:61355/
Server commands: [b]rowser, [q]uit
server>
```

This will open the browser with the documentation of your code like:

[![Home page for the generated local documentation](/static/images/migrations/sc-assets/builtin.png)](/static/images/migrations/sc-assets/builtin.png)

Scroll thru the end of the page to see the installed packages. And you will see something similar to:

[![Local installed packages documentation index](/static/images/migrations/sc-assets/scroll.png)](/static/images/migrations/sc-assets/scroll.png)

Clicking in the SnowConvert AI(package) you will see something like:

[![Home page for the snowconvert-helpers documentation](/static/images/migrations/sc-assets/other.png)](/static/images/migrations/sc-assets/other.png)

Clicking in the module helpers will display a screen similar to:

[![Home page for helpers module](/static/images/migrations/sc-assets/module.png)](/static/images/migrations/sc-assets/module.png)

Then you can scroll thru the functions and classes of the module.

[![Functions documentation](/static/images/migrations/sc-assets/final.png)](/static/images/migrations/sc-assets/final.png)

## Known Issues

No issues were found.

## Related EWIs

No related EWIs.

## Technical Documentation

### Functions

All the functions defined in the project.

#### access

Note

**`access`**`(path, mode, *, dir_fd=None, effective_ids=False, follow_symlinks=True)`

##### **Description:**

*Use the real uid/gid to test for access to a path.*

*dir\_fd, effective\_ids, and follow\_symlinks may not be implemented on your platform. If they are unavailable, using them will raise a NotImplementedError.*

*Note that most operations will use the effective uid/gid, therefore this routine can be used in a suid/sgid environment to test if the invoking user has the specified access to the path.*

##### **Parameters:**

- **`path,`** Path to be tested; can be string, bytes, or a path-like [object](http://localhost:65458/builtins.html#object)
- **`mode,`** Operating-system mode bitfield. Can be F\_OK to test existence, or the inclusive-OR of R\_OK, W\_OK, and X\_OK
- **`dir_fd,`** If not None, it should be a file descriptor open to a directory, and path should be relative; path will then be relative to that directory
- **`effective_ids,`** If True, access will use the effective uid/gid instead of the real uid/gid
- **`follow_symlinks,`** If False, and the last element of the path is a symbolic link, access will examine the symbolic link itself instead of the file the link points to

#### at\_exit\_helpers

Note

**`at_exit_helpers`**`()`

##### **Description:**

*Executes at the exit of the execution of the script.*

#### colored

Note

**`colored`**`(text, color='blue')`

##### **Description:**

*Prints colored text from the specified color.*

##### **Parameters:**

- `text`**`,`** The text to be printed
- `color="blue"`**`,`** The color to print

#### configure\_log

Note

**`configure_log`**`(configuration_path)`

##### **Description:**

*Configures the logging that will be performed for any data-related execution on the snowflake connection. The log file is named ‘snowflake\_python\_connector.log’ by default.*

**Parameters:**

- `configuration_path`**`,`** The configuration path of the file that contains all the settings desired for the logging

#### drop\_transient\_table

Note

**`drop_transient_table`**`(tempTableName, con=None)`

##### **Description:**

*Drops the transient table with the specified name.*

**Parameters:**

- `tempTableName`**`,`** The name of the temporary table
- `con=None`**`,`** The connection to be used, if None is passed it will use the last connection performed

#### exception\_hook

Note

**`exception_hook`**`(exctype, value, tback)`

##### **Description:**

**Parameters:**

- `exctype`
- `value`
- `tback`

#### exec

Note

**`exec`**`(sql_string, using=None, con=None)`

##### **Description:**

*Executes a sql string using the last connection, optionally it uses arguments or an specific connection. Examples:*

- *`exec("SELECT * FROM USER")`*
- *`exec("SELECT * FROM USER", con)`*
- *`exec("SELECT * FROM CUSTOMER WHERE CUSTOMERID= %S", customer)`*

**Parameters:**

- `sql_string`**`,`** The definition of the sql
- `using=None`**`,`** The optional parameter that can be used in the sql passed
- `con=None`**`,`** The connection to be used, if None is passed it will use the last connection performed

#### exec\_file

Note

**`exec_file`**`(filename, con=None)`

##### **Description:**

*Reads the content of a file and executes the sql statements contained with the specified connection.*

**Parameters:**

- `filename`**`,`** The filename to be read and executed
- `con=None`**`,`** The connection to be used, if None is passed it will use the last connection performed

#### exec\_os

Note

**`exec_os`**`(command)`

##### **Description:**

*Executes a command in the operating system.*

#### exec\_sql\_statement

Note

**`exec_sql_statement`**`(sql_string, con, using=None)`

##### **Description:**

*Executes a sql statement in the connection passed, with the optional arguments.*

**Parameters:**

- `sql_string`**`,`** The sql containing the string to be executed
- `con`**`,`** The connection to be used
- `using`**`,`** The optional parameters to be used in the sql execution

#### **expands\_using\_params**

Note

**`expands_using_params`**`(statement, params)`

##### **Description:**

*Expands the statement passed with the parameters.*

**Parameters:**

- `statement`**`,`** The sql containing the string to be executed
- `params`**`,`** The parameters of the sql statement

#### **expandvar**

Note

**`expandvar`**`(str)`

##### **Description:**

*Expands the variable from the string passed.*

**Parameters:**

- `str`**`,`** The string to be expanded with the variables

#### **expandvars**

Note

**`expandvars`**`(path, params, skip_escaped=False)`

##### **Description:**

*Expand environment variables of form $var and ${var}. If parameter ‘skip\_escaped’ is True, all escaped variable references (that is, preceded by backslashes) are skipped. Unknown variables are set to ‘default’. If ‘default’ is None, they are left unchanged.*

**Parameters:**

- `path`**`,`**
- `params`**`,`**
- `skip_escaped=False`**`,`**

#### **fast\_load**

Note

**`fast_load`**`(target_schema, filepath, stagename, target_table_name, con=None)`

##### **Description:**

*Executes the fast load with the passed parameters target\_schema, filepath, stagename and target\_table\_name.*

**Parameters:**

- `target_schema`**`,`** The name of the schema to be used in the fast load
- `filepath`**`,`** The filename path to be loaded in the table
- `target_table_name`**`,`** The name of the table that will have the data loaded
- `con=None`**`,`** The connection to be used, if None is passed it will use the last connection performed

#### **file\_exists\_and\_readable**

Note

**`file_exists_and_readable`**`(filename)`

##### **Description:**

**Parameters:**

- `filename`**`,`**

#### **get\_argkey**

Note

**`get_argkey`**`(astr)`

##### **Description:**

*Gets the argument key value from the passed string. It must start with the string ‘–param-’*

**Parameters:**

- `astr`**`,`** The argument string to be used. The string should have a value similar to –param-column=32 and the returned string will be ’32

#### **get\_error\_position**

Note

**`get_error_position`**`()`

##### **Description:**

*Gets the error position from the file using the information of the stack of the produced error.*

#### **get\_from\_vars\_or\_args\_or\_environment**

Note

**`get_from_vars_or_args_or_environment`**`(arg_pos, variable_name, vars, args)`

##### **Description:**

*Gets the argument from the position specified or gets the value from the table vars or gets the environment variable name passed.*

**Parameters:**

- `arg_pos`**`,`** The argument position to be used from the arguments parameter
- `variable_name`**`,`** The name of the variable to be obtained
- `vars`**`,`** The hash with the variables names and values
- `args`**`,`** The arguments array parameter

#### **import\_data\_to\_temptable**

Note

**`import_data_to_temptable`**`(tempTableName, inputDataPlaceholder, con)`

##### **Description:**

*Imports data to a temporary table using an input data place holder.*

**Parameters:**

- `tempTableName,` The temporary table name.
- `inputDataPlaceholder,` The input place holder used that is a stage in the snowflake database
- `con,` The connection to be used

#### **import\_file**

Note

**`import_file`**`(filename, separator=' ')`

##### **Description:**

*Imports the passed filename with the optional separator.*

**Parameters:**

- `filename,` The filename path to be imported
- `separator=' ',` The optional separator

#### **import\_file\_to\_temptable**

Note

**`import_file_to_temptable`**`(filename, tempTableName, columnDefinition)`

##### **Description:**

*Imports the file passed to a temporary table. It will use a public stage named as the temporary table with the prefix Stage\_. At the end of the loading to the temporary table, it will delete the stage that was used in the process.*

**Parameters:**

- `filename,` The name of the file to be read
- `tempTableName,` The name of the temporary table
- `columnDefinition,` The definition of all the fields that will have the temporary table

#### **import\_reset**

Note

**`import_reset`**`()`

##### **Description:**

#### **log**

Note

**`log`**`(*msg, level=20, writter=None)`

##### **Description:**

*Prints a message to the console (standard output) or to the log file, depending on if logging is enabled*

**Parameters:**

- `*msg,` The message to print or log
- `level=20,`
- `writter=None,`

#### **log\_on**

Note

**`log_on`**`(user=None, password=None, account=None, database=None, warehouse=None, role=None, login_timeout=10, authenticator=None)`

##### **Description:**

*Logs on the snowflake database with the credentials, database, warehouse, role, login\_timeout and authenticator passed parameters.*

**Parameters:**

- `user,` The user of the database
- `password` The password of the user of the database
- `database,` The database to be connected
- `warehouse,` The warehouse of the database to be connected
- `role,` The role to be connected
- `login_timeout,` The maximum timeout before giving error if the connection is taking too long to connect
- `authenticator,` The authenticator supported value to use like SNOWFLAKE, EXTERNALBROWSER, SNOWFLAKE\_JWT or OAUTH
- `token,` The OAUTH or JWT token

#### **os**

Note

**`os`**`(args)`

##### **Description:**

**Parameters:**

- `args,`

#### **print\_table**

Note

**`print_table`**`(dictionary)`

##### **Description:**

*Prints the dictionary without exposing user and password values.*

**Parameters:**

- `dictionary,`

#### **quit\_application**

Note

**`quit_application`**`(code=None)`

##### **Description:**

*Quits the application and optionally returns the passed code.*

**Parameters:**

- `code=None,` The code to be returned after it quits

#### **read\_params\_args**

Note

**`read_param_args`**`(args)`

##### **Description:**

*Reads the parameter arguments from the passed array.*

**Parameters:**

- `args,` The arguments to be used

#### **readrun**

Note

**readrun**(line, skip=0)

##### **Description:**

*Reads the given filename lines and optionally skips some lines at the beginning of the file.*

**Parameters:**

- `line,` The filename to be read
- `skip=0,` The lines to be skipped

#### **remark**

Note

**remark**(arg)

##### **Description:**

*Prints the argument.*

**Parameters:**

- `arg,` The argument to be printed

#### **repeat\_previous\_sql\_statement**

Note

**`repeat_previous_sql_statement`**`(con=None, n=1)`

##### **Description:**

*Repeats the previous executed sql statement(s).*

**Parameters:**

- `con=None,` Connection if specified. If it is not passed it will use the last connection performed
- `n=1,` The number of previous statements to be executed again

#### **set\_default\_error\_level**

Note

**`set_default_error_level`**`(severity_value)`

##### **Description:**

**Parameters:**

- `severity_value,`

#### **set\_error\_level**

Note

**`set_error_level`**`(arg, severity_value)`

##### **Description:**

**Parameters:**

- `arg,`
- `severity_value,`

#### **simple\_fast\_load**

Note

**`simple_fast_load`**`(con, target_schema, filepath, stagename, target_table_name)`

##### **Description:**

Executes a simple fast load in the connection and the passed parameter target\_schema, filepath, stagename and target table name.

**Parameters:**

- `arg,` The connection to be used
- `target_schema,` The name of the schema to be used in the fast load
- `filepath,` The filename path to be loaded in the table
- `target_table_name,` The name of the table that will have the data loaded

#### **stat**

Note

**`stat`**`(path, *, dir_fd=None, follow_symlinks=True)`

##### **Description:**

*Perform a stat system call on the given path.* dir\_fd and follow\_symlinks may not be implemented on your platform. If they are unavailable, using them will raise a NotImplementedError. It’s an error to use dir\_fd or follow\_symlinks when specifying path as an open file descriptor

**Parameters:**

- `path,` Path to be examined; can be string, bytes, a path-like [object](http://localhost:55262/builtins.html#object) or  
  open-file-descriptor int
- `dir_fd,` If not None, it should be a file descriptor open to a directory, and path should be a relative string; path will then be relative to that directory
- `follow_symlinks,` If False, and the last element of the path is a symbolic link, stat will examine the symbolic link itself instead of the file the link points to

#### **system**

Note

**`system`**`(command)`

##### **Description:**

*Execute the command in a subshell.*

**Parameters:**

- *`command`*`,`

#### **using**

Note

**`using`**`(*argv)`

##### **Description:**

**Parameters:**

- *`*argv`*`,`

### Classes

All the classes defined in the project

#### BeginLoading Class

This class contains the `import_file_to_tab` static function which provides support for the BEGIN LOADING and associated commands in FastLoad.

##### `import_file_to_tab()`

Parameters:

1. `target_schema_table`
   - the target schema (optional) and table name
2. `define_file`
   - The name of the file to be read
3. `define_columns`
   - The definition of all the columns for the temporary table
4. `begin_loading_columns`
   - The column names to insert. Dictates the order in which values are inserted
5. `begin_loading_values`
   - The list of raw insert values to convert
6. `field_delimiter`
   - The field delimiter
7. *(optional)* `skip_header`
   - The number of rows to skip
8. *(optional)* `input_data_place_holder`
   - The location of the file in a supported cloud provider. Set parameter when the file is not stored locally
9. *(optional)* `con`
   - The connection to be used

#### Export Class

Static methods in the class

- `defaults()`
- `null(value=None)`
- `record_mode(value=None)`
- `report(file, separator=' ')`
- `reset()`
- `separator_string(value=None)`
- `separator_width(value=None)`
- `side_titles(value=None)`
- `title_dashes(value=None, withValue=None)`
- `title_dashes_with(value=None)`
- `width(value=None)`

Data and other attributes defined here

- `expandedfilename = None`
- `separator = ''` \

#### Import Class

Methods in the class

- `reset()`

Static methods in the class

- `file(file, separator=' ')`
- `using(globals, *argv)`

Data and other attributes defined in the class

- `expandedfilename = None`
- `no_more_rows = False`
- `read_obj = None`
- `reader = None`
- `separator = ' '`

#### `Parameters` Class

Data and other attributes defined in the class

- `passed_variables = {}`

#####
