# Nov 19, 2026: Snowflake App Runtime serverless compute and Workspaces development (*Preview*)

Snowflake App Runtime serverless compute and development in Snowsight Workspaces are now in [Preview](/release-notes/preview-features).

**Serverless compute.** An app can now run on serverless compute instead of a
compute pool. Snowflake starts the app when a request arrives, suspends it after an idle
period of at least one hour, and bills only while it runs. Set `url_prefix` to
choose a stable URL for the app. Managed compute remains the default; you opt in for each app in
[`app.yml`](/developer-guide/snowflake-app-runtime/app-yml#label-snowflake-app-runtime-app-yml-serverless).
See [Serverless compute for Snowflake App Runtime](/developer-guide/snowflake-app-runtime/serverless).

**Python apps.** You can now build and deploy Python 3.13 apps, such as FastAPI
apps, on serverless compute. See
[Build a Python app for Snowflake App Runtime](/developer-guide/snowflake-app-runtime/build-python-app).

**Develop in Snowsight Workspaces.** You can now build an App Runtime app in
Snowsight Workspaces and preview it as you edit, without deploying. See
[Develop Snowflake App Runtime apps in Snowsight Workspaces](/developer-guide/snowflake-app-runtime/workspaces).

For limits that apply during the preview, see
[Snowflake App Runtime limitations](/developer-guide/snowflake-app-runtime/limitations).
