# Using third-party packages

Stages can be used to import third-party packages. You can also specify Anaconda packages to install when you create Python UDFs.

## Artifact Repository overview

With Artifact Repository, you can directly use Python packages from the Python Package Index ([PyPI](https://pypi.org/)) within Snowpark Python user-defined functions (UDFs) and stored procedures so that building and scaling Python-powered applications in Snowflake is easier.

### Get started

Use Snowflake’s default Artifact Repository (`snowflake.snowpark.pypi_shared_repository`) to connect and install PyPI packages within Snowpark UDFs and procedures.

By default, the `SNOWFLAKE.PYPI_REPOSITORY_USER` database role is granted to PUBLIC, so any user can use the shared PyPI repository.

If your account administrator has revoked this default grant, the account administrator (a user with the ACCOUNTADMIN role) must grant the role before you can use the repository:

Copy code

```
GRANT DATABASE ROLE SNOWFLAKE.PYPI_REPOSITORY_USER TO ROLE some_user_role;
```

`SNOWFLAKE.PYPI_REPOSITORY_USER` is required for any role that uses `snowflake.snowpark.pypi_shared_repository`, including roles that execute UDFs or stored procedures referencing it.

With this role, you can install the package from the repository. When you create the UDF, you set the `ARTIFACT_REPOSITORY` parameter to the artifact repository name.
You also set the `PACKAGES` parameter to the list of the names of the packages that will come from artifact repository. In the following example, because the artifact repository is configured with PyPI, the package `scikit-learn` is sourced from PyPI:

Copy code

```
CREATE OR REPLACE FUNCTION sklearn_udf()
  RETURNS FLOAT
  LANGUAGE PYTHON
  RUNTIME_VERSION = 3.12
  ARTIFACT_REPOSITORY = snowflake.snowpark.pypi_shared_repository
  PACKAGES = ('scikit-learn')
  HANDLER = 'udf'
  AS
$$
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

def udf():
  X, y = load_iris(return_X_y=True)
  X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

  model = RandomForestClassifier()
  model.fit(X_train, y_train)
  return model.score(X_test, y_test)
$$;

SELECT sklearn_udf();
```

Note

To specify a package version, add it as shown:

Copy code

```
PACKAGES = ('scikit-learn==1.5')
```

### Default package source

When you create a Python UDF or stored procedure without specifying `ARTIFACT_REPOSITORY`, Snowflake resolves the package source in this order:

1. The `ARTIFACT_REPOSITORY` clause on the function or stored procedure.
2. The [`DEFAULT_PYTHON_ARTIFACT_REPOSITORY`](/sql-reference/parameters#label-default-python-artifact-repository) parameter set at the schema, database, or account level.

An account administrator can unset `DEFAULT_PYTHON_ARTIFACT_REPOSITORY` at any level.

The valid values for `DEFAULT_PYTHON_ARTIFACT_REPOSITORY` are `snowflake.snowpark.pypi_shared_repository`, `snowflake.snowpark.anaconda_shared_repository`, or the fully qualified name of a [customer-hosted artifact repository](/developer-guide/udf/python/customer-hosted-python-artifact-repositories).

Set the default package source at the account, database, or schema level:

Copy code

```
-- Account-level default
ALTER ACCOUNT
  SET DEFAULT_PYTHON_ARTIFACT_REPOSITORY = snowflake.snowpark.pypi_shared_repository;

-- Database-level default
ALTER DATABASE my_db
  SET DEFAULT_PYTHON_ARTIFACT_REPOSITORY = snowflake.snowpark.pypi_shared_repository;

-- Schema-level default
ALTER SCHEMA my_schema
  SET DEFAULT_PYTHON_ARTIFACT_REPOSITORY = snowflake.snowpark.pypi_shared_repository;

-- Unset at any level
ALTER ACCOUNT UNSET DEFAULT_PYTHON_ARTIFACT_REPOSITORY;
```

Override the default on an individual function:

Copy code

```
CREATE OR REPLACE FUNCTION my_func()
  RETURNS STRING
  LANGUAGE PYTHON
  RUNTIME_VERSION = '3.14'
  ARTIFACT_REPOSITORY = snowflake.snowpark.pypi_shared_repository
  PACKAGES = ('numpy')
  HANDLER = 'h'
  AS $$
def h():
    import numpy
    return numpy.__version__
$$;
```

List functions by their package source:

Copy code

```
SELECT function_catalog AS database,
       function_schema  AS schema,
       function_name    AS name,
       argument_signature,
       function_language AS language,
       runtime_version,
       artifact_repository
FROM information_schema.functions
WHERE artifact_repository IS NOT NULL;
```

List stored procedures by their package source:

Copy code

```
SELECT procedure_catalog AS database,
       procedure_schema  AS schema,
       procedure_name    AS name,
       argument_signature,
       procedure_language AS language,
       runtime_version,
       artifact_repository
FROM information_schema.procedures
WHERE artifact_repository IS NOT NULL;
```

### Packages built only for x86

If a package is built only for x86, choose one of the warehouses that uses x86 CPU architecture — `MEMORY_1X_x86` or `MEMORY_16X_x86` — and then specify `RESOURCE_CONSTRAINT=(architecture='x86')`, as in the following example:

Copy code

```
CREATE OR REPLACE FUNCTION pymeos_example()
RETURNS STRING
LANGUAGE PYTHON
HANDLER='main'
RUNTIME_VERSION='3.11'
ARTIFACT_REPOSITORY=snowflake.snowpark.pypi_shared_repository
PACKAGES=('pymeos') -- dependency pymeos-cffi is x86 only
RESOURCE_CONSTRAINT=(architecture='x86')
AS $$
def main() -> str:
   from pymeos import pymeos_initialize, pymeos_finalize, TGeogPointInst, TGeogPointSeq

   # Always initialize MEOS library
   pymeos_initialize()

   sequence_from_string = TGeogPointSeq(
      string='[Point(10.0 10.0)@2019-09-01 00:00:00+01, Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(10.0 10.0)@2019-09-03 00:00:00+01]')

   sequence_from_points = TGeogPointSeq(instant_list=[TGeogPointInst(string='Point(10.0 10.0)@2019-09-01 00:00:00+01'),
        TGeogPointInst(string='Point(20.0 20.0)@2019-09-02 00:00:00+01'),
        TGeogPointInst(string='Point(10.0 10.0)@2019-09-03 00:00:00+01')],
          lower_inc=True, upper_inc=True)
   speed = sequence_from_points.speed()

   # Call finish at the end of your code
   pymeos_finalize()

   return speed
$$;

SELECT pymeos_example();
```

For more information, see [Snowpark-optimized warehouses](/user-guide/warehouses-snowpark-optimized).

You can use Artifact Repository with UDF and Stored Procedure client APIs such as the following:

- [snowflake.snowpark.udf.UDFRegistration](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/snowpark/api/snowflake.snowpark.udf.UDFRegistration)
- [snowflake.snowpark.functions.sproc](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/snowpark/api/snowflake.snowpark.functions.sproc)

When using them, specify the following parameters:

> - `ARTIFACT_REPOSITORY`
> - `PACKAGES`

and provide the package name in the `PACKAGES` field.

See the following example:

> Copy code
>
> ```
> ...
> ARTIFACT_REPOSITORY="snowflake.snowpark.pypi_shared_repository",
> PACKAGES=["urllib3", "requests"],
> ...
> ```

### Troubleshooting

If the package install fails for the function or procedure creation part, run the following pip command locally to see whether the package specification is valid:

Copy code

```
pip install <package name> --only-binary=:all: --python-version 3.12 –platform <platform_tag>
```

### Limitations

- Access to private repositories is not supported.
- You can use Artifact Repository directly in [Notebooks in Workspaces](/user-guide/ui-snowsight/notebooks-in-workspaces/notebooks-in-workspaces-artifact-repositories). You can’t use it directly in [Legacy Notebooks](/user-guide/ui-snowsight/notebooks), but you can call a UDF or stored procedure that uses PyPI packages from a legacy notebook.
- You cannot use Artifact Repository within anonymous stored procedures.

Note

- Snowflake does not check or curate the security of Python packages from external sources. You are responsible for evaluating these packages and ensuring that they are safe and reliable.
- Snowflake reserves the right to block or remove any package that may be harmful or risky, without prior notice. This is to protect the platform’s integrity.

## Importing packages through a Snowflake stage

Snowflake stages can be used to import packages. You can bring in any Python code that follows guidelines defined in [General limitations](/developer-guide/udf/python/udf-python-limitations#label-limitations-on-python-udfs).
For more information, see [Creating a Python UDF with code uploaded from a stage](/developer-guide/udf/python/udf-python-creating#label-udf-python-stage).

You can only upload pure Python packages or packages with native code through a Snowflake stage.

As an example, you can use the following SQL, which creates a warehouse named `so_warehouse` that has x86 CPU architecture:

Copy code

```
CREATE WAREHOUSE so_warehouse WITH
   WAREHOUSE_SIZE = 'LARGE'
   WAREHOUSE_TYPE = 'SNOWPARK-OPTIMIZED'
   RESOURCE_CONSTRAINT = 'MEMORY_16X_X86';
```

To install a package with native code via importing from Stage, use the following example:

Copy code

```
CREATE or REPLACE function native_module_test_zip()
  RETURNS string
  LANGUAGE python
  RUNTIME_VERSION=3.12
  RESOURCE_CONSTRAINT=(architecture='x86')
  IMPORTS=('@mystage/mycustompackage.zip')
  HANDLER='compute'
  as
  $$
  def compute():
      import mycustompackage
      return mycustompackage.mycustompackage()
  $$;
```

## Using third-party packages from Anaconda

Snowflake provides access to a curated set of Python packages built by Anaconda. These packages integrate directly into Snowflake’s Python features at no extra cost.

Anaconda is one of two package sources available for Python UDFs and stored procedures. To make Anaconda the default for a database, schema, or account, set `DEFAULT_PYTHON_ARTIFACT_REPOSITORY = snowflake.snowpark.anaconda_shared_repository` at that level, or specify `ARTIFACT_REPOSITORY` directly on the function. See [Default package source](#default-package-source).

### Licensing terms

- **In Snowflake:** Governed by your existing Snowflake customer agreement, including the Anaconda usage restrictions described in this documentation. No separate Anaconda terms apply for in-Snowflake use.
- **Local development:** From Snowflake’s [dedicated Anaconda repository](https://repo.anaconda.com/pkgs/snowflake/) : Subject to Anaconda’s Embedded End Customer Terms and Anaconda’s Terms of Service posted on the repository. Local use is limited to developing/testing workloads intended for deployment in Snowflake.

### User guidelines

#### Permitted uses

- **Within Snowflake:** Use packages freely across all supported Python features.

  > Note
  >
  > You cannot call a UDF within the DEFAULT clause of a CREATE TABLE statement, with the exception of packages that remain freely available in Snowflake Notebooks on Snowpark Container Services.
- **Local development:** Use packages from Snowflake’s dedicated Anaconda repository to develop or test workloads intended for Snowflake.

#### Prohibited uses

The following uses of packages are prohibited:

- Using packages for projects not related to Snowflake.
- Hosting or mirroring package content externally.
- Removing or modifying copyright or license notices.

### Finding and managing packages

Can’t find a package you need?

- Submit requests via the [Snowflake Ideas forum](https://community.snowflake.com/s/ideas).
- Pure Python packages (without compiled extensions) can be [uploaded directly to a Snowflake stage](/developer-guide/snowflake-cli/snowpark/upload).

### Support and security

#### Support coverage

Snowflake provides standard package support, including:

- Installation guidance
- Environment troubleshooting
- Integration assistance

#### Warranty and SLA

Anaconda packages are third-party software provided *as-is* and are not covered by Snowflake’s warranty or SLA (Service-level agreement).

#### Security practices

Anaconda packages provided by Snowflake are built on trusted infrastructure and digitally signed.

For more details, see [Anaconda’s Security Practices](https://www.anaconda.com/docs/reference/policies-practices/security) .

#### Compliance and licensing

Each package includes its own open-source license. Customers must comply with individual package license terms in addition to the usage guidelines outlined in this documentation.

#### Frequently asked questions

- **Can I use packages from other Anaconda channels (e.g., conda-forge or Anaconda Defaults)?** No. Other channels are separate offerings and may require a commercial license from Anaconda.
- **Can I use these packages locally for projects unrelated to Snowflake?** No. Local usage is strictly limited to developing or testing workloads intended for Snowflake deployment. Other uses require a separate Anaconda license.
- **Why does Snowpark Container Services require separate licensing?** Using packages in custom Docker images extends beyond Snowflake’s integrated environment, necessitating separate Anaconda licensing.

### Displaying and using packages

#### Displaying available packages

You can display all packages available and their version information by querying the PACKAGES view in the Information Schema.

Copy code

```
select * from information_schema.packages where language = 'python';
```

To display version information about a specific package, for example `numpy`, use this command:

Copy code

```
select * from information_schema.packages where (package_name = 'numpy' and language = 'python');
```

Note

Some packages in the Anaconda Snowflake channel are not intended for use inside Snowflake UDFs because UDFs are executed within a restricted engine.
For more information, see [Following good security practices](/developer-guide/udf/python/udf-python-designing#label-udf-python-security).

When queries that call Python UDFs are executed inside a Snowflake warehouse, Anaconda packages are installed seamlessly and cached on the virtual warehouse on your behalf.

#### Displaying imported packages

You can display a list of the packages and modules a UDF or UDTF is using by executing the [DESCRIBE FUNCTION](/sql-reference/sql/desc-function) command.
Executing the DESCRIBE FUNCTION command for a UDF whose handler is implemented in Python returns the values of several properties, including a list of imported modules and packages,
as well as installed packages, the function signature, and its return type.

When specifying the identifier for the UDF, be sure to include function parameter types, if any.

Copy code

```
desc function stock_sale_average(varchar, number, number);
```

#### Using Anaconda packages

For an example of how to use an imported Anaconda package in a Python UDF,
refer to [Importing a package in an in-line handler](/developer-guide/udf/python/udf-python-examples#label-udf-python-in-line-examples).

#### Setting packages policies

You can use a packages policy to set allowlists and blocklists for third-party Python packages from Anaconda and the Snowflake PyPI repository at the account level.
This lets you meet stricter auditing and security requirements and gives you more fine-grained control over which packages are available or blocked in your environment.
For more information, see [Packages policies](/developer-guide/udf/python/packages-policy).

### Performance on cold warehouses

For more efficient resource management, newly provisioned virtual warehouses do not preinstall Anaconda packages.
Instead, Anaconda packages are installed on-demand the first time a UDF is used.
The packages are cached for future UDF execution on the same warehouse. The cache is dropped when the warehouse is suspended.
This may result in slower performance the first time a UDF is used or after the warehouse is resumed.
The additional latency could be approximately 30 seconds.

## Local development and testing

To help you create a conda environment on your local machine for development and testing, Anaconda has
created a Snowflake channel which mirrors a subset of the packages and versions that are supported in
the Snowflake Python UDF environment.
You may use the Snowflake conda channel for local testing and development at no cost under the Supplemental Embedded Software
Terms to Anaconda’s Terms of Service.

For example, to create a new conda environment locally using the Snowflake channel, type something like
this on the command line:

Copy code

```
conda create --name py312_env -c https://repo.anaconda.com/pkgs/snowflake python=3.12 numpy pandas
```

Note that because of platform differences, your local conda environment may not be exactly the same as
the server environment.

## Best practices

Within the `create function` statement, the package specification (for example, `packages = ('numpy','pandas')`) should
only specify the top-level packages that the UDF is using directly.

When packages are sourced from Anaconda, Anaconda manages dependencies and installs them automatically. You don’t need to specify dependency packages. If you don’t specify a package version, Anaconda installs the most up-to-date version of the package and its dependencies. Specifying a particular version is generally not necessary.

When using `artifact_repository` to source packages from PyPI, specify version constraints to ensure production stability. Unlike Anaconda packages, which are curated for Snowflake compatibility, PyPI packages might introduce breaking changes in new releases. Consider using version bounds, such as `packages = ('pandas<3.0.0',)`, or pinning to specific versions.

Note that version resolution is performed once, when the UDF is created using the `create function` command.
After that, the resulting version resolution is frozen and the same set of packages will be used when this particular UDF executes.

For an example of how to use the package specification within the `create function` statement, see [Importing a package in an in-line handler](/developer-guide/udf/python/udf-python-examples#label-udf-python-in-line-examples).

## Known issues with third-party packages

### Performance with single row prediction

Some data science frameworks, such as Scikit-learn and TensorFlow, might be slow when doing single-row ML prediction.
To improve performance, do batch prediction instead of single-row prediction.
To do this, you can use vectorized Python UDFs, with which you can define Python functions that receive input rows in batches, on which machine
learning or data science libraries are optimized to operate. For more information, see [Vectorized Python UDFs](/developer-guide/udf/python/udf-python-batch).

### Downloading data on demand from data science libraries

Some data science libraries, such as [NLTK](https://www.nltk.org/data.html), [Keras](https://www.tensorflow.org/api_docs/python/tf/keras/datasets),
and [spaCy](https://spacy.io) provide functionality to download additional corpora, data, or models on demand.

However, on-demand downloading does not work with Python UDFs due to Snowflake security constraints, which disable some
capabilities, such as network access and writing to files.

To work around this issue, download the data to your local environment and then provide it
to the UDF via a Snowflake stage.

### XGBoost

When using XGBoost in UDF or UDTF for parallel prediction or training, the concurrency for each XGBoost instance should
be set to 1. This ensures that XGBoost is configured for optimal performance when executing in
the Snowflake environment.

Examples:

Copy code

```
import xgboost as xgb
model = xgb.Booster()
model.set_param('nthread', 1)
model.load_model(...)
```

Copy code

```
import xgboost as xgb
model = xgb.XGBRegressor(n_jobs=1)
```

### TensorFlow/Keras

When using Tensorflow/Keras for prediction, use Model.predict\_on\_batch and
not Model.predict.

Example:

Copy code

```
import keras
model = keras.models.load_model(...)
model.predict_on_batch(np.array([input]))
```
