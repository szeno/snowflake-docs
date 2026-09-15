# Onboarding questions in Cortex Analyst

Transition to Cortex Agents

Snowflake recommends transitioning to [Cortex Agents](/user-guide/snowflake-cortex/cortex-agents), which supports every Cortex Analyst capability with higher answer quality.

The *onboarding questions* feature in Cortex Analyst provides relevant suggestions for questions your users can ask while
interacting with your Cortex Analyst–powered conversational app, which will help them get started.

## How onboarding questions work

Cortex Analyst operates in one of three modes, depending on the configuration of your semantic model:

1. Generates questions using **Large Language Models** (Default mode without Verified Query Repository)
   When your semantic model doesn’t include a Verified Query Repository (VQR), Cortex Analyst uses the
   underlying Large Language Models (LLMs) to generate up to three suggested questions.
   Note that these questions may not always be answerable; for instance, the system might suggest a question that
   yields no results.
2. Suggests questions from the **Verified Query Repository** (Default mode with VQR)
   If your semantic model has a [Verified Query Repository (VQR)](/user-guide/views-semantic/verified-query-repository)
   defined, Cortex Analyst returns up to five suggested questions from the VQR. These questions are selected based on their similarity to
   the user’s input. For example, if a user asks, `What questions can I ask about revenue?`, Cortex Analyst returns up to five questions
   that are most likely about revenue from the VQR repository that are most likely answerable.
3. Returns **onboarding questions** configured in the semantic model (Customizable Mode with VQR)
   For more control over which questions are displayed, you can use the new `use_as_onboarding_question` flag in your VQR configuration.

   - When this flag is set to `true`, Cortex Analyst returns **all** questions marked as onboarding questions, regardless of their
     similarity to the user’s input.
   - This feature is helpful if you want to present a full set of predefined, answerable questions for users, such as in an
     onboarding experience. If you flag more than five questions, all of the flagged questions are returned in the response.

## How to configure onboarding questions

To define onboarding questions, you need to mark specific verified queries in the
semantic model with the `use_as_onboarding_question` flag. The example below shows how to set this up:

Copy code

```
verified_queries:

- name: "lowest revenue each month"
  question: For each month, what was the lowest daily revenue and on what date did that lowest revenue occur?

  use_as_onboarding_question: true

  sql: "WITH monthly_min_revenue AS (
SELECT
    DATE_TRUNC('MONTH', date) AS month,
    MIN(daily_revenue) AS min_revenue
FROM \__daily_revenue
GROUP BY
DATE_TRUNC('MONTH', date)

)

SELECT
    mmr.month,
    mmr.min_revenue,
    dr.date AS min_revenue_date
FROM monthly_min_revenue AS mmr JOIN \__daily_revenue AS dr
ON mmr.month = DATE_TRUNC('MONTH', dr.date)
AND mmr.min_revenue = dr.daily_revenue
ORDER BY mmr.month DESC NULLS LAST"

verified_at: 1715187400

verified_by: user_name
```
