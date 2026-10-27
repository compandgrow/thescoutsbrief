// Render a reel to MP4 (or a contact sheet of stills).
//   node engine/render.js reels/<id>            -> reels/<id>/out/reel.mp4
//   node engine/render.js reels/<id> probe 1 4 9 -> reels/<id>/out/probe.jpg
// Frames are drawn by window.seek(t) in headless Chromium, so output is deterministic.
const { chromium } = require("playwright");
const http = require("http");
const fs = require("fs");
const path = require("path");
const { execFileSync } = require("child_process");

const ROOT = path.resolve(__dirname, "..");
const FPS = 30;
const PARTS = Math.max(1, Math.min(4, require("os").cpus().length - 1));
const TYPES = { ".html": "text/html", ".js": "text/javascript", ".json": "application/json", ".woff2": "font/woff2", ".css": "text/css", ".png": "image/png", ".jpg": "image/jpeg", ".svg": "image/svg+xml" };

function serve() {
  return new Promise((res) => {
    const srv = http.createServer((req, rsp) => {
      const f = path.join(ROOT, decodeURIComponent(req.url.split("?")[0]));
      if (!f.startsWith(ROOT) || !fs.existsSync(f) || fs.statSync(f).isDirectory()) { rsp.writeHead(404); return rsp.end(); }
      rsp.writeHead(200, { "Content-Type": TYPES[path.extname(f)] || "application/octet-stream" });
      fs.createReadStream(f).pipe(rsp);
    });
    srv.listen(0, () => res(srv));
  });
}

async function openPage(browser, port, reelDir) {
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
  page.on("pageerror", (e) => console.error("PAGE ERROR:", e.message));
  const reel = JSON.parse(fs.readFileSync(path.join(ROOT, reelDir, "reel.json")));
  const tpl = reel.template || "templates/match-reel.html";
  await page.goto(`http://localhost:${port}/${tpl}?reel=${encodeURIComponent(reelDir)}`);
  await page.waitForFunction("window.ready === true", null, { timeout: 60000 });
  return page;
}

async function shot(page, t, file) {
  await page.evaluate((t) => { window.seek(t); return new Promise((r) => requestAnimationFrame(() => requestAnimationFrame(r))); }, t);
  await page.locator("#stage").screenshot({ path: file, type: "jpeg", quality: 92 });
}

(async () => {
  const [reelDir, mode, ...times] = process.argv.slice(2);
  const out = path.join(ROOT, reelDir, "out");
  fs.mkdirSync(out, { recursive: true });
  const srv = await serve();
  const port = srv.address().port;
  const browser = await chromium.launch();

  if (mode === "probe") {
    const page = await openPage(browser, port, reelDir);
    const files = [];
    for (const [i, t] of times.entries()) { const f = path.join(out, `probe_${i}.jpg`); await shot(page, Number(t), f); files.push(f); }
    const cols = Math.min(files.length, 4);
    const rows = Math.ceil(files.length / cols);
    if (files.length === 1) fs.copyFileSync(files[0], path.join(out, "probe.jpg"));
    else execFileSync("ffmpeg", ["-y", "-loglevel", "error", ...files.flatMap((f) => ["-i", f]), "-filter_complex",
      files.map((_, i) => `[${i}]scale=360:-1[s${i}]`).join(";") + ";" + files.map((_, i) => `[s${i}]`).join("") + `xstack=inputs=${files.length}:layout=${files.map((_, i) => `${(i % cols) * 360}_${Math.floor(i / cols) * 640}`).join("|")}:fill=black`,
      path.join(out, "probe.jpg")]);
    console.log("probe ->", path.join(out, "probe.jpg"), `(${rows}x${cols})`);
  } else {
    const timing = JSON.parse(fs.readFileSync(path.join(ROOT, reelDir, "timing.json")));
    const N = Math.ceil(timing.duration * FPS);
    const fdir = path.join(out, "frames");
    fs.rmSync(fdir, { recursive: true, force: true });
    fs.mkdirSync(fdir, { recursive: true });
    const t0 = Date.now();
    await Promise.all([...Array(PARTS).keys()].map(async (k) => {
      const page = await openPage(browser, port, reelDir);
      for (let f = k; f < N; f += PARTS) {
        await shot(page, f / FPS, path.join(fdir, `f_${String(f).padStart(5, "0")}.jpg`));
        if (k === 0 && f % 150 === 0) console.log(`frame ${f}/${N}  ${((Date.now() - t0) / 1000).toFixed(0)}s`);
      }
    }));
    const mixf = path.join(ROOT, reelDir, "audio/mix.wav");
    const mp4 = path.join(out, "reel.mp4");
    execFileSync("ffmpeg", ["-y", "-loglevel", "error", "-framerate", String(FPS), "-i", path.join(fdir, "f_%05d.jpg"), "-i", mixf,
      "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-crf", "18", "-preset", "medium", "-pix_fmt", "yuv420p",
      "-vf", "scale=in_range=pc:out_range=tv:out_color_matrix=bt709", "-color_range", "tv", "-colorspace", "bt709",
      "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-shortest", "-movflags", "+faststart", mp4]);
    execFileSync("ffmpeg", ["-y", "-loglevel", "error", "-i", mp4, "-vf", "fps=1,scale=180:-1,tile=8x" + Math.ceil(timing.duration / 8), "-frames:v", "1", path.join(out, "sheet.jpg")]);
    console.log(`done ${N} frames in ${((Date.now() - t0) / 1000).toFixed(0)}s -> ${mp4}`);
  }
  await browser.close();
  srv.close();
})();
