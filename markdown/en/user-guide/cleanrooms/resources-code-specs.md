# Code specs

Feature — Generally Available

Currently available in [these regions](/user-guide/cleanrooms/installing-dcr#label-dcr-supported-regions).

Not available in government and VPS deployments.

Any collaborator can package custom Python functions, stored procedures, or ML Jobs with collaboration templates. Templates in turn reference the code spec to perform complex data actions in the collaboration.
Common usage includes machine learning or customized data manipulation within a query. Your uploaded code can
import and use packages from an [approved bundle of Python packages](https://repo.anaconda.com/pkgs/snowflake/)
and the [Snowpark API](/user-guide/cleanrooms/demo-flows/snowpark#label-dcr-snowpark-udf).

Custom code can be called only via templates, and not directly.

Note

Python is the only coding language supported for function and stored procedure code specs.
ML Jobs code specs also run Python, but inside a Snowpark Container Services container
on a compute pool, where you can install additional packages using `pip_requirements`.

## Choosing a code spec type

Code specs support three execution types. Choose based on what your template needs to do:

- **ML Jobs** — For resource-intensive ML workloads: training, scoring, hyperparameter optimization, or any
  workload that needs GPU acceleration, distributed compute, or packages beyond the Anaconda bundle.
  See [ML Jobs in Data Clean Rooms](/user-guide/cleanrooms/ml-jobs).
- **Functions (UDF / UDTF)** — For logic that calculates and returns a value callable inline from SQL.
  See [User-defined functions overview](/developer-guide/udf/udf-overview).
- **Stored procedures** — For logic that needs to execute DML or DDL, or orchestrate multiple database
  operations in sequence.
  See [Stored procedures overview](/developer-guide/stored-procedure/stored-procedures-overview) and
  [Choosing stored procedure or UDF](/developer-guide/stored-procedures-vs-udfs).

The following sections show you how to upload and use code specs.

## Implementing custom code specs

Here is how to upload and use a code spec:

**The code submitter:**

1. [Creates and registers the code](#label-dcr-collaboration-create-and-register-code-spec) by calling [REGISTER\_CODE\_SPEC](/user-guide/cleanrooms/collaboration-api-reference#label-dcr-collab-register-code-spec).

   The code can be inline in the spec, or [linked from a stage](#label-dcr-collab-code-specs-staged-artifacts).
2. [Creates a template that references the code spec](#label-dcr-collaboration-create-and-register-code-spec-template) by ID in the template’s `code_specs` array. Add this field as a peer of the template and parameters fields as shown in this example:

   Copy code

   ```
   parameters:
     - name: <parameter_name>
       description: <parameter_description>
       required: <true_or_false>
       default: <default_value>
       type: <data_type>

   code_specs:             # Optional: List of code specs used by this template
     - <code_spec_id>        # One or more code spec IDs.

   template: |
     <template_content>
   ```
3. Registers the template and then [links the template into the collaboration](#label-dcr-collaboration-code-spec-link-template).

**The analysis runner:**

- Runs the template in the standard way by calling `RUN`.

Important

Snowflake runs security checks on any uploaded code specs before deploying them into a clean room. If a security check fails, the template
and its code spec will not be deployed and available for use.

To confirm that a template with a code spec is deployed and ready for use, take the following steps:

> 1. Find the name of the clean room application where you are trying to deploy the code spec:
>
>    Copy code
>
>    ```
>    SHOW APPLICATIONS LIKE 'SFDCR_<collaboration name>';
>    ```
> 2. Check the `upgrade_state` value in the DESCRIBE APPLICATION response. When the upgrade state is COMPLETE, the security checks have
>    passed and the new template and code spec are available to use. Pass in the application name returned by the command in the previous step using SQL like the following example:
>    SQL code:
>
>    Copy code
>
>    ```
>    DESCRIBE APPLICATION <application name>
>    ```

### Create and register the code specification

The first step in uploading custom code is to create and register the code specification.

Custom functions are defined in a YAML code specification. Each code spec exposes one or more functions that can be called by a template. The code specification can either include the code in the spec inline, or [link to code that lives on a Snowflake stage](#label-dcr-collab-code-specs-staged-artifacts).

A collaborator registers a spec by calling `REGISTRY.REGISTER_CODE_SPEC`, which returns the code spec ID.

After the template that references the code spec is linked into the collaboration, that code spec is visible to anyone in the collaboration who can access a template that links the code spec. Call `VIEW_CODE_SPECS` to list accessible code specs in a collaboration.

Anyone who can see a code spec in a collaboration can see and use it in their own templates in that collaboration. Any inline code can be viewed by any member of the collaboration, but staged artifact code cannot be viewed by collaborators. Collaborators need to ensure that the `content_hash` of the referenced artifacts matches for code integrity verification.

The following code specification exposes a single Python UDF called `normalize_value`, which calls the `normalize` function defined in that spec:

Copy code

```
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.REGISTRY.REGISTER_CODE_SPEC(
  $$
  api_version: 2.0.0
  spec_type: code_spec
  name: custom_udf
  version: v1
  functions:
    - name: normalize_value
      type: UDF
      language: PYTHON
      handler: normalize
      arguments:
        - name: value
          type: FLOAT
      returns: FLOAT
      code_body: |
        def normalize(value):
            return value / 100.0
  $$
);
```

### Create and register the calling template

After the code spec is registered, the collaborator then registers a template that uses this code spec. To use a code spec, add the code spec ID in the template’s `code_specs` field. Adding this template into the collaboration will also cause the code spec to be available in the collaboration.

A template calls a custom function using the syntax `cleanroom.spec_name$function_name`. Note the literal `.` and `$` name scoping marks.

Note

Use the spec name, not the spec ID, to reference a function in your template. This is so that you can quickly update the version of your code spec without having to change all the references to it in your template.

In the following example, a template uses function `normalize_value` from the code spec `custom_udf`:

Copy code

```
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.REGISTRY.REGISTER_TEMPLATE(
  $$
  api_version: 2.0.0
  spec_type: template
  name: normalization_template
  version: v1
  type: sql_analysis
  code_specs:
    - custom_udf_v1  -- Imports the code spec.
  template: |
    SELECT cleanroom.custom_udf$normalize_value(100)  -- Calls the UDF.
      AS normalized
        FROM {{ source_tables[0] }}
  $$
);
```

### Add the template to a collaboration

Add the template that calls your function to the collaboration in the standard way. For more information, see [Templates](/user-guide/cleanrooms/resources-templates#label-dcr-collaboration-add-templates-to-collaboration).

Snowflake validates and uploads to the collaboration when the calling template is added to a collaboration. The following example shows a request to add a template to an existing collaboration:

Copy code

```
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.COLLABORATION.ADD_TEMPLATE_REQUEST(
  'my_collaboration',
  'normalization_template_v1',
  ['consumer']
);
```

Note

Installing a template with a code spec triggers a Snowflake security check, and issues a new patch of the underlying clean room. The template will not be available or usable until the process is complete and the patch is installed.

To check the progress of the patch installation:

1. Find the name of the clean room application. Typically, this will be `SFDCR_<clean room name>`, but you can search to be sure:

   Copy code

   ```
   -- Find the exact name of the clean room application.
   SHOW APPLICATIONS LIKE 'SFDCR_%';
   ```
2. Check the status of the patch install. Wait for `upgrade_state` to be COMPLETE in the following query:

   Copy code

   ```
   DESCRIBE APPLICATION SFDCR_<application name>;
   ```

## Versioning your code

Every registered code spec must have a unique name + version across all registries in your account. A template loads a specific name and version of a code spec. If you want to create or consume a new version of your code, you must submit a new version of the template that references the new code version in the code\_specs field. You do not need to change the template body. For example:

Note

Unlike templates and data offerings, code specs can’t be unregistered. To change code, register a new version and reference it from your template, as described in this section.

**Step 1:** Consume version 1 of the code spec:

Copy code

```
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.REGISTRY.REGISTER_TEMPLATE(
  $$
  api_version: 2.0.0
  spec_type: template
  name: normalization_template
  version: v1
  type: sql_analysis
  code_specs:
    - custom_udf_v1  -- Code spec ID includes the version number.
  template: |
    SELECT cleanroom.custom_udf$normalize_value(100)  -- Calls the UDF.
      AS normalized
        FROM {{ source_tables[0] }}
  $$
);
```

**Step 2:** Update and register the new version of your code spec, and then update your template to use the new version:

Copy code

```
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.REGISTRY.REGISTER_TEMPLATE(
  $$
  api_version: 2.0.0
  spec_type: template
  name: normalization_template
  version: v2        -- Update the template version.
  type: sql_analysis
  code_specs:
    - custom_udf_v2  -- Use the new code spec.
  template: |
    SELECT cleanroom.custom_udf$normalize_value(100)  -- No change needed here.
      AS normalized
        FROM {{ source_tables[0] }}
  $$
);
```

Notice that function names do not include the version, so you do not need to change the calling code in the template body when you upload a new version of a function.

## Example specs

- [Inline UDF with code body](#inline-udf-with-code-body)
- [UDTF (User-Defined Table Function)](#udtf-user-defined-table-function)
- [Staged artifact with wheel package](#staged-artifact-with-wheel-package)
- [Stored procedure](#stored-procedure)
- [Multiple Python files as staged artifacts](#multiple-python-files-as-staged-artifacts)

### Inline UDF with code body

A simple UDF with inline Python code:

Copy code

```
api_version: 2.0.0
spec_type: code_spec
name: string_utils
version: v1
description: String utility functions

functions:
  - name: clean_string
    type: UDF
    language: PYTHON
    runtime_version: "3.10"
    handler: clean
    arguments:
      - name: input_str
        type: STRING
    returns: STRING
    description: Removes leading/trailing whitespace and converts to lowercase
    code_body: |
      def clean(input_str):
          if input_str is None:
              return None
          return input_str.strip().lower()

  - name: extract_domain
    type: UDF
    language: PYTHON
    runtime_version: "3.10"
    handler: extract
    arguments:
      - name: email
        type: STRING
    returns: STRING
    description: Extracts domain from email address
    code_body: |
      def extract(email):
          if email is None or '@' not in email:
              return None
          return email.split('@')[1]
```

### UDTF (User-Defined Table Function)

This example YAML defines a UDTF that returns multiple rows:

Copy code

```
api_version: 2.0.0
spec_type: code_spec
name: tokenizer
version: v1
description: Text tokenization UDTF

functions:
  - name: tokenize_text
    type: UDTF
    language: PYTHON
    runtime_version: "3.10"
    handler: Tokenizer
    arguments:
      - name: text
        type: STRING
      - name: delimiter
        type: STRING
    returns: TABLE(token STRING, position INTEGER)
    description: Splits text into tokens and returns each with its position
    code_body: |
      class Tokenizer:
          def process(self, text, delimiter):
              if text is None:
                  return
              tokens = text.split(delimiter if delimiter else ' ')
              for i, token in enumerate(tokens):
                  yield (token.strip(), i)
```

### Staged artifact with wheel package

Be sure to read the [stage\_path documentation requirements](/user-guide/cleanrooms/spec-code-spec#label-dcr-collab-code-spec-yaml) for linking to staged code in your code spec.

This example YAML uses a staged Python wheel package:

Copy code

```
api_version: 2.0.0
spec_type: code_spec
name: ml_scoring
version: v2
description: ML scoring functions using custom library

artifacts:
  - alias: ml_lib
    stage_path: "@MY_DB.PUBLIC.CODE_STAGE/libs/ml_scoring_lib-1.0.0-py3-none-any.whl"
    description: Custom ML scoring library
    content_hash: "a1b2c3d4e5f6..."

functions:
  - name: predict_score
    type: UDF
    language: PYTHON
    runtime_version: "3.10"
    handler: ml_scoring_lib.predictor.predict
    arguments:
      - name: features
        type: ARRAY
    returns: FLOAT
    packages:
      - numpy
      - scikit-learn
    imports:
      - ml_lib
    description: Predicts score using trained ML model
```

### Stored procedure

This example YAML defines a stored procedure for data processing:

Copy code

```
api_version: 2.0.0
spec_type: code_spec
name: data_processor
version: v1
description: Data processing procedures

procedures:
  - name: aggregate_metrics
    language: PYTHON
    runtime_version: "3.10"
    handler: process
    arguments:
      - name: table_name
        type: STRING
      - name: group_column
        type: STRING
    returns: STRING
    packages:
      - snowflake-snowpark-python
    description: Aggregates metrics by specified column
    code_body: |
      def process(session, table_name, group_column):
          df = session.table(table_name)
          result = df.group_by(group_column).count()
          result.write.mode("overwrite").save_as_table("aggregated_results")
          return f"Aggregated {df.count()} rows into aggregated_results"
```

### Multiple Python files as staged artifacts

Be sure to read the [stage\_path documentation requirements](/user-guide/cleanrooms/spec-code-spec#label-dcr-collab-code-spec-yaml) for linking to staged code in your code spec.

This example YAML uses multiple staged Python source files:

Copy code

```
api_version: 2.0.0
spec_type: code_spec
name: analytics_suite
version: v3
description: Analytics suite with multiple modules

artifacts:
  - alias: utils
    stage_path: "@MY_DB.PUBLIC.CODE_STAGE/analytics/utils.py"
    description: Utility functions
  - alias: transformers
    stage_path: "@MY_DB.PUBLIC.CODE_STAGE/analytics/transformers.py"
    description: Data transformation functions
  - alias: validators
    stage_path: "@MY_DB.PUBLIC.CODE_STAGE/analytics/validators.py"
    description: Validation functions

functions:
  - name: transform_and_validate
    type: UDF
    language: PYTHON
    runtime_version: "3.10"
    handler: transformers.transform_validate
    arguments:
      - name: data
        type: OBJECT
    returns: OBJECT
    imports:
      - utils
      - transformers
      - validators
    description: Transforms and validates input data
```
