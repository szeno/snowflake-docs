# Implementing differential privacy

[Enterprise Edition Feature](/user-guide/intro-editions)

This feature requires Enterprise Edition (or higher). To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

This topic contains information for the data provider who is implementing differential privacy for their account.

As you implement differential privacy for your dataset, your tasks involve three key concepts:

- [Privacy policies](/user-guide/diff-privacy/differential-privacy-admin-privacy-policies). A table or view is not protected by
  differential privacy until you assign a privacy policy to it. A table or view with a privacy policy is considered to be
  *privacy-protected*.
- [Privacy budgets](/user-guide/diff-privacy/differential-privacy-overview#label-diff-privacy-loss-budgets). As analysts query a privacy-protected table, you can
  [manage the privacy budgets](/user-guide/diff-privacy/differential-privacy-admin-privacy-budgets) associated with those analysts.
- [Privacy domains](/user-guide/diff-privacy/differential-privacy-privacy-domains). You should define a privacy domain for fact and
  dimension columns in a privacy-protected table or view.

**Limitations**

- You cannot assign a privacy policy and an aggregation policy or masking policy to the same table or view.
- Apart from querying the [noise interval](/user-guide/diff-privacy/differential-privacy-analyst#label-diff-privacy-understand-results), analysts don’t know whether they’re querying a
  privacy-protected table, so the data provider should inform them that query results contain noise.
- A data provider cannot monitor the privacy loss incurred by analysts running queries in another account.
- Applying multiple privacy policies to one table is currently not supported. Because of this, protecting more than one entity with
  entity-level differential privacy in a single table is not possible.
- Queries on replicated or cloned tables that have a privacy policy associated with an entity key
  are currently blocked.

## About entity-level privacy

An *entity* refers to a class of data subject that should be protected, for example people, organizations, or locations. If each individual
entity appeared in only one row, row-level privacy would be enough to protect their identities. However, if data belonging to an individual
entity appears in multiple rows (for example, in transactional data), differential privacy must be configured for entity-level privacy to
correctly protect each entity.

To achieve entity-level privacy, Snowflake lets you specify which attribute can be used to identify an entity (an *entity key*). This
lets Snowflake identify all of the records that belong to a particular entity within a dataset. For example, if the entity key is defined
as the column `email`, then Snowflake can determine that all records where `email=joe.smith@example.com` belong to the same entity.

In most cases, entity-level privacy is preferred over row-level privacy, but row-level privacy might be a good fit for a table if the
following is true:

- No column in the table uniquely identifies entities. Entity-level privacy requires an identifying column.
- Each individual entity only appears once.
- The table will not be used in a join. Joins with tables protected by row-level privacy are possible, but have
  [limitations](/user-guide/diff-privacy/differential-privacy-analyst#label-diff-privacy-joins-no-duplicates).

You choose whether to implement entity-level or row-level privacy when assigning a privacy policy to a table or view. For more information,
see [Assign a privacy policy](/user-guide/diff-privacy/differential-privacy-admin-privacy-policies#label-diff-privacy-admin-assign). If you choose to implement entity-level privacy, the data must also meet
[structural requirements](#label-diff-privacy-admin-entity-reqs) to ensure that the entity identifier is used correctly.

Tip

If you want to protect two separate tables with the same privacy policy, but they do not have the same entity key values, you can create
a new table that maps the two identifying columns, create a view that joins two of the tables, and apply the privacy policy to the view.
For example, you could use this strategy if the entity key in one table is `email` and in another table it is `user_id`, but
both refer to the same entities.

### Structural requirements for entity-level privacy

The structure of data protected by entity-level differential privacy must conform to certain requirements. These requirements must be met so
that Snowflake can accurately track the privacy loss associated with entities.

You should structure your data to meet these requirements *before* applying privacy policies to implement differential privacy. Snowflake
cannot determine whether data conforms to these structural requirements because they concern the meaning of the data, not the differential
privacy implementation. For example, if the entity keys for two different tables are both set to the column `user_id`, but one of the
columns contains values for a numeric identifier while the other column contains email addresses, Snowflake cannot correctly link entity information
across the two tables.

To achieve entity-level privacy, your data must conform to the following requirements:

- **Each row belongs to only one individual within an entity** — As an example, suppose a table contains users and households. If the
  entity that needs to be protected is users, the table cannot be structured such that each row is a household and all the users in that
  household are captured in other columns. You would need to restructure the table so there is only one row per user, with a `household_id`
  column to indicate which household a user belongs to.
- **Consistent entity identifier across all tables** — You can create a privacy policy that represents the protection needed for a single
  entity, then apply that policy to multiple tables that contain information about the entity. When you assign the privacy policy to each
  table, you need to specify the column that uniquely identifies the entity (that is, the entity key). The value that uniquely identifies an
  entity within these entity key columns must be the same. For example, suppose the `email` column is the entity key for two tables that
  contain information about an entity. If the email address of an entity is `joe@example.com` in one table, then the email address in the
  other table must also be `joe@example.com`.
- **Entity identifier in all tables**: Although an entity identifier is not required to implement entity-level privacy, you can make it possible for analysts to
  minimize noise in query joins by including the entity identifier in all tables related to an entity. In some cases, you might need to
  denormalize the entity key column to meet this requirement. For example, suppose you had the following tables where the entity is
  customers:

  | Table | Description |
  | --- | --- |
  | `customer` | Customer directory, where each row is a customer and has a `customer_id`. |
  | `transactions` | Customer transactions, where each row is a transaction and has a `transaction_id`. Each customer can have multiple transactions. |
  | `transaction_lines` | Unique items that were purchased in a transaction. There can be multiple rows in a single transaction. |

  Expand

  Show lessSee more

  Under best practices for normalization, the `transaction_lines` table would have the `transaction_id` but not the `customer_id`.
  The `transaction_lines` table would link to the `transactions` table, which could then be linked to the `customers` table with
  `customer_id`.

  However for differential privacy, you probably want to optimize the data for the analyst by adding the `customer_id` identifier to the
  `transaction_lines` table. This allows the analyst to minimize noise by including `customer_id` in the join key when joining the
  `transaction_lines` table with another table.

## Interactions with Snowflake features

This section discusses how the following differential privacy objects interact with other Snowflake features. It discusses the effect on
privacy policies, privacy budgets, and privacy domains.

### Data sharing

Secure views and tables with a privacy policy are protected by differential privacy when added to a share. Unsecured views are not
protected by privacy policies if they are queried via a share.

### Replication

For considerations when replicating privacy policies and privacy-protected tables and views, see
[Privacy policies](/user-guide/account-replication-considerations#label-account-replication-considerations-privacy-policy).

Note

There is a current limitation when querying replicated tables that have a privacy policy associated with an entity key. Queries on those tables are blocked until the limitation is removed.

### Cross-cloud auto-fulfillment

Keep the following in mind when using cross-cloud auto-fulfillment to replicate a data product:

- Administrators in the account to which the data product was replicated cannot adjust the privacy budget.
- Administrators cannot use a single account to view the privacy loss incurred in all regions.

### Cloning

For the effects of cloning privacy-protected tables and views, see [Cloning and differential privacy](/user-guide/object-clone#label-cloning-consideration-diff-privacy).

Note

There is a current limitation when querying cloned tables that have a privacy policy associated with an entity key. Queries on those tables are blocked until the limitation is removed.

### Views built on a privacy-protected base object

You can build a view on a privacy-protected table or view. However, the privacy domains of the base table or view are not inherited. As a
result, note the following:

- Privacy domains must be set on the columns of the new view.
- Adjusting the privacy domain of the base table does not affect the privacy domains of the view that is built on it.

### Materialized views

You can assign a privacy policy to a materialized view to make it privacy-protected.

Other interactions between privacy policies and materialized views include the following:

- You cannot create a materialized view based on a privacy-protected table or view.
- You cannot assign a privacy policy to a table if it is referenced as the base table of a materialized view.

### UDFs

Analysts cannot use a user-defined function to query a privacy-protected table.

### Streams

You cannot query a stream that is based on a privacy-protected table.

You cannot assign a privacy policy to a stream.

### Other policies

Privacy policies interact with other Snowflake policies in the following ways:

Masking policies
:   You cannot assign a privacy policy and a masking policy to the same table or view.

Row access policies
:   Row access policies take precedence over a privacy policy. If a row is blocked by the row access policy, it is not included in the results
    of the differentially private query.

Projection policies
:   Protecting a table with a privacy policy and any of its columns with a projection policy at the same time is currently not supported.
    While you’re able to assign the policies in this way, queries against the table will fail.

Aggregation policies
:   You cannot assign a privacy policy and an aggregation policy to the same table or view.

### Dynamic tables

You cannot create a dynamic table when the referenced source table is privacy-protected.

You can assign a privacy policy to a table that is referenced by an existing dynamic table; however, once the policy is assigned, the
dynamic table will no longer refresh.

### External tables

You can assign a privacy policy to an external table. If an analyst tries to aggregate on a VARIANT column, the query fails. However, if an
analyst tries to aggregate on a virtual column, it succeeds.

### Time travel

For time travel, when a previous version of a table is copied as a new table, the current version of a privacy domain is used for the table
because Snowflake does not store previous versions of the privacy domain in table metadata.
