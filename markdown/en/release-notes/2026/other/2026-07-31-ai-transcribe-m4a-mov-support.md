# Jul 31, 2026: AI\_TRANSCRIBE now supports M4A and MOV files

Snowflake Cortex AI\_TRANSCRIBE now supports M4A audio files and MOV (QuickTime) video files, including M4A audio
encoded with Apple Lossless (ALAC). M4A and MOV are common across Apple devices, screen and video recording tools,
and media production workflows, so you can now transcribe more of your existing recordings directly in Snowflake
without converting them to another format first.

Key use cases include:

- **Transcribe recordings from Apple devices:** M4A is the default format for voice memos and audio recordings on
  iPhone, iPad, and Mac. Transcribe them directly for search, summarization, and analysis.
- **Process screen and video recordings:** MOV is the native container for QuickTime, macOS, and iOS screen
  recordings. Transcribe demos, meetings, and webinars captured as MOV.
- **Analyze media production assets:** MOV is widely used in professional video editing and camera workflows.
  Transcribe raw or exported footage for captions, indexing, and content analysis.
- **Transcribe lossless audio:** M4A files encoded with Apple Lossless (ALAC) are supported, so you can transcribe
  high-quality archival recordings without re-encoding them first.
- **Simplify ingestion pipelines:** Ingest M4A and MOV files as-is and transcribe them with a single SQL query,
  eliminating custom transcoding steps before analysis.

For more information, see [AI\_TRANSCRIBE](/sql-reference/functions/ai_transcribe).
