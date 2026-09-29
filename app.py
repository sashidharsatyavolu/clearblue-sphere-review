
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Interactive Digital Sphere",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
#MainMenu, footer, header {visibility: hidden;}
.block-container {padding: 0 !important; max-width: 100% !important;}
[data-testid="stAppViewContainer"] {background: #01060b;}
[data-testid="stHeader"] {background: transparent;}
</style>
""", unsafe_allow_html=True)

html = r"""
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<style>
html,body{margin:0;width:100%;height:100%;overflow:hidden;background:#01060b}
#sphere{position:absolute;inset:0;width:100%;height:100%;cursor:grab}
#sphere:active{cursor:grabbing}
canvas{display:block;width:100%;height:100%}
</style>
</head>
<body>
<div id="sphere" aria-label="Interactive digital network sphere"></div>

<script type="module">
import * as THREE from "https://cdn.jsdelivr.net/npm/three@0.180.0/build/three.module.js";

const el=document.getElementById("sphere");
const reduced=matchMedia("(prefers-reduced-motion: reduce)").matches;

const scene=new THREE.Scene();
const camera=new THREE.PerspectiveCamera(32,1,.1,100);
camera.position.set(0,0,5.6);

const renderer=new THREE.WebGLRenderer({
  antialias:true,alpha:true,powerPreference:"high-performance"
});
renderer.setPixelRatio(Math.min(devicePixelRatio,2));
renderer.outputColorSpace=THREE.SRGBColorSpace;
renderer.toneMapping=THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure=1.2;
el.appendChild(renderer.domElement);

const root=new THREE.Group();
scene.add(root);

const core=new THREE.Mesh(
  new THREE.SphereGeometry(1.48,64,64),
  new THREE.MeshPhysicalMaterial({
    color:0x021322,roughness:.72,metalness:.08,
    transparent:true,opacity:.34,clearcoat:.45
  })
);
root.add(core);

const count=5200;
const pos=new Float32Array(count*3);
for(let i=0;i<count;i++){
  const z=Math.random()*2-1,a=Math.random()*Math.PI*2;
  const r=Math.sqrt(1-z*z),radius=1.505+Math.random()*.055;
  pos[i*3]=radius*r*Math.cos(a);
  pos[i*3+1]=radius*z;
  pos[i*3+2]=radius*r*Math.sin(a);
}
const geo=new THREE.BufferGeometry();
geo.setAttribute("position",new THREE.BufferAttribute(pos,3));
const mat=new THREE.PointsMaterial({
  color:0x8edcff,size:.014,transparent:true,opacity:.82,
  depthWrite:false,blending:THREE.AdditiveBlending
});
const particleGlobe=new THREE.Points(geo,mat);
root.add(particleGlobe);

const nodeCount=75;
const nodePos=new Float32Array(nodeCount*3);
for(let i=0;i<nodeCount;i++){
  const z=Math.random()*2-1,a=Math.random()*Math.PI*2;
  const r=Math.sqrt(1-z*z),radius=1.535;
  nodePos[i*3]=radius*r*Math.cos(a);
  nodePos[i*3+1]=radius*z;
  nodePos[i*3+2]=radius*r*Math.sin(a);
}
const nodeGeo=new THREE.BufferGeometry();
nodeGeo.setAttribute("position",new THREE.BufferAttribute(nodePos,3));
root.add(new THREE.Points(nodeGeo,new THREE.PointsMaterial({
  color:0xd5f5ff,size:.032,transparent:true,opacity:.9,
  blending:THREE.AdditiveBlending
})));

const atmosphere=new THREE.Mesh(
  new THREE.SphereGeometry(1.67,64,64),
  new THREE.ShaderMaterial({
    transparent:true,depthWrite:false,blending:THREE.AdditiveBlending,
    uniforms:{glow:{value:new THREE.Color(0x1ba9ff)}},
    vertexShader:`
      varying vec3 n; varying vec3 worldPos;
      void main(){
        n=normalize(normalMatrix*normal);
        vec4 w=modelMatrix*vec4(position,1.0);
        worldPos=w.xyz;
        gl_Position=projectionMatrix*viewMatrix*w;
      }`,
    fragmentShader:`
      uniform vec3 glow; varying vec3 n; varying vec3 worldPos;
      void main(){
        vec3 v=normalize(cameraPosition-worldPos);
        float edge=pow(1.0-max(dot(n,v),0.0),3.2);
        gl_FragColor=vec4(glow,edge*.42);
      }`
  })
);
root.add(atmosphere);

function orbit(rx,ry,rz,sx,sy,opacity,speed){
  const curve=new THREE.EllipseCurve(0,0,1.95*sx,.72*sy,0,Math.PI*2,false,0);
  const pts=curve.getPoints(240).map(p=>new THREE.Vector3(p.x,p.y,0));
  const line=new THREE.LineLoop(
    new THREE.BufferGeometry().setFromPoints(pts),
    new THREE.LineBasicMaterial({
      color:0x78d9ff,transparent:true,opacity,
      blending:THREE.AdditiveBlending
    })
  );
  line.rotation.set(rx,ry,rz);
  line.userData.speed=speed;
  root.add(line);
  return line;
}
const orbits=[
  orbit(1.02,.18,.2,1,1,.42,.028),
  orbit(1.68,-.52,-.34,1.05,.9,.28,-.018),
  orbit(.48,1.15,.8,.95,1.15,.22,.022),
  orbit(2.18,.38,-.75,1.12,.82,.17,-.014)
];

const floatCount=240;
const floatPos=new Float32Array(floatCount*3);
for(let i=0;i<floatCount;i++){
  const a=Math.random()*Math.PI*2,b=Math.acos(2*Math.random()-1);
  const r=1.9+Math.random()*1.4;
  floatPos[i*3]=r*Math.sin(b)*Math.cos(a);
  floatPos[i*3+1]=r*Math.cos(b);
  floatPos[i*3+2]=r*Math.sin(b)*Math.sin(a);
}
const floatGeo=new THREE.BufferGeometry();
floatGeo.setAttribute("position",new THREE.BufferAttribute(floatPos,3));
const floating=new THREE.Points(floatGeo,new THREE.PointsMaterial({
  color:0x399dd6,size:.012,transparent:true,opacity:.34,
  depthWrite:false,blending:THREE.AdditiveBlending
}));
scene.add(floating);

scene.add(new THREE.AmbientLight(0x0a2030,1.1));
const key=new THREE.PointLight(0x8bdfff,5.5,8);
key.position.set(3,2,4);scene.add(key);
const rim=new THREE.PointLight(0x008cff,6,7);
rim.position.set(-3,-1,2);scene.add(rim);

let mouseX=0,mouseY=0,targetX=0,targetY=0;
let dragging=false,sx=0,sy=0,rx=0,ry=0;

el.addEventListener("pointermove",e=>{
  const r=el.getBoundingClientRect();
  const px=(e.clientX-r.left)/r.width-.5;
  const py=(e.clientY-r.top)/r.height-.5;
  targetY=px*.34; targetX=-py*.22;
  if(dragging){
    root.rotation.y=ry+(e.clientX-sx)*.0035;
    root.rotation.x=rx+(e.clientY-sy)*.0035;
  }
});
el.addEventListener("pointerleave",()=>{targetX=0;targetY=0});
el.addEventListener("pointerdown",e=>{
  dragging=true;sx=e.clientX;sy=e.clientY;
  rx=root.rotation.x;ry=root.rotation.y;
  el.setPointerCapture(e.pointerId);
});
el.addEventListener("pointerup",e=>{
  dragging=false;el.releasePointerCapture(e.pointerId);
});

const clock=new THREE.Clock();
function animate(){
  requestAnimationFrame(animate);
  const t=clock.getElapsedTime();

  mouseX+=(targetX-mouseX)*.045;
  mouseY+=(targetY-mouseY)*.045;

  if(!dragging){
    root.rotation.x+=(mouseX-root.rotation.x)*.018;
    root.rotation.y+=mouseY*.006;
    if(!reduced)root.rotation.y+=.00075;
  }

  particleGlobe.rotation.y=t*.006;
  atmosphere.rotation.y=t*.003;
  floating.rotation.y=-t*.002;
  orbits.forEach(o=>o.rotation.z+=o.userData.speed);
  atmosphere.scale.setScalar(1+Math.sin(t*1.15)*.009);

  renderer.render(scene,camera);
}

function resize(){
  const w=Math.max(1,el.clientWidth),h=Math.max(1,el.clientHeight);
  camera.aspect=w/h;camera.updateProjectionMatrix();
  renderer.setSize(w,h);
  renderer.setPixelRatio(Math.min(devicePixelRatio,2));
}
addEventListener("resize",resize);
resize();animate();
</script>
</body>
</html>
"""

components.html(html, height=780, scrolling=False)
