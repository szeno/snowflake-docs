# Jan 21, 2026: Snowflake OAuth for local applications

Snowflake OAuth for local applications is now the preferred authentication method for local applications, including desktop applications and
local scripts. It is a strong authentication method that can be implemented without an administrator, requires minimal setup, and doesn’t
require the application to store secrets.

Snowflake OAuth uses a security integration to establish the interface between a client and Snowflake. Every Snowflake account now has a
built-in security integration `SNOWFLAKE$LOCAL_APPLICATION` that creates the interface between local applications and Snowflake. You can
adjust the parameters of the integration to perform administrative tasks like specifying how long OAuth access tokens and
refresh tokens are valid.

For more information, see [Using Snowflake OAuth for local applications](/user-guide/oauth-local-applications).
