# September 23, 2026: Container runtime for Streamlit apps in Snowflake Native Apps (*Preview*)

Providers can now run a Streamlit app inside a Snowflake Native App on a container runtime, in preview. The
Streamlit app runs as a Snowpark Container Services service on a compute pool that the app creates and owns in the
consumer account rather than on a virtual warehouse.

A container runtime lets a Streamlit app in a Snowflake Native App do the following:

- Install Python packages from PyPI or another external package index, instead of being limited to
  the Snowflake Anaconda Channel. This requires an external access integration that the consumer
  approves through an app specification.
- Use recent versions of the Streamlit library, including `streamlit-nightly` versions.
- Query consumer data on behalf of the signed-in viewer with restricted caller’s rights.

For migration steps, including compute resources, dependencies, and app code compatibility, see
[Convert a Streamlit app to a container runtime](/developer-guide/native-apps/adding-streamlit#label-streamlit-container-migrate-na).

Consumers install the app with the same command as before, and they’re no longer prompted to select
a warehouse when they open a container-runtime Streamlit app.

For more information, see:

- Provider guide: [Add a Streamlit app](/developer-guide/native-apps/adding-streamlit#label-streamlit-container-runtime-na)
- Runtime comparison: [Runtime environments for Streamlit apps](/developer-guide/streamlit/app-development/runtime-environments)
- SQL reference: [CREATE STREAMLIT](/sql-reference/sql/create-streamlit)
