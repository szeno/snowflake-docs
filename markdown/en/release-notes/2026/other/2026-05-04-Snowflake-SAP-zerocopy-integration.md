# May 4, 2026: SAP® BDC Zerocopy Connector (*General availability*)

The SAP® BDC Zerocopy Connector is now generally available, enabling zero-copy
data sharing between SAP® Business Data Cloud and Snowflake without moving or
duplicating data.

Two integration paths are supported:

- **SAP® Snowflake**: For SAP customers without an existing Snowflake account,
  provision a new Snowflake account directly from SAP for Me. A Zerocopy
  Connector is automatically created and enrolled with SAP® BDC as part of
  provisioning.
- **SAP® BDC Connect for Snowflake**: For customers with an existing Snowflake
  account, connect it to SAP® Business Data Cloud using an invitation link
  from SAP for Me.

Once connected, you can:

- Browse and mount SAP® data products as catalog-linked databases in Snowflake.
- Query SAP® data directly in Snowflake, including joins across multiple data
  products.
- Use Semantic Views generated from SAP® Core Schema Notation (CSN) to power
  AI capabilities such as Cortex Analyst on top of SAP® data.
- Publish Snowflake data back to SAP® BDC.
- Use the Cortex Code skill to manage the end-to-end lifecycle of the SAP® and
  Snowflake Zero-Copy integration through a conversational, step-by-step
  workflow — creating connectors, consuming SAP® BDC data products, publishing
  Snowflake data back to SAP® BDC, analyzing shared data, and troubleshooting
  issues.

For more information, see [About Snowflake and SAP® Zero-Copy Integration](/user-guide/data-integration/zero-copy/about-sap-snowflake).
