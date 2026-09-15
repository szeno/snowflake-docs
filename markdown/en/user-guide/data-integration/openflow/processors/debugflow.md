# DebugFlow 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-standard-nar

## Description

The DebugFlow processor aids testing and debugging the FlowFile framework by allowing various responses to be explicitly triggered in response to the receipt of a FlowFile or a timer event without a FlowFile if using timer or cron based scheduling. It can force responses needed to exercise or test various failure modes that can occur when a processor runs.

## Tags

FlowFile, debug, flow, processor, test, utility

## Input Requirement

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| @OnScheduled Pause Time | Specifies how long the processor should sleep in the @OnScheduled method, so that the processor can be forced to take a long time to start up |
| @OnStopped Pause Time | Specifies how long the processor should sleep in the @OnStopped method, so that the processor can be forced to take a long time to shutdown |
| @OnUnscheduled Pause Time | Specifies how long the processor should sleep in the @OnUnscheduled method, so that the processor can be forced to take a long time to respond when user clicks stop |
| Content Size | The number of bytes to write each time that the FlowFile is written to |
| CustomValidate Pause Time | Specifies how long the processor should sleep in the customValidate() method |
| Fail When @OnScheduled called | Specifies whether or not the Processor should throw an Exception when the methods annotated with @OnScheduled are called |
| Fail When @OnStopped called | Specifies whether or not the Processor should throw an Exception when the methods annotated with @OnStopped are called |
| Fail When @OnUnscheduled called | Specifies whether or not the Processor should throw an Exception when the methods annotated with @OnUnscheduled are called |
| FlowFile Exception Class | Exception class to be thrown (must extend java.lang. RuntimeException). |
| FlowFile Exception Iterations | Number of FlowFiles to throw exception. |
| FlowFile Failure Iterations | Number of FlowFiles to forward to failure relationship. |
| FlowFile Rollback Iterations | Number of FlowFiles to roll back (without penalty). |
| FlowFile Rollback Penalty Iterations | Number of FlowFiles to roll back with penalty. |
| FlowFile Rollback Yield Iterations | Number of FlowFiles to roll back and yield. |
| FlowFile Success Iterations | Number of FlowFiles to forward to success relationship. |
| Ignore Interrupts When Paused | If the Processor’s thread(s) are sleeping (due to one of the “Pause Time” properties above), and the thread is interrupted, this indicates whether the Processor should ignore the interrupt and continue sleeping or if it should allow itself to be interrupted. |
| No FlowFile Exception Class | Exception class to be thrown if no FlowFile (must extend java.lang. RuntimeException). |
| No FlowFile Exception Iterations | Number of times to throw NPE exception if no FlowFile. |
| No FlowFile Skip Iterations | Number of times to skip onTrigger if no FlowFile. |
| No FlowFile Yield Iterations | Number of times to yield if no FlowFile. |
| OnTrigger Pause Time | Specifies how long the processor should sleep in the onTrigger() method, so that the processor can be forced to take a long time to perform its task |
| Write Iterations | Number of times to write to the FlowFile |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | FlowFiles that failed to process. |
| success | FlowFiles processed successfully. |

Expand

Show lessSee more
