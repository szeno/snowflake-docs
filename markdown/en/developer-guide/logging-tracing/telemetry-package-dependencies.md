# Snowflake telemetry package dependencies

When you add the `com.snowflake:telemetry` package to the definition of your function or procedure, libraries that are dependencies of
Snowflake telemetry will be added to environment in which the function or procedure executes. Avoid importing other versions of these
libraries to support your own code because doing so may result in collisions and unexpected behavior.

You can use the telemetry package when adding code to perform logging or tracing to handlers written in Java or Scala.

The following tables list the libraries included for each telemetry package version.

## Version 0.1.0

| Group ID | Artifact ID | Version |
| --- | --- | --- |
| ch.qos.logback | logback-core | 1.3.6 |
| ch.qos.logback | logback-classic | 1.3.6 |
| io.opentelemetry | opentelemetry-api | 1.35.0 |
| io.opentelemetry | opentelemetry-context | 1.35.0 |
| io.opentelemetry | opentelemetry-sdk | 1.35.0 |
| io.opentelemetry | opentelemetry-sdk-common | 1.35.0 |
| io.opentelemetry | opentelemetry-sdk-trace | 1.35.0 |
| io.opentelemetry | opentelemetry-sdk-metrics | 1.35.0 |
| io.opentelemetry | opentelemetry-sdk-logs | 1.35.0 |
| io.opentelemetry | opentelemetry-api-events | 1.35.0-alpha |
| io.opentelemetry | opentelemetry-exporter-otlp-common | 1.35.0 |
| io.opentelemetry | opentelemetry-exporter-common | 1.35.0 |
| io.opentelemetry | opentelemetry-extension-incubator | 1.35.0-alpha |
| org.slf4j | slf4j-api | 2.0.4 |

Expand

Show lessSee more

## Version 0.0.1

| Group ID | Artifact ID | Version |
| --- | --- | --- |
| io.opentelemetry | opentelemetry-api | 1.21.0 |
| io.opentelemetry | opentelemetry-context | 1.21.0 |
| io.opentelemetry | opentelemetry-sdk | 1.21.0 |
| io.opentelemetry | opentelemetry-sdk-trace | 1.21.0 |
| io.opentelemetry | opentelemetry-sdk-metrics | 1.21.0 |
| io.opentelemetry | opentelemetry-sdk-logs | 1.21.0-alpha |
| io.opentelemetry | opentelemetry-api-logs | 1.21.0-alpha |
| io.opentelemetry | opentelemetry-semconv | 1.21.0-alpha |
| io.opentelemetry | opentelemetry-exporter-otlp-common | 1.21.0 |
| io.opentelemetry | opentelemetry-exporter-common | 1.21.0 |
| org.slf4j | slf4j-api | 1.7.25 |
| ch.qos.logback | logback-core | 1.2.3 |
| ch.qos.logback | logback-classic | 1.2.3 |
| io.opentelemetry.proto | opentelemetry-proto | 0.19.0-alpha |

Expand

Show lessSee more
