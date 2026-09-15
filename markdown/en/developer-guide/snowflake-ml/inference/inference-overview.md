# Model Inference in Snowflake

Snowflake uses two distinct compute engines:

- The warehouse (SQL Engine)
- Snowpark Container Service

The Snowflake Model Registry provides a unified interface to both engines. The optimal environment for your use cases depends on your latency, data type, and scaling requirements. Snowflake offers the following approaches to your inference workflows:

**Real-time Inference (REST API):** Designed for low-latency and real-time use cases. Requests are facilitated via HTTP endpoints and are ideal for powering external applications.

**Snowflake Native Batch Inference (SQL):** Designed for batch workloads that require integration with the Snowflake SQL ecosystem. For example, batch workloads can integrate with Dynamic Tables, Snowpark, DBT, and User Tasks. You can use a SQL function, you can embed intelligence directly into your existing data pipelines without moving data or managing external infrastructure.

**Job-based Batch Inference:** This approach is designed for high-throughput, distributed processing where inference is treated as a standalone compute stage. By decoupling inference from the SQL engine, you can optimize for both price and performance. You can use Batch Inference to help you handle massive datasets or navigate complex computational requirements. This is ideal for processing files—such as images, video, and audio—directly from Snowflake Stages.

## When to choose

Use the following table to align your specific workload requirements with the correct compute pattern.

| Feature | Real-Time Inference (SPCS) | Native Batch Inference (SQL) | Job-Based Batch (SPCS) |
| --- | --- | --- | --- |
| Primary Goal | Interactive Responses: Low-latency, sub-second feedback for live users. | Inline Intelligence: Seamlessly embedding models into SQL data pipelines. | Standalone Processing: Large-scale, decoupled compute for unstructured data. |
| Best For… | • Web/Mobile app backends. • Real-time user interactions. • High-concurrency request spikes. | • Upstream pipelines (Dynamic Tables, Snowpark). • SQL-first users (Analysts/DEs). • Tools like dbt. | • Processing files (Images, Video, Audio). • Large-scale historical backfills. • Multi-modal data processing. |
| Data Source | Small inputs passed via HTTP payload. | Data residing in Snowflake Tables. | Data residing in Snowflake Stages (Files). |
| Scalability | Horizontal autoscaling to meet request volume. | Serverless scaling via Virtual Warehouses. | High-throughput distributed processing for bulk data. |
| Key Advantage | Zero-Ops Complexity: Snowflake handles container orchestration, ingress, and security patching automatically. | Zero Infrastructure: Treat your model like a native SQL function. | Cost Optimization: Significant efficiency for distinct, high-volume compute stages. |

Expand

Show lessSee more

To monitor the estimated credits consumed by these inference workloads, whether run through a warehouse or through Snowpark
Container Services, query the [MODEL\_SERVING\_USAGE\_HISTORY view](/sql-reference/account-usage/model_serving_usage_history).
