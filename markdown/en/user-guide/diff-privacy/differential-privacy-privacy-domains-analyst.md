# Working with privacy domains as an analyst

[Enterprise Edition Feature](/user-guide/intro-editions)

This feature requires Enterprise Edition (or higher). To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

A *privacy domain* defines the possible values in a column, similar to a mathematical domain. Snowflake uses a privacy domain to determine
how much noise to introduce into results.

To gain a complete understanding of privacy domains before completing the tasks in this section, see [About privacy domains](/user-guide/diff-privacy/differential-privacy-privacy-domains).

If the data provider followed best practices, most numerical and categorical columns in a privacy-protected table have a privacy domain.
If the data provider didn’t set one on a column that you want to aggregate or use in a GROUP BY clause, you need to shape your query
so that it includes techniques that implicitly specify a privacy domain for that column.
Privacy domains that the data provider set on the table can also be lost based on operations done on the table. For example, if you aggregate
a field in a subquery with GROUP BY, the system might not be able to derive a privacy domain due to privacy constraints.

You can also write your query to narrow a privacy domain set by the data provider. This override can help improve the results of your
aggregation.

Note

To meet the [requirements of joining](/user-guide/diff-privacy/differential-privacy-analyst#label-diff-privacy-joins-data-types) with a privacy-protected table, an analyst might need to
define a privacy domain for a column of their own table, even if it is not privacy-protected. These privacy domains are defined at the
table level, and apply to all queries against the table. If you are an administrator for the analyst and need to specify a privacy domain
for the column of one of your tables, see [Setting a privacy domain](/user-guide/diff-privacy/differential-privacy-privacy-domains-admin#label-diff-privacy-admin-privacy-domains-create).

## Viewing privacy domains

It’s useful to view the privacy domains of a privacy-protected table before querying the table. Checking the privacy domains for each
column can help in the following ways:

- Determine whether the data provider set a privacy domain for a column.
- Determine the possible values found in the column, which can help you improve your analysis. For example, if the privacy domain is a
  range of possible values found in the column, you can determine the minimum and maximum of the range.
- Investigate why you’re getting more [noise](/user-guide/diff-privacy/differential-privacy-overview#label-diff-privacy-noisy-aggregates) in your results than expected. You can identify
  whether there are outlier values that aren’t important to your analysis, and remove those values from your aggregation to
  [improve results](#label-diff-privacy-analyst-privacy-domains-improve-results).

To see whether a column has a privacy domain and, if it does, determine the type and possible values of the domain, see [View a privacy domain](/user-guide/diff-privacy/differential-privacy-privacy-domains-admin#label-diff-privacy-domain-admin-view).

## Specifying a privacy domain

This section describes the techniques an analyst can use to set a privacy domain for the duration of a query. It summarizes how the
structure of a query specifies a privacy domain for a column.

### Specify a privacy domain for string columns

Filtering on a string column using a WHERE clause specifies a privacy domain for it. The privacy domain consists of the values that match
the filter. For example, queries specify a privacy domain for the `product` column if they include the following clauses:

> Copy code
>
> ```
> WHERE product = 'hackeysack' OR product = 'frisbee'
> ```
>
> Copy code
>
> ```
> WHERE product IN ('hackeysack', 'frisbee')
> ```

The privacy domain is an enumerated list consisting of `hackeysack` and `frisbee`.

If the data provider already set a privacy domain on the `product` column, Snowflake uses the intersection of the two privacy domains for
the duration of the query. For information, see [Interaction between admin-specified and analyst-specified privacy domains](/user-guide/diff-privacy/differential-privacy-privacy-domains#label-diff-privacy-privacy-domains-provider-analyst-interaction).

Values outside of the privacy domain for string columns are [treated as NULL](/user-guide/diff-privacy/differential-privacy-privacy-domains#label-diff-privacy-privacy-domains-excluded-string).

### Specify a privacy domain for numeric, date, and time columns

You can use filtering clauses or column transformations to specify a privacy domain for a numeric, date, or time column. These query
techniques specify a privacy domain that’s a range of possible values.

You can use the following techniques to specify a privacy domain for a numeric, date, or time column:

WHERE clause
:   For example:

    Copy code

    ```
    WHERE a < 10 AND a >= 0
    ```

    The specified privacy domain of the column `a` is between 0 and 10.

    If the data provider already set a privacy domain on the `a` column, Snowflake uses the intersection of the two privacy domains
    for the duration of the query. For information, see [Interaction between admin-specified and analyst-specified privacy domains](/user-guide/diff-privacy/differential-privacy-privacy-domains#label-diff-privacy-privacy-domains-provider-analyst-interaction).

    Using a filter removes values that fall outside the privacy domain, meaning these values are ignored when calculating aggregations.
    For more information, see [Numeric, date, and time](/user-guide/diff-privacy/differential-privacy-privacy-domains#label-diff-privacy-privacy-domains-excluded-numeric).

GREATEST and LEAST column transformations
:   For example:

    Copy code

    ```
    GREATEST(LEAST(a, 100), 0) AS clamped_a
    ```

    The specified range of the privacy domain is between 0 and 100.

    If the data provider already set a privacy domain on the `a` column, Snowflake uses the intersection of the two privacy domains
    for the duration of the query. For information, see [Interaction between admin-specified and analyst-specified privacy domains](/user-guide/diff-privacy/differential-privacy-privacy-domains#label-diff-privacy-privacy-domains-provider-analyst-interaction).

    If you’re narrowing a privacy domain set by the data provider, you can use just one of the GREATEST or LEAST transformations to decrease
    the maximum or increase the minimum while keeping the other end of the range the same as the privacy domain defined by the data provider.

    Values in the column that are outside of the privacy domain are [clamped](/user-guide/diff-privacy/differential-privacy-privacy-domains#label-diff-privacy-privacy-domains-excluded-numeric),
    meaning they are treated as if they are the nearest value in the domain (the minimum or maximum value).

#### Narrowing a privacy domain to improve results

Snowflake must introduce enough [noise](/user-guide/diff-privacy/differential-privacy-overview#label-diff-privacy-noisy-aggregates) to hide exact values within a privacy domain. If the
privacy domain includes values that are outliers from most of the data in the column, Snowflake must increase the noise to obscure the
presence of those values. Overriding a privacy domain to narrow its range can reduce noise because Snowflake no longer needs to obscure
the presence of values that are not important to your analysis.

The technique you use to narrow a privacy domain affects how your aggregations are calculated. Your choice depends upon what is important
to your analysis.

- If you use a filter ([WHERE clause](/user-guide/diff-privacy/differential-privacy-privacy-domains-analyst#label-diff-privacy-analyst-privacy-domain-set-range-where)) to narrow the privacy domain, values
  outside of the domain are ignored when calculating aggregations.

  Using a filter is the preferred technique when you think the outlier values of a privacy domain are due to data quality issues, or if
  these values are not relevant to your query. Excluding the outlier values from the privacy domain can retain the integrity of your
  analysis while significantly reducing the noise introduced into your results.
- If you use a [column transformation](/user-guide/diff-privacy/differential-privacy-privacy-domains-analyst#label-diff-privacy-analyst-privacy-domain-set-range-transformation), values in the column
  that are outside of the domain are [clamped](/user-guide/diff-privacy/differential-privacy-privacy-domains#label-diff-privacy-privacy-domains-excluded-numeric), meaning they are treated as if
  they are the nearest value in the domain (the minimum or maximum value).

  Using a column transformation can improve your analysis even if you think the outlier values are not data quality issues. For example, if
  you are taking the average of values, clamping outlier values using a column transformation might improve your analysis.

Note

If your query includes highly selective filters that target a limited number of records in a dataset, the relative amount of noise
actually increases because Snowflake must ensure that you cannot use your results to identify an individual.
