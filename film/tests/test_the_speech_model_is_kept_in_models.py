"""
The speech model is kept in models/.

2026-10-08: faster-whisper put the speech model (small 464 MB, base 142 MB)
in the user folder, %USERPROFILE%\\.cache\\huggingface\\hub, where nobody
looks and nothing of this toolkit's reaches -- while models/README.md says
the toolkit's models live in models/ "and nowhere else". Now it goes in
models/whisper/, beside the other three, ignored by git like them.
"""

import sys
import types

import pytest

from ffilm import voice


def test_the_speech_model_folder_is_inside_models(tmp_path, monkeypatch):
    monkeypatch.setenv("FFILM_MODELS", str(tmp_path))
    assert voice.speech_models_dir() == tmp_path / "whisper"


def test_a_model_in_the_users_cache_does_not_count(tmp_path, monkeypatch):
    """Only models/ is looked in; the old place is not a second home."""
    monkeypatch.setenv("FFILM_MODELS", str(tmp_path / "models"))
    monkeypatch.setenv("HF_HOME", str(tmp_path / "hf"))
    old = tmp_path / "hf" / "hub" / "models--Systran--faster-whisper-small"
    (old / "snapshots" / "abc").mkdir(parents=True)
    (old / "snapshots" / "abc" / "model.bin").write_bytes(b"x")
    assert not voice._model_cached("small")


def test_a_model_in_models_counts_once_its_weights_are_there(tmp_path, monkeypatch):
    monkeypatch.setenv("FFILM_MODELS", str(tmp_path))
    repo = tmp_path / "whisper" / "models--Systran--faster-whisper-small"
    (repo / "snapshots" / "abc").mkdir(parents=True)
    assert not voice._model_cached("small")          # a download just begun
    (repo / "snapshots" / "abc" / "model.bin").write_bytes(b"x")
    assert voice._model_cached("small")


def test_the_transcriber_is_told_to_download_into_models(tmp_path, monkeypatch):
    """Checked on the call itself, with a stand-in for faster-whisper that
    records what it was given and stops there: no model, no network."""
    monkeypatch.setenv("FFILM_MODELS", str(tmp_path))
    given = {}

    class WhisperModel:
        def __init__(self, size, **kw):
            given.update(kw, size=size)
            raise RuntimeError("stand-in stops here")

    monkeypatch.setitem(sys.modules, "faster_whisper",
                        types.SimpleNamespace(WhisperModel=WhisperModel))
    with pytest.raises(SystemExit):
        voice.transcribe(tmp_path / "take.wav", "small")
    assert given["size"] == "small"
    assert given["download_root"] == str(tmp_path / "whisper")
