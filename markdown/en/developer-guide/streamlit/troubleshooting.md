# Troubleshooting Streamlit in Snowflake

The following scenarios can help you troubleshoot issues that can occur when working with Streamlit in Snowflake.

## You can’t connect to the Snowflake backend

In some cases, browser extensions can make local network access (LNA) requests as part of normal operation.
For example, a security extension may detect Streamlit in Snowflake’s cross-origin traffic and then make an LNA request.
Chrome 142 introduced mandatory LNA restrictions. Because you can’t configure LNA at the extension
level, you must either disable the extension or allow LNA for
Snowsight. For more information about Chrome’s LNA restrictions, see
[New permission prompt for Local Network Access](https://developer.chrome.com/blog/local-network-access)
in the Chrome for Developers blog.

|  |  |
| --- | --- |
| Error | Unable to connect to the Snowflake backend. |
| Cause | A browser extension attempted to make a local network access (LNA) request that was blocked by Chrome’s LNA restrictions. |
| Solution | Disable the browser extension or allow LNA for Snowsight. |

Expand

Show lessSee more

Contact Snowflake support if the issue persists after performing the following steps:

- Verify you’re on the latest Snowsight release.
- Verify that the “Local network access” permission is enabled for Snowsight. If you use an enterprise managed browser,
  contact your IT administrator.
- Verify that load failures continue after temporarily disabling extensions.
- Verify that load failures continue after disabling the Chrome flag via `chrome://flags#local-network-access-check`.

## You can’t load the Streamlit app

Each Streamlit app running in Streamlit in Snowflake uses a unique subdomain.

Ensure that `*.snowflake.app` and `*.snowflake.com` are on the allowlist in your network (including content filtering systems), and
can connect to Snowflake. For Streamlit apps using container runtimes, also add `*.snowflakecomputing.app` to the allowlist.
When these domains are on the allowlist, your apps can communicate with Snowflake servers without any restrictions.
However, in some cases adding these domains may not be sufficient due to network policies blocking subpaths under them. If this occurs,
contact your network administrator.

In addition, to prevent any issues connecting to the Snowflake backend, ensure that WebSockets are not blocked in your network configuration.

|  |  |
| --- | --- |
| Error | ``` Could not reload streamlit files. Error: 092806 (P0002): The specified Streamlit was not found. ``` |
| Cause | The Snowflake WebSocket connection cannot reach the endpoint associated with the application. |
| Solution | Add \*.snowflake.app to the allowlist on the organization’s firewall configuration. For Streamlit apps using container runtimes, also add \*.snowflakecomputing.app to the allowlist.  If your account uses per-account URLs (enabled by setting [ENABLE\_PER\_ACCOUNT\_APP\_SERVICE\_URL](/sql-reference/parameters#label-enable-per-account-app-service-url) to `TRUE`), you can use a more specific allowlist entry: `*.orgname-account_name.region.cloud.snowflake.app`. |

Expand

Show lessSee more

## You can’t see your data or change your database

You might not be able to see your data or change the database, warehouse, or role because Streamlit apps run with owner’s rights by default, which means that they run with the privileges of the owner, not the privileges of the caller. Streamlit apps use the database and schema that the Streamlit in Snowflake app was created in, not the database and schema that the caller is currently using.

For more information, see [Understanding owner’s rights and Streamlit in Snowflake apps](/developer-guide/streamlit/object-management/owners-rights). To run a container-runtime app with the viewer’s
privileges instead, see [Restricted caller’s rights and Streamlit in Snowflake](/developer-guide/streamlit/features/restricted-callers-rights).

## Streamlit library feature doesn’t work

Ensure that the Streamlit library version and feature that you use are supported by Streamlit in Snowflake. For more information, see [Supported versions of the Streamlit library in warehouse runtimes](/developer-guide/streamlit/app-development/dependency-management#label-streamlit-supported-streamlit-versions-on-warehouses) and [Limitation details](/developer-guide/streamlit/limitations#label-streamlit-unsupported-features).

To ask questions on features in the open-source Streamlit library, see [Streamlit Community Forum](https://discuss.streamlit.io/).
