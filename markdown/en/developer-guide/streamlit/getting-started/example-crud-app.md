# Example: Build a form that writes to Snowflake

This example walks you through building a Streamlit in Snowflake app that collects user input through a form
and writes it to a Snowflake table. The app also reads the data back to display all
submissions, and uses `st.user` to track who submitted each entry.

The app uses a container runtime. Before you begin, make sure you’ve completed the
[prerequisites](/developer-guide/streamlit/getting-started/overview#label-streamlit-prereqs).

## Set up the target table

This example uses a database called `crud_demo`. You can substitute any database
and schema you have access to – just update the references in the SQL and app code to match.

Create a table to store form submissions. Run the following SQL in a worksheet or SQL session:

Copy code

```
CREATE OR REPLACE TABLE crud_demo.public.feedback (
   submitted_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
   submitted_by VARCHAR,
   category VARCHAR,
   rating INTEGER,
   comments VARCHAR
);
```

## Write the app code

On your local machine, create a file named `streamlit_app.py` with the following code.
If you plan to use Snowsight, you can paste this code into the editor after creating
the app.

Copy code

```
import streamlit as st

st.title("Feedback Form")
st.write(f"Logged in as: {st.user.user_name}")

conn = st.connection("snowflake")
session = conn.session()

with st.form("feedback_form"):
    category = st.selectbox(
        "Category", ["Bug Report", "Feature Request", "General Feedback"]
    )
    rating = st.slider("Rating", 1, 5, 3)
    comments = st.text_area("Comments")
    submitted = st.form_submit_button("Submit")

if submitted:
    session.sql(
        """
        INSERT INTO crud_demo.public.feedback
            (submitted_by, category, rating, comments)
        VALUES (?, ?, ?, ?)
        """,
        params=[st.user.user_name, category, rating, comments],
    ).collect()
    st.success("Feedback submitted!")

st.subheader("Last 10 submissions")
data = session.sql(
    "SELECT * FROM crud_demo.public.feedback ORDER BY submitted_at DESC LIMIT 10"
).to_pandas()
st.dataframe(data, use_container_width=True)
```

This app uses:

- `st.form` to collect input before submitting, preventing re-runs on every widget
  interaction.
- `st.connection("snowflake").session()` to get a Snowpark session for writing data.
  For more information, see [Manage secrets and configure your Streamlit app](/developer-guide/streamlit/app-development/secrets-and-configuration).
- `session.sql()` instead of `conn.query()` to read back the submissions.
  `conn.query()` caches results by default, so new entries wouldn’t appear until the
  cache expires. `session.sql()` executes a fresh query on every rerun.
- `st.user.user_name` to record who submitted each entry. For more information,
  see [Personalize your Streamlit app with user information](/developer-guide/streamlit/app-development/personalization).

## Declare dependencies

This app only uses `streamlit` and the built-in Snowflake connection, so no additional
dependencies are required.

For more information, see [Manage dependencies for your Streamlit app](/developer-guide/streamlit/app-development/dependency-management).

## Deploy the app

SnowsightSQLSnowflake CLI

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Projects** » **Streamlit**.
3. Select **+ Streamlit App**.
4. Enter `feedback_app` as the app name.
5. Select a database and schema.
6. Select **Run on container**, then select a compute pool and query warehouse.
7. Select **Create**.
8. In the editor, replace the starter code with the app code above.
9. Select **Run**.

1. Stage your app files:

   Copy code

   ```
   CREATE STAGE IF NOT EXISTS crud_demo.public.app_stage;

   PUT file:///path/to/streamlit_app.py @crud_demo.public.app_stage/feedback
   AUTO_COMPRESS = FALSE OVERWRITE = TRUE;
   ```
2. Create the Streamlit app:

   Copy code

   ```
   CREATE STREAMLIT crud_demo.public.feedback_app
   FROM '@crud_demo.public.app_stage/feedback'
   MAIN_FILE = 'streamlit_app.py'
   RUNTIME_NAME = 'SYSTEM$ST_CONTAINER_RUNTIME_PY3_11'
   COMPUTE_POOL = my_compute_pool
   QUERY_WAREHOUSE = my_warehouse;

   ALTER STREAMLIT crud_demo.public.feedback_app ADD LIVE VERSION FROM LAST;
   ```
3. To view your app, sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in), then In the navigation menu, select **Projects** » **Streamlit**, and select your app.

Note

[Snowflake CLI](/developer-guide/snowflake-cli/installation/installation) version 3.14.0
or later is required. Version 3.14+ uses the modern CREATE STREAMLIT syntax by default.

1. Create a project directory with the following structure:

   Copy code

   ```
   feedback_app/
   ├── snowflake.yml
   └── streamlit_app.py
   ```
2. Create a `snowflake.yml` file:

   Copy code

   ```
   definition_version: 2
   entities:
   feedback_app:
      type: streamlit
      identifier: feedback_app
      query_warehouse: my_warehouse
      compute_pool: my_compute_pool
      runtime_name: SYSTEM$ST_CONTAINER_RUNTIME_PY3_11
      main_file: streamlit_app.py
      artifacts:
      - streamlit_app.py
   ```
3. Deploy the app:

   Copy code

   ```
   snow streamlit deploy --open
   ```

## Try the app

1. Open the app in your browser.
2. Fill in the form fields and select **Submit**.
3. The feedback table below the form updates to show your new submission, including your
   email address and a timestamp.
4. Submit a few more entries, then try filtering or sorting the data in the table.

## Extend the app

Try adding a delete button next to each row, or a chart that shows the average rating
by category. For example, add the following after the dataframe:

Copy code

```
import plotly.express as px

if not data.empty:
    avg_ratings = data.groupby("CATEGORY")["RATING"].mean().reset_index()
    fig = px.bar(avg_ratings, x="CATEGORY", y="RATING", title="Average Rating by Category")
    st.plotly_chart(fig, use_container_width=True)
```

If you add `plotly`, declare it in a `requirements.txt` file:

```
plotly
```

For more complex dependency scenarios, you can use a `pyproject.toml` file instead.
For more information, see [Manage dependencies for your Streamlit app](/developer-guide/streamlit/app-development/dependency-management).

## Clean up

To remove the resources created in this example, run the following SQL:

Copy code

```
DROP STREAMLIT IF EXISTS crud_demo.public.feedback_app;
DROP TABLE IF EXISTS crud_demo.public.feedback;
```

## What’s next?

- [Create your Streamlit app](/developer-guide/streamlit/app-development/creating-your-app): Learn about all the options for creating apps.
- [Personalize your Streamlit app with user information](/developer-guide/streamlit/app-development/personalization): Explore all the user attributes available
  through `st.user`.
- [Manage secrets and configure your Streamlit app](/developer-guide/streamlit/app-development/secrets-and-configuration): Access secrets and external services
  in your app.
- [Sharing Streamlit in Snowflake apps](/developer-guide/streamlit/features/sharing-streamlit-apps): Share your app with other users.
