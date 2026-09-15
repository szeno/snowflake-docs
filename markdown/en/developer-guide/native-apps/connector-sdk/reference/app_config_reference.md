# App config SQL reference

Preview Feature — Open

Available to accounts in all regions in all cloud providers (including government regions). For details, contact your Snowflake representative.

File: `configuration/app_config.sql`

## Database objects and procedures

### STATE.APP\_CONFIG

An internal table to store all the connector configurations. This table follows the following structure:

| KEY | VALUE | UPDATED\_AT |
| --- | --- | --- |
| connector\_configuration | {warehouse: “wh”, destination\_db: “db”, destination\_schema: “s”} | TIMESTAMP\_NTZ\_1 |
| custom\_configuration | {journal\_table: “j\_table\_name”} | TIMESTAMP\_NTZ\_2 |
| connection\_configuration | {secret\_name: “secret\_db.schema.the\_secret”} | TIMESTAMP\_NTZ\_3 |
| … | {…} | … |

Expand

Show lessSee more

### PUBLIC.CONNECTOR\_CONFIGURATION

A view that retrieves and maps the data from the `APP_CONFIG` internal table
The mapping is as follows:

1. KEY (col) → CONFIG\_GROUP (col);
2. JSON keys from VALUE column (JSON key) → CONFIG\_KEY (col)
3. JSON values from VALUE column (JSON value) → VALUE (col)
4. UPDATED\_AT (col) → UPDATED\_AT (col)

Example CONNECTOR\_CONFIGURATION view created on example APP\_CONFIG:

| CONFIG\_GROUP | CONFIG\_KEY | VALUE | UPDATED\_AT |
| --- | --- | --- | --- |
| connector\_configuration | warehouse | wh | <timestamp\_ntz> |
| connector\_configuration | destination\_db | db | <timestamp\_ntz> |
| custom\_configuration | journal\_table | j\_table\_name | <timestamp\_ntz> |
| connection\_configuration | secret\_name | secret\_db.schema.the\_secret | <timestamp\_ntz> |
| … | … | … | … |

Expand

Show lessSee more

## Related Java objects

The following Java objects are tightly connected with the `APP_STATE` table:

- `ConnectorConfigurationService`
- `ConfigurationRepository`
- `ConfigurationMap`
- `KeyValueTable`
