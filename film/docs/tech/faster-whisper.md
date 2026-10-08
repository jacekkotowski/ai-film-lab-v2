# faster-whisper — captions

- **Optional extra**, not one of the four core packages:
  `uv sync --extra voice` (~100 MB model, fetched once). Without it,
  captions simply don't happen; the menu offers the install.
- Runs on this machine; nothing is sent anywhere.
- **Where the model is** (2026-10-08): `models/whisper/`, through
  `WhisperModel(..., download_root=...)` (`voice.speech_models_dir`).
  Without `download_root` it goes to `%USERPROFILE%\.cache\huggingface\hub`.
  The folder has the huggingface cache layout
  (`models--Systran--faster-whisper-small/snapshots/<hash>/model.bin` and
  three small files, no links on Windows), so a model already in the user
  cache can be moved in as it is: measured, `local_files_only=True` loads
  `small` from there in 8.6 s.
- The English transcriber misses German/Polish words, names and numbers:
  the `fix-captions` skill places those from the measured speech and keeps
  the script's spelling.
- Captions take their spelling from the text you pasted when recording:
  `narration.txt` (pictures), `script_intro.txt` / `script_outro.txt`
  (camera), `intro.txt` / `closing.txt` / `script.txt` (older projects).
