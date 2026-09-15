# Work with files in notebooks

This topic describes how you can upload and access files from your Snowflake Notebooks.

## Files in notebook environments

When you create a new notebook, the main notebook file is created. By default, the notebook file is assigned the same name as the notebook.

Files are stored in an internal stage that represents your notebook environment, and they persist between sessions. You can view them in the
**Files** tab on the left side of the notebook. To display a preview of the contents of the file, select the file name.

## Temporary filesystem in a notebook environment

Your notebook has a temporary filesystem that is available during an active session. Any files created during the session are saved in
this temporary stage. Files on the temporary stage will not be available after you end the current notebook session.

The following code creates a file called `myfile.txt` and writes some text in it:

Copy code

```
with open("myfile.txt",'w') as f:
    f.write("abc")
f.close()
```

You can access this file during the same session it was created.

Use the `listdir()` method to list the files in the temporary stage:

Copy code

```
import os
os.listdir()
```

Now disconnect from your current session and reconnect. Try the `listdir()` method again and `myfile.txt` file will not be listed.

## Persist files across notebook sessions

To persist your files across notebook sessions:

- [Store files in a Snowflake stage](#label-snowsight-file-stage)
- [Use Snowsight to upload files into a notebook](#label-snowsight-notebooks-add-files-from-local)
- [Sync with files from Git](#label-snowsight-notebooks-sync-git)

### Store files in a Snowflake stage

If you want your files to persist between sessions and reference these files across different notebooks, use a Snowflake stage to store them.
You can upload files from your local computer onto the stage and use file operations from Snowpark API to access them from your notebook.

#### Example

This example shows how to create a stage and store and retrieve files from it from your notebook.

To create a stage called `permanent_stage`, run the follow code in a SQL cell:

Copy code

```
CREATE OR REPLACE STAGE permanent_stage;
```

Next, to create a file called `myfile.txt` with some text in it, run the following code in a Python cell:

Copy code

```
with open("myfile.txt",'w') as f:
  f.write("abc")
f.close()
```

Note that at this point, `myfile.txt` is stored in the notebook’s temporary filesystem. To move this to the stage, you can use Snowpark
API to upload the `myfile.txt` to your `permanent_stage`:

Copy code

```
from snowflake.snowpark.context import get_active_session
session = get_active_session()

put_result = session.file.put("myfile.txt","@PERMANENT_STAGE", auto_compress= False)
put_result[0].status
```

If you disconnect your session and reconnect, you can run the following code in a SQL cell to verify whether the file still appears:

Copy code

```
LS @permanent_stage;
```

### Use Snowsight to upload files into a notebook

You can upload files from your local computer to be used in your Snowflake notebook.

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Projects** » **Notebooks**.
3. In the **Files** tab, next to the database object explorer, select the [![Add a dashboard tile](/static/images/snowsight/snowsight-dashboards-add-tile-icon.png)](/static/images/snowsight/snowsight-dashboards-add-tile-icon.png) icon to select files to upload.
4. Browse and select or drag and drop files into the dialog.
5. Select **Upload** to upload your file.

Note

If you’re uploading files to use as Python packages in your notebook, consider that only `.py` and `.zip` files are supported when running on
Warehouse Runtime. For Container Runtime, `.whl` (wheel) files are also supported. If you’re importing a package as a `.zip` file, ensure there
is an `__init__.py` file at the root to indicate that it’s a Python package.

Uploaded files are saved to the notebook’s internal stage and persisted between sessions. You can reference uploaded files using their
local paths from the notebook file. See [Referencing files in notebooks](#label-reference-files-in-notebooks).

Note

Only internal stages are supported. External stages (for example, Amazon S3, Google Cloud Storage, or Azure Blob Storage) are not supported.

### Use other editing environments to upload or download files

In addition to using the file browser in Snowsight, you can also work with files in the Notebooks stage using a local Snowpark
Python session, Snowflake CLI, or SnowSQL.

#### Local Snowpark Python session

You can upload and download files from your local computer into a notebook stage using the `session.file.put` and `session.file.get`
methods in Snowpark Python. This requires starting a Snowpark session from your local editing environment (not within Snowsight). For example:

Copy code

```
# Upload a local file to the notebook stage
res = session.file.put("aaa.csv", """snow://notebook/DEMO_DB.PUBLIC."JSMITH dbapi test"/versions/live""", overwrite=True)
# Download a file from the notebook stage to your local computer
res = session.file.get("""snow://notebook/DEMO_DB.PUBLIC."JSMITH dbapi test"/versions/live/aaa.json""", "aaa.csv")
```

Note

This method does not work from the SnowSQL CLI. You must run the method from a Python environment with an active Snowpark session.

#### SnowSQL commands

You can also upload or download files from the Notebooks stage using SnowSQL commands directly:

Copy code

```
-- Download a file from the notebook stage to your local computer
GET 'snow://notebook/SNOWPUBLIC.NOTEBOOKS."ADMIN_SPCS"/versions/live/ADMIN_SPCS.ipynb' 'file://download';

-- Upload a file from your local computer to the notebook stage
PUT 'file://test.json' 'snow://notebook/SNOWPUBLIC.NOTEBOOKS.ADMIN_SPCS/versions/live' overwrite = TRUE;
```

Before running these commands, make sure you have set the appropriate database, schema, and warehouse in your SnowSQL session.

### Sync with files from Git

If your notebook is connected to Git, then any files in the same Git folder as your notebook will be displayed in the **Files** tab.

For more information on working with files in Git, see [Sync notebooks with a Git repository](/user-guide/ui-snowsight/notebooks-snowgit).

## Referencing files in notebooks

Each file in the notebook environment has a stage path and a local path. You can use these paths to reference the file in the notebook.

### Referencing a local path with Python

In general, Python libraries use the local path to the file as reference to the file. For example, the following code accesses the `data.csv`
file that was uploaded to the same directory as the notebook that this code is running in:

Copy code

```
import pandas as pd
df = pd.read_csv("data.csv")
```

### Referencing the stage path with SQL

With SQL, Snowflake references files based on the stage path. The stage path for a file in your notebook is based on the following format:

Copy code

```
snow://notebook/<DATABASE>.<SCHEMA>.<NOTEBOOK_NAME>/versions/live/<file_name>
```

To find the stage path associated with the files in your notebook stage using the **Copy path** menu:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Projects** » **Notebooks**.
3. In the **Files** tab, next to the database object explorer, select the [![More options](/static/images/snowsight/snowsight-worksheet-explorer-ellipsis.png)](/static/images/snowsight/snowsight-worksheet-explorer-ellipsis.png) icon next to the file you
   want to get the path for.
4. Select **Copy path**. This copies the path of the file to your clipboard.

Then you can use the following SQL statement to list the stage file details:

Copy code

```
LIST 'snow://notebook/<DATABASE>.<SCHEMA>.<NOTEBOOK_NAME>/versions/live/data.csv'
```

## Limitations and considerations

- Load files before starting your notebook session. If you load files after a session has started, you have to restart your session to
  access the files.
- No restrictions on file types to upload.
- The size limit per file is 250 MB or less.
- Files that are written to a local path in the notebook are not displayed in the **Files** tab. However, you can still use the file in
  your notebook code.

  For example, if you create a file, `data.json`, you can access it as shown in the following code even though it won’t be visible
  in the **Files** UI:

  Copy code

  ```
  # Generate sample JSON file
  with open("data.json", "w") as f:
   f.write('{"fruit":"apple", "size":3.4, "weight":1.4}\n{"fruit":"orange", "size":5.4, "weight":3.2}')
  # Read from local JSON file (File doesn't show in UI)
  df = pd.read_json("data.json", lines=True)
  df
  ```
- Opening another `.ipynb` file that is not the main notebook file is not supported.

## Additional resources

> - [How to work with files in Snowflake Notebooks](https://github.com/Snowflake-Labs/snowflake-demo-notebooks/blob/main/Working%20with%20Files/Working%20with%20Files.ipynb)
> - [Navigating and Browsing Files in Snowflake Notebooks](https://github.com/Snowflake-Labs/snowflake-demo-notebooks/blob/main/Navigating%20and%20Browsing%20Files/Navigating%20and%20Browsing%20Files.ipynb)
