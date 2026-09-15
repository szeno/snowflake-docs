# StandardOCRService

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Description

Provides integration to Openflow OCR Service

## Tags

extract, image, ocr, openflow, tesseract, text

## Properties

In the list below required Properties are shown with an asterisk (\*).
Other properties are considered optional. The table also indicates any default values, and whether a property supports the NiFi Expression Language.

| Display Name | API Name | Default Value | Allowable Values | Description |
| --- | --- | --- | --- | --- |
| Communications Timeout \* | Communications Timeout | 60 secs |  | The amount of time to wait for a response from the OCR Service. |
| Custom Service URL \* | Custom Service URL |  |  | The Custom URL of the Openflow Tesseract OCR Service. |
| OCR Languages \* | OCR Languages | ENGLISH |  | The Languages to use when performing OCR if none are provided by the caller.This is a commma separated list of the following Valid Values:ENGLISH, KOREAN, KOREAN\_VERT, HEBREW |
| Service Location Strategy \* | Service Location Strategy | Default | - Default - Custom | Determines how Service Locations configured within this Controller for the Openflow Tesseract OCR Service. |

Expand

Show lessSee more

## State management

This component does not store state.

## Restricted

This component is not restricted.

## System Resource Considerations

This component does not specify system resource considerations.
