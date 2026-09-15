# Retrieving the URL for a Streamlit app

## Prerequisites

- The Streamlit app must already be uploaded to a stage in the connection you are currently using.
- Your current ROLE must have access to the app.

## How to get the URL for a deployed Streamlit app

The `snow streamlit get-url` command returns a URL for a deployed Streamlit app that you can then use to open the app in a browser.

To get an app URL, do the following:

1. Ensure your connection specifies the database and schema where your app is deployed.
2. Enter a command similar to the following:

   Copy code

   ```
   snow streamlit get-url my_streamlit_app
   ```

   ```
   https://snowflake.com/provider-deduced-from-connection/#/streamlit-apps/DB.SCHEMA.MY_STREAMLIT_APP
   ```

You can use the command to return the URL and open the app automatically in your default browser by using the `--open` option, similar to the following:

Copy code

```
snow streamlit get-url my_streamlit_app --open
```

## How to resolve common errors

- If the command fails because your ROLE does not have access to the Streamlit app, try the following:

  - Verify you are using the same ROLE in your browser that was used to deploy the app.
  - Switch to a ROLE that has access to the app. If you don’t have access to the ROLE used to create the app, the app developer can grant access to another ROLE with the `snow streamlit share` command.
- If the command fails because it could not find the Streamlit app, try the following:

  - Check the app name.
  - Verify you generated the URL using the same connection (host, account, database, and schema) that was used to deploy the app.
  - Ensure the database and schema are correct. If you specified the database and schema as a fully-qualified name, it overrides the values for them in the connection.
