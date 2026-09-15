# Jul 15, 2026: Consumer-controlled maintenance policies — General Availability

Consumer-controlled maintenance policies for Snowflake Native Apps are now generally available.

Consumers can define when Snowflake Native App upgrades happen in their accounts by creating a maintenance policy and applying
it to an account or an individual app. For more information, see
[Consumer-controlled maintenance policies](/developer-guide/native-apps/consumer-maintenance-policies).

Providers can configure release directives to respect consumer maintenance policies by setting the
UPGRADE\_IN\_MAINTENANCE\_WINDOW parameter, and can align Snowpark Container Services compute pool node maintenance with the consumer’s
maintenance window by setting the AUTOMATIC\_APPLICATION\_MAINTENANCE property on the application package. For more
information, see [Consumer-controlled maintenance policies: Provider guide](/developer-guide/native-apps/consumer-maintenance-policies-provider).
