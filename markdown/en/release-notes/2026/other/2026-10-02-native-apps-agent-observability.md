# Oct 2, 2026: Snowflake Native Apps: Observability for Cortex Agents

Observability for Cortex Agents in a Snowflake Native App now includes the following
capabilities:

- **Intellectual property protection during event logging:** When an app
  initiates a run through the REST `agent:run` API or SQL `DATA_AGENT_RUN`,
  Snowflake redacts orchestrator-authored content before writing the consumer
  event-table record.
- **Event sharing for agent telemetry:** When a consumer enables event sharing,
  the provider receives agent telemetry at the `AI_METADATA` sharing level by
  default or at the `AI_CONTENT` sharing level after the consumer approves the
  `SHARE_AI_OBSERVABILITY_CONTENT` app specification.

For more information, see
[Intellectual property protection during event logging](/developer-guide/native-apps/agents-mcp-servers#label-native-apps-agent-ip-protection)
and
[Event sharing for agent telemetry](/developer-guide/native-apps/agents-mcp-servers#label-native-apps-agent-event-sharing).
