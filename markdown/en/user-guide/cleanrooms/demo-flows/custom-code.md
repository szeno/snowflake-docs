# Upload and run custom functions in a clean room

End-of-life notice

The legacy Provider and Consumer Data Clean Rooms are being discontinued. See the
[end-of-life timeline](/user-guide/cleanrooms/pc-eol) for dates and migration guidance.

## Overview

You can upload custom Python UDFs and UDTFs into your clean room and run them from your templates to perform complex data actions. These
actions include machine learning or customized data manipulation within a query, as part of a single-step or
[multi-step flow](/user-guide/cleanrooms/multistep-flows). Python is the only coding language supported for custom UDFs.

Your uploaded code can import and use packages from an [approved bundle of Python packages](https://repo.anaconda.com/pkgs/snowflake/)
and the [Snowpark API](/user-guide/cleanrooms/demo-flows/snowpark#label-dcr-snowpark-udf).

Templates in a clean room can call code uploaded by the account that added the template. Uploaded code can’t be viewed or downloaded.
Snowflake scans uploaded code for security issues before installing the code.

There are different mechanisms for uploading code into a clean room, depending on your role:

**Providers**

- [Inline code upload](#label-dcr-provider-submitted-code): If you want to upload code using the default compute resources for a
  clean room, and need to use only the standard bundle of Python packages (including the Snowpark API), you should upload inline code.
- [Snowpark Container Services running within a clean room](/user-guide/cleanrooms/demo-flows/snowpark#label-dcr-snowpark-spcs): If you need more control over the
  environment, such as specifying additional compute or custom libraries, you can run a container within a clean room.

**Consumers**

- [Inline upload with template](#label-dcr-consumer-submitted-code): Consumers can upload and run a template bundled with code. The
  code is bound to the template, and must be approved by the clean room provider.

This topic shows how to upload and run custom Python UDFs and UDTFs as either a provider or a consumer.

Tip

For background information about how to develop your own Python UDFs in a clean room, see the following topics:

- [How UDFs work on Snowflake](/developer-guide/udf/python/udf-python-creating) for general background on how to write Python
  functions in Snowflake.
- [How to write UDTFs in Snowflake](/developer-guide/udf/python/udf-python-tabular-functions) if you want to return tables from
  your functions.
- [How to create and upload custom templates into a clean room.](/user-guide/cleanrooms/demo-flows/custom-templates) UDFs/UDTFs are
  called from a custom template.
- [Using Snowpark in clean rooms](/user-guide/cleanrooms/demo-flows/snowpark) (if you want to call your UDFs from Snowpark).

### Entry points for uploaded code

Each bundle of uploaded code can define multiple functions that call each other, but a bundle exposes only one handler function.
This handler function can be called by templates created or run by anyone who uses the clean room. If the code creates internal tables,
these tables can be accessed as described in [Using internal tables for multistep workflows](/user-guide/cleanrooms/multistep-flows).

For example, if you uploaded a function named `simple_add` that takes in two numeric parameters, you can call it from a template as shown
here. The function is always
referenced using the scope `cleanroom`. For example, a template could call `simple_add` like this:

Copy code

```
SELECT cleanroom.simple_add({{ price | sqlsafe | int }}, {{ tax | sqlsafe | int }}) ...
```

Tip

If the provider wants to run the code above, they must alias all SELECT columns that use an aggregate or custom function, because a
results table is generated behind the scenes:

Copy code

```
SELECT
  cleanroom.simple_add(
    {{ price | sqlsafe | int }}, {{ tax | sqlsafe | int }}
    ) AS TOTAL_ITEM_COST
...
```

You can upload multiple functions in a single package, and functions within a single package can call each other, but functions can’t call
functions within other packages. (They can call the handler functions, though.) For example, if you have a clean room where you upload two
packages, each with a handler function and two helper functions:

**Clean room with two uploaded Python packages**

| Package 1 | Package 2 |
| --- | --- |
| - **Handler function A** - Helper function **A1** - Helper function **A2** | - **Handler function B** - Helper function **B1** - Helper function **B2** |

Expand

Show lessSee more

- Code uploaded by either party (provider or consumer) can be run by templates submitted by either party.
- A template can call function A or function B, but not A1, A2, B1, or B2.
- Function A can call function B, and the reverse.
- Function A can’t call B1 or B2 and Function B can’t call A1 or A2.
- A1 can call A2 and the reverse. A1 and A2 can call B. A1 and A2 can’t call B1 or B2.
- B1 can call B2 and the reverse. B1 and B2 can call A. B1 and B2 can’t call A1 or A2.

### Updating or deleting custom functions

You can upload or overwrite an existing function or template that you uploaded, but you can’t delete an existing function or template. The
only way to “remove” a function is to create a dummy function with the exact same name and signature that always succeeds.

Uploading a function with the same signature as one that you previously uploaded will overwrite the existing function, where a
signature means the case-insensitive function name of an external handler, plus the data types of all its arguments, in the same order.
Argument names are not part of the signature. You can’t overwrite a function uploaded by another account.

Because the signature must match when you update a function, you cannot change the signature of an existing function: if you upload the
function `foo(name VARIANT age INTEGER)` and then upload the function `foo(name VARIANT age FLOAT)`, the second function will be added
to the clean room in addition to the first, because the argument types differ.

## Provider-submitted code

Provider-submitted functions can be uploaded as inline code or from a Snowflake stage. Both techniques are covered here.

Your uploaded code can natively import and use packages from an [approved set of Python packages](https://repo.anaconda.com/pkgs/snowflake/).
If you need a non-default package, you must use [Snowpark Container Services in a clean room](/user-guide/cleanrooms/demo-flows/snowpark#label-dcr-snowpark-spcs) to host your
code.

You can’t view uploaded provider code, even your own code, so be sure to include a copy of exactly what you upload into a clean room.

- [Overview](#overview-1)
- [Important notes about versioning](#important-notes-about-versioning)
- [Uploading provider-written inline functions](#uploading-provider-written-inline-functions)
- [Uploading provider-written functions from a stage](#uploading-provider-written-functions-from-a-stage)
- [Troubleshooting syntax errors or scan failures in uploaded code](#troubleshooting-syntax-errors-or-scan-failures-in-uploaded-code)
- [Security scans](#security-scans)
- [Uploading multiple Python functions in a single patch (bulk uploading)](#uploading-multiple-python-functions-in-a-single-patch-bulk-uploading)
- [Provider-written code examples](#provider-written-code-examples)

### Overview

Here is a high-level view of how a provider adds code to a clean room:

1. The provider creates and configures the clean room in the normal way.
2. The provider uploads a bundle by calling `provider.load_python_into_cleanroom`. You can either
   [upload your code inline](#label-dcr-upload-code-inline) directly within that procedure, or
   [upload a code file to a stage](#label-dcr-provider-code-from-stage), then provide the stage location to that procedure.

   Although each bundle can include multiple functions, only one handler function is exposed for each upload. To expose multiple functions to
   templates, upload each handler separately or do a bulk upload (described below).
3. If the clean room is exposed externally, security checks are run before the code is installed in the clean room, and you must call
   `provider.view_cleanroom_scan_status` to confirm that security checks have passed before incrementing the default version.
4. After each successful upload, a [new patch version of the clean room is generated](/user-guide/cleanrooms/dcr-versions). You
   must then increase the default version by calling `provider.set_default_release_directive` with the new patch number.
5. Create and upload a custom template that calls handlers in your code. The template must call the handler function using the `cleanroom` scope, that is: `cleanroom.my_function(...)`.
6. The consumer runs your template the same way as any other template.

   Tip

   If the consumer encounters a mount error when they install a clean room with custom code, this can indicate a syntax error in the code.

You can find code examples demonstrating this flow in the [provider-written code example section](#label-dcr-provider-written-code-examples).

### Important notes about versioning

Every time the provider uploads a function, it increases the clean room patch number (and there is a limit of 99 patch numbers). Therefore,
do your best to test and debug your code thoroughly before adding it to the clean room to reduce version updates during development.

You can upload multiple packages at once in a [single bulk upload](#label-dcr-bulk-upload-python) to reduce the number of patches
generated. However, bulk uploads can make it more challenging to debug if the upload has a security scan issue, because the file that
caused the problem isn’t reported in the error response.

If you do update a patch number, customers using the clean room UI might need to refresh the page to see the change. Customers using the
API should see changes immediately, but there can be a delay, depending on the available resources.
[Learn more about clean room versioning.](/user-guide/cleanrooms/dcr-versions)

### Uploading provider-written inline functions

You can upload the code inline in the `code` parameter of `provider.load_python_into_cleanroom`. Here is an example of uploading a
simple function inline:

Copy code

```
CALL samooha_by_snowflake_local_db.provider.load_python_into_cleanroom(
$cleanroom_name,
'simple_add',                         -- Name used to call the UDF from a template.
['first INTEGER', 'second INTEGER'],  -- Arguments of the UDF, specified as '<variable_name> <SQL type>' pairs.
['numpy', 'pandas'],                  -- Packages imported by the UDF.
'INTEGER',                            -- SQL return type of UDF.
'add_two',                            -- Handler function in your code called when external name is called.
$$
import numpy as np   # Not used, but you can load supported packages.
import pandas as pd

def add_two(first, second):
    return first + second
$$
);
```

The calling template calls `cleanroom.simple_add` to call this function.
The [provider examples](#label-dcr-provider-written-code-examples) demonstrate how to upload inline code.

### Uploading provider-written functions from a stage

You can upload Python files to a clean room stage and reference the stage when you call `provider.load_python_into_cleanroom`. Loading
code from a stage allows you to develop the code in your local system in an editor, avoid copy/paste errors when loading it inline, and
also have better versioning control of your source code. Note that you can upload multiple files in a single procedure call, but only one
handler function is exposed for each upload.

Code is loaded from a stage into the clean room when you call `load_python_into_cleanroom`; later changes to the code on the stage are not
propagated to the clean room.

To upload your UDF to a stage:

1. Create your .py file and make it available in a location where you can upload it to a Snowsight stage.
2. To get the name of the stage for your clean room, call `provider.get_stage_for_python_files`. You must use the specified stage; you cannot use
   an arbitrary stage that you create.
3. Upload the .py file to the stage for your clean room. There are
   [several ways to do this](/user-guide/data-load-local-file-system-stage), including using the CLI, Snowsight, or
   language-specific drivers.
4. Call `provider.load_python_into_cleanroom` with the stage location, handler, external name, arguments, and return type.
   Templates in your clean room can now call the function.

The following example code shows how to load code into a clean room from a stage.

Copy code

```
-- Save the following code as reverser.py:
--import numpy as np
--def main(some_string):
--  '''Return the reverse of a string plus a random number 1-10'''
--  return some_string[::-1] + str(np.random.randint(1,10))

-- Get the stage for your clean room.
CALL samooha_by_snowflake_local_db.provider.get_stage_for_python_files($cleanroom_name);

-- Save the file to the stage. Here is how to do it by using the Snowflake CLI
PUT file://~/reverser.py <STAGE_NAME> overwrite=True auto_compress=False;

-- Load the code from the stage into the clean room.
CALL samooha_by_snowflake_local_db.provider.load_python_into_cleanroom(
    $cleanroom_name,
    'reverse', -- Name used to call the function
    ['some_string  STRING'], -- Arguments and SQL types
    ['numpy'],               -- Any required packages
    ['/reverser.py'],        -- Relative path to file on stage
    'STRING',                -- Return type
    'reverser.main'          -- <FILE_NAME>.<FUNCTION_NAME>
);

-- Uploading code, even from a stage, increases the patch number.
CALL samooha_by_snowflake_local_db.provider.set_default_release_directive(
  $cleanroom_name, 'V1_0', <NEW_PATCH_NUMBER>);

-- Upload a template that calls the function.
CALL samooha_by_snowflake_local_db.provider.add_custom_sql_template(
    $cleanroom_name,
    $udf_template_name,
    $$
    SELECT
      p.status,
      cleanroom.reverse(p.status)
    FROM SAMOOHA_SAMPLE_DATABASE.DEMO.CUSTOMERS AS p
    LIMIT 100;
    $$
);

-- Switch to the consumer account and run the template to see the results.
```

The [provider examples](#label-dcr-provider-written-code-examples) demonstrate uploading code from a stage.

### Troubleshooting syntax errors or scan failures in uploaded code

If you upload a function that fails because of a syntax error, or if a security scan fails, an unpublishable patch can be generated. Therefore, you should thoroughly test your code before upload to ensure that it has no syntax errors.

You can see the list of packages, and their review status, by running the following SQL command, providing the clean room ID in the place indicated:

`SHOW VERSIONS IN APPLICATION PACKAGE samooha_cleanroom_cleanroom_id;`

### Security scans

A security scan is run after any action that generates a new patch version in an external clean room, such as when the provider uploads
Python into the clean room. (Consumer-submitted code, described on this page, does not trigger a security scan.) Internal clean rooms do
not run security scans, but if you change an internal clean room to an external clean room, it will trigger a security scan for that patch.
A clean room patch cannot be published externally until the patch has been scanned.

Snowflake Data Clean Rooms uses the [Snowflake Native App security scan framework](/developer-guide/native-apps/security-run-scan).
Follow the [native app security best practices](/developer-guide/native-apps/security-app-requirements) to avoid security scan errors.

You can perform additional patch-creating actions before the last security scan is complete. However, you must wait for
`provider.view_cleanroom_scan_status` to show success before you can update the default release directive in order to serve the
latest version of the clean room.

### Uploading multiple Python functions in a single patch (bulk uploading)

If you want to upload multiple Python packages to your clean room, you can call `prepare_python_for_cleanroom` multiple
times, then call `load_prepared_python_into_cleanroom` once to scan, upload, and generate a single patch for your clean room. The
following example demonstrates uploading a UDF and a UDTF using bulk uploading:

Copy code

```
---- Add custom inline UDF ----
CALL samooha_by_snowflake_local_db.provider.prepare_python_for_cleanroom(
    $cleanroom_name,
    'get_next_status',  -- Name of the UDF. Can be different from the handler.
    ['status VARCHAR'], -- Arguments of the UDF, specified as (variable name, SQL type).
    ['numpy'],          -- Packages needed by UDF.
    [],                 -- When providing the code inline, this is an empty array.
    'VARCHAR',          -- Return type of UDF.
    'get_next_status',  -- Handler.
    $$
import numpy as np
def get_next_status(status):
  """Return the next higher status, or a random status
  if no matching status found or at the top of the list."""

  statuses = ['MEMBER', 'SILVER', 'GOLD', 'PLATINUM', 'DIAMOND']
  try:
    return statuses[statuses.index(status.upper()) + 1]
  except:
    return 'NO MATCH'
    $$
);

---- Add custom inline UDTF. ----
CALL samooha_by_snowflake_local_db.provider.prepare_python_for_cleanroom(
    $cleanroom_name,
    'get_info',  -- Name of the UDTF. Can be different from the handler.
    ['hashed_email VARCHAR', 'days_active INT', 'status VARCHAR', 'income VARCHAR'],   -- Name/Type arguments of the UDTF.
    ['numpy'],         -- Packages used by UDTF.
    [],                -- When providing the code inline, this is an empty array.
    'TABLE(hashed_email VARCHAR, months_active INT, level VARCHAR)',  -- Return type of UDTF.
    'GetSomeVals',     -- Handler class name.
$$
class GetSomeVals:
  def __init__(self):
    self.month_days = 30

  def process(self, hashed_email, days_active, status, income):
    '''Change days into rough months, and also return whether we
    think the user's membership status is lower, higher, or equal to
    what is expected, based on their income.'''

    months_active = days_active // self.month_days
    brackets = ['0-50K', '50K-100K', '100K-250K', '250K+']
    statuses = ['MEMBER', 'SILVER', 'GOLD', 'PLATINUM']
    if(statuses.index(status) < brackets.index(income)):
      level = 'low'
    elif(statuses.index(status) > brackets.index(income)):
      level = 'high'
    else:
      level = 'equal'

    yield(hashed_email, months_active, level)
$$
);

-- Upload all stored procedures.
-- Note the new patch number returned by this procedure. Keep this number for later use.
CALL samooha_by_snowflake_local_db.provider.load_prepared_python_into_cleanroom($cleanroom_name);

-- Set the release directive specified by the last load_python_into_cleanroom call.
CALL samooha_by_snowflake_local_db.provider.set_default_release_directive($cleanroom_name, 'V1_0', <PATCH_NUMBER>);
```

### Provider-written code examples

The following examples demonstrate adding provider-written UDFs and UDTFs to a clean room.

Download the following examples and then upload them as worksheet files in your Snowflake account. You need separate accounts for
the provider and consumer, each with the clean rooms API installed. Replace the information as noted in the sample files.
[See instructions to upload a SQL worksheet into your Snowflake account](/user-guide/cleanrooms/tutorials-and-samples#label-dcr-list-of-sample-notebooks-and-worksheets).

- [Provider example code](/static/samples/clean-rooms/provider-udf-p.sql)
- [Consumer example code](/static/samples/clean-rooms/provider-udf-c.sql)
- [Loading a file from a stage](/static/samples/clean-rooms/udf_from_stage.ipynb). Run this notebook after you run the provider
  example to try loading a UDF from a stage.
- [Uploading multiple Python functions in a single patch.](/static/samples/clean-rooms/upload-multiple-python-packages.sql)
  This is a single-account internal testing clean room; you can use the same account for both the provider role and the consumer role.

## Consumer-submitted code

Consumer-uploaded code is bundled and uploaded with a custom template using the [consumer template upload flow](/user-guide/cleanrooms/demo-flows/custom-templates#label-dcr-consumer-written-templates). The uploaded code can be called by any template in the clean room.

To upload code as a consumer, you should understand [custom template syntax](/user-guide/cleanrooms/demo-flows/custom-templates).

Note that any code uploaded by a consumer can be seen by the provider when they request permission to upload. The consumer code is also
visible whenever a provider or consumer examines the template.

Here is an overview of the steps to upload custom consumer code:

1. The provider creates the clean room in the standard way and then invites the consumer.
2. The consumer installs and configures the clean room in the standard way.
3. The consumer prepares a template that calls the UDF or UDTF within the `cleanroom` namespace. For example, to call the
   consumer-defined `calculate_tax` function, a simple template might look like the following snippet:

   Copy code

   ```
   SELECT {{ cleanroom.calculate_tax(p.cost) }} AS Tax FROM my_db.my_sch.sales AS p;
   ```
4. The consumer prepares their Python code. We recommend using double quotation marks (`" "`) rather than single quotation marks (`' '`)
   in your code to avoid extra escaping needed later. Your code can reference [these supported Python libraries](https://repo.anaconda.com/pkgs/snowflake/).
5. The consumer passes their Python code into `consumer.generate_python_request_template`. The procedure returns the Python code as a
   stored procedure, with a placeholder for the custom JinjaSQL template. There are several multi-line strings in the template that use
   `$$` as multi-line delimiters.
6. The consumer replaces the template placeholder in the output from `generate_python_request_template` with their JinjaSQL template.
7. In the combined template, escape any single quotes like this: `\'`. This is because single quotes will be used as the outermost
   delimiter for the entire multi-line procedure string when you upload it to the clean room. Here is an example of a stored procedure that
   includes the consumer Python code and custom template, with character escaping:

   Copy code

   ```
   BEGIN

   CREATE OR REPLACE FUNCTION CLEANROOM.custom_compare(min_status STRING, max_status STRING, this_status STRING)
   RETURNS boolean
   LANGUAGE PYTHON
   RUNTIME_VERSION = 3.10
   PACKAGES = (\'numpy\')

   HANDLER = \'custom_compare\'
   AS $$
   import numpy as np

   def custom_compare(min_status:str, max_status:str, this_status:str):
     statuses = [\'MEMBER\', \'SILVER\', \'GOLD\', \'PLATINUM\']
     return ((statuses.index(this_status) >= statuses.index(min_status)) &
             (statuses.index(this_status) <= statuses.index(max_status)))
   $$;

   -- Custom template
   LET SQL_TEXT varchar := $$
   SELECT
     c.status,
     c.hashed_email
   FROM IDENTIFIER( {{ my_table[0] }} ) as c
   WHERE cleanroom.custom_compare({{ min_status }}, {{ max_status }}, c.status);
   $$;

   LET RES resultset := (EXECUTE IMMEDIATE :SQL_TEXT);
   RETURN TABLE(RES);

   END;
   ```
8. The consumer calls `consumer.create_template_request` with the combined template. Use single quotation marks (`' '`) instead of
   double dollar sign delimiters (`$$...$$`) around the code you provide for stored procedure in the `template_definition` argument. For example:

   Copy code

   ```
   CALL samooha_by_snowflake_local_db.consumer.create_template_request(
     $cleanroom_name,
     $template_name,
     '
   BEGIN

   -- First, define the Python UDF.
   CREATE OR REPLACE FUNCTION CLEANROOM.custom_compare(min_status STRING, max_status STRING, this_status STRING)
   RETURNS boolean
   LANGUAGE PYTHON
   RUNTIME_VERSION = 3.10
   PACKAGES = (\'numpy\')

   HANDLER = \'custom_compare\'
   AS $$
   import numpy as np

   def custom_compare(min_status:str, max_status:str, this_status:str):
     statuses = [\'MEMBER\', \'SILVER\', \'GOLD\', \'PLATINUM\']
     return ((statuses.index(this_status) >= statuses.index(min_status)) &
             (statuses.index(this_status) <= statuses.index(max_status)))
   $$;

   -- Then define and execute the SQL query.
   LET SQL_TEXT varchar := $$
   SELECT
     c.status,
     c.hashed_email
   FROM IDENTIFIER( {{ my_table[0] }} ) as c
   WHERE cleanroom.custom_compare({{ min_status }}, {{ max_status }}, c.status);
   $$;

   -- Execute the query and then return the result.
   LET RES resultset := (EXECUTE IMMEDIATE :SQL_TEXT);
   RETURN TABLE(RES);

   END;
   ');
   ```
9. The consumer and provider continue with the standard
   [consumer-defined template flow](/user-guide/cleanrooms/demo-flows/custom-templates#label-dcr-consumer-written-templates):

   1. The provider views the template request (`provider.list_pending_template_requests`) and then approves it by calling
      `approve_template_request`. In the request, the provider can see the template and the bundled code.
   2. The consumer checks the request status (`consumer.list_template_requests`), and when the status is APPROVED, runs the template (`consumer.run_analysis`).

   Consumer code uploads don’t trigger a security scan or affect the clean room patch number.

### Consumer-written code examples

The following examples demonstrate adding provider-written UDFs to a clean room.

Download the following examples and then upload them as worksheet files in your Snowflake account. You need separate accounts for
the provider and consumer, each with the clean rooms API installed. Replace the information as noted in the sample files.
[See instructions to upload a SQL worksheet into your Snowflake account](/user-guide/cleanrooms/tutorials-and-samples#label-dcr-list-of-sample-notebooks-and-worksheets).

- [Consumer-written, consumer-run code: Provider worksheet](/static/samples/clean-rooms/consumer-udf-p.sql)
- [Consumer-written, consumer-run code: Consumer worksheet](/static/samples/clean-rooms/consumer-udf-c.sql)
- [Consumer-written, provider-run code: Provider worksheet](/static/samples/clean-rooms/p-run-c-uploaded-code-p.sql)
- [Consumer-written, provider-run code: Consumer worksheet](/static/samples/clean-rooms/p-run-c-uploaded-code-c.sql)
