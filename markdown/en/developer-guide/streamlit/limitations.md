# Limitations and library changes

This topic describes limitations and feature behavior changes when a Streamlit feature
works differently in Snowflake than in the open-source library.

To view release notes for each Streamlit version, see [Streamlit documentation](https://docs.streamlit.io/develop/quick-reference/release-notes).

## Limitations and changes for all runtimes

The following limitations apply to all Streamlit in Snowflake apps, regardless of runtime environment:

- [Limitation details](#label-streamlit-unsupported-features)
- [Loading external resources](#label-streamlit-limitations-csp)
- [Custom components](#label-streamlit-custom-components) with external scripts
- [Query parameters](#label-streamlit-query-params)
- Using external stages isn’t supported.
- Replication isn’t supported.
- Using `.so` files isn’t supported.

## Limitations and changes that vary by runtime

The following table compares limitations that differ between warehouse runtimes and container runtimes.
For more information about runtime environments, see [Runtime environments for Streamlit apps](/developer-guide/streamlit/app-development/runtime-environments).

| Limitation | Warehouse runtime | Container runtime |
| --- | --- | --- |
| [Python versions](/developer-guide/streamlit/app-development/dependency-management#label-streamlit-supported-python-versions) | 3.9, 3.10, 3.11 | 3.11 only |
| [Streamlit versions](/developer-guide/streamlit/app-development/dependency-management#label-streamlit-supported-streamlit-versions) | 1.22+ (limited selection) | 1.50+ (any version, including `streamlit-nightly` versions) |
| [Custom Components v2](#label-streamlit-custom-components) | Not supported | Supported |
| [Displaying large amounts of data](#label-streamlit-limitations-data) | 32 MB | Configurable |
| [File uploads](#label-streamlit-limitations-st-file-uploader) | 200 MB | Configurable |
| [Mapbox and Carto](#label-streamlit-mapbox-carto) | Requires acknowledgement of the External Offerings Terms. | Not subject to the External Offerings Terms. |
| [Caching](#label-streamlit-caching) | Single-session caching. Cached values can’t be shared between sessions. | Fully supported. Cached values are shared across all viewer sessions unless you use session-scoping in the cache decorator. |
| [ROOT\_LOCATION parameter](/developer-guide/streamlit/migrations-and-upgrades/overview) | Supported as a legacy parameter in CREATE STREAMLIT. | Not supported |
| Maintenance window | Not applicable | Subject to the Snowpark Container Services [maintenance window](/developer-guide/snowpark-container-services/working-with-compute-pool#label-spcs-working-with-compute-pool-maintenance-window). |
| Static file serving | Not supported | Supported |

Expand

Show lessSee more

## Limitation details

### Unsupported Streamlit features

The following Streamlit features are not fully supported in Streamlit in Snowflake:

- [st.set\_page\_config](https://docs.streamlit.io/develop/api-reference/configuration/st.set_page_config):
  The `page_title`, `page_icon`, and `menu_items` properties of the
  `st.set_page_config` command aren’t supported.
- [config.toml](https://docs.streamlit.io/develop/api-reference/configuration/config.toml) file:
  For a summary of supported and unsupported configuration options, see [Streamlit configuration](/developer-guide/streamlit/app-development/secrets-and-configuration#label-streamlit-configuration).

### Loading external resources

All Streamlit in Snowflake apps run within a Content Security Policy (CSP) that restricts what resources can be
loaded. The CSP blocks loading scripts and styles from external domains and embedding external content in iframes.
It also blocks front-end calls that are generally considered unsafe, like `eval()`.
Images, media, and fonts can be loaded from any HTTPS domain.
For more information about the CSP, see [Content Security Policy](/developer-guide/streamlit/object-management/security#label-streamlit-content-security-policy).

For example, the following code runs without a Python error, but the script is not loaded or executed in the browser:

Copy code

```
# This won't work
st.html(
   "<script src="http://www.example.com/example.js"></script>",
   unsafe_allow_javascript=True
)
```

Note

App developers are responsible for security checks and the software supply chain of Streamlit in Snowflake app code per the
[Snowflake’s Shared Responsibility Model](https://www.snowflake.com/en/resources/report/snowflake-shared-responsibility-model/).

### Custom components

As a consequence of the CSP, custom components can’t load scripts from external domains
in warehouse and container runtimes.

- In warehouse runtimes, Components v2 (`st.components.v2.component`) isn’t supported.
- In container runtimes, Components v2 is fully supported, including package-based components that
  use an asset directory.

Components v1 (`st.components.v1.html`, `st.components.v1.iframe`) is supported in both runtimes.

Note

Components imported from a third-party source are subject to the license attached to that component. You are responsible
for ensuring that your use of a component is permitted by its license.

Snowflake doesn’t build or maintain third-party components that you might import into Streamlit in Snowflake. Use of such components is at
your own risk and is not subject to any warranties, service level agreements, or other similar guarantees by Snowflake.

### Query parameters

For [st.query\_params](https://docs.streamlit.io/develop/api-reference/caching-and-state/st.query_params) in Streamlit in Snowflake, a `streamlit-` prefix is added to each query parameter key in the URL. This prefix
isn’t included when you use `st.query_params` to get or set a value.

For example, consider the following URL:

```
https://app.snowflake.com/org/account_name/#/streamlit-apps/DB.SCHEMA.APP_NAME?streamlit-first_key=one&streamlit-second_key=two
```

The parameters in this URL are accessible in `st.query_params` as the following key-value pairs:

Copy code

```
{
   "first_key" : "one",
   "second_key" : "two"
}
```

### Displaying large amounts of data

Streamlit apps running in warehouse runtimes have a 32-MB limit on the size of messages exchanged between the backend and the
frontend. If you attempt to display more than 32 MB of data with a single Streamlit command, like `st.dataframe`, the following error occurs:

```
MessageSizeError: Data Size exceeds message limit
```

To avoid this limit, design your Streamlit app to display data in increments smaller than 32 MB. There is no explicit limit on the size of
a query you can run or the amount of data you can have in memory.

In container runtimes, this limit defaults to 200 MB and can be changed by setting the Streamlit configuration option,
`server.maxMessageSize`. However, the message size can’t exceed the capacity of the container’s memory. Allowing larger messages
could exceed the container’s memory limit, especially if concurrent viewers are present.

### File uploads

The default file-size limit for [st.file\_uploader](https://docs.streamlit.io/develop/api-reference/widgets/st.file_uploader) and [st.chat\_input](https://docs.streamlit.io/develop/api-reference/chat/st.chat_input) is 200 MB.
In warehouse runtimes, this isn’t configurable. In container runtimes, this limit can be changed by setting the Streamlit configuration option,
`server.maxUploadSize`. However, the file size can’t exceed the capacity of the container’s memory. Allowing larger files
could exceed the container’s memory limit, especially if concurrent viewers are present.

For larger files, consider processing data in smaller batches or using alternative uploading methods.

### Mapbox and Carto

Mapbox and Carto provide map tiles when you use the [st.map](https://docs.streamlit.io/develop/api-reference/charts/st.map) or [st.pydeck\_chart](https://docs.streamlit.io/develop/api-reference/charts/st.pydeck_chart) Streamlit commands.

In warehouse runtimes, which manage their packages with conda, Mapbox and Carto are third-party
applications that are subject to Snowflake’s
[External Offerings Terms](https://www.snowflake.com/legal/external-offering-terms/).

To use these commands in warehouse runtimes, you must acknowledge the External Offerings Terms.
Container runtimes don’t require this acknowledgement.

### Caching

Caching is partially supported in warehouse runtimes and fully supported in container runtimes.

In warehouse runtimes, caching is limited to single-session caching. Cached values can’t be shared between sessions.
In container runtimes, caching is fully supported. Cached values are shared across all viewer sessions.
