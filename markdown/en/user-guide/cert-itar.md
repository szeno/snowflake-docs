# ITAR

This topic describes how Snowflake supports customers with ITAR compliance requirements.

Note

Snowflake supports the ITAR certification in certain regions within each cloud platform.

For details, refer to [SnowGov Regions](/user-guide/intro-regions#label-us-gov-regions).

## Understanding ITAR compliance requirements

[Business Critical Feature](/user-guide/intro-editions)

Snowflake only offers the Business Critical Edition (or higher) for purchase and use in Snowflake Government Regions supporting customer
ITAR compliance.

The International Traffic in Arms Regulations
([ITAR](https://www.pmddtc.state.gov/ddtc_public?id=ddtc_kb_article_page&sys_id=24d528fddbfc930044f9ff621f961987)) is a United States
compliance standard that controls and restricts access and export of military and defense articles, services, and related technologies.

Companies that manufacture, provide, or distribute goods and services as specified on the United States Munitions List
([USML](https://www.ecfr.gov/cgi-bin/retrieveECFR?gp=&SID=70e390c181ea17f847fa696c47e3140a&mc=true&r=PART&n=pt22.1.121)) may be subject
to ITAR.

Snowflake supports customer ITAR compliance in the Snowflake [SnowGov regions](/user-guide/intro-regions#label-us-gov-regions) by limiting region access to
vetted Snowflake employees and contractors who are eligible to support ITAR workloads. For clarity, customers may not use the Snowflake
Service or the Snowflake Government Regions in connection with U.S. “classified information” (e.g. confidential, secret, or top secret).

For more information about the service offerings that are currently authorized, see [U.S. regions supporting public sector workloads](/user-guide/intro-regions#label-us-gov-regions).

## Export-controlled Data and Cross-region Features

Unlike commercial regions, where multiple regions belong to the same [region group](/user-guide/admin-account-identifier#label-region-groups), each government region
belongs to its own region group to maintain similar security controls, isolation, and compliance across that group. This distinction is
important because, by default, certain features and functionality are limited to the boundaries of a region group.

As an example, [replication](/user-guide/account-replication-intro) is only possible to the boundary of a region group. Because a database cannot be replicated to a region outside
of its region group, this default restriction prevents an organization within a government region from sharing data in a commercial region
without first contacting Snowflake to connect the different region groups. Data sharing is available to customers who
belong within the same government region because it is not crossing the boundary of a region group.

If an organization within a government region needs to replicate a database or share data outside of a government region, it must
contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support) to gain access to
other region groups before it can use these features.

## Considerations When Working with ITAR Workloads

Be aware of entering export-controlled data in any Snowflake [metadata fields](/sql-reference/metadata).

Note

If your Snowflake account is in a [U.S. government region](/user-guide/intro-regions#label-us-gov-regions) and you want to access data products that are
offered privately or on the Snowflake Marketplace, or offer listings either privately or on the Snowflake Marketplace, you must review and
acknowledge a cross-region disclaimer for your [organization](/user-guide/organizations).

For details, see:

- [Prepare to provide listings from accounts in U.S. government regions](https://other-docs.snowflake.com/en/collaboration/provider-becoming#label-listings-setup-gov-provider)
- [Prepare to access listings from accounts in U.S. government regions](https://other-docs.snowflake.com/en/collaboration/consumer-becoming#label-listings-setup-gov-consumer)
- [Limitations for accessing listings from accounts in U.S. government regions](https://other-docs.snowflake.com/en/collaboration/consumer-listings-access#label-listings-gov-consumer-limitations)
