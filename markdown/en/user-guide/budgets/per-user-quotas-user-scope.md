# Specify users in scope for a per-user quota

A quota’s user scope determines which users the quota monitors. You define the scope in three parts:
which users to include, which groups of users to exclude, and which individual users to always include
or exclude by name. This topic explains how Snowflake combines those parts, how to select users by
role, and how to set, change, and verify the scope.

## How user scope works

The following table describes the three parts of a quota’s user scope. Each part corresponds to a
section of the payload that you pass to the scope methods:

| Part | Payload section | What it defines |
| --- | --- | --- |
| Include | `applies_to` | All users in the account (`ALL_USERS`, the default), or a group of users (`GROUP_OF_USERS`) selected by user tags, roles, or both. In a group, one operator combines every tag and role: `UNION` (the default) includes users who match at least one, and `INTERSECTION` includes users who match all of them. |
| Exclude | `excluded_by` | User tags and roles whose users are removed from the scope. A user who matches any listed tag or role is excluded. Exclusions apply to either include type. |
| Named users | `usernames` | Individual users who are always in scope (`included`) or always out of scope (`excluded`), regardless of the include and exclude parts. |

Expand

Show lessSee more

Snowflake resolves the users in scope in the following order:

1. Start with the users selected by the include part.
2. Remove users who match any excluded tag or role.
3. Remove users named in `usernames.excluded`.
4. Add users named in `usernames.included`.

Because named users are applied last, a user in `usernames.included` is in scope even when an excluded
role or tag matches them, and a user in `usernames.excluded` is out of scope even when they match the
include part.

Snowflake resolves users at evaluation time, so changes to tag assignments and role grants are
reflected in the quota without any reconfiguration. A user can belong to more than one quota. Each
quota evaluates that user’s spending against its own limit independently.

### How role-based selection works

Selecting users by role determines who is in scope, not which usage counts toward the limit. The
quota monitors each user in scope individually; it doesn’t set a shared limit for everyone with a
role.

Only roles granted directly to a user count when including or excluding that user by role.
Inherited roles don’t count. For example, if `ANALYST` is granted to `TEAM_ROLE` and `TEAM_ROLE` is
granted to a user, selecting `ANALYST` doesn’t select that user through the inherited grant.

Once a user is in scope, all of their usage of the quota’s monitored domains and resources counts
toward their per-user limit, regardless of the primary and secondary roles active when they run a
request. For example, if a quota includes `ALICE` through a direct grant of `ANALYST`, their usage
still counts when `DATA_ENG` is the primary role and `ANALYST` is only a secondary role or isn’t
active at all. Switching roles doesn’t move the user out of scope or give them a separate usage
counter.

The following restrictions also apply:

- **Some roles can’t be used.** You can’t specify the `PUBLIC` role or a role that doesn’t exist.
  A role that is dropped after you add it selects no users.
- **Unquoted role names aren’t case-sensitive.** Snowflake stores each role name as the role it
  resolves to and removes duplicates. A role created with a quoted name, such as
  `"finance_analyst"`, is case-sensitive, so include its double quotes, escaped, in the role name.

For example, the following call selects users who are granted the role `"finance_analyst"`. The
dollar-quoted string passes the escaped quotes to `PARSE_JSON` unchanged:

Copy code

```
CALL my_quota!SET_QUOTA_USER_SCOPE(PARSE_JSON($${
  "applies_to": {"type": "GROUP_OF_USERS", "roles": ["\"finance_analyst\""]}
}$$));
```

When you grant or revoke a role, the quota reflects the change after a short delay. For more
information, see [Verify the user scope](#label-per-user-quota-verify-scope).

### Users that quotas cover

A quota that covers all users includes service users, both those you create (`TYPE = SERVICE`) and
Snowflake-managed ones (`TYPE = SNOWFLAKE_SERVICE`), such as Snowpark Container Services identities. You
can tag, include, and exclude `SERVICE` users like any other user, but you can’t tag or name
`SNOWFLAKE_SERVICE` users.

Quotas don’t cover the system user, which runs tasks and dynamic table refreshes by default. To count
that usage toward a quota, run them with `EXECUTE AS USER`.

## Set the user scope

To set the user scope, call `SET_QUOTA_USER_SCOPE` with a payload that contains one or more of the
`applies_to`, `excluded_by`, and `usernames` sections. The method replaces each list that you pass
and leaves the lists that you omit unchanged. To clear a list, pass an empty array. To call the scope
methods, use a role granted the quota’s `ADMIN` instance role, with the `USAGE` privilege on the
quota’s database and schema.

Snowflake applies the sections in a fixed order, regardless of their order in the payload:
`applies_to`, `excluded_by.user_tags`, `excluded_by.roles`, and then `usernames`. Lists that you
pass in the same call as a new include type are written after the include type changes, so the
change doesn’t clear them. `ADD_QUOTA_USER_SCOPE` and `REMOVE_QUOTA_USER_SCOPE` use the same order.

The following rules apply to the `applies_to` section:

- `type` is required. Pass `ALL_USERS` or `GROUP_OF_USERS`.
- `ALL_USERS` doesn’t accept `operator`, `user_tags`, or `roles`. Setting `ALL_USERS` clears the
  include roles, and also clears the include tags when the quota was scoped to a group of users.
  Exclusions and named users are kept.
- `GROUP_OF_USERS` requires `user_tags`, `roles`, or both, but either or both can be empty arrays.
  If you omit `operator`, the operator is set to `UNION`, even if it was `INTERSECTION` before.
- Each entry in `user_tags` is a pair of a tag reference and a value, in the form
  `[SYSTEM$REFERENCE('TAG', '<db>.<schema>.<tag>', 'SESSION', 'APPLYBUDGET'), '<value>']`. The role
  that sets the scope must have the `APPLYBUDGET` privilege on each tag.

`SET_QUOTA_USER_SCOPE` accepts up to 250 roles per call, counting roles already on the quota. A call
over the limit fails without changing the scope. To work with more roles, use
[ADD\_QUOTA\_USER\_SCOPE](#label-per-user-quota-add-remove-scope), which has no role limit.

The method returns the quota’s resulting user scope as a JSON string, in the same format as the
`users` object that [GET\_QUOTA\_SCOPE\_V2](#label-per-user-quota-verify-scope) returns.

**Example: Users who hold either of two roles, excluding account administrators**

Copy code

```
CALL my_quota!SET_QUOTA_USER_SCOPE(PARSE_JSON('{
  "applies_to":  {"type": "GROUP_OF_USERS", "operator": "UNION", "roles": ["ANALYST", "DATA_ENG"]},
  "excluded_by": {"roles": ["ACCOUNTADMIN"]}
}'));
```

Note

A user who holds `ACCOUNTADMIN` and `ANALYST` is out of scope in this example, because exclusions
remove matching users from the include part. To keep a specific administrator in scope, add them to
`usernames.included`.

**Example: All users except administrators and one named user**

Copy code

```
CALL my_quota!SET_QUOTA_USER_SCOPE(PARSE_JSON('{
  "applies_to":  {"type": "ALL_USERS"},
  "excluded_by": {"roles": ["ACCOUNTADMIN", "SECURITYADMIN"]},
  "usernames":   {"excluded": ["SVC_ETL"]}
}'));
```

**Example: Users who hold a role and carry a tag**

To select users who match a tag and also hold a role, use `INTERSECTION`. Because `SYSTEM$REFERENCE`
is a SQL expression rather than a JSON string literal, build the payload with `OBJECT_CONSTRUCT`
instead of `PARSE_JSON`:

Copy code

```
CALL my_quota!SET_QUOTA_USER_SCOPE(OBJECT_CONSTRUCT(
  'applies_to', OBJECT_CONSTRUCT(
    'type', 'GROUP_OF_USERS',
    'operator', 'INTERSECTION',
    'user_tags', [[(SELECT SYSTEM$REFERENCE('TAG', 'cost_mgmt_db.tags.cost_center', 'SESSION', 'APPLYBUDGET')), 'analytics']],
    'roles', ['ANALYST'])));
```

One operator applies to every include tag and role, so a scope such as “users tagged `finance` or
`analytics`, who also hold `ANALYST`” can’t be expressed in one quota.

**Example: Only named users**

To cover only the users that you name, pass empty `user_tags` and `roles` arrays. The include part
then selects no users, so only the users in `usernames.included` are in scope:

Copy code

```
CALL my_quota!SET_QUOTA_USER_SCOPE(PARSE_JSON('{
  "applies_to": {"type": "GROUP_OF_USERS", "operator": "UNION", "user_tags": [], "roles": []},
  "usernames":  {"included": ["ALICE", "CAROL"], "excluded": []}
}'));
```

**Example: Replace the list of excluded users**

Copy code

```
CALL my_quota!SET_QUOTA_USER_SCOPE(PARSE_JSON('{"usernames": {"excluded": ["BOB", "CAROL"]}}'));
```

This sets `usernames.excluded` to `BOB` and `CAROL`, and removes them from `usernames.included` if
they were listed there. The `applies_to` and `excluded_by` sections don’t change.

## Add to or remove from the user scope

To change a list without resending it, call `ADD_QUOTA_USER_SCOPE` or `REMOVE_QUOTA_USER_SCOPE`
with the entries to add or remove. Both methods accept the same sections as `SET_QUOTA_USER_SCOPE`,
with the following differences:

- Neither method accepts `type` or `operator`. To change them, use `SET_QUOTA_USER_SCOPE`.
- Each list that you pass must contain at least one entry, and the payload must contain at least one
  list.
- `ADD_QUOTA_USER_SCOPE` accepts up to 20 tags per call. It has no limit on roles.
- You can’t add include tags or roles while the include type is `ALL_USERS`.

Like `SET_QUOTA_USER_SCOPE`, both methods return the quota’s resulting user scope as a JSON string.

Adding a user to `usernames.included` removes them from `usernames.excluded`, and the reverse is
also true. Removing a user from one username list doesn’t add them to the other list. Removing an
entry that isn’t on the list leaves the list unchanged.

**Example: Add a role to the exclusions**

Copy code

```
CALL my_quota!ADD_QUOTA_USER_SCOPE(PARSE_JSON('{"excluded_by": {"roles": ["CONTRACTOR_RL"]}}'));
```

**Example: Add a role to the include part**

The include tags and the operator don’t change:

Copy code

```
CALL my_quota!ADD_QUOTA_USER_SCOPE(PARSE_JSON('{"applies_to": {"roles": ["DATA_STEWARD"]}}'));
```

**Example: Add a tag value to the exclusions**

Copy code

```
CALL my_quota!ADD_QUOTA_USER_SCOPE(OBJECT_CONSTRUCT(
  'excluded_by', OBJECT_CONSTRUCT('user_tags',
    [[(SELECT SYSTEM$REFERENCE('TAG', 'cost_mgmt_db.tags.employment', 'SESSION', 'APPLYBUDGET')), 'intern']])));
```

**Example: Remove a role and a user from the exclusions**

Copy code

```
CALL my_quota!REMOVE_QUOTA_USER_SCOPE(PARSE_JSON('{
  "excluded_by": {"roles": ["CONTRACTOR_RL"]},
  "usernames":   {"excluded": ["BOB"]}
}'));
```

## Rejected scope changes

Snowflake validates each call before it writes anything. A rejected call returns an error and leaves
the stored scope unchanged. The scope methods reject the following payloads:

- An empty payload, or a section with no fields.
- Unknown fields, including `shared_resources`. To change monitored domains, use
  `ADD_SHARED_RESOURCE` and `REMOVE_SHARED_RESOURCE`.
- `NULL` values or values of the wrong type.
- In `SET_QUOTA_USER_SCOPE`, an `applies_to` section without `type`, or with a `type` other than
  `ALL_USERS` or `GROUP_OF_USERS`.
- `ALL_USERS` with `operator`, `user_tags`, or `roles`.
- `GROUP_OF_USERS` with neither `user_tags` nor `roles`.
- A tag passed by name instead of by `SYSTEM$REFERENCE`.
- The `PUBLIC` role, or a role that doesn’t exist.
- The same user in both `usernames.included` and `usernames.excluded`, in `SET_QUOTA_USER_SCOPE` or
  `ADD_QUOTA_USER_SCOPE`.
- `type` or `operator` in `ADD_QUOTA_USER_SCOPE` or `REMOVE_QUOTA_USER_SCOPE`.
- `applies_to.user_tags` or `applies_to.roles` in `ADD_QUOTA_USER_SCOPE` while the include type is
  `ALL_USERS`.
- More than 250 roles in `SET_QUOTA_USER_SCOPE`, counting roles already on the quota.

## Verify the user scope

To view the quota’s full scope, call `GET_QUOTA_SCOPE_V2`:

Copy code

```
CALL my_quota!GET_QUOTA_SCOPE_V2();
```

A role granted the quota’s `ADMIN` or `VIEWER` instance role can call this method.

The method returns a JSON string that contains a `users` object, in the same format as the scope
payload, and the monitored domains in `shared_resources`. To query the result as JSON, parse it with
`PARSE_JSON`:

Copy code

```
CALL my_quota!GET_QUOTA_SCOPE_V2()
  ->> SELECT PARSE_JSON("GET_QUOTA_SCOPE_V2"):users AS users FROM $1;
```

For example, the method returns the following scope:

Copy code

```
{
  "users": {
    "applies_to": {
      "type": "GROUP_OF_USERS",
      "operator": "UNION",
      "user_tags": [
        {"tagId": 34, "tagDatabase": "COST_MGMT_DB", "tagSchema": "TAGS", "tagName": "DEPT", "tagValues": ["eng"]}
      ],
      "roles": ["ANALYST"]
    },
    "excluded_by": {
      "user_tags": [
        {"tagId": 12, "tagDatabase": "COST_MGMT_DB", "tagSchema": "TAGS", "tagName": "EMPLOYMENT", "tagValues": ["contractor"]}
      ],
      "roles": ["ACCOUNTADMIN"]
    },
    "usernames": {
      "included": [{"id": 304, "name": "ALICE"}],
      "excluded": [{"id": 306, "name": "BOB"}]
    }
  },
  "shared_resources": []
}
```

When the include type is `ALL_USERS`, `applies_to` contains only `{"type": "ALL_USERS"}`.

To list the users currently resolved into the quota’s scope:

Copy code

```
CALL my_quota!GET_USERS();
```

Note

`GET_USERS` reflects tag changes and role grants and revokes after approximately 10 to 15 minutes.

## Automate user roles and tags with SCIM

If you provision users through a SCIM identity provider, you can map identity provider groups to
Snowflake roles that are granted directly to users, or use the `snowflakeTags` attribute to apply user
tags automatically when users are created or updated. For more information about SCIM user tags, see
[Automating user tags with SCIM](/user-guide/cost-attributing#label-cost-attribute-scim). For provider-specific setup steps, see
the following topics:

- [SCIM with Microsoft Entra ID](/user-guide/scim-azure)
- [SCIM with Okta](/user-guide/scim-okta)
- [SCIM with a custom identity provider](/user-guide/scim-custom)

## Legacy scope methods

The `SET_USER_TAGS`, `INCLUDE_USERS`, and `EXCLUDE_USERS` methods and the `GET_QUOTA_SCOPE` method
still work, but they can’t select or exclude users by role. Snowflake recommends using
`SET_QUOTA_USER_SCOPE`, `ADD_QUOTA_USER_SCOPE`, `REMOVE_QUOTA_USER_SCOPE`, and
`GET_QUOTA_SCOPE_V2` instead.

### SET\_USER\_TAGS

`SET_USER_TAGS` replaces the include tags and sets the operator: `UNION`, `INTERSECTION`, or
`ALL_USERS`. The operator argument is required, even when you pass a single tag.

Copy code

```
CALL my_quota!SET_USER_TAGS(
    [
        [(SELECT SYSTEM$REFERENCE('TAG', 'cost_mgmt_db.tags.cost_center', 'SESSION', 'APPLYBUDGET')), 'finance'],
        [(SELECT SYSTEM$REFERENCE('TAG', 'cost_mgmt_db.tags.dept', 'SESSION', 'APPLYBUDGET')), 'analytics']
    ],
    'UNION'
);

-- Return the quota to all users. Pass an empty tag array.
CALL my_quota!SET_USER_TAGS([], 'ALL_USERS');
```

`SET_USER_TAGS` doesn’t change include or exclude roles. Its other effects depend on the operator:

- With `UNION` or `INTERSECTION`, it changes only the include tags and the operator.
- With `ALL_USERS`, it clears the include tags and the tag exclusions. When the quota was scoped to a
  group of users, it also clears both username lists.
- Don’t pass tags with `ALL_USERS` to exclude users. To exclude users by tag, use
  `EXCLUDE_USERS('TAG', ...)` or `excluded_by.user_tags`.

### EXCLUDE\_USERS with tags

`EXCLUDE_USERS('TAG', ...)` replaces the tag exclusions. It doesn’t change the include part. To
clear the tag exclusions, pass an empty array.

Copy code

```
CALL my_quota!EXCLUDE_USERS('TAG', [
    [(SELECT SYSTEM$REFERENCE('TAG', 'cost_mgmt_db.tags.usage_tier', 'SESSION', 'APPLYBUDGET')), 'high']
]);
```

### INCLUDE\_USERS and EXCLUDE\_USERS with user names

`INCLUDE_USERS` and `EXCLUDE_USERS('USER', ...)` add names to the username lists. Calling either one
again adds to the existing list rather than replacing it, and adding a user to one list removes them
from the other. To clear a list, pass an empty array.

Copy code

```
CALL my_quota!INCLUDE_USERS(['ALICE', 'BOB']);
CALL my_quota!EXCLUDE_USERS('USER', ['CAROL']);
```

### GET\_QUOTA\_SCOPE

`GET_QUOTA_SCOPE` returns the monitored domains, the users included and excluded by name, and the
include and exclude tags and the operator. It doesn’t return roles. To see the full scope, including
roles, use [GET\_QUOTA\_SCOPE\_V2](#label-per-user-quota-verify-scope).

### Migrate to the new scope methods

The following table maps each legacy call to its replacement:

| Legacy call | Replacement |
| --- | --- |
| `SET_USER_TAGS(<tags>, 'UNION')` or `'INTERSECTION'` | `SET_QUOTA_USER_SCOPE` with `applies_to` set to `GROUP_OF_USERS`, the operator, and `user_tags`. |
| `SET_USER_TAGS([], 'ALL_USERS')` | `SET_QUOTA_USER_SCOPE` with `applies_to` set to `ALL_USERS`. Unlike the legacy call, this clears the include roles and keeps the tag exclusions and named users. To also clear those, pass an empty `excluded_by.user_tags` list and empty `usernames` lists in the same call. |
| `SET_USER_TAGS(<tags>, 'ALL_USERS')` | `SET_QUOTA_USER_SCOPE` with `applies_to` set to `ALL_USERS` and the tags in `excluded_by.user_tags`. Unlike the legacy call, this clears the include roles and keeps both username lists. |
| `EXCLUDE_USERS('TAG', <tags>)` | `SET_QUOTA_USER_SCOPE` with `excluded_by.user_tags`. To add or remove one tag, use `ADD_QUOTA_USER_SCOPE` or `REMOVE_QUOTA_USER_SCOPE`. |
| `INCLUDE_USERS(<names>)` | `ADD_QUOTA_USER_SCOPE` with `usernames.included`. To replace the list, use `SET_QUOTA_USER_SCOPE`. |
| `EXCLUDE_USERS('USER', <names>)` | `ADD_QUOTA_USER_SCOPE` with `usernames.excluded`. To replace the list, use `SET_QUOTA_USER_SCOPE`. |
| `INCLUDE_USERS([])` or `EXCLUDE_USERS('USER', [])` | `SET_QUOTA_USER_SCOPE` with an empty `usernames.included` or `usernames.excluded` list. |
| `GET_QUOTA_SCOPE()` | `GET_QUOTA_SCOPE_V2()` |

Expand

Show lessSee more

## Related content

- [Per-user quotas](/user-guide/budgets/per-user-quotas)
- [Create and configure a per-user quota](/user-guide/budgets/per-user-quotas-create)
- [Per-user quota method reference](/user-guide/budgets/per-user-quotas-reference)
