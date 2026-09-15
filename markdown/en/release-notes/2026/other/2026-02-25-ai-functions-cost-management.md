# Mar 2, 2026: Monitor and control Cortex AI Functions spending (*General availability*)

The CORTEX\_AI\_FUNCTIONS\_USAGE\_HISTORY account usage view provides detailed telemetry for Cortex AI Functions, helping you to monitor usage patterns and implement automated cost controls across your organization. You can track credit consumption by function, model, user, role, warehouse, and query, forming the foundation for proactive AI cost governance.

Using the new view, you can:

- **Detect total monthly spending:** Aggregate credits at the account level to monitor overall AI Functions consumption and trigger alerts when predefined thresholds are exceeded.
- **Enforce monthly per-user spending limits:** Track usage by individual users and automatically revoke or restore AI function access based on configurable monthly credit limits.
- **Detect and cancel runaway queries:** Identify long-running or high-credit AI function queries and automatically cancel them before additional credits are consumed. This capability can be used as a drop-in replacement for previous query credit limit patterns.

The release is accompanied by a comprehensive user guide topic that includes production-ready SQL examples for:

- Daily and monthly credit consumption analysis
- Account-level monthly spending alerts
- Role-based access control with automated budget enforcement
- Automated monitoring and cancellation of excessive queries

For more information, see:

- [CORTEX\_AI\_FUNCTIONS\_USAGE\_HISTORY view reference](/sql-reference/account-usage/cortex_ai_functions_usage_history)
- [Managing AI Functions Cost with Account Usage](/user-guide/snowflake-cortex/ai-func-cost-management)
