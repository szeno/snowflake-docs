# Manage packages in notebooks on Container Runtime

Snowflake Notebooks on Container Runtime currently support common `pip` commands and workflows for managing packages. This includes the following common workflows:

- Use a package spec, such as a `requirements.txt` file, to set up a notebook environment.
- View all packages installed in a notebook environment.
- Uninstall packages.
- Export a package spec that captures the current notebook environment.
- Update packages in the notebook environment.

In addition to these workflows, Notebooks on Container Runtime supports other `pip` workflows.

## Prerequisite

Ensure that an external access integration (EAI) for PyPI is set up in the notebook or that Artifact Repository is active in the Snowflake account. For more information about PyPI EAI, see [Enable external access integrations in Snowsight](/user-guide/ui-snowsight/notebooks-external-access#label-notebooks-enable-eai-ui). For information about Artifact Repository, see [Artifact Repository overview](/developer-guide/udf/python/udf-python-packages#label-python-udfs-pypi).

## View all packages installed in a notebook environment

- To view a full list of the packages currently installed in the notebook environment and their respective versions, from a notebook cell, run the following command:

  Copy code

  ```
  !pip freeze
  ```

## Install individual packages in your notebook environment

You can modify your notebook’s Python environment by installing individual packages using inline `pip` commands in your notebook cells.

- To install a package, from a notebook cell, run the following command:

  Copy code

  ```
  !pip install <package_name>
  ```

## Install packages from a package spec to set up a notebook environment

You can modify your notebook’s Python environment using a package spec, such as a `requirements.txt` file, to install your desired packages. The following example shows how to install packages from a `requirements.txt` file stored locally. You can also install packages from a `requirements.txt` file stored in an internal or external stage.

1. Upload the `requirements.txt` file to the notebook.
   For information about the `requirements.txt` file, see [Requirements File Format](https://pip.pypa.io/en/stable/reference/requirements-file-format/).
2. To install all of the packages, from a notebook cell, run the following command:

   Copy code

   ```
   !pip install -r requirements.txt
   ```

## Update package versions in the notebook environment

1. From a notebook cell, run one of the following commands that corresponds to the version of the package you want to update to:

   - Latest version:

     Copy code

     ```
     !pip install <package_name> --upgrade
     ```
   - Specific version:

     Copy code

     ```
     !pip install <package_name> --<version>
     ```
2. To confirm that the update is complete, when prompted, restart the notebook kernel.

## Uninstall packages from a notebook environment

Complete the following steps to uninstall all of the packages that you installed using a package spec in the notebook environment.

1. Verify that a `requirements.txt` file exists in the notebook environment.
2. From a cell in the notebook, run the following command:

   Copy code

   ```
   !pip uninstall -r requirements.txt
   ```
3. To confirm that the packages were uninstalled, when prompted, restart the notebook kernel.

## Export packages in your notebook environment as a package spec

You can export a package spec that captures the current state of the notebook environment. With this package spec, you can quickly replicate
the notebook environment.

1. From a cell in the notebook, run the following command:

   Copy code

   ```
   !pip list --format=freeze <filename>.txt
   ```
2. To upload the file to a stage, run the following command:

   Copy code

   ```
   session.file.put("<path to file>/<filename>.txt", "@mystage/prefix1")
   ```

For more information about storing files in a stage, see [Store files in a Snowflake stage](/user-guide/ui-snowsight/notebooks-work-with-files#label-snowsight-file-stage).
