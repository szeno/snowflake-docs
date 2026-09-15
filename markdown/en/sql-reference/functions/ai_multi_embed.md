Categories:
:   [String & binary functions](/sql-reference/functions-string) (AI Functions)

# AI\_MULTI\_EMBED

Creates multimodal embeddings from text, an image, an audio file, or a video file. Embeddings are abstract
numerical representations of the features of an input that can be used to determine the degree of similarity
between inputs across modalities. Use AI\_MULTI\_EMBED for semantic search, scene retrieval, content indexing,
similarity search, and other tasks that combine visual, audio, and text understanding.

Unlike [AI\_EMBED](/sql-reference/functions/ai_embed), which returns a single embedding vector, AI\_MULTI\_EMBED returns
one or more embedding vectors together with metadata that describes each segment. For video and audio inputs,
the function generates separate embeddings for different modalities (visual, audio, transcription) and for
different segments of the asset.

The following table shows the regions where you can use the AI\_MULTI\_EMBED function:

| Data type | AWS US West 2 (Oregon) | AWS US East 1 (N. Virginia) | AWS Europe Central 1 (Frankfurt) | AWS Europe West 1 (Ireland) | AWS AP Southeast 2 (Sydney) | AWS AP Northeast 1 (Tokyo) | Azure East US 2 (Virginia) | Azure West Europe (Netherlands) | AWS (Cross-Region) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Text |  | ✔ |  |  |  |  |  |  | ✔ |
| Image |  | ✔ |  |  |  |  |  |  | ✔ |
| Audio |  | ✔ |  |  |  |  |  |  | ✔ |
| Video |  | ✔ |  |  |  |  |  |  | ✔ |

Expand

Show lessSee more

## Syntax

Copy code

```
AI_MULTI_EMBED( <model> , <input> [ , <options> ] )
```

## Arguments

**Required:**

`model`
:   A string specifying the multimodal embedding model to use. You can provide the following value:

    - `twelvelabs-marengo-embed-3-0`

    Supported models might have different [costs](/user-guide/snowflake-cortex/aisql-cost#label-cortex-llm-cost-considerations).

`input`
:   The content to generate embeddings from. Can be one of the following:

    - A string containing the text to embed.
    - A FILE object (created with [TO\_FILE](/sql-reference/functions/to_file)) referencing an image, audio, or
      video file in a Snowflake stage.

    The `twelvelabs-marengo-embed-3-0` model supports embedding generation for transcribed speech and text
    queries in 36 languages. For the full list, see the
    [TwelveLabs Marengo documentation](https://docs.twelvelabs.io/docs/concepts/models/marengo).

    Supported file formats:

    - **Video:** `.mp4`, `.mov`, `.avi`, `.mkv`, `.webm`, `.flv`
    - **Audio:** `.mp3`, `.wav`, `.flac`, `.ogg`
    - **Image:** `.jpg`, `.jpeg`, `.png`

    For the maximum supported duration and file size, see [Limitations](#limitations).

**Optional:**

`options`
:   An [object](/sql-reference/data-types-semistructured#label-data-type-object) containing zero or more of the following keys. The options apply only
    to video and audio inputs; they’re ignored for text and image inputs.

    - `start_sec`: A number that specifies the time point in seconds where embedding generation should begin.
      Minimum value: 0.

      Default: 0
    - `end_sec`: A number that specifies the time point in seconds where embedding generation should end. Must
      be greater than `start_sec` plus the segment length, and no greater than the duration of the media.

      Default: Duration of the media
    - `embedding_options`: An array specifying which modalities to embed. Valid array members:

      - `visual` — Visual embeddings from the video.
      - `audio` — Embeddings of the audio track.
      - `transcription` — Embeddings of the transcribed speech in the audio track.

      Defaults:

      - For video: `['visual', 'audio', 'transcription']`
      - For audio: `['audio', 'transcription']`
    - `embedding_scope`: An array specifying the scope of the returned embeddings. Provide one or both of the
      following values:

      - `clip` — Returns one embedding per segment (clip) of the asset.
      - `asset` — Returns a single embedding that represents the entire asset.

      Default: `['clip']`
    - `embedding_type`: An array specifying how embeddings are aggregated across modalities. Valid array
      members:

      - `separate_embedding` — Returns a separate embedding for each modality in `embedding_options`.
      - `fused_embedding` — Returns a weighted fusion of the modalities in `embedding_options`. For video,
        `fused_embedding` requires at least two modalities in `embedding_options`. For audio, `fused_embedding`
        requires both `audio` and `transcription` in `embedding_options`.

      Default: `['separate_embedding']`
    - `use_fixed_length_sec`: An integer that specifies the duration in seconds of each segment when using
      fixed-length segmentation. Range: 1 to 10.

      This option is mutually exclusive with `min_clip_sec`. If neither is provided, video uses dynamic
      (shot-boundary) segmentation and audio uses fixed-length segmentation of approximately 10 seconds.
    - `min_clip_sec`: An integer that specifies the minimum duration in seconds of each segment when using
      dynamic (shot-boundary) segmentation. Range: 1 to 5.

      Default: 4

      This option is mutually exclusive with `use_fixed_length_sec`. Dynamic segmentation applies only to
      video.

## Returns

Returns an [OBJECT](/sql-reference/data-types-structured) with the following fields:

- `error`: A string describing any error that occurred, or NULL if the call succeeded.
- `value`: An array of objects, one for each embedding. Each object contains the following fields:

  - `embedding`: An array of floats representing the embedding vector. The Marengo Embed 3.0 model returns
    512-dimensional vectors. Cast this value to `VECTOR(FLOAT, 512)` before using it with the
    [vector similarity functions](/sql-reference/functions-vector).
  - `embedding_option`: The modality of the embedding. One of `visual`, `audio`, `transcription`, or `fused`.
    Not present for text or image inputs.
  - `embedding_scope`: The scope of the embedding. One of `clip` or `asset`. Not present for text or image
    inputs.
  - `start_sec`: The starting timestamp of the segment in seconds. Not present for text or image inputs.
  - `end_sec`: The ending timestamp of the segment in seconds. Not present for text or image inputs.

## Access control requirements

You must use a role that has been granted the SNOWFLAKE.CORTEX\_USER database role *or* the
SNOWFLAKE.CORTEX\_EMBED\_USER database role to call this function. See [Cortex LLM privileges](/user-guide/snowflake-cortex/aisql-privileges-and-access#label-cortex-llm-privileges) for
more information on granting one of these privileges.

## Examples

### Embed a text query

Generate an embedding for a text query. Use this pattern to embed a search phrase so you can compare it
against embeddings stored for video or audio assets.

Copy code

```
SELECT AI_MULTI_EMBED('twelvelabs-marengo-embed-3-0', 'text to embed');
```

### Embed an image

Generate an embedding for a staged image:

Copy code

```
SELECT AI_MULTI_EMBED('twelvelabs-marengo-embed-3-0',
        TO_FILE('@my_files', 'dog.jpg'));
```

### Embed a video

Generate multimodal embeddings for a staged video. With the default options, the model returns visual,
audio, and transcription embeddings for each detected segment.

Copy code

```
SELECT AI_MULTI_EMBED('twelvelabs-marengo-embed-3-0',
        TO_FILE('@my_files', 'me-at-the-zoo.mp4'));
```

Example response:

```
{
  "error": null,
  "value": [
    {
      "embedding": [-0.022094727, 0.0053710938, 0.024291992, ...],
      "embedding_option": "visual",
      "embedding_scope": "clip",
      "start_sec": 0,
      "end_sec": 4.5
    },
    {
      "embedding": [-0.048095703, -0.10449219, -0.033935547, ...],
      "embedding_option": "audio",
      "embedding_scope": "clip",
      "start_sec": 0,
      "end_sec": 4.5
    },
    {
      "embedding": [0.03515625, 0.10205078, -0.0043945312, ...],
      "embedding_option": "transcription",
      "embedding_scope": "clip",
      "start_sec": 0,
      "end_sec": 4.5
    }
  ]
}
```

### Embed an audio file

Generate embeddings for a staged audio file:

Copy code

```
SELECT AI_MULTI_EMBED('twelvelabs-marengo-embed-3-0',
        TO_FILE('@my_files', 'nature.ogg'));
```

### Embed a video segment with custom options

Restrict embedding to the first 30 seconds of a video, request both clip-level and asset-level embeddings,
and use fixed 5-second segments:

Copy code

```
SELECT AI_MULTI_EMBED(
  'twelvelabs-marengo-embed-3-0',
  TO_FILE('@my_db.my_schema.files', 'nature.mp4'),
  {
    'start_sec':           0,
    'end_sec':             30,
    'embedding_options':   ['visual', 'audio', 'transcription'],
    'embedding_scope':     ['clip', 'asset'],
    'use_fixed_length_sec': 5
  }
) AS r;
```

### Embed a video with dynamic segmentation

Use dynamic (shot-boundary) segmentation with a 4-second minimum segment length:

Copy code

```
SELECT AI_MULTI_EMBED(
  'twelvelabs-marengo-embed-3-0',
  TO_FILE('@my_db.my_schema.files', 'nature.mp4'),
  {
    'start_sec':         0,
    'end_sec':           30,
    'embedding_options': ['visual', 'audio', 'transcription'],
    'embedding_scope':   ['clip', 'asset'],
    'min_clip_sec':      4
  }
) AS r;
```

### Search video segments with a text query

Use AI\_MULTI\_EMBED to build a video search workflow. The following query flattens the embeddings returned
for each video, stores one row per clip and modality, and then ranks clips by cosine similarity to a text
query. For the full walkthrough, including how to load the source videos, see
[Cortex AI Functions: Multimodal](/user-guide/snowflake-cortex/ai-multimodal).

Copy code

```
CREATE OR REPLACE TABLE video_embeddings AS
WITH embedding_index AS (
  SELECT
    video_file,
    AI_MULTI_EMBED('twelvelabs-marengo-embed-3-0', video_file) AS embeddings
  FROM video_table
)
SELECT
  video_file,
  f.value['embedding']::VECTOR(FLOAT, 512) AS embedding_vec,
  f.value['embedding_option']::STRING      AS embedding_option,
  f.value['start_sec']::FLOAT              AS start_sec,
  f.value['end_sec']::FLOAT                AS end_sec
FROM embedding_index,
LATERAL FLATTEN(input => embedding_index.embeddings['value']) f;

WITH query AS (
  SELECT
    (AI_MULTI_EMBED(
      'twelvelabs-marengo-embed-3-0',
      'Find segments where there is a man riding a skateboard'
    )):value[0]['embedding']::VECTOR(FLOAT, 512) AS query_embedding
)
SELECT
  v.video_file,
  v.start_sec,
  v.end_sec,
  VECTOR_COSINE_SIMILARITY(v.embedding_vec, q.query_embedding) AS similarity
FROM video_embeddings v
CROSS JOIN query q
ORDER BY similarity DESC
LIMIT 10;
```

## Limitations

- The `twelvelabs-marengo-embed-3-0` model has the following input limits:

  - Maximum video or audio duration: 4 hours
  - Maximum video or audio file size: 6 GB
  - Maximum text length: 500 tokens
  - Maximum image size: 5 MB
- The model is available in AWS US East 1 (N. Virginia) only. Cross-region inference is supported.
- FILE objects for AI\_MULTI\_EMBED can reference files in internal stages and external stages on AWS,
  Azure, or Google Cloud Storage. All stage encryption types are supported, including server-side
  encryption (SSE) and customer-side encryption (CSE).
- AI\_MULTI\_EMBED supports stages protected by [network policies](/user-guide/network-policies).

## Legal notices

Refer to [Snowflake AI and ML](/guides-overview-ai-features).
