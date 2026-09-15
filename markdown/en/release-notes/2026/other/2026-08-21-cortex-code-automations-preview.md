# Aug 21, 2026: CoCo automations in CLI and Snowsight (*Preview*)

CoCo automations in the CoCo CLI and CoCo in Snowsight are now available in public preview.
Automations let you schedule recurring, unattended CoCo runs that execute in a Snowflake-managed
sandbox. Each run creates a Cortex thread that you can inspect and continue in CoCo. Automations
created from one surface can be monitored and managed from the other.

The feature is available in all commercial regions on AWS, Azure, and Google Cloud. It is not
available in government, FedRAMP, DoD, VPS, or China deployments.

During public preview, user-created automations incur standard Snowflake task billing in addition to
CoCo token consumption for each run. System-initiated analysis does not incur charges.

The `EXECUTE AGENT TASK` account privilege controls access to automations and is granted to the
`PUBLIC` role by default. Administrators can revoke the privilege from `PUBLIC` and grant it only to
selected roles.

For more information, see:

- [CoCo automations in CLI and Snowsight](/user-guide/cortex-code/cortex-code-automations)
- [Snowflake CoWork Automations: `EXECUTE AGENT TASK` privilege granted to `PUBLIC` by default](/release-notes/bcr-bundles/un-bundled/bcr-2349)
