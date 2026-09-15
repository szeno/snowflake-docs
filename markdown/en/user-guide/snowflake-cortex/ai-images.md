# Cortex AI Functions: Multimodal

Note

Audio and video processing using AI\_COMPLETE is in public preview. All other multimodal capabilities described on this page are
generally available.

Cortex AI Functions support multimodal analysis across **documents, images, audio, and video**, enabling end-to-end
media understanding and processing pipelines directly inside Snowflake.

These functions process files stored on internal or external stages, extracting insights from textual, visual, and
audio signals. They can be combined to build advanced workflows for summarization, classification, transcription,
structured extraction, and analysis.

Cortex AI Functions give you instant access to industry-leading multimodal models to understand content across
modalities, allowing you to integrate unstructured media with structured data for downstream analytics and
applications.

Cortex AI Functions support a wide range of use cases, including:

- **Content understanding:** Summarize, classify, and describe documents, images, audio, and video.
- **Data extraction:** Extract structured information such as entities, objects, sentiment, and metadata.
- **Document intelligence:** Analyze charts, tables, and layouts within complex documents.
- **Transcription and conversation analysis:** Convert speech to text with timestamps and speaker identification.
- **Multimodal analytics:** Combine visual, audio, and textual signals for deeper insights.
- **Knowledge base creation:** Enrich datasets with media-derived context for search and discovery.
- **Compliance and moderation:** Detect harmful, unsafe, or policy-violating content.

Multimodal capabilities are available through existing Cortex AI Functions, including `AI_COMPLETE`,
`AI_TRANSCRIBE`, `AI_CLASSIFY`, `AI_EMBED`, and `AI_SIMILARITY`.

## Supported media types and functions

Cortex AI Functions support extraction of specific information in structured format from documents, images, audio,
and video files. You can define the exact schema you want the model to return, such as detected objects, colors,
labels, or other domain-specific attributes.

| Media type | Primary functions | Common tasks |
| --- | --- | --- |
| Documents | `AI_COMPLETE`, `AI_PARSE_DOCUMENT`, `AI_EXTRACT` | Q&A, summarization, extraction, comparison, chart understanding |
| Images | `AI_COMPLETE`, `AI_CLASSIFY`, `AI_EMBED`, `AI_EXTRACT`, `AI_SIMILARITY`, `AI_FILTER` | Caption, compare, classify, extract entities, image search |
| Audio | `AI_COMPLETE`, `AI_TRANSCRIBE` | Caption, compare, classify, extract entities, transcribe, identify speakers |
| Video | `AI_COMPLETE`, `AI_TRANSCRIBE` | Summarize, classify, extract metadata, search scenes, transcribe video or audio tracks |
| Video | `AI_MULTI_EMBED` (`twelvelabs-marengo-embed-3-0` only) | Video semantic search such as scene search, quotes, visual similarity, sports events, and brand and product search |

Expand

Show lessSee more

Multimodal functions can process single or multiple files stored in internal or external stages. For information
about creating a suitable stage, see [Create stage for media files](#label-cortex-llm-media-files). In addition, you can dive deeper into
[Cortex AI for Document Intelligence](/user-guide/snowflake-cortex/ai-documents) in our dedicated
documentation.

## Examples

### Video metadata extraction

The following example shows how to extract structured metadata from a library of social media videos using
AI\_COMPLETE. The query processes video files stored in a stage and returns a JSON object for each video, including
sentiment, summary, detected brands and products, content safety classification, visual attributes, and music
metadata.

In this example, a table is first created from staged video files using the [FILE](/sql-reference/data-types-unstructured#label-data-types-file) data
type. The query then calls AI\_COMPLETE with a multimodal model to analyze each video and return structured results. A
filter is applied to show output for a single video file.

Copy code

```
-- Create video table using TO_FILE data type
CREATE OR REPLACE TABLE video_ads_table AS
SELECT
    TO_FILE('@video_ads', RELATIVE_PATH) AS video_file,
    RELATIVE_PATH
FROM DIRECTORY(@video_ads);

-- Extract metadata from videos in a single query
SELECT
    AI_COMPLETE(
        'gemini-3.1-pro',
        'Analyze the attached video and extract the required data points. Respond in JSON.',
        video_file,
        {},
        {
            'type': 'json',
            'schema': {
                'type': 'object',
                'properties': {
                    'sentiment':                {'type': 'string'},
                    'summary':                  {'type': 'string'},
                    'brands':                   {'type': 'array', 'items': {'type': 'string'}},
                    'products':                 {'type': 'array', 'items': {'type': 'string'}},
                    'harmful_content_detected': {'type': 'boolean'},
                    'lighting':                 {'type': 'string'},
                    'visible_items':            {'type': 'array', 'items': {'type': 'string'}},
                    'music_metadata':           {
                        'type': 'object',
                        'properties': {
                            'genre': {'type': 'string'},
                            'tempo': {'type': 'string'},
                            'mood':  {'type': 'string'}
                        },
                        'required': ['genre', 'tempo', 'mood']
                    }
                },
                'required': ['sentiment', 'summary', 'brands', 'products',
                             'harmful_content_detected', 'lighting', 'visible_items', 'music_metadata']
            }
        }
    )
FROM video_ads_table
-- Extract metadata from a single file as an example
WHERE FL_GET_RELATIVE_PATH(video_file) = 'dog_food_creative_052.mp4';
```

Response:

```
{
  "brands": [
    "Rude Dog Food"
  ],
  "harmful_content_detected": false,
  "lighting": "natural",
  "music_metadata": {
    "genre": "Acoustic",
    "mood": "Upbeat",
    "tempo": "Medium"
  },
  "products": [
    "Hypoallergenic dog food",
    "Meat grinder"
  ],
  "sentiment": "positive",
  "summary": "A man demonstrates how to make hypoallergenic dog food at home using a meat grinder, highlighting the ingredients and process, while promoting his brand, Rude Dog Food, for those who don't have the time to make it themselves.",
  "visible_items": [
    "Meat grinder",
    "Bowl",
    "Meat",
    "Vegetables",
    "Cutting board",
    "Knife",
    "Spatula",
    "String lights"
  ]
}
```

### Video transcript analysis

The following example transcribes a [video file](https://www.youtube.com/watch?v=QEQZs8SLhQE) stored in the
`podcast_videos_S3` stage.

Copy code

```
SELECT AI_TRANSCRIBE(TO_FILE('@podcast_videos_S3', 'podcast-interview.mp4'));
```

Response:

```
{
  "audio_duration": 5423.744,
  "text": "Welcome to the New York Times Popcast, your deepest duende of music news and criticism. I'm John Caramonica, and I'm the critic. I'm Joe Cascarelli, and I'm the reporter. I'm Rosalía and I'm here today with you guys. Yes. Thank you so much for being here. Like literally on some days, Jo. Some days. On some days, I think, is this person the only good pop star?
  ...
  Thank you for being here. Loved. Every episode of Popcast is at nytimes.com slash popcast. We're on YouTube at Popcast. Subscribe. We're on Instagram and TikTok at Popcast. Tap that like. Tap that follow. Tap in. Don't tap out. Credits and links and bio. We'll be back next week. Yes. Invite me anytime to eat more snacks, please. I lost my hands in Jerez"
}
```

Once you have the transcript, you can use AI\_COMPLETE to perform additional analysis. This example identifies retail
brands mentioned in the conversation for use in advertising or sponsorship analytics.

Copy code

```
SELECT
    AI_COMPLETE('claude-sonnet-4-5',
        PROMPT('Return a list of any Retail Brands mentioned in this podcast {0}',
            TO_VARCHAR(transcription_results))) AS brands_identified
FROM podcast_video_transcription;
```

Response:

```
Retail Brands Mentioned in Podcast

Based on the transcript analysis, the following brands were identified:

Calvin Klein — Mentioned in relation to Rosalía's commercial appearance.
Kinder Bueno — Cited as one of Rosalía's favorite snacks.
Nutella — Referenced as a preferred treat.
Nestlé — Mentioned as the manufacturer of Milky Bar ice cream bites.
Nongshim — Korean snack brand discussed during the tasting segment.
Cap'n Crunch — Referenced for its scent similarity to Korean snacks.
Doritos — Mentioned by one of the hosts while discussing snack collections.
```

### Video search

Cortex AI Functions let you perform semantic video searches. To do this, you generate multimodal embeddings for the
video content using `AI_MULTI_EMBED` and store them in a table, where they can be searched using a SQL query.

The Twelve Labs Marengo 3 embedding model converts each video into one or more 512-dimensional vectors, capturing
visual, audio, and text-based semantics across scenes or segments. These vectors can then be searched to find similar
scenes, detect objects or actions, or retrieve relevant moments in large video libraries.

This example uses a small library of short-form videos (such as TikTok clips) stored in a Snowflake stage. The goal is
to perform semantic search across this collection — for example, finding videos of a man riding a skateboard.

Note

This example is extensive and contains multiple steps that must be performed in sequence.

#### Create a media table to hold video metadata and embeddings

First, register the video library in a Snowflake table. Each row represents a video file stored in the stage.
Use the stage’s directory table to create `FILE` objects for each video, then store these in the table.

Copy code

```
CREATE OR REPLACE TABLE video_table AS
  (SELECT TO_FILE('@MY_VIDEOS', RELATIVE_PATH) AS video_file
    FROM DIRECTORY(@MY_VIDEOS));
```

Inspect the table to verify that the table contains the video files from the stage:

Copy code

```
SELECT * FROM video_table;
```

Response:

```
+-----------------------------------------------------+
|                 VIDEO_FILE                          |
+-----------------------------------------------------+
| {                                                   |
|   "CONTENT_TYPE": "video/mp4",                      |
|   "ETAG": "64fb6fecc9a8f99b48f46f81e77d66be",       |
|   "LAST_MODIFIED": "Mon, 08 Dec 2025 19:24:23 GMT", |
|   "RELATIVE_PATH": "content_video_2.mp4",           |
|   "SIZE": 2974020,                                  |
|   "STAGE": "@MY_VIDEOS"                             |
| }                                                   |
+-----------------------------------------------------+
| ...                                                 |
+-----------------------------------------------------+
| {                                                   |
|   "CONTENT_TYPE": "video/mp4",                      |
|   "ETAG": "357277a66571924e2aefefd7ba582a1c",       |
|   "LAST_MODIFIED": "Mon, 08 Dec 2025 19:24:19 GMT", |
|   "RELATIVE_PATH": "content_video_4.mp4",           |
|   "SIZE": 1270501,                                  |
|   "STAGE": "@MY_VIDEOS"                            |
| }                                                   |
+-----------------------------------------------------+
```

#### Generate video embeddings

Next, use the `AI_MULTI_EMBED` function to generate embeddings for each video in the table. The following example
generates embeddings using the Twelve Labs Marengo 3 model.

Copy code

```
SELECT
  video_file,
  AI_MULTI_EMBED('twelvelabs-marengo-embed-3-0', video_file) AS embeddings
FROM video_table;
```

The model returns a multimodal fingerprint of each video, with one or more embeddings for each modality (visual,
audio, transcription) and timestamps indicating the segment range (`start_sec`, `end_sec`). For example:

```
{
    "error": null,
    "value": [
        {
        "embedding": [
            -0.022094727,
            0.0053710938,
            0.024291992,

            0.06347656,
            0.0013122559,
            -0.016845703
        ],
        "embedding_option": "audio",
        "end_sec": 33.466667,
        "start_sec": 0

        },
        {
        "embedding": [
            0.03515625,
            0.10205078,
            -0.0043945312,
        ...

            0.041748047,
            0.016357422,
            -0.007385254
        ],
        "embedding_option": "visual",
        "end_sec": 33.466667,
        "start_sec": 0
        },
        {
        "embedding": [
            -0.048095703,
            -0.10449219,
            -0.033935547,
       ...
            -0.004333496,
            0.088378906,
            0.029541016
        ],
        "embedding_option": "transcription",
        "end_sec": 1,
        "start_sec": 0
        }
    ]
}
```

#### Create table of embeddings

To facilitate searching, create a new table that stores the video file along with its generated embeddings. Flatten
the embeddings arrays from the `AI_MULTI_EMBED` output so that each row of the new table contains a single embedding
vector for a segment of a video, along with its modality and timestamps. This structure is essentially a catalog of
scenes.

Copy code

```
CREATE OR REPLACE TABLE tik_tok_embeddings AS

WITH embedding_index AS (
    SELECT
        video_file,
        AI_MULTI_EMBED('twelvelabs-marengo-embed-3-0', video_file) AS embeddings
    FROM video_table
)

SELECT
    video_file,
    f.value['embedding']::VECTOR(FLOAT, 512)      AS embedding_vec,
    f.value['embedding_option']::STRING           AS embedding_option,
    f.value['start_sec']::FLOAT                   AS start_sec,
    f.value['end_sec']::FLOAT                     AS end_sec
FROM embedding_index,
LATERAL FLATTEN(input => embedding_index.embeddings['value']) f;
```

The result contains one row per embedding segment per video, with the following columns:

- `video_file`: The FILE object representing the video.
- `embedding_vec`: The embedding vector for a segment in the video file.
- `embedding_option`: The modality of the embedding (visual, audio, or transcription).
- `start_sec`: The starting timestamp of the segment in seconds.
- `end_sec`: The ending timestamp of the segment in seconds.

#### Create text embedding from query and search

To search for relevant video segments, generate an embedding vector for the text query using the same embedding model
used to generate the video clip embeddings. Then, compare the query embedding to the video embeddings stored in the
table using a vector similarity function. Order the result by similarity to find the most relevant video segments.
The result includes the video file, the timestamps, and the similarity score for each similar segment.

Copy code

```
WITH query AS (
SELECT
    (AI_MULTI_EMBED(
    'twelvelabs-marengo-embed-3-0',  'Find segments where there is a man riding a skateboard'
    )):value[0]['embedding']::VECTOR(FLOAT, 512) AS query_embedding
)
SELECT
    video_file,
    v.start_sec,
    v.end_sec,
    VECTOR_COSINE_SIMILARITY(v.embedding_vec, q.query_embedding) AS similarity
FROM tik_tok_embeddings v
CROSS JOIN query q
ORDER BY similarity DESC
LIMIT 10;
```

The top results show high similarity scores for two specific segments in a single video:

```
+-----------------------------------------------------+-----------+---------+------------------+
|                    video_file                       | start_sec | end_sec |    similarity    |
+-----------------------------------------------------+-----------+---------+------------------+
| content_video_1.mp4                                 | 5.5       | 11.5    | 0.6915           |
+-----------------------------------------------------+-----------+---------+------------------+
| content_video_1.mp4                                 | 11.5      | 17.0    | 0.5646           |
+-----------------------------------------------------+-----------+---------+------------------+
```

By checking the first video segment (from 5.5 to 11.5 seconds), you can confirm that it indeed contains a skateboarder.

![Screenshot from a video search result showing a man riding a skateboard](/static/images/skateboarding.png)

### Audio-based sentiment analytics

This example shows how to analyze a call center audio recording using AI\_COMPLETE to extract structured sentiment
insights based on both spoken content and vocal delivery. The model evaluates agent and customer behavior, including
tone, professionalism, anger, and escalation signals, and returns a JSON object summarizing overall sentiment,
participant dynamics, escalation events, and interaction outcome.

Copy code

```
-- Create audio table using TO_FILE data type
CREATE OR REPLACE TABLE call_center_logs AS (
    SELECT
        TO_FILE('@AUDIO_STAGE', RELATIVE_PATH) AS audio_files,
        RELATIVE_PATH
    FROM DIRECTORY(@AUDIO_STAGE)
);

-- Analyze audio in a single query
SELECT
    FL_GET_RELATIVE_PATH(audio_files) AS file_name,
    AI_COMPLETE(
        'gemini-3.1-pro',
        'Analyze the attached audio call center recording. You are an acoustic and semantic analyzer.
Evaluate both the literal spoken words and the vocal delivery (pitch, pace, tone, volume, and pauses).

Focus on two participants:
- AGENT: detect sarcasm, passive-aggressiveness, rudeness, or professionalism
- CUSTOMER: detect anger, frustration, distress, or calmness

Return ONLY raw JSON. No markdown, no backticks, no preamble.',
        audio_files,
        {},
        {
            'type': 'json',
            'schema': {
                'type': 'object',
                'properties': {
                    'overall_sentiment': {'type': 'string'},
                    'agent': {
                        'type': 'object',
                        'properties': {
                            'tone':            {'type': 'string'},
                            'sarcasm_level':   {'type': 'string', 'enum': ['none', 'low', 'medium', 'high']},
                            'rudeness_level':  {'type': 'string', 'enum': ['none', 'low', 'medium', 'high']},
                            'professionalism': {'type': 'string', 'enum': ['poor', 'fair', 'good', 'excellent']},
                            'key_signals':     {'type': 'array', 'items': {'type': 'string'}}
                        },
                        'required': ['tone', 'sarcasm_level', 'rudeness_level', 'professionalism', 'key_signals']
                    },
                    'customer': {
                        'type': 'object',
                        'properties': {
                            'sentiment':    {'type': 'string'},
                            'anger_level':  {'type': 'string', 'enum': ['calm', 'mild', 'moderate', 'high', 'furious']},
                            'tone':         {'type': 'string'},
                            'key_signals':  {'type': 'array', 'items': {'type': 'string'}}
                        },
                        'required': ['sentiment', 'anger_level', 'tone', 'key_signals']
                    },
                    'escalation_detected':  {'type': 'boolean'},
                    'escalation_summary':   {'type': 'string'},
                    'resolution_sentiment': {'type': 'string'},
                    'agent_effectiveness':  {'type': 'string'}
                },
                'required': ['overall_sentiment', 'agent', 'customer', 'escalation_detected',
                             'escalation_summary', 'resolution_sentiment', 'agent_effectiveness']
            }
        }
    ) AS analysis
FROM call_center_logs
WHERE FL_GET_RELATIVE_PATH(audio_files) = 'consultation_1.wav';
```

Response:

```
{
  "agent": {
    "key_signals": [
      "Dismissed customer concerns",
      "Insulted customer risk tolerance",
      "Told customer she was overreacting"
    ],
    "professionalism": "poor",
    "rudeness_level": "high",
    "sarcasm_level": "low",
    "tone": "condescending"
  },
  "agent_effectiveness": "poor",
  "customer": {
    "anger_level": "high",
    "key_signals": [
      "Stressed about $40k loss",
      "Demanded to sell all assets",
      "Expressed regret trusting agent"
    ],
    "sentiment": "negative",
    "tone": "frustrated"
  },
  "escalation_detected": true,
  "escalation_summary": "Customer escalated to liquidating all assets due to the agent's dismissive and rude behavior regarding her financial losses.",
  "overall_sentiment": "negative",
  "resolution_sentiment": "negative"
}
```

### Vision Q&A example

The following example uses Anthropic’s Claude Sonnet 4.6 model to summarize a pie chart
`science-employment-slide.jpeg` stored in the `@myimages` stage.

![Pie chart showing the distribution of occupations where mathematics is considered "extremely important" in 2023](/static/images/cortex-llm/science-employment-slide.jpeg)

The distribution of occupations where mathematics is considered “extremely important” in 2023

Copy code

```
SELECT AI_COMPLETE('claude-sonnet-4-6',
    'Summarize the insights from this pie chart in 100 words',
    TO_FILE('@myimages', 'science-employment-slide.jpeg'));
```

Response:

```
This pie chart shows the distribution of occupations where mathematics is considered "extremely important" in 2023.
Data scientists dominate with nearly half (48.7%) of all such positions, followed by operations research analysts
at 29.6%. The remaining positions are distributed among statisticians (7.8%), actuaries (7.2%), physicists (5.1%),
mathematicians (0.6%), and other mathematical science occupations (1.1%). This distribution highlights the growing
importance of data science in mathematics-intensive careers, while traditional mathematics roles represent a smaller
share of the workforce.
```

### Compare images example

Use the [PROMPT helper function](/sql-reference/functions/prompt) to process multiple images in a single
AI\_COMPLETE call. The following example uses Anthropic’s Claude Sonnet 4.6 model to compare two different ad
creatives from the `@myimages` stage.

![Images of two ads for electric cars](/static/images/cortex-llm/two-ad-creatives.png)

Image of two ads for electric cars

Copy code

```
SELECT AI_COMPLETE('claude-sonnet-4-6',
    PROMPT('Compare this image {0} to this image {1} and describe the ideal audience for each in two concise bullets no longer than 10 words',
    TO_FILE('@myimages', 'adcreative_1.png'),
    TO_FILE('@myimages', 'adcreative_2.png')
));
```

Response:

```
First image ("Discover a New Energy"):
• Conservative luxury SUV buyers seeking a subtle transition to electrification

Second image ("Electrify Your Drive"):
• Young, tech-savvy urbanites attracted to bold, progressive automotive design
```

## Create stage for media files

Cortex AI Functions that process media files (documents, images, audio, or video) require the files to be stored on
an internal or external stage. Most of these functions require the stage to use server-side encryption;
`AI_MULTI_EMBED` supports all stage encryption types, including server-side encryption (SSE) and
customer-side encryption (CSE). If you want to be able to query the stage or programmatically process all the
files stored there, the stage must have a directory table.

The SQL below creates a suitable internal stage:

Copy code

```
CREATE OR REPLACE STAGE input_stage
  DIRECTORY = ( ENABLE = true )
  ENCRYPTION = ( TYPE = 'SNOWFLAKE_SSE' );
```

To process files from external object storage (for example, Amazon S3), create a storage integration, then create an
external stage that uses the storage integration. To learn how to configure a Snowflake storage integration, see our
detailed guides:

- [Amazon S3 storage integration](/user-guide/data-load-s3-config-storage-integration)
- [Azure container integration](/user-guide/data-load-azure-config)
- [Google Cloud Storage integration](/user-guide/data-load-gcs-config)

Create an external stage that references the integration and points to your cloud storage container. This example
points to an Amazon S3 bucket:

Copy code

```
CREATE OR REPLACE STAGE my_aisql_media_files
  STORAGE_INTEGRATION = my_s3_integration
  URL = 's3://my_bucket/prefix/'
  DIRECTORY = ( ENABLE = TRUE )
  ENCRYPTION = ( TYPE = 'AWS_SSE_S3' );
```

With an internal or external stage created, and files stored there, you can use Cortex AI Functions to process media
files stored in the stage. For document parsing, see
[Parsing documents with AI\_PARSE\_DOCUMENT](/user-guide/snowflake-cortex/parse-document).

Note

Cortex AI Functions that process media files are currently incompatible with custom
[network policies](/user-guide/network-policies), except for `AI_MULTI_EMBED`, which supports network
policy protected stages.

### Cortex AI Functions storage best practices

You may find the following best practices helpful when working with media files in stages with Cortex AI Functions:

- Establish a scheme for organizing media files in stages. For example, create a separate stage for each team or
  project, and store the different types of media files in subdirectories.
- Enable directory listings on stages to allow querying and programmatic access to its files.

  Tip

  To automatically refresh the directory table for the external stage when new or updated files are available, set
  AUTO\_REFRESH = TRUE when creating the stage.
- For external stages, use fine-grained policies on the cloud provider side (for example, AWS IAM policies)
  to restrict the storage integration’s access to only what is necessary.
- Always use encryption, such as AWS\_SSE or SNOWFLAKE\_SSE, to protect your data at rest.

## Model limitations

All models available to Snowflake Cortex have limitations on the total number of input and output tokens, known as
the model’s *context window*. The context window size is measured in tokens. Inputs exceeding the context window
limit result in an error. Output which would exceed the context window limit is truncated.

For text models, tokens generally represent approximately four characters of text, so the word count corresponding
to a limit is less than the token count.

For multimodal models, the token count per image and video depends on the model’s architecture. Tokens within a
prompt (for example, “what animal is this?”) also contribute to the model’s context window.

| Model | Context window (tokens) | File types | File size | Files per prompt |
| --- | --- | --- | --- | --- |
| `openai-gpt-4.1` | 1,047,576 | .jpg, .jpeg, .png, .webp, .gif | 10MB | 5 |
| `claude-4-opus` | 200,000 | .jpg, .jpeg, .png, .webp, .gif | 3.75 MB [[L1]](#citation-L1) | 20 |
| `claude-4-sonnet` | 200,000 | .jpg, .jpeg, .png, .webp, .gif | 3.75 MB [[L1]](#citation-L1) | 20 |
| `claude-3-7-sonnet` | 200,000 | .jpg, .jpeg, .png, .webp, .gif | 3.75 MB [[L1]](#citation-L1) | 20 |
| `claude-sonnet-4-6` | 1,000,000 | .jpg, .jpeg, .png, .webp, .gif | 3.75 MB [[L1]](#citation-L1) | 20 |
| `llama4-maverick` | 128,000 | .jpg, .jpeg, .png, .webp, .gif, .bmp | 10 MB | 10 |
| `llama-4-scout` | 128,000 | .jpg, .jpeg, .png, .webp, .gif, .bmp | 10 MB | 10 |
| `pixtral-large` | 128,000 | .jpg, .jpeg, .png, .webp, .gif, .bmp | 10 MB | 8 |
| `voyage-multimodal-3` | 32,768 | .jpg, .png, .pg, .gif, .bmp | 10 MB | 5 |
| `gemini-3.1-pro` | 1,000,000 | **Images:** .jpg, .jpeg, .png, .webp, .gif **Audio:** .wav, .mp3, .aiff, .aac, .ogg, .flac, .m4a, .mp4, .pcm, .webm **Video:** .mp4, .mpeg, .mov, .avi, .flv, .mpg, .webm, .wmv, .3gpp | 100 MB combined [[P1]](#citation-P1) | 20 images + 10 audio + 10 video [[P1]](#citation-P1) |
| `gemini-3.1-flash-lite` | 1,048,576 | **Images:** .jpg, .jpeg, .png, .webp, .gif **Audio:** .wav, .mp3, .aiff, .aac, .ogg, .flac, .m4a, .mp4, .pcm, .webm **Video:** .mp4, .mpeg, .mov, .avi, .flv, .mpg, .webm, .wmv, .3gpp | 100 MB combined [[P1]](#citation-P1) | 20 images + 10 audio + 10 video [[P1]](#citation-P1) |
| `gemini-3.5-flash` | 1,000,000 | **Images:** .jpg, .jpeg, .png, .webp, .gif **Audio:** .wav, .mp3, .aiff, .aac, .ogg, .flac, .m4a, .mp4, .pcm, .webm **Video:** .mp4, .mpeg, .mov, .avi, .flv, .mpg, .webm, .wmv, .3gpp | 100 MB combined [[P1]](#citation-P1) | 20 images + 10 audio + 10 video [[P1]](#citation-P1) |
| `twelvelabs-marengo-embed-3-0` [[M1]](#citation-M1) | 4 hours (duration) [[M2]](#citation-M2) | **Video:** .mp4, .mov, .avi, .mkv, .wmv, .webm | 6 GB (video or audio) [[M3]](#citation-M3) | N/A (embedding model) |

Expand

Show lessSee more

[l1]
Images must be smaller than 8000x8000 pixels. Limits apply to each individual image.

[p1]
A single request can include up to 20 image files, 10 audio files, and 10 video files, with a combined payload size of up to 100 MB.

[m1]
Available in US East (N. Virginia) only; cross-region inference is supported.

[m2]
Marengo Embed 3.0 is an embedding model with no text-token context window. The value indicates the maximum video
duration that can be embedded in a single call.

[m3]
Maximum image size is 5 MB. For stage and encryption requirements, see
[AI\_MULTI\_EMBED](/sql-reference/functions/ai_multi_embed).

Note

For per-model regional availability, see [Regional availability](/user-guide/snowflake-cortex/aisql-regional-availability#label-cortex-llm-availability) on the
Cortex AI Functions page.

## Error conditions

| Message | Explanation |
| --- | --- |
| Request failed for external function SYSTEM$COMPLETE\_WITH\_IMAGE\_INTERNAL with remote service error: 400 ‘”invalid image path” | Either the file extension or the file itself is not accepted by the model. The message might also mean that the file path is incorrect; that is, the file does not exist at the specified location. Filenames are case-sensitive. |
| Error in secure object | May indicate that the stage does not exist. Check the stage name and ensure that the stage exists and is accessible. Be sure to use the at (@) sign at the beginning of the stage path, such as `@myimages`. |
| Request failed for external function \_COMPLETE\_WITH\_PROMPT with remote service error: 400 ‘”invalid request parameters: unsupported image format: image/\*\* | Unsupported image format given to `claude-sonnet-4-6`, that is, other than .jpeg, .png, .webp, or .gif. |
| Request failed for external function \_COMPLETE\_WITH\_PROMPT with remote service error: 400 ‘”invalid request parameters: Image data exceeds the limit of 5.00 MB” | The provided image given to `claude-sonnet-4-6` exceeds 5 MB. |

Expand

Show lessSee more

## Legal

The data classification of inputs and outputs are as set forth in the following table.

| Input data classification | Output data classification | Designation |
| --- | --- | --- |
| Usage Data | Customer Data | Generally available functions are Covered AI Features. Preview functions are Preview AI Features.  [[1]](#footnote-1) |

Expand

Show lessSee more

[1]
Represents the defined term used in the AI Terms and Acceptable Use Policy.

For additional information, refer to [Snowflake AI and ML](/guides-overview-ai-features).
