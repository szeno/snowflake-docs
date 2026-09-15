# Packages policies

## Introduction

Using a packages policy enables you to set allowlists and blocklists for third-party Python packages from Anaconda and the Snowflake PyPI repository at the account level.
This lets you meet stricter auditing and security requirements and gives you more fine-grained control over which packages are
available or blocked in your environment.

For more information about how Snowpark Python allows you to bring in third-party packages from
Anaconda, see [Using third-party packages](/developer-guide/udf/python/udf-python-packages#label-python-udfs-anaconda).

When you create a Python UDF, UDTF or stored procedure, the allowlist and blocklist will be taken into account when creating the Python environment. The allowlist and blocklist will apply to all packages that are required to create the Python environment, including packages from both Anaconda and the Snowflake PyPI repository.
If it’s not possible to create an environment with the specified packages, the query will fail.

When you execute a Python UDF, UDTF or stored procedure, Snowflake will check the allowlist and blocklist and
make sure that all of the packages are allowed by the packages policy. Otherwise, the query will fail.

## Limitations

- Packages policies will not be applied for built-in functions and will also not be applied for native apps.
- Packages policies apply to packages from Anaconda and the Snowflake PyPI repository.

## Implementing and using a packages policy

In order to create a packages policy object, you must have the following privileges:

- USAGE on the database and schema in which you plan to create the packages policy.
- CREATE PACKAGES POLICY on the schema in which you plan to create the packages policy.

After the packages policy object is created, you must have the following privileges to apply it to the account:

- OWNERSHIP on the packages policy object.
- APPLY PACKAGES POLICY on the account.

Follow these steps to implement a packages policy.

### Step 1: Create a packages policy admin custom role

Create a custom role that allows users to create and manage packages policies. Throughout this topic, the example custom role is named
`policy_admin`, although the role could have any appropriate name.

If the custom role already exists, continue to the next step.

Otherwise, create the `policy_admin` custom role.

Copy code

```
USE ROLE useradmin;

CREATE ROLE policy_admin;
```

### Step 2: Grant privileges to the `policy_admin` custom role

If the `policy_admin` custom role does not already have the following privileges, grant these privileges as shown below:

- USAGE on the database and schema that will contain the packages policy.
- CREATE PACKAGES POLICY on the schema that will contain the packages policy.
- APPLY PACKAGES POLICY on the account.

Copy code

```
USE ROLE securityadmin;

GRANT USAGE ON DATABASE yourdb TO ROLE policy_admin;

GRANT USAGE, CREATE PACKAGES POLICY ON SCHEMA yourdb.yourschema TO ROLE policy_admin;

GRANT APPLY PACKAGES POLICY ON ACCOUNT TO ROLE policy_admin;
```

### Step 3: Create a new packages policy

Using the `policy_admin` custom role, create a new packages policy, with a language, allowlist, and blocklist
specified. ALLOWLIST, BLOCKLIST, ADDITIONAL\_CREATION\_BLOCKLIST, and COMMENT are optional parameters. By default, the allowlist value is `('*')`,
and the blocklist value is `()`.

If a package is specified in both the allowlist and the blocklist, then the blocklist takes precedence.
You must explicitly add the Python runtime version in the allowlist and
you must also explicitly add all packages and underlying dependencies of a parent package to the allowlist.

You can specify a particular package version or a range of versions by using these version
specifiers in the allowlist or blocklist: : `==`, `<=`, `>=`, `<`,or `>`.
For example, `numpy>=1.2.3`.
You can use wildcards, such as, `numpy==1.2.*`, which means any micro version of numpy 1.2.

Note

Currently, in an allowlist or blocklist, only one range operator can be specified per package.
Specifying multiple range operators is not supported, for example `pkg>1.0, <1.5`.
Because of this, to configure a policy to allow an interval of a package version, set one side of
the range in the allowlist and the other side of the range in the blocklist.
For example, to allow package versions greater than 1.0 and less than 1.5,
set the allowlist to `pkg>1.0` and the blocklist to `pkg>1.5`.

Copy code

```
USE ROLE policy_admin;

CREATE PACKAGES POLICY yourdb.yourschema.packages_policy_prod_1
  LANGUAGE PYTHON
  ALLOWLIST = ('numpy', 'pandas==1.2.3', ...)
  BLOCKLIST = ('numpy==1.2.3', 'bad_package', ...)
  ADDITIONAL_CREATION_BLOCKLIST = ('bad_package2', 'bad_package3', ...)
  COMMENT = 'Packages policy for the prod_1 environment'
;
```

Where:

> `yourdb.yourschema.packages_policy_prod_1`
> :   The fully qualified name of the packages policy.
>
> `LANGUAGE PYTHON`
> :   The language that this packages policy will apply to.
>
> `ALLOWLIST = ('numpy', 'pandas==1.2.3', ...)`
> :   The allowlist for this packages policy. This is a comma-separated string with package specs.
>
> `BLOCKLIST = ('numpy==1.2.3', 'bad_package', ...)`
> :   The blocklist for this packages policy. This is a comma-separated string with package specs.
>
> `ADDITIONAL_CREATION_BLOCKLIST = ('bad_package2', 'bad_package3', ...)`
> :   Specifies a list of package specs that are blocked at creation time. To unset this parameter, specify an empty list.
>     If the `ADDITIONAL_CREATION_BLOCKLIST` is set, it is appended to the basic BLOCKLIST at the creation time.
>     For temporary UDFs and anonymous stored procedures, the `ADDITIONAL_CREATION_BLOCKLIST` is appended to the `BLOCKLIST` at both creation and execution time.
>
> `COMMENT = 'Packages policy for the prod_1 environment'`
> :   A comment specifying the purpose of the packages policy.

In the example above, the blocklist applied for the creation time will be the `ADDITIONAL_CREATION_BLOCKLIST` plus the `BLOCKLIST` so the blocked packages will be
`numpy==1.2.3`, `bad_package`, `bad_package2` and `bad_package3`.
The blocklist applied for the execution will be: `numpy==1.2.3` and `bad_package`.
For temporary UDFs and anonymous stored procedures, the blocklist containing `numpy==1.2.3`, `bad_package`, `bad_package2` and `bad_package3`
will be applied at both creation and execution time.

#### Find package dependencies

To get a list of the dependencies of a Python package, use one of the following functions, depending on your requirements:

- [SYSTEM$RESOLVE\_PYTHON\_PACKAGES](/sql-reference/functions/system_resolve_python_packages)
- [SHOW\_PYTHON\_PACKAGES\_DEPENDENCIES](/sql-reference/functions/show_python_packages_dependencies) - Note that this function only works for Anaconda (Conda) packages.

**SYSTEM$RESOLVE\_PYTHON\_PACKAGES**

For packages from both Artifact Repository and Anaconda, use the `SYSTEM$RESOLVE_PYTHON_PACKAGES` system function.
This function works with packages from PyPI (via Artifact Repository) and packages from Anaconda.

> **Syntax:**
>
> Copy code
>
> ```
> SYSTEM$RESOLVE_PYTHON_PACKAGES(<python_version>, <package_spec_string>, [<artifact_repository_name>])
> ```
>
> Where:
>
> - `python_version`: String specifying the Python version (e.g., ’3.12’)
> - `package_spec_string`: Package specifications in PACKAGES clause format (e.g., `$$('numpy>=1.20.0', 'pandas==1.3.0')$$`). Use `$$()$$` to return only base packages.
> - `artifact_repository_name`: Optional artifact repository name. If not provided, uses the default Anaconda repository.
>
> **Returns:** A JSON array of resolved package specifications in the format `["package1==version1", "package2==version2", ...]`.
> Always includes base packages (e.g., Python runtime) in addition to the requested packages.
>
> **Examples:**
>
> Using the default Anaconda repository:
>
> Copy code
>
> ```
> SELECT SYSTEM$RESOLVE_PYTHON_PACKAGES('3.12', $$('numpy>=1.20.0', 'pandas==1.3.0')$$);
> ```
>
> The result is a list of the resolved packages and their dependencies:
>
> ```
> ["_libgcc_mutex==0.1", "_openmp_mutex==5.1", "numpy==1.24.3", "pandas==1.5.3", "python==3.12.20", ...]
> ```
>
> Using a custom PyPI artifact repository:
>
> Copy code
>
> ```
> SELECT SYSTEM$RESOLVE_PYTHON_PACKAGES('3.12', $$('scikit-learn')$$, 'snowflake.snowpark.pypi_shared_repository');
> ```
>
> To show only the base packages (Python runtime and dependencies):
>
> Copy code
>
> ```
> SELECT SYSTEM$RESOLVE_PYTHON_PACKAGES('3.12', $$()$$);
> ```
>
> Unlike `SHOW_PYTHON_PACKAGES_DEPENDENCIES`, which only supports Anaconda packages,
> `SYSTEM$RESOLVE_PYTHON_PACKAGES` can resolve dependencies for packages from both Artifact Repository and Anaconda.
> This function can be called by any user without special privileges.
>
> If you want to know which packages a function is using, you can use [DESCRIBE FUNCTION](/sql-reference/sql/desc-function) to print them out.
> This is an alternative way to identify all of the dependencies of a package.
> To do this, create a function and in the package specification, provide the top level packages.
> Next, use DESCRIBE FUNCTION to get a list of all of the packages and their dependencies.
> You can copy and paste this list into the package allowlist.
> Note that the packages policy must be temporarily unset or some packages might be blocked.
> The following example shows how to find the dependencies for the ‘snowflake-snowpark-python’ package.
>
> Copy code
>
> ```
> CREATE OR REPLACE FUNCTION my_udf()
>   RETURNS STRING
>   LANGUAGE PYTHON
>   PACKAGES = ('snowflake-snowpark-python')
>   RUNTIME_VERSION = 3.10
>   HANDLER = 'echo'
> AS $$
> def echo():
> return 'hi'
> $$;
>
> DESCRIBE FUNCTION my_udf();
> ```
>
> If you want to show all of the packages and versions that are available,
> query the INFORMATION\_SCHEMA.PACKAGES view.
>
> Copy code
>
> ```
> SELECT * FROM information_schema.packages;
> ```
>
> If you want to see the current set of packages you are using, you can use this SQL statement.
>
> Copy code
>
> ```
> -- at the database level
>
> CREATE OR REPLACE VIEW USED_ANACONDA_PACKAGES
>   AS SELECT FUNCTION_NAME, VALUE PACKAGE_NAME
>   FROM (SELECT FUNCTION_NAME,PARSE_JSON(PACKAGES)
>   PACKAGES FROM INFORMATION_SCHEMA.FUNCTIONS
>   WHERE FUNCTION_LANGUAGE='PYTHON') USED_PACKAGES,LATERAL FLATTEN(USED_PACKAGES.PACKAGES);
>
> -- at the account level
>
> CREATE OR REPLACE VIEW ACCOUNT_USED_ANACONDA_PACKAGES
>   AS SELECT FUNCTION_CATALOG, FUNCTION_SCHEMA, FUNCTION_NAME, VALUE PACKAGE_NAME
>   FROM (SELECT FUNCTION_CATALOG, FUNCTION_SCHEMA, FUNCTION_NAME,PARSE_JSON(PACKAGES)
>   PACKAGES FROM SNOWFLAKE.ACCOUNT_USAGE.FUNCTIONS
>   WHERE FUNCTION_LANGUAGE='PYTHON') USED_PACKAGES,LATERAL FLATTEN(USED_PACKAGES.PACKAGES);
> ```
>
> To get a list of third-party packages that are available from Anaconda, use the [GET\_ANACONDA\_PACKAGES\_REPODATA](/sql-reference/functions/get_anaconda_packages_repodata) function.
> The parameter is the architecture, which can be:
> `linux-64`, `linux-aarch64`, `osx-64`, `osx-arm64`, `win-64`, or `noarch`.
>
> For example, to show the list of third-party packages from Anaconda for the `linux-64` architecture, use this command.
>
> Copy code
>
> ```
> USE ROLE ACCOUNTADMIN;
>
> SELECT SNOWFLAKE.SNOWPARK.GET_ANACONDA_PACKAGES_REPODATA('linux-64');
> ```

**SHOW\_PYTHON\_PACKAGES\_DEPENDENCIES**

The first parameter is the Python runtime version you are using and the second is a list of the packages to show dependencies for.
For example, to show the dependencies of the `numpy` package, use this command.

Copy code

```
USE ROLE ACCOUNTADMIN;

SELECT SNOWFLAKE.SNOWPARK.SHOW_PYTHON_PACKAGES_DEPENDENCIES('3.12', ['numpy']);
```

The result is a list of the dependencies and their versions.

```
['_libgcc_mutex==0.1', '_openmp_mutex==5.1', 'blas==1.0', 'ca-certificates==2024.9.24', 'intel-openmp==2023.1.0',
'ld_impl_linux-64==2.40', 'ld_impl_linux-aarch64==2.40', 'libffi==3.4.4', 'libgcc-ng==11.2.0', 'libgfortran-ng==11.2.0',
'libgfortran5==11.2.0', 'libgomp==11.2.0', 'libopenblas==0.3.21', 'libstdcxx-ng==11.2.0', 'mkl-service==2.4.0', 'mkl==2023.1.0',
'mkl_fft==1.3.10', 'mkl_random==1.2.7', 'ncurses==6.4', 'numpy-base==2.0.1', 'numpy==2.0.1', 'openssl==3.0.15', 'python==3.12.20',
'readline==8.2', 'sqlite==3.45.3', 'tbb==2021.8.0', 'tk==8.6.14', 'tzdata==2024b', 'xz==5.4.6', 'zlib==1.2.13']
```

To show the dependencies of Python 3.12 within Snowpark environment, call the function without specifying any packages.

Copy code

```
SELECT SNOWFLAKE.SNOWPARK.SHOW_PYTHON_PACKAGES_DEPENDENCIES('3.12', []);
```

### Step 4: Set the packages policy on an account

Using the `policy_admin` custom role, set the policy on an account with the [ALTER ACCOUNT](/sql-reference/sql/alter-account) command.

Copy code

```
USE ROLE policy_admin;

ALTER ACCOUNT SET PACKAGES POLICY yourdb.yourschema.packages_policy_prod_1;
```

Note

To replace a packages policy that is already set for an account, unset the packages policy first and then set the new packages
policy for the account. Alternatively, you can use FORCE to set the packages policy without having to unset the packages policy. For example:

Copy code

```
ALTER ACCOUNT SET PACKAGES POLICY yourdb.yourschema.packages_policy_prod_2 force;
```

If you want to see which policy is active on the account, you can use this SQL statement.

Copy code

```
SELECT * FROM TABLE(information_schema.policy_references(ref_entity_domain=>'ACCOUNT', ref_entity_name=>'<your_account_name>'))
```

The result of this query will display a column with the name `POLICY_STATUS`.

Later, if you want to unset the package policy on your account, use this SQL statement.

Copy code

```
ALTER ACCOUNT UNSET PACKAGES POLICY;
```

### Privileges required to execute DDL commands

The following table summarizes the relationship between the packages policy DDL operations and their necessary privileges.

| Operation | Privilege required |
| --- | --- |
| Create packages policy | A role with the CREATE PACKAGES POLICY privilege on the schema. |
| Alter packages policy | A role with the OWNERSHIP privilege on the packages policy. |
| Drop packages policy | A role with the OWNERSHIP privilege on the packages policy. |
| Describe packages policy | A role with the OWNERSHIP or USAGE privilege on the packages policy. |
| Show packages policies | A role with the OWNERSHIP or USAGE privilege on the packages policy. |
| Set & unset packages policy | A role with the APPLY PACKAGES POLICY privilege on the account and the OWNERSHIP privilege on the packages policy. |

Expand

Show lessSee more

## Packages policy DDL

Snowflake provides the following DDL commands to manage packages policy objects:

- [CREATE PACKAGES POLICY](/sql-reference/sql/create-packages-policy)
- [ALTER PACKAGES POLICY](/sql-reference/sql/alter-packages-policy)
- [DROP PACKAGES POLICY](/sql-reference/sql/drop-packages-policy)
- [SHOW PACKAGES POLICIES](/sql-reference/sql/show-packages-policies)
- [DESCRIBE PACKAGES POLICY](/sql-reference/sql/desc-packages-policy)

## Packages policy observability

Users who do not have access to the packages policy that is set on the account are able to see the contents of it.

Users can control who sees the contents of the packages policy by adding the USAGE privilege to the packages policies.
The account administrator or packages policy owner can grant this privilege to roles that need to use packages policies.

Copy code

```
GRANT USAGE ON PACKAGES POLICY <packages policy name> TO ROLE <user role>;
```

The [CURRENT\_PACKAGES\_POLICY](/sql-reference/info-schema/current_packages_policy) Information Schema view displays a row for each
Snowpark packages policy on the current account.

Copy code

```
SELECT * FROM information_schema.current_packages_policy;
```

```
+------+----------+-----------+-----------+-------------------------------+---------+
| NAME | LANGUAGE | ALLOWLIST | BLOCKLIST | ADDITIONAL_CREATION_BLOCKLIST | COMMENT |
+------+----------+-----------+-----------+-------------------------------+---------+
| P1   | PYTHON   | ['*']     | []        | [NULL]                        | [NULL]  |
+------+----------+-----------+-----------+-------------------------------+---------+
```

To see the Anaconda packages that are used at the database level for function, use this SQL statement.

Copy code

```
USE DATABASE mydb;

CREATE OR REPLACE VIEW USED_ANACONDA_PACKAGES
  AS
  SELECT FUNCTION_NAME, VALUE PACKAGE_NAME
  FROM (SELECT FUNCTION_NAME,PARSE_JSON(PACKAGES)
  PACKAGES FROM INFORMATION_SCHEMA.FUNCTIONS
  WHERE FUNCTION_LANGUAGE='PYTHON') USED_PACKAGES,LATERAL FLATTEN(USED_PACKAGES.PACKAGES);
```

To see the Anaconda packages that are used at the account level for function, use this SQL statement.

Copy code

```
USE DATABASE mydb;

CREATE OR REPLACE VIEW ACCOUNT_USED_ANACONDA_PACKAGES
  AS
  SELECT  FUNCTION_CATALOG, FUNCTION_SCHEMA, FUNCTION_NAME, VALUE PACKAGE_NAME
  FROM (SELECT FUNCTION_CATALOG, FUNCTION_SCHEMA, FUNCTION_NAME,PARSE_JSON(PACKAGES)
  PACKAGES FROM SNOWFLAKE.ACCOUNT_USAGE.FUNCTIONS
  WHERE FUNCTION_LANGUAGE='PYTHON') USED_PACKAGES,LATERAL FLATTEN(USED_PACKAGES.PACKAGES);
```

To see all of the installed Anaconda packages on your account, use this SQL statement.

Copy code

```
USE DATABASE mydb;

CREATE OR REPLACE VIEW ACCOUNT_USED_ANACONDA_PACKAGES
  AS
  SELECT 'FUNCTION' TYPE, FUNCTION_CATALOG DATABASE, FUNCTION_SCHEMA SCHEMA, FUNCTION_NAME NAME, VALUE::STRING PACKAGE_NAME
  FROM (SELECT FUNCTION_CATALOG, FUNCTION_SCHEMA, FUNCTION_NAME,PARSE_JSON(PACKAGES)
  PACKAGES FROM SNOWFLAKE.ACCOUNT_USAGE.FUNCTIONS
  WHERE FUNCTION_LANGUAGE='PYTHON' AND PACKAGES IS NOT NULL) USED_PACKAGES,LATERAL FLATTEN(USED_PACKAGES.PACKAGES)
  UNION
  (SELECT 'PROCEDURE' TYPE, PROCEDURE_CATALOG DATABASE, PROCEDURE_SCHEMA SCHEMA, PROCEDURE_NAME, VALUE::STRING PACKAGE_NAME
  FROM (SELECT PROCEDURE_CATALOG, PROCEDURE_SCHEMA,PROCEDURE_NAME,PARSE_JSON(PACKAGES)
  PACKAGES FROM SNOWFLAKE.ACCOUNT_USAGE.PROCEDURES
  WHERE PROCEDURE_LANGUAGE='PYTHON' AND PACKAGES IS NOT NULL) USED_PACKAGES,LATERAL FLATTEN(USED_PACKAGES.PACKAGES));
```

## Replication and packages policies

Packages policies are replicated from a source account to target accounts if the database containing the packages policy is
[replicated](/user-guide/account-replication-intro). For more information, see [Dangling references and packages policies](/user-guide/account-replication-considerations#label-dangling-references-packages-policies).
