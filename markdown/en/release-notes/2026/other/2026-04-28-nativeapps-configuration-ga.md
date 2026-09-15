# Apr 28, 2026: Snowflake Native Apps: Configuration (*General availability*)

With this release, app configuration is now generally available for Snowflake Native Apps. Providers can
define configurations that request values from consumers at installation or runtime, covering
application names for inter-app communication, free-form strings, and secret-based authorization.
Consumers provide values through Snowsight, the Python Permission SDK, or SQL.

This release also adds better support for OAuth authorization from app consumers. Using the new
`SECRET_AUTHORIZATION` configuration type, a Snowflake Native App can request OAuth authorization from
the consumer, who completes a standard OAuth consent flow. The app then uses the resulting tokens
to call external services without the provider handling any credentials.

For more information, see the following topics:

- [Application configuration](/developer-guide/native-apps/app-configuration)
- [Request OAuth authorization from consumers](/developer-guide/native-apps/app-configuration-secret-authorization)
