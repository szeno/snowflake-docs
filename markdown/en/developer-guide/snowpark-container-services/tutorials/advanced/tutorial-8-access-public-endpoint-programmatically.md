# Tutorial 8: Access the public endpoint programmatically

Feature — Generally Available

Snowpark Container Services is available to accounts in [AWS, Microsoft Azure, and Google Cloud Platform commercial regions](/user-guide/intro-regions#label-na-general-regions), with some exceptions. For more information, see [Available regions and considerations](/developer-guide/snowpark-container-services/overview#label-snowpark-containers-overview-available-regions).

## Introduction

In [Tutorial 1](/developer-guide/snowpark-container-services/tutorials/tutorial-1), you learned how to
[access a public endpoint by using a web browser](/developer-guide/snowpark-container-services/tutorials/tutorial-1#label-snowpark-containers-tutorial-1-step-4).
Using the browser, you sent a request to the public endpoint, which is the ingress endpoint.
This required you to first authenticated with Snowflake, and then
you interacted with the service by using the web UI that the service provides.

In this tutorial, you access the same public endpoint programmatically.
The tutorial shows you three different options
to authenticate when you log into Snowflake: by using a programmatic access token (PAT),
by using a JSON Web Token (JWT), and using a Session Token from the Python Connector

## Prerequisites

1. Start `echo_service` service as described in [Tutorial 1](/developer-guide/snowpark-container-services/tutorials/tutorial-1).
2. To verify that the service is running, execute the [DESCRIBE SERVICE](/sql-reference/sql/desc-service) command.

   Copy code

   ```
   DESC SERVICE echo_service;
   ```
3. In the `status` column, verify that it shows that the service status as RUNNING.

   If the status is PENDING, it indicates that the service is still starting.
4. To investigate why the service isn’t RUNNING,
   execute the [SHOW SERVICE CONTAINERS IN SERVICE](/sql-reference/sql/show-service-containers-in-service) command, and then
   review the `status` of individual containers:

   Copy code

   ```
   SHOW SERVICE CONTAINERS IN SERVICE echo_service;
   ```

Important

Don’t proceed with this tutorial until you have the `echo_service` running.

## Option 1: Send requests to the service endpoint programmatically by using a PAT

This option shows you how to access a service endpoint programmatically by using
curl and Python.
In both cases you use a
[programmatic access token (PAT)](/user-guide/programmatic-access-tokens)
for authentication. Snowflake recommends that you use PAT for programmatic access.

### Set up a PAT

This procedure is a continuation of [Tutorial 1](/developer-guide/snowpark-container-services/tutorials/tutorial-1). Use the same user (`testuser`), database (`tutorial_db`),
and schema (`data_schema`) as in Tutorial 1.

1. To create a PAT for the user, run the following command.

   You should review the PAT-related
   [prerequisites](/user-guide/programmatic-access-tokens#label-pat-prerequisites) because if you don’t meet those prerequisites, you can generate a PAT but
   you can’t authenticate by using the PAT.

   Copy code

   ```
   ALTER USER ADD PROGRAMMATIC ACCESS TOKEN example_token role_restriction='PUBLIC';
   ```

   This command creates a PAT to sign in to Snowflake as a `testuser` with the role `public`.

   Example output:

   ```
   +---------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
   | token_name    | token_secret                                                                                                                                                                                                                    |
   |---------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
   | EXAMPLE_TOKEN | exampleiOiIyMDY0Mzc2MDQ1MzIyNDIiLCJhbGciOiJFUzI1NiJ9.eyJwIjoiMzE0OTk4ODUxMzozMTQ5OTg4MTAxIiwiaXNzIjoiU0Y6MTAwMyIsImV4cCI6MTc2NTUwMTY4NH0.tYDChZeiA9rIUR5Oow9ztoNoaAhyEWMaXZdZKAP0ELnuY8gN3_hMsMy4PE9dGIs2JE9CafYjxgCFOOrku4LP4g |
   +---------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
   ```
2. Save the `token_secret` value for later use.

   You need this value later to authenticate when you send requests to the public endpoint.
3. To find the ingress URL for the public endpoint that the `echo_service` exposes, run the following command:

   Copy code

   ```
   SHOW ENDPOINTS IN SERVICE echo_service;
   ```

   Example output:

   ```
   +--------------+------+------------+----------+-----------+---------------------------------------------------------------------+
   | name         | port | port_range | protocol | is_public | ingress_url                                                         |
   |--------------+------+------------+----------+-----------+---------------------------------------------------------------------|
   | echoendpoint | 8000 | NULL       | HTTP     | true      | <endpoint-id>-<orgname>-<acctname>.snowflakecomputing.app           |
   +--------------+------+------------+----------+-----------+---------------------------------------------------------------------+
   ```
4. Save the `ingress_url` value for later use.

   You need this value later to send requests to the public endpoint.

Now you are ready to sign in to Snowflake by using the PAT for authentication and send programmatic
requests to the *ingress\_url* of the public endpoint of the `echo_service`.

### Send requests to the service endpoint programmatically by using a PAT

In this section, you send programmatic requests to the public endpoint of the `echo_service` using curl and Python.

#### Send request using curl

Save the PAT to an environment variable.

For example, on a Mac or Linux operating system,
you can use the following command:

Copy code

```
$ pat=<pat-token-from-previous-step>
```

Send a request to the public endpoint of the `echo_service`, as shown
in the following example:

Copy code

```
$ curl -v "https://<ingress-URL>/ui" \
      --header "Authorization: Snowflake Token=\"${pat}\""
```

The command sends a GET request to the public endpoint of the `echo_service`, providing the
following information:

- The URL (`https://<ingress-URL>/ui`) of the endpoint. The string `/ui` appended to the
  ingress URL causes the service to execute the `ui()` function.
  For more information, see the `echo_service.py` file.
- The `Authorization` header with PAT token for authentication.

In response, the `echo_service` in this example serves an HTML page, which curl prints to the console.
Without the PAT, the endpoint returns a redirect to the Snowflake sign-in page.

#### Send request using Python

To send a request to the public endpoint of the `echo_service`,
use a PAT for authentication by using Python, as shown in the following
example steps:

1. In the `invokeUsingPat.py` file, save the following code:

> Copy code
>
> ```
> import argparse
> import logging
> import sys
> import requests
> logger = logging.getLogger(__name__)
> def main():
>     args = _parse_args()
>     if args.pat is None:
>         logger.error("PAT is required to proceed.")
>         sys.exit(1)
>     logger.info("Using PAT for authentication.")
>     url = args.spcs_url
>     connect_to_spcs(args.pat, url)
> def connect_to_spcs(token, url):
>     headers = {'Authorization': f'Snowflake Token="{token}"'}
>     data = {"input": "test"}
>     logger.info(f"Headers: {headers}")
>     logger.info(f"URL: {url}")
>     response = requests.post(f'{url}', headers=headers, data=data)
>     assert response.status_code == 200, f"Response code is not 200: {response.text}"
>     logger.info("========================================")
>     logger.info("Response succeeded. Details below:")
>     logger.info(response.text)
> def _parse_args():
>     logging.basicConfig(stream=sys.stdout, level=logging.INFO)
>     cli_parser = argparse.ArgumentParser()
>     cli_parser.add_argument('--pat', required=True, help='Personal Access Token (PAT) for the user.')
>     cli_parser.add_argument('--spcs_url', required=True,
>                             help='The SPCS URL to connect programmatically.')
>     args = cli_parser.parse_args()
>     return args
> if __name__ == "__main__":
>     main()
> ```

1. Run the code that you saved by sending the following request:

> Copy code
>
> ```
> $ python ./invokeUsingPat.py \
>   --spcs_url "https://<endpoint-id>-<orgname>-<acctname>.snowflakecomputing.app/ui" \
>   –pat ${pat}
> ```
>
> When the request arrives, the service executes the `ui()` function, which
> renders an HTML form as shown in the following example. For more information,
> see the
> “Reviewing the service code” step of [Tutorial 1](/developer-guide/snowpark-container-services/tutorials/tutorial-1#label-snowpark-containers-tutorial-1-step-6a).
>
> Copy code
>
> ```
> <!DOCTYPE html>
> <html lang="en">
> <head>
>   <title>Welcome to echo service!</title>
> </head>
>
> <body>
>   <h1>Welcome to echo service!</h1>
>   <form action="/ui" method="post">
>     <label for="input">Input:<label><br />
>     <input type="text" id="input" name="input"><br />
>   </form>
>   <h2>Input:</h2>
>
>   <h2>Output:</h2>
>
> </body>
> ```

## Option 2: Send requests to the service endpoint programmatically by using a JWT

In this option, the Python sample code that you are provided uses [key pair authentication](/user-guide/key-pair-auth). By using the key pair
that you provide, the sample code performs the following actions:

1. Generates a JSON Web Token (JWT).
2. Exchanges the JWT with Snowflake for an OAuth token.
3. Uses the OAuth token for authentication when the sample code communicates
   with the `echo_service` public endpoint.

### Set up a JWT

To communicate with the `echo_service` programmatically,
complete the following steps. By using the Python code provided, you send
requests to the public endpoint that the `echo_service` exposes.

1. At the command prompt or in the terminal, create a directory, and then navigate to it.
2. Configure key pair authentication for the user:

   1. Generate a [key pair](/user-guide/key-pair-auth#label-configuring-key-pair-authentication):

      1. Generate a private key by running the following command.

         To simplify the steps, you generate an unencrypted private key. You can also use an encrypted private key but it requires that you enter the password.

         Copy code

         ```
         openssl genrsa 2048 | openssl pkcs8 -topk8 -inform PEM -out rsa_key.p8 -nocrypt
         ```
      2. To generate a public key (`rsa_key.pub`) by referencing the private key that you created, run the following command:

         Copy code

         ```
         openssl rsa -in rsa_key.p8 -pubout -out rsa_key.pub
         ```
   2. In the directory, verify that you generated the private key and public key.
   3. Assign the public key to the user that you are using to test the programmatic access.

      This action lets the user specify the key for authentication.

      Copy code

      ```
      ALTER USER <user-name> SET RSA_PUBLIC_KEY='MIIBIjANBgkqh...';
      ```
3. In Python files, save the provided sample code:

   1. In the `generateJWT.py` file, save the following code:

      Copy code

      ```
      # To run this on the command line, enter:
      #   python3 generateJWT.py --account=<account_identifier> --user=<username> --private_key_file_path=<path_to_private_key_file>

      from cryptography.hazmat.primitives.serialization import load_pem_private_key
      from cryptography.hazmat.primitives.serialization import Encoding
      from cryptography.hazmat.primitives.serialization import PublicFormat
      from cryptography.hazmat.backends import default_backend
      from datetime import timedelta, timezone, datetime
      import argparse
      import base64
      from getpass import getpass
      import hashlib
      import logging
      import sys

      # This class relies on the PyJWT module (https://pypi.org/project/PyJWT/).
      import jwt

      logger = logging.getLogger(__name__)

      try:
          from typing import Text
      except ImportError:
          logger.debug('# Python 3.5.0 and 3.5.1 have incompatible typing modules.', exc_info=True)
          from typing_extensions import Text

      ISSUER = "iss"
      EXPIRE_TIME = "exp"
      ISSUE_TIME = "iat"
      SUBJECT = "sub"

      # If you generated an encrypted private key, implement this method to return
      # the passphrase for decrypting your private key. As an example, this function
      # prompts the user for the passphrase.
      def get_private_key_passphrase():
          return getpass('Passphrase for private key: ')

      class JWTGenerator(object):
          """
          Creates and signs a JWT with the specified private key file, username, and account identifier. The JWTGenerator keeps the
          generated token and only regenerates the token if a specified period of time has passed.
          """
          LIFETIME = timedelta(minutes=59)  # The tokens will have a 59-minute lifetime
          RENEWAL_DELTA = timedelta(minutes=54)  # Tokens will be renewed after 54 minutes
          ALGORITHM = "RS256"  # Tokens will be generated by using RSA with SHA256

          def __init__(self, account: Text, user: Text, private_key_file_path: Text,
                lifetime: timedelta = LIFETIME, renewal_delay: timedelta = RENEWAL_DELTA):
        """
        __init__ creates an object that generates JWTs for the specified user, account identifier, and private key.
        :param account: Your Snowflake account identifier. See https://docs.snowflake.com/en/user-guide/admin-account-identifier.html. Note that if you are by using the account locator, exclude any region information from the account locator.
        :param user: The Snowflake username.
        :param private_key_file_path: Path to the private key file used for signing the JWTs.
        :param lifetime: The number of minutes (as a timedelta) during which the key will be valid.
        :param renewal_delay: The number of minutes (as a timedelta) from now after which the JWT generator should renew the JWT.
        """

        logger.info(
            """Creating JWTGenerator with arguments
            account : %s, user : %s, lifetime : %s, renewal_delay : %s""",
            account, user, lifetime, renewal_delay)

        # Construct the fully qualified name of the user in uppercase.
        self.account = self.prepare_account_name_for_jwt(account)
        self.user = user.upper()
        self.qualified_username = self.account + "." + self.user

        self.lifetime = lifetime
        self.renewal_delay = renewal_delay
        self.private_key_file_path = private_key_file_path
        self.renew_time = datetime.now(timezone.utc)
        self.token = None

        # Load the private key from the specified file.
        with open(self.private_key_file_path, 'rb') as pem_in:
            pemlines = pem_in.read()
            try:
                # Try to access the private key without a passphrase.
                self.private_key = load_pem_private_key(pemlines, None, default_backend())
            except TypeError:
                # If that fails, provide the passphrase returned from get_private_key_passphrase().
                self.private_key = load_pem_private_key(pemlines, get_private_key_passphrase().encode(), default_backend())

          def prepare_account_name_for_jwt(self, raw_account: Text) -> Text:
        """
        Prepare the account identifier for use in the JWT.
        For the JWT, the account identifier must not include the subdomain or any region or cloud provider information.
        :param raw_account: The specified account identifier.
        :return: The account identifier in a form that can be used to generate the JWT.
        """
        account = raw_account
        if not '.global' in account:
            # Handle the general case.
            idx = account.find('.')
            if idx > 0:
                account = account[0:idx]
        else:
            # Handle the replication case.
            idx = account.find('-')
            if idx > 0:
                account = account[0:idx]
        # Use uppercase for the account identifier.
        return account.upper()

          def get_token(self) -> Text:
        """
        Generates a new JWT. If a JWT has already been generated earlier, return the previously generated token unless the
        specified renewal time has passed.
        :return: the new token
        """
        now = datetime.now(timezone.utc)  # Fetch the current time

        # If the token has expired or doesn't exist, regenerate the token.
        if self.token is None or self.renew_time <= now:
            logger.info("Generating a new token because the present time (%s) is later than the renewal time (%s)",
                        now, self.renew_time)
            # Calculate the next time we need to renew the token.
            self.renew_time = now + self.renewal_delay

            # Prepare the fields for the payload.
            # Generate the public key fingerprint for the issuer in the payload.
            public_key_fp = self.calculate_public_key_fingerprint(self.private_key)

            # Create our payload
            payload = {
                # Set the issuer to the fully qualified username concatenated with the public key fingerprint.
                ISSUER: self.qualified_username + '.' + public_key_fp,

                # Set the subject to the fully qualified username.
                SUBJECT: self.qualified_username,

                # Set the issue time to now.
                ISSUE_TIME: now,

                # Set the expiration time, based on the lifetime specified for this object.
                EXPIRE_TIME: now + self.lifetime
            }

            # Regenerate the actual token
            token = jwt.encode(payload, key=self.private_key, algorithm=JWTGenerator.ALGORITHM)
            # If you are by using a version of PyJWT prior to 2.0, jwt.encode returns a byte string instead of a string.
            # If the token is a byte string, convert it to a string.
            if isinstance(token, bytes):
              token = token.decode('utf-8')
            self.token = token
            logger.info("Generated a JWT with the following payload: %s", jwt.decode(self.token, key=self.private_key.public_key(), algorithms=[JWTGenerator.ALGORITHM]))

        return self.token

          def calculate_public_key_fingerprint(self, private_key: Text) -> Text:
        """
        Given a private key in PEM format, return the public key fingerprint.
        :param private_key: private key string
        :return: public key fingerprint
        """
        # Get the raw bytes of public key.
        public_key_raw = private_key.public_key().public_bytes(Encoding.DER, PublicFormat.SubjectPublicKeyInfo)

        # Get the sha256 hash of the raw bytes.
        sha256hash = hashlib.sha256()
        sha256hash.update(public_key_raw)

        # Base64-encode the value and prepend the prefix 'SHA256:'.
        public_key_fp = 'SHA256:' + base64.b64encode(sha256hash.digest()).decode('utf-8')
        logger.info("Public key fingerprint is %s", public_key_fp)

        return public_key_fp

      def main():
          logging.basicConfig(stream=sys.stdout, level=logging.INFO)
          cli_parser = argparse.ArgumentParser()
          cli_parser.add_argument('--account', required=True, help='The account identifier (e.g. "myorganization-myaccount" for "myorganization-myaccount.snowflakecomputing.com").')
          cli_parser.add_argument('--user', required=True, help='The user name.')
          cli_parser.add_argument('--private_key_file_path', required=True, help='Path to the private key file used for signing the JWT.')
          cli_parser.add_argument('--lifetime', type=int, default=59, help='The number of minutes that the JWT should be valid for.')
          cli_parser.add_argument('--renewal_delay', type=int, default=54, help='The number of minutes before the JWT generator should produce a new JWT.')
          args = cli_parser.parse_args()

          token = JWTGenerator(args.account, args.user, args.private_key_file_path, timedelta(minutes=args.lifetime), timedelta(minutes=args.renewal_delay)).get_token()
          print('JWT:')
          print(token)

      if __name__ == "__main__":
          main()
      ```
   2. In the `access-via-keypair.py` file, save the following code:

      Copy code

      ```
      from generateJWT import JWTGenerator
      from datetime import timedelta
      import argparse
      import logging
      import sys
      import requests
      logger = logging.getLogger(__name__)

      def main():
        args = _parse_args()
        token = _get_token(args)
        snowflake_jwt = token_exchange(token,endpoint=args.endpoint, role=args.role,
                  snowflake_account_url=args.snowflake_account_url,
                  snowflake_account=args.account)
        spcs_url=f'https://{args.endpoint}{args.endpoint_path}'
        connect_to_spcs(snowflake_jwt, spcs_url)

      def _get_token(args):
        token = JWTGenerator(args.account, args.user, args.private_key_file_path, timedelta(minutes=args.lifetime),
            timedelta(minutes=args.renewal_delay)).get_token()
        logger.info("Key Pair JWT: %s" % token)
        return token

      def token_exchange(token, role, endpoint, snowflake_account_url, snowflake_account):
        scope_role = f'session:role:{role}' if role is not None else None
        scope = f'{scope_role} {endpoint}' if scope_role is not None else endpoint
        data = {
          'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer',
          'scope': scope,
          'assertion': token,
        }
        logger.info(data)
        url = f'https://{snowflake_account}.snowflakecomputing.com/oauth/token'
        if snowflake_account_url:
          url =       f'{snowflake_account_url}/oauth/token'
        logger.info("oauth url: %s" %url)
        response = requests.post(url, data=data)
        logger.info("snowflake jwt : %s" % response.text)
        assert 200 == response.status_code, "unable to get snowflake token"
        return response.text

      def connect_to_spcs(token, url):
        # Create a request to the ingress endpoint with authz.
        headers = {'Authorization': f'Snowflake Token="{token}"'}
        response = requests.post(f'{url}', headers=headers)
        logger.info("return code %s" % response.status_code)
        logger.info(response.text)

      def _parse_args():
        logging.basicConfig(stream=sys.stdout, level=logging.INFO)
        cli_parser = argparse.ArgumentParser()
        cli_parser.add_argument('--account', required=True,
              help='The account identifier (for example, "myorganization-myaccount" for '
                '"myorganization-myaccount.snowflakecomputing.com").')
        cli_parser.add_argument('--user', required=True, help='The user name.')
        cli_parser.add_argument('--private_key_file_path', required=True,
              help='Path to the private key file used for signing the JWT.')
        cli_parser.add_argument('--lifetime', type=int, default=59,
              help='The number of minutes that the JWT should be valid for.')
        cli_parser.add_argument('--renewal_delay', type=int, default=54,
              help='The number of minutes before the JWT generator should produce a new JWT.')
        cli_parser.add_argument('--role',
              help='The role we want to use to create and maintain a session for. If a role isn\'t provided, '
                'use the default role.')
        cli_parser.add_argument('--endpoint', required=True,
              help='The ingress endpoint of the service')
        cli_parser.add_argument('--endpoint-path', default='/',
              help='The url path for the ingress endpoint of the service')
        cli_parser.add_argument('--snowflake_account_url', default=None,
              help='The account url of the account for which we want to log in. Type of '
                'https://myorganization-myaccount.snowflakecomputing.com')
        args = cli_parser.parse_args()
        return args

      if __name__ == "__main__":
        main()
      ```

### Send requests to the service endpoint programmatically by using a JWT

- To make the ingress call to the `echo_service` public endpoint, execute the
  `access-via-keypair.py` Python code:

  Copy code

  ```
  python3 access-via-keypair.py \
    --account <account-identifier> \
    --user <user-name> \
    --role TEST_ROLE \
    --private_key_file_path rsa_key.p8 \
    --endpoint <ingress-hostname> \
    --endpoint-path /ui
  ```

Important

The name specified by the `--role` flag must exactly match the case of
the role name shown by [SHOW ROLES](/sql-reference/sql/show-roles).

For more information about `account-identifier`, see [Account identifiers](/user-guide/admin-account-identifier).

### How authentication works when you use a JWT

The code first converts the provided key pair into a JWT token. It then sends
the JWT token to Snowflake to obtain an OAuth token. Finally, the code uses the
OAuth token to connect to Snowflake and access the public endpoint.

Specifically, the code performs the following actions:

1. The code calls the `_get_token(args)` function to generate a JWT from the key pair that you provide.

   The function implementation is shown in the following example:

   Copy code

   ```
   def _get_token(args):
    token = JWTGenerator(args.account,
                        args.user,
                        args.private_key_file_path,
                        timedelta(minutes=args.lifetime),
                        timedelta(minutes=args.renewal_delay)).get_token()
    logger.info("Key Pair JWT: %s" % token)
    return token
   ```

   `JWTGenerator` is a helper class that is provided to you. The following list
   includes information about the parameters that you provide when you create
   this object:

   - `args.account` and the `args.user` parameters: A JWT has several fields.
     For more information, see [token format](/developer-guide/sql-api/authenticating#label-sql-api-authenticating-key-pair). `iss` is one of the JWT’s fields. This field value includes
     the Snowflake account name and a user name. Therefore, you provide these values as parameters.
   - Two `timedelta` parameters provide the following information:
     - `lifetime` specifies the number of minutes during which the key will be valid (60 minutes).
     - `renewal_delay` specifies the number of minutes from now after which the JWT generator should renew the JWT.
2. The code calls the `token_exchange()` function to connect to Snowflake, and
   then exchange the JWT for an OAuth token:

   Copy code

   ```
   scope_role = f'session:role:{role}' if role is not None else None
   scope = f'{scope_role} {endpoint}' if scope_role is not None else endpoint

   data = {
    'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer',
    'scope': scope,
    'assertion': token,
   }
   ```

   The preceding code constructs JSON text that sets the scope for the OAuth token,
   which is the public endpoint that can be accessed by using the specified role.
   This code then makes a POST request to Snowflake. Snowflake passes the JSON
   text to exchange the JWT
   for an OAuth token (see [Token exchange](/user-guide/oauth-custom#label-oauth-token-exchange)), as shown in the
   following example:

   Copy code

   ```
   url = f'{snowflake_account_url}/oauth/token'
   response = requests.post(url, data=data)
   assert 200 == response.status_code, "unable to get Snowflake token"
   return response.text
   ```
3. To connect to the public endpoint of the `echo_service`, the code then calls `connect_to_spcs()` function.

   It provides the URL (`https://<ingress-URL>/ui`) of the endpoint and the OAuth token for authentication.

   Copy code

   ```
   headers = {'Authorization': f'Snowflake Token="{token}"'}
   response = requests.post(f'{url}', headers=headers)
   ```

   The `url` is the `spcs_url` that you provided to the program and the `token` is the OAuth token.

   The `echo_service` in this example serves an HTML page, as explained in the preceding section.
   This sample code simply prints the HTML in the response.

## Option 3: Send requests to the service endpoint programmatically by using a session token

This option shows how to access a service endpoint programmatically by using a session token for authentication. You can obtain the session token by using the Python Connector, as shown in the following example.

This code provides an alternative to key-pair authentication; however, there is no guarantee that it will work with future versions of the [Snowflake Connector](/developer-guide/python-connector/python-connector) for Python. The example first uses the connector to generate a session token that represents your identity, then uses that token to authenticate to the public endpoint.

1. Configure a connection named “test”.

   For more instructions, see [Connecting using the `connections.toml` file](/developer-guide/python-connector/python-connector-connect#label-python-connection-toml).
2. Save the following Python code to a `spcs-connect.py` file.

   Copy code

   ```
   import argparse
   import requests
   import snowflake.connector

   parser = argparse.ArgumentParser(prog='myprogram')
   parser.add_argument('target', help="https endpoint or fully qualified service name")
   parser.add_argument('-c', '--config', default="default", help="snowflake connection name")
   parser.add_argument('-p', '--path', default="/", help="url path when service name is provided")
   args = parser.parse_args()

   with snowflake.connector.connect(
        connection_name=args.config,
        session_parameters={ 'PYTHON_CONNECTOR_QUERY_RESULT_FORMAT': 'json' },
   ) as conn:
    target = args.target
    # derive url from target arg
    if target.startswith("https:"):
        url = target
    else: # assume target is service name
        print(f"lookup up endpoint url for service: {target}")
        for (name, port, range, protocol, is_public, hostname) in conn.cursor().execute(
                f"SHOW ENDPOINTS IN SERVICE {target}"):
            if is_public:
                url = f"https://{hostname}{args.path}"
                break

    # Obtain a session token.
    token_data = conn._rest._token_request('ISSUE')
    token = token_data['data']['sessionToken']

    # Request headers
    headers = {'Authorization': f'Snowflake Token="{token}"'}

    # connect
    print(f"connecting to {url} ...")
    response = requests.get(url, headers=headers)
    print(response.text)
   ```
3. Update the Python code by supplying the connection name to
   `snowflake.connector.connect`, similar to the following example:

   Copy code

   ```
   with snowflake.connector.connect(
        connection_name="test",
   ) as conn:
    target = args.target
   ```
4. Use the following command to run the Python code that first generates
   a session token, and then sends a request to the public endpoint of
   the service programmatically by using the session token:

   Copy code

   ```
   python spcs-connect.py "https://<ingress-URL>/ui"
   ```

   Alternatively, if you know the hostname of the public endpoint —
   [SHOW ENDPOINTS](/sql-reference/sql/show-endpoints) — you can
   use the following script. For example, if the hostname of the public endpoint is
   `ewapx-testorg-testaccount.snowflakecomputing.app`, you can use the following script:

   Copy code

   ```
   python spcs-connect.py -c test -p "https://ewapx-testorg-testaccount.snowflakecomputing.app/"
   ```

   Example output:

   Copy code

   ```
   <!DOCTYPE html>
   <html lang=“en”>

   <head>
     <title>Welcome to echo service!</title>
   </head>

   <body>
     <h1>Welcome to echo service!</h1>
     <form action="/ui" method="post">
    <label for="input">Input:<label><br />
    <input type="text" id="input" name="input"><br />
     </form>
     <h2>Input:</h2>

     <h2>Output:</h2>

   </body>

   </html>
   ```

## Clean up

For instructions,
see the [Tutorial 1, Clean up step](/developer-guide/snowpark-container-services/tutorials/tutorial-1).
