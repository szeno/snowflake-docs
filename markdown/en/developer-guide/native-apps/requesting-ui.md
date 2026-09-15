# Create a user interface to request privileges and references

Feature — Generally Available

The Snowflake Native App Framework is generally available on supported cloud platforms. For additional information, see
[Support for private connectivity, VPS, and government regions](/developer-guide/native-apps/limitations#label-native-apps-supported-clouds).

This topic describes how you, as a provider, create a user interface using Streamlit and the
Snowsight to allow consumers to grant privileges and create references for an installed
Snowflake Native App. To access Snowflake privileges and references from a Streamlit program, the Snowflake Native App Framework
provides the Python Permission SDK.

See [Python Permission SDK reference](/developer-guide/native-apps/requesting-permission-sdk-ref) for information on the methods in the Python Permission SDK.

## About privileges and references

For general information on requesting privileges and references from the consumer using the
Snowflake Native App Framework, refer to [Create and access objects in a consumer account](/developer-guide/native-apps/requesting-about).

## About the Python Permission SDK

The Snowflake Native App Framework provides the Python Permission SDK which allows a provider to do the following within a
Snowflake Native App:

- Check for account level privileges.
- Request global privileges that are listed in the manifest file.
- Request references to objects and their corresponding object level privileges as defined
  in the manifest file.
- Request privileged actions, for example creating an API integration or creating a share.

Using the Python Permission SDK, Snowsight displays the access requests in the
**Security** tab of the installed Snowflake Native App.

See [Python Permission SDK reference](/developer-guide/native-apps/requesting-permission-sdk-ref) for information on the methods in the Python Permission SDK.

## Workflow for creating an interface to approve privileges and bind references

The following general workflow outlines the steps required to implement a Streamlit app to
request grants for privileges and references from the consumer.

1. Create an application package.
2. In the manifest file, specify the privileges and define the references required for the Snowflake Native App.
3. Add a Streamlit app to your application package.
4. Add an `environment.yml` file to your application package.

   Note

   The `environment.yml` file must be in the same directory as main Streamlit file
   used to implement the Snowsight interface.
5. Add the `snowflake-native-apps-permission` library as a dependency.
6. Import the `snowflake.permissions` library in your Streamlit app.
7. Add functions to your Streamlit app that call the functions provided by the SDK.

## Add the Python Permission SDK to your Streamlit environment

To use the Python Permission SDK in a Streamlit app, add the `snowflake-native-apps-permission`
package as a dependency in your `environment.yml` file as shown in the following example:

Copy code

```
name: sf_env
channels:
- snowflake
dependencies:
- snowflake-native-apps-permission
```

## Import the Python Permission SDK in a Streamlit app

To import the Python Permission SDK into your Streamlit app, include the following import statement in
your app:

Copy code

```
import snowflake.permissions as permissions
```

## Request privileges from the consumer

The following examples show how to perform different tasks using the Python Permission SDK.

### Check Account Level Privileges

This example shows how to use the
[get\_held\_account\_privileges()](/developer-guide/native-apps/requesting-permission-sdk-ref#label-native-apps-get-held-account-privileges) method of the
Python Permission SDK to check if permissions declared in the manifest file are granted to the installed Snowflake Native App.

For example, if a Snowflake Native App needs to create a database outside of the APPLICATION object, a provider
can define the reference in the manifest file as follows:

Copy code

```
privileges:
- CREATE DATABASE:
    description: "Creation of ingestion (required) and audit databases"
```

Using the Python Permission SDK, you can use the [get\_held\_account\_privileges()](/developer-guide/native-apps/requesting-permission-sdk-ref#label-native-apps-get-held-account-privileges)
method to obtain a list of privileges that have been granted to the Snowflake Native App.

Copy code

```
import streamlit as st
import snowflake.permissions as permissions
...
if not permissions.get_held_account_privileges(["CREATE DATABASE"]):
    st.error("The app needs CREATE DB privilege to replicate data")
```

This example calls the [get\_held\_account\_privileges()](/developer-guide/native-apps/requesting-permission-sdk-ref#label-native-apps-get-held-account-privileges) function, passing the
CREATE DATABASE permission as a parameter. A provider can use the [get\_held\_account\_privileges()](/developer-guide/native-apps/requesting-permission-sdk-ref#label-native-apps-get-held-account-privileges)
function to wait until the consumer grants the required privileges to the app.

Note

Only privileges defined in the manifest file are valid arguments to
[get\_held\_account\_privileges()](/developer-guide/native-apps/requesting-permission-sdk-ref#label-native-apps-get-held-account-privileges). Passing other arguments results in an error.

## Request privileged actions from the consumer

Providers can use the Python Permission SDK to request privileged actions required by the Snowflake Native App.

For example, to request an API integration that allows the Snowflake Native App to connect to a
ServiceNow instance, a provider would define the API integration in the manifest file:

Copy code

```
references:
- servicenow_api_integration:
  label: "API INTEGRATION for ServiceNow communication"
  description: "An integration required in order to support extraction and visualization of ServiceNow data."
  privileges:
    - USAGE
  object_type: API Integration
  register_callback: config.register_reference
```

Next, in the Streamlit app, the provider calls the [request\_reference()](/developer-guide/native-apps/requesting-permission-sdk-ref#label-native-apps-request-reference) method
to request the USAGE privilege on the API integration as shown in the following example:

Copy code

```
permissions.request_reference("servicenow_api_integration")
```
