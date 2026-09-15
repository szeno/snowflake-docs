Categories:
:   [System functions](/sql-reference/functions-system) (System Information)

# SHOW\_PYTHON\_PACKAGES\_DEPENDENCIES

Returns a list of the dependencies and their versions for the Python packages that were specified.

Note

This function only works for Anaconda (Conda) packages. To resolve dependencies for packages from Artifact Repository (PyPI) or to work with packages from both Anaconda and Artifact Repository, use the [SYSTEM$RESOLVE\_PYTHON\_PACKAGES](/sql-reference/functions/system_resolve_python_packages) function instead.

For more information, see [Packages policies](/developer-guide/udf/python/packages-policy).

## Syntax

Copy code

```
SNOWFLAKE.SNOWPARK.SHOW_PYTHON_PACKAGES_DEPENDENCIES( '<Python_runtime_version>', '<packages_list>' )
```

## Arguments

`Python_runtime_version`
:   String specifying the version of the Python runtime.

`packages_list`
:   ARRAY of strings that specify the list of packages to check.

    You can use an [ARRAY constant](/sql-reference/data-types-semistructured#label-array-constant) to specify this list.

## Returns

Returns a JSON array that contains the dependencies and their versions.
Each element in the array is a string in the following format: `<package_name>==<version_name>`.

## Access control requirements

You must use the ACCOUNTADMIN role to call this function.

## Examples

The following example returns a list of the dependencies of the `numpy` Python package with the Python 3.10 runtime.

Copy code

```
USE ROLE ACCOUNTADMIN;

select SNOWFLAKE.SNOWPARK.SHOW_PYTHON_PACKAGES_DEPENDENCIES('3.10', ['numpy']);
```

The result is a list of the dependencies and their versions.

```
['_libgcc_mutex==0.1', '_openmp_mutex==5.1', 'blas==1.0', 'ca-certificates==2023.05.30', 'intel-openmp==2021.4.0',
'ld_impl_linux-64==2.38', 'ld_impl_linux-aarch64==2.38', 'libffi==3.4.4', 'libgcc-ng==11.2.0', 'libgfortran-ng==11.2.0',
'libgfortran5==11.2.0', 'libgomp==11.2.0', 'libopenblas==0.3.21', 'libstdcxx-ng==11.2.0', 'mkl-service==2.4.0',
'mkl==2021.4.0', 'mkl_fft==1.3.1', 'mkl_random==1.2.2', 'ncurses==6.4', 'numpy-base==1.24.3', 'numpy==1.24.3',
'openssl==3.0.10', 'python==3.10', 'readline==8.2', 'six==1.16.0', 'sqlite==3.41.2', 'tk==8.6.12', 'xz==5.4.2', 'zlib==1.2.13']
```

## See also

- [SYSTEM$RESOLVE\_PYTHON\_PACKAGES](/sql-reference/functions/system_resolve_python_packages) - Returns dependencies for both Anaconda and Artifact Repository packages (no special privileges required)
- [Packages policies](/developer-guide/udf/python/packages-policy) - Packages policies for Python
