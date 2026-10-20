Categories:
:   [System functions](/sql-reference/functions-system) (System functions)

# SYSTEM$RESOLVE\_PYTHON\_PACKAGES

Returns a list of the resolved dependencies and their versions for the Python packages that were specified.
This function works with packages from both Anaconda and Artifact Repository (PyPI).

## Syntax

Copy code

```
SYSTEM$RESOLVE_PYTHON_PACKAGES( '<python_version>', '<package_spec_string>' [ , '<artifact_repository_name>' ] )
```

## Arguments

`python_version`
:   String specifying the version of the Python runtime (e.g., ’3.12’).

`package_spec_string`
:   String containing package specifications in `PACKAGES` clause format, for example, `$$('numpy', 'pandas')$$`.
    Use `$$()$$` to return only base packages (Python runtime and its dependencies).

`artifact_repository_name`
:   Optional. String specifying the artifact repository name (e.g., ‘snowflake.snowpark.pypi\_shared\_repository’).
    If not provided or empty, uses the default Anaconda repository.

## Returns

Returns a JSON array that contains the resolved packages and their dependencies.
Each element in the array is a string in the following format: `<package_name>==<version_name>`.
The result always includes base packages (e.g., Python runtime and system libraries).

## Access control requirements

This function can be called by any user. No special privileges are required.

## Usage notes

- Unlike [SHOW\_PYTHON\_PACKAGES\_DEPENDENCIES](/sql-reference/functions/show_python_packages_dependencies), which only works with Anaconda packages,
  `SYSTEM$RESOLVE_PYTHON_PACKAGES` works with packages from both Anaconda and Artifact Repository (PyPI).
- The function creates a temporary UDF internally to resolve package dependencies and automatically cleans it up.
- Use this function when you need to determine all dependencies for packages that will be included in a packages policy.

## Examples

**Example 1: Resolve packages from Anaconda**

The following example returns a list of the dependencies of the `numpy` and `pandas` Python packages
with the Python 3.12 runtime from the default Anaconda repository:

Copy code

```
SELECT SYSTEM$RESOLVE_PYTHON_PACKAGES('3.12', $$('numpy', 'pandas')$$);
```

The result lists the resolved versions of `numpy`, `pandas`, and their dependencies in
`<package_name>==<version_name>` format. The versions depend on the selected runtime and the packages
available in the repository when you run the function.

**Example 2: Resolve packages from Artifact Repository (PyPI)**

The following example resolves the `scikit-learn` package from a PyPI artifact repository:

Copy code

```
SELECT SYSTEM$RESOLVE_PYTHON_PACKAGES('3.12', $$('scikit-learn')$$, 'snowflake.snowpark.pypi_shared_repository');
```

**Example 3: Get base packages only**

The following example returns only the base packages for Python 3.12:

Copy code

```
SELECT SYSTEM$RESOLVE_PYTHON_PACKAGES('3.12', $$()$$);
```

The result contains the resolved Python runtime and its system dependencies. No additional Python
packages are requested.

## See also

- [SHOW\_PYTHON\_PACKAGES\_DEPENDENCIES](/sql-reference/functions/show_python_packages_dependencies) - Returns dependencies for Anaconda packages only (requires ACCOUNTADMIN role)
- [Packages policies](/developer-guide/udf/python/packages-policy) - Packages policies for Python
- [Using third-party packages](/developer-guide/udf/python/udf-python-packages) - Using Python packages in UDFs
