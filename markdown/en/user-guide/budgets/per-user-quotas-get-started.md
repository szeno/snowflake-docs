# Get started with per-user quotas

This topic walks through setting up an account-wide AI spending guardrail in a few minutes, followed
by the most common patterns organizations use to structure per-user quotas across roles, teams,
usage tiers, and individual exceptions.

## Set up an account-wide AI guardrail

The fastest way to prevent unexpected AI spend is to create a single quota that covers all users in
the account, sets both a monthly limit and a daily burst limit,
and blocks users automatically when they reach either limit.

Run the following statements with the `ACCOUNTADMIN` role. To delegate quota administration to a custom role, see
[Create a custom role for quota administration](/user-guide/budgets/per-user-quotas-create#label-per-user-quota-admin-role).

Copy code

```
USE SCHEMA cost_mgmt_db.quota_schema;

-- 1. Create the quota.
CREATE SNOWFLAKE.CORE.QUOTA account_ai_guardrail();

-- 2. Monitor all AI domains.
CALL account_ai_guardrail!ADD_SHARED_RESOURCE('AI FUNCTION');
CALL account_ai_guardrail!ADD_SHARED_RESOURCE('SNOWFLAKE COCO');
CALL account_ai_guardrail!ADD_SHARED_RESOURCE('CORTEX AGENT');
CALL account_ai_guardrail!ADD_SHARED_RESOURCE('SNOWFLAKE COWORK');
CALL account_ai_guardrail!ADD_SHARED_RESOURCE('AI GATEWAY');

-- 3. Cover all users in the account.
CALL account_ai_guardrail!SET_QUOTA_USER_SCOPE(PARSE_JSON('{"applies_to": {"type": "ALL_USERS"}}'));

-- 4. Set a 500-credit monthly limit and a 100-credit daily burst limit per user.
CALL account_ai_guardrail!SET_PER_USER_LIMIT(500);
CALL account_ai_guardrail!SET_PER_USER_LIMIT(100, 'DAILY');

-- 5. Email users when their projected monthly spend reaches 80% of the limit.
CALL account_ai_guardrail!ADD_NOTIFICATION_THRESHOLD(80, 'PROJECTED', TRUE, 'MONTHLY');
```

Before you enable enforcement, verify the quota’s scope, limits, and resolved user list:

Copy code

```
CALL account_ai_guardrail!GET_QUOTA_SCOPE_V2();
CALL account_ai_guardrail!GET_CONFIG();
CALL account_ai_guardrail!GET_USERS();
```

`GET_USERS` is eventually consistent: it can take approximately 10 to 15 minutes to reflect tag and role
changes. If the user list isn’t what you expect, wait and call `GET_USERS` again before you change the scope.

After the scope is correct, enable built-in block enforcement and email users when they’re blocked:

Copy code

```
CALL account_ai_guardrail!SET_BLOCK_ENFORCEMENT_ENABLED(TRUE, TRUE);
```

Any user in the account can check their own usage and remaining headroom at any time without
additional privileges:

Copy code

```
SELECT * FROM TABLE(SNOWFLAKE.LOCAL.MY_BUDGET_SUMMARY());
```

## Choose an implementation pattern

Most organizations use one or a combination of the following patterns to match how they manage
users and budgets:

| Pattern | When to use it | How it’s configured |
| --- | --- | --- |
| [Account-wide guardrail](#label-per-user-quota-account-guardrail) | You want one baseline ceiling for everyone in the account. | One quota with `ALL_USERS`. |
| [Quotas by role or team](#label-per-user-quota-pattern-roles-teams) | Different functional roles or departments need different default limits. | One quota per role (`applies_to.roles`) or department tag (`applies_to.user_tags`). |
| [Quotas by usage tier](#label-per-user-quota-pattern-usage-tiers) | You group users into capacity tiers (for example, standard users at 200 credits and power users at 1,000 credits). | One quota per tier role or `usage_tier` tag value. |
| [Role within a cost center](#label-per-user-quota-pattern-intersection) | The same functional role has different budgets depending on the business unit or cost center. | One quota per combination, using `operator = 'INTERSECTION'` with both `roles` and `user_tags`. |
| [Single-user or temporary exceptions](#label-per-user-quota-pattern-overrides) | Specific users need a temporary boost for a project or a custom ongoing cap without changing their roles or tags. | `SET_USER_QUOTA_OVERRIDE` on the existing quota (up to 200 overrides per quota). |

Expand

Show lessSee more

Important

In each pattern, the script enables block enforcement right after it sets the scope. Instead, call
`SET_BLOCK_ENFORCEMENT_ENABLED` only after `GET_USERS` returns the users you expect, which can take approximately
10 to 15 minutes. If you combine patterns with the account-wide guardrail, the lowest limit across overlapping
quotas binds, so the guardrail also caps any higher tier limit. Set the guardrail limits above your highest tier,
or add the higher-tier roles to the guardrail’s `excluded_by.roles`.

## Pattern 1: Quotas for different roles or teams

When teams already have functional roles in Snowflake (such as `ANALYST` and `DATA_ENG`), you can
scope a quota to each role. Quota membership updates automatically as you grant and revoke those
roles, including through SCIM.

Important

When you scope quotas by role, use the same role to grant access to the features the quota monitors.
For example, grant Snowflake CoCo access only through a `COCO_POWER_USER` role, or grant access to all
AI features only through an `AI_POWER_USER` role, and scope the matching quota to that role. Granting
the role then gives a user both the access and the limit, and revoking it removes both. For this
pairing to hold, the role must be the only way users get that access, so don’t also grant that access
to other roles, such as `PUBLIC`. Also grant the role directly to users: a user who gets it through
another role gains the access but isn’t selected by the quota.

Before you scope a quota to a role, keep these two rules in mind:

- Only **direct** grants to users count. To check which users are directly granted a role, run
  `SHOW GRANTS OF ROLE <role_name>;` and inspect rows where `granted_to = 'USER'`. For more information, see
  [How role-based selection works](/user-guide/budgets/per-user-quotas-user-scope#label-per-user-quota-role-selection).
- If a user holds **both** roles and belongs to two quotas that monitor the same domain, both quotas
  count all of that user’s spend in the domain, and the **lowest limit binds**. For more information, see
  [Override limits for specific users](/user-guide/budgets/per-user-quotas-overrides).

To prevent a lower-limit role quota from capping users who also hold a higher-limit role, exclude
the higher-limit role from the lower-limit quota:

Copy code

```
USE SCHEMA cost_mgmt_db.quota_schema;

-- Analysts: 200 credits/month.
-- Exclude DATA_ENG so users who hold both ANALYST and DATA_ENG
-- are governed only by the higher data_eng_ai_quota limit.
CREATE SNOWFLAKE.CORE.QUOTA analyst_ai_quota();
CALL analyst_ai_quota!ADD_SHARED_RESOURCE('SNOWFLAKE COCO');
CALL analyst_ai_quota!ADD_SHARED_RESOURCE('CORTEX AGENT');
CALL analyst_ai_quota!ADD_SHARED_RESOURCE('SNOWFLAKE COWORK');
CALL analyst_ai_quota!SET_QUOTA_USER_SCOPE(PARSE_JSON('{
  "applies_to":  {"type": "GROUP_OF_USERS", "operator": "UNION", "roles": ["ANALYST"]},
  "excluded_by": {"roles": ["DATA_ENG"]}
}'));
CALL analyst_ai_quota!SET_PER_USER_LIMIT(200);
CALL analyst_ai_quota!SET_BLOCK_ENFORCEMENT_ENABLED(TRUE, TRUE);

-- Data engineers: 600 credits/month.
CREATE SNOWFLAKE.CORE.QUOTA data_eng_ai_quota();
CALL data_eng_ai_quota!ADD_SHARED_RESOURCE('SNOWFLAKE COCO');
CALL data_eng_ai_quota!ADD_SHARED_RESOURCE('CORTEX AGENT');
CALL data_eng_ai_quota!ADD_SHARED_RESOURCE('SNOWFLAKE COWORK');
CALL data_eng_ai_quota!SET_QUOTA_USER_SCOPE(PARSE_JSON('{
  "applies_to":  {"type": "GROUP_OF_USERS", "operator": "UNION", "roles": ["DATA_ENG"]}
}'));
CALL data_eng_ai_quota!SET_PER_USER_LIMIT(600);
CALL data_eng_ai_quota!SET_BLOCK_ENFORCEMENT_ENABLED(TRUE, TRUE);
```

If your organization represents teams with user tags (for example, `cost_center = 'analytics'`)
instead of roles, pass `user_tags` in `applies_to` in the same way. For details, see
[Specify users in scope](/user-guide/budgets/per-user-quotas-user-scope#label-per-user-quota-set-scope).

## Pattern 2: Quotas based on usage tiers

When users across different teams need standard versus power-user limits (for example, 1x versus 5x
Snowflake CoCo limits), define one quota per tier. You can represent tiers with either roles or user
tags.

### Option A: Tier roles

Create dedicated tier roles (such as `COCO_STANDARD_USER` and `COCO_POWER_USER`), grant Snowflake
CoCo access to those roles, and grant the appropriate tier role directly to each user. Exclude `COCO_POWER_USER`
from the standard quota so that even if a user holds both roles, the standard quota doesn’t cap
them:

Copy code

```
USE SCHEMA cost_mgmt_db.quota_schema;

-- Standard tier: 200 credits/month, 30 credits/day.
CREATE SNOWFLAKE.CORE.QUOTA coco_standard_quota();
CALL coco_standard_quota!ADD_SHARED_RESOURCE('SNOWFLAKE COCO');
CALL coco_standard_quota!SET_QUOTA_USER_SCOPE(PARSE_JSON('{
  "applies_to":  {"type": "GROUP_OF_USERS", "roles": ["COCO_STANDARD_USER"]},
  "excluded_by": {"roles": ["COCO_POWER_USER"]}
}'));
CALL coco_standard_quota!SET_PER_USER_LIMIT(200);
CALL coco_standard_quota!SET_PER_USER_LIMIT(30, 'DAILY');
CALL coco_standard_quota!SET_BLOCK_ENFORCEMENT_ENABLED(TRUE, TRUE);

-- Power-user tier: 1,000 credits/month, 150 credits/day.
CREATE SNOWFLAKE.CORE.QUOTA coco_power_quota();
CALL coco_power_quota!ADD_SHARED_RESOURCE('SNOWFLAKE COCO');
CALL coco_power_quota!SET_QUOTA_USER_SCOPE(PARSE_JSON('{
  "applies_to":  {"type": "GROUP_OF_USERS", "roles": ["COCO_POWER_USER"]}
}'));
CALL coco_power_quota!SET_PER_USER_LIMIT(1000);
CALL coco_power_quota!SET_PER_USER_LIMIT(150, 'DAILY');
CALL coco_power_quota!SET_BLOCK_ENFORCEMENT_ENABLED(TRUE, TRUE);
```

To promote a user to the power-user tier, grant them `COCO_POWER_USER`:

Copy code

```
GRANT ROLE COCO_POWER_USER TO USER alice;
```

### Option B: Tier tags

If you already tag users, use a single tag such as `cost_mgmt_db.tags.usage_tier` with values
`'standard'` and `'power'`. Because a user object can have only one value per tag at a time,
changing a user’s tag value automatically moves them from the standard quota to the power-user quota
with no overlap:

Copy code

```
USE SCHEMA cost_mgmt_db.quota_schema;

-- Standard tier: usage_tier = 'standard'.
CREATE SNOWFLAKE.CORE.QUOTA tier_standard_quota();
CALL tier_standard_quota!ADD_SHARED_RESOURCE('SNOWFLAKE COCO');
CALL tier_standard_quota!SET_QUOTA_USER_SCOPE(OBJECT_CONSTRUCT(
  'applies_to', OBJECT_CONSTRUCT(
    'type', 'GROUP_OF_USERS',
    'user_tags', [[(SELECT SYSTEM$REFERENCE('TAG', 'cost_mgmt_db.tags.usage_tier', 'SESSION', 'APPLYBUDGET')), 'standard']])));
CALL tier_standard_quota!SET_PER_USER_LIMIT(200);
CALL tier_standard_quota!SET_BLOCK_ENFORCEMENT_ENABLED(TRUE, TRUE);

-- Power-user tier: usage_tier = 'power'.
CREATE SNOWFLAKE.CORE.QUOTA tier_power_quota();
CALL tier_power_quota!ADD_SHARED_RESOURCE('SNOWFLAKE COCO');
CALL tier_power_quota!SET_QUOTA_USER_SCOPE(OBJECT_CONSTRUCT(
  'applies_to', OBJECT_CONSTRUCT(
    'type', 'GROUP_OF_USERS',
    'user_tags', [[(SELECT SYSTEM$REFERENCE('TAG', 'cost_mgmt_db.tags.usage_tier', 'SESSION', 'APPLYBUDGET')), 'power']])));
CALL tier_power_quota!SET_PER_USER_LIMIT(1000);
CALL tier_power_quota!SET_BLOCK_ENFORCEMENT_ENABLED(TRUE, TRUE);

-- Move ALICE from the standard tier to the power-user tier.
ALTER USER alice SET TAG cost_mgmt_db.tags.usage_tier = 'power';
```

## Pattern 3: Role within a specific cost center

When the same role (`DATA_ENG`) is shared across departments that have different budgets, combine
the role and a department or cost-center tag using `INTERSECTION`:

Copy code

```
USE SCHEMA cost_mgmt_db.quota_schema;

-- Data engineers in Finance: 300 credits/month.
CREATE SNOWFLAKE.CORE.QUOTA finance_data_eng_quota();
CALL finance_data_eng_quota!ADD_SHARED_RESOURCE('AI FUNCTION');
CALL finance_data_eng_quota!ADD_SHARED_RESOURCE('SNOWFLAKE COCO');
CALL finance_data_eng_quota!SET_QUOTA_USER_SCOPE(OBJECT_CONSTRUCT(
  'applies_to', OBJECT_CONSTRUCT(
    'type', 'GROUP_OF_USERS',
    'operator', 'INTERSECTION',
    'user_tags', [[(SELECT SYSTEM$REFERENCE('TAG', 'cost_mgmt_db.tags.cost_center', 'SESSION', 'APPLYBUDGET')), 'finance']],
    'roles', ['DATA_ENG'])));
CALL finance_data_eng_quota!SET_PER_USER_LIMIT(300);
CALL finance_data_eng_quota!SET_BLOCK_ENFORCEMENT_ENABLED(TRUE, TRUE);

-- Data engineers in Product: 1,000 credits/month.
CREATE SNOWFLAKE.CORE.QUOTA product_data_eng_quota();
CALL product_data_eng_quota!ADD_SHARED_RESOURCE('AI FUNCTION');
CALL product_data_eng_quota!ADD_SHARED_RESOURCE('SNOWFLAKE COCO');
CALL product_data_eng_quota!SET_QUOTA_USER_SCOPE(OBJECT_CONSTRUCT(
  'applies_to', OBJECT_CONSTRUCT(
    'type', 'GROUP_OF_USERS',
    'operator', 'INTERSECTION',
    'user_tags', [[(SELECT SYSTEM$REFERENCE('TAG', 'cost_mgmt_db.tags.cost_center', 'SESSION', 'APPLYBUDGET')), 'product']],
    'roles', ['DATA_ENG'])));
CALL product_data_eng_quota!SET_PER_USER_LIMIT(1000);
CALL product_data_eng_quota!SET_BLOCK_ENFORCEMENT_ENABLED(TRUE, TRUE);
```

## Pattern 4: Temporary or individual exceptions with limit overrides

When one or a few users in a quota need extra headroom for a sprint or investigation, don’t create a
separate single-user quota or change their roles or tags. Instead, set a per-user limit override on
their existing quota with an expiration date:

Copy code

```
-- Give ALICE 1,500 credits/month on analyst_ai_quota until December 1, 2026.
-- At 00:00 UTC on December 1, ALICE automatically reverts to the 200-credit quota default.
CALL analyst_ai_quota!SET_USER_QUOTA_OVERRIDE(
  ['ALICE'],
  'MONTHLY',
  1500,
  '2026-12-01'
);

-- Inspect active overrides on the quota.
CALL analyst_ai_quota!LIST_USER_QUOTA_OVERRIDES();
```

If the user is also covered by an account-wide guardrail quota (such as `account_ai_guardrail` with
a 500-credit monthly limit), raise their override on that quota as well so the lower guardrail limit
doesn’t still block them:

Copy code

```
CALL account_ai_guardrail!SET_USER_QUOTA_OVERRIDE(
  ['ALICE'],
  'MONTHLY',
  1500,
  '2026-12-01'
);
```

For more information about overrides, see
[Override limits for specific users](/user-guide/budgets/per-user-quotas-overrides).

## Related content

- [Per-user quotas](/user-guide/budgets/per-user-quotas)
- [Create and configure a per-user quota](/user-guide/budgets/per-user-quotas-create)
- [Specify users in scope for a per-user quota](/user-guide/budgets/per-user-quotas-user-scope)
- [Override limits for specific users in a per-user quota](/user-guide/budgets/per-user-quotas-overrides)
- [Block users at a per-user quota limit](/user-guide/budgets/per-user-quotas-enforcement)
