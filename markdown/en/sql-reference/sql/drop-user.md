# DROP USER

Removes the specified user from the system.

See also:
:   [CREATE USER](/sql-reference/sql/create-user) , [ALTER USER](/sql-reference/sql/alter-user) , [SHOW USERS](/sql-reference/sql/show-users) , [DESCRIBE USER](/sql-reference/sql/desc-user)

## Syntax

Copy code

```
DROP USER [ IF EXISTS ] <name>
```

## Parameters

`name`
:   Specifies the identifier for the user to drop. If the identifier contains spaces, special characters, or mixed-case characters, the
    entire string must be enclosed in double quotes. Identifiers enclosed in double quotes are also case-sensitive.

## Usage notes

- Dropped users cannot be recovered; they must be recreated.

  If you want to disable a user, use [ALTER USER](/sql-reference/sql/alter-user) and set `DISABLED = TRUE` instead.
- If there is a conflict between a local user object and an [organization user](/user-guide/organization-users), a user that
  corresponds to the organization user is automatically created when you drop the local user.

- When the IF EXISTS clause is specified and the target object doesn’t exist, the command completes successfully
  without returning an error.

Important

When you drop a user, the folders, worksheets, and dashboards owned by that user become inaccessible and **do not** transfer to another user
unless sharing is enabled.

Share recipients with [View, View + Run, and Edit permissions](/user-guide/ui-snowsight-worksheets#label-sharing-worksheets-and-folders)
will retain their assigned permissions and can still access the shared folders, worksheets, and dashboards. However, only users with Edit
permissions can modify or delete the shared folders, worksheets, and dashboards. If you don’t give Edit permissions to at least one other
user before you drop the owner, that owner’s folders, worksheets, and dashboards cannot be deleted.

If a dropped user’s worksheets do not have sharing enabled, an administrator can [recover up to 500 worksheets owned by the user](/user-guide/ui-snowsight-worksheets#label-snowsight-worksheets-recover).

Caution

Any worksheets in the Classic Console will be permanently deleted, and dashboards will be inaccessible if they were not previously shared
with another user.

## Examples

> Copy code
>
> ```
> DROP USER user1;
> ```
