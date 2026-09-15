# Notice of planned future deprecation: Snowpipe Streaming classic architecture

## Important service update: Advance notice of planned deprecation

**Action required:** Begin reviewing migration resources.

Snowflake is providing advance notice regarding the planned deprecation of the Snowpipe Streaming classic architecture.
This strategic transition is necessary because the successor platform, the
[Snowpipe Streaming high-performance architecture](/user-guide/snowpipe-streaming/snowpipe-streaming-high-performance-overview),
fundamentally supersedes the classic version by providing greater performance, scalability, and stability.
Moving forward, all innovation and major enhancements are built exclusively on the high-performance architecture.

To ensure that every customer benefits from the most modern and capable platform, Snowflake will eventually retire the classic architecture.

## What this means for you today

**No immediate action is required.**

- Your existing pipelines are safe. The classic architecture isn’t deprecated today, and your current workloads continue to operate normally.
- Support continues uninterrupted. Your current service level agreements (SLAs) and support models remain unchanged.

## Expected timeline and migration window

To ensure you have a well-supported transition, Snowflake is finalizing the official deprecation timeline:

- Snowflake plans to issue a formal deprecation announcement in mid-2026.
- This forthcoming formal announcement will provide you with the full transition timeline, specific milestones,
  detailed migration guides, and the final end-of-life date.
- After the formal deprecation is announced, an 18-month sunset period begins. This period is provided to give your engineering
  teams time to plan, test, and safely migrate your workloads.

## Special note for Kafka Connect users

If you rely on the Snowflake Kafka Connector to stream data, the
[Snowflake Connector for Kafka (v4)](/user-guide/kafka-connector/index)
natively supports the high-performance architecture:

- The [Snowflake Connector for Kafka (v4)](/user-guide/kafka-connector/index) is now generally available
  and natively uses the high-performance architecture.
- For migration guidance from the classic Kafka connector (v3), see
  [Migrate from v3 to v4](/user-guide/kafka-connector/migrate-v3-to-v4).
- Snowflake intends to fully upgrade all Snowflake-supported connectors to the high-performance architecture before deprecation.

## Frequently asked questions (FAQs)

Do I need to change anything right now?
:   No immediate changes are required. This is an advance notice to encourage you to begin planning and conduct early
    validation when you’re ready.

Is there a replacement?
:   Yes. The [Snowpipe Streaming high-performance architecture](/user-guide/snowpipe-streaming/snowpipe-streaming-high-performance-overview) is
    the recommended path forward.

How should I plan my migration if I use a third-party connector?
:   Third-party connectors are encouraged to begin migrating or planning to migrate as part of this notice.

Where can I find more information?
:   Snowflake strongly recommends that you begin assessing your current pipelines now and prioritize upgrading to the
    high-performance architecture where possible. To get started, review the following resources:

    - [High-performance architecture overview](/user-guide/snowpipe-streaming/snowpipe-streaming-high-performance-overview)
    - [Migration guide](/user-guide/snowpipe-streaming/snowpipe-streaming-high-performance-migration)

## Contact us

For general questions regarding this strategic transition, reach out to [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).
