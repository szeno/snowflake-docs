# Build a Snowpark project

The `snow snowpark build` command builds the Snowpark project as one or more `.zip` archive files that can be used by the `deploy` command. The command builds the archives using only the `src` directory specified in the project file.

Caution

`snow snowpark build` executes code from packages in your `requirements.txt` as part of the build process. Only build projects and dependencies you trust.

Copy code

```
snow snowpark build
```

```
Resolving dependencies from requirements.txt
  No external dependencies.
Preparing artifacts for source code
  Creating: app.zip
Build done.
```

Additional options:

- `--allow-shared-libraries`: Allows shared (`.so`/`.dll`) libraries, when using packages installed through `pip`.
- `--ignore-anaconda`: Doesn’t look up packages on the Snowflake Anaconda channel.
- `--index-url`: Specifies the base URL of the Python Package Index to use for package lookup. This URL should point to a repository compliant with PEP 503 (the simple repository API) or a local directory laid out in the same format.
- `--skip-version-check`: Skips comparing versions of dependencies between requirements and Anaconda.
- `--project [-p]`: Specifies the path where the Snowpark project resides. Defaults to the current working directory.
