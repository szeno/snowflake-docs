# UnpackContent 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-standard-nar

## Description

Unpacks the content of FlowFiles that have been packaged with one of several different Packaging Formats, emitting one to many FlowFiles for each input FlowFile. Supported formats are TAR, ZIP, and FlowFile Stream packages.

## Tags

Unpack, archive, flowfile-stream, flowfile-stream-v3, tar, un-merge, zip

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| File Filter | Only files contained in the archive whose names match the given regular expression will be extracted (tar/zip only) |
| Filename Character Set | If supplied this character set will be supplied to the Zip utility to attempt to decode filenames using the specific character set. If not specified the default platform character set will be used. This is useful if a Zip was created with a different character set than the platform default and the zip uses non standard values to specify. |
| Packaging Format | The Packaging Format used to create the file |
| Password | Password used for decrypting Zip archives encrypted with ZipCrypto or AES. Configuring a password disables support for alternative Zip compression algorithms. |
| allow-stored-entries-wdd | Some zip archives contain stored entries with data descriptors which by spec should not happen. If this property is true they will be read anyway. If false and such an entry is discovered the zip will fail to process. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | The original FlowFile is sent to this relationship when it cannot be unpacked for some reason |
| original | The original FlowFile is sent to this relationship after it has been successfully unpacked |
| success | Unpacked FlowFiles are sent to this relationship |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| mime.type | If the FlowFile is successfully unpacked, its MIME Type is no longer known, so the mime.type attribute is set to application/octet-stream. |
| fragment.identifier | All unpacked FlowFiles produced from the same parent FlowFile will have the same randomly generated UUID added for this attribute |
| fragment.index | A one-up number that indicates the ordering of the unpacked FlowFiles that were created from a single parent FlowFile |
| fragment.count | The number of unpacked FlowFiles generated from the parent FlowFile |
| segment.original.filename | The filename of the parent FlowFile. Extensions of .tar, .zip or .pkg are removed because the MergeContent processor automatically adds those extensions if it is used to rebuild the original FlowFile |
| file.lastModifiedTime | The date and time that the unpacked file was last modified (tar and zip only). |
| file.creationTime | The date and time that the file was created. For encrypted zip files this attribute always holds the same value as file.lastModifiedTime. For tar and unencrypted zip files if available it will be returned otherwise this will be the same value asfile.lastModifiedTime. |
| file.lastMetadataChange | The date and time the file’s metadata changed (tar only). |
| file.lastAccessTime | The date and time the file was last accessed (tar and unencrypted zip files only) |
| file.owner | The owner of the unpacked file (tar only) |
| file.group | The group owner of the unpacked file (tar only) |
| file.size | The uncompressed size of the unpacked file (tar and zip only) |
| file.permissions | The read/write/execute permissions of the unpacked file (tar and unencrypted zip files only) |
| file.encryptionMethod | The encryption method for entries in Zip archives |

Expand

Show lessSee more

## Use cases

| Unpack Zip containing filenames with special characters, created on Windows with filename charset ‘Cp437’ or ‘IBM437’. |
| --- |

Expand

Show lessSee more

## See also

- [org.apache.nifi.processors.standard.MergeContent](/user-guide/data-integration/openflow/processors/mergecontent)
