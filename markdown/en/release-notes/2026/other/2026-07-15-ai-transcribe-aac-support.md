# Jul 15, 2026: AI\_TRANSCRIBE now supports AAC audio files

Snowflake Cortex AI\_TRANSCRIBE now supports AAC (Advanced Audio Coding) input, both as a standalone audio file and as
the audio track inside a supported video file. Because AAC is one of the most widely used audio codecs across podcasts,
streaming, and video pipelines, you can now transcribe a wider range of real-world recordings directly in Snowflake,
without first converting them to another format.

Key use cases include:

- **Transcribe streaming and broadcast audio:** AAC is a dominant codec for internet radio, live streams, and digital
  broadcasting. Transcribe audio captured as AAC for media monitoring, search, and analysis.
- **Process podcast and media libraries:** AAC is a standard codec for podcast and streaming audio distribution.
  Transcribe episodes and media archives to power search, summarization, and content analysis.
- **Analyze video soundtracks:** AAC is the default audio track in MP4 video. Transcribe webinars, interviews, and
  marketing videos whose audio is encoded as AAC.
- **Transcribe contact center and call recordings:** Many call recording and streaming platforms store captured audio as
  AAC. Transcribe support calls and combine the output with other Cortex AI Functions for sentiment and quality analysis.
- **Simplify audio ingestion pipelines:** Ingest AAC files as-is and transcribe them with a single SQL query,
  eliminating custom transcoding steps before analysis.

For more information, see [AI\_TRANSCRIBE](/sql-reference/functions/ai_transcribe).
