# Guidelines for using Python extensions in Openflow

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

This topic describes the limitations, supported configurations, and best practices when
using Python extensions in Openflow.

Python processors in Openflow use NiFi’s Py4J bridge architecture, which has fundamentally
different resource characteristics than native Java processors. Because Python processors
run as external OS processes outside the JVM, they consume additional system memory, are not
governed by NiFi’s internal resource management, and have limited observability. These
differences affect runtime sizing, capacity planning, and monitoring.

## Architecture differences

Python processors run as external OS processes rather than within the JVM. This
architecture affects how resources are allocated, monitored, and managed:

| Processor type | Java processor | Python processor |
| --- | --- | --- |
| Runtime environment | JVM internal threads | External OS process |
| Memory management | Managed within JVM heap | Separate process memory |
| Lifecycle | NiFi-controlled | External process lifecycle |
| Monitoring | Full NiFi observability | Limited visibility |

Expand

Show lessSee more

## Runtime size constraints

Python extensions are only available on Medium and Large runtimes. Small runtimes
do not support Python processors due to CPU and memory constraints. Snowflake Openflow
blocks Python extensions on Small runtimes:

| Runtime size | Python support | Notes |
| --- | --- | --- |
| Small | Not supported | Python processors are blocked on Small runtimes due to CPU and memory constraints. |
| Medium | Limited (up to 2 Python processors) | The limit is for the entire runtime, not per connector or process group. This limit is currently a recommendation that will be an enforced maximum value for Openflow runtimes in the future. |
| Large | Limited (up to 4 Python processors) | The limit is for the entire runtime, not per connector or process group. This limit is currently a recommendation that will be an enforced maximum value for Openflow runtimes in the future. |

Expand

Show lessSee more

## Best practices

Follow these guidelines for working with Python processors in Openflow:

- Use Java for CPU-heavy operations. Java provides more efficient thread management
  within the JVM. Groovy scripting is a Java-based alternative.
- Use Medium or Large runtimes. Python is not available on Small runtimes.
- Limit the number of Python processors. Stay within the documented limits per runtime size.
- Monitor resource usage. Watch for memory pressure and CPU contention.
- Plan for upgrades. Custom Python processors might require a virtual environment (venv) reset
  after runtime upgrades. For more information, see
  [Restore Python processors following runtime upgrades](#label-openflow-python-ext-restore).
- Use single-threaded Python processors. Openflow does not support Python processors spawning
  subprocesses or using multithreading.

## Limitations on using Python processors

The following limitations apply when using Python processors in Openflow.

Runtime constraints
:   Python extensions can only be used with Medium or Large runtimes. Python extensions
    cannot be used with Small runtimes. This is disabled by the platform.

Memory overhead
:   Each Python processor spawns an external OS process with its own memory footprint.
    Python processes can collectively compete with the JVM for resources.

No NiFi resource management
:   Python processors are not observed or limited by NiFi’s internal resource management.
    CPU-heavy Python operations can consume approximately 50% of total server CPU time.

Monitoring gaps
:   The platform lacks visibility into external Python process health and resource consumption.

Upgrade handling
:   After runtime upgrades, custom Python processors might fail to load or exhibit unexpected
    behavior until virtual environments are recreated.

## Restore Python processors following runtime upgrades

If Python processors fail after upgrading the runtime, do the following:

1. Increment the processor version in the `ProcessorDetails.version` field.
2. Rebuild and re-upload the NiFi Archive (NAR) binary. This triggers the Python virtual
   environment cache to reset.
3. Remove and re-add the processor on the canvas. This triggers reinitialization of the
   Py4J bridge.
