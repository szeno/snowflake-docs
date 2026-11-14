# Nov 11, 2026: Select per-user quota users by role (*General availability*)

You can now define the users in a [per-user quota](/user-guide/budgets/per-user-quotas) by the roles
they hold, in addition to user tags and user names. A role selects the users who are directly granted
it, so quota scope stays current as you grant and revoke roles, including roles that your identity
provider provisions.

The new `SET_QUOTA_USER_SCOPE`, `ADD_QUOTA_USER_SCOPE`, and `REMOVE_QUOTA_USER_SCOPE` methods define
the scope in three parts: which users to include (all users, or a group selected by user tags, roles,
or both), which groups of users to exclude by user tag or role, and which users to always include or
exclude by name. For example, the following call scopes a quota to users who hold `ANALYST` or
`DATA_ENG`, excluding users who hold `ACCOUNTADMIN`:

Copy code

```
CALL my_quota!SET_QUOTA_USER_SCOPE(PARSE_JSON('{
  "applies_to":  {"type": "GROUP_OF_USERS", "roles": ["ANALYST", "DATA_ENG"]},
  "excluded_by": {"roles": ["ACCOUNTADMIN"]}
}'));
```

You can also exclude users by tag from quotas scoped by tag. Previously, tag exclusions applied only
to quotas that cover all users. The new `GET_QUOTA_SCOPE_V2` method returns the full scope. The
existing `SET_USER_TAGS`, `INCLUDE_USERS`, `EXCLUDE_USERS`, and `GET_QUOTA_SCOPE` methods continue to
work.

You can also select users by role in Snowsight when you create or edit a quota.

For more information, see [Specify users in scope for a per-user quota](/user-guide/budgets/per-user-quotas-user-scope).
