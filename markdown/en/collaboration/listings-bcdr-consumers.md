# Consumer fulfillment behavior

Traditionally, Snowflake uses two primary fulfillment patterns:

- **Same-region access**: Consumers in the same region as the provider access data directly from the provider’s account without additional replication.
- **Cross-region access**: Providers use [auto-fulfillment](/collaboration/provider-listings-auto-fulfillment) to replicate data and metadata to a Secure Share Area (SSA) in the consumer’s region.

## The impact of failover groups for listings

With the introduction of failover groups for listings, Snowflake ensures that metadata and relationships remain intact in a
secondary data recovery (DR) account. This capability provides a specialized access pattern designed to prevent downtime for your consumers,
regardless of the region that is currently the primary.

## Consumer access patterns

After providers configure [Business Continuity and Disaster Recovery (BCDR)](/collaboration/listings-bcdr) for listings, the fulfillment path depends on the consumer’s location relative to the listing’s original primary region.

### The original primary region

In the region where the listing was originally created, sometimes called the *Home* region, consumers access data directly from the original provider account.

- **Failover status**: Regardless of the failover status, even if the listing fails over to a secondary region, consumers in the original region don’t switch to an SSA.
- **Data updates**: These consumers continue to receive fresh data through the failover group, which replicates data back from the new primary to the old primary.

### Secondary and remote regions

For consumers located in any other region — including the region where the DR secondary account resides — fulfillment follows the SSA pattern.

- **Unified mount point**: To ensure a seamless experience, Snowflake maintains a single *mount point* per region. In these regions, that mount point is the SSA.
- **Failover resiliency**: If a failover occurs, the SSA begins sourcing its updates from the new primary account. The consumer’s connection to the SSA remains unchanged, resulting in zero downtime.

## Comparison of fulfillment paths

The following table summarizes how fulfillment works based on the consumer location.

| Consumer location | Fulfillment source | Access method |
| --- | --- | --- |
| Original primary region | Original provider account | Direct share |
| Secondary (DR) region | SSA | Auto-fulfillment |
| All other remote regions | SSA | Auto-fulfillment |

Expand

Show lessSee more
