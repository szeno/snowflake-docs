# Listing the contents of a repository

Snowflake CLI supports the following ways to list the contents of a Git repository:

- [List branches in a repository](#label-snowcli-git-list-branches)
- [List tags in a repository](#label-snowcli-git-list-tags)
- [List files in a repository](#label-snowcli-git-list-files)

## List branches in a repository

The `snow git list-branches` command lists all of the branches in a repository.

Copy code

```
snow git list-branches <REPO_NAME>
```

where:

- `<REPO_NAME>` is the ID of the repository stage.

For example, to list all of the branches in a repository named `my_snow_git`, enter the following command:

Copy code

```
snow git list-branches my_snow_git
```

```
show git branches in my_snow_git
+--------------------------------------------------------------------------------------------------------------------------------------------+
| name                                     | path                                     | checkouts | commit_hash                              |
|------------------------------------------+------------------------------------------+-----------+------------------------------------------|
| SNOW-1011750-service-create-options      | /branches/SNOW-1011750-service-create-op |           | 729855df0104c8d0ef1c7a3e8f79fe50c6c8d2fa |
|                                          | tions                                    |           |                                          |
| SNOW-1011775-containers-to-spcs-int-test | /branches/SNOW-1011775-containers-to-spc |           | e81b00de6b0eb73a99a7baaa39b0afa5ea1202d0 |
| s                                        | s-int-tests                              |           |                                          |
| SNOW-1105629-git-integration-tests       | /branches/SNOW-1105629-git-integration-t |           | 712b07b5e692624c34caabe07d64801615ce5f0f |
+--------------------------------------------------------------------------------------------------------------------------------------------+
```

## List tags in a repository

The `snow git list-tabs` command lists all of the tags in a repository.

Copy code

```
snow git list-tags <REPO_NAME>
```

where:

- `<REPO_NAME>` is the ID of the repository stage you want to create. Note that if the repository stage already exists, the command fails.

For example, to list all of the tags in a repository named `my_snow_git`, enter the following command:

Copy code

```
snow git list-tags my_snow_git
```

```
show git tags in my_snow_git
+--------------------------------------------------------------------------------------------------------------+
| name           | path                 | commit_hash                 | author                       | message |
|----------------+----------------------+-----------------------------+------------------------------+---------|
| v2.0.0rc3      | /tags/v2.0.0rc3      | 2b019d2841da823d8001f23c6f3 | None                         | None    |
|                |                      | 064e5899142a0               |                              |         |
| v2.1.0-rc0     | /tags/v2.1.0-rc0     | 829887b758b43b86959611dd612 | None                         | None    |
|                |                      | 7638da75cf871               |                              |         |
| v2.1.0-rc1     | /tags/v2.1.0-rc1     | b7efe1fe9c0925b95ba214e233b | None                         | None    |
|                |                      | 18924fa0404b3               |                              |         |
+--------------------------------------------------------------------------------------------------------------+
```

## List files in a repository

The `snow git list-files` command lists all of the files on a specified repository state (a specific branch, tag or commit).

Copy code

```
snow git list-files <REPO_PATH>
```

where:

- `<REPO_PATH>` is a stage path with a specific scope where the value is the repository name is followed by a suffix specifying which branch, tag or commit. The following lists some different types of values:

  - `@snowcli_git/branches/main/` refers to last commit of the `main` branch.
  - `@snowcli_git/tags/v2.1.0/` refers to a commit tagged `v2.1.0`.
  - `@snowcli_git/commits/1e939d69ca6fd0f89074e7e97c9fd1/` refers to a specific commit. Commit hashes should be between 6 and 40 characters long.

  A repository path can also be a subdirectory or file in the repository, but still must be preceded with a scope prefix.

The following example lists all of the files in the `my_snow_git` repository marked with the `v2.0.0` tag:

Copy code

```
snow git list-files @my_snow_git/tags/v2.0.0/
```

```
ls @snowcli_git/tags/v2.0.0/
+---------------------------------------------------------------------------------------------------------------------------------+
| name                                    | size | md5  | sha1                                     | last_modified                |
|-----------------------------------------+------+------+------------------------------------------+------------------------------|
| snowcli_git/tags/v2.0.0/CONTRIBUTING.md | 5472 | None | 1cc437b88d20afe4d5751bd576114e3b20be27ea | Mon, 5 Feb 2024 13:16:25 GMT |
| snowcli_git/tags/v2.0.0/LEGAL.md        | 251  | None | 4453da50b7a2222006289ff977bfb23583657214 | Mon, 5 Feb 2024 13:16:25 GMT |
| snowcli_git/tags/v2.0.0/README.md       | 1258 | None | bdc918baae93467c258c6634c872ca6bd4ee1e9c | Mon, 5 Feb 2024 13:16:25 GMT |
| snowcli_git/tags/v2.0.0/SECURITY.md     | 308  | None | 27e7e1b2fd28a86943b3f4c0a35a931577422389 | Mon, 5 Feb 2024 13:16:25 GMT |
| ...
+---------------------------------------------------------------------------------------------------------------------------------+
```

The following example lists all of the files in the `tests/` directory of the `my_snow_git` repository marked with the `v2.0.0` tag:

Copy code

```
snow git list-files @my_snow_git/tags/v2.0.0/tests --pattern ".*\.toml"
```

```
ls @snowcli_git/tags/v2.0.0/tests pattern = '.*\.toml'
+-----------------------------------------------------------------------------------------------------------------------------------------+
| name                                            | size | md5  | sha1                                     | last_modified                |
|-------------------------------------------------+------+------+------------------------------------------+------------------------------|
| snowcli_git/tags/v2.0.0/tests/empty_config.toml | 0    | None | e69de29bb2d1d6434b8b29ae775ad8c2e48c5391 | Mon, 5 Feb 2024 13:16:25 GMT |
| snowcli_git/tags/v2.0.0/tests/test.toml         | 381  | None | 45f1c00f16eba1b7bc7b4ab2982afe95d0161e7f | Mon, 5 Feb 2024 13:16:25 GMT |
+-----------------------------------------------------------------------------------------------------------------------------------------+
```
