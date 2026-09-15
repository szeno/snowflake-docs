# Snowflake Native App Framework: Providers must accept terms of service to set the DISTRIBUTION property to EXTERNAL

To publish or upgrade a Snowflake Native App in a consumer account, a provider must set the `DISTRIBUTION`
property of the application package to `EXTERNAL`. A provider can set this property using the
[CREATE APPLICATION PACKAGE](/sql-reference/sql/create-application-package) or
[ALTER APPLICATION PACKAGE](/sql-reference/sql/alter-application-package) commands.

Before the change:
:   Before, providers could set `DISTRIBUTION=EXTERNAL` or create a version or patch for an application
    package without accepting the Provider Terms of Service.

After the change:
:   If a provider tries to set the `DISTRIBUTION` property to `EXTERNAL`, or if they create a version
    or patch for an application package where the `DISTRIBUTION` property has been set to `EXTERNAL`,
    they get an error message prompting them to accept the terms. The action they took with the command does
    not complete.

Ref: n/a
