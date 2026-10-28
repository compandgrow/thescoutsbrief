// "Scout" — the gorilla presenter for The Scout Brief.
// Pure function of state: Presenter.draw({t, emo, mouth, slam}) sets every attribute.
// Emotion = a blend of numeric face parameters, so any two moods can cross-fade.

const NS = "http://www.w3.org/2000/svg";

export const EMOTIONS = {
  //            brow angle(+ = angry)  brow lift  eye open  pupil  smile(-1..1)  mouth width  round(O)  red  shake  steam  vein  tilt  blush  bounce
  neutral:      { brow: 0,   lift: 0,   eye: 1.0,  pupil: 1.0, smile: 0.25, width: 1.0,  round: 0,   red: 0,    shake: 0,  steam: 0, vein: 0, tilt: 0,  blush: 0.15, bounce: 0 },
  smug:         { brow: 6,   lift: 4,   eye: 0.72, pupil: 1.0, smile: 0.55, width: 0.95, round: 0,   red: 0,    shake: 0,  steam: 0, vein: 0, tilt: 5,  blush: 0.2,  bounce: 0, asym: 1 },
  happy:        { brow: -4,  lift: 9,   eye: 0.9,  pupil: 1.05,smile: 0.9,  width: 1.15, round: 0,   red: 0,    shake: 0,  steam: 0, vein: 0, tilt: -2, blush: 0.5,  bounce: 0.4 },
  excited:      { brow: -6,  lift: 16,  eye: 1.18, pupil: 1.15,smile: 1.0,  width: 1.25, round: 0,   red: 0,    shake: 0,  steam: 0, vein: 0, tilt: 0,  blush: 0.6,  bounce: 1 },
  shocked:      { brow: -10, lift: 24,  eye: 1.35, pupil: 0.65,smile: 0,    width: 0.6,  round: 1,   red: 0,    shake: 1,  steam: 0, vein: 0, tilt: 0,  blush: 0,    bounce: 0 },
  disappointed: { brow: -16, lift: 2,   eye: 0.62, pupil: 1.0, smile: -0.6, width: 0.9,  round: 0,   red: 0,    shake: 0,  steam: 0, vein: 0, tilt: -6, blush: 0,    bounce: 0 },
  angry:        { brow: 22,  lift: -8,  eye: 0.78, pupil: 0.85,smile: -0.7, width: 1.05, round: 0,   red: 0.45, shake: 3,  steam: 0.25, vein: 1, tilt: 0, blush: 0, bounce: 0 },
  laughing:     { brow: -8,  lift: 14,  eye: 0.35, pupil: 1.0, smile: 1.0,  width: 1.3,  round: 0,   red: 0.12, shake: 0,  steam: 0, vein: 0, tilt: -4, blush: 0.9,  bounce: 1.2, laugh: 1 },
  furious:      { brow: 32,  lift: -12, eye: 0.62, pupil: 0.7, smile: -1.0, width: 1.25, round: 0,   red: 0.9,  shake: 9,  steam: 1, vein: 1, tilt: 0,  blush: 0,    bounce: 0 },
};

const SKIN = [104, 94, 112], RAGE = [196, 52, 44];   // gorilla face grey -> rage red
const MUZ = [140, 129, 145], MUZ_RAGE = [222, 96, 82];
const lerp = (a, b, k) => a + (b - a) * k;
const mix = (c1, c2, k) => `rgb(${c1.map((v, i) => Math.round(lerp(v, c2[i], k))).join(",")})`;
const hash = (n) => { const s = Math.sin(n * 127.1 + 311.7) * 43758.5453; return s - Math.floor(s); };

export function blend(a, b, k) {
  const out = {};
  for (const key of Object.keys(EMOTIONS.neutral)) out[key] = lerp(a[key] ?? 0, b[key] ?? 0, k);
  out.asym = lerp(a.asym ?? 0, b.asym ?? 0, k);
  out.laugh = lerp(a.laugh ?? 0, b.laugh ?? 0, k);
  return out;
}

function el(tag, attrs = {}, parent) {
  const e = document.createElementNS(NS, tag);
  for (const [k, v] of Object.entries(attrs)) e.setAttribute(k, v);
  if (parent) parent.appendChild(e);
  return e;
}

const DEFAULT_THEME = { accent: "#8b5cf6", suit: ["#241a38", "#140f20"], desk: ["#2a1f45", "#130e1f"], lapel: "#1b1430" };

export function createPresenter(container, opts = {}) {
  const T = { ...DEFAULT_THEME, ...(opts.theme || {}) };
  const W = 700, H = 760;
  const svg = el("svg", { viewBox: `0 0 ${W} ${H}`, width: "100%", height: "100%", style: "overflow:visible" });
  container.appendChild(svg);
  const defs = el("defs", {}, svg);
  const suitGrad = el("linearGradient", { id: "suit", x1: 0, y1: 0, x2: 0, y2: 1 }, defs);
  el("stop", { offset: 0, "stop-color": T.suit[0] }, suitGrad);
  el("stop", { offset: 1, "stop-color": T.suit[1] }, suitGrad);
  const deskGrad = el("linearGradient", { id: "desk", x1: 0, y1: 0, x2: 0, y2: 1 }, defs);
  el("stop", { offset: 0, "stop-color": T.desk[0] }, deskGrad);
  el("stop", { offset: 1, "stop-color": T.desk[1] }, deskGrad);
  const glow = el("radialGradient", { id: "rage", cx: 0.5, cy: 0.5, r: 0.5 }, defs);
  el("stop", { offset: 0, "stop-color": "#ff3b2f", "stop-opacity": 0.55 }, glow);
  el("stop", { offset: 1, "stop-color": "#ff3b2f", "stop-opacity": 0 }, glow);

  const back = el("radialGradient", { id: "backlight", cx: 0.5, cy: 0.5, r: 0.5 }, defs);
  el("stop", { offset: 0, "stop-color": T.accent, "stop-opacity": 0.38 }, back);
  el("stop", { offset: 1, "stop-color": T.accent, "stop-opacity": 0 }, back);
  el("ellipse", { cx: 350, cy: 300, rx: 300, ry: 280, fill: "url(#backlight)" }, svg);
  const rageGlow = el("ellipse", { cx: 350, cy: 300, rx: 330, ry: 300, fill: "url(#rage)", opacity: 0 }, svg);

  // whole figure (shake + bounce applied here)
  const fig = el("g", {}, svg);
  const FUR = "#24202a", FUR_HI = "#3a3442", MUZZLE = "#8c8191";
  // torso: big gorilla shoulders in a suit
  const torso = el("g", {}, fig);
  el("path", { d: "M30 760 C30 560 150 470 350 470 C550 470 670 560 670 760 Z", fill: "url(#suit)", stroke: T.accent, "stroke-opacity": 0.4, "stroke-width": 4 }, torso);
  el("path", { d: "M290 478 L350 610 L410 478 Z", fill: "#f4f1ff" }, torso);              // shirt
  el("path", { d: "M336 500 L364 500 L376 650 L350 682 L324 650 Z", fill: T.accent }, torso); // tie
  el("path", { d: "M290 478 L350 610 L245 560 Z M410 478 L350 610 L455 560 Z", fill: T.lapel }, torso); // lapels
  el("circle", { cx: 500, cy: 610, r: 15, fill: T.accent }, torso);                       // badge
  el("circle", { cx: 500, cy: 610, r: 6, fill: "#0d0a14" }, torso);
  // fur poking out of the collar
  el("path", { d: "M262 482 C280 470 300 492 318 474 C334 492 352 466 370 482 C386 466 404 490 420 474 C430 486 440 480 446 484 L430 500 L272 500 Z", fill: FUR }, torso);

  // head group (tilt applied here)
  const head = el("g", {}, fig);
  // fur skull with sagittal crest
  el("path", { d: "M350 52 C392 52 420 80 440 104 C510 128 540 200 540 290 C540 410 470 492 350 492 C230 492 160 410 160 290 C160 200 190 128 260 104 C280 80 308 52 350 52 Z", fill: FUR, stroke: T.accent, "stroke-opacity": 0.55, "stroke-width": 5 }, head);
  // fur tufts
  for (const [x1, y1, x2, y2] of [[300, 70, 320, 112], [350, 58, 352, 104], [400, 70, 382, 112], [200, 180, 228, 206], [500, 180, 472, 206], [180, 330, 206, 340], [520, 330, 494, 340]])
    el("path", { d: `M${x1} ${y1} Q${(x1 + x2) / 2 + 6} ${(y1 + y2) / 2} ${x2} ${y2}`, fill: "none", stroke: FUR_HI, "stroke-width": 6, "stroke-linecap": "round" }, head);
  const earL = el("ellipse", { cx: 168, cy: 292, rx: 22, ry: 28 }, head);
  const earR = el("ellipse", { cx: 532, cy: 292, rx: 22, ry: 28 }, head);
  // face mask: eye lobes + forehead + big muzzle
  const face = el("path", { d: "M350 196 C380 178 470 176 478 236 C486 290 462 318 446 330 C470 352 476 400 456 440 C432 484 392 496 350 496 C308 496 268 484 244 440 C224 400 230 352 254 330 C238 318 214 290 222 236 C230 176 320 178 350 196 Z" }, head);
  const muzzle = el("path", { d: "M350 318 C420 316 462 350 460 410 C458 466 410 492 350 492 C290 492 242 466 240 410 C238 350 280 316 350 318 Z", fill: MUZZLE, class: "muzzle" }, head);
  // headset (over the fur)
  el("path", { d: "M176 300 C160 70 540 70 524 300", fill: "none", stroke: "#0d0a14", "stroke-width": 15, "stroke-linecap": "round" }, head);
  el("rect", { x: 150, y: 262, width: 38, height: 72, rx: 15, fill: "#0d0a14" }, head);
  el("rect", { x: 512, y: 262, width: 38, height: 72, rx: 15, fill: "#0d0a14" }, head);
  el("path", { d: "M170 330 C176 420 222 450 262 452", fill: "none", stroke: "#0d0a14", "stroke-width": 7, "stroke-linecap": "round" }, head);
  el("circle", { cx: 266, cy: 452, r: 11, fill: T.accent }, head);

  const blushL = el("ellipse", { cx: 262, cy: 366, rx: 26, ry: 13, fill: "#d27a8c" }, head);
  const blushR = el("ellipse", { cx: 438, cy: 366, rx: 26, ry: 13, fill: "#d27a8c" }, head);

  // eyes
  function makeEye(cx) {
    const g = el("g", {}, head);
    const clipId = "eyeclip" + cx;
    const cp = el("clipPath", { id: clipId }, defs);
    const clipE = el("ellipse", { cx, cy: 285, rx: 31, ry: 34 }, cp);
    const white = el("ellipse", { cx, cy: 285, rx: 31, ry: 34, fill: "#f6efe4" }, g);
    const inner = el("g", { "clip-path": `url(#${clipId})` }, g);
    const iris = el("circle", { cx, cy: 288, r: 17, fill: "#6b3f1f" }, inner);
    const pupil = el("circle", { cx, cy: 288, r: 9, fill: "#0d0a14" }, inner);
    const shine = el("circle", { cx: cx + 5, cy: 282, r: 4.5, fill: "#fff" }, inner);
    const lid = el("rect", { x: cx - 45, y: 200, width: 90, height: 60 }, inner);       // upper lid (skin)
    const lidLine = el("path", { fill: "none", stroke: "#1a161d", "stroke-width": 5, "stroke-linecap": "round" }, g);
    return { cx, clipE, white, iris, pupil, shine, lid, lidLine };
  }
  const eyeL = makeEye(290), eyeR = makeEye(410);
  // heavy brow ridge
  const browL = el("path", { fill: "#1a161d" }, head);
  const browR = el("path", { fill: "#1a161d" }, head);
  // wide gorilla nose with nostrils
  el("path", { d: "M306 332 C314 306 386 306 394 332 C400 352 378 362 350 360 C322 362 300 352 306 332 Z", fill: "#4a4150", class: "nose" }, head);
  el("ellipse", { cx: 333, cy: 344, rx: 11, ry: 7, fill: "#16121a", transform: "rotate(-14 333 344)" }, head);
  el("ellipse", { cx: 367, cy: 344, rx: 11, ry: 7, fill: "#16121a", transform: "rotate(14 367 344)" }, head);

  // mouth
  const mouthClip = el("clipPath", { id: "mouthclip" }, defs);
  const mouthClipPath = el("path", {}, mouthClip);
  const mouthG = el("g", {}, head);
  const mouthFill = el("path", { fill: "#2a0a14" }, mouthG);
  const mouthInner = el("g", { "clip-path": "url(#mouthclip)" }, mouthG);
  const teeth = el("rect", { x: 250, y: 0, width: 200, height: 14, fill: "#f6efe4" }, mouthInner);
  const fangs = [326, 374].map((x) => el("path", { d: `M${x - 9} 0 L${x + 9} 0 L${x} 26 Z`, fill: "#f6efe4" }, mouthInner));
  const tongue = el("ellipse", { cx: 350, cy: 0, rx: 36, ry: 18, fill: "#c9435a" }, mouthInner);
  const mouthLine = el("path", { fill: "none", stroke: "#1a161d", "stroke-width": 6, "stroke-linecap": "round", "stroke-linejoin": "round" }, mouthG);

  // anger marks
  const vein = el("g", { transform: "translate(452 150)" }, head);
  for (const r of [0, 90, 180, 270])
    el("path", { d: "M6 -4 C14 -14 22 -8 18 0", fill: "none", stroke: "#ff3b3b", "stroke-width": 8, "stroke-linecap": "round", transform: `rotate(${r})` }, vein);
  const tears = [290, 410].map((x) => el("path", { d: `M${x + (x < 350 ? -38 : 38)} 300 C${x + (x < 350 ? -50 : 50)} 325 ${x + (x < 350 ? -46 : 46)} 340 ${x + (x < 350 ? -38 : 38)} 340 C${x + (x < 350 ? -30 : 30)} 340 ${x + (x < 350 ? -26 : 26)} 325 ${x + (x < 350 ? -38 : 38)} 300 Z`, fill: "#7fd3ff" }, head));
  const sweat = el("path", { d: "M486 196 C474 218 476 232 486 234 C496 232 498 218 486 196 Z", fill: "#7fd3ff" }, head);

  // steam puffs (above head, outside head group so they rise straight)
  const steamG = el("g", {}, fig);
  const puffs = [];
  for (let i = 0; i < 8; i++) puffs.push(el("circle", { r: 20, fill: "#f4f1ff" }, steamG));

  // desk + big gorilla fists
  const deskG = el("g", {}, svg);
  const fistL = el("g", {}, deskG), fistR = el("g", {}, deskG);
  for (const f of [fistL, fistR]) {
    el("rect", { x: -62, y: -44, width: 124, height: 80, rx: 34, fill: T.lapel }, f);      // sleeve
    el("path", { d: "M-58 -46 C-50 -64 50 -64 58 -46 L54 -38 L-54 -38 Z", fill: FUR }, f);  // fur at the cuff
    el("rect", { x: -56, y: -100, width: 112, height: 78, rx: 30, class: "skin" }, f);
    for (const dx of [-28, 0, 28]) el("path", { d: `M${dx} -98 L${dx} -70`, stroke: "#2e2833", "stroke-width": 5, "stroke-linecap": "round" }, f);
  }
  const deskTop = el("rect", { x: -220, y: 600, width: W + 440, height: 26, rx: 6, fill: T.accent }, deskG);
  const deskFront = el("rect", { x: -220, y: 624, width: W + 440, height: 140, fill: "url(#desk)" }, deskG);

  const skins = () => [face, earL, earR, eyeL.lid, eyeR.lid, ...svg.querySelectorAll(".skin")];
  const muzzles = () => [muzzle];

  function eyeDraw(e, s, side, blink, gx, gy) {
    const open = Math.max(0.04, s.eye * blink);
    const ry = 34 * Math.min(open, 1.35);
    const rx = 31 * (1 + (s.eye - 1) * 0.25);
    e.clipE.setAttribute("ry", ry); e.white.setAttribute("ry", ry);
    e.clipE.setAttribute("rx", rx); e.white.setAttribute("rx", rx);
    const px = e.cx + gx, py = 288 + gy;
    e.iris.setAttribute("cx", px); e.iris.setAttribute("cy", py);
    e.iris.setAttribute("r", 15 * (0.85 + 0.15 * s.pupil));
    e.pupil.setAttribute("cx", px); e.pupil.setAttribute("cy", py);
    e.pupil.setAttribute("r", 8 * s.pupil);
    e.shine.setAttribute("cx", px + 5); e.shine.setAttribute("cy", py - 6);
    // angry lid: slanted toward the nose
    const slant = s.brow * 0.9 * side;                       // side: -1 left eye, +1 right eye
    const lidY = 285 - ry - 2 + Math.max(0, s.brow) * 0.55;
    e.lid.setAttribute("y", lidY - 60);
    e.lid.setAttribute("transform", `rotate(${slant} ${e.cx} ${lidY})`);
    // lid line follows top of the visible eye
    const ty = Math.max(285 - ry, lidY);
    const a = (slant * Math.PI) / 180;
    const x1 = e.cx - rx, x2 = e.cx + rx;
    const y1 = ty - Math.tan(a) * rx, y2 = ty + Math.tan(a) * rx;
    e.lidLine.setAttribute("d", blink < 0.25 ? `M${x1} 285 Q${e.cx} 292 ${x2} 285` : `M${x1} ${Math.min(y1, 285)} L${x2} ${Math.min(y2, 285)}`);
    e.lidLine.setAttribute("opacity", blink < 0.25 || s.brow > 8 ? 1 : 0);
    if (s.laugh > 0.5) {               // ^ ^ eyes
      e.white.setAttribute("opacity", 0); e.iris.setAttribute("opacity", 0); e.pupil.setAttribute("opacity", 0); e.shine.setAttribute("opacity", 0);
      e.lidLine.setAttribute("d", `M${e.cx - 30} 296 Q${e.cx} 262 ${e.cx + 30} 296`);
      e.lidLine.setAttribute("opacity", 1); e.lidLine.setAttribute("stroke-width", 8);
    } else {
      for (const n of [e.white, e.iris, e.pupil, e.shine]) n.setAttribute("opacity", 1);
      e.lidLine.setAttribute("stroke-width", 5);
    }
  }

  function browDraw(path, cx, side, s) {
    const asym = side < 0 ? s.asym * 8 : -s.asym * 4;
    const y = 232 - s.lift - asym;
    const ang = (s.brow * side * Math.PI) / 180;           // inner end down when angry
    const L = 50, th = 24;   // heavy gorilla brow ridge
    const dx = Math.cos(ang) * L, dy = Math.sin(ang) * L;
    const x1 = cx - dx, y1 = y - dy, x2 = cx + dx, y2 = y + dy;
    path.setAttribute("d", `M${x1} ${y1 - th / 2} Q${cx} ${y - th - 6} ${x2} ${y2 - th / 2} L${x2} ${y2 + th / 2} Q${cx} ${y - 2} ${x1} ${y1 + th / 2} Z`);
  }

  function mouthDraw(s, open) {
    const cx = 350, cy = 414;
    const round = s.round;
    const W2 = lerp(52 * s.width, 26, round) + open * 4;
    const smile = s.smile;
    const cornerY = cy - smile * 16;
    const o = Math.max(open, round * 0.85);
    const upY = cy - 2 - o * 10 - smile * 3 - (s.red > 0.5 ? o * 6 : 0);
    const loY = cy + 4 + o * 58 + Math.max(0, smile) * 14 - (smile < 0 ? smile * -4 : 0);
    const roundBulge = round * 30;
    const d = `M${cx - W2} ${cornerY} C${cx - W2 * 0.6} ${upY - roundBulge * 0.5} ${cx + W2 * 0.6} ${upY - roundBulge * 0.5} ${cx + W2} ${cornerY} C${cx + W2 * 0.7 + roundBulge * 0.3} ${loY} ${cx - W2 * 0.7 - roundBulge * 0.3} ${loY} ${cx - W2} ${cornerY} Z`;
    const visible = o > 0.05 || smile > 0.5;
    mouthClipPath.setAttribute("d", d);
    mouthFill.setAttribute("d", d);
    mouthFill.setAttribute("opacity", visible ? 1 : 0);
    teeth.setAttribute("y", upY - 6); teeth.setAttribute("height", 10 + o * 6 + (s.red > 0.5 ? 10 : 0));
    tongue.setAttribute("cy", loY - 6);
    const fangK = Math.min(1, Math.max(0, (s.red - 0.3) * 2.5));   // bared fangs when angry
    fangs.forEach((f, i) => { f.setAttribute("transform", `translate(0 ${upY + 2}) scale(1 ${0.3 + fangK})`); f.setAttribute("opacity", fangK > 0.05 ? 1 : 0); f.setAttribute("transform-origin", `${i ? 374 : 326} 0`); });
    tongue.setAttribute("opacity", o > 0.3 ? 1 : 0);
    if (visible) mouthLine.setAttribute("d", d);
    else mouthLine.setAttribute("d", `M${cx - W2} ${cornerY} Q${cx} ${cy + smile * 22} ${cx + W2} ${cornerY}`);
  }

  function draw({ t, emo, mouth = 0, slam = 0, fistY = 0 }) {
    const s = emo;
    // idle motion
    const breathe = Math.sin(t * 2 * Math.PI * 0.28) * 4;
    const bob = mouth * 3 + (s.laugh || 0) * Math.sin(t * Math.PI * 8.4) * 7 + s.bounce * Math.abs(Math.sin(t * Math.PI * 3.2)) * -12;
    const shakeX = s.shake * (Math.sin(t * 71) * 0.6 + Math.sin(t * 113) * 0.4);
    const shakeY = s.shake * 0.4 * Math.sin(t * 97);
    const slamDip = slam * 10;
    fig.setAttribute("transform", `translate(${shakeX} ${breathe * 0.5 + bob + shakeY + slamDip})`);
    const tilt = s.tilt + Math.sin(t * 0.9) * 1.5 + mouth * Math.sin(t * 5) * 1.2;
    head.setAttribute("transform", `rotate(${tilt} 350 470)`);

    // blink: deterministic, ~every 3.5 s
    const period = 3.5, k = Math.floor(t / period), ph = t - k * period - hash(k) * 2.2;
    const blink = ph > 0 && ph < 0.14 ? Math.abs(ph - 0.07) / 0.07 : 1;
    // gaze: mostly at camera, occasional glance to the card above
    const g = Math.sin(t * 0.7) > 0.85 ? 1 : 0;
    const gx = Math.sin(t * 0.37) * 3, gy = -g * 8 + (s.brow > 15 ? 3 : 0);

    const skin = mix(SKIN, RAGE, s.red);
    for (const n of skins()) n.setAttribute("fill", skin);
    for (const n of muzzles()) n.setAttribute("fill", mix(MUZ, MUZ_RAGE, s.red));
    rageGlow.setAttribute("opacity", Math.max(0, s.red - 0.3) * (0.8 + 0.2 * Math.sin(t * 12)));
    blushL.setAttribute("opacity", s.blush * 0.5); blushR.setAttribute("opacity", s.blush * 0.5);

    eyeDraw(eyeL, s, 1, blink, gx, gy);   // side flips so inner ends drop when angry
    eyeDraw(eyeR, s, -1, blink, gx, gy);
    browDraw(browL, 290, 1, s);
    browDraw(browR, 410, -1, s);
    const laughBeat = (s.laugh || 0) * Math.abs(Math.sin(t * Math.PI * 4.2));
    mouthDraw(s, Math.max(mouth, laughBeat * 0.75));
    tears.forEach((tr, i) => {
      const drop = ((t * 0.9 + i * 0.45) % 1);
      tr.setAttribute("opacity", s.laugh > 0.5 ? (1 - drop) : 0);
      tr.setAttribute("transform", `translate(0 ${drop * 40})`);
    });

    const vp = 1 + 0.12 * Math.sin(t * 14);
    vein.setAttribute("opacity", s.vein > 0.5 ? (s.vein - 0.5) * 2 : 0);
    vein.setAttribute("transform", `translate(452 150) scale(${vp})`);
    sweat.setAttribute("opacity", s.round * 0.9 + (s.smile < -0.4 && s.red < 0.2 ? 0.6 : 0));

    puffs.forEach((p, i) => {
      const side = i % 2 ? 1 : -1;
      const life = ((t * 1.3 + i * 0.37) % 1);
      const x = 350 + side * (130 + life * 90 + hash(i) * 20);
      const y = 150 - life * 170;
      p.setAttribute("cx", x); p.setAttribute("cy", y);
      p.setAttribute("r", 14 + life * 32);
      p.setAttribute("opacity", s.steam * (1 - life) * 0.85);
    });

    // fists rest on desk; slam lifts then drops them
    const up = s.red > 0.5 ? Math.max(0, Math.sin(t * 6)) * 6 : 0;
    fistL.setAttribute("transform", `translate(${200 + shakeX * 0.3} ${618 - up + fistY})`);
    fistR.setAttribute("transform", `translate(${500 + shakeX * 0.3} ${618 - up + fistY})`);
    deskG.setAttribute("transform", `translate(0 ${slam * 6})`);
  }

  return { draw, svg, deskFront };
}

// Smooth emotion over time from a list of [time, emotionName] cues.
export function emotionAt(cues, t, fade = 0.28) {
  let cur = EMOTIONS.neutral, prev = EMOTIONS.neutral, start = -10;
  for (const [ct, name] of cues) {
    if (ct > t) break;
    prev = blend(prev, cur, Math.min(1, (ct - start) / fade));
    cur = EMOTIONS[name] || EMOTIONS.neutral;
    start = ct;
  }
  const k = Math.min(1, (t - start) / fade);
  const e = k * k * (3 - 2 * k);
  return blend(prev, cur, e);
}

// Desk-slam impulse from a list of slam times: quick lift, hard drop, settle.
export function slamAt(times, t) {
  let v = 0;
  for (const s of times) {
    const d = t - s;
    if (d >= 0 && d < 0.6) v = Math.max(v, Math.exp(-d * 9) * Math.cos(d * 30) * 1.0);
  }
  return v;
}

// Fist height for slams: wind up 0.3 s before, smash down at the slam time.
export function fistAt(times, t) {
  let y = 0;
  for (const s of times) {
    const d = t - s;
    if (d > -0.32 && d <= 0) y = Math.min(y, -150 * Math.sin(((d + 0.32) / 0.32) * Math.PI / 2) * (d > -0.06 ? (-d / 0.06) : 1));
  }
  return y;
}
