# Mar 09, 2026: Streamlit in Snowflake container runtime and secrets support (*General availability*)

The Streamlit in Snowflake container runtime is now generally available. Container runtimes run your Streamlit in Snowflake apps on
Snowpark Container Services compute pools, providing access to GPUs, broader Python package support, and long-running
services without sleep timers.

This release also includes general availability for the following container-runtime features:

- **Secrets**: Use `st.secrets` to securely access Snowflake secrets in your container-runtime apps.
  Secrets are also automatically mapped to environment variables.
- **Sharing**: Share container-runtime apps using app-viewer URLs without the Snowsight interface.
- **Logging and tracing**: Container runtimes automatically capture standard output and standard error
  from your apps.

Container runtimes are available in all commercial regions. Government and China regions are not supported.

For more information, see:

- [Runtime environments for Streamlit apps](/developer-guide/streamlit/app-development/runtime-environments)
- [Manage secrets and configure your Streamlit app](/developer-guide/streamlit/app-development/secrets-and-configuration)
- [Sharing Streamlit in Snowflake apps](/developer-guide/streamlit/features/sharing-streamlit-apps)
- [Logging and tracing for Streamlit in Snowflake](/developer-guide/streamlit/features/logging-tracing)
