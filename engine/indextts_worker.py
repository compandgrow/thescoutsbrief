"""Runs inside the IndexTTS virtualenv (its own Python 3.11 + torch). Called by engine/voice.py.

  <indextts>/.venv/bin/python engine/indextts_worker.py jobs.json

jobs.json = {"model_dir": "...", "speaker": "ref.wav", "jobs": [{"text", "emo_vector", "emo_alpha", "out"}, ...]}
Loads the model once and writes one wav per job. Emotion vector order:
[happy, angry, sad, afraid, disgusted, melancholic, surprised, calm]
"""
import json, os, sys, time

spec = json.load(open(sys.argv[1]))
model_dir = spec["model_dir"]
sys.path.insert(0, os.path.dirname(model_dir))   # the IndexTTS checkout
from indextts.infer_v2_5 import IndexTTS2        # noqa: E402

t0 = time.time()
tts = IndexTTS2(cfg_path=os.path.join(model_dir, "config.yaml"), model_dir=model_dir, device="cpu")
print(f"model loaded in {time.time() - t0:.0f}s", flush=True)
for i, job in enumerate(spec["jobs"]):
    t1 = time.time()
    tts.infer(spk_audio_prompt=spec["speaker"], text=job["text"], output_path=job["out"], lang="EN",
              emo_vector=job["emo_vector"], emo_alpha=job.get("emo_alpha", 1.0), use_random=False, verbose=False)
    print(f"[{i + 1}/{len(spec['jobs'])}] {time.time() - t1:.0f}s  {job['text'][:60]}", flush=True)
