#!/usr/bin/env bash
# Idempotent setup for a fresh cloud session.
set -e
cd "$(dirname "$0")"
[ -d node_modules/gsap ] || npm i --silent
python3 -c "import numpy, kokoro_onnx, soundfile, scipy" 2>/dev/null || python3 -m pip install -q numpy kokoro-onnx soundfile scipy
python3 -c "import numpy, kokoro_onnx, soundfile, scipy" || { echo "ERROR: voice Python packages missing for $(command -v python3)"; exit 1; }
python3 -c "import pitchapi" 2>/dev/null || python3 -m pip install -q pitchapi || echo "WARN: pitchapi SDK not installed"
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
# Helper models straight from Hugging Face (IndexTTS's own downloader picks a China mirror when it can't reach Google).
if [ -f "$IDX/checkpoints/config.yaml" ] && [ ! -f "$IDX/checkpoints/hf_cache/bigvgan/bigvgan_generator.pt" ]; then
  (cd "$IDX" && .venv/bin/python - <<'PY'
import os, shutil
from huggingface_hub import snapshot_download, hf_hub_download
c = "checkpoints/hf_cache"; os.makedirs(c, exist_ok=True)
snapshot_download("facebook/w2v-bert-2.0", local_dir=f"{c}/w2v-bert-2.0")
shutil.copy2(hf_hub_download("amphion/MaskGCT", "semantic_codec/model.safetensors", local_dir=f"{c}/_maskgct"), f"{c}/semantic_codec_model.safetensors")
hf_hub_download("funasr/campplus", "campplus_cn_common.bin", local_dir=c)
for f in ("config.json", "bigvgan_generator.pt"):
    hf_hub_download("nvidia/bigvgan_v2_22khz_80band_256x", f, local_dir=f"{c}/bigvgan")
PY
  ) || echo "WARN: IndexTTS helper model download failed"
fi
[ -f assets/voice/scout_reference.wav ] || echo "NOTE: add assets/voice/scout_reference.wav to use IndexTTS"
