# Authentication and connection options

## Key pair authentication support

Snowflake SQLAlchemy supports key pair authentication, which allows you to authenticate without providing a password. This is useful for CI/CD pipelines and automated scripts.

### Generating a key pair

First, generate a private key and public key:

Copy code

```
# Generate private key (encrypted)
openssl genrsa 2048 | openssl pkcs8 -topk8 -inform PEM -out rsa_key.p8 -v1 PBE-SHA1-3DES

# Or generate unencrypted key (not recommended for production)
openssl genrsa 2048 | openssl pkcs8 -topk8 -inform PEM -nocrypt -out rsa_key.p8

# Extract public key
openssl rsa -in rsa_key.p8 -pubout -out rsa_key.pub
```

### Using key pair authentication

Pass the private key file path as `private_key_file` in `connect_args`. If the key is encrypted, pass its passphrase as `private_key_file_pwd` (an alias of `private_key_password`). The `URL` helper doesn’t accept these parameters, and `private_key_file` can’t be set in the URL query string:

Copy code

```
from sqlalchemy import create_engine

engine = create_engine(
    'snowflake://user@account/database/schema',
    connect_args={
        'authenticator': 'SNOWFLAKE_JWT',
        'private_key_file': '/path/to/rsa_key.p8',
        'private_key_file_pwd': 'your_passphrase',  # if encrypted
    }
)
```

Or pass the key itself as `private_key`. This parameter accepts the key as DER-encoded bytes or as a private key object from the `cryptography` package. The following example loads an encrypted PEM file and converts it to unencrypted DER bytes in memory:

Copy code

```
from cryptography.hazmat.primitives import serialization
from sqlalchemy import create_engine

with open('/path/to/rsa_key.p8', 'rb') as f:
    key = serialization.load_pem_private_key(f.read(), password=b'your_passphrase')

private_key = key.private_bytes(
    encoding=serialization.Encoding.DER,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption(),
)

engine = create_engine(
    'snowflake://user@account/database/schema',
    connect_args={
        'authenticator': 'SNOWFLAKE_JWT',
        'private_key': private_key,
    }
)
```

## PrivateLink and account name handling

When using AWS PrivateLink or another private connectivity service, specify the account as `<account>.<region>.privatelink` (or `<account>.privatelink` for regionless account identifiers). The dialect extracts the account name and connects to the matching `privatelink.snowflakecomputing.com` host:

Copy code

```
from sqlalchemy import create_engine

engine = create_engine(
    'snowflake://user:password@myaccount.eu-central-1.privatelink/database/schema'
)
```

## SSO authentication

Snowflake SQLAlchemy supports single sign-on (SSO) authentication with identity providers such as Okta and Microsoft Entra ID (formerly Azure Active Directory).

### Native Okta SSO

To authenticate natively through Okta, set `authenticator` to your Okta URL:

Copy code

```
from sqlalchemy import create_engine

engine = create_engine(
    'snowflake://user@account/database/schema',
    connect_args={
        'authenticator': 'https://your-okta-instance.okta.com',
    }
)
```

### External browser authentication

For any SAML 2.0 identity provider, including Okta and Microsoft Entra ID, use the `externalbrowser` authenticator:

Copy code

```
from sqlalchemy import create_engine

engine = create_engine(
    'snowflake://user@account/database/schema',
    connect_args={
        'authenticator': 'externalbrowser',
    }
)
```

When the connection opens, your default browser opens and redirects to your identity provider’s login page. After successful authentication, the browser returns to Snowflake.
