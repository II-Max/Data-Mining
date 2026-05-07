# Data

This folder stores runtime data and secrets used by the pipeline.

- `API.env` — Place your SerpApi key here. Either a single line with the key, or `SERPAPI_KEY=your_key`.
- Output Excel files created by the pipeline are saved here by default.
- `mining_log.txt` — Operation logs are written to `logs/mining_log.txt` by default.

Security: Do not commit `API.env` to version control. Add `Data/API.env` to `.gitignore` if needed.
