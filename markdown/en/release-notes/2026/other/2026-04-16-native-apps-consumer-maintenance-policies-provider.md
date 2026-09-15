# Apr 16, 2026: Consumer-controlled maintenance policies: Provider support (*Preview*)

Provider-side support for consumer-controlled maintenance policies is now in public preview for
Snowflake Native Apps.

Providers can now configure release directives to respect consumer maintenance policies by setting
the UPGRADE\_IN\_MAINTENANCE\_WINDOW parameter. Providers can also align Snowpark Container Services compute pool node
maintenance with the consumer’s maintenance window by setting the AUTOMATIC\_APPLICATION\_MAINTENANCE
property on the application package.

For more information, see [Consumer-controlled maintenance policies: Provider guide](/developer-guide/native-apps/consumer-maintenance-policies-provider).
