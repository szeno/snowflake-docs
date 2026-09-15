# Cortex AI Guardrails

[Enterprise Edition Feature](/user-guide/intro-editions)

This feature requires Enterprise Edition (or higher). To inquire about upgrading,
please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

## Overview

Cortex AI Guardrails, part of the [Snowflake Horizon Catalog](/user-guide/snowflake-horizon), provide
run-time protection against prompt injection and jailbreak attacks on [CoCo](/user-guide/cortex-code/cortex-code), [Snowflake CoWork](/user-guide/snowflake-cortex/snowflake-cowork), and [Cortex Agents](/user-guide/snowflake-cortex/cortex-agents).

As enterprises move AI applications from pilot to production, they face increased risk from adversarial prompts
that can threaten data integrity and security. Cortex AI Guardrails extend Snowflake’s default protections
against known prompt injection techniques by adding guardrails to detect and mitigate adversarial threats.

Integrated centrally into Snowflake Horizon Catalog, Cortex AI Guardrails leverage contextual reasoning to
detect and neutralize malicious intent, preventing adversarial threats from circumventing established security
boundaries and hardened permissions.

### Key capabilities

Cortex AI Guardrails provide the following protections:

- **Prompt injection detection**: Scans each tool’s outputs to detect and flag indirect
  prompt injections that attempt to override system instructions. Combined with the base model’s
  built-in protections against known prompt injection and jailbreak techniques, this provides layered
  coverage to block direct and indirect attack paths.
- **Jailbreak prevention**: Detects attempts to bypass the model’s safety protocols and security boundaries.
- **Zero-day style protection**: Uses advanced techniques to identify sophisticated, previously unknown
  attack patterns in real time.

## Configure Cortex AI Guardrails

You can configure Cortex AI Guardrails at the account level using the `AI_SETTINGS` parameter. This
provides centralized control over guardrail behavior for CoCo, Snowflake CoWork, and Cortex Agents in
your account. Users with the ACCOUNTADMIN role can configure Cortex AI Guardrails.

Note

Cortex AI Guardrails are available to Commercial (non-Gov, VPS, Sovereign) accounts that have [Cross-region inference](/user-guide/snowflake-cortex/cross-region-inference) enabled.
The account parameter `CORTEX_ENABLED_CROSS_REGION` must be set to `ANY_REGION`, `AWS_US`, `AWS_EU`, `AWS_JP`, `AWS_APJ`, or `AWS_GLOBAL`.
For details on this parameter, see [CORTEX\_ENABLED\_CROSS\_REGION](/sql-reference/parameters#label-cortex-enable-cross-region).

### Enable guardrails

To enable Cortex AI Guardrails for your account, use the ALTER ACCOUNT command with the `AI_SETTINGS`
parameter:

Copy code

```
ALTER ACCOUNT SET AI_SETTINGS = $$
  guardrails:
    advanced_prompt_injection:
      - enabled: true
$$;
```

### View guardrail settings

To view the current guardrail configuration for your account:

Copy code

```
SHOW PARAMETERS LIKE 'AI_SETTINGS' IN ACCOUNT;
```

### Disable guardrails

To disable Cortex AI Guardrails:

Copy code

```
ALTER ACCOUNT UNSET AI_SETTINGS;
```

## Monitor guardrail activity

The [CORTEX\_AI\_GUARDRAILS\_USAGE\_HISTORY](/sql-reference/account-usage/cortex_ai_guardrails_usage_history) view in the ACCOUNT\_USAGE schema provides a historical record of all guardrail scan activity for your account, including credit and token consumption.

Use this view to:

- Review which requests were flagged for possible prompt injection (`GUARDRAILS_SIGNAL = TRUE`)
- Monitor credit and token consumption for guardrail scans
- Audit guardrail activity by user, agentic source, or role

For example, to retrieve all requests where a guardrail scan was flagged:

Copy code

```
SELECT *
  FROM SNOWFLAKE.ACCOUNT_USAGE.CORTEX_AI_GUARDRAILS_USAGE_HISTORY
  WHERE GUARDRAILS_SIGNAL = TRUE
    AND USAGE_TIME >= DATEADD('hour', -72, CURRENT_TIMESTAMP())
  LIMIT 100;
```

Guardrail activity is also captured in the conversation and trace logs for each client:

- **CoCo**: Review detected threats in the conversation logs. For where those logs are stored and how to manage them, see [Conversation history](/user-guide/cortex-code/security#label-cortex-code-security-conversation-history).
- **Snowflake CoWork** and **Cortex Agents**: Review conversation and trace data in Cortex Agent monitoring (for example in Snowsight, **AI & ML** » **Agents**, then the **Observability** pane for the agent). For details, see [Monitor Cortex Agent requests](/user-guide/snowflake-cortex/cortex-agents-monitor#label-cortex-agents-access-conversation-logs).

## Considerations

- While Cortex AI Guardrails are optimized for high accuracy, some legitimate prompts may occasionally be
  flagged. Review your guardrail logs periodically to identify any patterns.
- Cortex AI Guardrails for prompt injection are currently available with [CoCo](/user-guide/cortex-code/cortex-code), [Snowflake CoWork](/user-guide/snowflake-cortex/snowflake-cowork), and [Cortex Agents](/user-guide/snowflake-cortex/cortex-agents).

## Cost

You are charged credits for the use of Cortex AI Guardrails as listed in the
[Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf). Usage is measured based on the number of tokens scanned.

## Related topics

- [AI Observability in Snowflake Cortex](/user-guide/snowflake-cortex/ai-observability)
- [Snowflake Horizon Catalog](/user-guide/snowflake-horizon)
- [Overview of Snowflake CoCo](/user-guide/cortex-code/cortex-code)
- [Overview of Snowflake CoWork](/user-guide/snowflake-cortex/snowflake-cowork)
- [Cortex Agents](/user-guide/snowflake-cortex/cortex-agents)
- [Snowflake AI and ML](/guides-overview-ai-features)
