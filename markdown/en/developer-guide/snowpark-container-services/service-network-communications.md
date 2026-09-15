# Service networking

Feature — Generally Available

Snowpark Container Services is available to accounts in [AWS, Microsoft Azure, and Google Cloud Platform commercial regions](/user-guide/intro-regions#label-na-general-regions), with some exceptions. For more information, see [Available regions and considerations](/developer-guide/snowpark-container-services/overview#label-snowpark-containers-overview-available-regions).

With Snowpark Container Services services, there are three types of networking to consider:

- Ingress networking: How to connect from outside Snowflake into your service.
- Egress networking: How your service connects to resources outside Snowflake.
- Service-to-service communication in Snowpark Container Services.

The following sections explain how to configure each kind of networking.

## Configure service ingress

To allow anything to interact with your service from the internet, you declare the network ports on which your service is
listening as endpoints in the service specification file. These endpoints control ingress.

By default, service endpoints are private. Only
[service functions](/developer-guide/snowpark-container-services/working-with-services#label-snowpark-containers-service-communicating-service-function) and
[service-to-service communications](/developer-guide/snowpark-container-services/working-with-services#label-snowpark-containers-service-communicating-service-to-service)
can make requests to the private endpoints. You can declare an endpoint as public to allow requests to an endpoint from the
internet as shown in the following example service specification.

Note

Creating a public endpoint is a privileged operation and the service’s owner role must have the BIND SERVICE ENDPOINT privilege on the account.

Copy code

```
endpoints:
- name: <endpoint name>
  port: <port number>
  protocol : < TCP / HTTP >
  public: true
  corsSettings:                  # optional CORS configuration
    Access-Control-Allow-Origin: # required list of allowed origins
      - <origin>                 # for example, "http://example.com"
      - <origin>
        ...
    Access-Control-Allow-Methods: # optional list of HTTP methods
      - <method>
      - <method>
        ...
    Access-Control-Allow-Headers: # optional list of HTTP headers
      - <header-name>
      - <header-name>
        ...
    Access-Control-Expose-Headers: # optional list of HTTP headers
      - <header-name>
      - <header-name>
        ...
```

For an example, see [Tutorial 1](/developer-guide/snowpark-container-services/tutorials/tutorial-1).

When you make an endpoint public, Snowflake allocates a unique hostname to the public endpoint. Snowflake sends incoming requests with that hostname to the service.

If you want to expose multiple service endpoints behind a single host name, you can create a *gateway*. A gateway routes ingress requests to one or more service endpoints, based on the gateway configuration. For more information about gateways and scenarios for creating a gateway, see [Use Gateways to route ingress requests to multiple endpoints](/developer-guide/snowpark-container-services/gateway)

### Ingress connection timeout

Ingress endpoints have a timeout of 90 seconds. If there is no activity on a connection to an ingress endpoint for 90 seconds, Snowflake terminates the connection. If your application needs longer connectivity, use polling or WebSockets.

### Ingress web browser authentication logout

If you’re building a web app that runs as a service, you have the option to allow users to log out from your app by directing them to `/sfc-endpoint/logout`.

After logging out, the user will be required to re-authenticate to Snowflake to access the public endpoint of the service.

### Ingress and web app security

You can create a Snowpark Container Services service for web hosting using the public endpoint support (network ingress). For added
security, Snowflake employs a proxy service to monitor incoming requests from clients to your service and outgoing responses from your
service to the clients. This section explains what the proxy does and how it impacts a service deployed to Snowpark Container Services.

Note

When you test a service locally, you are not using the Snowflake proxy and therefore there will be differences between your experience running
a service locally as opposed to when deployed in Snowpark Container Services. Review this section and update your local setup for better
testing.

For example:

- The proxy does not forward an incoming HTTP request if the request uses a banned HTTP method.
- The proxy sends a 403 response to the client if the Content-Type header in the response indicates that the response contains an executable.

Additionally, the proxy can also inject new headers and alter existing headers in the request and the response, with your container and data security in
mind.

For example, upon receiving a request, your service might send HTML, JavaScript, CSS, and other content for a web page to the client browser
in the response. The web page in the browser is part of your service, acting as the user interface. For security reasons, if your service has restrictions (such as a restriction on making network connections to other sites), you might also want the web page for your service to have the same restrictions.

By default, services have limited permissions to access the internet. The browser should also restrict the client app from accessing the internet and potentially sharing data in most cases. If you set up an External Access Integration (EAI) to allow your service to access `example.com` (see [Configure service egress](#label-working-with-services-jobs-egress)), the web page for your service should also be able to access `example.com` through your browser.

The Snowflake proxy applies the same network restrictions on the service and the web page by adding a `Content-Security-Policy` (CSP) header in the response. By default, the proxy adds a baseline CSP in the
response to protect against common security threats. Browser security is a best effort to balance functionality with security, it is a shared responsibility to ensure this baseline is appropriate for your use case. In addition, if your service is configured to use an EAI, the proxy
applies the same network rules from the EAI to the CSP for the web page. This CSP enables the web page in the browser to access the same sites that the service can access.

Snowflake provides CORS support which you configure in the service specification.

The Snowflake proxy returns the CORS settings defined in the service specification. Note that the proxy removes any CORS headers returned by the service.

The following CORS headers are set by default:

- `Access-Control-Expose-Headers` header always reports the following header names, in addition to headers configured in the service specification for the endpoint.

  - `X-Frame-Options`
  - `Cross-Origin-Opener-Policy`
  - `Cross-Origin-Resource-Policy`
  - `X-Content-Type-Options`
  - `Cross-Origin-Embedder-Policy`
  - `Content-Security-Policy-Report-Only`
  - `Content-Security-Policy`
- `Access-Control-Max-Age` is set to two hours.
- `Access-Control-Allow-Credentials` is set to true.

In addition, Snowflake sets the `Vary` header with the value `Origin` to indicate to the browser that based on the value of the `Origin`, the value to `Access-Control-Allow-Origin` might be different.

The `Authorization` header is required to make the CORS request. You can specify a programmatic access token (PAT) in this header (`Authorization: "Snowflake Token=\"${patToken}\""`). For information on generating a programmatic access token, see [Using programmatic access tokens for authentication](/user-guide/programmatic-access-tokens).

The following sections explain how the Snowflake proxy handles incoming requests for your service and modifies the outgoing responses from your service to the clients.

#### Requests incoming to the service

When a request arrives, the proxy does the following before forwarding the request to the service:

- **Incoming requests with banned HTTP methods:** If an incoming HTTP request uses any of the following banned HTTP methods, the proxy does not forward the request to your service:

  - `TRACE`
  - `CONNECT`
- **Incoming requests header scrubbing:** Snowflake proxy removes the following request headers if present:

  - `X-SF-SPCS-Authorization`
  - `Authorization`: Only removed if it contains a Snowflake token; otherwise, it is passed through to your service.

#### Responses outgoing to the clients

The Snowflake proxy applies these modifications to the response sent by your service before forwarding the response to the client.

- **Header Scrubbing:** Snowflake proxy removes these response headers, if present:

  - `X-XSS-Protection`
  - `Server`
  - `X-Powered-By`
  - `Public-Key-Pins`
- **CORS headers manipulation:** See [Ingress and CORS considerations](#label-additional-considerations-ingress-cors).
- **Content-Type response header:** If your service response includes the Content-Type header with any of the following MIME type values
  (that indicate an executable), Snowflake proxy does not forward that response to the client. Instead, the proxy sends a `403 Forbidden`
  response.

  - `application/x-msdownload`: Microsoft executable.
  - `application/exe`: Generic executable.
  - `application/x-exe`: Another generic executable.
  - `application/dos-exe`: DOS executable.
  - `application/x-winexe`: Windows executable.
  - `application/msdos-windows`: MS-DOS Windows executable.
  - `application/x-msdos-program`: MS-DOS executable.
  - `application/x-sh`: Unix shell script.
  - `application/x-bsh`: Bourne shell script.
  - `application/x-csh`: C shell script.
  - `application/x-tcsh`: Tcsh shell script.
  - `application/batch`: Windows batch file.
- **X-Frame-Options response header:** To prevent clickjacking attacks, the Snowflake proxy sets this response header to `DENY`, preventing other web pages from using an iframe to the web page for your service.
- **Cross-Origin-Opener-Policy (COOP) response header:** Snowflake sets the COOP response header to `same-origin` to prevent referring cross-origin windows from accessing your service tab.
- **Cross-Origin-Resource-Policy (CORP) response header:** Snowflake sets the CORP header to `same-origin` to prevent external sites from loading resources exposed by the ingress endpoint (for example, in an iframe).
- **X-Content-Type-Options response header:** Snowflake proxy sets this header to `nosniff` to ensure the clients do not change the MIME
  type stated in the response by your service.
- **Cross-Origin-Embedder-Policy (COEP) response header:** Snowflake proxy sets the COEP response header to `credentialless`, which means
  when loading a cross-origin object such as an image or a script, if the remote object does not support Cross-Origin Resource Sharing (CORS) protocol, Snowflake does not send the credentials when loading it.
- **Content-Security-Policy-Report-Only response header:** Snowflake proxy replaces this response header with a new value directing
  the client to send the CSP reports to Snowflake.
- **Content-Security-Policy (CSP) response header:** By default the Snowflake proxy adds the following baseline CSP to protect against common
  web attacks.

  Copy code

  ```
  default-src 'self' 'unsafe-inline' 'unsafe-eval' blob: data:; object-src 'none'; connect-src 'self'; frame-ancestors 'self';
  ```

  There are two content security policy considerations:

  - In addition to the baseline content security policy that proxy adds, the service itself can explicitly add a CSP in the response. A
    service might choose to enhance security by adding a stricter CSP. For example, a service might add the following CSP to allow scripts only from `self`.

    Copy code

    ```
    script-src 'self'
    ```

    In the resulting response sent to the client, there will be two CSP headers. Upon receiving the response, the client browsers then apply
    the strictest content security policy that includes the additional restrictions specified by each policy.
  - If you configure an External Access Integration (EAI) to allow your service to access an external site
    ([Configure service egress](#label-working-with-services-jobs-egress)), the Snowflake proxy creates a CSP that allows your web page to access that site. For example, suppose a
    network rule associated with an EAI allows your service egress access to `example.com`. Then, Snowflake proxy adds this CSP response header:

    Copy code

    ```
    default-src 'self' 'unsafe-inline' 'unsafe-eval' http://example.com https://example.com blob: data:; object-src 'none'; connect-src 'self' http://example.com https://example.com wss://example.com; frame-ancestors 'self';
    ```

    Browsers honor the content access policy received in the response. In this example, browsers allow the app access to `example.com` but not other sites.

### Ingress and CORS considerations

By default, browsers block web apps hosted on one server from sending requests to another server with a different hostname. For instance, if you host a web app outside Snowpark Container Services that needs to interact with a backend service deployed within Snowpark Container Services, this restriction applies.

CORS (Cross-Origin Resource Sharing) enables a Snowpark Container Services service to tell the browsers to allow requests from web apps hosted outside its environment. You can configure each public endpoint to specify how it responds to both CORS preflight requests and standard requests.

Snowflake proxy always overrides the following response headers:

- `Access-Control-Allow-Origin`
- `Access-Control-Allow-Methods`
- `Access-Control-Allow-Headers`
- `Access-Control-Expose-Headers`
- `Access-Control-Max-Age`
- `Access-Control-Allow-Credentials`

The Snowflake proxy does not include any of these CORS headers in the response when either of the following is true:

- CORS is not configured for the service endpoint. That is, there no `corsSettings` in the service specification
- CORS is configured for the service endpoint, but the `Origin` header in the request doesn’t match the specified `Access-Control-Allow-Origin` field in the service specification

In the service specification, you can configure CORS settings for each public endpoint. When the `origin` header in the request matches the `Access-Control-Allow-Origin` field specified for the endpoint in the specification, the proxy includes in the response the CORS headers defined in the specification, with the following adjustments:

- `Access-Control-Allow-Origin`: Returns the `Origin` header from the request.
- `Access-Control-Expose-Headers`: Merges the list of allowed headers you configured with these always-exposed headers: `X-Frame-Options`, `Cross-Origin-Opener-Policy`, `Cross-Origin-Resource-Policy`,
  `X-Content-Type-Options`, `Cross-Origin-Embedder-Policy`, `Content-Security-Policy-Report-Only`, `Content-Security-Policy`.
- `Access-Control-Max-Age`: Is set to two hours.
- `Access-Control-Allow-Credentials`: Is set to true.

### Ingress and your Identity Provider (IdP) considerations

An account administrator can configure all ingress URLs to redirect to your identity provider (IdP) when an
unauthenticated viewer accesses an app. This process eliminates the additional customer step of selecting the IdP
from the login page, resulting in fewer clicks and a smoother login flow.

To redirect unauthenticated users from ingress URLs to your IdP, use the [ALTER ACCOUNT](/sql-reference/sql/alter-account)
SQL command to set the `LOGIN_IDP_REDIRECT` account property to include `SPCS`:

Copy code

```
ALTER ACCOUNT SET LOGIN_IDP_REDIRECT = (SPCS = <your_security_integration>);
```

For a full overview of `LOGIN_IDP_REDIRECT`, including the procedure
for reaching the Snowflake sign-in page when the IdP is unavailable,
see [Automatically redirecting users to your identity provider](/user-guide/admin-security-fed-auth-idp-redirect).

For more information about configuring your Snowflake account to use an IdP, see the following topics:

- [Configuring Snowflake to use federated authentication](/user-guide/admin-security-fed-auth-configure-snowflake)
- [Configuring an identity provider (IdP) for Snowflake](/user-guide/admin-security-fed-auth-security-integration)

### Ingress and SSO considerations

When accessing the public endpoint from the internet, you might find that username/password authentication works, but SSO results in a blank page or the error: “OAuth client integration with the given client ID is not found.”

This happens when you’re using the old style of federated authentication (SSO) with Snowflake instead of the newer security integration version as explained in [Configuring SAML 2.0 federated authentication](/user-guide/admin-security-fed-auth-security-integration). Do the following to verify:

1. Run the following query:

   Copy code

   ```
   SHOW PARAMETERS LIKE 'SAML_IDENTITY_PROVIDER' IN ACCOUNT;
   ```

   If you have this parameter set, then at some point you were using the old-style federated authentication.
2. If the preceding parameter was set, run the following query
   to see if you have a SAML security integration:

   Copy code

   ```
   SHOW INTEGRATIONS
     ->> SELECT * FROM $1 WHERE "type" = 'SAML2';
   ```

   If you don’t have any integrations of the SAML2 type, then you’re using the old style federated authentication.

In this case, the solution is to migrate from the old-style federated authentication to the new integration-style federated authentication. For more information, see [Migrating to a SAML2 security integration](/user-guide/admin-security-fed-auth-configure-snowflake).

## Configure service egress

Your application code might require access to the internet. By default, application containers don’t have
permission to access the internet. You need to enable internet access using
[External Access Integrations (EAIs)](/developer-guide/external-network-access/external-network-access-overview).

Typically, you want an account administrator to create EAIs to manage external access allowed from services (including job services). Account
administrators can then grant EAI usage to specific roles that developers use to run services.

The following example outlines the steps in creating an EAI that allows egress traffic to specific destinations specified using
network rules. You then refer to the EAI when creating a service to allow requests to specific internet destinations.

**Example**

Suppose you want your application code to send requests to the following destinations:

- HTTPS requests to translation.googleapis.com
- HTTP and HTTPS requests to google.com

Follow these steps to enable your service to access these domains on the internet:

1. Create an External Access Integration (EAI). This requires appropriate permissions. For example, you can use ACCOUNTADMIN role
   to create an EAI. This is a two-step process:

   1. Use the [CREATE NETWORK RULE](/sql-reference/sql/create-network-rule) command to create one or more egress network rules listing external
      destinations you want to allow access to. You can accomplish this example with one network rule, but for illustration, we
      create two network rules:

      1. Create a network rule named `translate_network_rule`:

         Copy code

         ```
         CREATE OR REPLACE NETWORK RULE translate_network_rule
           MODE = EGRESS
           TYPE = HOST_PORT
           VALUE_LIST = ('translation.googleapis.com');
         ```

         This rule allows TCP connections to the `translation.googleapis.com` destination. The domain in the VALUE\_LIST
         property does not specify the optional port number, so the default port 443 (HTTPS) is assumed. This allows your
         application to connect to any URL that starts with `https://translation.googleapis.com/`.
      2. Create a network rule named `google_network_rule`:

         Copy code

         ```
         CREATE OR REPLACE NETWORK RULE google_network_rule
           MODE = EGRESS
           TYPE = HOST_PORT
           VALUE_LIST = ('google.com:80', 'google.com:443');
         ```

         This allows your application to connect to any URL that starts with `http://google.com/` or
         `https://google.com/`.

      Note

      For the `VALUE_LIST` parameter, you must provide a full host name. Wildcards (for example, `*.googleapis.com`) are not supported.

      Snowpark Container Services supports only the network rules that allow ports 22, 80, 443, and 1024+. If a network rule
      referenced allows access to other ports, creation of the service will fail. Contact your account representative if you
      require use of additional ports.

      Note

      To allow your service to send HTTP or HTTPS requests to any destination on the internet, you specify “0.0.0.0”
      as the domain in the VALUE\_LIST property. The following network rule allows sending both “HTTP” and “HTTPS” requests
      anywhere on the internet. Only ports 80 or 443 are supported with “0.0.0.0”.

      Copy code

      ```
      CREATE NETWORK RULE allow_all_rule
        TYPE = 'HOST_PORT'
        MODE= 'EGRESS'
        VALUE_LIST = ('0.0.0.0:443','0.0.0.0:80');
      ```
   2. [Create an external access integration (EAI)](/developer-guide/external-network-access/creating-using-external-network-access)
      that specifies that the preceding two egress network rules are allowed:

      Copy code

      ```
      CREATE EXTERNAL ACCESS INTEGRATION google_apis_access_integration
        ALLOWED_NETWORK_RULES = (translate_network_rule, google_network_rule)
        ENABLED = true;
      ```

      Now the account admin can grant usage of the integration to developers to allow them to run a service that can access
      specific destinations on the internet.

      Copy code

      ```
      GRANT USAGE ON INTEGRATION google_apis_access_integration TO ROLE test_role;
      ```
2. Create the service by providing the EAI as shown in the following examples. The owner role that is creating the service needs the USAGE privilege on the EAI and READ privilege on the secrets referenced. Note that you cannot use the
   ACCOUNTADMIN role to create a service.

   - Create a service:

     Copy code

     ```
     USE ROLE test_role;

     CREATE SERVICE eai_service
       IN COMPUTE POOL MYPOOL
       EXTERNAL_ACCESS_INTEGRATIONS = (GOOGLE_APIS_ACCESS_INTEGRATION)
       FROM SPECIFICATION
       $$
       spec:
         containers:
     - name: main
       image: /db/data_schema/tutorial_repository/my_echo_service_image:tutorial
       env:
         TEST_FILE_STAGE: source_stage/test_file
       args:
         - read_secret.py
         endpoints:
     - name: read
       port: 8080
       $$;
     ```

     This example CREATE SERVICE request uses an inline service specification and specifies the optional
     EXTERNAL\_ACCESS\_INTEGRATIONS property to include the EAI. The EAI specifies the network rules that allow egress traffic
     from the service to the specific destinations.
   - Execute a job service:

     Copy code

     ```
     EXECUTE JOB SERVICE
       IN COMPUTE POOL tt_cp
       NAME = example_job_service
       EXTERNAL_ACCESS_INTEGRATIONS = (GOOGLE_APIS_ACCESS_INTEGRATION)
       FROM SPECIFICATION $$
       spec:
         container:
         - name: curl
     image: /tutorial_db/data_schema/tutorial_repo/alpine-curl:latest
     command:
     - "curl"
     - "http://google.com/"
       $$;
     ```

     This example EXECUTE JOB SERVICE command specifies inline specification and the optional EXTERNAL\_ACCESS\_INTEGRATIONS property
     to include the EAI. This allows egress traffic from the job to destinations specified in the network rules the EAI allows.

### Network egress using private connectivity

Instead of routing network egress via the public internet, you might opt to direct your service’s egress traffic through a
[private connectivity endpoint](/user-guide/private-connectivity-outbound).

You first need to create the private connectivity endpoint in your Snowflake account. Then configure a network rule to permit outgoing
traffic to use [private connectivity](/user-guide/private-connectivity-outbound). The process for setting up an External Access
Integration (EAI) remains the same as described in the preceding section.

Note

Private communication requires that both Snowflake and the customer’s cloud account use the same cloud provider and same region.

For example, if you want to enable your service’s outbound internet access to an Amazon S3 bucket via private connectivity, you do the
following:

1. Enable the private link connectivity for the self-maintained endpoint service (Amazon S3). For step-by-step instructions, see
   [AWS Private Link for Amazon S3](https://docs.aws.amazon.com/AmazonS3/latest/userguide/privatelink-interface-endpoints.html).
2. Call the [SYSTEM$PROVISION\_PRIVATELINK\_ENDPOINT](/sql-reference/functions/system_provision_privatelink_endpoint) system function to provision a private connectivity
   endpoint in your Snowflake VNet. This enables Snowflake to connect to the external service (in this example, Amazon S3) using private
   connectivity.

   Copy code

   ```
   USE ROLE ACCOUNTADMIN;

   SELECT SYSTEM$PROVISION_PRIVATELINK_ENDPOINT(
     'com.amazonaws.us-west-2.s3',
     '*.s3.us-west-2.amazonaws.com'
   );
   ```
3. In the cloud provider account, approve the endpoint. In this example, for Amazon AWS, see
   [Accept or reject connection requests](https://docs.aws.amazon.com/vpc/latest/privatelink/configure-endpoint-service.html#accept-reject-connection-requests)
   in the AWS documentation. Also, to approve the endpoint in Azure, see the
   [Azure documentation](https://learn.microsoft.com/en-us/azure/private-link/manage-private-endpoint?tabs=manage-private-link-powershell#private-endpoint-connections).
4. Use the [CREATE NETWORK RULE](/sql-reference/sql/create-network-rule) command to create an egress network rule specifying the external destinations
   that you want to allow access to.

   Copy code

   ```
   CREATE OR REPLACE NETWORK RULE private_link_network_rule
     MODE = EGRESS
     TYPE = PRIVATE_HOST_PORT
     VALUE_LIST = ('<bucket-name>.s3.us-west-2.amazonaws.com');
   ```

   The TYPE parameter value is set to PRIVATE\_HOST\_PORT. It indicates that the network rule allows outgoing network traffic to use
   [private connectivity](/user-guide/private-connectivity-outbound).
5. The rest of the steps to create an EAI and use it to create a service are the same as explained in the preceding section
   (see [Configure service egress](#label-working-with-services-jobs-egress)).

For more information about working with private connectivity endpoints, see the following:

- [Manage private connectivity endpoints: AWS](/user-guide/private-manage-endpoints-aws)
- [Manage private connectivity endpoints: Azure](/user-guide/private-manage-endpoints-azure)
- [Manage private connectivity endpoints: Google Cloud](/user-guide/private-manage-endpoints-gcp)

## Considerations when Configuring communications between services

There are two considerations:

- **Communications between containers of a service instance:** If a service instance runs multiple containers, these containers
  can communicate with each other over localhost (there is no need to define endpoints in the service specification).
- **Communication between containers across multiple services or multiple service instances:** Containers belonging to
  different services (or different instances of the same service) can communicate using endpoints defined in specification files.
  For more information, see [Service-to-service communications](/developer-guide/snowpark-container-services/working-with-services#label-snowpark-containers-service-communicating-service-to-service).
