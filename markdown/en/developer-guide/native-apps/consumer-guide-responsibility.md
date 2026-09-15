# Separation of responsibilities for Native Apps

Feature — Generally Available

The Snowflake Native App Framework is generally available on supported cloud platforms. For additional information, see
[Support for private connectivity, VPS, and government regions](/developer-guide/native-apps/limitations#label-native-apps-supported-clouds).

Caution

This section uses language that has been reviewed and approved by Snowflake legal and security
teams. Any changes require sign-off from both teams before publication.

Traditional connected apps take data out of a data warehouse and process it elsewhere before
returning results. They need access to a customer account to take data out or to perform privileged
operations in an account. Native Apps bring application logic to where the data resides in a
consumer’s Snowflake account so that the data does not need to be transferred for processing. This
is the primary benefit of Native Apps and most Native Apps are built to process data in the consumer
account while taking advantage of all Snowflake AI Data Cloud functionality under Snowflake
governance.

The Snowflake Native App Framework intentionally restricts what a Snowflake Native App can see and do by default. It does not
provide any access to consumer data by default while also protecting the provider’s intellectual
property (IP) by default. Both defaults can be selectively and carefully relaxed by the respective
owners of the data and other objects such as stored procedures and functions. A consumer can enable
the app to access just the data or other objects that it needs for performing its intended purpose
and the app can expose the data or objects to its users in the consumer account that the provider
selects. Such relaxation happens through explicit actions and under Snowflake Role-Based Access
Controls (RBAC). For example, a knowledge graph application may need to access some tables and views
in the consumer’s databases to build the knowledge graph, while key insights stored in an
application database may be appropriate for users to access. Both these accesses can happen only
through explicit grants from the consumer account admin and the application (as configured by the
provider), respectively.

The defaults are intended to minimize but cannot eliminate risks to consumer’s data and the
operational use of the Snowflake account. An app may request additional privileges from the consumer
account admin or their delegates throughout its lifecycle. Such privileges may provide additional
powers to the app and potentially expose the consumer to risks including but not limited to
exfiltration of data, breach of privacy, or violation of regulatory requirements. For example, a
connector app may need to send data to a service outside the Snowflake account for a legitimate
purpose, but consumer data that it has access to must be carefully reviewed for business
justification and the target of its external access (such as an ERP system) must be scrutinized by
a consumer account administrator or their delegate before approval.

Snowflake also performs security scans on application packages submitted for external sharing. They
are intended to help the provider find common vulnerabilities and violations of guidelines. They are
not a replacement for provider’s and consumer’s responsibilities to review the app they publish and
install respectively. Please note that:

- Provider is the seller of record; not Snowflake.
- Consumer is responsible for security, privacy, compliance and all other necessary reviews of the
  provider’s app. Any security scanning or other vetting done by Snowflake is not a substitute for
  a consumer’s due diligence.
- Any additional privileges requested by the application beyond what the Snowflake Native App Framework grants must be
  scrutinized by the consumer before grants are made. The impact of such additional privileges is
  for the consumer to determine before granting them.
