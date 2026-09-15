# Creating an external function for GCP using the Google Cloud console

These topics provide detailed instructions for using the Google Cloud Console user interface to create an external function hosted on
GCP (Google Cloud Platform). You can use these instructions either to create the sample external function provided by Snowflake or as
a guide to create your own external function.

In these topics, you will learn how to:

- Create a basic Google Cloud Function as a remote service and a Google Cloud API Gateway as a proxy service.
- Create an API integration and the external function itself in Snowflake.
- Secure the API Gateway through a security policy.

These topics assume that you are already familiar with the Google Cloud Console. They describe the general steps that you need to complete,
but do not describe the Console in detail.

Tip

Google also provides a command-line interface that you can use for many of these steps. For more details, see the GCP
[gcloud documentation](https://cloud.google.com/api-gateway/docs/quickstart).

**See also:**

- [Planning an external function for GCP](/sql-reference/external-functions-creating-gcp-planning)

**Steps:**

- [Step 1: Create the remote service (Google Cloud Function) in the console](/sql-reference/external-functions-creating-gcp-ui-remote-service)
- [Step 2: Create the proxy service (Google Cloud API Gateway) in the console](/sql-reference/external-functions-creating-gcp-ui-proxy-service)
- [Step 3: Create the API integration for GCP in Snowflake](/sql-reference/external-functions-creating-gcp-common-api-integration)
- [Step 4: Create the external function for GCP in Snowflake](/sql-reference/external-functions-creating-gcp-common-ext-function)
- [Step 5: Create a GCP security policy for the proxy service in the console](/sql-reference/external-functions-creating-gcp-ui-security-policy)
