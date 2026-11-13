# Geospatial maps in Snowflake CoWork

[Preview Feature](/release-notes/preview-features)  — Open

Available to all accounts.

Snowflake CoWork can turn geospatial query results into interactive maps. Ask a question that needs
locations, regions, or density over geography, and the agent plots the answer on a map instead of a
Vega-Lite chart.

Maps use a dedicated map specification (MapSpec), not Vega-Lite. The agent cites a map with a
`<map>` tag and streams it on the `response.map` channel of the Cortex Agents Run API. For chart
customization that applies only to Vega-Lite charts, see
[Customize charts in Snowflake CoWork](/user-guide/snowflake-cortex/snowflake-cowork/chart-customization).

## Ask for a map

Ask for geography the same way you ask for any other insight. Examples:

- Show store locations on a map colored by revenue.
- Map delivery density across the city as hexagons.
- Plot the sales territories as polygons.

The agent chooses a map when the result has location columns or geospatial geometry. You can also ask
explicitly for a map, an H3 density map, or a polygon overlay.

## Layer types

Maps support three layer types:

| Layer type | When the agent uses it | Typical source columns |
| --- | --- | --- |
| **Points (lat/lon)** | Individual places such as stores, sites, or addresses | Latitude and longitude columns (numeric or numeric strings) |
| **H3 hexagons** | Density, heatmaps, or aggregates over area when there is no region polygon to group by | H3 cell IDs produced by SQL such as [H3\_LATLNG\_TO\_CELL\_STRING](/sql-reference/functions/h3_latlng_to_cell_string) |
| **GeoJSON** | Lines and existing region polygons such as ZIP codes, territories, or routes | `GEOGRAPHY` or `GEOMETRY` columns |

Expand

Show lessSee more

Color encoding is optional on every layer. Sequential measures use a color ramp. Categorical fields
such as region names or IDs keep discrete colors.

The map camera fits to the plotted data, including H3 hexagon outlines, so the first view shows the
relevant geography rather than the whole world.

## Interact with a map

In chat, you can:

- Pan and scroll-zoom the map in the inline results card and in the expanded view.
- Open Explore to inspect the map and related results in the right panel.
- Ask follow-up questions such as “color that by revenue” or “switch that to H3”. The agent keeps
  map context across turns so it can revise the same map.

Maps don’t use the manual chart editor for bar, line, pie, and scatter charts. To change styling or layer choice, ask
Snowflake CoWork in chat or use the map settings available in Explore.

## Save, refresh, and share

You can save a map as an artifact the same way you save a chart. Saved maps appear in the artifacts
hub, can be shared by link, and refresh under the viewer’s credentials when the map is query-backed.

- **Query-backed maps** keep a reference to their source query. Refresh reruns that query under the
  current viewer’s credentials, the same as chart artifacts.
- **Snapshot-only maps** (for example, maps built from MCP row sets or procedure results with no
  reusable query) render from the rows captured in the map specification. They don’t refresh from a
  live query.
- In a **shared conversation** snapshot, maps are captured with the rest of the thread at share time
  and don’t refresh.

For artifact lifecycle, permissions, and sharing controls, see
[Chart and Thread artifacts in Snowflake CoWork](/user-guide/snowflake-cortex/snowflake-cowork/artifacts).

## Maps in the Cortex Agents Run API

When an agent produces a map, the Run API streams a `response.map` event and includes a `map`
content block in the final response. The payload carries a `map_spec` string (the MapSpec), not a
Vega-Lite `chart_spec`. Clients that render agent responses should handle `map` alongside `chart`
and `table`.

For the event and schema details, see [Maps (`response.map`)](/user-guide/snowflake-cortex/cortex-agents-run#label-snowflake-agents-run-maps).

## Limitations

- Maps don’t use `<chart_customization>` or `vega_template`. Those controls apply only to Vega-Lite
  charts. Style a map by asking the agent or by using the map settings in Explore.
- The manual chart editor UI isn’t available for maps.
- Snapshot-only maps don’t refresh, including when shared.
- Image (PNG) export isn’t available for maps. Query-backed maps still support data export such as
  CSV or copy.
