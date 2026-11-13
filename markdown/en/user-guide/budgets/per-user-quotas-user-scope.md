# Specify users in scope for a per-user quota

A quota’s user scope determines which users the quota measures and enforces limits on. This topic
explains the default scope, how to narrow it with tags, how to include or exclude individual users,
and how to verify the result.

## Default scope and covered users

By default, a new quota monitors all users in the account, so no scope configuration is required.
You can narrow the scope to a subset of users with tags, add or remove individual users by name, or
combine both.

A quota that covers all users includes service users, both those you create (`TYPE = SERVICE`) and
Snowflake-managed ones (`TYPE = SNOWFLAKE_SERVICE`), such as Snowpark Container Services identities. You
can tag, include, and exclude `SERVICE` users like any other user, but you can’t tag or name
`SNOWFLAKE_SERVICE` users.

Quotas don’t cover the system user, which runs tasks and dynamic table refreshes by default. To count
that usage toward a quota, run them with `EXECUTE AS USER`.

## Scope users with tags

To scope the quota to users selected by tag, call `SET_USER_TAGS` with the tags, passed by reference,
and how to combine them: `UNION` or `INTERSECTION`. The operator argument is required, even when you
pass a single tag; calling `SET_USER_TAGS` without it returns an error. The `SET_USER_TAGS` call is atomic
and idempotent: any existing tags are overwritten.

Copy code

```
CALL my_quota!SET_USER_TAGS(
    [
        [(SELECT SYSTEM$REFERENCE('TAG', 'cost_mgmt_db.tags.cost_center', 'SESSION', 'APPLYBUDGET')), 'finance'],
        [(SELECT SYSTEM$REFERENCE('TAG', 'cost_mgmt_db.tags.dept', 'SESSION', 'APPLYBUDGET')), 'analytics']
    ],
    'UNION'
);
```

Note

The role used to set user tags on a quota must have the `APPLYBUDGET` privilege on each tag.

To return a quota to all users, call `SET_USER_TAGS` with an empty tag array and `ALL_USERS` in place
of `UNION` or `INTERSECTION`:

Copy code

```
CALL my_quota!SET_USER_TAGS([], 'ALL_USERS');
```

Note

- Pass an empty tag array with `ALL_USERS`. Don’t pass tags with `ALL_USERS` to exclude users. To
  exclude users by tag, use `EXCLUDE_USERS('TAG', ...)` as described in the next section.
- `SET_USER_TAGS([], 'ALL_USERS')` also clears any tag exclusions on the quota. Set tag exclusions
  again after you call it.
- After any change to the user scope, call `GET_USERS` to confirm which users are in scope.

## Exclude users by tag

To remove users who carry specific tags from the scope, call `EXCLUDE_USERS` with the `'TAG'`
keyword and the tags that identify the users to exclude. Tag exclusions apply in either scope mode:
they remove matching users from all users or from users selected by tag. The call replaces any
existing tag exclusions and doesn’t change the scope mode or the tags used to select users.

In the following example, the quota excludes any user tagged with a `usage_tier` tag whose value is
`high`:

Copy code

```
CALL my_quota!EXCLUDE_USERS('TAG', [
    [(SELECT SYSTEM$REFERENCE('TAG', 'cost_mgmt_db.tags.usage_tier', 'SESSION', 'APPLYBUDGET')), 'high']
]);
```

To clear all tag exclusions, pass an empty array:

Copy code

```
CALL my_quota!EXCLUDE_USERS('TAG', []);
```

## Include or exclude individual users

To add specific users directly, pass their names to `INCLUDE_USERS`. To exclude specific users, pass
their names to `EXCLUDE_USERS` with the `'USER'` keyword:

Copy code

```
CALL my_quota!INCLUDE_USERS(['ALICE', 'BOB']);
CALL my_quota!EXCLUDE_USERS('USER', ['CAROL']);
```

Unlike `SET_USER_TAGS`, both methods accumulate. Calling either one again adds to the existing list
rather than replacing it. Including a user who is on the exclude list moves them to the include list,
and the reverse is also true.

Naming a user this way takes precedence over the quota’s tag scope. An included user is monitored
whether or not they match the tags, and an excluded user stays out even while they still match. Later
tag changes don’t override the named lists: a user who gains a matching tag joins the scope, but a
user you excluded by name stays excluded.

Note

To clear a list, pass an empty array: `INCLUDE_USERS([])` or `EXCLUDE_USERS('USER', [])`.

Switching the quota from users selected by tag back to all users clears both lists, so adjust
individual users after you set the scope:

| Scope change | Effect on the include and exclude lists |
| --- | --- |
| From users selected by tag to all users | Both lists are cleared. |
| From all users to all users (calling `ALL_USERS` again) | Both lists are kept. |
| From all users to users selected by tag (`UNION` or `INTERSECTION`) | Both lists are kept. |

Expand

Show lessSee more

A user can belong to more than one quota. Each quota evaluates that user’s spending against its own
limit independently.

## Verify the user scope

To verify the current user scope:

Copy code

```
CALL my_quota!GET_QUOTA_SCOPE();
```

The method returns a JSON object showing the attached monitored domains, the users included and
excluded by name, the configured tags, and the operator:

Copy code

```
{
  "excluded_users": [
    {
      "user_id": 3817,
      "user_name": "CAROL"
    }
  ],
  "included_users": [
    {
      "user_id": 2153,
      "user_name": "ALICE"
    },
    {
      "user_id": 6253,
      "user_name": "BOB"
    }
  ],
  "shared_resources": [
    {
      "domain": "CORTEX_AGENT",
      "id": -1,
      "name": "[ALL-AGENTS]"
    }
  ],
  "user_tags": {
    "operator": "UNION",
    "tags": [
      {
        "type": "tag",
        "tag_database": "cost_mgmt_db",
        "tag_schema": "tags",
        "tag_key": "COST_CENTER",
        "tag_values": ["FINANCE"]
      },
      {
        "type": "tag",
        "tag_database": "cost_mgmt_db",
        "tag_schema": "tags",
        "tag_key": "DEPT",
        "tag_values": ["ANALYTICS"]
      }
    ]
  }
}
```

The `shared_resources` array lists the monitored domains added with
[ADD\_SHARED\_RESOURCE](/user-guide/budgets/per-user-quotas#label-per-user-quota-supported-resources).
When a whole domain is attached rather than a specific resource, the entry has an `id` of `-1` and a
bracketed `name` such as `[ALL-AGENTS]`.

The `included_users` and `excluded_users` arrays list the users added or removed by name with
`INCLUDE_USERS` and `EXCLUDE_USERS`. Both arrays are empty when the quota is scoped only by tags.

To list the users currently resolved into the quota’s scope:

Copy code

```
CALL my_quota!GET_USERS();
```

Note

- Use `GET_QUOTA_SCOPE` to confirm which domains a quota monitors after calling `ADD_SHARED_RESOURCE`
  or `REMOVE_SHARED_RESOURCE`.
- User resolution relies on [TAG\_REFERENCES](/sql-reference/account-usage/tag_references), which can
  lag by up to approximately 2 hours. Recent tag changes might not appear in `GET_USERS` immediately.

## Automate user tagging with SCIM

If you want to automate user tagging, you can provision users through a SCIM identity provider
and use the `snowflakeTags` attribute to apply tags automatically when users are created or
updated. For more information, see [Automating user tags with SCIM](/user-guide/cost-attributing#label-cost-attribute-scim).
For provider-specific setup steps, see the following topics:

- [SCIM with Microsoft Entra ID](/user-guide/scim-azure)
- [SCIM with Okta](/user-guide/scim-okta)
- [SCIM with a custom identity provider](/user-guide/scim-custom)

## Related content

- [Per-user quotas](/user-guide/budgets/per-user-quotas)
- [Create and configure a per-user quota](/user-guide/budgets/per-user-quotas-create)
- [Per-user quota method reference](/user-guide/budgets/per-user-quotas-reference)
