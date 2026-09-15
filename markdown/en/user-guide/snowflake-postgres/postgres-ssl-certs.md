# Snowflake Postgres SSL certificates

Snowflake Postgres runs with secure SSL connections to clusters. When connecting clients and applications to a cluster, include
`SSLMODE=require` in your settings, or the equivalent setting for non-`libpq`-based drivers. For more details and connection
troubleshooting tips, see [Connecting to Snowflake Postgres](/user-guide/snowflake-postgres/connecting-to-snowflakepg).

For an added layer of security, admins and instance owners can retrieve the public certificate portion of the root CA (Certificate
Authority) public certificate and private key pair that is used to sign each Snowflake Postgres server’s certificate. These root CA
certificates (and their non-shared private keys) are unique to each Snowflake account. Once retrieved, the root CA certificate can be used
for additional verification of the server certificates presented at connection time to protect against man-in-the-middle (MITM) attacks.

## Retrieving the SSL public root certificate

SnowsightSQL

1. In the navigation menu, select **Postgres**.
2. In the **More Options [⋮]** menu at the top right, select **Download Certificate**.
3. Select **Download** in the confirmation dialog.

You can retrieve the root CA certificate from the `certificate` field returned by the [DESCRIBE POSTGRES INSTANCE](/sql-reference/sql/desc-postgres-instance)
command. This certificate is the same for all instances on a given account.

Copy code

```
DESCRIBE POSTGRES INSTANCE my_postgres
 ->> SELECT "property", "value"
     FROM $1
     WHERE "property" = 'certificate';
```

## Configuring Postgres clients for SSL certificate verification

1. Place the root CA certificate text, including the “—BEGIN CERTIFICATE—“ and “—END CERTIFICATE—“ lines, in a file
   in a secure location on your client host. If you already have a root CA store file with contents that you want to reuse, you can append
   your Snowflake Postgres root CA certificate text to it.
2. In your connection configuration:
   1. Specify the root CA public certificate location with the `sslrootcert=/path/to/root/certfile` in your connection parameters.
   2. Specify either `sslmode=verify-ca` or `sslmode=verify-full` (instead of `sslmode=require`)
      in your connection parameters.

Note

`sslrootcert` has a default value of `$HOME/.postgresql/root.crt` for the client system user making the connection. If you place
your root CA certificate at that location, you don’t need to specify the `sslrootcert` parameter for your connection.

Here is how these two `sslmode` values work:

- **verify-ca**: Verifies that the server is trustworthy by checking that it was signed by the root CA certificate pair
  using the present root CA public certificate.
- **verify-full**: Performs the `verify-ca` verification and additionally verifies that the server host name matches
  a name stored in the server certificate. Snowflake ensures that this will work for all signed server certificates signed with your
  account’s root CA.

The SSL connection fails if the server certificate can’t be verified per the specified `sslmode` parameter. Snowflake recommends
`verify-full` in most security-sensitive environments.

Warning

If there is a root CA certificate present, then `sslmode=require` performs the same verification as `sslmode=verify-ca`. The presence
of a root CA certificate at `$HOME/.postgresql/root.crt` for a server with a certificate signed by a different CA is a common source of
SSL connection errors. If this happens, you can simply append your Snowflake root CA certificate’s text to that file, or place it somewhere
else specified by the connection’s `sslrootcert` parameter.

Note

For a full explanation of how these different `sslmode` setting levels prevent against MITM attacks, see the PostgreSQL chapter on
[Protection provided in different sslmode settings](https://www.postgresql.org/docs/current/libpq-ssl.html#LIBPQ-SSL-PROTECTION).
