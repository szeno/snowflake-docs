# Tutorial: Answer questions about time-series revenue data with Cortex Analyst

Transition to Cortex Agents

Snowflake recommends transitioning to [Cortex Agents](/user-guide/snowflake-cortex/cortex-agents), which supports every Cortex Analyst capability with higher answer quality.

## Introduction

Cortex Analyst transforms natural-language questions about your data into results by generating and executing SQL queries.
This tutorial describes how to set up Cortex Analyst to respond to questions about a time-series revenue data set.

### What you will learn

- Establish a semantic model for the data set.
- Create a Streamlit app that queries Cortex Analyst.

### Prerequisites

The following prerequisites are required to complete this tutorial:

- You have a Snowflake account and user with a role that grants the necessary
  privileges to create a database, schema, tables, stage, and virtual warehouse objects.
- You have [Streamlit](https://pypi.org/project/streamlit/) set up on your local system.

Refer to the [Snowflake in 20 minutes](/user-guide/tutorials/snowflake-in-20minutes) for instructions to meet these requirements.

## Step 1: Setup

### Getting the sample data

You will use a sample dataset downloaded
[from GitHub](https://github.com/Snowflake-Labs/sfguide-getting-started-with-cortex-analyst/tree/main/data).
Download the following data files to your system:

- `daily_revenue.csv`
- `product.csv`
- `region.csv`

Also download the [semantic model YAML](https://github.com/Snowflake-Labs/sfguide-getting-started-with-cortex-analyst/blob/main/revenue_timeseries.yaml) from GitHub.

You might want to take a look at this semantic model before proceeding. The semantic model supplements the SQL schema of
each table with additional information that helps Cortex Analyst understand questions about the data. For more
information, see [Using SQL commands to create and manage semantic views](/user-guide/views-semantic/sql).

Note

In a non-tutorial setting, you would bring your own data, possibly already in a Snowflake table, and develop
your own semantic model.

### Creating the Snowflake objects

Use Snowsight, the Snowflake UI, to create the Snowflake objects needed for this tutorial. After you complete the
tutorial, you can drop these objects.

Note

Use a role that can create databases, schemas, warehouses, stages, and tables.

To create the objects:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Projects** » **Worksheets**, and then select the **+** button. A new SQL worksheet appears.
3. Paste the SQL code below into the worksheet, then select **Run All** from the drop-down menu at the top right
   of the worksheet.

Copy code

```
/*--
• Database, schema, warehouse, and stage creation
--*/

USE ROLE SECURITYADMIN;

CREATE ROLE IF NOT EXISTS cortex_user_role;
GRANT DATABASE ROLE SNOWFLAKE.CORTEX_USER TO ROLE cortex_user_role;

GRANT ROLE cortex_user_role TO USER <user>;

USE ROLE sysadmin;

-- Create demo database
CREATE OR REPLACE DATABASE cortex_analyst_demo;

-- Create schema
CREATE OR REPLACE SCHEMA cortex_analyst_demo.revenue_timeseries;

-- Create warehouse
CREATE OR REPLACE WAREHOUSE cortex_analyst_wh
    WAREHOUSE_SIZE = 'large'
    WAREHOUSE_TYPE = 'standard'
    AUTO_SUSPEND = 60
    AUTO_RESUME = TRUE
    INITIALLY_SUSPENDED = TRUE
COMMENT = 'Warehouse for Cortex Analyst demo';

GRANT USAGE ON WAREHOUSE cortex_analyst_wh TO ROLE cortex_user_role;
GRANT OPERATE ON WAREHOUSE cortex_analyst_wh TO ROLE cortex_user_role;

GRANT OWNERSHIP ON SCHEMA cortex_analyst_demo.revenue_timeseries TO ROLE cortex_user_role;
GRANT OWNERSHIP ON DATABASE cortex_analyst_demo TO ROLE cortex_user_role;

USE ROLE cortex_user_role;

-- Use the created warehouse
USE WAREHOUSE cortex_analyst_wh;

USE DATABASE cortex_analyst_demo;
USE SCHEMA cortex_analyst_demo.revenue_timeseries;

-- Create stage for raw data
CREATE OR REPLACE STAGE raw_data DIRECTORY = (ENABLE = TRUE);

/*--
• Fact and Dimension Table Creation
--*/

-- Fact table: daily_revenue
CREATE OR REPLACE TABLE cortex_analyst_demo.revenue_timeseries.daily_revenue (
    date DATE,
    revenue FLOAT,
    cogs FLOAT,
    forecasted_revenue FLOAT,
    product_id INT,
    region_id INT
);

-- Dimension table: product_dim
CREATE OR REPLACE TABLE cortex_analyst_demo.revenue_timeseries.product_dim (
    product_id INT,
    product_line VARCHAR(16777216)
);

-- Dimension table: region_dim
CREATE OR REPLACE TABLE cortex_analyst_demo.revenue_timeseries.region_dim (
    region_id INT,
    sales_region VARCHAR(16777216),
    state VARCHAR(16777216)
);
```

The SQL above creates the following objects:

- A database named `cortex_analyst_demo`
- A schema within that database called `revenue_timeseries`
- Three tables in that schema: `daily_revenue`, `product_dim`, and `region_dim`
- A stage named `raw_data` that will hold the raw data we will load into these tables
- A virtual warehouse named `cortex_analyst_wh`

Note

The virtual warehouse is initially suspended. It starts automatically when you run a query.

## Step 2: Load the data into Snowflake

To get the data from the CSV files into Snowflake, you will upload them to the stage, then load the data from the stage
into the tables. At the same time, you will upload the semantic model YAML file for use in a later step.

The files you will upload are:

- `daily_revenue.csv`
- `product.csv`
- `region.csv`
- `revenue_timeseries.yaml`

To upload the files in Snowsight:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Ingestion** » **Add Data**, and then select **Load files into a stage**.
3. Drag the four files you downloaded in the previous step into the Snowsight window.
4. Choose the database `cortex_analyst_demo` and the stage `raw_data`, then select the **Upload** button to upload the files.

Now that you have uploaded the files, load the data from the CSV files by executing the SQL commands below in a Snowsight worksheet.

Copy code

```
USE WAREHOUSE cortex_analyst_wh;

COPY INTO cortex_analyst_demo.revenue_timeseries.daily_revenue
FROM @raw_data
FILES = ('daily_revenue.csv')
FILE_FORMAT = (
    TYPE=CSV,
    SKIP_HEADER=1,
    FIELD_DELIMITER=',',
    TRIM_SPACE=FALSE,
    FIELD_OPTIONALLY_ENCLOSED_BY=NONE,
    REPLACE_INVALID_CHARACTERS=TRUE,
    DATE_FORMAT=AUTO,
    TIME_FORMAT=AUTO,
    TIMESTAMP_FORMAT=AUTO
    EMPTY_FIELD_AS_NULL = FALSE
    error_on_column_count_mismatch=false
)
ON_ERROR=CONTINUE
FORCE = TRUE;

COPY INTO cortex_analyst_demo.revenue_timeseries.product_dim
FROM @raw_data
FILES = ('product.csv')
FILE_FORMAT = (
    TYPE=CSV,
    SKIP_HEADER=1,
    FIELD_DELIMITER=',',
    TRIM_SPACE=FALSE,
    FIELD_OPTIONALLY_ENCLOSED_BY=NONE,
    REPLACE_INVALID_CHARACTERS=TRUE,
    DATE_FORMAT=AUTO,
    TIME_FORMAT=AUTO,
    TIMESTAMP_FORMAT=AUTO
    EMPTY_FIELD_AS_NULL = FALSE
    error_on_column_count_mismatch=false
)
ON_ERROR=CONTINUE
FORCE = TRUE ;

COPY INTO cortex_analyst_demo.revenue_timeseries.region_dim
FROM @raw_data
FILES = ('region.csv')
FILE_FORMAT = (
    TYPE=CSV,
    SKIP_HEADER=1,
    FIELD_DELIMITER=',',
    TRIM_SPACE=FALSE,
    FIELD_OPTIONALLY_ENCLOSED_BY=NONE,
    REPLACE_INVALID_CHARACTERS=TRUE,
    DATE_FORMAT=AUTO,
    TIME_FORMAT=AUTO,
    TIMESTAMP_FORMAT=AUTO
    EMPTY_FIELD_AS_NULL = FALSE
    error_on_column_count_mismatch=false
)
ON_ERROR=CONTINUE
FORCE = TRUE ;
```

Note

Only the result of the last command is shown in the output pane. You can run the commands line by line to see the results of each command.

## Step 3: Create a Streamlit app to talk to your data through Cortex Analyst

To create a Streamlit app that uses Cortex Analyst:

1. Create a Python file locally called `analyst_demo.py`.
2. Copy the code below into the file.
3. Replace the placeholder values with your account details.
4. Run the Streamlit app using `streamlit run analyst_demo.py`.

Copy code

```
from typing import Any, Dict, List, Optional

import pandas as pd
import requests
import snowflake.connector
import streamlit as st

DATABASE = "CORTEX_ANALYST_DEMO"
SCHEMA = "REVENUE_TIMESERIES"
STAGE = "RAW_DATA"
FILE = "revenue_timeseries.yaml"
WAREHOUSE = "CORTEX_ANALYST_WH"

# replace values below with your Snowflake connection information
HOST = "<host>"
ACCOUNT = "<account>"
USER = "<user>"
PASSWORD = "<password>"
ROLE = "<role>"

if 'CONN' not in st.session_state or st.session_state.CONN is None:
    st.session_state.CONN = snowflake.connector.connect(
        user=USER,
        password=PASSWORD,
        account=ACCOUNT,
        host=HOST,
        port=443,
        warehouse=WAREHOUSE,
        role=ROLE,
    )

def send_message(prompt: str) -> Dict[str, Any]:
    """Calls the REST API and returns the response."""
    request_body = {
        "messages": [{"role": "user", "content": [{"type": "text", "text": prompt}]}],
        "semantic_model_file": f"@{DATABASE}.{SCHEMA}.{STAGE}/{FILE}",
    }
    resp = requests.post(
        url=f"https://{HOST}/api/v2/cortex/analyst/message",
        json=request_body,
        headers={
            "Authorization": f'Snowflake Token="{st.session_state.CONN.rest.token}"',
            "Content-Type": "application/json",
        },
    )
    request_id = resp.headers.get("X-Snowflake-Request-Id")
    if resp.status_code < 400:
        return {**resp.json(), "request_id": request_id}  # type: ignore[arg-type]
    else:
        raise Exception(
            f"Failed request (id: {request_id}) with status {resp.status_code}: {resp.text}"
        )

def process_message(prompt: str) -> None:
    """Processes a message and adds the response to the chat."""
    st.session_state.messages.append(
        {"role": "user", "content": [{"type": "text", "text": prompt}]}
    )
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Generating response..."):
            response = send_message(prompt=prompt)
            request_id = response["request_id"]
            content = response["message"]["content"]
            display_content(content=content, request_id=request_id)  # type: ignore[arg-type]
    st.session_state.messages.append(
        {"role": "assistant", "content": content, "request_id": request_id}
    )

def display_content(
    content: List[Dict[str, str]],
    request_id: Optional[str] = None,
    message_index: Optional[int] = None,
) -> None:
    """Displays a content item for a message."""
    message_index = message_index or len(st.session_state.messages)
    if request_id:
        with st.expander("Request ID", expanded=False):
            st.markdown(request_id)
    for item in content:
        if item["type"] == "text":
            st.markdown(item["text"])
        elif item["type"] == "suggestions":
            with st.expander("Suggestions", expanded=True):
                for suggestion_index, suggestion in enumerate(item["suggestions"]):
                    if st.button(suggestion, key=f"{message_index}_{suggestion_index}"):
                        st.session_state.active_suggestion = suggestion
        elif item["type"] == "sql":
            with st.expander("SQL Query", expanded=False):
                st.code(item["statement"], language="sql")
            with st.expander("Results", expanded=True):
                with st.spinner("Running SQL..."):
                    df = pd.read_sql(item["statement"], st.session_state.CONN)
                    if len(df.index) > 1:
                        data_tab, line_tab, bar_tab = st.tabs(
                            ["Data", "Line Chart", "Bar Chart"]
                        )
                        data_tab.dataframe(df)
                        if len(df.columns) > 1:
                            df = df.set_index(df.columns[0])
                        with line_tab:
                            st.line_chart(df)
                        with bar_tab:
                            st.bar_chart(df)
                    else:
                        st.dataframe(df)

st.title("Cortex Analyst")
st.markdown(f"Semantic Model: `{FILE}`")

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.suggestions = []
    st.session_state.active_suggestion = None

for message_index, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"]):
        display_content(
            content=message["content"],
            request_id=message.get("request_id"),
            message_index=message_index,
        )

if user_input := st.chat_input("What is your question?"):
    process_message(prompt=user_input)

if st.session_state.active_suggestion:
    process_message(prompt=st.session_state.active_suggestion)
    st.session_state.active_suggestion = None
```

When you run the app, it prompts you to enter a question. Start with “What questions can I ask?” and try some of its suggestions.

## Step 4: Clean up

### Clean up (optional)

Execute the following [DROP <object>](/sql-reference/sql/drop) commands to return your system to its state before you began the tutorial:

Copy code

```
DROP DATABASE IF EXISTS cortex_analyst_demo;
DROP WAREHOUSE IF EXISTS cortex_analyst_wh;
```

Dropping the database automatically removes all child database objects such as tables.

## Next steps

Congratulations! You have successfully built a simple Cortex Analyst app to “talk to your data” in Snowflake.

### Additional resources

Continue learning using the following resources:

- [Cortex Analyst overview](/user-guide/snowflake-cortex/cortex-analyst)
- [YAML specification for semantic views](/user-guide/views-semantic/semantic-view-yaml-spec)
- [Verified Query Repository](/user-guide/views-semantic/verified-query-repository)
- [REST API](/user-guide/snowflake-cortex/cortex-analyst/rest-api)
