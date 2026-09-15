# AWS data file encryption

Snowflake supports either client-side encryption (CSE) or server-side encryption (SSE). Either can be configured to decrypt files staged in S3 buckets.

- Client-side encryption:

  - AWS\_CSE: Requires a MASTER\_KEY value. The [master key](https://csrc.nist.gov/glossary/term/master_key) must be a 128-bit or 256-bit key in Base64-encoded form.

    For client-side encryption, Snowflake supports using a master key stored in Snowflake; using a master key stored in AWS Key Management Service (AWS KMS) is not supported.

    Snowflake supports AWS V1 encryption standards. (AWS V2 encryption standards are not supported.)

    For more information, see the AWS documentation for [client-side encryption](http://docs.aws.amazon.com/AmazonS3/latest/dev/UsingClientSideEncryption.html).
- Server-side encryption (SSE):

  - AWS\_SSE\_S3: Requires no additional encryption settings.
  - AWS\_SSE\_KMS: Accepts an optional KMS\_KEY\_ID value.

  For more information, see the AWS documentation for [server-side encryption](http://docs.aws.amazon.com/AmazonS3/latest/dev/serv-side-encryption.html).

  Using AWS Key Management Service (KMS) to manage keys requires configuring an IAM policy. For information, see the [KMS documentation](https://aws.amazon.com/documentation/kms/).

**Next:** [Create an S3 stage](/user-guide/data-load-s3-create-stage)
