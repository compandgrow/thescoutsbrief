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
