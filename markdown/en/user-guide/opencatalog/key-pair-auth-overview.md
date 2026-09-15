# Overview of key pair authentication in Snowflake Open Catalog

Feature — Generally Available

Not available in government regions.

This topic describes using key pair authentication and key pair rotation in Snowflake Open Catalog.

Open Catalog supports using key pair authentication for enhanced authentication security as an alternative to
using a client ID and secret.

This authentication method requires, as a minimum, a 2048-bit RSA key pair. You can generate the Privacy Enhanced Mail (PEM) private-public
key pair using OpenSSL. The public key is assigned to the Open Catalog user who uses a client application to connect and authenticate
to Snowflake.
