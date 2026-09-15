# May 4, 2026: Snowpark Container Services autoscaling policies (*General availability*)

With this release, autoscaling policies for Snowpark Container Services are now generally available.
Autoscaling policies extend the existing CPU-based autoscaling by letting you define metric-based rules
that control how Snowflake scales service instances up, scales them down, or suspends them automatically.
Policies support Snowflake-provided platform metrics and custom metrics that your service emits, giving you
fine-grained control over scaling behavior based on CPU utilization, memory usage, ingress
connection rate, and more.

For more information, see [Scaling services](/developer-guide/snowpark-container-services/scaling-services).
