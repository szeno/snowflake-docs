# October 14, 2024 — Snowflake Data Clean Rooms release notes

With this release, we are pleased to announce the availability of the following new features and enhancements in this update to Snowflake
Data Clean Rooms.

## Clean room overlap stats

Clean room statistics now include overlap statistics. These statistics describe how many distinct identifiers within join columns belong to
a certain group based on the attribute columns enabled by the template.

For more information, see [Run an analysis in the UI](/user-guide/cleanrooms/v1/web-app-working).

## Provider-initiated activation for third-party connectors

Providers can now activate audiences to third-party activation endpoints (including Google Ads, Meta, Ads, LiveRamp, The Trade Desk, and
Yahoo). Note that consumers still need to enable this option for providers while installing the clean room.

For more information, see [Working with Clean Rooms](/user-guide/cleanrooms/v1/activation#label-clean-rooms-push-provider-run-analysis).

## Security scans for custom templates

Providers can view the results of security scans that run automatically to help identify vulnerabilities in custom templates created using
the developer APIs. This helps identify parts of the custom template that might be susceptible to SQL injection attacks.

For more information, see [Security scans for custom templates](/user-guide/cleanrooms/scan-custom-template).
