# Introduction to external functions

This topic describes external functions, which call executable code that is developed, maintained, stored, and
executed outside Snowflake.

This topic helps you:

- Understand what an external function is.
- Decide whether an external function is the best way for you to implement a
  [UDF (user-defined function).](/developer-guide/udf/udf-overview)
- Choose the cloud platform for your external function.

Note

When using external functions in China, use the [syntax and workflow described for AWS](/sql-reference/external-functions-creating-aws).

## What is an external function?

An *external function* calls code that is executed outside Snowflake.

The remotely executed code is known as a *remote service*.

Information sent to a remote service is usually relayed through a *proxy service*.

Snowflake stores security-related external function information in an *API integration*.

The diagram below shows the basic information flow from a client program, through Snowflake, and to the remote
service:

![](/static/images/external-functions-overview-07.png)

Each of the key components is described in more detail below.

External Function:
:   An external function is a type of [UDF](/developer-guide/udf/udf-overview).
    Unlike other UDFs, an external function does not contain its own code;
    instead, the external function calls code that is stored and executed outside Snowflake.

    Inside Snowflake, the external function is stored as a database object that contains information that
    Snowflake uses to call the remote service. This stored information includes the URL of the
    [proxy service](/sql-reference/external-functions-introduction#label-external-functions-introduction-miniglossary-proxy-service)
    that relays information to and from the remote service. This information is specified as
    part of the [CREATE EXTERNAL FUNCTION](/sql-reference/sql/create-external-function) command.

    The database object that represents the external function is created in a specific database and schema. The
    external function can be called using dot notation to represent the fully-qualified name. For example:

    Copy code

    ```
    select my_database.my_schema.my_external_function(col1) from table1;
    ```

Remote Service:
:   The remotely executed code is known as a remote service.

    The remote service must act like a function. For example, it must return a value.

    Snowflake supports *scalar* external functions; the remote service must return exactly one row for each
    row received.

    To be called by the Snowflake external function feature, the remote service must:

    - Accept [JSON](https://www.json.org) inputs and return JSON outputs. (For more information about
      Snowflake-compatible HTTP headers and JSON formatted data, see [Remote service input and output data formats](/sql-reference/external-functions-data-format#label-external-functions-data-format).)
    - Expose an HTTPS endpoint.

    For example, a remote service can be implemented as:

    - An AWS Lambda function.
    - A Microsoft Azure Function.
    - An HTTPS server (e.g. Node.js) running on an EC2 instance.

Proxy Service:
:   Snowflake does not call a
    [remote service](/sql-reference/external-functions-introduction#label-external-functions-introduction-miniglossary-remote-service) directly.
    Instead, Snowflake calls a proxy service, which relays the data to the remote service.

    The proxy service can increase security by authenticating requests to the remote service.

    The proxy service can support subscription-based billing for a remote service. For example, the proxy service
    can verify that a caller to the remote service is a paid subscriber.

    The proxy service also relays the response from the remote service back to Snowflake.

    Examples of proxy services include:

    - Amazon API Gateway.
    - Microsoft Azure API Management service.

API Integration:
:   An *integration* is a Snowflake object that provides an interface between Snowflake and third-party services.
    An API integration stores information, such as security information, that is needed to work with a proxy service
    or remote service.

    An API integration is created with the [CREATE API INTEGRATION](/sql-reference/sql/create-api-integration) command.

Users can write and call their own remote services, or call remote services written by third parties. These remote
services can be written using any HTTP server stack, including cloud serverless compute services such as AWS Lambda.

From the perspective of a user running a SQL statement, an external function behaves like any other
[UDF](/developer-guide/udf/udf-overview) . External functions follow these rules:

- External functions return a value.
- External functions can accept parameters.
- An external function can appear in any clause of a SQL statement in which other types of
  [UDF](/developer-guide/udf/udf-overview) can appear. For example:

  Copy code

  ```
  select my_external_function_2(column_1, column_2)
   from table_1;

  select col1
   from table_1
   where my_external_function_3(col2) < 0;

  create view view1 (col1) as
   select my_external_function_5(col1)
       from table9;
  ```
- An external function can be part of a more complex expression:

  Copy code

  ```
  select upper(zipcode_to_city_external_function(zipcode))
    from address_table;
  ```
- The returned value can be a compound value, such as a VARIANT that contains JSON.
- External functions can be overloaded; two different functions can have the same name
  but different signatures (different numbers or data types of input parameters).

## How external functions work

Snowflake does not call a remote service directly. Instead, Snowflake calls the remote service through a cloud
provider’s native HTTPS proxy service, for example API Gateway on AWS.

The main steps to call an external function are:

1. A user’s client program passes Snowflake a SQL statement that calls an external function.
2. When evaluating the external function as part of the query execution, Snowflake reads the external function
   definition and the corresponding API integration information.

   - The information from the external function definition includes:

     - The URL of the proxy service.
     - The name of the corresponding API integration.
   - The information from the API integration includes:

     - The proxy service resource to use. The resource contains information about the remote service, such as the
       location of that service.
     - The authentication information for that proxy service resource.

   Snowflake then composes an HTTP POST command that includes:

   - The data to be processed. This data is in JSON format.
   - HTTP header information. (Details are documented in [CREATE EXTERNAL FUNCTION](/sql-reference/sql/create-external-function).)
   - Authentication information from the API integration.

   Snowflake then sends the POST request to the proxy service.
3. The proxy service receives the POST and then processes and forwards the request to the actual remote service.
   You can loosely think of the proxy service and resource as a “relay function” that calls the remote service.
4. The remote service processes the data and returns the result, which is passed back through the chain to the
   original SQL statement.
5. If the remote service responds with an HTTP code to signal
   [asynchronous](/sql-reference/external-functions-implementation#label-external-functions-introduction-miniglossary-asynchronous) processing, then Snowflake
   sends one or more HTTP GET requests to retrieve the result from the remote service. Snowflake continues to send GET
   requests as long as it receives the response code to keep requesting, or until the external function times out
   or returns an error.

Typically, when a query has a large number of rows to send to a remote service, the rows are split into
batches. Batches typically allow more parallelism and faster queries. In some cases, batches reduce
overloading of the remote service.

A remote service returns 1 batch of rows for each batch received. For a scalar external function, the
number of rows in the returned batch is equal to the number of rows in the received batch.

Each batch has a unique batch ID, which is included in each request sent from Snowflake to the remote service.

Retry operations (e.g. due to timeouts) are typically done at the batch level.

## Advantages of external functions

External functions have the following advantages over other [UDFs](/developer-guide/udf/udf-overview):

- The code for the remote service can be written in languages that other UDFs cannot be written in,
  including:

  - Go
  - C#
- Remote services can use functions and libraries that can’t be accessed by internal UDFs. For example,
  remote services can interface with commercially available third-party libraries,
  such as machine-learning scoring libraries.
- Developers can write remote services that can be called both from Snowflake and from other software
  written to use the same interface.

## Limitations of external functions

External functions have the following limitations, which can be loosely grouped into creation-time limitations and
execution-time limitations.

### Creation-time limitations and requirements

- Before an external function can be called the first time, an administrator must do
  some configuration work. This work requires knowledge of the cloud platform (e.g. AWS or Microsoft Azure),
  especially about security.
- Snowflake calls remote services indirectly through a cloud HTTP proxy service (such as
  the Amazon API Gateway), so the remote service for an external function must be
  callable from a proxy service. Fortunately, almost any function that can act as
  an HTTPS endpoint can be accessed as an external function via a proxy service.
  The function author must program the proxy service to call the remote service
  (e.g. a function running on AWS Lambda).
- Some cloud platforms might have specific requirements. For example, on AWS, external functions
  require regional endpoints or private endpoints. For more details, see
  [Supported platforms](#label-external-functions-supported-platforms). For more details about Amazon API Gateway regional and
  private endpoints, see [Choosing your endpoint type: Regional endpoint vs. Private endpoint](/sql-reference/external-functions-creating-aws-planning#label-external-functions-aws-endpoint-type).
- Only functions, not stored procedures, can be written using the external functions feature.
- [Future grants](/sql-reference/sql/grant-privilege#label-grant-privilege-schema-future-grants) of privileges on external functions are not supported.

### Execution-time limitations and issues

- Because the remote service is opaque to Snowflake, the optimizer might not be able to perform
  some optimizations that it could perform for equivalent functions.
- External functions have more overhead than functions (both built-in functions and internal UDFs) and
  usually execute more slowly.
- Currently, external functions must be scalar functions. A scalar external function returns a single value for each
  input row.
- Currently, external functions cannot be shared with data consumers via
  [Secure Data Sharing](/user-guide/data-sharing-gs).
- The maximum response size per batch is 10MB.
- External functions cannot be used in the following situations:

  - As part of a database object (e.g. table, view, UDF, or masking policy) shared
    via [Secure Data Sharing](/user-guide/data-sharing-intro). For example, you cannot create a shared view that uses an
    external function. The following is not supported:

    Copy code

    ```
    CREATE VIEW my_shared_view AS SELECT my_external_function(x) ...;
    CREATE SHARE things_to_share;
    ...
    GRANT SELECT ON VIEW my_shared_view TO SHARE things_to_share;
    ...
    ```
  - A `DEFAULT` clause of a `CREATE TABLE` statement. In other words, the default
    value for a column cannot be an expression that calls an external function.
    If you try to include an external function in a `DEFAULT` clause, then the
    `CREATE TABLE` statement fails.
  - A [COPY transformation](/user-guide/data-load-transform).
- External functions can raise additional security issues. For example, if you call a
  third party’s function, that party could keep copies of the data passed to the function.

## Billing for external functions usage

Using external functions incurs normal costs associated with:

- [Snowflake warehouse usage.](/user-guide/cost-understanding-compute#label-virtual-warehouse-credit-usage)
- [Data transfer.](/user-guide/cost-understanding-data-transfer)

In addition, you might need to pay indirect or third-party charges, including charges by the provider of the remote service. Charges can
vary from vendor to vendor.

Note

Data sent via Amazon API Gateway Private Endpoints incurs AWS PrivateLink charges for both ingress and egress.

## Supported platforms

### Platforms that support calling an external function

In general, an external function can be called from a Snowflake account on any cloud platform that Snowflake supports:

- Amazon Web Services (AWS)
- Microsoft Azure
- Google Cloud Platform (GCP)

Exceptions are listed below:

- An external function accessed through an AWS API Gateway private endpoint can be accessed only from a Snowflake VPC (Virtual Private
  Cloud) on AWS and in the same AWS region. For more details about private endpoints on AWS, see
  [Choosing your endpoint type: Regional endpoint vs. Private endpoint](/sql-reference/external-functions-creating-aws-planning#label-external-functions-aws-endpoint-type).

The SQL syntax for calling an external function is the same on all platforms.

The SQL statements ([CREATE EXTERNAL FUNCTION](/sql-reference/sql/create-external-function) and
[CREATE API INTEGRATION](/sql-reference/sql/create-api-integration)) that configure access to these services
are the same for all platforms. However, the clauses within these statements vary, depending upon the platforms
hosting the proxy service and the remote service.

### Platforms that support creating an external function’s remote service and proxy service

Although an external function can be called from any platform, the external function’s remote service and
proxy service must each be created on specific supported platforms.

In many cases, the platform and account for the remote service are the same as the platform and account for the
proxy service. However, that is not required. For example, a SQL query could call an Azure Function (remote
service) via an AWS API Gateway (proxy service). The SQL query itself could be running on a Snowflake instance
running on GCP.

#### Platforms that support a remote service

You need an HTTP server stack to host the remote service. Any HTTP server stack that can support the remote
service should be compatible with external functions.

To create your remote service, you typically need:

- An account with a cloud platform’s provider (e.g. a Microsoft Azure account to create an Azure Function). This
  account provides storage and compute services for the remote service. This account is separate from your
  Snowflake account.

Snowflake provides instructions for creating a remote service as:

- An AWS Lambda function.
- A Microsoft Azure function.
- A Google Cloud Function.

#### Platforms that support a proxy service

You need an instance of a native HTTP proxy service on a cloud platform.

To configure your proxy service, you typically need:

- An account with a cloud platform’s provider (e.g. an Amazon account to use AWS). This account provides
  storage and compute services for the proxy service. This account is separate from your Snowflake account.
- A cloud platform role that has the privileges required to configure a proxy service.
  This cloud platform role is separate from your Snowflake role(s).

The following HTTPS proxy services are supported:

- Amazon API Gateway.
- Microsoft Azure API Management Service.
- Google Cloud API Gateway.

The sections below contain platform-specific information that users should be aware of before choosing a platform.

### Platform-specific restrictions

AWS:

- This feature supports only regional and private endpoints for the Amazon API Gateway. (For a description of the
  different types of endpoints, see
  [endpoints](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-basic-concept.html) .)
- Snowflake external functions and API integrations do not support
  [AWS custom domains](https://docs.aws.amazon.com/apigateway/latest/developerguide/how-to-custom-domains.html).
  To access an Amazon API Gateway from Snowflake, use the default URL generated by AWS, which looks similar to the following:

  Copy code

  ```
  https://api-id.execute-api.region.amazonaws.com/stage
  ```
