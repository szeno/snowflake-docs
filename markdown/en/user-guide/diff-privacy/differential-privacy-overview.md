# Differential privacy in Snowflake

[Enterprise Edition Feature](/user-guide/intro-editions)

This feature requires Enterprise Edition (or higher). To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Differential privacy is a widely recognized standard for data privacy that limits the risk that a user could leak sensitive information
from a sensitive dataset. It protects the identity and information of individual entities in the data, for example, people, corporations,
and locations. While each individual entity’s information is protected, differential privacy still lets data consumers learn
statistics, trends, and behaviors about groups of individuals.

Differential privacy provides strong protection against re-identification that is particularly effective against targeted privacy attacks.
This protection lets you share sensitive data across teams, outside of your organization, and across regulatory lines. Differential
privacy mitigates the increased re-identification risk associated with joining two sensitive datasets, adding new fields, unmasking existing
fields, or providing individual rows instead of pre-aggregated data.

Unlike other privacy methodologies, differential privacy does the following:

- Protects against targeted privacy attacks, for example differencing and amplification attacks.
- Quantifies and manages the trade-off between privacy and utility, that is, controls how much non-sensitive information data consumers
  can learn about the data.
- Removes the need for data providers to transform sensitive data to reduce re-identification risk (for example, masking,
  redaction, and bucketing).

## How does differential privacy protect sensitive information?

Under differential privacy, query results must not reveal information that could be used to identify an individual entity. Snowflake does
the following to enforce differential privacy:

- [Returns noisy aggregates](#label-diff-privacy-noisy-aggregates).
- [Limits privacy loss](#label-diff-privacy-loss-budgets).

### Noisy aggregates

Differentially private queries must aggregate data to return results; row-level queries like `SELECT *` are blocked. These aggregates
are noisy; they’re not the exact result of a computation. Noise (that is, variation or randomization) is introduced into the result to
obscure whether any particular row or entity was included in the aggregation.

The addition of noise protects against privacy attacks like thin-slicing and differencing. The amount of noise that’s added to the query
result depends on several factors that influence the sensitivity of the query, including the number of records queried, type of aggregate,
and types of data transformations. Snowflake calculates the sensitivity of a query based on rigorous mathematics, but it can be understood
loosely as the query’s potential to leak information about an individual entity. In general, less-sensitive queries have less noise,
potentially to the point that it’s statistically negligible. Very sensitive queries, for example a query that tries to single out an
individual entity, have a large amount of noise to prevent sensitive information from being leaked.

Snowflake does not introduce noise into intermediate aggregations that occur before the final aggregation of the query; noise is only
introduced once per query.

Snowflake considers the number of rows in the privacy-protected table to be public. For example, executing `SELECT COUNT(*) FROM t`, where
table `t` is protected by a privacy policy, returns an exact result without incurring any privacy loss.

For more information about how to understand the level of noise, see [Understanding query results](/user-guide/diff-privacy/differential-privacy-analyst#label-diff-privacy-understand-results).

### Limiting privacy loss

Every query against a protected dataset can result in the exposure of private information associated with an individual, including the
noisy aggregate results that differentially private queries produce. In differential privacy, this disclosure of information is known as
*privacy loss*, and is a quantifiable unit of measure. The more private information that is revealed by a query, the higher the privacy
loss associated with that query. Because privacy loss is quantifiable, Snowflake can use differential privacy to protect sensitive data
across a history of queries up to a certain degree of statistical confidence.

Privacy loss accumulates as a user executes queries against the protected data. When the cumulative privacy loss reaches a certain
threshold, subsequently letting the user see more results would theoretically let them identify individuals with an unacceptable level of
confidence. A *privacy budget* sets a limit on how much privacy loss is acceptable. Snowflake tallies the privacy loss of the queries
executed by a user or group of users and makes sure that tally never exceeds the privacy budget associated with those users. When the
user’s privacy budget reaches the budget limit set by the privacy policy creator, queries submitted by that user fail until that user’s budget is
refreshed. Snowflake offers a customizable privacy budget with a default value that sets the privacy loss threshold and the
refresh period.

Snowflake uses a [privacy policy](/user-guide/diff-privacy/differential-privacy-admin-privacy-policies), which is a schema-level
object, to associate a privacy budget with a user or group of users. When an administrator assigns that privacy policy to a table or view,
it becomes *privacy-protected*. When a user runs a query against a privacy-protected table, Snowflake uses the privacy policy to determine
which privacy budget is associated with the user and ensures that the privacy loss the query incurs will not exceed the budget’s limit.

## Differential privacy in theory vs. in practice

The standard of differential privacy comes from academic literature, and was formulated to have strong, mathematically proven privacy
guarantees, particularly against theoretical privacy attacks. In particular, privacy settings like privacy budget are set more conservatively
when discussed in academic settings. These settings favor strong protection against theoretical privacy attacks, at the expense of data
utility (analytical fidelity, accuracy, and availability). When considering the tradeoff between privacy and utility for your use case,
including for highly sensitive data like PII and PHI, consider the following:

- Practical privacy attacks aren’t as effective as theoretical privacy attacks described in academic literature that assume that attackers
  have unlimited compute resources and access to all datasets except the one they’re attacking.
- Data consumers typically don’t want to intentionally launch attacks because the data provider can revoke the consumer’s data access, and
  the analytical value of the data is too high for them to risk losing it.

Snowflake has selected default settings that reasonably balance privacy protection and utility in line with the goals of real-world use
cases, but you can always set different settings to meet your specific needs.

## Differential privacy workflow

The following workflow consists of tasks performed by the data provider who is protecting their data with differential privacy
and tasks for an analyst who is querying the data after it’s protected.

**Data provider:**

- If you want to implement [entity-level privacy](/user-guide/diff-privacy/differential-privacy-admin#label-diff-privacy-admin-entity-privacy), structure your data to meet requirements.
- [Create a privacy policy](/user-guide/diff-privacy/differential-privacy-admin-privacy-policies#label-diff-privacy-admin-create) that associates privacy budgets with users based on factors like role or
  account.
- [Assign the privacy policy](/user-guide/diff-privacy/differential-privacy-admin-privacy-policies#label-diff-privacy-admin-assign) to a table or view so that queries must be differentially private.
- [Define a privacy domain](/user-guide/diff-privacy/differential-privacy-privacy-domains-admin#label-diff-privacy-admin-privacy-domains-create) for numerical and categorical columns in the
  privacy-protected table or view.
- Grant privileges to the analysts so that they can access the privacy-protected data.
- As analysts execute queries against the privacy-protected data, you can
  [manage the privacy budgets associated with the users](/user-guide/diff-privacy/differential-privacy-admin-privacy-budgets).

**Analyst:**

- [View the privacy domains](/user-guide/diff-privacy/differential-privacy-privacy-domains-admin#label-diff-privacy-domain-admin-view) that the data provider defined for the columns in the
  privacy-protected table to better understand the contents of the column.
- If the data provider forgot to set a privacy domain for a column that you want to use in an aggregation or in a GROUP BY clause,
  [specify the privacy domain for the column](/user-guide/diff-privacy/differential-privacy-privacy-domains-analyst#label-diff-privacy-analyst-privacy-domains-set).
- [Execute differentially private queries](/user-guide/diff-privacy/differential-privacy-analyst#label-diff-privacy-query-fundamentals) against privacy-protected tables and views.
- Use the noise interval to [help understand the results](/user-guide/diff-privacy/differential-privacy-analyst#label-diff-privacy-understand-results) of an aggregation.
- If desired, [narrow the data provider’s privacy domain](/user-guide/diff-privacy/differential-privacy-privacy-domains-analyst#label-diff-privacy-analyst-privacy-domains-improve-results) to try to
  improve the results of the query.

## Limitations

- When a table is privacy-protected, analysts can only query the following data types:

  - [Numeric data types](/sql-reference/data-types-numeric)
  - [String data types](/sql-reference/data-types-text). Binary types are not supported.
  - [Logical data types](/sql-reference/data-types-logical)
  - [Date & time data types](/sql-reference/data-types-datetime). For timestamps, only TIMESTAMP\_NTZ is supported.
- Some Snowflake features are currently not supported when using differential privacy. For details, see [Interactions with Snowflake features](/user-guide/diff-privacy/differential-privacy-admin#label-diff-privacy-admin-snowflake-features).
- Query functionality is limited in order to protect privacy. For a list of supported operators, query syntax, and functions,
  see [Differential privacy SQL reference](/user-guide/diff-privacy/differential-privacy-sql-reference).
- When a query is run on a privacy-protected table, Snowflake first calculates statistics that influence how much noise will be added, then
  it runs the query. If the data changes in between these two steps, the amount of noise added may be incorrect. Snowflake recommends that
  data providers schedule data updates so that they don’t occur when analysts can run queries.

## Next steps

If you’re a data provider who is using differential privacy to protect your dataset, see [Implementing differential privacy](/user-guide/diff-privacy/differential-privacy-admin).

If you’re an analyst who is querying a dataset that’s protected by differential privacy, see [Querying data protected by differential privacy](/user-guide/diff-privacy/differential-privacy-analyst).
