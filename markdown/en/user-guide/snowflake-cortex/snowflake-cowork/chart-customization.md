# Customize charts in Snowflake CoWork

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Snowflake CoWork generates charts automatically from your data. You can customize those charts,
controlling colors, fonts, chart types, and more, by adding configuration to your agent or
semantic view.

## Overview

Customization works at two levels:

- **Agent level**: Applies to all charts across every semantic view attached to the agent. Use this
  for global defaults such as brand colors and fonts.
- **Semantic view level**: Applies only to charts generated from that specific semantic view. Use
  this for column-specific rules and domain-specific chart type preferences.

At each level, two mechanisms are available:

- **vega\_template**: A partial [Vega-Lite](https://vega.github.io/vega-lite/) JSON spec that is
  deterministically merged into every generated chart. Use this for anything that must always apply.
- **Free-text instructions**: Natural language guidance injected into the chart generation prompt.
  The LLM makes a best effort to follow these, but they aren’t guaranteed.

Note

When both agent and semantic view define a `vega_template`, the agent template is applied
first and the semantic view template is applied second. On conflicting keys, the semantic view
wins.

## Agent-level customization

Add a `<chart_customization>` block inside `instructions.orchestration` in your agent
configuration. You can combine font theming and a global default palette:

Copy code

```
<chart_customization>
Prefer horizontal bar charts for ranked data.
vega_template:
{
  "background": "antiquewhite",
  "config": {
    "title":  { "font": "monospace", "fontStyle": "italic", "fontSize": 20, "fontWeight": "lighter" },
    "axis":   { "labelFont": "monospace", "titleFont": "monospace", "titleFontSize": 15, "labelFontSize": 10 },
    "header": { "labelFont": "monospace", "titleFont": "monospace", "labelFontSize": 10 },
    "legend": { "labelFont": "monospace", "titleFont": "monospace", "titleFontSize": 18, "labelFontSize": 15 },
    "mark":   { "font": "monospace" }
  }
}
</chart_customization>
```

Use the agent level for:

- Brand color palette
- Default visual theme (fonts, background)
- Cross-domain style preferences
- Number or currency formatting defaults

Avoid column-specific color mappings at the agent level. Column names differ between semantic views
and are silently ignored when not found.

## Semantic-view-level customization

Add a `<chart_customization>` block inside the `module_custom_instructions.sql_generation`
field of your semantic view YAML. This field takes precedence over the legacy
`custom_instructions` field when both are set.

Copy code

```
CREATE OR REPLACE SEMANTIC VIEW my_db.my_schema.my_view
  FROM @my_stage/semantic_view.yaml;
```

Copy code

```
# semantic_view.yaml
name: my_view
module_custom_instructions:
  sql_generation: |
    <chart_customization>
    Always use a line chart for time series data.
    vega_template:
    {
      "transform": [
        {
          "calculate": "datum.CATEGORY === 'Furniture' ? '#4e79a7' : datum.CATEGORY === 'Technology' ? '#f28e2b' : datum.CATEGORY === 'Office Supplies' ? '#e15759' : ''",
          "as": "_color"
        }
      ],
      "encoding": {
        "color": { "field": "CATEGORY", "type": "nominal", "scale": { "range": { "field": "_color" } } }
      }
    }
    </chart_customization>
tables:
  ...
```

Use the semantic view level for:

- Per-column color mappings
- Domain-specific chart type rules
- Metric-specific formatting
- Overriding agent-level defaults

## Use with caution: templates affect every chart

`vega_template` is merged into **every chart** generated at that level. There’s no per-question
or per-chart-type filtering. If you add an `encoding.y` override at the agent level, it applies
to bar charts, line charts, scatter plots, and pie charts alike.

Before adding a template, consider:

- **Scope**: Agent-level templates affect all charts across all semantic views. Prefer the semantic
  view level when a rule is specific to one domain or dataset.
- **Wildcard encodings**: A template encoding that omits `field` (for example,
  `"y": {"axis": {"format": "..."}}`) applies to every chart’s `y` axis regardless of what
  column is plotted. Use `field` to pin it to a specific column when the semantic view is known.
- **Mark overrides**: Setting `"mark": "line"` at the agent level forces every chart to a line,
  including ones where the LLM would correctly choose a bar or pie. Only override `mark` at the
  semantic view level where you have domain knowledge about the data.
- **Transform arrays**: A `calculate` transform in the template (for example, `_color`) is
  injected into every chart’s `transform` array. If the data doesn’t contain the referenced
  column, Vega-Lite silently produces `null` values for the calculated field.

When in doubt, start at the semantic view level and promote to the agent level only after
confirming the rule is safe for all charts.

To validate a template before deploying it, paste a representative chart spec (with your
`vega_template` already merged in) into the
[Vega Editor](https://vega.github.io/editor). The editor shows live warnings and errors in the
console. A valid template should produce no warnings. Common things to catch this way: invalid
property names, type mismatches, unreachable `calculate` expressions, and scale configuration
errors.

## Fonts

Font settings are controlled through the `config` block in `vega_template`. All font properties
are applied globally to the chart and affect every chart generated, regardless of data.

Note

Use CSS generic font families for maximum compatibility. Charts in Snowflake CoWork are
rendered in two contexts: in the Snowsight browser UI (client-side, fonts depend on the user’s
OS and browser) and server-side in a Linux container for validation and image export. Named fonts
like `Arial` or `Georgia` might not be installed in the server-side container. CSS generic
families always resolve correctly in both contexts:

| Generic family | Resolves to |
| --- | --- |
| `sans-serif` | Arial (Windows/macOS), DejaVu Sans or Liberation Sans (Linux) |
| `serif` | Times New Roman (Windows/macOS), DejaVu Serif or Liberation Serif (Linux) |
| `monospace` | Courier New (Windows/macOS), DejaVu Sans Mono or Liberation Mono (Linux) |

Expand

Show lessSee more

If you need a custom brand font, it must be installed in the server-side rendering container
**and** served through CSS `@font-face` in Snowsight.

Copy code

```
{
  "config": {
    "title":  { "font": "serif", "fontSize": 20, "fontWeight": "bold", "fontStyle": "italic" },
    "axis":   { "labelFont": "monospace", "titleFont": "monospace", "labelFontSize": 11, "titleFontSize": 13 },
    "header": { "labelFont": "serif", "titleFont": "serif", "labelFontSize": 11 },
    "legend": { "labelFont": "serif", "titleFont": "serif", "labelFontSize": 12, "titleFontSize": 13 },
    "mark":   { "font": "serif" }
  }
}
```

Common `config` font properties:

| Property | Where it applies |
| --- | --- |
| `title.font`, `title.fontSize`, `title.fontWeight`, `title.fontStyle` | Chart title |
| `axis.labelFont`, `axis.labelFontSize` | Axis tick labels |
| `axis.titleFont`, `axis.titleFontSize` | Axis titles (for example, “Revenue”) |
| `header.labelFont`, `header.labelFontSize` | Facet / small-multiple headers |
| `legend.labelFont`, `legend.labelFontSize` | Legend value labels |
| `legend.titleFont`, `legend.titleFontSize` | Legend title |
| `mark.font` | Text marks (annotations) |

Expand

Show lessSee more

You can also set a global `background` color alongside fonts:

Copy code

```
{
  "background": "#f9f9f9",
  "config": {
    "title":  { "font": "monospace", "fontStyle": "italic", "fontSize": 20, "fontWeight": "lighter" },
    "axis":   { "labelFont": "monospace", "titleFont": "monospace", "titleFontSize": 15, "labelFontSize": 10 },
    "header": { "labelFont": "monospace", "titleFont": "monospace", "labelFontSize": 10 },
    "legend": { "labelFont": "monospace", "titleFont": "monospace", "titleFontSize": 18, "labelFontSize": 15 },
    "mark":   { "font": "monospace" }
  }
}
```

## Colors

### LLM instructions (soft)

The simplest way to apply color rules is to describe them in free text. The LLM interprets these
on a best-effort basis.

Copy code

```
<chart_customization>
Color Active status green, Inactive status red, and Pending status yellow.
</chart_customization>
```

Use this for quick, approximate color guidance when exact hex values aren’t required.

### Exact value mapping with \_color

Map specific column values to exact hex colors using a `calculate` transform. Values not listed
receive an empty string, and Vega-Lite renders those with its own default.

Copy code

```
{
  "transform": [
    {
      "calculate": "datum.STATUS === 'Active' ? '#22c55e' : datum.STATUS === 'Inactive' ? '#ef4444' : datum.STATUS === 'Pending' ? '#eab308' : ''",
      "as": "_color"
    }
  ],
  "encoding": {
    "color": {
      "field": "STATUS",
      "type": "nominal",
      "scale": { "range": { "field": "_color" } }
    }
  }
}
```

Use this when you need exact, guaranteed colors for every known value.

Note

The `_color` transform and the `encoding.color` block are always merged into the chart,
regardless of which column the LLM chose to color by. This means:

- The mapping only works correctly when the chart’s color channel actually uses the same column
  referenced in the `calculate` expression (for example, `STATUS`). If the LLM assigns color
  to a different column, the `_color` field is present in the data but the colors don’t match.
- Only one column can be targeted per template.

### Pinned values with palette fallback

Pin colors for key values and let the rest be auto-assigned from a palette. Use
`"merge": "extend"` to preserve the LLM’s existing color choices and only add new mappings.

Copy code

```
{
  "encoding": {
    "color": {
      "scale": {
        "domain": ["Furniture", "Technology", "Office Supplies"],
        "range":  ["#4e79a7", "#f28e2b", "#e15759"],
        "scheme": "tableau10"
      }
    }
  },
  "usermeta": { "merge": "extend" }
}
```

Data values not in `domain` are automatically assigned the next available color from `scheme`.
After assignment, `scheme` is removed from the final spec.

Supported scheme names: `tableau10`, `tableau20`, `category10`, `category20`,
`category20b`, `category20c`, `dark2`, `paired`, `pastel1`, `pastel2`, `set1`,
`set2`, `set3`, `accent`.

## Disabling Snowsight styling

By default, Snowflake CoWork applies Snowsight UI theme adjustments on top of the generated chart.
To opt out and render the chart exactly as specified in your `vega_template`, set `ui-merge` to
`"none"` in `usermeta`:

Copy code

```
{
  "usermeta": { "ui-merge": "none" }
}
```

This is useful when you want full control over the visual output, for example, when applying a
custom brand theme and you don’t want Snowsight to override colors, fonts, or backgrounds.

Note

`ui-merge` is interpreted by the Snowsight client-side renderer, not by the orchestrator
backend. It has no effect on the chart spec produced by the merge engine. It only controls how
Snowsight applies its own theme on top of the final spec when displaying the chart in the
browser.

## Number and currency formatting (experimental)

Axis and legend labels can be formatted using [D3 format strings](https://d3js.org/d3-format)
through `vega_template`. This is useful for enforcing consistent currency symbols, decimal
places, or SI suffixes across all charts.

Set `axis.format` for quantitative axes (`x`, `y`) and `legend.format` for color/size
legends:

Copy code

```
{
  "encoding": {
    "y": { "axis": { "format": "$,.0f" } }
  }
}
```

Note

`axis.format` is applied by Vega-Lite only when the channel’s data type is
`"quantitative"`. If the LLM infers a different type (for example, `"ordinal"` for a year
or ID column), the format string is silently ignored. This is an accepted limitation of the
`vega_template` approach because the merge is applied without inspecting inferred types.

**Workaround**: Force the type explicitly in the template (`override` mode):

Copy code

```
{
  "encoding": {
    "y": { "type": "quantitative", "axis": { "format": "$,.0f" } }
  }
}
```

This guarantees the format applies but may affect other type-dependent rendering (axis ticks,
binning).

Common D3 format strings:

| Format | Output example | Use for |
| --- | --- | --- |
| `$,.0f` | $1,234,567 | Dollar amounts, no decimals |
| `$,.2f` | $1,234,567.89 | Dollar amounts, 2 decimals |
| `,.0f` | 1,234,567 | Large integers with thousands separator |
| `.1%` | 42.3% | Percentages |
| `.2s` | 1.2M | Large numbers with SI prefix |
| `.2f` | 3.14 | Fixed 2 decimal places |

Expand

Show lessSee more

To apply formatting to all quantitative channels at the agent level (without knowing the specific
column name):

Copy code

```
{
  "encoding": {
    "y": { "axis": { "format": "$,.0f" } },
    "x": { "axis": { "format": "$,.0f" } },
    "color": { "legend": { "format": "$,.0f" } }
  },
  "usermeta": { "merge": "extend" }
}
```

Use `"merge": "extend"` so the format is added only to channels the LLM already populated,
without overwriting their `field` or `type` settings.

## Merge modes

Control how `vega_template` interacts with the LLM-generated chart by setting
`"usermeta": {"merge": "<mode>"}` inside the template.

| Mode | Behavior |
| --- | --- |
| `override` (default) | Template values overwrite the chart. Use when you need to enforce a specific setting. |
| `extend` | Existing chart values are preserved. New keys and additional scale entries are added. Use when you want to add to the chart without replacing what the LLM chose. |

Expand

Show lessSee more

Rules that apply to both modes:

- The `data` block is never overwritten.
- Encoding overrides apply only when the template’s `field` matches the chart’s `field`, or the
  template omits `field`.
- After merging, domain entries not present in the actual data are automatically removed.

**Example: force a line chart**

Copy code

```
{
  "mark": "line",
  "usermeta": { "merge": "override" }
}
```
