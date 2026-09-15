# Install the Snowflake Python APIs library

You can install the Snowflake Python APIs library for use with conda or a virtual environment. Before you start, be sure to review the
[supported Python versions](/developer-guide/snowflake-python-api/snowflake-python-overview#label-snowflake-python-supported-versions).

To set up the Snowflake Python APIs library, complete the following steps:

1. [Activate](#label-snowflake-python-activate-environment) a Python environment.
2. Optional: To use the library in government regions, [build the Python cryptography library](#label-snowflake-python-build-cryptography-library)
   in the environment.

   Note

   The Snowflake Python APIs library relies on the [Python cryptography library](https://pypi.org/project/cryptography/) for authentication.
   If you’re using a FIPS-compliant Python environment, you must compile the cryptography library against the system’s FIPS-compliant OpenSSL.
3. [Install](#label-snowflake-python-install-snowflake-library) the library.
4. [Set options](#label-snowflake-python-client-options) for the Python API client.

## Activate a Python environment

To set up an environment in which to run Python code, you need to activate a Python environment. For example, you can use conda or a
virtual environment (venv).

condavenv

Note

These steps are only shown as an example, and following along with the example might require additional rights to third-party data,
products, or services that are not owned or provided by Snowflake. Ensure that you have the appropriate rights to third-party data,
products, or services before continuing.

You can use `conda` to create an environment for running Python code. If you don’t have conda, you can install it from the conda website.

For information about conda, see [Conda Documentation](https://docs.conda.io/en/latest/). To download and install conda, see
[Installing conda](https://conda.io/projects/conda/en/latest/user-guide/install/index.html).

1. Create a conda environment:

   Copy code

   ```
   conda create -n <env_name> python==3.10
   ```
2. Activate the environment:

   Copy code

   ```
   conda activate <env_name>
   ```

You can use `venv` to create a virtual environment for running Python code. If you don’t have Python yet, you can download and install Python,
and then create a virtual environment.

For information about venv, see [venv — Creation of virtual environments](https://docs.python.org/3/library/venv.html#module-venv).
To download Python, see [Python Downloads](https://www.python.org/downloads/).

1. Use `venv` to create a virtual environment:

   Copy code

   ```
   cd <your Python project root folder>
   python3 -m venv '.venv'
   ```
2. Activate the environment:

   Copy code

   ```
   source '.venv/bin/activate'
   ```

## Build the Python cryptography library for government regions

For authentication, the Snowflake Python APIs use the [Snowflake Connector for Python](/developer-guide/python-connector/python-connector),
which relies on the [Python cryptography library](https://pypi.org/project/cryptography/). The cryptography library depends on the
[OpenSSL](https://www.openssl.org/) C library for all cryptographic operations and ships wheel packages with a statically linked OpenSSL
dependency included.

As such, when you install `cryptography` by using the default command `pip install cryptography`, the library uses its own version
of OpenSSL rather than the system’s version. For more information, see [Use of OpenSSL](https://cryptography.io/en/latest/openssl/).

If you’re using the Python API to connect to Snowflake accounts in government regions, you need to ensure that you use a FIPS-compliant
Python environment. To ensure FIPS compliance, instead of installing the cryptography library from a PyPI wheel, you must compile it
yourself against your system’s FIPS-compliant OpenSSL.

- For instructions on building the cryptography library on your specific operating system, see
  [Installation](https://cryptography.io/en/latest/installation/#installation) in the `cryptography` documentation.

Important

You must build the cryptography library in this manner before you run `pip install snowflake -U`. This build sets the `cryptography`
dependency and ensures that the `cryptography` package is not pulled from PyPI.

The cryptography library must be compiled using a version that meets the dependency requirements defined in the
[Snowflake Connector for Python library](https://github.com/snowflakedb/snowflake-connector-python/blob/main/setup.cfg#L50).

## Install the Snowflake Python APIs library

You can install the Snowflake Python APIs library from the Python Package Index (PyPI).

- In the conda or virtual environment that you created, run the following `pip` command to install the library:

  Copy code

  ```
  pip install snowflake -U
  ```

  The [snowflake](https://pypi.org/project/snowflake/) package is the [PEP 420 namespace](https://peps.python.org/pep-0420/) parent
  package for the Snowflake Python APIs. It includes `snowflake.core`, which is the subpackage that provides Python APIs for managing Snowflake
  resource objects.

  Installing the `snowflake` package automatically installs `snowflake.core` along with its required dependencies, including
  `snowflake-connector-python`.
- To also install the [Snowpark ML](/developer-guide/snowflake-ml/snowpark-ml) library as an extra package dependency, you can run
  the following `pip` command:

  Copy code

  ```
  pip install "snowflake[ml]" -U
  ```

After you install the library, you must create a connection to Snowflake before you can use the API. For more information about connecting,
see [Connect to Snowflake with the Snowflake Python APIs](/developer-guide/snowflake-python-api/snowflake-python-connecting-snowflake).

## Set Python API client options

You can set the following environment variables to control client options for the Snowflake Python APIs:

`_SNOWFLAKE_PRINT_VERBOSE_STACK_TRACE`
:   Specifies whether full stack tracing is enabled in printed error messages.

    Possible values:

    - Enabled: `true`, `t`, `yes`, `y`, `on`, or undefined
    - Disabled: Any other value

    Default: Enabled

    When this option is disabled, the API client sets `sys.tracebacklimit` to `0` when processing requests. This setting causes the
    client to suppress traceback information for all types of exceptions (not only the ones related to the API client) and to print only the error
    messages.

    To disable this option for Python notebook environments, run the following line in your notebook:

    Copy code

    ```
    %env _SNOWFLAKE_PRINT_VERBOSE_STACK_TRACE=false
    ```

`_SNOWFLAKE_ENABLE_RETRY_REQUEST_QUERY`
:   Specifies whether automatic retries are enabled on query requests with specific status codes.

    Possible values:

    - Enabled: `true`, `t`, `yes`, `y`, `on`
    - Disabled: Any other value or undefined

    Default: Enabled

    When this option is enabled, the API client automatically retries query requests when they have the following status codes:

    - `202`
    - `429`
    - `503`
    - `504`
