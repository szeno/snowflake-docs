# Working with the file system

Feature — Generally Available

Available to all AWS, Azure, and GCP commercial regions. PrivateLink is supported.

## The Workspaces file system

The files shown in the left-hand pane of the Workspaces environment represent the contents of your Workspace directory, which is the notebook’s
working directory.

![Workspaces file system](/static/images/snowsight/workspaces/workspaces-file-system.png)

Running `ls` in the Workspace directory lists all files and folders in the directory, including notebooks and any other project assets.

## Referencing files

You can reference files in the current Workspace directory by relative path. For example, you want to read in a notebook and a sample dataset (in CSV) that are in your workspace:

```
ml-intent-prediction/
├── data/
│   └── sample_data.csv
├── notebooks/
│   └── analysis.ipynb
└── utilities.py
```

In a Python cell, run the following code:

Copy code

```
import pandas as pd

df = pd.read_csv("../data/sample_data.csv")
df.head()
```

## Writing files

If you own or have the “Edit access” to the Workspace, you can create folders, save and/or remove files programmatically using a Python cell
or the notebook terminal.

For example, to print your current working directory, run:

Copy code

```
%pwd
```

To create a folder, run:

Copy code

```
%mkdir my_folder
```

The folder `my_folder` will appear in the Workspace file explorer in the left pane shortly.

To save a file in `my_folder`, change directory to the folder first:

Copy code

```
%cd my_folder
```

Then run:

Copy code

```
%%writefile notes.txt
Hello, world!
This is line 2.
```

Or use:

Copy code

```
!echo "Hello, world!" > sample.txt
```

To delete the last file, run:

Copy code

```
!rm sample.txt
```

Note

- If you run the commands in the terminal, click **Refresh** in the Workspace’s ellipsis menu to see the folders/files display or be removed.
- Appending is not supported.

### The `/tmp` directory

The `/tmp` directory is also read/write and is suitable for scratch work or temporary data that does not need to persist.

An example of writing a file to `/tmp`:

Copy code

```
file_path = "/tmp/sample.txt"

with open(file_path, "w") as f:
    f.write("Hello from Python!\\nThis is a sample file saved in /tmp.")

print(f"File written to {file_path}")
```

To list files in the `/tmp` directory, run the following:

Copy code

```
%%bash
cd /tmp
ls
```

To store files for later use outside a Workspace, write them to a Snowflake stage with write access using Snowpark file operation APIs.

To learn more about required stage privileges, see [write access](/user-guide/security-access-control-privileges#label-access-control-privileges-stage). For Snowpark file operations, see
[Snowpark file operation APIs](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/1.6.1/api/snowflake.snowpark.FileOperation#snowflake.snowpark.FileOperation).
