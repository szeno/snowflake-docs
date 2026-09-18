# Spark job specification reference

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

The job specification defines how your Spark job runs. In SQL it’s the YAML in the `WITH SPECIFICATION` clause; in the
REST API it’s the `bundle` object in the request body. The following fields apply to Spark jobs. For the full set of
generic configuration fields, see the [`code_bundle.yml` reference](/developer-guide/code-bundles/code-bundle-yml-reference).

| Field | Required? | Language | Description |
| --- | --- | --- | --- |
| `type` | Required | All | Must be `spark` for Spark jobs. |
| `compute_type` | Required | All | Must be `warehouse`. The job runs on the session’s warehouse. |
| `language` | Required | All | `scala`, `java`, or `python`. |
| `compute_options.runtime_version` | Optional | All | The Snowpark Connect for Spark client version ([`snowpark-connect`](/release-notes/clients-drivers/snowpark-connect-2026)) to run with, installed at job startup (for example, `"1.41.0"`). Defaults to the latest available client version. Also determines the `snowflake-snowpark-python` version and the supported Python range. |
| `compute_options.language_version` | Required for Scala/Java; Optional for Python | All | For Python, the Python interpreter version (for example, `"3.12"`); defaults to `"3.11"` and is constrained by the selected client version. Required for Scala/Java: the Scala binary version (`"2.12"` or `"2.13"`), which must match your JAR’s compiled Scala version. |
| `properties.spark_conf` | Optional | All | Map of Spark configuration properties. |
| `properties.java_dependencies.jars` | Optional | Scala/Java | List of dependency JARs on a stage. Added to the classpath automatically. |
| `properties.python_files` | Optional | Python | List of Python files or archives placed on `PYTHONPATH`. Not installed (unlike `python_dependencies`). |
| `properties.python_dependencies.wheels` | Optional | Python | List of Python wheels (`.whl`) on a stage. On warehouse compute the wheels are staged with the job but are not automatically installed; to install packages, use `packages` or `requirements_files`. |
| `properties.python_dependencies.requirements_files` | Optional | Python | List of stage paths to `requirements.txt` files. |
| `properties.python_dependencies.packages` | Optional | Python | List of PyPI packages to install (for example, `numpy==1.26.4`). |
| `artifact_repositories` | Optional | Python | List of artifact repositories used to resolve PyPI dependencies (on warehouse compute, at most one). Defaults to `snowflake.snowpark.pypi_shared_repository`. |
| `secrets` | Optional | All | List of [Snowflake secrets](/sql-reference/sql/create-secret) to attach. |
| `external_access_integrations` | Optional | All | List of [external access integrations](/developer-guide/external-network-access/creating-using-external-network-access) to attach. |

Expand

Show lessSee more

## compute\_options.runtime\_version

The `runtime_version` property selects the Snowpark Connect for Spark client version (the
[`snowpark-connect`](/release-notes/clients-drivers/snowpark-connect-2026) package) that the job runs with; the value is
installed as `snowpark-connect==<runtime_version>` at job startup. It’s optional: when omitted, Snowflake uses the
latest available client version. The selected client version also determines the `snowflake-snowpark-python` version and
the range of Python interpreter versions you can select with `language_version`. Always quote the value.

## compute\_options.language\_version

The `language_version` property selects the language runtime:

- For Python, it’s the Python interpreter version (for example, `"3.12"`). When omitted, it defaults to `"3.11"`. The
  versions you can select are constrained by the client version chosen with `runtime_version`.
- For Scala or Java, it’s the Scala binary version (`"2.12"` or `"2.13"`) and is required. It must match the Scala
  version your JAR was compiled with; a mismatch prevents the Spark session from starting.

Always quote the value.

## properties.python\_files

The `python_files` list specifies Python files or archives to place on `PYTHONPATH`. They are made importable but are
**not** installed (unlike `python_dependencies`). Use it for your own modules and supporting code.

## properties.python\_dependencies

The `python_dependencies` object specifies the Python dependencies for the job:

- `packages`: PyPI package specifiers to install (for example, `numpy==1.26.4`).
- `requirements_files`: stage paths to `requirements.txt` files whose packages are installed.
- `wheels`: wheel files (`.whl`) on a stage.

PyPI dependencies in `packages` and `requirements_files` are resolved and installed through an artifact repository. If
you don’t set `artifact_repositories`, Snowflake uses the account-level `snowflake.snowpark.pypi_shared_repository`,
which proxies PyPI and doesn’t require an external access integration. To use the Snowflake Anaconda channel, set
`artifact_repositories` to `snowflake.snowpark.anaconda_shared_repository`.

Note

On warehouse compute, wheels listed in `wheels` are staged with the job but are not automatically installed. To install
a package, add it to `packages` or to a `requirements.txt` referenced by `requirements_files`.

## properties.java\_dependencies.jars

(Scala/Java) The `jars` list specifies dependency JARs on a stage to add to the job’s classpath automatically. Use it
for libraries your application needs in addition to your main JAR.

## properties.spark\_conf

The `spark_conf` property is a map of Spark configuration properties applied to the job’s Spark session.
