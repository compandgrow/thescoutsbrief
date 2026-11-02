// "The Inspector": a 3D fox detective (trench coat, fedora) for the Scout Files story series.
// Built in code with Three.js: smooth velvety fur (physical sheen), soft lighting, a noir office.
// Like presenter.js, every frame is a pure function of draw({t, emo, mouth, slam, fistY}), so renders are
// deterministic. emo = the blended face parameters from presenter.js EMOTIONS. Motion is smoothed from the
// whole lip-sync track (opts.mouthTrack), never from frame-to-frame state.
import * as THREE from "/node_modules/three/build/three.module.js";

const W = 1080, H = 1920;
const lerp = (a, b, k) => a + (b - a) * k;
const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
const smooth = (a, b, x) => { const k = clamp((x - a) / (b - a)); return k * k * (3 - 2 * k); };
const hash = (n) => { const s = Math.sin(n * 127.1 + 311.7) * 43758.5453; return s - Math.floor(s); };
const noise = (t, seed = 0) => Math.sin(t * 1.7 + seed) * 0.5 + Math.sin(t * 2.9 + seed * 2.1) * 0.3 + Math.sin(t * 4.3 + seed * 3.7) * 0.2;

const COL = {
  fur: 0xd9692a, cream: 0xf7efe4, nose: 0x1b1515, coat: 0xb89062, coatDark: 0x8d6c45, hat: 0x2b2a30,
  shirt: 0xece6dc, paw: 0x2d221d, desk: 0x3b2618, deskTop: 0x4b301f, folder: 0xd9b66c, wall: 0x221c1a,
  brow: 0x4a2412, eyeWhite: 0xfdfaf4, iris: 0x7a4718, pupil: 0x110c09, mouth: 0x3b0e14, tongue: 0xd8626c,
};

// fur: soft diffuse + sheen so it reads as velvet, not plastic
const furMaterial = (color, extra = {}) => new THREE.MeshPhysicalMaterial({
  color, roughness: 0.82, sheen: 1, sheenRoughness: 0.45, sheenColor: new THREE.Color(0xffd9b8), ...extra });
const cloth = (color, extra = {}) => new THREE.MeshStandardMaterial({ color, roughness: 0.9, metalness: 0, ...extra });

// paint vertices orange/cream by a function of position (one smooth mesh, no seams between colours)
function paint(geo, fn) {
  const p = geo.attributes.position, c = new Float32Array(p.count * 3), v = new THREE.Vector3();
  const A = new THREE.Color(COL.fur), B = new THREE.Color(COL.cream), out = new THREE.Color();
  for (let i = 0; i < p.count; i++) {
    v.fromBufferAttribute(p, i);
    out.copy(A).lerp(B, clamp(fn(v)));
    c.set([out.r, out.g, out.b], i * 3);
  }
  geo.setAttribute("color", new THREE.BufferAttribute(c, 3));
  return geo;
}

function wallTexture() {
  // back wall with soft slats of light from a window blind (painted, so no harsh stripes move over the fox)
  const c = document.createElement("canvas");
  c.width = 512; c.height = 1024;
  const g = c.getContext("2d");
  g.fillStyle = "#231d1b"; g.fillRect(0, 0, 512, 1024);
  g.save(); g.translate(330, 260); g.rotate(-0.32);
  for (let i = 0; i < 9; i++) {
    const grd = g.createLinearGradient(-260, 0, 260, 0);
    grd.addColorStop(0, "rgba(255,214,160,0)"); grd.addColorStop(0.5, `rgba(255,214,160,${0.16 - i * 0.012})`); grd.addColorStop(1, "rgba(255,214,160,0)");
    g.fillStyle = grd; g.fillRect(-260, i * 44, 520, 24);
  }
  g.restore();
  const tex = new THREE.CanvasTexture(c);
  tex.colorSpace = THREE.SRGBColorSpace;
  return tex;
}

function stampTexture(text, color) {
  const c = document.createElement("canvas");
  c.width = 512; c.height = 360;
  const g = c.getContext("2d");
  g.fillStyle = "#d9b66c"; g.fillRect(0, 0, 512, 360);
  g.save(); g.translate(256, 180); g.rotate(-0.18);
  g.strokeStyle = color; g.lineWidth = 10; g.strokeRect(-200, -52, 400, 104);
  g.fillStyle = color; g.font = "bold 70px Anton, Impact, sans-serif"; g.textAlign = "center"; g.textBaseline = "middle";
  g.fillText(text, 0, 4); g.restore();
  const tex = new THREE.CanvasTexture(c);
  tex.colorSpace = THREE.SRGBColorSpace;
  return tex;
}

function lathe(points, segs = 64) {
  return new THREE.LatheGeometry(points.map(([r, y]) => new THREE.Vector2(r, y)), segs);
}

export function createDetective(stage, opts = {}) {
  const TH = opts.theme || {};
  const accent = new THREE.Color(TH.accent || "#e5484d");
  const track = opts.mouthTrack || [], FPS = opts.fps || 30;
  // lip-sync smoothed with a small gaussian (fast enough for syllables, no frame jitter)
  const mouthAt = (t, sigma = 1.3, span = 3) => {
    const f = t * FPS; let s = 0, w = 0;
    for (let k = Math.floor(f) - span; k <= Math.ceil(f) + span; k++) {
      const wk = Math.exp(-((k - f) ** 2) / (2 * sigma * sigma));
      s += (track[Math.min(track.length - 1, Math.max(0, k))] || 0) * wk; w += wk;
    }
    return w ? s / w : 0;
  };
  const speechAt = (t) => mouthAt(t, 7, 18);   // slow speech energy for head and hand motion

  const renderer = new THREE.WebGLRenderer({ antialias: true, preserveDrawingBuffer: true });
  renderer.setPixelRatio(opts.pixelRatio || 1);
  renderer.setSize(W, H, false);
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.15;
  const cv = renderer.domElement;
  Object.assign(cv.style, { position: "absolute", left: 0, top: 0, width: W + "px", height: H + "px" });
  stage.insertBefore(cv, opts.before || null);

  const scene = new THREE.Scene();
  scene.background = new THREE.Color(0x0d0a09);
  const camera = new THREE.PerspectiveCamera(30, W / H, 0.1, 50);

  function mesh(geo, mat, parent, { pos, rot, scale, shadow = true } = {}) {
    const m = new THREE.Mesh(geo, mat);
    if (pos) m.position.set(...pos);
    if (rot) m.rotation.set(...rot);
    if (scale) m.scale.set(...scale);
    m.castShadow = shadow; m.receiveShadow = true;
    parent.add(m);
    return m;
  }

  // ---------- room ----------
  mesh(new THREE.PlaneGeometry(9, 12), new THREE.MeshStandardMaterial({ map: wallTexture(), roughness: 1 }), scene, { pos: [0, 3, -2.2], shadow: false });
  const board = mesh(new THREE.BoxGeometry(2.0, 1.3, 0.05), cloth(0x2c1d15), scene, { pos: [1.65, 2.95, -2.12], shadow: false });
  for (let i = 0; i < 6; i++) {
    mesh(new THREE.PlaneGeometry(0.28, 0.2), cloth(i % 2 ? 0xe9e1cf : 0xd9b66c), board,
      { pos: [(hash(i) - 0.5) * 1.6, (hash(i + 9) - 0.5) * 1.0, 0.03], rot: [0, 0, (hash(i + 3) - 0.5) * 0.4], shadow: false });
  }
  const pins = [0, 3, 1, 4, 2, 5, 0, 4].map((i) => new THREE.Vector3(1.65 + (hash(i) - 0.5) * 1.6, 2.95 + (hash(i + 9) - 0.5) * 1.0, -2.07));
  scene.add(new THREE.Line(new THREE.BufferGeometry().setFromPoints(pins), new THREE.LineBasicMaterial({ color: accent })));

  // ---------- body ----------
  const rig = new THREE.Group(); rig.position.y = -0.1; scene.add(rig);
  const body = new THREE.Group(); rig.add(body);
  const coat = cloth(COL.coat), coatDark = cloth(COL.coatDark);
  const torso = mesh(lathe([[0.001, -0.2], [0.5, -0.2], [0.52, 0.2], [0.55, 0.62], [0.52, 0.86], [0.36, 1.0], [0.17, 1.08], [0.001, 1.1]]), coat, body, { scale: [1.12, 1, 0.72] });
  // shirt + tie in the V of the coat
  const vShape = new THREE.Shape(); vShape.moveTo(-0.17, 1.03); vShape.lineTo(0.17, 1.03); vShape.lineTo(0, 0.48); vShape.closePath();
  mesh(new THREE.ShapeGeometry(vShape), cloth(COL.shirt), body, { pos: [0, 0, 0.39], rot: [-0.18, 0, 0], shadow: false });
  const tieShape = new THREE.Shape(); tieShape.moveTo(-0.035, 0.98); tieShape.lineTo(0.035, 0.98); tieShape.lineTo(0.055, 0.6); tieShape.lineTo(0, 0.52); tieShape.lineTo(-0.055, 0.6); tieShape.closePath();
  mesh(new THREE.ExtrudeGeometry(tieShape, { depth: 0.015, bevelEnabled: true, bevelThickness: 0.006, bevelSize: 0.006, bevelSegments: 3 }), cloth(accent.getHex(), { roughness: 0.6 }), body, { pos: [0, 0, 0.395], rot: [-0.18, 0, 0] });
  // lapels and popped collar as soft bevelled shapes
  for (const s of [-1, 1]) {
    const lap = new THREE.Shape(); lap.moveTo(0, 0); lap.lineTo(s * 0.2, 0.05); lap.lineTo(s * 0.12, 0.55); lap.lineTo(s * 0.02, 0.6); lap.closePath();
    mesh(new THREE.ExtrudeGeometry(lap, { depth: 0.02, bevelEnabled: true, bevelThickness: 0.012, bevelSize: 0.012, bevelSegments: 4 }), coatDark, body, { pos: [s * 0.02, 0.46, 0.37], rot: [-0.2, 0, 0] });
    for (const y of [0.42, 0.24]) mesh(new THREE.SphereGeometry(0.028, 16, 12), cloth(0x2a1a10, { roughness: 0.4 }), body, { pos: [s * 0.2, y, 0.385] });
  }


  // ---------- head ----------
  const neck = new THREE.Group(); neck.position.set(0, 1.12, 0.02); body.add(neck);
  const head = new THREE.Group(); head.position.set(0, 0.4, 0); neck.add(head);
  const headGeo = new THREE.SphereGeometry(0.42, 64, 48);
  {   // cheek tufts: pull the lower sides of the skull out into soft points
    const p = headGeo.attributes.position, v = new THREE.Vector3();
    for (let i = 0; i < p.count; i++) {
      v.fromBufferAttribute(p, i);
      const side = smooth(0.18, 0.4, Math.abs(v.x)) * smooth(0.05, -0.2, v.y) * smooth(-0.3, 0.1, v.z);
      v.x *= 1 + side * 0.32; v.y -= side * 0.08;
      p.setXYZ(i, v.x, v.y, v.z);
    }
    headGeo.computeVertexNormals();
  }
  paint(headGeo, (v) => smooth(-0.02, -0.12, v.y) * smooth(-0.05, 0.15, v.z) + smooth(0.28, 0.4, Math.abs(v.x)) * smooth(0.0, -0.15, v.y));
  const furMat = furMaterial(0xffffff, { vertexColors: true });
  mesh(headGeo, furMat, head, { scale: [1.0, 0.95, 0.95] });
  const snoutGeo = paint(new THREE.SphereGeometry(1, 48, 32), (v) => smooth(0.15, -0.25, v.y));
  const snout = mesh(snoutGeo, furMat, head, { pos: [0, -0.1, 0.45], scale: [0.18, 0.145, 0.38] });
  const chinGeo = paint(new THREE.SphereGeometry(1, 40, 28), () => 1);
  const chin = mesh(chinGeo, furMat, head, { pos: [0, -0.21, 0.42], scale: [0.15, 0.08, 0.24] });
  mesh(new THREE.SphereGeometry(0.065, 24, 18), new THREE.MeshPhysicalMaterial({ color: COL.nose, roughness: 0.25, clearcoat: 1 }), head, { pos: [0, -0.04, 0.825], scale: [1.2, 0.85, 1] });

  // mouth: just under the snout tip, reshaped every frame from open/width/smile
  const mouthMesh = new THREE.Mesh(new THREE.BufferGeometry(), new THREE.MeshBasicMaterial({ color: COL.mouth, side: THREE.DoubleSide }));
  mouthMesh.position.set(0, -0.24, 0.64); mouthMesh.rotation.x = -0.3; head.add(mouthMesh);
  const tongue = new THREE.Mesh(new THREE.CircleGeometry(0.04, 24), new THREE.MeshBasicMaterial({ color: COL.tongue }));
  tongue.position.z = 0.002; mouthMesh.add(tongue);
  function mouthShape(open, width, smile) {
    const w = 0.1 * width, o = 0.008 + open * 0.11, cy = smile * 0.035;
    const sh = new THREE.Shape();
    sh.moveTo(-w, cy);
    sh.bezierCurveTo(-w * 0.45, 0.012, w * 0.45, 0.012, w, cy);
    sh.bezierCurveTo(w * 0.65, cy - o * 1.15, -w * 0.65, cy - o * 1.15, -w, cy);
    return new THREE.ShapeGeometry(sh, 24);
  }

  // eyes: big, glossy, with iris + two highlights; blinks squash the eye smoothly
  const eyes = [], brows = [];
  const eyeWhite = new THREE.MeshPhysicalMaterial({ color: COL.eyeWhite, roughness: 0.2, clearcoat: 1 });
  const irisMat = new THREE.MeshPhysicalMaterial({ color: COL.iris, roughness: 0.3, clearcoat: 1 });
  const pupilMat = new THREE.MeshBasicMaterial({ color: COL.pupil }), glint = new THREE.MeshBasicMaterial({ color: 0xffffff });
  for (const s of [-1, 1]) {
    const eye = new THREE.Group(); eye.position.set(s * 0.155, 0.075, 0.335); eye.rotation.y = s * 0.3; head.add(eye);
    mesh(new THREE.SphereGeometry(0.1, 40, 30), eyeWhite, eye, { scale: [1, 1.12, 0.55], shadow: false });
    const iris = mesh(new THREE.SphereGeometry(0.062, 32, 24), irisMat, eye, { pos: [0, -0.006, 0.033], scale: [1, 1.08, 0.5], shadow: false });
    const pupil = mesh(new THREE.SphereGeometry(0.036, 24, 18), pupilMat, iris, { pos: [0, 0, 0.034], scale: [1, 1, 0.4], shadow: false });
    mesh(new THREE.SphereGeometry(0.014, 12, 10), glint, iris, { pos: [0.022, 0.026, 0.05], shadow: false });
    mesh(new THREE.SphereGeometry(0.007, 10, 8), glint, iris, { pos: [-0.018, -0.02, 0.05], shadow: false });
    eyes.push({ eye, iris, pupil, s });
    const brow = mesh(new THREE.CapsuleGeometry(0.024, 0.12, 8, 16), cloth(COL.brow, { roughness: 0.7 }), head, { pos: [s * 0.16, 0.215, 0.375], rot: [0, 0, Math.PI / 2] });
    brows.push({ brow, s });
  }

  // ears
  const ears = [];
  // one cone per ear: cream inner ear painted on the front face (two overlapping cones flickered)
  const earProfile = [];
  for (let i = 0; i <= 12; i++) { const k = i / 12; earProfile.push([0.15 * Math.pow(1 - k, 0.85) + 0.001, -0.2 + 0.4 * k]); }
  const earGeo = paint(lathe(earProfile, 48), (v) => smooth(0.03, 0.09, v.z) * smooth(0.13, 0.0, v.y) * smooth(-0.2, -0.12, v.y));
  const tipMat = cloth(COL.nose, { roughness: 0.8 });
  const earMat = cloth(0xffffff, { vertexColors: true, roughness: 0.85 });   // plain diffuse: sheen shimmered on thin cones
  for (const s of [-1, 1]) {
    const ear = new THREE.Group(); ear.position.set(s * 0.33, 0.33, -0.04); ear.scale.setScalar(1.1); head.add(ear);
    mesh(earGeo, earMat, ear, { pos: [0, 0.17, 0], scale: [1, 1, 0.55] });
    mesh(new THREE.ConeGeometry(0.062, 0.13, 32), tipMat, ear, { pos: [0, 0.33, 0], scale: [1, 1, 0.55] });
    ears.push({ ear, s });
  }

  // fedora: smooth lathed brim (turned up at the sides) and pinched crown
  const hat = new THREE.Group(); hat.position.set(0, 0.36, -0.02); hat.rotation.set(-0.08, 0, 0.09); head.add(hat);
  const hatMat = cloth(COL.hat, { roughness: 0.75 });
  mesh(lathe([[0.001, 0], [0.3, 0.0], [0.52, 0.012], [0.6, 0.05], [0.61, 0.07], [0.58, 0.035], [0.3, 0.02], [0.001, 0.02]], 72), hatMat, hat, { scale: [1, 1, 0.9] });
  mesh(lathe([[0.001, 0.32], [0.18, 0.33], [0.27, 0.27], [0.3, 0.12], [0.31, 0.0], [0.001, 0.0]], 64), hatMat, hat, { scale: [0.72, 1, 0.72] });
  mesh(new THREE.CylinderGeometry(0.318, 0.322, 0.07, 64, 1, true), cloth(accent.getHex(), { roughness: 0.6 }), hat, { pos: [0, 0.05, 0], scale: [0.73, 1, 0.73] });

  head.traverse((o) => { if (o.isMesh) o.receiveShadow = false; });
  for (const { ear } of ears) ear.traverse((o) => { if (o.isMesh) o.castShadow = false; });

  // steam puffs (furious)
  const steam = [];
  for (let i = 0; i < 8; i++) {
    const m = new THREE.Mesh(new THREE.SphereGeometry(0.06, 16, 12), new THREE.MeshBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0, depthWrite: false }));
    head.add(m); steam.push(m);
  }

  // ---------- arms: forearms resting on the desk ----------
  const arms = [];
  for (const s of [-1, 1]) {
    const shoulder = new THREE.Group(); shoulder.position.set(s * 0.52, 0.82, 0); body.add(shoulder);
    mesh(new THREE.CapsuleGeometry(0.14, 0.4, 10, 24), coat, shoulder, { pos: [0, -0.25, 0] });
    const elbow = new THREE.Group(); elbow.position.set(0, -0.48, 0); shoulder.add(elbow);
    mesh(new THREE.CapsuleGeometry(0.125, 0.36, 10, 24), coat, elbow, { pos: [0, -0.2, 0] });
    mesh(new THREE.TorusGeometry(0.12, 0.03, 12, 32), coatDark, elbow, { pos: [0, -0.38, 0], rot: [Math.PI / 2, 0, 0] });
    mesh(new THREE.SphereGeometry(0.12, 32, 24), furMaterial(COL.paw), elbow, { pos: [0, -0.47, 0.02], scale: [1, 0.8, 1.15] });
    arms.push({ shoulder, elbow, s });
  }

  // ---------- desk and props ----------
  const desk = new THREE.Group(); desk.position.set(0, 0.12, 0.75); scene.add(desk);
  mesh(new THREE.BoxGeometry(3.6, 0.12, 1.3), cloth(COL.deskTop, { roughness: 0.55 }), desk, { pos: [0, 0.18, 0] });
  mesh(new THREE.BoxGeometry(3.5, 1.0, 0.1), cloth(COL.desk), desk, { pos: [0, -0.37, 0.58], shadow: false });
  const files = new THREE.Group(); files.position.set(0.98, 0.26, 0.05); files.rotation.y = -0.25; desk.add(files);
  for (let i = 0; i < 3; i++) mesh(new THREE.BoxGeometry(0.62, 0.025, 0.44), cloth(COL.folder), files, { pos: [0, i * 0.03, 0], rot: [0, (hash(i) - 0.5) * 0.25, 0] });
  mesh(new THREE.PlaneGeometry(0.6, 0.42), new THREE.MeshStandardMaterial({ map: stampTexture("CLASSIFIED", "#b3261e"), roughness: 0.9 }), files, { pos: [0, 0.09, 0], rot: [-Math.PI / 2, 0, 0], shadow: false });
  const lamp = new THREE.Group(); lamp.position.set(-1.15, 0.24, -0.1); desk.add(lamp);
  const brass = new THREE.MeshStandardMaterial({ color: 0xa47c32, roughness: 0.35, metalness: 0.8 });
  mesh(new THREE.CylinderGeometry(0.16, 0.2, 0.05, 48), brass, lamp);
  mesh(new THREE.CylinderGeometry(0.025, 0.025, 0.55, 16), brass, lamp, { pos: [0, 0.28, 0] });
  mesh(new THREE.CylinderGeometry(0.08, 0.3, 0.2, 48, 1, true), new THREE.MeshPhysicalMaterial({ color: 0x1f6b45, roughness: 0.3, clearcoat: 1, side: THREE.DoubleSide }), lamp, { pos: [0.08, 0.6, 0.05], rot: [0, 0, -0.15] });
  const bulb = new THREE.Mesh(new THREE.SphereGeometry(0.06, 16, 12), new THREE.MeshBasicMaterial({ color: 0xffe6b5 }));
  bulb.position.set(0.08, 0.5, 0.05); lamp.add(bulb);
  const mag = new THREE.Group(); mag.position.set(0.45, 0.27, 0.35); mag.rotation.set(-Math.PI / 2, 0, 0.7); desk.add(mag);
  mesh(new THREE.TorusGeometry(0.12, 0.018, 16, 48), brass, mag);
  mesh(new THREE.CylinderGeometry(0.02, 0.025, 0.24, 16), cloth(0x5a3a22), mag, { pos: [0, -0.24, 0] });

  // ---------- lights: soft key, warm lamp, accent rim (no light patterns on the face) ----------
  scene.add(new THREE.HemisphereLight(0xffe7cc, 0x1a0f0c, 0.55));
  const key = new THREE.DirectionalLight(0xffe2bd, 2.4);
  key.position.set(-2.5, 4.5, 4); key.target.position.set(0, 1.4, 0);
  key.castShadow = true; key.shadow.mapSize.set(2048, 2048); key.shadow.radius = 6; key.shadow.bias = -0.0002; key.shadow.normalBias = 0.025;
  Object.assign(key.shadow.camera, { left: -2.5, right: 2.5, top: 3, bottom: -1, near: 0.5, far: 12 });
  scene.add(key, key.target);
  const rim = new THREE.DirectionalLight(accent, 3.2); rim.position.set(2.2, 3.2, -3); scene.add(rim);
  const rim2 = new THREE.DirectionalLight(0x7aa0ff, 1.2); rim2.position.set(-2.4, 2.6, -2.5); scene.add(rim2);
  const lampLight = new THREE.PointLight(0xffc77a, 5, 3.5, 1.5); lampLight.position.set(-1.07, 0.75, 0.8); scene.add(lampLight);
  const rage = new THREE.PointLight(0xff2a1a, 0, 6, 1.4); rage.position.set(0, 2.2, 1.6); scene.add(rage);

  const baseTint = new THREE.Color(0xffffff), rageTint = new THREE.Color(0xff8a7a);

  function draw({ t, emo, mouth = 0, slam = 0, fistY = 0 }) {
    const e = emo;
    const m = track.length ? mouthAt(t) : mouth;
    const sp = track.length ? speechAt(t) : mouth;

    // camera: slow push-in, gentle drift; a single soft bump on a desk slam
    const push = smooth(0, 40, t);
    camera.position.set(noise(t * 0.25, 1) * 0.05, 1.76 + noise(t * 0.2, 2) * 0.015 - Math.max(0, slam) * 0.025, lerp(9.2, 8.6, push));
    camera.lookAt(0, 1.92 - push * 0.04, 0);

    // body: breathing, soft bounce for happy/excited/laughing, lean in when angry
    const breathe = Math.sin(t * 1.9) * 0.01;
    const bounce = (Math.sin(t * 6.5) * 0.5 + 0.5) * e.bounce * 0.025 + (e.laugh || 0) * (Math.sin(t * 11) * 0.5 + 0.5) * 0.02;
    body.position.y = bounce;
    torso.scale.y = 1 + breathe;
    body.rotation.x = -e.red * 0.07 + (e.round || 0) * 0.03;
    const tremble = e.shake > 2 ? (e.shake - 2) / 7 : 0;            // only real rage shakes, and smoothly
    body.position.x = noise(t * 9, 3) * tremble * 0.012;

    // head: speech-driven nods and turns (from the smoothed speech energy), tilt, laugh tilt-back
    head.rotation.x = -sp * 0.08 + noise(t * 0.6, 4) * 0.035 - (e.laugh || 0) * 0.16 + e.red * 0.05;
    head.rotation.y = noise(t * 0.45, 5) * 0.09 + sp * noise(t * 1.6, 6) * 0.05;
    head.rotation.z = (e.tilt * Math.PI) / 180 + noise(t * 0.5, 7) * 0.025;
    head.position.x = noise(t * 11, 8) * tremble * 0.006;

    // tint warms toward red with rage
    furMat.color.copy(baseTint).lerp(rageTint, e.red * 0.55);
    rage.intensity = e.red * 9;

    // eyes: smooth blink every ~3.6 s (with a double blink sometimes), openness, pupils, slow gaze
    const cycle = 3.6, ph = t % cycle, idx = Math.floor(t / cycle);
    let blink = Math.exp(-((ph - 3.4) ** 2) / 0.0035);
    if (hash(idx) > 0.7) blink = Math.max(blink, Math.exp(-((ph - 3.12) ** 2) / 0.0035));
    for (const { eye, pupil, iris } of eyes) {
      const open = clamp(e.eye, 0.25, 1.35) * (1 - blink * 0.92);
      eye.scale.set(1, Math.max(0.06, open), 1);
      pupil.scale.setScalar(e.pupil);
      iris.position.x = noise(t * 0.35, 9) * 0.012;
      iris.position.y = -0.006 + noise(t * 0.3, 10) * 0.006;
    }
    for (const { brow, s } of brows) {
      brow.rotation.z = Math.PI / 2 + s * (e.brow * Math.PI / 180) * 0.85 + (e.asym || 0) * (s > 0 ? 0.22 : 0);
      brow.position.y = 0.215 + e.lift * 0.0028 - blink * 0.01;
    }
    for (const { ear, s } of ears) {
      ear.rotation.x = -e.red * 0.7 + (e.round || 0) * 0.12;
      ear.rotation.z = s * (-0.42 + e.red * 0.45 - (e.lift > 10 ? 0.1 : 0)) + noise(t * 0.8, 11 + s) * 0.04;
    }

    // mouth + jaw: smoothed lip-sync plus emotion shape
    const open = clamp(m * 0.9 + (e.round || 0) * 0.42 + (e.laugh || 0) * 0.3 * (0.6 + 0.4 * Math.sin(t * 16)), 0, 1.1);
    mouthMesh.geometry.dispose();
    mouthMesh.geometry = mouthShape(open, lerp(e.width, 0.6, (e.round || 0) * 0.6), e.smile);
    tongue.visible = open > 0.3;
    tongue.position.y = -0.03 - open * 0.05;
    chin.position.y = -0.21 - open * 0.035;

    // arms: forearms on the desk; small speech-driven hand moves; right fist winds up and slams
    const raise = clamp(-fistY / 150);
    for (const { shoulder, elbow, s } of arms) {
      const gest = sp * noise(t * 1.3, 12 + s) * 0.18;
      shoulder.rotation.set(-0.55 + gest, 0, s * 0.12);
      elbow.rotation.set(-1.15 - gest * 0.6, 0, s * -0.12);
      if (s > 0) {
        shoulder.rotation.x = lerp(shoulder.rotation.x, -2.1, raise);
        elbow.rotation.x = lerp(elbow.rotation.x, -1.0, raise);
      }
    }
    files.position.y = 0.26 + Math.max(0, slam) * 0.06;
    mag.position.y = 0.27 + Math.max(0, slam) * 0.08;

    steam.forEach((p, i) => {
      const k = (t * 0.8 + i / steam.length) % 1, s = i % 2 ? 1 : -1;
      p.position.set(s * (0.34 + k * 0.12), 0.45 + k * 0.5, -0.05);
      p.scale.setScalar(0.6 + k * 1.5);
      p.material.opacity = e.steam * (1 - k) * 0.7;
    });

    renderer.render(scene, camera);
  }

  return { draw, canvas: cv };
}
