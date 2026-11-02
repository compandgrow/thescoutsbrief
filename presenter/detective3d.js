// "The Inspector": a 3D fox detective (trench coat, fedora) for the Scout Files story series.
// Built from primitives in Three.js with toon shading and outlines. Like presenter.js, every frame is a pure
// function of draw({t, emo, mouth, slam, fistY}), so renders are deterministic. emo = the blended face
// parameters from presenter.js EMOTIONS (brow, lift, eye, pupil, smile, width, round, red, shake, tilt, bounce...).
import * as THREE from "/node_modules/three/build/three.module.js";

const W = 1080, H = 1920;
const lerp = (a, b, k) => a + (b - a) * k;
const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
const hash = (n) => { const s = Math.sin(n * 127.1 + 311.7) * 43758.5453; return s - Math.floor(s); };

const COL = {
  fur: 0xe2742c, furDark: 0xb4531a, cream: 0xf6efe2, nose: 0x1a1414, coat: 0xb58f5a, coatDark: 0x8a6a3e,
  hat: 0x2a2a31, shirt: 0xe9e4da, paw: 0x2b201b, desk: 0x3a2417, deskTop: 0x4a2f1e, folder: 0xd8b56a,
  wall: 0x1b1716, brow: 0x5a2c12, eyeWhite: 0xfbf8f2, pupil: 0x15100c, mouth: 0x3a0d12, tongue: 0xd8606a,
};

function toonGradient() {
  const data = new Uint8Array([70, 70, 70, 255, 150, 150, 150, 255, 235, 235, 235, 255]);
  const tex = new THREE.DataTexture(data, 3, 1, THREE.RGBAFormat);
  tex.minFilter = tex.magFilter = THREE.NearestFilter;
  tex.needsUpdate = true;
  return tex;
}

function blindsTexture() {
  // light cookie for the key light: horizontal slats of light, like a window with venetian blinds
  const c = document.createElement("canvas");
  c.width = c.height = 512;
  const g = c.getContext("2d");
  g.fillStyle = "#000"; g.fillRect(0, 0, 512, 512);
  const grd = g.createRadialGradient(256, 256, 40, 256, 256, 256);
  grd.addColorStop(0, "#fff"); grd.addColorStop(1, "#000");
  for (let y = 0; y < 512; y += 46) { g.fillStyle = grd; g.fillRect(0, y, 512, 28); }
  const tex = new THREE.CanvasTexture(c);
  tex.colorSpace = THREE.SRGBColorSpace;
  return tex;
}

function stampTexture(text, color) {
  const c = document.createElement("canvas");
  c.width = 512; c.height = 256;
  const g = c.getContext("2d");
  g.fillStyle = "#d8b56a"; g.fillRect(0, 0, 512, 256);
  g.save(); g.translate(256, 128); g.rotate(-0.18);
  g.strokeStyle = color; g.lineWidth = 10; g.strokeRect(-200, -52, 400, 104);
  g.fillStyle = color; g.font = "bold 70px Anton, Impact, sans-serif"; g.textAlign = "center"; g.textBaseline = "middle";
  g.fillText(text, 0, 4); g.restore();
  const tex = new THREE.CanvasTexture(c);
  tex.colorSpace = THREE.SRGBColorSpace;
  return tex;
}

export function createDetective(stage, opts = {}) {
  const TH = opts.theme || {};
  const accent = new THREE.Color(TH.accent || "#e5484d");

  const renderer = new THREE.WebGLRenderer({ antialias: true, preserveDrawingBuffer: true, alpha: false });
  renderer.setPixelRatio(1);
  renderer.setSize(W, H, false);
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  const cv = renderer.domElement;
  Object.assign(cv.style, { position: "absolute", left: 0, top: 0, width: W + "px", height: H + "px" });
  stage.insertBefore(cv, opts.before || null);

  const scene = new THREE.Scene();
  scene.background = new THREE.Color(0x0c0909);
  scene.fog = new THREE.Fog(0x0c0909, 9, 18);
  const camera = new THREE.PerspectiveCamera(30, W / H, 0.1, 50);

  const grad = toonGradient();
  const toon = (color, extra = {}) => new THREE.MeshToonMaterial({ color, gradientMap: grad, ...extra });
  const outlineMat = new THREE.MeshBasicMaterial({ color: 0x0a0605, side: THREE.BackSide });
  const outlined = [];
  function part(geo, mat, parent, { pos, rot, scale, outline = 0.025, shadow = true } = {}) {
    const m = new THREE.Mesh(geo, mat);
    if (pos) m.position.set(...pos);
    if (rot) m.rotation.set(...rot);
    if (scale) m.scale.set(...scale);
    m.castShadow = shadow; m.receiveShadow = true;
    parent.add(m);
    if (outline) {
      const o = new THREE.Mesh(geo, outlineMat);
      o.scale.setScalar(1 + outline);
      m.add(o);
      outlined.push(o);
    }
    return m;
  }

  // ---------- room ----------
  const wall = new THREE.Mesh(new THREE.PlaneGeometry(14, 12), toon(COL.wall));
  wall.position.set(0, 3, -2.2); wall.receiveShadow = true; scene.add(wall);
  const floor = new THREE.Mesh(new THREE.PlaneGeometry(14, 10), toon(0x120d0b));
  floor.rotation.x = -Math.PI / 2; floor.position.y = -0.4; floor.receiveShadow = true; scene.add(floor);
  // a framed "evidence board" on the back wall: red strings between pinned notes
  const board = part(new THREE.BoxGeometry(2.2, 1.4, 0.05), toon(0x2a1c14), scene, { pos: [1.55, 2.75, -2.12], outline: 0 });
  for (let i = 0; i < 6; i++) {
    const nx = (hash(i) - 0.5) * 1.8, ny = (hash(i + 9) - 0.5) * 1.1;
    part(new THREE.PlaneGeometry(0.28, 0.2), toon(i % 2 ? 0xe9e1cf : 0xd8b56a), board, { pos: [nx, ny, 0.03], rot: [0, 0, (hash(i + 3) - 0.5) * 0.4], outline: 0, shadow: false });
  }
  const strings = new THREE.BufferGeometry().setFromPoints([0, 3, 1, 4, 2, 5, 0, 4].map((i) => new THREE.Vector3(1.55 + (hash(i) - 0.5) * 1.8, 2.75 + (hash(i + 9) - 0.5) * 1.1, -2.07)));
  scene.add(new THREE.Line(strings, new THREE.LineBasicMaterial({ color: accent })));

  // ---------- body ----------
  const rig = new THREE.Group(); rig.position.y = -0.1; scene.add(rig);
  const body = new THREE.Group(); rig.add(body);
  const coat = toon(COL.coat), coatDark = toon(COL.coatDark), fur = toon(COL.fur), cream = toon(COL.cream);
  const torso = part(new THREE.CapsuleGeometry(0.5, 0.55, 8, 24), coat, body, { pos: [0, 0.55, 0], scale: [1.18, 1, 0.78] });
  // shirt V, tie, lapels, popped collar, buttons
  part(new THREE.ConeGeometry(0.2, 0.55, 3), toon(COL.shirt), body, { pos: [0, 0.95, 0.36], rot: [Math.PI + 0.25, 0, 0], scale: [1, 1, 0.3], outline: 0 });
  const tie = part(new THREE.BoxGeometry(0.08, 0.42, 0.03), toon(accent.getHex()), body, { pos: [0, 0.9, 0.43], rot: [-0.25, 0, 0], outline: 0.06 });
  for (const s of [-1, 1]) {
    part(new THREE.BoxGeometry(0.2, 0.62, 0.05), coatDark, body, { pos: [s * 0.2, 0.86, 0.38], rot: [-0.28, 0, s * 0.42] });
    part(new THREE.BoxGeometry(0.26, 0.3, 0.05), coat, body, { pos: [s * 0.3, 1.2, 0.12], rot: [-0.15, s * 0.5, s * -0.35] });   // popped collar
    for (const y of [0.55, 0.32]) part(new THREE.SphereGeometry(0.03, 12, 8), toon(0x2a1a10), body, { pos: [s * 0.17, y, 0.42], outline: 0 });
  }

  // ---------- head ----------
  const neck = new THREE.Group(); neck.position.set(0, 1.22, 0.02); body.add(neck);
  const head = new THREE.Group(); head.position.set(0, 0.36, 0); neck.add(head);
  const skullMat = toon(COL.fur);
  part(new THREE.SphereGeometry(0.42, 32, 24), skullMat, head, { scale: [1.05, 0.95, 0.95] });
  for (const s of [-1, 1]) {   // cheek fluff
    part(new THREE.ConeGeometry(0.1, 0.24, 16), cream, head, { pos: [s * 0.37, -0.17, 0.1], rot: [0.2, 0, s * 2.2], scale: [1, 1, 0.6] });
  }
  part(new THREE.SphereGeometry(0.3, 28, 20), cream, head, { pos: [0, -0.15, 0.26], scale: [1.05, 0.72, 1.0] });   // lower face
  const snout = part(new THREE.SphereGeometry(0.2, 28, 20), cream, head, { pos: [0, -0.1, 0.48], scale: [0.9, 0.7, 1.25] });
  part(new THREE.SphereGeometry(0.17, 24, 16), skullMat, head, { pos: [0, 0.0, 0.44], scale: [0.85, 0.55, 1.2], outline: 0.02 });   // orange bridge
  part(new THREE.SphereGeometry(0.06, 16, 12), toon(COL.nose), head, { pos: [0, -0.02, 0.7], scale: [1.2, 0.85, 1] });

  // mouth: a flat shape just in front of the snout, rebuilt each frame from open/width/smile
  const mouthMat = new THREE.MeshBasicMaterial({ color: COL.mouth, side: THREE.DoubleSide });
  const mouthMesh = new THREE.Mesh(new THREE.BufferGeometry(), mouthMat);
  mouthMesh.position.set(0, -0.15, 0.665); mouthMesh.rotation.x = -0.35; head.add(mouthMesh);
  const tongue = new THREE.Mesh(new THREE.CircleGeometry(0.035, 20), new THREE.MeshBasicMaterial({ color: COL.tongue }));
  tongue.position.set(0, -0.012, 0.002); mouthMesh.add(tongue);
  function mouthShape(open, width, smile) {
    const w = 0.095 * width, o = 0.005 + open * 0.1, cy = smile * 0.032;
    const sh = new THREE.Shape();
    sh.moveTo(-w, cy);
    sh.bezierCurveTo(-w * 0.5, cy * 0.15 + o * 0.12, w * 0.5, cy * 0.15 + o * 0.12, w, cy);          // upper lip
    sh.bezierCurveTo(w * 0.6, cy - o * 1.1 - 0.004, -w * 0.6, cy - o * 1.1 - 0.004, -w, cy);          // lower lip
    return new THREE.ShapeGeometry(sh, 16);
  }

  // eyes, lids, brows
  const eyes = [], brows = [];
  for (const s of [-1, 1]) {
    const eye = new THREE.Group(); eye.position.set(s * 0.155, 0.08, 0.33); eye.rotation.y = s * 0.28; head.add(eye);
    part(new THREE.SphereGeometry(0.09, 24, 18), toon(COL.eyeWhite), eye, { scale: [1, 1.12, 0.55], outline: 0.06 });
    const pupil = part(new THREE.SphereGeometry(0.048, 18, 14), new THREE.MeshBasicMaterial({ color: COL.pupil }), eye, { pos: [0, -0.005, 0.042], scale: [1, 1.1, 0.5], outline: 0 });
    part(new THREE.SphereGeometry(0.014, 10, 8), new THREE.MeshBasicMaterial({ color: 0xffffff }), pupil, { pos: [0.018, 0.022, 0.03], outline: 0, shadow: false });
    const lid = part(new THREE.SphereGeometry(0.098, 24, 12, 0, Math.PI * 2, 0, Math.PI / 2), skullMat, eye, { scale: [1, 1.15, 0.62], outline: 0 });
    eyes.push({ eye, pupil, lid, s });
    const brow = part(new THREE.CapsuleGeometry(0.022, 0.13, 4, 10), toon(COL.brow), head, { pos: [s * 0.16, 0.21, 0.37], rot: [0, 0, Math.PI / 2], outline: 0.08 });
    brows.push({ brow, s });
  }

  // ears (poke out from under the hat brim)
  const ears = [];
  for (const s of [-1, 1]) {
    const ear = new THREE.Group(); ear.position.set(s * 0.27, 0.3, -0.05); head.add(ear);
    part(new THREE.ConeGeometry(0.14, 0.38, 20), fur, ear, { pos: [0, 0.17, 0], scale: [1, 1, 0.55] });
    part(new THREE.ConeGeometry(0.085, 0.24, 16), cream, ear, { pos: [0, 0.14, 0.045], scale: [1, 1, 0.4], outline: 0 });
    part(new THREE.ConeGeometry(0.06, 0.12, 16), toon(COL.nose), ear, { pos: [0, 0.32, 0], scale: [1, 1, 0.55], outline: 0 });
    ears.push({ ear, s });
  }

  // fedora
  const hat = new THREE.Group(); hat.position.set(0, 0.36, -0.02); hat.rotation.set(-0.08, 0, 0.1); head.add(hat);
  const hatMat = toon(COL.hat);
  part(new THREE.CylinderGeometry(0.56, 0.6, 0.035, 40), hatMat, hat, { scale: [1, 1, 0.92] });
  part(new THREE.CylinderGeometry(0.27, 0.32, 0.3, 32), hatMat, hat, { pos: [0, 0.16, 0], scale: [1.05, 1, 0.9] });
  part(new THREE.CylinderGeometry(0.325, 0.33, 0.07, 32), toon(accent.getHex()), hat, { pos: [0, 0.045, 0], scale: [1.05, 1, 0.9], outline: 0 });
  part(new THREE.BoxGeometry(0.42, 0.05, 0.08), hatMat, hat, { pos: [0, 0.31, 0], outline: 0 });   // crown dent ridge

  // steam puffs (furious)
  const steam = [];
  for (let i = 0; i < 8; i++) {
    const m = new THREE.Mesh(new THREE.SphereGeometry(0.06, 12, 10), new THREE.MeshBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0 }));
    head.add(m); steam.push(m);
  }

  // ---------- arms ----------
  const arms = [];
  for (const s of [-1, 1]) {
    const shoulder = new THREE.Group(); shoulder.position.set(s * 0.56, 1.0, 0); body.add(shoulder);
    const upper = part(new THREE.CapsuleGeometry(0.13, 0.42, 6, 14), coat, shoulder, { pos: [0, -0.26, 0] });
    const elbow = new THREE.Group(); elbow.position.set(0, -0.5, 0); shoulder.add(elbow);
    part(new THREE.CapsuleGeometry(0.115, 0.38, 6, 14), coat, elbow, { pos: [0, -0.22, 0] });
    part(new THREE.CylinderGeometry(0.125, 0.125, 0.07, 16), coatDark, elbow, { pos: [0, -0.42, 0], outline: 0 });   // cuff
    const paw = part(new THREE.SphereGeometry(0.11, 18, 14), toon(COL.paw), elbow, { pos: [0, -0.5, 0.02], scale: [1, 0.85, 1.1] });
    arms.push({ shoulder, elbow, paw, s, upper });
  }

  // ---------- desk and props ----------
  const desk = new THREE.Group(); desk.position.set(0, 0.12, 0.75); scene.add(desk);
  part(new THREE.BoxGeometry(3.6, 0.12, 1.3), toon(COL.deskTop), desk, { pos: [0, 0.18, 0] });
  part(new THREE.BoxGeometry(3.5, 1.0, 0.1), toon(COL.desk), desk, { pos: [0, -0.37, 0.58], outline: 0 });
  // case files with a stamp
  const files = new THREE.Group(); files.position.set(0.95, 0.26, 0.05); files.rotation.y = -0.25; desk.add(files);
  for (let i = 0; i < 3; i++) part(new THREE.BoxGeometry(0.62, 0.025, 0.44), toon(COL.folder), files, { pos: [0, i * 0.03, 0], rot: [0, (hash(i) - 0.5) * 0.25, 0], outline: 0.01 });
  const top = new THREE.Mesh(new THREE.PlaneGeometry(0.6, 0.42), new THREE.MeshToonMaterial({ map: stampTexture("CLASSIFIED", "#b3261e"), gradientMap: grad }));
  top.rotation.x = -Math.PI / 2; top.position.y = 0.09; files.add(top);
  // banker's lamp (green shade) — also the warm key light source
  const lamp = new THREE.Group(); lamp.position.set(-1.15, 0.24, -0.1); desk.add(lamp);
  part(new THREE.CylinderGeometry(0.16, 0.2, 0.05, 24), toon(0x8a6a2a), lamp);
  part(new THREE.CylinderGeometry(0.025, 0.025, 0.55, 10), toon(0x8a6a2a), lamp, { pos: [0, 0.28, 0], outline: 0 });
  part(new THREE.CylinderGeometry(0.08, 0.3, 0.2, 24, 1, true), toon(0x1f6b45, { side: THREE.DoubleSide }), lamp, { pos: [0.08, 0.6, 0.05], rot: [0, 0, -0.15] });
  const bulb = new THREE.Mesh(new THREE.SphereGeometry(0.06, 12, 10), new THREE.MeshBasicMaterial({ color: 0xffe2a8 }));
  bulb.position.set(0.08, 0.5, 0.05); lamp.add(bulb);
  // magnifying glass
  const mag = new THREE.Group(); mag.position.set(0.45, 0.27, 0.35); mag.rotation.set(-Math.PI / 2, 0, 0.7); desk.add(mag);
  part(new THREE.TorusGeometry(0.12, 0.018, 10, 30), toon(0x2b2b2b), mag);
  part(new THREE.CylinderGeometry(0.02, 0.025, 0.24, 10), toon(0x5a3a22), mag, { pos: [0, -0.24, 0], outline: 0 });

  // ---------- lights ----------
  scene.add(new THREE.AmbientLight(0x6a5a70, 0.55));
  const key = new THREE.SpotLight(0xffe0b0, 90, 14, 0.5, 0.6, 1.6);
  key.position.set(-3.2, 4.6, 3.4); key.target.position.set(0.2, 1.4, -0.5);
  key.map = blindsTexture();
  key.castShadow = true; key.shadow.mapSize.set(1024, 1024); key.shadow.bias = -0.0008;
  scene.add(key, key.target);
  const rim = new THREE.DirectionalLight(accent, 2.2); rim.position.set(2.5, 3, -3); scene.add(rim);
  const lampLight = new THREE.PointLight(0xffc77a, 6, 3.5, 1.6); lampLight.position.set(-1.07, 0.7, 0.8); scene.add(lampLight);
  const rage = new THREE.PointLight(0xff2a1a, 0, 6, 1.4); rage.position.set(0, 2.2, 1.6); scene.add(rage);

  const baseFur = new THREE.Color(COL.fur), rageFur = new THREE.Color(0xd8361c);

  function draw({ t, emo, mouth = 0, slam = 0, fistY = 0 }) {
    const e = emo;
    // camera: slow push-in plus a little handheld drift; the fox sits in the lower half of the frame
    const push = clamp(t / 40);
    camera.position.set(Math.sin(t * 0.35) * 0.06, 1.75 + Math.sin(t * 0.5) * 0.02, lerp(9.4, 8.7, push));
    camera.lookAt(0, 1.92 - push * 0.04, 0);
    camera.position.y += slam * 0.04 * Math.sin(t * 70);

    // body: breathing, bounce (happy/excited/laughing), lean
    const breathe = Math.sin(t * 2.1) * 0.012;
    const bounce = Math.abs(Math.sin(t * 7.5)) * e.bounce * 0.035 + (e.laugh || 0) * Math.abs(Math.sin(t * 14)) * 0.025;
    body.position.y = bounce;
    torso.scale.y = 1 + breathe;
    body.rotation.x = -e.red * 0.08 + (e.round || 0) * 0.04;          // leans in when angry
    body.position.x = Math.sin(t * 61) * e.shake * 0.0025;

    // head: talking nods, tilt, shake, laugh tilt-back
    head.rotation.x = -mouth * 0.07 + Math.sin(t * 1.3) * 0.02 - (e.laugh || 0) * 0.18 + e.red * 0.06;
    head.rotation.z = (e.tilt * Math.PI) / 180 + Math.sin(t * 0.9) * 0.02;
    head.rotation.y = Math.sin(t * 0.6) * 0.06;
    head.position.x = Math.sin(t * 73) * e.shake * 0.004;

    // fur turns red with rage
    skullMat.color.copy(baseFur).lerp(rageFur, e.red * 0.6);
    rage.intensity = e.red * 10;

    // eyes: open amount x blink, pupil size; lids drop as eye openness falls
    const bt = t % 3.7, blinkK = bt > 3.55 ? Math.sin(((bt - 3.55) / 0.15) * Math.PI) : 0;
    for (const { eye, pupil, lid, s } of eyes) {
      const open = clamp(e.eye * (1 - blinkK), 0.05, 1.4);
      eye.scale.set(1, lerp(0.55, 1, clamp(open)) * (open > 1 ? open * 0.9 : 1), 1);
      lid.rotation.x = lerp(-0.2, -1.65, clamp(open));                 // lid rolls up out of view when open
      pupil.scale.setScalar(e.pupil);
      pupil.position.x = Math.sin(t * 0.4) * 0.01;
    }
    for (const { brow, s } of brows) {
      brow.rotation.z = Math.PI / 2 + s * (e.brow * Math.PI / 180) * 0.9 + (e.asym || 0) * (s > 0 ? 0.25 : 0);
      brow.position.y = 0.21 + e.lift * 0.0028;
    }
    // ears: back when angry, up when shocked/excited
    for (const { ear, s } of ears) {
      ear.rotation.x = -e.red * 0.75 + (e.round || 0) * 0.15;
      ear.rotation.z = s * (-0.35 + e.red * 0.5 - (e.lift > 10 ? 0.12 : 0)) + Math.sin(t * 3 + s) * 0.03;
    }

    // mouth: lip-sync amplitude + emotion shape (O when shocked)
    const open = clamp(mouth * 0.95 + (e.round || 0) * 0.45 + (e.laugh || 0) * 0.35 * (0.6 + 0.4 * Math.sin(t * 18)), 0, 1.1);
    mouthMesh.geometry.dispose();
    mouthMesh.geometry = mouthShape(open, lerp(e.width, 0.6, (e.round || 0) * 0.6), e.smile);
    tongue.visible = open > 0.35;
    tongue.position.y = -0.03 - open * 0.04;

    // arms: forearms resting on the desk, gesture with speech, right fist winds up and slams
    const raise = clamp(-fistY / 150);
    for (const { shoulder, elbow, s } of arms) {
      const talk = Math.sin(t * 2.4 + s) * 0.08 * clamp(mouth * 2);
      shoulder.rotation.set(-0.95 + talk, 0, s * 0.18);
      elbow.rotation.set(-0.85 - talk * 0.5, 0, s * -0.1);
      if (s > 0) {
        shoulder.rotation.x = lerp(shoulder.rotation.x, -2.3, raise);
        elbow.rotation.x = lerp(elbow.rotation.x, -1.3, raise);
      }
    }
    // props jump on a slam
    files.position.y = 0.26 + Math.max(0, slam) * 0.08;
    mag.position.y = 0.27 + Math.max(0, slam) * 0.1;

    // steam from the ears when furious
    steam.forEach((m, i) => {
      const ph = (t * 0.9 + i / steam.length) % 1;
      const s = i % 2 ? 1 : -1;
      m.position.set(s * (0.34 + ph * 0.12), 0.45 + ph * 0.5, -0.05);
      m.scale.setScalar(0.6 + ph * 1.4);
      m.material.opacity = e.steam * (1 - ph) * 0.8;
    });

    renderer.render(scene, camera);
  }

  return { draw, canvas: cv };
}
