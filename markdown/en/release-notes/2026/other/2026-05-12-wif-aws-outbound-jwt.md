# May 12, 2026: JWT-based authentication for AWS Workload Identity Federation (*General availability*)

The Snowflake Python connector now supports a JWT-based authentication method for AWS Workload
Identity Federation (WIF). The new method uses the AWS `GetWebIdentityToken` API to produce
a standards-based JWT instead of the existing `GetCallerIdentity`-based pre-signed request
method. The existing `GetCallerIdentity`-based method remains supported, but Snowflake recommends
upgrading to the JWT-based method.

To use the JWT-based method, set the `SNOWFLAKE_ENABLE_AWS_WIF_OUTBOUND_TOKEN` environment
variable to `true` in your application’s runtime environment, and configure an `ISSUER`
on the Snowflake service user. Requires Python connector v4.5.0 or later.

For more information, see [Upgrade to JWT-based authentication](/user-guide/workload-identity-federation#label-wif-aws-upgrade-jwt).
