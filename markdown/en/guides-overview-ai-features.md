# Snowflake AI and ML

Snowflake offers two broad categories of powerful, intelligent features based on Artificial Intelligence (AI) and
Machine Learning (ML). These features can help you do more with your data in less time than ever before.

- **Snowflake Cortex** is a suite of AI features that use large language models (LLMs) to understand unstructured data,
  answer freeform questions, and provide intelligent assistance. This suite of Snowflake AI Features comprises:

  - [Cortex Agents](/user-guide/snowflake-cortex/cortex-agents)
  - [Snowflake Cortex AI Functions (including LLM functions)](/user-guide/snowflake-cortex/aisql)
  - [Cortex Analyst](/user-guide/snowflake-cortex/cortex-analyst)
  - [Cortex Fine-tuning](/user-guide/snowflake-cortex/cortex-finetuning)
  - [Cortex Search](/user-guide/snowflake-cortex/cortex-search/cortex-search-overview)
  - [Snowflake CoWork](/user-guide/snowflake-cortex/snowflake-cowork)
  - [Cortex Code](/user-guide/cortex-code/cortex-code)
    - [Cortex Code in Snowsight](/user-guide/cortex-code/cortex-code-snowsight)
    - [Cortex Code CLI](/user-guide/cortex-code/cortex-code-cli)
      - [Cortex Code Agent SDK](/user-guide/cortex-code-agent-sdk/cortex-code-agent-sdk)
      - [Cortex Code CLI Model Context Protocol (MCP) support](/user-guide/cortex-code/cortex-code-mcp)
      - [Cortex Code CLI Agent Client Protocol (ACP) support](/user-guide/cortex-code/cortex-code-acp)
      - [Cortex Code CLI plugins](/user-guide/cortex-code/cortex-code-plugins)
  - [Cortex AI Guardrails](/user-guide/snowflake-cortex/cortex-ai-guardrails)
- **Snowflake ML** provides functionality for you to build your own models.

  - [ML Functions](/guides-overview-ml-functions) simplify the process of creating and using traditional machine
    learning models to detect patterns in your structured data. These powerful out-of-the-box analysis tools help
    time-strapped analysts, data engineers, and data scientists understand, predict, and classify data, without any
    programming.
  - For data scientists and developers, [Snowflake ML](/developer-guide/snowflake-ml/overview) lets you develop
    and operationalize custom models to solve your unique data challenges, while keeping your data inside Snowflake.
    Snowflake ML incorporates model development classes based on popular ML frameworks, along with ML Ops capabilities
    such as a feature store, a model registry, framework connectors, and immutable data snapshots.

## Use of Snowflake AI features

Snowflake AI Features and their underlying models are designed with the following principles in mind:

- **Full security.** Except as you elect, all AI models run inside of Snowflake’s security and governance perimeter. Your data is not
  available to other customers or model developers.
- **Data privacy.** Snowflake never uses your Customer Data to train models made available to our customer base.
- **Control.** You have control over your team’s use of Snowflake AI Features through familiar
  [role-based access control](/user-guide/security-access-control-overview).

## AI/ML model update process

Snowflake is continually working to improve the quality of its offerings, including the models powering the Snowflake AI Features.
This section describes how updates to those models fit into [Snowflake’s Behavior Change](/release-notes/intro-bcr-releases) process.

## Model Update and Behavior Change Policy

### Overview

Snowflake continuously updates the models that power Cortex AI features to improve quality,
performance, and availability. These updates may introduce changes to model behavior,
availability, or lifecycle status.

This document describes how model changes are defined, how they are communicated, and
how model lifecycle and deprecation are managed.

### Model lifecycle

Models in Cortex follow a defined lifecycle to communicate readiness and stability:

- Private Preview
- Public Preview
- General Availability (GA)
- Legacy
- End of Life (EOL)

Lifecycle status reflects the maturity and support level of a model. As models progress through
these stages, their status will be reflected across customer-facing surfaces.

Preview models are intended for evaluation and may change more frequently. GA models are
considered stable and suitable for production use.

### Types of model changes

A model update is considered a behavior change if it results in any of the following:

- Changes to required syntax, including specifying a model or model version
- Changes to the structure of model outputs
- Deprecation of a model

These changes may impact how customers interact with models and should be reviewed as part
of normal governance processes.

### How changes are communicated

Snowflake communicates model-related updates through the following mechanisms:

- [Behavior Change Releases (BCRs)](/release-notes/intro-bcr-releases) —
  Used for changes that may require customer action or impact existing workflows
- [What’s New](/release-notes/new-features) —
  Used for improvements or additions that do not materially change how customers
  interact with models

Model deprecations are communicated separately from bundled releases to provide clear and
timely notification.

### Deprecation policy

Snowflake periodically deprecates models to ensure customers have access to high-quality,
well-supported options.

For General Availability (GA) models:

- Snowflake will make reasonable efforts to provide at least 60 days advance notice prior
  to deprecation

For Preview models:

- Deprecation timelines are not guaranteed and may occur with shorter notice

During the deprecation period:

- Customers are expected to migrate to alternative models before the deprecation date
- After deprecation, models may no longer be available for use

Lifecycle status will reflect deprecation through the transition to Legacy and ultimately End of
Life.

### Legal notices

- If you choose to use any of the Snowflake AI Features, your use is subject to our
  [Acceptable Use Policy](https://www.snowflake.com/legal/acceptable-use-policy/).
- The outputs of Snowflake AI Features may be inaccurate, inappropriate, inefficient, or biased. Decisions based on such
  outputs, including those built into automatic pipelines, should have human oversight and review processes to ensure they are
  safe, accurate, and suitable for your intended use.
- Your use of any Snowflake AI Feature that is identified as being powered by a third-party, open-source model is subject to any
  applicable license agreement and/or acceptable use policy set forth under the Offering-Specific Terms page available at
  <https://www.snowflake.com/legal/>.
- For further information, see the [Snowflake AI Trust and Safety FAQ](https://www.snowflake.com/en/legal/snowflake-ai-trust-and-safety/).
