# October 20, 2026: Online Feature Store (*General availability*)

Online Feature Store is now generally available and is no longer in
[Preview](/release-notes/preview-features).

The Online Feature Store serves the latest feature values with low-latency online retrieval
for real-time ML applications such as fraud detection, recommendations, and personalization.
Use batch, stream, and real-time feature views, ingest events through REST APIs, and
integrate with real-time model inference.

With general availability, you can choose a size for the Feature Store online service to
match your workload, and resize it later as your traffic changes. Online service usage is
billed through the Feature Store online service compute, autoscale compute, and storage
components. For details, see
[Cost and billing considerations](/developer-guide/snowflake-ml/feature-store/online-feature-store#label-online-fs-cost-billing).

Feature Store monitoring in Snowsight is also generally available. Use it to track offline
refresh status, online serving latency and errors, and stream ingest health. For details, see
[Monitoring and Observability](/developer-guide/snowflake-ml/feature-store/monitoring).

The Online Feature Store is available in AWS and Azure commercial regions. It isn’t available
on Google Cloud.

For more information, see
[Serving online features](/developer-guide/snowflake-ml/feature-store/online-feature-store).
