# Nov 20, 2026: Container runtime for Streamlit apps in Snowflake Native Apps (*General availability*)

With this release, the container runtime for Streamlit apps in a Snowflake Native App is now generally
available. Providers can run a Streamlit app inside a Snowflake Native App as a Snowpark Container Services service on a
compute pool that the app creates and owns in the consumer account, instead of on a virtual
warehouse.

A container runtime lets a Streamlit app in a Snowflake Native App do the following:

- Install Python packages from PyPI or another external package index, instead of being limited to
  the Snowflake Anaconda Channel. This requires an external access integration that the consumer
  approves through an app specification.
- Use recent versions of the Streamlit library, including `streamlit-nightly` versions.
- Query consumer data on behalf of the signed-in viewer with restricted caller’s rights.

Consumers install the app as they install any other Snowflake Native App, and they aren’t prompted to
select a warehouse when they open a container-runtime Streamlit app.

For more information, see:

- Provider guide: [Add a Streamlit app](/developer-guide/native-apps/adding-streamlit#label-streamlit-container-runtime-na)
- Runtime comparison: [Runtime environments for Streamlit apps](/developer-guide/streamlit/app-development/runtime-environments)
- SQL reference: [CREATE STREAMLIT](/sql-reference/sql/create-streamlit)
