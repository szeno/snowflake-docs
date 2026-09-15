# ConsumeTwitter 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-social-media-nar

## Description

Streams tweets from Twitter’s streaming API v2. The stream provides a sample stream or a search stream based on previously uploaded rules. This processor also provides a pass through for certain fields of the tweet to be returned as part of the response. See <https://developer.twitter.com/en/docs/twitter-api/data-dictionary/introduction> for more information regarding the Tweet object model.

## Tags

json, social media, status, tweets, twitter

## Input Requirement

FORBIDDEN

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| backfill-minutes | The number of minutes (up to 5 minutes) of streaming data to be requested after a disconnect. Only available for project with academic research access. See <https://developer.twitter.com/en/docs/twitter-api/tweets/filtered-stream/integrate/recovery-and-redundancy-features> |
| backoff-attempts | The number of reconnection tries the processor will attempt in the event of a disconnection of the stream for any reason, before throwing an exception. To start a stream after this exception occur and the connection is fixed, please stop and restart the processor. If the valueof this property is 0, then backoff will never occur and the processor will always need to be restartedif the stream fails. |
| backoff-time | The duration to backoff before requesting a new stream ifthe current one fails for any reason. Will increase by factor of 2 every time a restart fails |
| base-path | The base path that the processor will use for making HTTP requests. The default value should be sufficient for most use cases. |
| batch-size | The maximum size of the number of Tweets to be written to a single FlowFile. Will write fewer Tweets based on the number available in the queue at the time of processor invocation. |
| bearer-token | The Bearer Token provided by Twitter. |
| connect-timeout | The maximum time in which client should establish a connection with the Twitter API before a time out. Setting the value to 0 disables connection timeouts. |
| expansions | A comma-separated list of expansions for objects in the returned tweet. See <https://developer.twitter.com/en/docs/twitter-api/expansions> for proper usage. Possible field values include: author\_id, referenced\_tweets.id, referenced\_tweets.id.author\_id, entities.mentions.username, attachments.poll\_ids, attachments.media\_keys ,in\_reply\_to\_user\_id, geo.place\_id |
| maximum-backoff-time | The maximum duration to backoff to start attempting a new stream. It is recommended that this number be much higher than the ‘Backoff Time’ property |
| media-fields | A comma-separated list of media fields to be returned as part of the tweet. Refer to <https://developer.twitter.com/en/docs/twitter-api/data-dictionary/object-model/media> for proper usage. Possible field values include: alt\_text, duration\_ms, height, media\_key, non\_public\_metrics, organic\_metrics, preview\_image\_url, promoted\_metrics, public\_metrics, type, url, width |
| place-fields | A comma-separated list of place fields to be returned as part of the tweet. Refer to <https://developer.twitter.com/en/docs/twitter-api/data-dictionary/object-model/place> for proper usage. Possible field values include: contained\_within, country, country\_code, full\_name, geo, id, name, place\_type |
| poll-fields | A comma-separated list of poll fields to be returned as part of the tweet. Refer to <https://developer.twitter.com/en/docs/twitter-api/data-dictionary/object-model/poll> for proper usage. Possible field values include: duration\_minutes, end\_datetime, id, options, voting\_status |
| queue-size | Maximum size of internal queue for streamed messages |
| read-timeout | The maximum time of inactivity between receiving tweets from Twitter through the API before a timeout. Setting the value to 0 disables read timeouts. |
| stream-endpoint | The source from which the processor will consume Tweets. |
| tweet-fields | A comma-separated list of tweet fields to be returned as part of the tweet. Refer to <https://developer.twitter.com/en/docs/twitter-api/data-dictionary/object-model/tweet> for proper usage. Possible field values include: attachments, author\_id, context\_annotations, conversation\_id, created\_at, entities, geo, id, in\_reply\_to\_user\_id, lang, non\_public\_metrics, organic\_metrics, possibly\_sensitive, promoted\_metrics, public\_metrics, referenced\_tweets, reply\_settings, source, text, withheld |
| user-fields | A comma-separated list of user fields to be returned as part of the tweet. Refer to <https://developer.twitter.com/en/docs/twitter-api/data-dictionary/object-model/user> for proper usage. Possible field values include: created\_at, description, entities, id, location, name, pinned\_tweet\_id, profile\_image\_url, protected, public\_metrics, url, username, verified, withheld |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| success | FlowFiles containing an array of one or more Tweets |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| mime.type | The MIME Type set to application/json |
| tweets | The number of Tweets in the FlowFile |

Expand

Show lessSee more
