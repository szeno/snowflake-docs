# Jun 1, 2026: Restricted caller’s rights in Streamlit in Snowflake (*General availability*)

With this release, restricted caller’s rights in Streamlit in Snowflake is now generally available. This feature requires Streamlit version 1.53.1 or later.

By default, Streamlit in Snowflake apps run with the privileges of the app owner. With restricted caller’s
rights, you can configure a container-runtime app to run with a limited set of the
caller’s privileges instead, giving viewers access only to the data their own role can see.

For more information, see [Restricted caller’s rights and Streamlit in Snowflake](/developer-guide/streamlit/features/restricted-callers-rights).
