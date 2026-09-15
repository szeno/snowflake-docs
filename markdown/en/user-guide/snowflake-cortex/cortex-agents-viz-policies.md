# Visualization policies for chart customization in Snowflake CoWork

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Visualization policies let you define conditional chart rules that fire only when specific conditions are
met, for example, “apply brand colors only when the CATEGORY column is used for color.” This is
more precise than a `vega_template`, which always applies to every chart unconditionally.

For general chart customization information, see
[Customize charts in Snowflake CoWork](/user-guide/snowflake-cortex/snowflake-cowork/chart-customization).

## How it works

Each policy has:

- **Rules**: Conditions that must all be true for the policy to fire. Omit rules to match every
  chart.
- **Actions**: What to apply when the policy fires.

Policies are evaluated after the chart is generated and actions are applied directly to the chart
spec.

## Where to define policies

Add a `viz_policies:` marker inside a `<chart_customization>` block, followed by a JSON array.
Policies can be defined at the agent level or the semantic view level.

Copy code

```
<chart_customization>
viz_policies:
[
  { "name": "my_policy", "rules": [...], "actions": [...] }
]
</chart_customization>
```

When an agent-level policy and a semantic view policy share the same `name`, the semantic view
policy wins.

### Full semantic view example

Copy code

```
module_custom_instructions:
  sql_generation: |
    <chart_customization>
    viz_policies:
    [
      {
        "name": "brand_colors",
        "rules": [{ "column": "CATEGORY", "role": "COLOR" }],
        "actions": [{
          "type": "ensure_color",
          "params": {
            "mapping": {
              "Furniture":       "#4e79a7",
              "Technology":      "#f28e2b",
              "Office Supplies": "#e15759"
            }
          }
        }]
      },
      {
        "name": "revenue_format",
        "rules": [{ "column": "REVENUE", "role": "Y_AXIS" }],
        "actions": [{
          "type": "ensure_number_format",
          "params": { "format": "$,.0f", "channel": "y" }
        }]
      }
    ]
    </chart_customization>
```

## Rules

Each rule can match on:

| Field | Description | Example values |
| --- | --- | --- |
| `column` | Column name (case-insensitive). Omit to match any column. | `"REVENUE"`, `"STATUS"` |
| `role` | Where the column is used in the chart. Omit to match any role. | `X_AXIS`, `Y_AXIS`, `COLOR`, `FILL`, `STROKE`, `SHAPE`, `SIZE`, `TOOLTIP`, `THETA` |
| `viz_type` | Chart type. Omit to match any chart type. | `bar`, `line`, `arc`, `point`, `rect` |
| `negate` | When `true`, the rule matches when the condition is **not** met. | `true`, `false` |

Expand

Show lessSee more

Multiple rules in one policy are combined with AND. All rules must match for the policy to fire.

### Role values

| Value | Vega-Lite channels matched |
| --- | --- |
| `X_AXIS` | `x`, `x2` |
| `Y_AXIS` | `y`, `y2` |
| `COLOR` | `color` |
| `FILL` | `fill` |
| `STROKE` | `stroke` |
| `SHAPE` | `shape` |
| `SIZE` | `size` |
| `TOOLTIP` | `tooltip` |
| `THETA` | `theta` |

Expand

Show lessSee more

`COLOR`, `FILL`, and `STROKE` are separate roles. `ensure_color` checks all three channels
(`color`, `fill`, `stroke`) and applies to whichever one is present, but in rules they are
distinct: use `COLOR` for the `color` channel, `FILL` for `fill`, and so on.

Important

The `column` field must match the **raw column name as it appears in the data** (for example,
`"REVENUE"`, `"ORDER_STATUS"`), not a display label or alias. Column matching is
case-insensitive.

Be aware that the LLM may rename or alias columns in the generated SQL (for example, selecting
`SUM(REVENUE) AS TOTAL`). In that case the column in the chart is `TOTAL`, not
`REVENUE`, and the rule doesn’t fire. To avoid this, use explicit column aliases in your
semantic view metrics definitions, or use the `role` field alone (without `column`) to match
by encoding position instead of by name.

## Actions

All actions are applied directly to the chart spec. They’re deterministic and add no latency.

| Action | What it does |
| --- | --- |
| `ensure_color` | Maps column values to specific hex colors |
| `ensure_shape` | Maps column values to point shapes (scatter plots only) |
| `ensure_number_format` | Applies a D3 format string to an axis or legend |
| `ensure_sort` | Overrides the sort order on an encoding channel |
| `ensure_axis_range` | Pins the minimum or maximum of an axis scale |

Expand

Show lessSee more

### ensure\_color

Maps column values to specific hex colors. Unmapped values are auto-assigned colors from the
chart’s existing palette.

Copy code

```
{
  "type": "ensure_color",
  "params": {
    "mapping": {
      "Active":   "#22c55e",
      "Inactive": "#ef4444",
      "Pending":  "#eab308"
    }
  }
}
```

| Param | Required | Description |
| --- | --- | --- |
| `mapping` | Yes | Column value to hex color |

Expand

Show lessSee more

### ensure\_shape

Maps column values to point shapes on scatter plots.

Copy code

```
{
  "type": "ensure_shape",
  "params": {
    "mapping": {
      "Active":   "circle",
      "Inactive": "square",
      "Pending":  "diamond"
    }
  }
}
```

Supported shapes: `circle`, `square`, `diamond`, `triangle-up`, `triangle-down`,
`triangle-right`, `triangle-left`, `cross`, `star`.

Note

`ensure_shape` only applies to scatter plots (`mark: point`). It’s silently skipped for all
other chart types.

### ensure\_number\_format

Formats an axis or legend using a [D3 format string](https://d3js.org/d3-format).

Copy code

```
{
  "type": "ensure_number_format",
  "params": {
    "format": "$,.0f",
    "channel": "y"
  }
}
```

| Param | Required | Description |
| --- | --- | --- |
| `format` | Yes | D3 format string. Examples: `$,.0f` (dollars), `.1%` (percent), `.2s` (1.2M) |
| `channel` | No | Axis channels: `x`, `y`, `x2`, `y2` (writes to `axis.format`). Legend channels: `color`, `size`, `opacity` (writes to `legend.format`). Omit to apply to all quantitative channels present in the chart. |

Expand

Show lessSee more

### ensure\_sort

Overrides the sort order on an encoding channel.

Copy code

```
{
  "type": "ensure_sort",
  "params": {
    "channel": "x",
    "order": "descending"
  }
}
```

For a fixed sequence (for example, fiscal quarters or lifecycle stages):

Copy code

```
{
  "type": "ensure_sort",
  "params": {
    "channel": "x",
    "custom_order": ["Q1", "Q2", "Q3", "Q4"]
  }
}
```

| Param | Required | Description |
| --- | --- | --- |
| `channel` | No | Encoding channel to sort. Default: `y` |
| `order` | No | `ascending`, `descending`, or `none` (preserves SQL row order) |
| `custom_order` | No | Explicit value sequence. When set, `order` is ignored. |

Expand

Show lessSee more

### ensure\_axis\_range

Pins the minimum or maximum of an axis scale.

Copy code

```
{
  "type": "ensure_axis_range",
  "params": {
    "channel": "y",
    "min": 0
  }
}
```

| Param | Required | Description |
| --- | --- | --- |
| `channel` | No | `x` or `y`. Default: `y` |
| `min` | No | Minimum scale value |
| `max` | No | Maximum scale value |

Expand

Show lessSee more

## Examples

### Brand colors when CATEGORY is on the color channel

Copy code

```
[
  {
    "name": "brand_colors",
    "rules": [
      { "column": "CATEGORY", "role": "COLOR" }
    ],
    "actions": [
      {
        "type": "ensure_color",
        "params": {
          "mapping": {
            "Furniture":       "#4e79a7",
            "Technology":      "#f28e2b",
            "Office Supplies": "#e15759"
          }
        }
      }
    ]
  }
]
```

### Dollar formatting and descending sort for REVENUE

Copy code

```
[
  {
    "name": "revenue_formatting",
    "rules": [
      { "column": "REVENUE", "role": "Y_AXIS" }
    ],
    "actions": [
      {
        "type": "ensure_number_format",
        "params": { "format": "$,.0f", "channel": "y" }
      },
      {
        "type": "ensure_sort",
        "params": { "channel": "y", "order": "descending" }
      }
    ]
  }
]
```

### Apply descending sort only when QUARTER is not on the X axis

`negate: true` inverts a rule. The policy fires when the condition is **not** met. This is
useful for applying a default that should be skipped when a specific column is already present.

Copy code

```
[
  {
    "name": "default_descending_unless_quarter",
    "rules": [
      { "column": "QUARTER", "role": "X_AXIS", "negate": true }
    ],
    "actions": [
      {
        "type": "ensure_sort",
        "params": { "channel": "y", "order": "descending" }
      }
    ]
  }
]
```

The policy fires and sorts descending on every chart **except** those where `QUARTER` is on the
X axis (where chronological order should be preserved instead).

### Force Y-axis to start at zero for bar charts

Copy code

```
[
  {
    "name": "bar_zero_baseline",
    "rules": [
      { "viz_type": "bar" }
    ],
    "actions": [
      {
        "type": "ensure_axis_range",
        "params": { "channel": "y", "min": 0 }
      }
    ]
  }
]
```

## Known limitations

- **Column aliasing can prevent rules from matching.** The `column` field in a rule matches the
  column name as it appears in the chart’s encoding, not the original table column. If the LLM
  aliases a column in the SQL (for example, `SUM(REVENUE) AS TOTAL`), a rule with
  `"column": "REVENUE"` doesn’t fire because the chart’s field is `TOTAL`. To avoid this,
  define explicit column aliases in your semantic view metrics, or use `role` alone (without
  `column`) to match by encoding position.
- **Multiple ensure\_color actions silently overwrite each other.** If two policies both fire
  `ensure_color` on the same chart, the second one replaces the first’s `_color` transform.
  No warning is surfaced. The same applies to `ensure_shape` with `_shape`. To avoid this,
  write mutually exclusive rules (for example, each `ensure_color` policy should include
  `"role": "COLOR"` with a distinct `"column"`).
- **Typos in parameter names are silently ignored.** If a parameter key is misspelled (for example,
  `"chanell"` instead of `"channel"`), the action still runs using default values for the
  missing parameter. A warning is logged server-side but no feedback is visible to the user.
  Double-check parameter names against the documented schemas.

## Notes

- Multiple actions in one policy all execute when the policy fires.
- Multiple policies can fire on the same chart. They’re applied in order.
- A semantic view policy with the same `name` as an agent-level policy replaces it.
