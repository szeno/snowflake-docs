# Snowpark Migration Accelerator: Using SMA with Jupyter Notebooks

## Can I use Python notebook (.ipynb files) in the tool?

**Yes**! Place your notebook files (.ipynb) in the source directory you select as input for the tool. The notebooks can be located in any subfolder within that directory. You can include both Python files (.py) and notebook files (.ipynb) in your source directory or its subfolders. The tool will process all compatible files regardless of their location in the directory structure.

*Converting notebook files (.ipynb) to Python (.py) files offers several advantages:*

1. Better version control: Python files are easier to track changes and manage in version control systems like Git
2. Improved collaboration: Team members can review and edit code more efficiently in standard Python files
3. Easier automation: Python files can be directly executed in automated pipelines and scheduled jobs
4. Cleaner code organization: Python files encourage better code structure and modularity
5. Reduced file size: Python files are typically smaller than notebook files, which contain additional metadata

You have two options:

1. Keep your notebooks as they are if you plan to continue using them in notebook format. SMA can analyze and convert notebooks directly.
2. Extract the Python code into .py files if you want to move away from using notebooks. While this is possible through a workaround, it’s not necessary since SMA can process both notebooks and Python files.

To extract only the Python code from Jupyter notebook files, you can use the nbconvert utility. Here’s how:

1. Install the [nbconvert](https://pypi.org/project/nbconvert/) package using one of these commands:

   - For Windows/Linux: `pip install nbconvert`
   - For MacOS: `pip3 install nbconvert` or `python3 -m pip install nbconvert`
2. Make a backup copy of your Jupyter notebook directory
3. Convert all Jupyter notebooks to Python scripts using the command line:

   - For Windows/Linux:
     `find /path/to/folder/with/notebooks -name '*.ipynb' | xargs python -m nbconvert --to script`
   - For MacOS:
     `find /path/to/folder/with/notebooks -name '*.ipynb' | xargs python3 -m nbconvert --to script`

   This will create Python script files in the same directory as your notebooks.
4. Process the converted Python files by running SMA for Python on the output directory.
