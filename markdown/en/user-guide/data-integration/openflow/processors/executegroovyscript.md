# ExecuteGroovyScript 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-groovyx-nar

## Description

Experimental Extended Groovy script processor. The script is responsible for handling the incoming flow file (transfer to SUCCESS or remove, e.g.) as well as any flow files created by the script. If the handling is incomplete or incorrect, the session will be rolled back.

## Tags

groovy, groovyx, script

## Input Requirement

ALLOWED

## Supports Sensitive Dynamic Properties

true

## Properties

| Property | Description |
| --- | --- |
| groovyx-additional-classpath | Classpath list separated by semicolon or comma. You can use masks like *\**, *\*.jar* in file name. |
| groovyx-failure-strategy | What to do with unhandled exceptions. If you want to manage exception by code then keep the default value *rollback*. If *transfer to failure* selected and unhandled exception occurred then all flowFiles received from incoming queues in this session will be transferred to *failure* relationship with additional attributes set: ERROR\_MESSAGE and ERROR\_STACKTRACE. If *rollback* selected and unhandled exception occurred then all flowFiles received from incoming queues will be penalized and returned. If the processor has no incoming connections then this parameter has no effect. |
| groovyx-script-body | Body of script to execute. Only one of Script File or Script Body may be used |
| groovyx-script-file | Path to script file to execute. Only one of Script File or Script Body may be used |

Expand

Show lessSee more

## State management

| Scopes | Description |
| --- | --- |
| LOCAL | Scripts can store and retrieve state using the State Management APIs. Consult the State Manager section of the Developer’s Guide for more details. |
| CLUSTER | Scripts can store and retrieve state using the State Management APIs. Consult the State Manager section of the Developer’s Guide for more details. |

Expand

Show lessSee more

## Restrictions

| Required Permission | Explanation |
| --- | --- |
| execute code | Provides operator the ability to execute arbitrary code assuming all permissions that NiFi has. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | FlowFiles that failed to be processed |
| success | FlowFiles that were successfully processed |

Expand

Show lessSee more

## See also

- [org.apache.nifi.processors.script.ExecuteScript](/user-guide/data-integration/openflow/processors/executescript)
