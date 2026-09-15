# Feb 20, 2026: Snowflake Native Apps: Configuration (*Preview*)

Snowflake Native Apps can now request configuration values from consumers using application configurations.

This capability allows an app to define configuration keys that request specific information from the consumer, such as the name of a server app for inter-app communication, or an arbitrary string value like an external URL or account identifier. Configurations can be marked as sensitive to protect values such as API keys or access tokens from exposure in query history and command output.

For more information, see [Application configuration](/developer-guide/native-apps/app-configuration).
