# About organizational listings

Organizational listings in Snowflake allow you to share data products securely within your organization, making it easier for internal consumers to discover and use trusted resources in the Internal Marketplace. Providers can create and manage listings with the Snowflake API or Provider Studio in Snowsight.

## The Internal Marketplace

The Internal Marketplace in Snowflake is a curated, secure space for collaborative data sharing within
your organization. It centralizes internally-available data products, allowing teams to discover,
trust, and apply resources without needing to navigate external marketplaces. By offering an organized
way to discover data products, the Internal Marketplace supports collaboration and data-driven
decision-making across your company.

The Internal Marketplace is similar to the public Snowflake Marketplace, but it is exclusively for your organization.
It allows you to easily discover and use vetted data shared within your internal teams. Access can be managed
by account targeting and Role-Based Access Control (RBAC), ensuring that data remains secure and accessible
only to authorized users.

## Organizational listing providers

For those creating and sharing data products, the Internal Marketplace provides a secure platform to publish data products
internally. Providers can create and manage organizational listings using Provider Studio in Snowsight or
via the API. Publishing data products in the Internal Marketplace ensures teams access consistent datasets, reducing
redundancy and supporting unified, data-driven initiatives.

Centralizing data offerings in the Internal Marketplace helps you manage access to sensitive information, maintaining data security
and integrity while enabling the organization to innovate with trusted data.

Providers can create and manage organizational listings by using Provider Studio or the API.

## Organizational listing consumers

For team members and data consumers, organizational listings provide a way to discover and access internal-only data resources. The
Internal Marketplace lets users locate data products without having to browse through externally-shared listings
in Snowflake Marketplace. Each organizational listing can be curated to meet your organizational
standards, so consumers can use these data products confidently for their analytics and projects.

## Internal Marketplace listings in government regions

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Providers in government regions can configure organizational listings in the Internal Marketplace and share those listings with consumers in commercial or Virtual Private Snowflake (VPS) accounts. Providers can also configure [Cross-Cloud Auto-Fulfillment](/collaboration/provider-listings-auto-fulfillment) on these listings. When configured, auto-fulfillment will be triggered after the consumer accesses the listing.

Consumers in government regions can programmatically access listings created by providers in commercial or VPS accounts using the Uniform Listing Locator (ULL) or by mounting the shared database.

### Limitations when working with Internal Marketplace listings in government regions

- Consumers can’t search the Internal Marketplace in Snowsight for listings in government regions.

  - To access a listing in Snowsight, select the listing URL received from the provider.
  - To access and test a listing programmatically, run the following code:

    Copy code

    ```
    SHOW AVAILABLE LISTINGS;
    SELECT * FROM <ull>.<schema>.<view>
    ```
- To trigger auto-fulfillment on a listing, consumers must get the listing through Snowsight. This functionality isn’t supported using SQL.
- Custom organization profiles aren’t supported.
- The [ACCESS\_HISTORY](/sql-reference/organization-usage/access_history) view for these listings in the organization account isn’t visible to consumers.
