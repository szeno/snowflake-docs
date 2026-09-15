# Code specification

Feature — Generally Available

Currently available in [these regions](/user-guide/cleanrooms/installing-dcr#label-dcr-supported-regions).

Not available in government and VPS deployments.

This specification defines one or more code functions, procedures, or ML Jobs that can be called by a template.

A code specification can contain a maximum of 5 ML jobs, and a maximum of 5 functions and procedures combined.
At least one of `ml_jobs`, `functions`, or `procedures` must be defined.

For examples of different kinds of code specs, see [Example specs](/user-guide/cleanrooms/resources-code-specs#label-dcr-collab-code-spec-examples).

Identifiers in the code specification have the following general requirements:

- **Names**: Must be valid [Snowflake identifiers](/sql-reference/identifiers-syntax) that start with a letter and contain only
  alphanumeric characters and underscores.
- **Quoted identifiers**: Double-quoted identifiers are supported for names with special characters.
- **Case sensitivity**: Unquoted identifiers are case-insensitive; quoted identifiers preserve case.

Copy code

```
api_version: 2.0.0              # Required: Must be "2.0.0"
spec_type: code_spec            # Required: Must be "code_spec"
name: <identifier>              # Required: Unique name of this code spec.
version: <version_id>           # Required: Alphanumeric with underscores (max 20 chars)
description: <description_text> # Optional: Description (max 1,000 chars)

artifacts:                      # Optional: Staged files for import
  - alias: <identifier>         # One or more artifact items...
    stage_path: <stage_path>    # Required: Full stage path. See below for additional requirements.
    description: <description_text>  # Optional: Description (max 500 chars)
    content_hash: <sha256_hash>      # Optional: Lowercase SHA-256 hash for integrity verification

functions:                      # Required if no procedures or ML jobs defined
  - name: <identifier>          # One or more functions...
    type: UDF | UDTF            # Required: Function type
    language: PYTHON            # Required: Currently only PYTHON supported
    runtime_version: <python_version>  # Optional: Python runtime (3.10 - 3.14)
    handler: <handler>          # Required: Handler function
    arguments:                  # Optional: One or more function arguments
      - name: <arg_name>        # Argument name
        type: <sql_type>        # Snowflake SQL type of this argument
    returns: <sql_type>         # Required: Snowflake return type
    packages:                   # Optional: Package dependencies
      - <package_name>          # One or more package items...
    imports:                    # Optional: Artifact aliases to import
      - <artifact_alias>        # One or more import items...
    code_body: |                # Optional: Inline Python code (max 12 MB)
      <inline_python_code>
    description: <description_text>  # Optional: Description of this function.

procedures:                     # Required if no functions or ML jobs defined
  - name: <identifier>          # One or more procedure items...
    language: PYTHON            # Required: Currently only PYTHON supported
    runtime_version: <python_version>  # Optional: Python runtime version (3.10 - 3.14)
    handler: <handler>          # Required: Handler function
    arguments:                  # Optional: One or more procedure arguments
      - name: <arg_name>        # Argument name
        type: <sql_type>        # Snowflake SQL type of this argument
    returns: <sql_type>         # Optional: Return type
    packages:                   # Optional: Package dependencies
      - <package_name>          # One or more package items...
    imports:                    # Optional: Artifact aliases to import
      - <artifact_alias>        # One or more import items...
    code_body: |                # Optional: Inline Python code
      # inline python_code ...
    description: <description_text>  # Optional: Description of this procedure.

ml_jobs:                        # Required if no functions or procedures defined
  - name: <identifier>          # One or more ML job items...
    entrypoint: <script.py>     # Required: Python script (.py) to run
    stage_code_dir: <stage_path> # Required: Stage directory containing the code
    pip_requirements:           # Optional: pip packages to install
      - <package_spec>          # One or more package items...
    description: <description_text> # Optional: Description (max 1,000 chars)
    allow_monitoring: <boolean> # Optional: Allow log monitoring (default: false)
    image_tag: <tag>            # Optional: Container image version (max 64 chars)
```

`api_version`
:   The version of the Collaboration API used. Must be `2.0.0`.

`spec_type`
:   Specification type identifier. Must be `code_spec`.

`name: identifier`
:   A unique name for this code spec within this registry. Must be a valid
    [Snowflake identifier](/sql-reference/identifiers-syntax) with a maximum of 75 characters. This is used as the last name segment
    when calling the function in a template: `cleanroom.code_spec_name$function_name`

`version: version_id`
:   Custom version identifier. Must be alphanumeric with underscores, maximum 20 characters.

`description: description_text` (*Optional*)
:   A description of the code spec (maximum 1,000 characters).

`artifacts` (*Optional*)
:   A list of staged files or packages that can be imported by your functions or procedures, and
    [optionally exposed via handler functions](/user-guide/cleanrooms/resources-code-specs#label-dcr-collab-code-specs-staged-artifacts). Maximum of 5 per spec.

    `alias: identifier`
    :   An alias for referencing this artifact in imports. When referencing this alias within this spec, use the bare alias name rather than

        `cleanroom.spec_name$alias`.

    `stage_path: stage_path`
    :   Full stage path to the artifact file. For example, `@DB.SCHEMA.STAGE/path/file.whl`.

    - **The stage must be internal.** External stages aren’t supported.
    - **The stage must have DIRECTORY enabled**: The stage containing artifacts must have `DIRECTORY = (ENABLE = TRUE)` set.
    - **Stage path format**: Must follow `@[DB.]SCHEMA.STAGE/path/to/file.ext` format.
    - **No path traversal**: Stage paths can’t contain `..` or `\`.
    - **This artifact must exist**: The file must exist at the specified stage path when the code spec is registered.
    - **The stage must have SNOWFLAKE\_SSE server-side encryption enabled.** When creating or altering the stage, set
      `ENCRYPTION = (TYPE = 'SNOWFLAKE_SSE')`.
    - **If you push, delete, or update a staged code file,** you must call `ALTER STAGE {stage name} REFRESH` to ensure that the
      collaboration has the latest information from the stage. Code updates are supported only before you register the code spec, as this is
      when the version is assigned and the hash checksum calculated.

    `description: description_text` (*Optional*)
    :   A description of the artifact (maximum 500 characters).

    `content_hash: sha256_hash` (*Optional*)
    :   Lowercase SHA-256 hash for integrity verification (64 hex characters).

`functions` (*Required if no procedures or ML jobs are defined*)
:   A list of UDF or UDTF definitions.

    `name: identifier`
    :   The function name to expose to the calling template. Must be a valid [Snowflake identifier](/sql-reference/identifiers-syntax).

    `type`
    :   The function type. One of `UDF` or `UDTF`.

    `language`
    :   The function language. Currently only `PYTHON` is supported.

    `runtime_version: python_version` (*Optional*)
    :   Python runtime version to use. Supported versions: `3.10` to `3.14`.

    `handler: handler`
    :   The name of the handler function in the function code to call when `name` is called.

    `arguments` (*Optional*)
    :   Function arguments as a list of name-type pairs. Types must be valid Snowflake SQL types.

    `returns: sql_type`
    :   The return type. For UDFs, use a SQL type such as STRING or FLOAT. For UDTFs, use `TABLE(column_definitions)`.

    `packages` (*Optional*)
    :   A list of packages used by this code. This can be any of [these Anaconda Python packages](https://repo.anaconda.com/pkgs/snowflake/)
        or [these Snowpark API packages](/user-guide/cleanrooms/demo-flows/snowpark#label-dcr-snowpark-udf). For example: `snowflake-snowpark-python`, `numpy`.

    `imports` (*Optional*)
    :   A list of artifacts to import. These must be aliases from the artifacts list in this spec.

    `code_body` (*Optional*)
    :   Inline Python code. Mutually exclusive with staged imports. Maximum size is 12 MB.

    `description: description_text` (*Optional*)
    :   A description of the function (maximum 500 characters).

`procedures` (*Required if no functions or ML jobs are defined*)
:   A list of stored procedure definitions. Fields are similar to `functions`, except there is no `type` field.

`ml_jobs` (*Required if no functions or procedures are defined*)
:   A list of ML job definitions. Maximum of 5 ML jobs per code spec. This limit is independent of the
    functions and procedures limit (which is also 5). Unlike functions and procedures, ML jobs run in
    an isolated container on a compute pool, which enables GPU acceleration, distributed training, arbitrary pip
    packages, and long-running asynchronous execution.

    For more information, see [ML Jobs in Data Clean Rooms](/user-guide/cleanrooms/ml-jobs).

    `name: identifier`
    :   The ML job name. Must be a valid Snowflake identifier with a maximum of 255 characters. Names are
        case-insensitive and must be unique within the code spec. This name is used in the template call pattern:
        `cleanroom.code_spec_name$ml_job_name(compute_pool, num_instances, warehouse, args_json)`.

    `entrypoint: script.py`
    :   The Python file to execute as the entry point. Must be a `.py` file (case-sensitive), for example
        `train.py` or `run_pipeline.py`. Module path notation such as `module.function` isn’t supported: the
        entrypoint must always be a Python file.

    `stage_code_dir: stage_path`
    :   The stage directory containing the Python code to run. Must follow the format
        `@DB.SCHEMA.STAGE/path`
        and point to a directory, not a file.

        - **The stage must be internal.** External stages aren’t supported.
        - **The stage must have DIRECTORY enabled**: Set `DIRECTORY = (ENABLE = TRUE)` when creating the stage.
        - **The stage must have SNOWFLAKE\_SSE encryption enabled**: Set `ENCRYPTION = (TYPE = 'SNOWFLAKE_SSE')` when
          creating the stage.
        - **No path traversal**: Stage paths can’t contain `..` or backslashes.
        - **Upload files without compression**: When you upload files with `PUT`, set `AUTO_COMPRESS = FALSE`
          so that files are stored as-is. Compressed uploads change the file names and contents, which breaks
          the entrypoint and integrity verification.
        - **Refresh the directory after uploading files**: Call `ALTER STAGE stage_name REFRESH` after uploading
          or updating any files. The collaboration uses a directory view to access staged code. Without a refresh,
          newly uploaded files aren’t visible to the collaboration and creation can stall.
        - **Supported contents**: The directory can contain any file type, including Python scripts (`.py`),
          wheel packages (`.whl`), JAR files (`.jar`), shared libraries (`.so`), archive files (`.zip`,
          `.tar.gz`), configuration files (`.json`, `.yaml`), and serialized model artifacts (`.pkl`,
          `.joblib`). Nested subdirectories are supported. Only the `entrypoint` file must be a `.py` script.
        - **Maximum 500 files per directory**: The `stage_code_dir` can contain at most 500 files
          (including all files in subdirectories). Registration fails if this limit is exceeded.
        - **Total directory size**: Keep the combined size of the `stage_code_dir` under approximately 2 GB.
        - **Integrity verification**: At registration, the system computes a SHA-256 hash for every file
          in the directory. When the collaboration loads the code, all hashes are re-verified. If any file
          has been modified, added, or removed since registration, the template request fails. Re-register
          the code spec after modifying staged files.

        Note

        ML Jobs code specs registered before the
        [June 18, 2026 release](/release-notes/2026/other/2026-06-18-dcr) (Clean Rooms API Version 16.3)
        don’t have content hashes and can’t be added to a collaboration. For resolution steps, see
        [ML Jobs troubleshooting](/user-guide/cleanrooms/v2/troubleshooting#ml-jobs).

    `pip_requirements` (*Optional*)
    :   A list of pip package requirements to install in the container at runtime. For example:
        `scikit-learn>=1.0`, `xgboost`, `pandas`. Unlike function and procedure code specs, ML jobs can use
        any pip-installable package — not just the Anaconda-approved bundle.

    `description: description_text` (*Optional*)
    :   A description of the ML job (maximum 1,000 characters).

    `allow_monitoring: boolean` (*Optional*)
    :   Whether to allow the analysis runner to view container logs for this ML job. Default: `false`.

    `image_tag: tag` (*Optional*)
    :   The ML runtime image version to use. Maximum 64 characters. If omitted, the collaboration uses the
        latest available runtime image, resolved when the code spec is added to a collaboration.
        The default image is updated when new
        runtime versions are released.
        Pinning `image_tag` to a specific version is recommended so that your code spec runs against a
        known set of pre-installed libraries and runtime behavior.

        All pinned versions are preserved unchanged across patches.

    The following example registers a code spec with two ML jobs:

    Copy code

    ```
    CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.REGISTRY.REGISTER_CODE_SPEC(
    $$
    api_version: 2.0.0
    spec_type: code_spec
    name: my_ml_model
    version: V0
    ml_jobs:
      - name: my_train_job
        entrypoint: train.py
        stage_code_dir: '@MY_DB.PUBLIC.MY_STAGE/ml_project'
        image_tag: "2.9.0"
        pip_requirements:
          - pandas
          - xgboost
          - scikit-learn
      - name: my_score_job
        entrypoint: score.py
        stage_code_dir: '@MY_DB.PUBLIC.MY_STAGE/ml_project'
        image_tag: "2.9.0"
        pip_requirements:
          - pandas
          - xgboost
          - scikit-learn
    $$);
    ```

    Templates that reference ML Jobs code specs call the generated procedure using the pattern
    `cleanroom.<code_spec_name>$<ml_job_name>(compute_pool, num_instances, warehouse, args_json)`.
