# About Snowflake and SAP® Zero-Copy Integration

Feature — Generally Available

This integration is generally available to accounts in all AWS, Azure, and GCP commercial regions. It is not available in VPS deployments, government regions, or the People’s Republic of China.

For details, see [Supported regions](#supported-regions).

Snowflake and SAP® have partnered to offer customers a seamless zero-copy integration between the two platforms. The integration leverages SAP® Business Data Cloud that enables customers to harmonize SAP® and non-SAP® data at scale in Snowflake, while optimizing total cost of ownership across workloads.

Leveraging zero copy data access, data and AI teams can work with semantically rich SAP® Data Products in real time without added cost and complexity of ETL pipelines, and allows them to build AI and machine learning applications fueled by trusted SAP Data Products and grounded in the context of all their mission-critical data, ensuring accurate, reliable, and trustworthy AI outcomes.

## Two Ways to Integrate Snowflake and SAP®

The integration delivers two distinct offerings, providing customers choice.
Both leverage SAP® Business Data Cloud to enable zero-copy data sharing between SAP® Business Data Cloud and Snowflake.

### SAP® Snowflake

Designed for new Snowflake customers, SAP® Snowflake makes Snowflake available in SAP® Business Data Cloud as a certified SAP® Solution Extension. From advanced analytics and ML to data engineering, applications, and marketplace it puts the Snowflake platform directly in the hands of SAP® users. For more information, see [SAP Snowflake](https://help.sap.com/docs/business-data-cloud/sap-snowflake/introducing-sap-snowflake) in the SAP® documentation.

![SAP® Snowflake architecture](/static/images/openflow/sap-snowflake.png)

#### SAP® Business Data Cloud Connect for Snowflake

Designed for existing Snowflake customers, SAP® Business Data Cloud (BDC) Connect for Snowflake
enables customers to share Data Products from SAP® BDC with their existing Snowflake accounts.
This gives Snowflake users real-time access to semantically rich SAP® Data Products without duplication of data.

![SAP® BDC Connect for Snowflake architecture](/static/images/openflow/sap-bdc.png)

For more information and set up instructions for either of these offerings, see [Setup tasks for SAP® Snowflake and SAP® BDC Connect for Snowflake](/user-guide/data-integration/zero-copy/sap-sql/setup-tasks).

## Supported regions

On the Snowflake side, the integration is available to accounts in all AWS, Azure, and GCP commercial regions. For the full list, see [Supported cloud regions](/user-guide/intro-regions).

The integration is not available in the following Snowflake deployments:

- [Virtual Private Snowflake (VPS)](/user-guide/intro-editions)
- [Government regions](/user-guide/intro-regions#label-us-gov-regions)
- The People’s Republic of China

On the SAP® side, SAP® Business Data Cloud and your Snowflake account don’t have to be on the same cloud or in the same region. The integration supports cross-cloud and cross-region connections, and the connection is bidirectional: you can consume SAP® data products in Snowflake and publish Snowflake data back to SAP® BDC.
