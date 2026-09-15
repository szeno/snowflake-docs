# Example: Build a personalized data dashboard

This example walks you through building a Streamlit in Snowflake app that queries Snowflake data, adds a
third-party charting library, and personalizes the display for each viewer. By the end,
you’ll understand the core development cycle: create, deploy, edit, and redeploy.

The app uses a container runtime. Before you begin, make sure you’ve completed the
[prerequisites](/developer-guide/streamlit/getting-started/overview#label-streamlit-prereqs).

## Set up sample data

This example uses a database called `dashboard_demo`. You can substitute any database
and schema you have access to – just update the references in the SQL and app code to match.

Create a table with sample revenue data. Run the following SQL in a worksheet or SQL session:

Copy code

```
CREATE OR REPLACE TABLE dashboard_demo.public.monthly_revenue (
   month DATE,
   region VARCHAR,
   revenue NUMBER(12, 2)
);

INSERT INTO dashboard_demo.public.monthly_revenue VALUES
   ('2026-01-01', 'North America', 125000.00),
   ('2026-01-01', 'Europe', 98000.00),
   ('2026-01-01', 'Asia Pacific', 87000.00),
   ('2026-02-01', 'North America', 132000.00),
   ('2026-02-01', 'Europe', 101000.00),
   ('2026-02-01', 'Asia Pacific', 93000.00),
   ('2026-03-01', 'North America', 141000.00),
   ('2026-03-01', 'Europe', 110000.00),
   ('2026-03-01', 'Asia Pacific', 99000.00);
```

## Write the app code

On your local machine, in a project directory of your choice, create a file named
`streamlit_app.py` with the following code. If you plan to use Snowsight,
you can paste this code into the editor after creating the app.

Copy code

```
import streamlit as st
import plotly.express as px

st.title("Revenue Dashboard")
st.write(f"Welcome, {st.user.user_name}!")

conn = st.connection("snowflake")

df = conn.query("""
    SELECT month, region, revenue
    FROM dashboard_demo.public.monthly_revenue
    ORDER BY month
""")

selected_regions = st.multiselect(
    "Filter by region",
    options=df["REGION"].unique(),
    default=df["REGION"].unique(),
)

filtered = df[df["REGION"].isin(selected_regions)]

fig = px.bar(
    filtered,
    x="MONTH",
    y="REVENUE",
    color="REGION",
    barmode="group",
    title="Monthly Revenue by Region",
)
st.plotly_chart(fig, use_container_width=True)

st.dataframe(filtered, use_container_width=True)
```

This app uses:

- `conn.query()` to query data from Snowflake. Results are cached automatically, so
  the query only runs once until the cache expires. For more information, see
  [Manage secrets and configure your Streamlit app](/developer-guide/streamlit/app-development/secrets-and-configuration).
- `st.user.user_name` to greet the current viewer. For more information, see
  [Personalize your Streamlit app with user information](/developer-guide/streamlit/app-development/personalization).
- `plotly` for interactive charts, which is an external dependency that you declare in the
  next step.

## Declare dependencies

Container runtimes install packages listed in a `requirements.txt` file. Create a
`requirements.txt` file alongside your `streamlit_app.py`:

```
plotly
streamlit
```

When the app starts, the container runtime automatically installs the declared packages.
For more complex dependency scenarios, you can use a `pyproject.toml` file instead.
For more information, see [Manage dependencies for your Streamlit app](/developer-guide/streamlit/app-development/dependency-management).

## Deploy the app

SnowsightSQLSnowflake CLI

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Projects** » **Streamlit**.
3. Select **+ Streamlit App**.
4. Enter `revenue_dashboard` as the app name.
5. Select a database and schema.
6. Select **Run on container**, then select a compute pool and query warehouse.
7. Select **Create**.
8. In the editor, replace the starter code with the app code above.
9. Upload or create the `requirements.txt` file by selecting **+** (Add) »
   **Create new file**, entering `requirements.txt`, and pasting the contents.
10. Select **Run**.

1. Stage your app files:

   Copy code

   ```
   CREATE STAGE IF NOT EXISTS dashboard_demo.public.app_stage;

   PUT file:///path/to/streamlit_app.py @dashboard_demo.public.app_stage/dashboard
   AUTO_COMPRESS = FALSE OVERWRITE = TRUE;
   PUT file:///path/to/requirements.txt @dashboard_demo.public.app_stage/dashboard
   AUTO_COMPRESS = FALSE OVERWRITE = TRUE;
   ```
2. Create the Streamlit app:

   Copy code

   ```
   CREATE STREAMLIT dashboard_demo.public.revenue_dashboard
   FROM '@dashboard_demo.public.app_stage/dashboard'
   MAIN_FILE = 'streamlit_app.py'
   RUNTIME_NAME = 'SYSTEM$ST_CONTAINER_RUNTIME_PY3_11'
   COMPUTE_POOL = my_compute_pool
   QUERY_WAREHOUSE = my_warehouse;

   ALTER STREAMLIT dashboard_demo.public.revenue_dashboard ADD LIVE VERSION FROM LAST;
   ```
3. To view your app, sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in), then In the navigation menu, select **Projects** » **Streamlit**, and select your app.

Note

[Snowflake CLI](/developer-guide/snowflake-cli/installation/installation) version 3.14.0
or later is required. Version 3.14+ uses the modern CREATE STREAMLIT syntax by default.

1. Create a project directory with the following structure:

   Copy code

   ```
   revenue_dashboard/
   ├── snowflake.yml
   ├── requirements.txt
   └── streamlit_app.py
   ```
2. Create a `snowflake.yml` file:

   Copy code

   ```
   definition_version: 2
   entities:
   revenue_dashboard:
      type: streamlit
      identifier: revenue_dashboard
      query_warehouse: my_warehouse
      compute_pool: my_compute_pool
      runtime_name: SYSTEM$ST_CONTAINER_RUNTIME_PY3_11
      main_file: streamlit_app.py
      artifacts:
      - streamlit_app.py
      - requirements.txt
   ```
3. Deploy the app:

   Copy code

   ```
   snow streamlit deploy --open
   ```

## Make a change

Try editing your app to see the development cycle in action. Add a summary metric by
inserting the following two lines into `streamlit_app.py`, between the
`filtered = ...` line and the `fig = px.bar(...)` line:

Copy code

```
total = filtered["REVENUE"].sum()
st.metric("Total Revenue", f"${total:,.0f}")
```

SnowsightSQLSnowflake CLI

If you’re editing in the browser, paste the lines into the editor and select **Run**.

Stage the updated file, then copy it to your app’s live version location:

Copy code

```
PUT file:///path/to/streamlit_app.py @dashboard_demo.public.app_stage/dashboard
   AUTO_COMPRESS = FALSE OVERWRITE = TRUE;

DESCRIBE STREAMLIT dashboard_demo.public.revenue_dashboard;
-- Copy the live_version_location_uri value from the result.

COPY FILES INTO '<live_version_location_uri>'
   FROM @dashboard_demo.public.app_stage/dashboard
   FILES = ('streamlit_app.py');
```

Save the file locally and redeploy:

Copy code

```
snow streamlit deploy --replace
```

For more information about the editing workflow, see
[Edit your Streamlit app](/developer-guide/streamlit/app-development/editing-your-app).

## Clean up

To remove the resources created in this example, run the following SQL:

Copy code

```
DROP STREAMLIT IF EXISTS dashboard_demo.public.revenue_dashboard;
DROP TABLE IF EXISTS dashboard_demo.public.monthly_revenue;
```

## What’s next?

- [Example: Build a form that writes to Snowflake](/developer-guide/streamlit/getting-started/example-crud-app): Build an app with a form that writes data back to Snowflake.
- [Personalize your Streamlit app with user information](/developer-guide/streamlit/app-development/personalization): Learn more about personalizing apps with
  `st.user`.
- [External network access in Streamlit in Snowflake](/developer-guide/streamlit/features/external-access): Connect your app to external APIs.
