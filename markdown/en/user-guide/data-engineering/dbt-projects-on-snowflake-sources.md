# Supported dbt project source file locations

dbt project object source files can be in any one of the following locations:

> - **An internal named stage**, for example:
>
>   `'@my_db.my_schema.my_internal_named_stage/path/to/dbt_projects_or_projects_parent'`
>
>   Internal user stages and table stages aren’t supported.
> - **A dbt workspace**, for example:
>
>   `'snow://workspace/user$.public."my_workspace_name"/versions/live'`
>
>   Workspace URIs use `versions/live`, which refers to the active working state of the workspace. We recommend enclosing the workspace name in double quotes because workspace names are case-sensitive and can contain special characters.
> - **An existing dbt project stage**, for example:
>
>   `'snow://dbt/my_db.my_schema.my_existing_dbt_project_object/versions/live'`
>
>   The version specifier is required and is `live`.
> - **A Git repository stage**, for example:
>
>   `'@my_db.my_schema.my_git_repository_stage/branches/my_branch/path/to/dbt_project_or_projects_parent'`
>
>   For more information about creating and managing a Git repository object and stage, see [Using a Git repository in Snowflake](/developer-guide/git/git-overview) and [CREATE GIT REPOSITORY](/sql-reference/sql/create-git-repository).
