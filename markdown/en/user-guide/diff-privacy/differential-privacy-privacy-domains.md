# About privacy domains

[Enterprise Edition Feature](/user-guide/intro-editions)

This feature requires Enterprise Edition (or higher). To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Within [differential privacy in Snowflake](/user-guide/diff-privacy/differential-privacy-overview), a *privacy domain* defines the possible
values in a column, similar to a mathematical domain. A privacy domain is either a range of values with a minimum and maximum or an
enumerated list of values.

The privacy domain is one factor that Snowflake uses to calculate the amount of [noise](/user-guide/diff-privacy/differential-privacy-overview#label-diff-privacy-noisy-aggregates) that
must be added to preserve privacy. Because of this, most fields should have a finite privacy domain; otherwise, the amount of noise added
would need to be infinite. By default, fields without privacy domains are assumed to have an infinite domain.

## Which columns need a privacy domain?

With the exception of a COUNT function, a query cannot aggregate a column unless the column has a privacy domain. Similarly, a query cannot
use a column in a GROUP BY clause unless the column has a privacy domain. For example, in the following query, score needs to have a
privacy domain, but age does not:

Copy code

```
SELECT COUNT(age) AS count_age where age >= 20 and age <= 100 FROM t1 GROUP BY score
```

## Defining a privacy domain

While both administrators and the analysts who are running queries can define a privacy domain for a column, they do so in different ways:

- An administrator uses CREATE TABLE and ALTER TABLE commands to set a privacy domain for a column. An administrator for the data provider
  sets privacy domains before giving access to analysts. [In some circumstances](/user-guide/diff-privacy/differential-privacy-analyst#label-diff-privacy-joins-data-types), an
  administrator for the analyst might also need to set privacy domains on tables being joined with the data provider’s protected tables. If
  you’re an administrator who needs to set privacy domains, see [Working with privacy domains as an administrator](/user-guide/diff-privacy/differential-privacy-privacy-domains-admin).
- An analyst shapes a query to implicitly specify a privacy domain using query elements like filters and column transformations. These
  privacy domains can be specified for columns without a privacy domain or can narrow a privacy domain set by the data provider. If you’re
  an analyst who needs to specify or narrow a privacy domain, see [Working with privacy domains as an analyst](/user-guide/diff-privacy/differential-privacy-privacy-domains-analyst).

## Interactions between privacy domains

Multiple privacy domains can be involved in a query. There can be an admin-specified privacy domain and an analyst-specified privacy
domain on the same column. Alternatively, a query might join two tables on a column that has a privacy domain in both tables.

Snowflake evaluates all privacy domains and calculates the privacy domain to use for the duration of the query. For information about
how this query-time privacy domain is determined, see:

- [Interaction between admin-specified and analyst-specified privacy domains](#label-diff-privacy-privacy-domains-provider-analyst-interaction)
- [Privacy domains and joins](#label-diff-privacy-privacy-domains-joins)

### Interaction between admin-specified and analyst-specified privacy domains

An analyst uses query elements to implicitly specify a privacy domain for a column. For example, filtering on a column defines a privacy
domain for it. This analyst-specified privacy domain exists only for the duration of the query; it doesn’t change the privacy domain that
an administrator set on the column.

An analyst-specified privacy domain can narrow an admin-specified privacy domain, but can never expand it. The query-time privacy domain
is the intersection between the privacy domain specified by the query and the privacy domain set by the administrator. For example, if the
data provider set the privacy domain as a range (5, 15) and the query uses filters to specify the privacy domain as a range (0, 10), then
the effective, query-time privacy domain is (5, 10).

Similarly, if the administrator set the privacy domain as a list ( ‘blue’, ‘yellow’ ) and the query uses filters to specify a
privacy domain of ( ‘orange’, ‘blue’) , the query-time privacy domain is ( ‘blue’ ).

### Privacy domains and joins

When an analyst joins two tables on a column that has a privacy domain in both tables, the type of join determines the
query-time privacy domain. During the duration of the query, the effective privacy domain can be the intersection of the two privacy
domains, the union of the two privacy domains, or just one of the privacy domains.

In the following table, `domainL` refers to the privacy domain on the join column in the left table and `domainR` refers to the privacy
domain on the join column in the right table.

| Join type | Query-time privacy domain |
| --- | --- |
| INNER | Intersection of `domainL` and `domainR` |
| OUTER | Union of `domainL` and `domainR` |
| LEFT | `domainL` |
| RIGHT | `domainR` |
| LEFT SEMI | Intersection of `domainL` and `domainR` |
| LEFT ANTI | `domainL` |

Expand

Show lessSee more

For example, suppose the `day` column in `t1` has a privacy domain of (1, 100) and the `day` column in `t2` has a privacy domain of
(0, 90). When an analyst joins `t1` and `t2` on `day`, the query-time privacy domain is (1, 90), which is the intersection of the two
privacy domains.

## Values outside a privacy domain

A privacy domain defines *possible* values in a column, not necessarily *actual* values. The following summarizes what happens to values
that are not included in the list or range of the privacy domain.

Strings
:   Values in a string column that fall outside the privacy domain are always treated as NULL for the duration of the query. This is true
    regardless of whether it is an admin-specified privacy domain, an analyst-specified privacy domain, or an intersection of privacy
    domains.

    For example, suppose the data provider set a privacy domain on a column `state` of (`'california'`, `'oregon'`) and the analyst
    wrote a query that filters the `state` column to (`'nevada'`, `'oregon'`). If the query uses the `state` column in a GROUP BY
    clause, then the result contains two groups: `OREGON` and `NULL`. The `NULL` group includes all records where the value of
    the `state` column is not `OREGON` along with records where the value of the `state` column is literally `NULL`.

Numeric, date, and time
:   Snowflake treats numeric, date, and time values that fall outside the range of a privacy domain differently depending on
    whether the privacy domain was defined by an administrator or an analyst.

    Admin-specified:
    :   When the data provider defines a range privacy domain that contains a subset of the column’s actual values, the values outside the
        privacy domain are *clamped*, meaning they are treated as if they are the nearest value in the domain (the minimum or maximum
        value). For example, if the privacy domain of a column consists of integers between 1-100, a record with an actual value of 105 is
        treated as if it has a value of 100 when calculating aggregations. Analysts cannot access values outside the privacy domain.

        When a [join of two privacy-protected tables](#label-diff-privacy-privacy-domains-joins) results in the intersection of privacy
        domains, values outside the query-time privacy domain are clamped.

    Analyst-specified:
    :   When an analyst specifies a privacy domain for a column that doesn’t have one or narrows an admin-specified privacy domain, the
        query itself determines what happens to values that fall outside the privacy domain.

        - If the query uses a filter ([WHERE clause](/user-guide/diff-privacy/differential-privacy-privacy-domains-analyst#label-diff-privacy-analyst-privacy-domain-set-range-where)), values outside of
          the privacy domain are ignored when calculating aggregations.
        - If the query uses a [column transformation](/user-guide/diff-privacy/differential-privacy-privacy-domains-analyst#label-diff-privacy-analyst-privacy-domain-set-range-transformation), values in
          the column that are outside of the privacy domain are clamped like an admin-specified privacy domain.

## How intermediary query elements affect privacy domains

How a query is written can affect whether the range of a privacy domain changes or even whether a privacy domain still exists on a column.
This section helps you understand how intermediary parts of a query, that is, parts of the query before the final aggregation, can affect
the privacy domain of a column.

Adding new columns
:   If a query adds a new column that is based on an existing column, specifying or narrowing a privacy domain on the original column has no
    effect on the new column.

    In the following example, assume the data provider defined the privacy domain on the `score` column as a range between 0 and 100. When
    the query specifies the privacy domain of `score` as a range between 1 and 2, it has no effect on the privacy domain of the column
    `score_derived`.

    Copy code

    ```
    SELECT COUNT(score_derived)
      FROM (SELECT score, score_derived FROM t1 WHERE score <= 2);
    ```

    For example, the output might be:

    ```
    ----------------------------
    |"count(""SCORE_DERIVED"")"|
    ----------------------------
    |31                        |
    ----------------------------
    ```

Using a GROUP BY clause in intermediary aggregations
:   For intermediary portions of a query, using a GROUP BY clause while aggregating a column removes the privacy domain from the column. As a
    result, you need to specify a new privacy domain on the column if it is used in the final aggregation of the query.

    In the following example, the initial aggregation removes any privacy domain that has been set on the `score` column. The query
    succeeds only because it sets a privacy domain on the alias of the column before the final aggregation.

    Copy code

    ```
    SELECT COUNT(num_scores)
      FROM (SELECT COUNT(score) AS num_scores
        FROM t1
        GROUP BY age)
      WHERE num_scores >= 0 AND num_scores <= 100;
    ```
