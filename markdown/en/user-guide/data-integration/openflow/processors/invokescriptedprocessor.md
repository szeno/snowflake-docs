# InvokeScriptedProcessor 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-scripting-nar

## Description

Experimental - Invokes a script engine for a Processor defined in the given script. The script must define a valid class that implements the Processor interface, and it must set a variable ‘processor’ to an instance of the class. Processor methods such as onTrigger() will be delegated to the scripted Processor instance. Also any Relationships or PropertyDescriptors defined by the scripted processor will be added to the configuration dialog. The scripted processor can implement public void setLogger(ComponentLog logger) to get access to the parent logger, as well as public void onScheduled(ProcessContext context) and public void onStopped(ProcessContext context) methods to be invoked when the parent InvokeScriptedProcessor is scheduled or stopped, respectively. NOTE: The script will be loaded when the processor is populated with property values, see the Restrictions section for more security implications. Experimental: Impact of sustained usage not yet verified.

## Tags

groovy, invoke, script

## Input Requirement

## Supports Sensitive Dynamic Properties

true

## Properties

| Property | Description |
| --- | --- |
| Module Directory | Comma-separated list of paths to files and/or directories which contain modules required by the script. |
| Script Body | Body of script to execute. Only one of Script File or Script Body may be used |
| Script Engine | Language Engine for executing scripts |
| Script File | Path to script file to execute. Only one of Script File or Script Body may be used |

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

## See also

- [org.apache.nifi.processors.script.ExecuteScript](/user-guide/data-integration/openflow/processors/executescript)
