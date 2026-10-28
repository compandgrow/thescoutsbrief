#!/usr/bin/env bash
# Idempotent setup for a fresh cloud session.
set -e
cd "$(dirname "$0")"
[ -d node_modules/gsap ] || npm i --silent
python3 -c "import kokoro_onnx, soundfile, scipy" 2>/dev/null || pip install -q kokoro-onnx soundfile scipy
python3 -c "import pitchapi" 2>/dev/null || pip install -q pitchapi || echo "WARN: pitchapi SDK not installed"
mkdir -p models
for f in kokoro-v1.0.onnx voices-v1.0.bin; do
  [ -s models/$f ] || curl -sSL -o models/$f "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/$f"
done
echo "setup ok"

# --- IndexTTS 2.5 (emotional voice). Optional: falls back to the offline voice if anything is missing.
IDX=/home/user/indextts
if [ ! -d "$IDX" ]; then
  git clone -q --depth 1 --branch v2.5.0 https://github.com/index-tts/index-tts.git "$IDX" || echo "WARN: IndexTTS clone failed"
fi
if [ -d "$IDX" ] && [ ! -x "$IDX/.venv/bin/python" ]; then
  (cd "$IDX" && uv venv -q --python 3.11 .venv \
    && uv pip install -q --python .venv/bin/python "torch==2.8.*" "torchaudio==2.8.*" \
    && uv pip install -q --python .venv/bin/python --no-sources -e . "huggingface_hub[cli]") || echo "WARN: IndexTTS install failed"
fi
if [ -x "$IDX/.venv/bin/python" ] && [ ! -f "$IDX/checkpoints/config.yaml" ]; then
  if curl -s -o /dev/null --max-time 10 https://huggingface.co; then
    (cd "$IDX" && .venv/bin/hf download IndexTeam/IndexTTS-2.5 --local-dir=checkpoints) || echo "WARN: IndexTTS model download failed"
  else
    echo "NOTE: huggingface.co is blocked; IndexTTS models not downloaded (offline voice will be used)"
  fi
fi
[ -f assets/voice/scout_reference.wav ] || echo "NOTE: add assets/voice/scout_reference.wav to use IndexTTS"
