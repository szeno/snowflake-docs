# Managing costs for Streamlit in Snowflake

This topic describes billing considerations for Streamlit in Snowflake.

## Billing considerations for Streamlit in Snowflake

Streamlit in Snowflake billing is based on the app’s runtime environment and query warehouse. The runtime environment
executes the Python code in your Streamlit app and can be either a container or warehouse. The query
warehouse executes any SQL queries within your app’s code.

### Query warehouse

When your app’s code executes SQL queries, those queries use the app’s query warehouse.
Snowflake automatically resumes and suspends the query warehouse according to its
own AUTO\_RESUME and AUTO\_SUSPEND values.

### Container runtime

Feature — Generally Available

Not supported in government regions.

If your Streamlit app uses a container runtime, you are billed for the usage of the
underlying Snowpark Container Services compute pool. In this case, the Streamlit app is a long-running
service. The Streamlit server runs continuously on a node of the compute pool, allowing
viewers to quickly access the app. Concurrent viewers connect to a single Streamlit
server.

When an app runs on `SYSTEM_COMPUTE_POOL_CPU`, Snowflake runs three Streamlit apps per
compute pool node. Otherwise, a single app can run on a node in the compute pool; a Streamlit app
takes an entire node.

After three days of viewer inactivity, the Streamlit server process ends and
Snowflake suspends the compute pool according to its own AUTO\_SUSPEND value. If you
try to keep a session alive for three days without a new viewer connecting, the app
will probably be suspended. It’s a best practice to move long-running computations to another service.
For more information about compute pool billing, see [Understanding compute cost](/user-guide/cost-understanding-compute).

### Warehouse runtime

If your app uses a warehouse runtime, Snowflake resumes the app’s code warehouse
when someone visits the app. Each time a viewer connects to the app, a new Streamlit server
process starts in the code warehouse and a WebSocket connection is established. Concurrent
viewers each connect to their own Streamlit server running in the same code warehouse.

A WebSocket connection keeps the code warehouse active and expires approximately 15 minutes
after the associated viewer’s last activity. However, this can be affected by the viewer’s
browser settings and activity. Mouse movement over the app counts as activity and keeps
the WebSocket connection alive. You can change the WebSocket timeout value for your
account by contacting Snowflake Support.

The code warehouse is billed for the time it is active. To conserve credits, you
can do one of the following:

- Manually suspend the app from Snowsight.
- Close all browser tabs running the app, or navigate away from the app. This closes the WebSocket
  connection and allows the warehouse to auto-suspend.
- Set a custom sleep timer for the app. This automatically suspends the warehouse after a specified period
  of inactivity. For more information, see [Custom sleep timer for a Streamlit app](/developer-guide/streamlit/features/sleep-timer).

For guidelines on selecting a warehouse, see [Guidelines for selecting resources in Streamlit in Snowflake](/developer-guide/streamlit/app-development/runtime-environments#label-streamlit-guidelines-wh).
