# Initialize a Snowpark project

The first step when creating Snowpark projects is to create a project boilerplate. The `snow init` command creates a fully-functional boilerplate with the following structure:

```
snowflake.yml      - project definition
requirements.txt   - project dependencies
app/               - code of functions and procedures
  __init__.py
  functions.py     - example functions
  procedures.py    - example procedures
  common.py        - example "shared library"
```

- The `snowflake.yml` file contains a [project definition](/developer-guide/snowflake-cli/project-definitions/about) that describes the project structure that the `snow snowpark` commands use.
- The `app` directory stores the project code. You can think about it as a Python module. All functions and procedures must reside in this directory.
- The `requirements.txt` file contains project dependencies. Snowflake CLI supports all requirement specifiers supported by `pip`, such as a package name, a URL for a package, or a local path.

  You can add more dependencies (such as previously deployed custom packages) as `imports` parameters in the function and procedure declarations in the [project definition](/developer-guide/snowflake-cli/project-definitions/about).
