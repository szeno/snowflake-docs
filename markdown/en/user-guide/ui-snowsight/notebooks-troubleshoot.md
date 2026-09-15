# Troubleshoot errors in Snowflake Notebooks

The following scenarios can help you troubleshoot issues that can occur when using Snowflake Notebooks.

## Total number of notebooks exceeds the limit in Snowsight

The following error occurs when the total number of notebooks in your account exceeds 6,000 and you refresh the Notebooks list:

```
Result size for streamlit list exceeded the limit. Streamlit list was truncated.
```

Users can still create new notebooks; however, Snowflake recommends that you remove notebooks that are no longer being used by the account.

## Notebooks (Warehouse Runtime) error when updating a package

Snowflake has deprecated the older `snowflake-ml` package, which is no longer supported. It has been removed from the package selector and is
not available in the Snowflake Anaconda channel. If you are using `snowflake-ml` and try to add, remove, or update packages in your
notebooks, those notebooks will fail because `snowflake-ml` is no longer accessible.

To avoid issues, switch to `snowflake-ml-python`, which is the correct package for Snowflake ML.

## Plotly error

```
st.plotly_chart(fig, render_mode='svg')

WebGL is not supported by your browser - visit https://get.webgl.org for more info.
```

Plotly will switch to webgl if there are more than 1,000 datapoints.

## AttributeError: `NoneType`

The following error occurs when a cell is renamed to the same name as an existing variable in the notebook:

```
AttributeError: ‘NoneType’ object has no attribute ‘sql’
```

For example, you have the following in a Python cell called `cell1`:

Copy code

```
session = get_active_session() #establishing a Snowpark session
```

If you then rename `cell2` to “session”, and reference “session” in `cell3`, Notebooks attempts to reference “session” (the cell
name) and not the Snowpark session, causing an error.

## Early disconnection

The notebook session runs as a stored procedure. The timeout is 30 minutes on Warehouse Runtime and 60 minutes on Container Runtime. If your
notebook unexpectedly disconnects before the timeout, your ACCOUNTADMIN or the warehouse owner might have set the [STATEMENT\_TIMEOUT\_IN\_SECONDS](/sql-reference/parameters#label-statement-timeout-in-seconds)
parameter to a particular value (for example, 5 minutes), which limits how long all statements can run on the warehouse, including notebook sessions.
This parameter is set at the warehouse or account level, and when it is set for both a warehouse and a session, the lowest non-zero value is enforced.

To allow the notebook to run longer, you can use the default warehouse [SYSTEM$STREAMLIT\_NOTEBOOK$WAREHOUSE](/user-guide/warehouses-overview#label-default-warehouse) or
change the [STATEMENT\_TIMEOUT\_IN\_SECONDS](/sql-reference/parameters#label-statement-timeout-in-seconds) parameter to a longer duration.

For details on the idle time setting, see [Idle time and reconnection](/user-guide/ui-snowsight/notebooks-setup#label-notebooks-idle-time-property).

## Fail to reconnect

If you do not have cookies enabled on your browser, you cannot automatically reconnect to the notebook session while it should still be
active (before timing out due to inactivity). When you reopen the notebook, an error message displays:

```
Notebook connection lost and cannot reconnect. Restart or end session.
```

Restarting the session will end the current [EXECUTE NOTEBOOK](/sql-reference/sql/execute-notebook) query and start a new session. Ending the session
will end the current [EXECUTE NOTEBOOK](/sql-reference/sql/execute-notebook) query.

If you do not take either action, the current [EXECUTE NOTEBOOK](/sql-reference/sql/execute-notebook) query will continue running on the warehouse,
shown in **Query History**.

## Unable to connect due to firewall

The following popup occurs when you try to start your notebook:

```
Something went wrong. Unable to connect. A firewall or ad blocker might be preventing you from connecting.
```

Ensure that `*.snowflake.app` and `*.snowflake.com` are on the allowlist in your network (including content filtering systems), and
can connect to Snowflake. For Streamlit apps using container runtimes, also add `*.snowflakecomputing.app` to the allowlist.
When these domains are on the allowlist, your apps can communicate with Snowflake servers without any restrictions.
However, in some cases adding these domains may not be sufficient due to network policies blocking subpaths under them. If this occurs,
contact your network administrator.

In addition, to prevent any issues connecting to the Snowflake backend, ensure that WebSockets are not blocked in your network configuration.

## Missing packages

The following message occurs in a cell output if you’re trying to use a package that is not installed in your notebook environment:

```
ModuleNotFoundError: Line 2: Module Not Found: snowflake.core. To import packages from Anaconda, install them first using the package
selector at the top of the page.
```

Import the necessary package by following the instructions on the [Import Python packages to use in notebooks](/user-guide/ui-snowsight/notebooks-import-packages) page.

### Missing package from existing notebook

New versions of notebooks are continually being released and notebooks are auto-upgraded to the latest version.
Sometimes, when upgrading an old notebook, the packages in the notebook environment aren’t compatible with the upgrade.
This could possibly cause the notebook to fail to start.

The following is an example of an error message when the `Libpython` package is missing:

```
SnowflakeInternalException{signature=std::vector<sf::RuntimePathLinkage> sf::{anonymous}::buildRuntimeFileSet(const sf::UdfRuntime&, std::string_view, const std::vector<sf::udf::ThirdPartyLibrariesInfo>&, bool):"libpython_missing", internalMsg=[XP_WORKER_FAILURE: Unexpected error signaled by function 'std::vector<sf::RuntimePathLinkage> sf::{anonymous}::buildRuntimeFileSet(const sf::UdfRuntime&, std::string_view, const std::vector<sf::udf::ThirdPartyLibrariesInfo>&, bool)'
Assert "libpython_missing"[{"function": "std::vector<sf::RuntimePathLinkage> sf::{anonymous}::buildRuntimeFileSet(const sf::UdfRuntime&, std::string_view, const std::vector<sf::udf::ThirdPartyLibrariesInfo>&, bool)", "line": 1307, "stack frame ptr": "0xf2ff65553120",  "libPythonOnHost": "/opt/sfc/deployments/prod1/ExecPlatform/cache/directory_cache/server_2921757878/v3/python_udf_libs/.data/4e8f2a35e2a60eb4cce3538d6f794bd7881d238d64b1b3e28c72c0f3d58843f0/lib/libpython3.9.so.1.0"}]], userMsg=Processing aborted due to error 300010:791225565; incident 9770775., reporter=unknown, dumpFile= file://, isAborting=true, isVerbose=false}
```

To resolve this error, try the following steps:

- Refresh the webpage and start the notebook again.
- If the issue persists, open the package selector and check whether all installed packages are valid. In the drop-down for each package, you
  can see the available versions. Selecting the latest version of the package usually clears the error.

## Missing notebook

Notebooks are schema-level objects, meaning they are stored within a specific schema in a database. If a schema is dropped (deleted), all
objects contained within it (including notebooks) are also dropped. If you do not see a notebook that previously existed, it’s possible that
the schema it belonged to has been dropped. In this case, the notebook is permanently deleted and cannot be recovered.

To help prevent accidental loss of notebooks:

- Review the objects contained in a schema before dropping it.
- Limit schema drop privileges to avoid accidental or unauthorized deletions.
- Consider exporting notebook contents in version-controlled scripts outside of the notebook.

If your notebook is missing and the schema still exists, ensure that your current role has the necessary privileges to view the schema and
its objects.

## Read-only file system issue

Some Python libraries download or cache data to a local user directory. However, the default user directory `/home/udf` is read-only.
To work around this, set the path as `/tmp` which is a writable location.
Note that the environment variable used to set the write directory may vary depending on which library you are using.
The following is a list of known libraries that present this issue:

- matplotlib
- HuggingFace
- catboost

### matplotlib example

You might see this warning when using matplotlib:

```
Matplotlib created a temporary cache directory at /tmp/matplotlib-2fk8582w because the default path (/home/udf/.config/matplotlib) is
not a writable directory; it is highly recommended to set the MPLCONFIGDIR environment variable to a writable directory, in particular
to speed up the import of Matplotlib and to better support multiprocessing.
```

Resolve this warning using this code, which sets the `MPLCONFIGDIR` variable to `/tmp/`:

Copy code

```
import os
os.environ["MPLCONFIGDIR"] = '/tmp/'
import matplotlib.pyplot as plt
```

### Huggingface example

You might see this warning when using Huggingface:

```
Readonly file system: `/home/udf/.cache`
```

The following code sets the `HF_HOME` and `SENTENCE_TRANSFORMERS_HOME` variables to `/tmp/` to get rid of this error:

Copy code

```
import os
os.environ['HF_HOME'] = '/tmp'
os.environ['SENTENCE_TRANSFORMERS_HOME'] = '/tmp'

from sentence_transformers import SentenceTransformer
model = SentenceTransformer("Snowflake/snowflake-arctic-embed-xs")
```

## Output message is too large when using `df.collect()`

The following message is displayed in the cell output when you run `df.collect()`:

```
MessageSizeError: Data of size 522.0 MB exceeds the message size limit of 200.0 MB.
This is often caused by a large chart or dataframe. Please decrease the amount of data sent to the browser,
or increase the limit by setting the config option server.maxMessageSize.
Click here to learn more about config options.
Note that increasing the limit may lead to long loading times and large memory consumption of the client's browser and the Streamlit server.
```

Snowflake Notebooks automatically truncates results in the cell output for large datasets in following cases:

- All SQL cell results.
- Python cell results if it’s a `snowpark.Dataframe`.

The issue with the above cell is that `df.collect()` returns a `List` instead of `snowpark.Dataframe`. Lists are not automatically
truncated. To get around this issue, directly output the results of the DataFrame.

Copy code

```
df
```

## Notebook crashes when using `df.to_pandas()` on Snowpark DataFrames

When running `df.to_pandas()`, all the data is loaded into memory and may result in the Notebook session terminating if the data size
exceeds the associated Notebook warehouse’s memory limit.

### Example 1: Exporting a Snowpark table to pandas DataFrame

Copy code

```
data = session.table("BIG_TABLE")
df = data.to_pandas() # This may lead to memory error
```

#### Workaround for example 1

The following example shows how you can rewrite the code to read in the table with Snowpark pandas.

Copy code

```
# Import Snowpark pandas
import modin.pandas as pd
import snowflake.snowpark.modin.plugin
# Create a Snowpark pandas DataFrame from BIG_TABLE
df = pd.read_snowflake("BIG_TABLE")
# Keep working with your data using the pandas API
df.dropna()
```

### Example 2: Referencing a SQL cell containing large results

If you have the following code in a SQL cell called `cell1`, the output result is 500M rows.

Copy code

```
SELECT * from BIG_TABLE
```

Then, when you fetch the results into a pandas DataFrame, the notebook crashes because the data is too large to fit in memory:

Copy code

```
df = cell1.to_pandas() # This may lead to memory error
```

In general, for large datasets, Snowflake recommends that you avoid using `df.to_pandas()`. Instead, to operate on your data with pandas, use
the Snowpark pandas API and a [Snowpark-optimized warehouse](/user-guide/warehouses-snowpark-optimized). The
[Snowpark pandas API](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/modin/index) lets you run your
pandas code directly on your data in Snowflake with the query performed in SQL. This allows you to run pandas code on data that does not
fit in the notebook’s memory.

#### Workaround for example 2

In the second cell referencing example above, you can convert your SQL cell result to a Snowpark DataFrame first. Then, you can convert it
into Snowpark pandas.

Copy code

```
SELECT * from BIG_TABLE
snowpark_df = cell1.to_df()
df = snowpark_df.to_snowpark_pandas()
# Keep working with your data using the Snowpark pandas API
```

For more details, see [pandas on Snowflake in notebooks](/user-guide/ui-snowsight/notebooks-use-with-snowflake#label-notebooks-snowpark-pandas).

## Unable to connect due to VPN split tunneling

If your VPN is configured to use split tunneling, you must add both `*.snowflake.com` and `*.snowflake.app` to your network
policy allowlist. If your account uses per-account URLs (enabled by setting
[ENABLE\_PER\_ACCOUNT\_APP\_SERVICE\_URL](/sql-reference/parameters#label-enable-per-account-app-service-url) to `TRUE`),
you can use a more specific entry: `*.orgname-account-name.region.cloud.snowflake.app`.

## Notebook does not exist error

The following message is displayed in the cell output when you attempt to run a notebook whose name contains special characters:

```
Notebook <name> does not exist or not authorized
```

Notebook names are Snowflake identifiers. Any notebook name with special characters such as dots and spaces must be enclosed in double
quotes to meet identifier rules.

## Package version conflict

If you run a non-interactive notebook that loads a package version from the base image, and then attempt to install a new version, the new
version will not be loaded. Ensure that the package version matches the base image. In an interactive notebook, you’ll be prompted to restart the
notebook to use the new version.

## Scheduled SPCS notebook failing to run

Before running a scheduled notebook on Container Runtime, you must create an image repository. If an image repository is missing, the following error is displayed:

```
Failed to retrieve image.
```

For details on how to create an image repository, see [CREATE IMAGE REPOSITORY](/sql-reference/sql/create-image-repository).

## Log messages failing to appear in output

If log messages aren’t appearing in the notebook output, ensure that logs are directed to `stdout`. Here is an example of how to configure
logging correctly:

Copy code

```
import logging
import sys

# Create a logger
logger = logging.getLogger()

# Set the log level
logger.setLevel(logging.DEBUG)

# Create a stream handler that writes to sys.stdout
stdout_handler = logging.StreamHandler(sys.stdout)

# Set the log format (optional)
formatter = logging.Formatter('%(levelname)s: %(message)s')
stdout_handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(stdout_handler)

# Test the logging output
logger.warning("This is a warning message.")
```

To highlight errors, you can send them to `stderr` using a similar approach. Alternatively, if you’re working with Streamlit in Snowflake Notebooks, you can use its built-in functions for clearer formatting:

Copy code

```
import streamlit as st st.warning("This is a warning message.")
st.write("This is a normal message.")
st.error("This is an error message.")
```

## Unable to execute notebook

When you create a notebook using [CREATE NOTEBOOK](/sql-reference/sql/create-notebook), the notebook does not automatically have a live version in the
version stage. If you attempt to run a notebook using [EXECUTE NOTEBOOK](/sql-reference/sql/execute-notebook) without setting a live version first, or if
you create a notebook and it gets dropped, the following error occurs:

```
Live version is not found.
```

To resolve this error, use the following command to set the initial live version:

Copy code

```
ALTER NOTEBOOK <name> ADD LIVE VERSION FROM LAST;
```
