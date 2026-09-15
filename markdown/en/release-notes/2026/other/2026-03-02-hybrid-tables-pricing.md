# Mar 02, 2026: Simplified pricing for hybrid tables

Snowflake has simplified the pricing model for hybrid tables.
Previously, hybrid tables were billed based on three categories:
hybrid table storage, virtual warehouse compute, and hybrid table
requests (serverless credits for read and write operations on the
underlying row storage).

As of March 1, 2026, hybrid table requests
are no longer charged as a separate billing category.

Hybrid tables are now billed based on two categories:

- **Hybrid table storage**: A flat monthly rate per GB for data
  stored in hybrid tables.
- **Virtual warehouse compute**: Standard warehouse consumption
  for queries executed against hybrid tables.

For more information, see
[Evaluate cost for hybrid tables](/user-guide/tables-hybrid-cost).
