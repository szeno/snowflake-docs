# Refreshing a repository

The `snow git fetch` command updates a repository stage with all branches, tags, and new commits from a remote repository.

To fetch changes in a repository, use the following command:

Copy code

```
snow git fetch <REPO_NAME>
```

where:

- `<REPO_NAME>` is the ID of the repository stage.

The following example refreshes a repository named `my_snow_git`:

Copy code

```
snow git fetch my_snow_git
```

```
alter Git repository my_snow_git fetch
+-------------------------------------------------------------------+
| status                                                            |
|-------------------------------------------------------------------|
| Git Repository MY_SNOW_GIT is up to date. No change was fetched.. |
+-------------------------------------------------------------------+
```
