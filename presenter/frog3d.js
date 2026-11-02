// "Inspector Croak": a 3D frog detective (fedora, trench coat) for the Scout Files story series.
// Glossy amphibian skin, bulging eyes with real eyelids, a hinged jaw that opens to talk, a throat sac that
// puffs when angry or laughing. Every frame is a pure function of draw({t, emo, mouth, slam, fistY}); the
// lip-sync is smoothed from the whole track (opts.mouthTrack), so motion is deterministic and smooth.
import * as THREE from "/node_modules/three/build/three.module.js";

const W = 1080, H = 1920;
const lerp = (a, b, k) => a + (b - a) * k;
const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
const smooth = (a, b, x) => { const k = clamp((x - a) / (b - a)); return k * k * (3 - 2 * k); };
const hash = (n) => { const s = Math.sin(n * 127.1 + 311.7) * 43758.5453; return s - Math.floor(s); };
const noise = (t, seed = 0) => Math.sin(t * 1.7 + seed) * 0.5 + Math.sin(t * 2.9 + seed * 2.1) * 0.3 + Math.sin(t * 4.3 + seed * 3.7) * 0.2;

const SKIN = new THREE.Color(0x4fae3a), SKIN_DARK = new THREE.Color(0x2f7d2a), BELLY = new THREE.Color(0xe8efb0), SPOT = new THREE.Color(0x2c6a25);
const COL = {
  coat: 0xb89062, coatDark: 0x8d6c45, hat: 0x6a5039, shirt: 0xece6dc, desk: 0x3b2618, deskTop: 0x4b301f,
  folder: 0xd9b66c, iris: 0xe0a326, pupil: 0x0d0a08, mouth: 0x4a0f18, tongue: 0xd8607a, blush: 0xff7a8a,
};

function skinPaint(geo, belly) {
  // top: green with darker crown and soft spots; front/underside: pale belly colour
  const p = geo.attributes.position, c = new Float32Array(p.count * 3), v = new THREE.Vector3(), out = new THREE.Color();
  for (let i = 0; i < p.count; i++) {
    v.fromBufferAttribute(p, i);
    out.copy(SKIN).lerp(SKIN_DARK, smooth(0.15, 0.5, v.y) * 0.6);
    const sp = Math.sin(v.x * 23 + 1.3) * Math.sin(v.z * 19 + 0.7) * Math.sin(v.y * 17 + 2.1);
    out.lerp(SPOT, smooth(0.75, 0.95, sp) * smooth(0.1, 0.3, v.y) * 0.25);
    out.lerp(BELLY, clamp(belly(v)));
    c.set([out.r, out.g, out.b], i * 3);
  }
  geo.setAttribute("color", new THREE.BufferAttribute(c, 3));
  return geo;
}

function wallTexture() {
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

const lathe = (points, segs = 64) => new THREE.LatheGeometry(points.map(([r, y]) => new THREE.Vector2(r, y)), segs);

export function createFrog(stage, opts = {}) {
  const TH = opts.theme || {};
  const accent = new THREE.Color(TH.accent || "#e5484d");
  const track = opts.mouthTrack || [], FPS = opts.fps || 30;
  const mouthAt = (t, sigma = 1.3, span = 3) => {
    const f = t * FPS; let s = 0, w = 0;
    for (let k = Math.floor(f) - span; k <= Math.ceil(f) + span; k++) {
      const wk = Math.exp(-((k - f) ** 2) / (2 * sigma * sigma));
      s += (track[Math.min(track.length - 1, Math.max(0, k))] || 0) * wk; w += wk;
    }
    return w ? s / w : 0;
  };
  const speechAt = (t) => mouthAt(t, 7, 18);

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

  function mesh(geo, mat, parent, { pos, rot, scale, shadow = true, receive = true } = {}) {
    const m = new THREE.Mesh(geo, mat);
    if (pos) m.position.set(...pos);
    if (rot) m.rotation.set(...rot);
    if (scale) m.scale.set(...scale);
    m.castShadow = shadow; m.receiveShadow = receive;
    parent.add(m);
    return m;
  }
  const cloth = (color, extra = {}) => new THREE.MeshStandardMaterial({ color, roughness: 0.9, ...extra });
  const skinMat = new THREE.MeshPhysicalMaterial({ color: 0xffffff, vertexColors: true, roughness: 0.42, clearcoat: 0.55, clearcoatRoughness: 0.28, sheen: 0.4, sheenColor: new THREE.Color(0xd8ffb0), sheenRoughness: 0.5 });

  // ---------- room ----------
  mesh(new THREE.PlaneGeometry(9, 12), new THREE.MeshStandardMaterial({ map: wallTexture(), roughness: 1 }), scene, { pos: [0, 3, -2.2], shadow: false });
  const board = mesh(new THREE.BoxGeometry(2.0, 1.3, 0.05), cloth(0x2c1d15), scene, { pos: [1.65, 2.95, -2.12], shadow: false });
  for (let i = 0; i < 6; i++) {
    mesh(new THREE.PlaneGeometry(0.28, 0.2), cloth(i % 2 ? 0xe9e1cf : 0xd9b66c), board,
      { pos: [(hash(i) - 0.5) * 1.6, (hash(i + 9) - 0.5) * 1.0, 0.03], rot: [0, 0, (hash(i + 3) - 0.5) * 0.4], shadow: false });
  }
  const pins = [0, 3, 1, 4, 2, 5, 0, 4].map((i) => new THREE.Vector3(1.65 + (hash(i) - 0.5) * 1.6, 2.95 + (hash(i + 9) - 0.5) * 1.0, -2.07));
  scene.add(new THREE.Line(new THREE.BufferGeometry().setFromPoints(pins), new THREE.LineBasicMaterial({ color: accent })));

  // ---------- body (trench coat) ----------
  const rig = new THREE.Group(); rig.position.y = -0.2; rig.scale.setScalar(1.12); scene.add(rig);
  const body = new THREE.Group(); rig.add(body);
  const coat = cloth(COL.coat), coatDark = cloth(COL.coatDark);
  const torso = mesh(lathe([[0.001, -0.2], [0.52, -0.2], [0.55, 0.2], [0.58, 0.6], [0.56, 0.84], [0.42, 0.98], [0.2, 1.05], [0.001, 1.06]]), coat, body, { scale: [1.15, 1, 0.74] });
  const vShape = new THREE.Shape(); vShape.moveTo(-0.17, 1.0); vShape.lineTo(0.17, 1.0); vShape.lineTo(0, 0.48); vShape.closePath();
  mesh(new THREE.ShapeGeometry(vShape), cloth(COL.shirt), body, { pos: [0, 0, 0.405], rot: [-0.18, 0, 0], shadow: false });
  const tieShape = new THREE.Shape(); tieShape.moveTo(-0.035, 0.96); tieShape.lineTo(0.035, 0.96); tieShape.lineTo(0.055, 0.6); tieShape.lineTo(0, 0.52); tieShape.lineTo(-0.055, 0.6); tieShape.closePath();
  mesh(new THREE.ExtrudeGeometry(tieShape, { depth: 0.015, bevelEnabled: true, bevelThickness: 0.006, bevelSize: 0.006, bevelSegments: 3 }), cloth(accent.getHex(), { roughness: 0.6 }), body, { pos: [0, 0, 0.41], rot: [-0.18, 0, 0] });
  for (const s of [-1, 1]) {
    const lap = new THREE.Shape(); lap.moveTo(0, 0); lap.lineTo(s * 0.2, 0.05); lap.lineTo(s * 0.12, 0.52); lap.lineTo(s * 0.02, 0.56); lap.closePath();
    mesh(new THREE.ExtrudeGeometry(lap, { depth: 0.02, bevelEnabled: true, bevelThickness: 0.012, bevelSize: 0.012, bevelSegments: 4 }), coatDark, body, { pos: [s * 0.02, 0.46, 0.385], rot: [-0.2, 0, 0] });
    for (const y of [0.42, 0.24]) mesh(new THREE.SphereGeometry(0.028, 16, 12), cloth(0x2a1a10, { roughness: 0.4 }), body, { pos: [s * 0.2, y, 0.4] });
  }

  // ---------- head: upper skull + hinged jaw (the seam is the mouth) ----------
  const neck = new THREE.Group(); neck.position.set(0, 1.0, 0.04); body.add(neck);
  const head = new THREE.Group(); head.position.set(0, 0.3, 0); neck.add(head);
  const R = 0.5, SX = 1.2;
  const upperGeo = skinPaint(new THREE.SphereGeometry(R, 72, 36, 0, Math.PI * 2, 0, Math.PI * 0.5), (v) => smooth(0.12, 0.0, v.y) * smooth(0.25, 0.45, v.z) * 0.5);
  mesh(upperGeo, skinMat, head, { scale: [SX, 0.86, 1.0], receive: false });
  // roof of the mouth (seen when the jaw drops)
  mesh(new THREE.CircleGeometry(R * 0.985, 64), new THREE.MeshStandardMaterial({ color: COL.mouth, roughness: 0.6, side: THREE.DoubleSide }), head, { pos: [0, -0.002, 0], rot: [Math.PI / 2, 0, 0], scale: [SX, 1, 1], shadow: false, receive: false });
  const jaw = new THREE.Group(); jaw.position.set(0, 0, -0.36); head.add(jaw);
  const jawGeo = skinPaint(new THREE.SphereGeometry(R, 72, 36, 0, Math.PI * 2, Math.PI * 0.5, Math.PI * 0.5), (v) => smooth(-0.05, -0.25, v.y) * 0.9 + smooth(0.2, 0.45, v.z) * 0.5);
  mesh(jawGeo, skinMat, jaw, { pos: [0, 0, 0.36], scale: [SX * 1.0, 0.7, 1.0], receive: false });
  // mouth floor + tongue on top of the jaw
  mesh(new THREE.CircleGeometry(R * 0.96, 64), new THREE.MeshStandardMaterial({ color: COL.mouth, roughness: 0.6 }), jaw, { pos: [0, -0.03, 0.36], rot: [-Math.PI / 2, 0, 0], scale: [SX, 1, 1], shadow: false, receive: false });
  const tongue = mesh(new THREE.SphereGeometry(0.2, 32, 16), new THREE.MeshPhysicalMaterial({ color: COL.tongue, roughness: 0.35, clearcoat: 0.6 }), jaw, { pos: [0, -0.035, 0.5], scale: [0.8, 0.2, 0.6], shadow: false, receive: false });
  // throat sac: puffs out under the jaw when angry or laughing
  const sac = mesh(new THREE.SphereGeometry(0.22, 40, 24), new THREE.MeshPhysicalMaterial({ color: 0xf0f2c8, roughness: 0.35, clearcoat: 0.6, transmission: 0 }), jaw, { pos: [0, -0.2, 0.62], scale: [1, 0.7, 0.8], receive: false });

  // lip line along the front of the seam; corners lift with a smile
  const lipMat = new THREE.MeshStandardMaterial({ color: 0x1f4d18, roughness: 0.5 });
  const lip = new THREE.Mesh(new THREE.BufferGeometry(), lipMat); head.add(lip);
  function lipGeo(smile, open) {
    const pts = [];
    for (let i = 0; i <= 24; i++) {
      const k = i / 24, a = lerp(-1.05, 1.05, k);                 // angle around the front
      const x = Math.sin(a) * R * SX * 1.004, z = Math.cos(a) * R * 1.004;
      const edge = Math.abs(a) / 1.05;
      pts.push(new THREE.Vector3(x, smile * 0.07 * edge ** 2.2 - open * 0.01, z));
    }
    return new THREE.TubeGeometry(new THREE.CatmullRomCurve3(pts), 48, 0.012, 8, false);
  }

  // blush spots
  const blushMat = new THREE.MeshBasicMaterial({ color: COL.blush, transparent: true, opacity: 0, depthWrite: false });
  for (const s of [-1, 1]) mesh(new THREE.CircleGeometry(0.075, 32), blushMat, head, { pos: [s * 0.46, 0.06, 0.3], rot: [0, s * 0.95, 0], scale: [1.2, 0.7, 1], shadow: false, receive: false });

  // ---------- eyes: bulges on top, white eyeballs, golden irises, real eyelids ----------
  const eyes = [];
  const eyeballMat = new THREE.MeshPhysicalMaterial({ color: 0xfdfcf6, roughness: 0.15, clearcoat: 1 });
  const irisMat = new THREE.MeshPhysicalMaterial({ color: COL.iris, roughness: 0.25, clearcoat: 1 });
  const pupilMat = new THREE.MeshBasicMaterial({ color: COL.pupil }), glint = new THREE.MeshBasicMaterial({ color: 0xffffff });
  const lidGeo = skinPaint(new THREE.SphereGeometry(0.172, 48, 24, 0, Math.PI * 2, 0, Math.PI * 0.5), () => 0);
  const bumpGeo = skinPaint(new THREE.SphereGeometry(0.18, 48, 32), () => 0);
  for (const s of [-1, 1]) {
    const socket = new THREE.Group(); socket.position.set(s * 0.29, 0.32, 0.16); socket.rotation.set(0.15, s * 0.3, s * -0.12); head.add(socket);
    mesh(bumpGeo, skinMat, socket, { pos: [0, -0.06, -0.07], scale: [0.95, 0.8, 0.9], receive: false });
    mesh(new THREE.SphereGeometry(0.16, 48, 36), eyeballMat, socket, { pos: [0, 0.01, 0.04], shadow: false, receive: false });
    const look = new THREE.Group(); look.position.set(0, 0.01, 0.04); socket.add(look);
    const iris = mesh(new THREE.SphereGeometry(0.078, 40, 30), irisMat, look, { pos: [0, 0, 0.142], scale: [1, 1, 0.4], shadow: false, receive: false });
    const pupil = mesh(new THREE.SphereGeometry(0.05, 32, 24), pupilMat, iris, { pos: [0, 0, 0.07], scale: [1.2, 0.95, 0.5], shadow: false, receive: false });
    mesh(new THREE.SphereGeometry(0.02, 14, 10), glint, iris, { pos: [0.03, 0.035, 0.1], shadow: false, receive: false });
    mesh(new THREE.SphereGeometry(0.009, 10, 8), glint, iris, { pos: [-0.025, -0.03, 0.1], shadow: false, receive: false });
    // upper lid: a skin dome hinged at the eye centre; rotating it forward closes the eye; z-tilt makes angry/sad shapes
    const lidPivot = new THREE.Group(); lidPivot.position.set(0, 0.01, 0.04); lidPivot.rotation.order = "ZXY"; socket.add(lidPivot);
    mesh(lidGeo, skinMat, lidPivot, { receive: false });
    // lower lid for squints (laughing, smug)
    const lowPivot = new THREE.Group(); lowPivot.position.set(0, 0.01, 0.04); socket.add(lowPivot);
    mesh(lidGeo, skinMat, lowPivot, { rot: [Math.PI, 0, 0], receive: false });
    eyes.push({ socket, look, pupil, lidPivot, lowPivot, s });
  }

  // ---------- fedora: tipped back between the eyes ----------
  const hat = new THREE.Group(); hat.position.set(0, 0.4, -0.1); hat.rotation.set(-0.18, 0, 0.08); hat.scale.setScalar(1.2); head.add(hat);
  const hatMat = cloth(COL.hat, { roughness: 0.75 });
  mesh(lathe([[0.001, 0], [0.22, 0.0], [0.38, 0.012], [0.44, 0.045], [0.45, 0.065], [0.42, 0.032], [0.22, 0.02], [0.001, 0.02]], 72), hatMat, hat);
  mesh(lathe([[0.001, 0.27], [0.13, 0.28], [0.2, 0.23], [0.22, 0.1], [0.23, 0.0], [0.001, 0.0]], 64), hatMat, hat);
  mesh(new THREE.CylinderGeometry(0.234, 0.236, 0.06, 64, 1, true), cloth(accent.getHex(), { roughness: 0.6 }), hat, { pos: [0, 0.045, 0] });

  // steam (furious)
  const steam = [];
  for (let i = 0; i < 8; i++) {
    const m = new THREE.Mesh(new THREE.SphereGeometry(0.06, 16, 12), new THREE.MeshBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0, depthWrite: false }));
    head.add(m); steam.push(m);
  }

  // ---------- arms with three-fingered frog hands resting on the desk ----------
  const arms = [];
  for (const s of [-1, 1]) {
    const shoulder = new THREE.Group(); shoulder.position.set(s * 0.54, 0.8, 0); body.add(shoulder);
    mesh(new THREE.CapsuleGeometry(0.14, 0.4, 10, 24), coat, shoulder, { pos: [0, -0.25, 0] });
    const elbow = new THREE.Group(); elbow.position.set(0, -0.48, 0); shoulder.add(elbow);
    mesh(new THREE.CapsuleGeometry(0.125, 0.34, 10, 24), coat, elbow, { pos: [0, -0.19, 0] });
    mesh(new THREE.TorusGeometry(0.12, 0.03, 12, 32), coatDark, elbow, { pos: [0, -0.37, 0], rot: [Math.PI / 2, 0, 0] });
    const hand = new THREE.Group(); hand.position.set(0, -0.45, 0.02); elbow.add(hand);
    const handGeo = skinPaint(new THREE.SphereGeometry(0.1, 32, 24), () => 0);
    mesh(handGeo, skinMat, hand, { scale: [1.1, 0.8, 1] });
    for (const f of [-1, 0, 1]) {
      const finger = new THREE.Group(); finger.position.set(f * 0.06, -0.06, 0.03); finger.rotation.set(-0.2, 0, f * 0.35); hand.add(finger);
      mesh(new THREE.CapsuleGeometry(0.028, 0.08, 6, 12), skinMat, finger, { pos: [0, -0.05, 0] });
      mesh(new THREE.SphereGeometry(0.04, 20, 14), skinMat, finger, { pos: [0, -0.11, 0] });   // toe pad
    }
    arms.push({ shoulder, elbow, hand, s });
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

  // ---------- lights ----------
  scene.add(new THREE.HemisphereLight(0xfff0dc, 0x1a0f0c, 0.6));
  const key = new THREE.DirectionalLight(0xffe2bd, 2.5);
  key.position.set(-2.5, 4.5, 4); key.target.position.set(0, 1.4, 0);
  key.castShadow = true; key.shadow.mapSize.set(2048, 2048); key.shadow.bias = -0.0002; key.shadow.normalBias = 0.025;
  Object.assign(key.shadow.camera, { left: -2.5, right: 2.5, top: 3, bottom: -1, near: 0.5, far: 12 });
  scene.add(key, key.target);
  const rim = new THREE.DirectionalLight(accent, 3.0); rim.position.set(2.2, 3.2, -3); scene.add(rim);
  const rim2 = new THREE.DirectionalLight(0x7aa0ff, 1.3); rim2.position.set(-2.4, 2.6, -2.5); scene.add(rim2);
  const fill = new THREE.PointLight(0xfff2e0, 2.2, 6, 1.5); fill.position.set(0.6, 1.7, 2.6); scene.add(fill);
  const lampLight = new THREE.PointLight(0xffc77a, 5, 3.5, 1.5); lampLight.position.set(-1.07, 0.75, 0.8); scene.add(lampLight);
  const rage = new THREE.PointLight(0xff2a1a, 0, 6, 1.4); rage.position.set(0, 2.2, 1.6); scene.add(rage);

  const baseTint = new THREE.Color(0xffffff), rageTint = new THREE.Color(0xff9a7a);

  function draw({ t, emo, mouth = 0, slam = 0, fistY = 0 }) {
    const e = emo;
    const m = track.length ? mouthAt(t) : mouth;
    const sp = track.length ? speechAt(t) : mouth;

    const push = smooth(0, 40, t);
    camera.position.set(noise(t * 0.25, 1) * 0.05, 1.74 + noise(t * 0.2, 2) * 0.015 - Math.max(0, slam) * 0.025, lerp(9.2, 8.6, push));
    camera.lookAt(0, 1.9 - push * 0.04, 0);

    const breathe = Math.sin(t * 1.9) * 0.01;
    const bounce = (Math.sin(t * 6.5) * 0.5 + 0.5) * e.bounce * 0.03 + (e.laugh || 0) * (Math.sin(t * 11) * 0.5 + 0.5) * 0.025;
    body.position.y = bounce;
    torso.scale.y = 1 + breathe;
    body.rotation.x = -e.red * 0.07 + (e.round || 0) * 0.03;
    const tremble = e.shake > 2 ? (e.shake - 2) / 7 : 0;
    body.position.x = noise(t * 9, 3) * tremble * 0.012;

    head.rotation.x = -sp * 0.07 + noise(t * 0.6, 4) * 0.03 - (e.laugh || 0) * 0.14 + e.red * 0.05;
    head.rotation.y = noise(t * 0.45, 5) * 0.09 + sp * noise(t * 1.6, 6) * 0.05;
    head.rotation.z = (e.tilt * Math.PI) / 180 + noise(t * 0.5, 7) * 0.025;
    head.position.x = noise(t * 11, 8) * tremble * 0.006;

    skinMat.color.copy(baseTint).lerp(rageTint, e.red * 0.5);
    rage.intensity = e.red * 9;
    blushMat.opacity = clamp(e.blush) * 0.45;

    // jaw: lip-sync plus emotion (O when shocked, wide when laughing)
    const open = clamp(m * 0.8 + (e.round || 0) * 0.25 + (e.laugh || 0) * 0.3 * (0.6 + 0.4 * Math.sin(t * 15)), 0, 1.0);
    jaw.rotation.x = open * 0.2;
    tongue.position.y = -0.035 + open * 0.02;
    lip.geometry.dispose();
    lip.geometry = lipGeo(e.smile, open);
    const puff = Math.max(e.red * 0.9, (e.laugh || 0) * 0.6) * (0.75 + 0.25 * Math.sin(t * 5));
    sac.scale.set(0.55 + puff * 0.6, 0.35 + puff * 0.6, 0.5 + puff * 0.5);

    // eyes: lids from openness (+ smooth blink), z-tilt from brow angle (angry = inner corners down), gaze drift
    const cycle = 3.8, ph = t % cycle, idx = Math.floor(t / cycle);
    let blink = Math.exp(-((ph - 3.6) ** 2) / 0.004);
    if (hash(idx) > 0.7) blink = Math.max(blink, Math.exp(-((ph - 3.3) ** 2) / 0.004));
    for (const { look, pupil, lidPivot, lowPivot, s } of eyes) {
      const openK = clamp((e.eye - 0.3) / 1.0);                        // 0 = squeezed, 1 = wide
      const closure = Math.max(blink, 1 - openK) ;
      lidPivot.rotation.x = lerp(-0.95 - e.lift * 0.012, 1.55, closure);   // back = open, forward = shut
      lidPivot.rotation.z = -s * (e.brow * Math.PI / 180) * 0.9 + (e.asym || 0) * (s > 0 ? -0.25 : 0);
      lowPivot.rotation.x = lerp(1.25, 0.55, clamp((e.laugh || 0) + (e.asym || 0) * 0.4 + Math.max(0, e.smile - 0.6)));
      pupil.scale.set(1.25 * e.pupil, 0.95 * e.pupil, 0.5);
      look.rotation.y = noise(t * 0.35, 9) * 0.12;
      look.rotation.x = noise(t * 0.3, 10) * 0.06;
    }

    // arms: hands on the desk, small speech-driven moves; right fist winds up and slams
    const raise = clamp(-fistY / 150);
    for (const { shoulder, elbow, hand, s } of arms) {
      const gest = sp * noise(t * 1.3, 12 + s) * 0.18;
      shoulder.rotation.set(-0.55 + gest, 0, s * 0.12);
      elbow.rotation.set(-1.15 - gest * 0.6, 0, s * -0.12);
      hand.rotation.x = 0.9;
      if (s > 0) {
        shoulder.rotation.x = lerp(shoulder.rotation.x, -2.1, raise);
        elbow.rotation.x = lerp(elbow.rotation.x, -1.0, raise);
      }
    }
    files.position.y = 0.26 + Math.max(0, slam) * 0.06;
    mag.position.y = 0.27 + Math.max(0, slam) * 0.08;

    steam.forEach((p, i) => {
      const k = (t * 0.8 + i / steam.length) % 1, s = i % 2 ? 1 : -1;
      p.position.set(s * (0.3 + k * 0.1), 0.55 + k * 0.5, 0.0);
      p.scale.setScalar(0.6 + k * 1.5);
      p.material.opacity = e.steam * (1 - k) * 0.7;
    });

    renderer.render(scene, camera);
  }

  return { draw, canvas: cv };
}
