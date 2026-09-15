# Upload an existing Python package

Snowflake CLI allows you to add existing Python packages to Snowpark imports using the `snow snowpark package` commands. You can use already implemented packages, such as those from PyPi, in your functions and procedures.

To add a Python package to Snowpark imports, do the following:

1. [Check whether a package is already available](#label-snowcli-check-for-package).
2. [Download a package and create a Snowflake artifact](#label-snowcli-download-package).
3. [Upload the package to a Snowflake stage](#label-snowcli-upload-package).
4. [Use the package in Snowpark procedures and functions](#label-snowcli-use-package).

## Check whether a package is already available

To check whether a package is not already available use the `snow snowpark package lookup` command.

The following example illustrates looking up a package that is already available on the Snowflake Anaconda channel:

Copy code

```
snow snowpark package lookup numpy
```

```
Package `numpy` is available in Anaconda. Latest available version: 1.26.4.
```

If a package is not available on the Snowflake Anaconda channel, you can get a message similar to the following:

Copy code

```
snow snowpark package lookup july
```

```
Package `july` is not available in Anaconda. To prepare Snowpark compatible package run:

  snow snowpark package create july
```

For more information, see the [snowpark package lookup](/developer-guide/snowflake-cli/command-reference/snowpark-commands/package-commands/lookup) command.

## Download a package and create a Snowflake artifact

To download a package and create a Snowflake artifact to upload use the `snow snowpark package create` command.

Copy code

```
snow snowpark package create <name>
```

where:

- `<name>` can be any requirement specifier supported by `pip`, such as a package name, an URL for a package, or a local file path.

Additional options:

- `--allow-shared-libraries`: Allows shared (`.so`/`.dll`) libraries, when using packages installed through `pip`.
- `--ignore-anaconda`: Does not lookup packages on Snowflake Anaconda channel.
- `--index-url`: Specifies the base URL of the Python Package Index to use for package lookup. This URL should point to a repository compliant with PEP 503 (the simple repository API) or a local directory laid out in the same format.
- `--skip-version-check`: Skips comparing versions of dependencies between requirements and Anaconda.

The following examples illustrate some different situations for creating Snowflake artifacts:

- [Example: create a package with Anaconda dependencies](#label-snowcli-snowpark-anaconda)
- [Example: create a package using the option](#label-snowcli-snowpark-ignore-anaconda)
- [Example: create a package already available in the Snowflake Anaconda channel](#label-snowcli-snowpark-existing-anaconda)

### Example: create a package with Anaconda dependencies

This example creates a Python package as a zip file that can be uploaded to a stage and later imported by a Snowpark Python app. Dependencies for “july” package are found on the Anaconda channel, so they were excluded from the `.zip` file. The command displays the packages you would need to include in `requirements.txt` of your Snowpark project.

Copy code

```
snow snowpark package create july==0.1
```

```
Package july.zip created. You can now upload it to a stage using
snow snowpark package upload -f july.zip -s <stage-name>`
and reference it in your procedure or function.
Remember to add it to imports in the procedure or function definition.

The package july==0.1 is successfully created, but depends on the following
Anaconda libraries. They need to be included in project requirements,
as their are not included in .zip.
matplotlib
numpy
```

### Example: create a package using the `--ignore-anaconda` option

This example creates the `july.zip` package that you can use in your Snowpark project without needing to add any dependencies to the `requirements.txt` file. The error messages indicate that some packages contain shared libraries, which might not work, such as when creating a package using Windows.

Copy code

```
snow snowpark package create july==0.1 --ignore-anaconda --allow-shared-libraries
```

```
2024-05-09 15:34:02 ERROR Following dependencies utilise shared libraries, not supported by Conda:
2024-05-09 15:34:02 ERROR contourpy
numpy
pillow
kiwisolver
matplotlib
fonttools
2024-05-09 15:34:02 ERROR You may still try to create your package with --allow-shared-libraries, but the might not work.
2024-05-09 15:34:02 ERROR You may also request adding the package to Snowflake Conda channel
2024-05-09 15:34:02 ERROR at https://support.anaconda.com/

Package july.zip created. You can now upload it to a stage using
snow snowpark package upload -f july.zip -s <stage-name>`
and reference it in your procedure or function.
Remember to add it to imports in the procedure or function definition.
```

### Example: create a package already available in the Snowflake Anaconda channel

This example fails to create the package because it already exists. You can still forcibly create the package by using the `--ignore-anaconda` option.

Copy code

```
snow snowpark package create matplotlib
```

```
Package matplotlib is already available in Snowflake Anaconda Channel.
```

For more information about creating a package, see the [snowpark package create](/developer-guide/snowflake-cli/command-reference/snowpark-commands/package-commands/create) command.

## Upload the package to a Snowflake stage

To upload your package, use the `snow snowpark package upload` command.

This command uploads a Python package zip file to a Snowflake stage so it can be referenced in the imports of a procedure or function.

Copy code

```
snow snowpark package upload --file="july.zip" --stage="packages"
```

```
Package july.zip UPLOADED to Snowflake @packages/july.zip.
```

## Use the package in Snowpark procedures and functions

To use the package in procedures or functions, add it to the `imports` parameter of [Snowpark definition](/developer-guide/snowflake-cli/snowpark/create#label-snowcli-func-proc-properties) section in `snowflake.yml`.

> Copy code
>
> ```
> get_custom_package_version:
>   handler: "functions.get_custom_package_version"
>   signature: ""
>   returns: string
>   type: function
>   imports:
>     - "@packages/july.zip"
>   meta:
>     use_mixins:
>       - snowpark_shared
> ```
>
> Then import your package in the function handler.
>
> Copy code
>
> ```
> # functions.py
> import july
>
> def get_custom_package_version():
>   return july.__VERSION__
> ```
