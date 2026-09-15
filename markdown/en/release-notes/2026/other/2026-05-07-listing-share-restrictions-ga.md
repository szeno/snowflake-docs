# May 7, 2026: Listing share restrictions (*General availability*)

Listing share restrictions are now generally available. Providers can enable share restrictions on
private external listings to prevent consumers in lower editions or non-HIPAA accounts from accessing
their data.

Share restrictions can be enabled at two levels:

- **Account level**: Enforces restrictions on all private external listings owned by the provider account.
  Enable using Provider Studio settings or `ALTER ACCOUNT SET ENABLE_LISTING_SHARE_RESTRICTIONS = TRUE`.
- **Listing level**: Enables restrictions for a specific listing using the listing details settings in
  Snowsight or the `share_restrictions` field in the listing manifest.

For more information, see [Listing share restrictions](/collaboration/listing-share-restrictions).
