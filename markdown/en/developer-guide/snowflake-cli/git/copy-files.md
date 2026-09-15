# Copying files in Git

The `snow git copy` command copies files from given state of the repository (specific branch, tag, or commit) into another stage or local file system.

Copy code

```
snow git copy <REPO_PATH> <DEST_PATH> [--parallel INT]
```

where:

- `<REPO_PATH>` is a stage path with a specific scope where the value is the repository name followed by a suffix specifying which branch, tag, or commit to copy. The following lists some different types of values:

  - `@snowcli_git/branches/main/` refers to last commit of the “main” branch
  - `@snowcli_git/tags/v2.1.0/` refers to a commit tagged `v2.1.0`.
  - `@snowcli_git/commits/1e939d69ca6fd0f89074e7e97c9fd1/` refers to a specific commit. Commit hashes should be between 6 and 40 characters long.

  A repository path can also be a subdirectory or file in the repository, but still must be preceded with a scope prefix.
- `<DEST_PATH>` is a path to a local directory or to a remote directory on the Snowflake stage.
- `--parallel` specifies the number of threads to use when downloading files.

When `<DEST_PATH>` specifies a stage, the command operates differently based on its suffix format, as follows:

- If the source ends with a `/`, such as `@my_snow_git/branches/main/tests/plugin/`, the command copies the contents of the `plugin` directory into the destination.
- If the source does not end with a `/`, such as `@my_snow_git/branches/main/tests/plugin`, the command copies the entire `plugin` directory.

## Example: Copy files from a commit to a directory in a stage

This example creates a `snowcli2.0/` directory on stage `@public` and copies all files from the commit marked with tag `v2.0.0` into that directory:

Copy code

```
snow git copy @my_snow_git/tags/v2.0.0/ @public/snowcli2.0/
```

## Example: Copy files from inside a directory to a directory in a stage

The following example creates a `plugin_tests` directory on the `test_stage` stage and copies the contents of the `tests/plugin/` directory into it.

Copy code

```
snow git copy @my_snow_git/branches/main/tests/plugin/ @test_stage/plugin_tests/
```

## Example: Copy an entire directory to a directory in a stage

This example creates a `plugin_tests` directory on the *test\_stage* stage and copies the entire `tests/plugin` directory into it. Because `tests/plugin` does note end with a /, the command copies all of the files to `@test_stage/plugin_tests/plugin`.

Copy code

```
snow git copy @snowcli_git/branches/main/tests/plugin @test_stage/plugin_tests
```

## Example: Copy files from a directory in a stage to the local file system

The following example creates a `plugin_tests` directory in the local file system and downloads the contents of the `tests/plugin` directory into it.

Copy code

```
snow git copy @snowcli_git/branches/main/tests/plugin plugin_tests/
```
