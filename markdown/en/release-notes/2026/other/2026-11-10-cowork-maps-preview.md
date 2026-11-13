# November 10, 2026: Geospatial maps in Snowflake CoWork (*Preview*)

Geospatial maps are now available in preview in Snowflake CoWork. When a question returns locations,
regions, or density over geography, the agent can plot the result on an interactive map: latitude
and longitude points, H3 hexagons, or `GEOGRAPHY` and `GEOMETRY` shapes. You can pan and zoom the
map in chat, open Explore on a query-backed map, and save or share it as an artifact. Query-backed
maps re-run under the viewer’s credentials. Maps use a dedicated map specification rather than
Vega-Lite, so `<chart_customization>` and `vega_template` don’t apply.

For more information, see [Geospatial maps in Snowflake CoWork](/user-guide/snowflake-cortex/snowflake-cowork/maps).
