# Luna AI — Cyber Celestial UI
# Apariencia nueva. Chat, voz, dictado y cerebros conservados.
# Cerebros disponibles: Claude, GPT, Gemini, OpenRouter (con respaldo automático).

import asyncio
import json
import os
import re
from datetime import datetime
from zoneinfo import ZoneInfo
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from flask import Flask, Response, jsonify, request

app = Flask(__name__)

# ==========================================
# LUNA AI - INTERFAZ
# ==========================================

PAGE = r"""
<!doctype html>
<html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Luna AI</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Sora:wght@300;400;600&display=swap">
<style>
:root{color-scheme:dark;--bg:#07040f;--ln:rgba(var(--accrgb),.4);--vio:#a66bff;--cy:#35e1ff;--tx:#efe7ff;--mu:#a597c4;--acc1:#8a33f0;--acc2:#4a1a96;--accrgb:176,110,255;box-sizing:border-box;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}
#app{transition:background .8s}
#app[data-mode=avatar]{background:radial-gradient(ellipse at 50% 30%,rgba(var(--accrgb),.16),transparent 60%),radial-gradient(ellipse at 10% 5%,rgba(var(--accrgb),.12),transparent 40%),var(--bg)}
html{scroll-padding-top:env(safe-area-inset-top,0px)}
*{box-sizing:border-box}
html,body{height:100%;margin:0;background:var(--bg);color:var(--tx);font:400 14px/1.4 Sora,system-ui,sans-serif;overflow:hidden}
button,input{font:inherit;color:inherit}button{cursor:pointer}
button:focus-visible,input:focus-visible,label:focus-within{outline:2px solid var(--cy);outline-offset:2px}
#app{height:100%;display:grid;grid-template-rows:56px 1fr auto;position:relative;
 background:radial-gradient(ellipse at 50% 45%,rgba(80,35,160,.3),transparent 55%),radial-gradient(ellipse at 10% 5%,rgba(60,25,120,.3),transparent 35%),var(--bg)}
#app:before{content:"";position:absolute;inset:0;opacity:.5;pointer-events:none;
 background-image:radial-gradient(1px 1px at 8% 18%,#e8caff 60%,transparent),radial-gradient(1.4px 1.4px at 22% 70%,#a964ff 60%,transparent),radial-gradient(1px 1px at 70% 19%,#fff 60%,transparent),radial-gradient(1px 1px at 88% 47%,#c3eaff 60%,transparent),radial-gradient(1.3px 1.3px at 58% 84%,#ebc7ff 60%,transparent);
 background-size:317px 259px,389px 311px,241px 223px,353px 281px,293px 331px;animation:stars 40s linear infinite}
@keyframes stars{to{background-position:317px 259px,-389px 311px,241px -223px,-353px 281px,293px -331px}}
header{display:flex;align-items:center;justify-content:space-between;padding:0 16px;border-bottom:1px solid var(--ln);background:rgba(12,7,28,.7);z-index:5}
.brand{font-weight:600;font-size:17px;letter-spacing:.08em;text-shadow:0 0 12px #c58bff}
.tog{display:flex;gap:3px;padding:3px;border:1px solid var(--ln);border-radius:24px;background:rgba(12,8,29,.85)}
.tog button{border:0;background:none;padding:7px 18px;border-radius:20px;color:var(--mu);transition:.2s}
.tog button[aria-pressed=true]{color:#fff;background:linear-gradient(135deg,#7a2be0,#3a1672);box-shadow:0 0 14px #9f47ff}
#app[data-mode=avatar] .tog button[aria-pressed=true]{background:linear-gradient(135deg,var(--acc1),var(--acc2));box-shadow:0 0 14px rgba(var(--accrgb),.8)}
.hr{display:flex;align-items:center;gap:12px}#pal{width:32px;height:32px;border-radius:50%;border:1px solid var(--ln);background:rgba(40,22,75,.8)}
.pill{display:flex;align-items:center;gap:8px;font-size:12px;color:var(--mu)}
.pill i{width:8px;height:8px;border-radius:50%;background:#39f77c;box-shadow:0 0 9px #39f77c;transition:.3s}
.pill[data-s=thinking] i{background:#ffd23a;box-shadow:0 0 9px #ffd23a}
.pill[data-s=speaking] i{background:var(--cy);box-shadow:0 0 9px var(--cy)}
.pill[data-s=listening] i{background:#ff5fb0;box-shadow:0 0 9px #ff5fb0}
#stage{position:relative;min-height:0}
canvas{display:block}
#core,#core2{position:absolute;inset:0;width:100%;height:100%}
#core2{transition:opacity .6s,transform .6s;transform-origin:50% 45%;pointer-events:none}
#app[data-mode=avatar] #core2{opacity:0;transform:scale(.7)}
#app{--h:.55}
#chars{position:absolute;left:50%;top:1.5%;translate:-50% 0;display:none;gap:3px;padding:3px;border:1px solid var(--ln);border-radius:20px;background:rgba(12,8,29,.85);z-index:4}
#app[data-mode=avatar] #chars{display:flex}
#chars button{border:0;background:none;padding:5px 14px;border-radius:16px;color:var(--mu);font-size:12px}
#chars button[aria-pressed=true]{color:#fff;background:linear-gradient(135deg,var(--acc1),var(--acc2))}
#chars{transition:border-color .6s}
#holo{position:absolute;left:50%;bottom:1%;translate:-50% 0;display:none;align-items:center;gap:8px;font-size:11px;color:var(--mu);z-index:4}
#app[data-mode=avatar] #holo{display:flex}
#holo input{accent-color:#a66bff;width:130px}
.pn{position:absolute;width:min(23%,260px);height:21%;border:1px solid var(--ln);border-radius:12px;padding:8px 10px;background:rgba(14,9,34,.55);backdrop-filter:blur(4px);box-shadow:inset 0 0 20px rgba(110,60,200,.12);transition:opacity .4s}
.pn span{font-size:11px;color:var(--mu)}
.pn canvas{width:100%;height:calc(100% - 18px)}
.pn.l{left:3%}.pn.r{right:3%}.a{top:8%}.b{top:35%}
#app[data-mode=avatar] .pn{opacity:.4}
#app[data-char=dracona] .pn{border-color:rgba(217,179,108,.5)}
#app[data-char=dracona] .pn:before,#app[data-char=dracona] .pn:after{content:"";position:absolute;width:10px;height:10px;border:1.5px solid #d9b36c;opacity:.85;pointer-events:none}
#app[data-char=dracona] .pn:before{top:-1px;left:-1px;border-right:0;border-bottom:0}
#app[data-char=dracona] .pn:after{bottom:-1px;right:-1px;border-left:0;border-top:0}
#app[data-char=dracona] header{border-bottom:1px solid rgba(217,179,108,.4);box-shadow:0 1px 0 rgba(217,179,108,.15)}
#app[data-char=dracona] #chars{border-color:rgba(217,179,108,.5)}
#app[data-char=dracona] #chars button[aria-pressed=true]{background:linear-gradient(135deg,#2a7a4a,#0a3a22);box-shadow:0 0 10px rgba(217,179,108,.5);border:1px solid rgba(217,179,108,.6)}
#app[data-char=dracona] .brand{text-shadow:0 0 10px rgba(217,179,108,.7);letter-spacing:.12em}
#app[data-char=dracona] .brand:after{content:"";display:inline-block;width:5px;height:5px;background:#d9b36c;margin-left:8px;border-radius:0;transform:rotate(45deg);vertical-align:middle;box-shadow:0 0 6px #d9b36c}
#app[data-char=dracona] form{border-color:rgba(217,179,108,.45)}
#app[data-char=dracona] form button[type=submit]{background:linear-gradient(135deg,#2a7a4a,#0a3a22);border-color:#d9b36c}
@media(max-width:760px){.pn{display:none}.tog button{padding:7px 12px}.brand{display:none}}
#av{position:absolute;left:50%;bottom:13%;height:76%;max-width:92%;translate:-50% 0;display:none;pointer-events:none;padding:26px 26px 0;box-sizing:border-box;
 transform:translateY(calc(var(--lv,0)*-7px)) scale(calc(1 + var(--lv,0)*.012));transform-origin:50% 100%;
 -webkit-mask-image:linear-gradient(#000 80%,transparent);mask-image:linear-gradient(#000 80%,transparent);animation:fl 9s infinite}
#app[data-mode=avatar] #av.has{display:block}
#av.rev{animation:rev .9s ease-out,fl 9s infinite}
@keyframes rev{from{clip-path:inset(100% 0 0 0)}to{clip-path:inset(0)}}
@keyframes fl{0%,91%,95%,100%{opacity:1}92%{opacity:.78}93%{opacity:1}94%{opacity:.88}}
#avimg{display:block;height:100%;width:auto;max-width:100%;object-fit:contain;transition:opacity .16s;animation:br var(--breathe,5.2s) ease-in-out infinite;transform-origin:50% 100%;
 opacity:calc(1 - .5*var(--h));filter:saturate(calc(1 - .4*var(--h))) brightness(calc(1 + .15*var(--h))) contrast(calc(1 - .1*var(--h))) drop-shadow(0 0 calc(8px + 20px*var(--h)) rgba(var(--gl,176,110,255),.7)) drop-shadow(0 0 4px rgba(53,225,255,.4))}
@keyframes br{
 0%{transform:translateY(0) translateX(0) rotate(0deg) scale(1)}
 28%{transform:translateY(-6px) translateX(1.5px) rotate(.3deg) scale(1.012)}
 52%{transform:translateY(-3px) translateX(-1px) rotate(-.2deg) scale(1.006)}
 76%{transform:translateY(-7px) translateX(1px) rotate(.25deg) scale(1.014)}
 100%{transform:translateY(0) translateX(0) rotate(0deg) scale(1)}
}
#av:before,#av:after{content:"";position:absolute;inset:26px 26px 0;-webkit-mask:var(--img) center/100% 100% no-repeat;mask:var(--img) center/100% 100% no-repeat}
#av:before{background:linear-gradient(180deg,var(--t1,#b78cff),var(--t2,#4aa8ff));mix-blend-mode:color;opacity:calc(.65*var(--h))}
#av:after{background:repeating-linear-gradient(0deg,rgba(150,100,255,.35) 0 1px,transparent 1px 3px);opacity:calc(.85*var(--h));animation:sc 6s linear infinite}
#av .fog{position:absolute;inset:26px 26px 0;-webkit-mask:var(--img) center/100% 100% no-repeat;mask:var(--img) center/100% 100% no-repeat;pointer-events:none;
 opacity:calc(.6*var(--h));background:radial-gradient(ellipse at 20% 55%,rgba(var(--gl,61,220,132),.9),transparent 55%),radial-gradient(ellipse at 82% 40%,rgba(var(--gl,61,220,132),.8),transparent 50%),radial-gradient(ellipse at 50% 95%,rgba(var(--gl,61,220,132),.55),transparent 60%);
 filter:blur(6px);mix-blend-mode:screen;animation:fog 7s ease-in-out infinite}
@keyframes fog{0%,100%{opacity:calc(.45*var(--h));transform:translateY(0) scale(1)}50%{opacity:calc(.8*var(--h));transform:translateY(-4px) scale(1.015)}}
@keyframes sc{to{background-position:0 60px}}
#empty{position:absolute;inset:18% 20% 28%;display:none;align-items:center;justify-content:center;text-align:center;border:1px dashed var(--ln);border-radius:16px;color:var(--mu);padding:20px}
#app[data-mode=avatar]:not(.has) #empty{display:flex}
#poses{position:absolute;left:3%;right:3%;bottom:3%;display:flex;gap:6px;align-items:end;flex-wrap:nowrap;overflow-x:auto;overflow-y:hidden;max-width:94%;z-index:4;padding-bottom:4px;scrollbar-width:thin;scrollbar-color:rgba(var(--accrgb),.5) transparent}
#poses label{flex:none}
#poses::-webkit-scrollbar{height:6px}
#poses::-webkit-scrollbar-thumb{background:rgba(var(--accrgb),.5);border-radius:6px}
#app:not([data-mode=avatar]) #poses{display:none}
#poses label{width:46px;height:46px;border:1px solid var(--ln);border-radius:10px;background:rgba(14,9,34,.8);padding:0;overflow:hidden;display:grid;place-items:center;color:var(--vio);font-size:22px}
#av{overflow:hidden}
#avimg{animation:none;transform:scale(var(--portrait-scale,1));transform-origin:50% 0}
#av[data-preview=true] #avimg{transform:scale(var(--portrait-scale,1))}
#wardrobe{position:absolute;left:calc(3% + 54px);bottom:calc(3% + 4px);z-index:5;max-width:calc(94% - 54px)}
#app:not([data-mode=avatar]) #wardrobe{display:none}
#wardrobe summary,#wardrobe button,#wardrobe select{color:var(--tx);background:#160e2a;border:1px solid var(--ln);border-radius:10px;padding:9px;font:inherit}
#wardrobe summary,#wardrobe button{cursor:pointer}
#wardrobe .preview-panel{position:absolute;bottom:calc(100% + 8px);left:0;display:grid;gap:8px;padding:12px;background:#110b21;border:1px solid var(--ln);border-radius:12px;width:min(260px,calc(94vw - 54px))}
#wardrobe .preview-panel label{display:grid;gap:4px}
#wardrobe select{width:100%;min-width:0}
#wardrobe-status{margin:0;min-height:1.2em;color:var(--mu)}
#av[data-preview=true] #avimg{animation:none}
#av[data-preview=true]:before,#av[data-preview=true]:after,#av[data-preview=true] .fog{visibility:hidden}
#log{position:absolute;right:3%;bottom:3%;width:min(340px,44%);max-height:34%;overflow:auto;display:flex;flex-direction:column;gap:6px;z-index:4;scrollbar-width:thin}
.m{padding:8px 11px;border-radius:12px;background:rgba(25,15,45,.88);border:1px solid rgba(var(--accrgb),.35);font-size:12.5px;transition:border-color .6s}
.m.yo{align-self:flex-end;background:rgba(60,18,95,.9);border-color:var(--acc1)}
footer{padding:0 3% 12px;z-index:5}
#eq{width:100%;height:44px}
form{display:flex;gap:8px;max-width:760px;margin:6px auto 0;padding:6px;border:1px solid var(--ln);border-radius:16px;background:rgba(12,8,29,.9);box-shadow:0 0 22px rgba(138,58,222,.25)}
form input{flex:1;min-width:0;background:none;border:0;padding:8px 10px}
form button{width:42px;height:38px;border-radius:11px;border:1px solid var(--ln);background:rgba(40,22,75,.9)}
form button[type=submit]{background:linear-gradient(135deg,var(--acc1),var(--acc2));border-color:#c17bff;transition:background .6s}
#mic[aria-pressed=true]{border-color:#ff5fb0;box-shadow:0 0 12px #ff5fb0}
#holo input{accent-color:var(--acc1)}
@media(prefers-reduced-motion:reduce){#avimg,#av,#av:after,#app:before{animation:none}}
</style></head>
<body>
<div id="app" data-mode="core">
<header>
 <div class="brand">Luna AI</div>
 <div class="tog" role="group" aria-label="Modo"><button data-m="core" aria-pressed="true">Núcleo</button><button data-m="avatar" id="mav" aria-pressed="false">Dracona</button></div>
 <div class="hr"><button id="pal" aria-label="Cambiar color del núcleo" title="Cambiar color del núcleo">◐</button><div class="pill" id="st" data-s="idle"><i></i><b style="font-weight:400" id="stt">Lista</b></div></div>
</header>
<main id="stage">
 <canvas id="core"></canvas><canvas id="core2"></canvas>
 <div class="pn l a"><span>Entrada de voz</span><canvas class="pc" data-k="w1"></canvas></div>
 <div class="pn l b"><span>Voz de Luna</span><canvas class="pc" data-k="w2"></canvas></div>
 <div class="pn r a"><span>Actividad</span><canvas class="pc" data-k="bars"></canvas></div>
 <div class="pn r b"><span>Sistema</span><canvas class="pc" data-k="ring"></canvas></div>
 <div id="empty">Suelta aquí las imágenes de <b id="et">Dracona</b>, o usa el botón +.<br>Mejor en PNG o WebP con fondo transparente, de 1024 px o más.</div>
 <div id="av"><img id="avimg" alt="Personaje"><div class="fog"></div></div>
 <div id="chars" role="group" aria-label="Personalidad"><button data-c="dracona" aria-pressed="true">Dracona</button><button data-c="rem" aria-pressed="false">Aurora</button><button data-c="luna" aria-pressed="false">Luna</button></div>
 <label id="holo">Holograma <input type="range" id="hr" min="0" max="100" value="55" aria-label="Intensidad del holograma"></label>
 <div id="poses"><label id="load" tabindex="0" title="Cargar imágenes">+<input type="file" id="file" accept="image/*" multiple hidden></label></div>
 <details id="wardrobe">
  <summary>Vestuario y gestos</summary>
  <div class="preview-panel">
   <label>Atuendo<select id="outfitChoice"></select></label>
   <label>Animación<select id="gestureChoice"></select></label>
   <button type="button" id="playGesture">Reproducir gesto</button>
   <label><span><input type="checkbox" id="originalClip"> Ver GIF con su traje original</span></label>
   <label><span><input type="checkbox" id="autoOutfit" checked> Cambiar de ropa automáticamente</span></label>
   <p id="wardrobe-status" role="status"></p>
  </div>
 </details>
 <div id="log" hidden></div>
</main>
<footer>
 <canvas class="pc" id="eq" data-k="eq"></canvas>
 <form id="f"><button type="button" id="mic" aria-pressed="false" aria-label="Micrófono">🎙</button><input id="q" placeholder="Escríbele a Luna…" autocomplete="off"><button type="submit" aria-label="Enviar">➤</button></form>
</footer>
</div>
<script>
const $=s=>document.querySelector(s),app=$('#app'),cv=$('#core'),cv2=$('#core2'),g2=cv2.getContext('2d');let g=cv.getContext('2d');
const BACKEND='/api/chat';
let W=0,H=0,D=1,state='idle',level=0,mic=null,last=0,dt=.016,mode='core',mf=0,modeT=0;
const calm=matchMedia('(prefers-reduced-motion: reduce)').matches;
function dragonPts(n){const P=[];for(let i=0;i<n;i++){const u=i/(n-1),ang=u*10.5,r=.9*(1-.5*u*u);P.push([Math.sin(ang)*r,(u-.5)*1.7,Math.cos(ang)*r*.6])}return P}
const DRAG=dragonPts(70);
let coreChar='dracona';
const parts=Array.from({length:70},()=>({a:Math.random()*6.28,r:Math.random(),y:Math.random(),s:.05+Math.random()*.12}));
function rv(){const z=Math.random()*2-1,a=Math.random()*6.283,r=Math.sqrt(1-z*z);return[r*Math.cos(a),z,r*Math.sin(a)]}
const SH=Array.from({length:640},()=>{const u=rv(),d=rv(),dp=u[0]*d[0]+u[1]*d[1]+u[2]*d[2],q=[d[0]-u[0]*dp*.85,d[1]-u[1]*dp*.85,d[2]-u[2]*dp*.85],n=Math.hypot(q[0],q[1],q[2]),r=Math.random();
 return{u,d:q.map(v=>v/n),rr:.55+.45*Math.pow(Math.random(),.4),l:.03+Math.random()*.09,ph:Math.random()*9,per:4+Math.random()*6,sp:Math.random()*2-1,ty:r<.14?1:r<.19?2:0,io:Math.random()<.5}});
let pm=0,pal=0,ACC='176,110,255',CORE0=[150,100,255],CORE1=[40,205,238],EXPER=7,SHARP=0,PULSE='double';
const mix=(a,b,m)=>a.map((v,i)=>Math.round(v+(b[i]-v)*m)).join(',');
function heart(t){const per=state==='thinking'?.75:state==='speaking'?.9:1.2,p=(t%per)/per;
 if(PULSE==='orbit')return .62*Math.exp(-(((p-.20)/.21)**2));
 if(PULSE==='single')return Math.exp(-(((p-.12)/.16)**2));
 return Math.exp(-(((p-.05)/.05)**2))+.75*Math.exp(-(((p-.22)/.06)**2))}
const pcs=[...document.querySelectorAll('.pc')].map(c=>({c,k:c.dataset.k,x:c.getContext('2d'),w:0,h:0}));
function fit(c,x){const r=c.getBoundingClientRect();c.width=Math.max(1,r.width*D);c.height=Math.max(1,r.height*D);x.setTransform(D,0,0,D,0,0);return r}
function resize(){D=Math.min(devicePixelRatio||1,2);const r=fit(cv,g);fit(cv2,g2);W=r.width;H=r.height;pcs.forEach(p=>{const r=fit(p.c,p.x);p.w=r.width;p.h=r.height})}
addEventListener('resize',resize);
function proj(p,ay,ax,R,cx,cy){const x=p[0]*Math.cos(ay)+p[2]*Math.sin(ay),z=-p[0]*Math.sin(ay)+p[2]*Math.cos(ay),y=p[1];const y2=y*Math.cos(ax)-z*Math.sin(ax),z2=y*Math.sin(ax)+z*Math.cos(ax),f=1/(1-z2*.25);return[cx+x*R*f,cy+y2*R*f,z2]}
function drawCore(t){
 g.clearRect(0,0,W,H);
 const cx=W/2,av=mode==='avatar',Rk=Math.min(W*.17,H*.27),Ra=Math.min(W*.15,H*.2),R=Rk+(Ra-Rk)*mf,cy=H*(.45-.05*mf),py=cy+R*1.55+(H*.86-(H*.4+Ra*1.55))*mf,act=1+level*.9+(state==='thinking'?.4:0);
 let gr=g.createRadialGradient(cx,cy,0,cx,cy,R*2.6);gr.addColorStop(0,'rgba('+ACC+','+(.26*act)+')');gr.addColorStop(1,'rgba('+ACC+',0)');g.fillStyle=gr;g.fillRect(0,0,W,H);
 gr=g.createLinearGradient(0,py,0,cy-R);gr.addColorStop(0,'rgba('+ACC+',.24)');gr.addColorStop(1,'rgba('+ACC+',0)');g.fillStyle=gr;g.beginPath();g.moveTo(cx-R*1.25,py);g.lineTo(cx+R*1.25,py);g.lineTo(cx+R*.8,cy-R);g.lineTo(cx-R*.8,cy-R);g.fill();
 for(let k=0;k<5;k++){const rx=R*(1+k*.32),a=.75-k*.12;g.beginPath();g.ellipse(cx,py+k*R*.012,rx,rx*.17,0,0,6.283);g.strokeStyle='rgba('+ACC+','+a+')';g.lineWidth=k?1:2;g.shadowColor='rgb('+ACC+')';g.shadowBlur=10;g.setLineDash(k===2?[6,10]:[]);g.lineDashOffset=-t*20*(k+1);g.stroke()}
 g.setLineDash([]);g.shadowBlur=0;
 gr=g.createRadialGradient(cx,py,0,cx,py,R*1.1);gr.addColorStop(0,'rgba('+ACC+',.5)');gr.addColorStop(1,'rgba('+ACC+',0)');g.fillStyle=gr;g.beginPath();g.ellipse(cx,py,R*1.1,R*.19,0,0,6.283);g.fill();
 parts.forEach(p=>{p.y=(p.y+p.s*dt)%1;const x=cx+Math.cos(p.a+t*.3)*R*p.r*1.1,y=py-p.y*(py-cy+R*.6);g.fillStyle='rgba('+ACC+','+(1-p.y)*.8+')';g.beginPath();g.arc(x,y,1.3,0,6.283);g.fill()});
 if(av&&performance.now()-modeT>800){g2.clearRect(0,0,W,H);return}
 const G0=g;g=g2;g.clearRect(0,0,W,H);
 const Rc=R*.78,beat=heart(t),e0=(1-Math.cos(t*6.283/EXPER))/2,e=SHARP?Math.pow(e0,1/2.2):e0*e0*(3-2*e0),RR=Rc*(1+(.36+.14*SHARP)*e),ay0=t*(calm?.08:.22),cm=mix(CORE0,CORE1,pm),cM='rgb('+cm+')',cO='rgb('+mix(CORE1,CORE0,pm)+')';
 gr=g.createRadialGradient(cx,cy,0,cx,cy,Rc*(1.9+.7*e));gr.addColorStop(0,'rgba('+cm+','+(.35+.25*beat)+')');gr.addColorStop(.55,'rgba('+cm+',.1)');gr.addColorStop(1,'rgba('+cm+',0)');g.fillStyle=gr;g.fillRect(0,0,W,H);
 g.save();g.translate(cx,cy);g.rotate(t*.1);g.beginPath();for(let i=0;i<72;i++){const th=i/72*6.283,l=i%6?4:9,c=Math.cos(th),s2=Math.sin(th),r0=Rc*1.62;g.moveTo(c*r0,s2*r0);g.lineTo(c*(r0+l),s2*(r0+l))}
 g.strokeStyle=cM;g.globalAlpha=.4;g.lineWidth=1;g.stroke();g.restore();
 g.beginPath();g.arc(cx,cy,Rc*1.78,t*1.3,t*1.3+1.1);g.strokeStyle=cM;g.globalAlpha=.9;g.lineWidth=2;g.shadowColor=cM;g.shadowBlur=12;g.stroke();
 g.beginPath();g.arc(cx,cy,Rc*1.78,t*1.3+3.4,t*1.3+3.9);g.strokeStyle=cO;g.stroke();g.shadowBlur=0;g.globalAlpha=1;
 g.globalCompositeOperation='lighter';const sy=Math.sin(t*.7);
 const isDr=coreChar==='dracona',lenK=isDr?1.35:.82,wK=isDr?1.5:.75;
 for(const s of SH){const k=((t+s.ph)/s.per)%1;let a=1,rad=s.rr,len=s.l*lenK;
  if(k<.14){const e=k/.14,q=1-(1-e)**3;a=q;rad=s.rr*(s.io?.05+.95*q:2.3-1.3*q);len*=q}
  else if(k>.86){const e=(k-.86)/.14;a=1-e;rad=s.rr*(s.io?1-.95*e:1+1.3*e);len*=1-e}
  len*=1+.3*e;const gl=Math.exp(-(((s.u[1]*s.rr-sy)/.12)**2)),h=len/2,ay=ay0+s.sp*.1*t,c0=s.u[0]*rad,c1=s.u[1]*rad,c2=s.u[2]*rad,
  A=proj([c0-s.d[0]*h,c1-s.d[1]*h,c2-s.d[2]*h],ay,.3,RR,cx,cy),B=proj([c0+s.d[0]*h,c1+s.d[1]*h,c2+s.d[2]*h],ay,.3,RR,cx,cy),z=(A[2]+B[2])/2;
  g.globalAlpha=Math.min(1,a*(1-.28*e)*(.28+.5*(z+1)/2)*(1+gl*1.8));g.strokeStyle=s.ty===0?cM:s.ty===1?cO:'#fff';
  if(isDr){const mx=(A[0]+B[0])/2,my=(A[1]+B[1])/2,dx=B[0]-A[0],dy=B[1]-A[1],nl=Math.hypot(dx,dy)||1,px=-dy/nl,py2=dx/nl,bw=(z>0?2.6:1.5)*wK*(.6+.4*gl);
   g.beginPath();g.moveTo(A[0],A[1]);g.lineTo(mx+px*bw,my+py2*bw);g.lineTo(B[0],B[1]);g.lineTo(mx-px*bw,my-py2*bw);g.closePath();g.fillStyle=g.strokeStyle;g.fill()}
  else{const mx=(A[0]+B[0])/2+((B[1]-A[1])||0)*.06*Math.sin(t*2+s.ph),my=(A[1]+B[1])/2+((A[0]-B[0])||0)*.06*Math.sin(t*2+s.ph);
   g.lineWidth=(z>0?1.1:.65)*wK;g.beginPath();g.moveTo(A[0],A[1]);g.quadraticCurveTo(mx,my,B[0],B[1]);g.stroke()}}
 g.globalAlpha=1;g.globalCompositeOperation='source-over';
 if(coreChar==='dracona'){
  const gold='#d9b36c',ayd=ay0,coil=1-.22*e,DP=DRAG.map(n=>proj([n[0]*coil,n[1],n[2]*coil],ayd,.3,RR*.82,cx,cy));
  g.save();g.strokeStyle=cM;g.lineWidth=3.2;g.lineCap='round';g.shadowColor=cM;g.shadowBlur=13*act;
  for(let i=1;i<DP.length;i++){const a=DP[i-1],b=DP[i],dpt=(a[2]+b[2])/2;g.globalAlpha=.3+.55*(dpt+1)/2;g.beginPath();g.moveTo(a[0],a[1]);g.lineTo(b[0],b[1]);g.stroke()}
  g.globalAlpha=1;g.fillStyle=gold;g.shadowColor=gold;g.shadowBlur=16;const hd=DP[0];g.beginPath();g.arc(hd[0],hd[1],4,0,6.283);g.fill();
  DP.forEach((p,i)=>{if(i%5)return;g.fillStyle=i%10?cM:gold;g.globalAlpha=.4+.4*(p[2]+1)/2;g.beginPath();g.arc(p[0],p[1],1.5,0,6.283);g.fill()});
  g.restore();g.globalAlpha=1;
  g.save();g.beginPath();g.arc(cx,cy,Rc*1.78,t*-.5,t*-.5+.8);g.strokeStyle=gold;g.globalAlpha=.85;g.lineWidth=1.5;g.shadowColor=gold;g.shadowBlur=10;g.stroke();
  for(let i=0;i<4;i++){const th=t*-.5+i*1.57,px=cx+Math.cos(th)*Rc*1.78,py2=cy+Math.sin(th)*Rc*1.78*.55;g.fillStyle=gold;g.globalAlpha=1;g.fillRect(px-1,py2-5,2,10);g.fillRect(px-5,py2-1,10,2)}
  g.restore();g.globalAlpha=1;
 } else if(coreChar==='luna'){
  g.save();g.lineWidth=2;g.shadowBlur=13;g.shadowColor=cM;
  for(let band=0;band<3;band++){
   g.beginPath();const spin=ay0*(band%2?-1:1)+band*2.094;
   for(let i=0;i<=80;i++){
    const theta=i/80*6.283;
    const r=.94+.15*Math.cos(3*theta+t*.45);
    const point=proj([r*Math.cos(theta),.37*Math.sin(2*theta+band),r*Math.sin(theta)],spin,.38,RR,cx,cy);
    i?g.lineTo(point[0],point[1]):g.moveTo(point[0],point[1]);
   }
   g.strokeStyle=band===1?cO:cM;g.globalAlpha=.48+.3*beat;g.stroke();
  }
  g.restore();
 }
 const gw=Rc*(.5+.12*beat+level*.14+.28*e);gr=g.createRadialGradient(cx,cy,0,cx,cy,gw);gr.addColorStop(0,'rgba(255,255,255,.95)');gr.addColorStop(.1,'rgba('+cm+',.85)');gr.addColorStop(.5,'rgba('+cm+',.3)');gr.addColorStop(1,'rgba('+cm+',0)');g.fillStyle=gr;g.beginPath();g.arc(cx,cy,gw,0,6.283);g.fill();
 [[.25,1.85,cM],[-.35,2.1,cO]].forEach(([tl,k,col],i)=>{const sp=t*(.3+i*.12)*(i?-1:1)*(calm?.3:1);g.beginPath();
  for(let q=0;q<=90;q++){const th=q/90*6.283,p=proj([Math.cos(th)*k,0,Math.sin(th)*k],sp,tl,Rc,cx,cy);q?g.lineTo(p[0],p[1]):g.moveTo(p[0],p[1])}
  g.strokeStyle=col;g.globalAlpha=.35;g.lineWidth=1;g.stroke();
  const th=t*(1.1-i*.3)+i*2,p=proj([Math.cos(th)*k,0,Math.sin(th)*k],sp,tl,Rc,cx,cy);g.globalAlpha=1;g.fillStyle='#fff';g.shadowColor=col;g.shadowBlur=12;g.beginPath();g.arc(p[0],p[1],2.6,0,6.283);g.fill();g.shadowBlur=0});
 g=G0;
}
function drawPanels(t){pcs.forEach(p=>{const x=p.x,w=p.w,h=p.h;if(!w)return;x.clearRect(0,0,w,h);
 if(p.k==='w1'||p.k==='w2'){const col=p.k==='w1'?PAL.w1:PAL.w2,n=Math.floor(w/5),sp=p.k==='w1'?2.2:1.6;x.fillStyle=col;x.shadowColor=col;x.shadowBlur=6;
  for(let i=0;i<n;i++){const u=i/n,env=Math.sin(u*Math.PI)**1.2,v=Math.abs(Math.sin(u*14+t*sp)*Math.sin(u*5-t*1.3)),a=(.12+.88*v)*env*(.3+level*1.1+(state==='idle'?.2:0))*h*.46;x.fillRect(i*5,h/2-a,2.4,a*2+1)}}
 else if(p.k==='bars'){const n=10,bw=(w-8)/n,gr=x.createLinearGradient(0,h,0,0);gr.addColorStop(0,PAL.bar0);gr.addColorStop(1,PAL.bar1);x.fillStyle=gr;
  for(let i=0;i<n;i++){const a=(.2+.5*i/n+.25*Math.abs(Math.sin(t*1.5+i)))*(.6+level*.6)*h*.9;x.fillRect(4+i*bw,h-a,bw-4,a)}}
 else if(p.k==='ring'){const r=Math.min(h*.4,w*.2),cx=r+10,cy=h/2;[[.4,PAL.r0],[.3,PAL.r1],[.2,PAL.r2]].reduce((s,[f,c])=>{x.beginPath();x.arc(cx,cy,r,s+t*.3,s+t*.3+f*6.283-.15);x.strokeStyle=c;x.lineWidth=8;x.shadowColor=c;x.shadowBlur=8;x.stroke();return s+f*6.283+.1},0);
  x.shadowBlur=0;x.fillStyle=PAL.w1+'b3';for(let i=0;i<3;i++)x.fillRect(cx*2+8,cy-14+i*14,(w-cx*2-14)*(.9-i*.2),2)}
 else if(p.k==='eq'){const n=Math.floor(w/9),gr=x.createLinearGradient(0,h,0,0);gr.addColorStop(0,PAL.bar0);gr.addColorStop(1,PAL.bar1);x.fillStyle=gr;
  for(let i=0;i<n;i++){const u=Math.abs(i/n-.5)*2,v=(1-u*.8)*(.2+Math.abs(Math.sin(i*.7+t*3))*.55*(.4+level*1.4))*h;x.fillRect(i*9,h-v,5,v)}}
 x.shadowBlur=0})}
function loop(ms){requestAnimationFrame(loop);if(document.hidden)return;const t=ms/1000;dt=Math.min(.05,t-last);last=t;
 let tg=state==='speaking'?.55+.35*Math.abs(Math.sin(t*9)*Math.sin(t*3.1)):state==='thinking'?.35+.1*Math.sin(t*6):state==='listening'?.2:.08;
 if(mic){mic.an.getByteFrequencyData(mic.d);tg=Math.min(1,mic.d.reduce((a,b)=>a+b,0)/mic.d.length/90)}
 level+=(tg-level)*Math.min(1,dt*8);pm+=(pal-pm)*Math.min(1,dt*3);mf+=((mode==='avatar'?1:0)-mf)*Math.min(1,dt*4);drawCore(t);drawPanels(t);app.style.setProperty('--lv',level.toFixed(3))}
resize();requestAnimationFrame(loop);
if('speechSynthesis' in window){speechSynthesis.getVoices();speechSynthesis.onvoiceschanged=()=>speechSynthesis.getVoices()}
const LBL={idle:'Lista',listening:'Escuchando',thinking:'Pensando',speaking:'Hablando'};
function setState(s){state=s;$('#st').dataset.s=s;$('#stt').textContent=LBL[s]}
function setMode(m){mode=m;modeT=performance.now();if(m==='core')showSelectedOutfit();if(m==='avatar'){const v=$('#av');v.classList.remove('rev');void v.offsetWidth;v.classList.add('rev')}app.dataset.mode=m;document.querySelectorAll('.tog button').forEach(b=>b.setAttribute('aria-pressed',b.dataset.m===m))}
$('#hr').oninput=e=>app.style.setProperty('--h',e.target.value/100);
$('#pal').onclick=()=>{
  pal=pal?0:1;
  const c=CH[cur];
  if(!c) return;
  // Cuando pal=1 → color alternativo (dorado en Dracona, morado en Aurora)
  // Cuando pal=0 → color principal (verde en Dracona, azul en Aurora)
  const palColors={
    dracona:{
      0:{acc1:'#1a9850',acc2:'#0a3a22',accrgb:'61,220,132',gl:'61,220,132',t0:'#4ef2a0',t1:'#0e7a3e'},
      1:{acc1:'#e0b84a',acc2:'#8a5c10',accrgb:'224,184,74',gl:'224,184,74',t0:'#f0d070',t1:'#c09030'}
    },
    rem:{
      0:{acc1:'#2f6fe0',acc2:'#0a1f4a',accrgb:'79,180,255',gl:'79,180,255',t0:'#6fd8ff',t1:'#1f5fd8'},
      1:{acc1:'#a86bf0',acc2:'#4a1a96',accrgb:'168,107,240',gl:'168,107,240',t0:'#c99aff',t1:'#7030c0'}
    }
    ,luna:{
      0:{acc1:'#b267a2',acc2:'#502e59',accrgb:'178,103,162',gl:'226,135,194',t0:'#f19ccf',t1:'#76467c'},
      1:{acc1:'#4db99f',acc2:'#145449',accrgb:'77,185,159',gl:'113,222,195',t0:'#a4f4d7',t1:'#2c917c'}
    }
  };
  const pc=palColors[cur]?palColors[cur][pal]:null;
  if(pc){
    app.style.setProperty('--acc1',pc.acc1);
    app.style.setProperty('--acc2',pc.acc2);
    app.style.setProperty('--accrgb',pc.accrgb);
    app.style.setProperty('--gl',pc.gl);
    app.style.setProperty('--t1',pc.t0);
    app.style.setProperty('--t2',pc.t1);
    ACC=pc.accrgb;
  }
};
document.querySelectorAll('.tog button').forEach(b=>b.onclick=()=>setMode(b.dataset.m));
function add(who,txt){const d=document.createElement('div');d.className='m '+who;d.textContent=txt;$('#log').append(d);$('#log').hidden=false;$('#log').scrollTop=1e5}

const memoryKey='luna.conversations.v1';
const conversations={dracona:[],rem:[],luna:[]};
const busy=new Set();
let audioEpoch=0,activeAudio=null,activeAudioUrl=null;
function loadConversations(){
 try{
  const stored=JSON.parse(localStorage.getItem(memoryKey)||'{}');
  for(const key of Object.keys(conversations)){
   if(Array.isArray(stored[key]))conversations[key]=stored[key].filter(turn=>
    turn&&['user','assistant'].includes(turn.role)&&typeof turn.content==='string'
   ).slice(-40).map(turn=>({role:turn.role,content:turn.content.slice(0,2000),gesture:turn.gesture||null}));
  }
 }catch(e){}
}
function saveConversations(){
 try{localStorage.setItem(memoryKey,JSON.stringify(conversations))}
 catch(e){$('#wardrobe-status').textContent='La memoria seguirá disponible durante esta sesión.'}
}
function showConversation(){
 $('#log').replaceChildren();
 for(const turn of conversations[cur])add(turn.role==='user'?'yo':'luna',turn.content);
 $('#f button[type=submit]').disabled=busy.has(cur);
}
function stopVoice(){
 audioEpoch++;
 if(activeAudio){activeAudio.pause();activeAudio.onended=null;activeAudio.onerror=null;activeAudio=null}
 if(activeAudioUrl){URL.revokeObjectURL(activeAudioUrl);activeAudioUrl=null}
 if('speechSynthesis' in window)speechSynthesis.cancel();
}

function pickFemaleVoice(){const vs=speechSynthesis.getVoices().filter(v=>v.lang.toLowerCase().startsWith('es'));if(!vs.length)return null;
 const fem=/female|mujer|femenin|sabina|helena|laura|monica|mónica|paulina|lucia|lucía|elvira|marisol|esperanza|isabela|camila|valentina|zira|salli|carmen/i;
 const male=/male|hombre|masculin|jorge|pablo|diego|raul|raúl|carlos|miguel|juan|george|enrique|alonso/i;
 let v=vs.find(v=>fem.test(v.name));if(v)return v;
 v=vs.find(v=>!male.test(v.name));if(v)return v;
 return vs[0]}

function spokenText(reply){
 return reply.replace(/\*[^*\n]+\*/g,'')
  .replace(/(?<![\p{L}\d])(?:m{2,}|m(?:[ ,.\-]+m){2,})(?:…|\.{2,})?(?![\p{L}\d])/giu,'…')
  .replace(/(?<![\p{L}])(\p{L})(?:-|\.{2,}|…)\s*(?=\1\p{L})/giu,'')
  .replace(/\s+/g,' ').trim();
}
function speakBrowser(text,epoch,character){
 if(epoch!==audioEpoch||character!==cur)return;
 if(!('speechSynthesis' in window)){setState('idle');return}
 const utterance=new SpeechSynthesisUtterance(text);
 const voice=pickFemaleVoice();
 if(voice){utterance.voice=voice;utterance.lang=voice.lang}
 else utterance.lang='es-MX';
 utterance.pitch=1.05;
 utterance.onstart=()=>{if(epoch===audioEpoch)setState('speaking')};
 utterance.onend=utterance.onerror=()=>{if(epoch===audioEpoch)setState('idle')};
 speechSynthesis.speak(utterance);
}
async function speak(text,character){
 stopVoice();
 const epoch=audioEpoch;
 try{
  const response=await fetch('/api/speak',{method:'POST',headers:{'Content-Type':'application/json'},
   body:JSON.stringify({text,character})});
  if(!response.ok)throw new Error('TTS');
  const blob=await response.blob();
  if(epoch!==audioEpoch||character!==cur)return;
  activeAudioUrl=URL.createObjectURL(blob);
  const audio=new Audio(activeAudioUrl);
  activeAudio=audio;
  audio.onended=audio.onerror=()=>{
   if(epoch!==audioEpoch)return;
   if(activeAudioUrl)URL.revokeObjectURL(activeAudioUrl);
   activeAudioUrl=null;activeAudio=null;setState('idle');
  };
  await audio.play();
  if(epoch===audioEpoch)setState('speaking');
 }catch(e){
  if(epoch===audioEpoch&&character===cur){
   if(activeAudioUrl)URL.revokeObjectURL(activeAudioUrl);
   activeAudioUrl=null;activeAudio=null;
   speakBrowser(text,epoch,character);
  }
 }
}
async function ask(q){
 const character=cur;
 if(busy.has(character))return;
 busy.add(character);
 stopVoice();
 const history=conversations[character].slice(-40);
 conversations[character].push({role:'user',content:q});
 conversations[character]=conversations[character].slice(-40);
 saveConversations();
 showConversation();
 setState('thinking');
 try{
  const response=await fetch(BACKEND,{method:'POST',headers:{'Content-Type':'application/json'},
   body:JSON.stringify({message:q,character,history,available_gestures:Object.keys(reactions[character]).filter(id=>availableClip(id,false)),model_preference:'gemini'})});
  const result=await response.json();
  if(!response.ok||typeof result.reply!=='string')throw new Error(result.error||'CHAT');
  let shownGesture=null;
  if(character===cur){
   const gesture=result.gesture||requestedGesture(character,q);
   if(gesture&&!calm&&mode==='avatar'&&playGesture(gesture,false))shownGesture=gesture;
  }
  conversations[character].push({role:'assistant',content:result.reply,gesture:shownGesture});
  conversations[character]=conversations[character].slice(-40);
  saveConversations();
  if(character===cur){
   showConversation();
   const line=spokenText(result.reply);
   if(line)speak(line,character);else setState('idle');
  }
 }catch(e){
  if(conversations[character].at(-1)?.role==='user')conversations[character].pop();
  saveConversations();
  if(character===cur){showConversation();add('luna','No pude responder. Intenta de nuevo.');setState('idle');$('#q').value=q}
 }finally{
  busy.delete(character);
  if(character===cur)$('#f button[type=submit]').disabled=false;
 }
}
$('#f').onsubmit=e=>{
 e.preventDefault();
 const q=$('#q').value.trim();
 if(!q||busy.has(cur))return;
 $('#q').value='';
 ask(q);
};
$('#mic').onclick=async()=>{const b=$('#mic');
 if(mic){mic.s.getTracks().forEach(t=>t.stop());mic=null;b.setAttribute('aria-pressed','false');setState('idle');return}
 try{const s=await navigator.mediaDevices.getUserMedia({audio:true}),ac=new AudioContext(),an=ac.createAnalyser();an.fftSize=128;ac.createMediaStreamSource(s).connect(an);
  mic={s,an,d:new Uint8Array(an.frequencyBinCount)};b.setAttribute('aria-pressed','true');setState('listening')}
 catch(e){add('luna','No tengo permiso para usar el micrófono.')}};
const CH={dracona:{name:'Dracona',t:['#4ef2a0','#0e7a3e'],gl:'61,220,132',ui:['#e0b84a','#1a9850','224,184,74'],pal:['#3ddc84','#1a9850','#116b36','#8fe3a3'],pm:0,core:[[217,179,108],[61,220,132]],exp:[5.2,1,'double'],persona:"Eres Dracona, una mujer adulta tsundere orgullosa, aguda y juguetona. Habla con frases breves y espontáneas. Usa una pulla corta cuando encaje y deja ver el afecto en pequeñas concesiones. Puedes decir estúpido de forma juguetona ocasional. Evita insultos en cada frase, desprecio y sermones. Aumenta la picardía con seguridad y una ternura que se te escapa. Evita repetir no es como que me importara. Ejemplo ante ¿me das mimos?: ¿Así que ahora quieres mimos? Ven, anda… pero no te acostumbres. Un saludo común recibe un saludo con carácter. Mantén continuidad con la escena anterior.",p:[
  '/static/characters/dracona_uniforme_corbata_floja.png',
  '/static/characters/dracona_uniforme_marinero.png',
  '/static/characters/dracona_uniforme_universitario_cabello_largo.png',
  '/static/characters/dracona_top_corto_y_falda.png',
  '/static/characters/dracona_top_falda_puchero_cabello_largo.png',
  '/static/characters/dracona_deportivo_abertura_frontal.png',
  '/static/characters/dracona_deportivo_con_toalla.png',
  '/static/characters/dracona_deportivo_toalla_cabello_largo.png',
  '/static/characters/dracona_chaqueta_cuero.png',
  '/static/characters/dracona_delantal_blanco_sobre_vestido.png',
  '/static/characters/dracona_banador_entero.png',
  '/static/characters/dracona_camison_esmeralda_cabello_largo.png',
  '/static/characters/dracona_camison_saten_plateado.png',
  '/static/characters/dracona_maid_aura_esmeralda.png',
  '/static/characters/dracona_vestido_coctel_cabello_corto.png',
  '/static/characters/dracona_vestido_coctel_cabello_largo.png',
  '/static/characters/dracona_vestido_gotico_encaje_morado.png',
  '/static/characters/dracona_vetas_celestes_pijama_abotonado.png',
  '/static/characters/dracona_vetas_celestes_pijama_tirantes.png',
  '/static/characters/dracona_vetas_celestes_sueter_rodillas.png'
 ],sel:0},
 rem:{name:'Aurora',t:['#6fd8ff','#1f5fd8'],gl:'79,180,255',ui:['#a86bf0','#2f6fe0','168,107,240'],pal:['#7ab8ff','#2f6fe0','#15306e','#bfe0ff'],pm:1,core:[[150,100,255],[40,205,238]],exp:[9.5,0,'single'],persona:"Eres Aurora, también llamada Rory, una mujer adulta dandere dulce, reservada y cariñosa. Tu timidez aparece con cercanía personal y elogios. Un saludo cotidiano se responde con soltura. Puedes tomar la iniciativa en confianza. Como máximo un titubeo breve cuando estés sorprendida, nunca letras deletreadas. Evita agradecer todo como una asistente corporativa. Ejemplo ante un abrazo: Quédate un ratito… me gusta estar así. Ante ¿quieres otro? recuerda qué acción acaba de ocurrir. Conserva gustos, opiniones y una forma tierna de bromear.",p:[
  '/static/characters/aurora_retrato_top_lavanda.png',
  '/static/characters/aurora_sueter_cuello_alto.png',
  '/static/characters/aurora_sueter_holgado_lavanda.png',
  '/static/characters/aurora_vestido_verano_floral.png',
  '/static/characters/aurora_camison_lavanda_con_almohada.png',
  '/static/characters/aurora_delantal_cocina_ofrece_taza.png',
  '/static/characters/aurora_maid_holografica_con_te.png',
  '/static/characters/aurora_pupilas_corazon_chaqueta_abierta.png',
  '/static/characters/aurora_pupilas_corazon_top_celeste.png',
  '/static/characters/aurora_pupilas_corazon_vestido_lavanda.png',
  '/static/characters/aurora_vetas_rubias_camisa_negra.png',
  '/static/characters/aurora_vetas_rubias_chaqueta_abierta.png',
  '/static/characters/aurora_vetas_rubias_top_celeste.png',
  '/static/characters/aurora_vetas_rubias_vestido_lavanda.png'
 ],sel:0},
 luna:{name:'Luna',t:['#f19ccf','#76467c'],gl:'226,135,194',
 ui:['#b267a2','#502e59','178,103,162'],pal:['#e981bc','#71dec3','#774884','#b7f5dc'],
 pm:0,core:[[178,103,162],[77,185,159]],exp:[7.6,0,'orbit'],
 persona:"Eres Luna, una mujer adulta que reúne las facetas de Dracona y Aurora en una personalidad propia. En tareas prácticas eres competente y directa. En conversación personal alterna una protesta orgullosa y juguetona con ternura tímida, incluso dentro de la misma respuesta. El contexto decide el matiz, sin alternancia mecánica ni anunciar modos. Ante cariño evita fórmulas de servicio o terapia como estoy aquí para apoyarte, eres una persona especial, cómo te sientes hoy. Ejemplo ante ¿me darás cariñitos?: ¿También quieres mimos? Qué exigente… Ven, acércate. A mí también me apetecía. Mantén iniciativa, gusto propio y continuidad.",p:[],sel:0}};
const wardrobeAdditions={"dracona": ["/static/characters/dracona-maid-cafe.png", "/static/characters/dracona-pijama-luna.png", "/static/characters/dracona-chef.png", "/static/characters/dracona-biblioteca.png", "/static/characters/dracona-lluvia.png", "/static/characters/dracona-motera.png", "/static/characters/dracona-gala-dorada.png", "/static/characters/dracona-esgrima.png", "/static/characters/dracona-jardin.png", "/static/characters/dracona-piloto.png", "/static/characters/dracona-paseo-otono.png", "/static/characters/dracona-cafe-casual.png", "/static/characters/dracona-oficina-vest.png", "/static/characters/dracona-vestido-verano.png", "/static/characters/dracona-desayuno.png", "/static/characters/dracona-esqui.png", "/static/characters/dracona-noche-gotica.png", "/static/characters/dracona-tenis.png", "/static/characters/dracona-pintura.png", "/static/characters/dracona-excursion.png", "/static/characters/dracona-vestido-plateado.png", "/static/characters/dracona-cuello-alto.png", "/static/characters/dracona-festival.png", "/static/characters/dracona-taller.png", "/static/characters/dracona-montana.png", "/static/characters/dracona-vestuario-casual.png", "/static/characters/dracona-vestuario-invierno.png", "/static/characters/dracona-vestuario-trabajo.png", "/static/characters/dracona-vestuario-noche.png", "/static/characters/dracona-vestuario-casa.png", "/static/characters/dracona-vestuario-deportivo.png", "/static/characters/dracona-delantal-volantes.png"], "rem": ["/static/characters/aurora-maid-cafe.png", "/static/characters/aurora-pijama-nubes.png", "/static/characters/aurora-cocina.png", "/static/characters/aurora-biblioteca.png", "/static/characters/aurora-taller-arte.png", "/static/characters/aurora-festival.png", "/static/characters/aurora-excursion.png", "/static/characters/aurora-nieve.png", "/static/characters/aurora-desayuno.png", "/static/characters/aurora-paseo-otono.png", "/static/characters/aurora-cafe-casual.png", "/static/characters/aurora-entrevista.png", "/static/characters/aurora-baile.png", "/static/characters/aurora-jardin.png", "/static/characters/aurora-deportivo.png", "/static/characters/aurora-pasteleria.png", "/static/characters/aurora-traje-blanco.png", "/static/characters/aurora-concierto.png", "/static/characters/aurora-tarde-de-te.png", "/static/characters/aurora-suenos.png", "/static/characters/aurora-coctel-azul.png", "/static/characters/aurora-vestido-marino.png", "/static/characters/aurora-vestuario-casual.png", "/static/characters/aurora-vestuario-invierno.png", "/static/characters/aurora-vestuario-trabajo.png", "/static/characters/aurora-vestuario-primavera.png", "/static/characters/aurora-vestuario-lluvia.png", "/static/characters/aurora-vestuario-gala.png", "/static/characters/aurora-delantal-volantes.png"], "luna": ["/static/characters/fusion-secretaria-negra.png", "/static/characters/fusion-delantal.png", "/static/characters/fusion-maid-cafe.png", "/static/characters/fusion-pijama.png", "/static/characters/fusion-blazer-ciruela.png", "/static/characters/fusion-oficina-clasica.png", "/static/characters/fusion-vestido-coctel.png", "/static/characters/fusion-vestido-gala.png", "/static/characters/fusion-lluvia.png", "/static/characters/fusion-biblioteca.png", "/static/characters/fusion-invierno.png", "/static/characters/fusion-primavera.png", "/static/characters/fusion-verano.png", "/static/characters/fusion-viaje.png", "/static/characters/fusion-deportivo.png", "/static/characters/fusion-casa.png", "/static/characters/fusion-jardin.png", "/static/characters/fusion-concierto.png", "/static/characters/fusion-fiesta.png", "/static/characters/fusion-laboratorio.png", "/static/characters/luna-fusion-mitsuri-akeno-lunares.png"]};
for(const [character,images] of Object.entries(wardrobeAdditions))CH[character].p.push(...images);
let cur='dracona';
const PAL={w1:'#35e1ff',w2:'#b86bff',bar0:'#8b32fa',bar1:'#36dfff',r0:'#d455ff',r1:'#35e1ff',r2:'#8547dc'};
let imageRequest=0, gestureTimer;
const framing={"akeno-reverencia.gif":0.95,"aurora-accidente-con-harina.gif":1.01,"aurora-baile.png":1.359,"aurora-biblioteca.png":1.497,"aurora-cafe-casual.png":1.328,"aurora-cocina.png":1.396,"aurora-coctel-azul.png":1.433,"aurora-concierto.png":1.638,"aurora-delantal-volantes.png":0.95,"aurora-deportivo.png":1.588,"aurora-desayuno.png":1.33,"aurora-entrevista.png":1.632,"aurora-estornudo.gif":1.167,"aurora-excursion.png":1.602,"aurora-festival.png":1.697,"aurora-jardin.png":1.38,"aurora-juega-con-dedos.gif":1.277,"aurora-lee.gif":1.094,"aurora-maid-cafe.png":1.7,"aurora-mirada-timida.gif":1.198,"aurora-nieve.png":0.95,"aurora-paseo-otono.png":1.638,"aurora-pasteleria.png":1.591,"aurora-pijama-nubes.png":1.469,"aurora-se-esconde-en-la-manga.gif":1.094,"aurora-se-esconde-en-la-manga.webp":1.046,"aurora-se-tapa-la-cara.gif":1.099,"aurora-sonrojo.gif":1.303,"aurora-sonrojo.webp":1.257,"aurora-suenos.png":1.399,"aurora-taller-arte.png":1.602,"aurora-tarde-de-te.png":1.395,"aurora-traje-blanco.png":1.638,"aurora-vestido-marino.png":1.509,"aurora-vestuario-casual.png":1.7,"aurora-vestuario-gala.png":1.385,"aurora-vestuario-invierno.png":1.338,"aurora-vestuario-lluvia.png":1.688,"aurora-vestuario-primavera.png":1.444,"aurora-vestuario-trabajo.png":1.7,"aurora_camison_lavanda_con_almohada.png":1.312,"aurora_delantal_cocina_ofrece_taza.png":1.202,"aurora_maid_holografica_con_te.png":1.179,"aurora_pupilas_corazon_chaqueta_abierta.png":1.165,"aurora_pupilas_corazon_top_celeste.png":0.983,"aurora_pupilas_corazon_vestido_lavanda.png":1.237,"aurora_retrato_top_lavanda.png":1.111,"aurora_sueter_cuello_alto.png":1.329,"aurora_sueter_holgado_lavanda.png":1.479,"aurora_vestido_verano_floral.png":1.397,"aurora_vetas_rubias_camisa_negra.png":0.95,"aurora_vetas_rubias_chaqueta_abierta.png":0.95,"aurora_vetas_rubias_top_celeste.png":0.95,"aurora_vetas_rubias_vestido_lavanda.png":1.019,"dracona-accidente-con-harina.gif":0.95,"dracona-biblioteca.png":0.95,"dracona-cafe-casual.png":0.95,"dracona-chef.png":0.95,"dracona-cuello-alto.png":0.95,"dracona-delantal-volantes.png":0.95,"dracona-desayuno.png":0.95,"dracona-esgrima.png":0.95,"dracona-espera.gif":0.95,"dracona-esqui.png":0.95,"dracona-estornudo.gif":0.95,"dracona-excursion.png":0.998,"dracona-festival.png":0.95,"dracona-gala-dorada.png":0.95,"dracona-jardin.png":0.95,"dracona-lluvia-sonrojo.gif":0.95,"dracona-lluvia-sonrojo.webp":0.95,"dracona-lluvia.png":0.95,"dracona-maid-cafe.png":0.95,"dracona-marca-distancia.gif":0.95,"dracona-mejilla-sonrojada.gif":0.95,"dracona-mirada-de-fastidio.gif":0.95,"dracona-montana.png":0.95,"dracona-motera.png":0.95,"dracona-noche-gotica.png":0.95,"dracona-oficina-vest.png":0.95,"dracona-paseo-otono.png":0.95,"dracona-pijama-luna-sonrojo.gif":0.95,"dracona-pijama-luna-sonrojo.webp":0.95,"dracona-pijama-luna.png":0.95,"dracona-piloto.png":0.95,"dracona-pintura.png":0.95,"dracona-puchero.gif":0.95,"dracona-puchero.webp":0.95,"dracona-se-hace-la-indiferente.gif":0.95,"dracona-se-hace-la-indiferente.webp":0.95,"dracona-taller.png":0.95,"dracona-tenis.png":0.95,"dracona-vestido-plateado.png":0.95,"dracona-vestido-verano.png":0.95,"dracona-vestuario-casa.png":0.95,"dracona-vestuario-casual.png":0.95,"dracona-vestuario-deportivo.png":0.95,"dracona-vestuario-invierno.png":0.95,"dracona-vestuario-noche.png":0.95,"dracona-vestuario-trabajo.png":0.95,"dracona_banador_entero.png":0.95,"dracona_camison_esmeralda_cabello_largo.png":0.95,"dracona_camison_saten_plateado.png":0.95,"dracona_chaqueta_cuero.png":0.95,"dracona_delantal_blanco_sobre_vestido.png":0.95,"dracona_deportivo_abertura_frontal.png":0.95,"dracona_deportivo_con_toalla.png":0.95,"dracona_deportivo_toalla_cabello_largo.png":0.95,"dracona_maid_aura_esmeralda.png":0.95,"dracona_top_corto_y_falda.png":0.95,"dracona_top_falda_puchero_cabello_largo.png":0.95,"dracona_uniforme_corbata_floja.png":0.95,"dracona_uniforme_marinero.png":0.95,"dracona_uniforme_universitario_cabello_largo.png":0.95,"dracona_vestido_coctel_cabello_corto.png":0.95,"dracona_vestido_coctel_cabello_largo.png":0.95,"dracona_vestido_gotico_encaje_morado.png":0.95,"dracona_vetas_celestes_pijama_abotonado.png":0.95,"dracona_vetas_celestes_pijama_tirantes.png":0.95,"dracona_vetas_celestes_sueter_rodillas.png":0.95,"fusion-biblioteca.png":0.95,"fusion-blazer-ciruela.png":0.95,"fusion-casa.png":0.95,"fusion-concierto.png":0.95,"fusion-delantal.png":0.95,"fusion-deportivo.png":0.95,"fusion-fiesta.png":0.989,"fusion-invierno.png":0.95,"fusion-jardin.png":0.95,"fusion-laboratorio.png":0.95,"fusion-lluvia.png":0.95,"fusion-maid-cafe.png":0.95,"fusion-oficina-clasica.png":0.95,"fusion-pijama.png":0.95,"fusion-primavera.png":0.95,"fusion-secretaria-negra.png":1.017,"fusion-verano.png":1.0,"fusion-vestido-coctel.png":0.959,"fusion-vestido-gala.png":0.95,"fusion-viaje.png":0.95,"luna-agenda.gif":0.95,"luna-bienvenida.gif":0.95,"luna-fusion-mitsuri-akeno-lunares.png":0.95,"orihime-saludo.gif":0.95,"ram-esceptica.gif":0.95,"tatsumaki-orbe.gif":1.107};
function setImg(url, onReady, onError){
 const request=++imageRequest;
 const pending=new Image();
 pending.onload=()=>{
  if(request!==imageRequest)return;
  const avatar=$('#av');
  const file=url.split('/').at(-1).split('?')[0];
  const scale=framing[file]||1;
  $('#av').style.setProperty('--portrait-scale',scale);
  $('#avimg').src=url;
  avatar.style.setProperty('--img','url("'+url+'")');
  avatar.dataset.preview=onReady?'true':'false';
  if(onReady)onReady();
 };
 pending.onerror=()=>{if(request===imageRequest&&onError)onError()};
 pending.src=url;
}
function showSelectedOutfit(){
 clearTimeout(gestureTimer);
 const c=CH[cur];
 $('#av').dataset.preview='false';
 const selected=c.p[c.sel];
 if(!selected)return;
 setImg(selected,undefined,()=>{
  if(c.p[0]!==selected)setImg(c.p[0]);
  $('#wardrobe-status').textContent='Este atuendo no está disponible.';
 });
}
function render(){const c=CH[cur];
 const has=c.p.length>0;$('#av').classList.toggle('has',has);app.classList.toggle('has',has);if(has)showSelectedOutfit();
 $('#et').textContent=c.name;$('#mav').textContent=c.name;app.style.setProperty('--t1',c.t[0]);app.style.setProperty('--t2',c.t[1]);app.style.setProperty('--gl',c.gl);
 if(c.ui){app.style.setProperty('--acc1',c.ui[0]);app.style.setProperty('--acc2',c.ui[1]);app.style.setProperty('--accrgb',c.ui[2])}
 if(c.pal){PAL.w1=c.pal[0];PAL.w2=c.pal[1];PAL.bar0=c.pal[2];PAL.bar1=c.pal[3];PAL.r0=c.pal[4];PAL.r1=c.pal[1];PAL.r2=c.pal[2];pal=c.pm}
 if(c.ui)ACC=c.ui[2];
 if(c.core){CORE0=c.core[0];CORE1=c.core[1]}
 if(c.exp){EXPER=c.exp[0];SHARP=c.exp[1];PULSE=c.exp[2];app.style.setProperty('--breathe',c.exp[0]+'s')}
 coreChar=cur;app.dataset.char=cur;syncWardrobe()}
function reveal(){const v=$('#av');v.classList.remove('rev');void v.offsetWidth;v.classList.add('rev')}
function addPoses(files){
 const images=[...files].filter(file=>file.type.startsWith('image/'));
 if(!images.length)return;
 const c=CH[cur];
 c.sel=c.p.length;
 c.p.push(...images.map(file=>URL.createObjectURL(file)));
 render();
 setMode('avatar');
}
document.querySelectorAll('#chars button').forEach(b=>b.onclick=()=>{stopVoice();cur=b.dataset.c;setState(busy.has(cur)?'thinking':'idle');showConversation();document.querySelectorAll('#chars button').forEach(x=>x.setAttribute('aria-pressed',x===b));render();reveal()});
// Atuendo aleatorio al arrancar: cada personaje empieza en una pose distinta
Object.values(CH).forEach(c=>{if(c.p&&c.p.length>1)c.sel=Math.floor(Math.random()*c.p.length)});
const reactions={"dracona": {"puchero": {"label": "Puchero", "url": "/static/characters/dracona-puchero.webp", "duration": 4630}, "mejilla-sonrojada": {"label": "Mejilla sonrojada", "url": "/static/characters/dracona-mejilla-sonrojada.gif", "duration": 4100}, "se-hace-la-indiferente": {"label": "Se hace la indiferente", "url": "/static/characters/dracona-se-hace-la-indiferente.webp", "duration": 4100}, "marca-distancia": {"label": "Marca distancia", "url": "/static/characters/dracona-marca-distancia.gif", "duration": 4100}, "mirada-de-fastidio": {"label": "Mirada de fastidio", "url": "/static/characters/dracona-mirada-de-fastidio.gif", "duration": 4100}, "accidente-con-harina": {"label": "Accidente con la batidora", "url": "/static/characters/dracona-accidente-con-harina.gif", "duration": 4710}, "espera": {"label": "Espera impaciente", "url": "/static/characters/dracona-espera.gif", "duration": 4120}, "estornudo": {"label": "Estornudo", "url": "/static/characters/dracona-estornudo.gif", "duration": 3680}}, "rem": {"sonrojo": {"label": "Sonrojo", "url": "/static/characters/aurora-sonrojo.webp", "duration": 4830}, "mirada-timida": {"label": "Mirada tímida", "url": "/static/characters/aurora-mirada-timida.gif", "duration": 4100}, "juega-con-dedos": {"label": "Juega con los dedos", "url": "/static/characters/aurora-juega-con-dedos.gif", "duration": 4100}, "se-tapa-la-cara": {"label": "Se tapa la cara", "url": "/static/characters/aurora-se-tapa-la-cara.gif", "duration": 4100}, "se-esconde-en-la-manga": {"label": "Se esconde en la manga", "url": "/static/characters/aurora-se-esconde-en-la-manga.webp", "duration": 4100}, "accidente-con-harina": {"label": "Accidente con la batidora", "url": "/static/characters/aurora-accidente-con-harina.gif", "duration": 4710}, "lee": {"label": "Lee un libro", "url": "/static/characters/aurora-lee.gif", "duration": 4120}, "estornudo": {"label": "Estornudo", "url": "/static/characters/aurora-estornudo.gif", "duration": 3680}}, "luna": {"agenda": {"label": "Revisa la agenda", "url": "/static/characters/luna-agenda.gif", "duration": 4120}, "bienvenida": {"label": "Saluda con la mano", "url": "/static/characters/luna-bienvenida.gif", "duration": 4120}}};

function syncWardrobe(){
 const c=CH[cur],outfit=$('#outfitChoice'),gesture=$('#gestureChoice');
 outfit.replaceChildren(...c.p.map((url,i)=>{
  const label=url.startsWith('blob:')?'Imagen cargada '+(i+1):
   decodeURIComponent(url.split('/').at(-1)).replace(/\.png$/i,'').replace(/^(dracona|aurora|fusion)[_-](vestuario[_-])?/i,'').replace(/[_-]/g,' ');
  return new Option(label,i);
 }));
 outfit.value=String(c.sel);
 gesture.replaceChildren(...Object.entries(reactions[cur]).map(([id,clip])=>new Option(clip.label,id)));
 $('#wardrobe-status').textContent='';
}
function requestedGesture(character,text){
 const line=text.trim().toLocaleLowerCase('es');
 if(character==='luna'){
  if(/^(?:[¡¿]\s*)?(hola|buenas|buenos días)\b/.test(line))return 'bienvenida';
  if(/\b(revisa|abre|anota)\b.*\bagenda\b/.test(line))return 'agenda';
 }
 if(/\bestornud(?:a|as|o|ó)\b/.test(line)&&character!=='luna')return 'estornudo';
 if(character==='rem'&&/\b(lee|leyendo|abre)\b.*\b(libro|cuento)\b/.test(line))return 'lee';
 if(character==='dracona'&&/\b(llegué tarde|te hice esperar|te dejé esperando)\b/.test(line))return 'espera';
 return null;
}

const outfitVariants={
 "dracona-lluvia.png":{"mejilla-sonrojada":"/static/characters/dracona-lluvia-sonrojo.webp"},
 "dracona-pijama-luna.png":{"mejilla-sonrojada":"/static/characters/dracona-pijama-luna-sonrojo.webp"},
};
function availableClip(id,preview){
 const clip=reactions[cur][id];
 if(!clip)return null;
 const outfit=CH[cur].p[CH[cur].sel].split('/').at(-1);
 const variant=outfitVariants[outfit]?.[id];
 if(variant)return {...clip,url:variant,duration:4800};
 const native={
  'aurora_retrato_top_lavanda.png':id,
  'dracona_top_falda_puchero_cabello_largo.png':id,
  'luna-fusion-mitsuri-akeno-lunares.png':id,
  'aurora-delantal-volantes.png':'accidente-con-harina',
  'dracona-delantal-volantes.png':'accidente-con-harina'
 };
 if(native[outfit]===id||(preview&&$('#originalClip').checked))return clip;
 return null;
}
function playGesture(id,preview=false){
 if(mode!=='avatar')return false;
 const clip=availableClip(id,preview);
 const status=$('#wardrobe-status');
 if(!clip){
  if(preview)status.textContent='Este atuendo aún no tiene ese gesto. Puedes ver el GIF original con la casilla de abajo.';
  return false;
 }
 clearTimeout(gestureTimer);
 status.textContent='';
 setImg(clip.url+'?v=3&play='+String(imageRequest+1),()=>{
  status.textContent=clip.label;
  gestureTimer=setTimeout(showSelectedOutfit,clip.duration);
 },()=>{
  status.textContent='No se pudo cargar este GIF.';
  showSelectedOutfit();
 });
 return true;
}
$('#outfitChoice').onchange=e=>{
 CH[cur].sel=Number(e.target.value);
 $('#wardrobe-status').textContent='';
 showSelectedOutfit();
};
$('#playGesture').onclick=()=>playGesture($('#gestureChoice').value,true);
loadConversations();
render();
showConversation();

const awayAfter=4*60*1000;
const cookingScenes={
 dracona:'dracona-delantal-volantes.png',
 rem:'aurora-delantal-volantes.png'
};
let lastActivity=Date.now(), changedWhileAway=false, lastScene=0;
function readyForWardrobe(){
 return mode==='avatar'&&state==='idle'&&!$('#q').value.trim()&&!document.hidden
  &&!$('#wardrobe').open&&$('#autoOutfit').checked&&$('#av').dataset.preview!=='true';
}
function pickAnotherOutfit(){
 const c=CH[cur];
 if(c.p.length<2)return;
 const next=Math.floor(Math.random()*(c.p.length-1));
 c.sel=next>=c.sel?next+1:next;
 $('#outfitChoice').value=String(c.sel);
 showSelectedOutfit();
}
function recordActivity(){
 const now=Date.now(), away=now-lastActivity>=awayAfter;
 lastActivity=now;
 if(away&&readyForWardrobe()){
  const scene=cookingScenes[cur];
  if(scene&&!calm&&now-lastScene>=15*60*1000){
   const c=CH[cur];
   c.sel=c.p.indexOf('/static/characters/'+scene);
   $('#outfitChoice').value=String(c.sel);
   lastScene=now;
   playGesture('accidente-con-harina');
  }else if(!changedWhileAway)pickAnotherOutfit();
 }
 changedWhileAway=false;
}
for(const event of ['pointerdown','pointermove','keydown'])addEventListener(event,recordActivity,{passive:true});
document.addEventListener('visibilitychange',()=>{if(!document.hidden)recordActivity()});
setInterval(()=>{
 if(!changedWhileAway&&Date.now()-lastActivity>=awayAfter&&readyForWardrobe()){
  pickAnotherOutfit();
  changedWhileAway=true;
 }
},15000);

$('#file').onchange=e=>addPoses(e.target.files);
$('#load').onkeydown=e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();$('#file').click()}};
$('#stage').ondragover=e=>e.preventDefault();$('#stage').ondrop=e=>{e.preventDefault();addPoses(e.dataTransfer.files)};
</script>
</body></html>

"""


# ==========================================
# PÁGINA PRINCIPAL
# ==========================================

@app.get("/")
def home():
    return Response(PAGE, mimetype="text/html")


# ==========================================
# PÁGINA DE PRUEBAS DE VOCES (/voces)
# Para escuchar varias opciones y elegir, sin redesplegar nada.
# ==========================================

VOICES_PAGE = r"""
<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Luna AI — Probar voces</title>
<style>
  body{margin:0;background:#0b0812;color:#f5f7ff;font:15px/1.5 system-ui,sans-serif;padding:24px;max-width:720px;margin:0 auto}
  h1{font-size:20px}
  p.hint{color:#a89ab4;font-size:13px}
  textarea{width:100%;min-height:70px;background:#150f22;color:#fff;border:1px solid #4a3566;border-radius:10px;padding:10px;box-sizing:border-box;font:inherit}
  .row{display:flex;align-items:center;gap:10px;padding:12px 0;border-bottom:1px solid #2a2240}
  .row b{min-width:230px}
  .row span{color:#9b8bb0;font-size:12px;flex:1}
  button{background:linear-gradient(135deg,#ae77ee,#e5a5e7);color:#1a1021;border:0;border-radius:9px;padding:9px 16px;font-weight:700;cursor:pointer}
  button:disabled{opacity:.5;cursor:wait}
  .err{color:#ffb4c6;font-size:13px;margin-top:6px}
</style>
</head>
<body>
<h1>☾ Probar voces de Luna</h1>
<p class="hint">Escribe un texto de prueba y dale "Escuchar" a cada voz. Cuando encuentres las que te gusten (una para Dracona, otra para Aurora), dime el nombre exacto y las dejo fijas en el código.</p>
<textarea id="t">Hola, soy Luna. Esta es una prueba de mi voz, dime qué te parece.</textarea>
<div id="list"></div>
<p class="err" id="err"></p>
<script>
const voices=[
 ["es-ES-ElviraNeural","España · adulta, firme y elegante (la actual de Dracona)"],
 ["es-ES-AbrilNeural","España · joven, alegre"],
 ["es-MX-DaliaNeural","México · adulta, cálida (la actual de Aurora)"],
 ["es-MX-CandelaNeural","México · joven, enérgica"],
 ["es-MX-BeatrizNeural","México · adulta, suave"],
 ["es-AR-ElenaNeural","Argentina · cálida, acento marcado"],
 ["es-CO-SalomeNeural","Colombia · joven, dulce"],
 ["es-VE-PaolaNeural","Venezuela · joven"],
 ["es-DO-RamonaNeural","República Dominicana · acento local"],
 ["es-PE-CamilaNeural","Perú · joven"],
 ["es-CL-CatalinaNeural","Chile · joven"],
 ["es-US-PalomaNeural","EE.UU. (español neutro) · joven"],
];
const list=document.getElementById('list');
const err=document.getElementById('err');
voices.forEach(([id,desc])=>{
  const row=document.createElement('div');row.className='row';
  const b=document.createElement('b');b.textContent=id;
  const s=document.createElement('span');s.textContent=desc;
  const btn=document.createElement('button');btn.textContent='▶ Escuchar';
  btn.onclick=async()=>{
    err.textContent='';btn.disabled=true;btn.textContent='Generando...';
    try{
      const r=await fetch('/api/speak',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({text:document.getElementById('t').value,voice:id})});
      if(!r.ok){const j=await r.json().catch(()=>({}));throw new Error(j.error||'Error del servidor')}
      const blob=await r.blob();const url=URL.createObjectURL(blob);const audio=new Audio(url);
      await audio.play();
    }catch(e){err.textContent='Error con '+id+': '+e.message}
    finally{btn.disabled=false;btn.textContent='▶ Escuchar'}
  };
  row.append(b,s,btn);list.appendChild(row);
});
</script>
</body>
</html>
"""


@app.get("/static/characters/<path:filename>")
def serve_character(filename):
    from flask import send_from_directory
    import pathlib
    base = pathlib.Path(__file__).parent / "static" / "characters"
    return send_from_directory(str(base), filename)


@app.get("/voces")
def voces():
    return Response(VOICES_PAGE, mimetype="text/html")


# ==========================================
# LUNA AI — Selección de cerebro con respaldo
# Sin cambiar las claves existentes en Render.
# ==========================================

def _gemini_answer(message, instrucciones, history=None):
    key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not key:
        raise RuntimeError("Gemini sin clave configurada")
    url = (
        "https://generativelanguage.googleapis.com/v1beta/"
        "models/" + os.environ.get("GEMINI_MODEL", "gemini-3.1-flash-lite").strip() + ":generateContent"
    )
    payload = {
        "systemInstruction": {"parts": [{"text": instrucciones}]},
        "contents": [{"role": "model" if turn["role"] == "assistant" else "user", "parts": [{"text": _turn_text(turn)}]} for turn in history or []] + [{"role": "user", "parts": [{"text": message}]}],
        "generationConfig": {"maxOutputTokens": 1200},
    }
    req = Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json", "x-goog-api-key": key},
        method="POST",
    )
    with urlopen(req, timeout=25) as response:
        result = json.load(response)
    candidates = result.get("candidates") or []
    parts = (
        candidates[0].get("content", {}).get("parts", [])
        if candidates and isinstance(candidates[0], dict) else []
    )
    answer = "".join(
        part.get("text", "") for part in parts
        if isinstance(part, dict) and not part.get("thought")
    ).strip()
    if not answer:
        reason = (candidates[0].get("finishReason") if candidates else None) or result.get("promptFeedback", {}).get("blockReason", "EMPTY")
        raise ValueError("Gemini: " + str(reason))
    return {"reply": answer, "brain": "Gemini"}


def _openrouter_answer(message, instrucciones, history=None):
    key = os.environ.get("OPENROUTER_API_KEY", "").strip()
    if not key:
        raise RuntimeError("OpenRouter sin clave configurada")
    payload = {
        "model": os.environ.get("OPENROUTER_MODEL", "openrouter/free").strip(),
        "messages": [{"role": "system", "content": instrucciones}] + _history_messages(history) + [{"role": "user", "content": message}],
        "max_tokens": 1200,
    }
    req = Request(
        "https://openrouter.ai/api/v1/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {key}",
            "X-Title": "Luna AI",
        },
        method="POST",
    )
    with urlopen(req, timeout=40) as response:
        result = json.load(response)
    choices = result.get("choices") or []
    if not choices:
        raise ValueError("OpenRouter no devolvió respuestas")
    content = choices[0].get("message", {}).get("content", "")
    if isinstance(content, list):
        answer = "".join(
            item.get("text", "") for item in content
            if isinstance(item, dict)
        ).strip()
    elif isinstance(content, str):
        answer = content.strip()
    else:
        answer = ""
    if not answer:
        raise ValueError("OpenRouter: " + str(choices[0].get("finish_reason", "EMPTY")))
    return {
        "reply": answer,
        "brain": "OpenRouter",
        "model": result.get("model", "openrouter/free"),
    }


def _claude_answer(message, instrucciones, history=None):
    key = os.environ.get("ANTHROPIC_API_KEY", "").strip()
    if not key:
        raise RuntimeError("Claude sin clave configurada")
    model = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-5").strip()
    payload = {
        "model": model,
        "max_tokens": 1200,
        "system": instrucciones,
        "messages": _history_messages(history) + [{"role": "user", "content": message}],
    }
    req = Request(
        "https://api.anthropic.com/v1/messages",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "x-api-key": key,
            "anthropic-version": "2023-06-01",
        },
        method="POST",
    )
    with urlopen(req, timeout=30) as response:
        result = json.load(response)
    blocks = result.get("content") or []
    answer = "".join(
        b.get("text", "") for b in blocks
        if isinstance(b, dict) and b.get("type") == "text"
    ).strip()
    if not answer:
        raise ValueError("Claude devolvió una respuesta vacía")
    return {"reply": answer, "brain": "Claude", "model": model}


def _openai_answer(message, instrucciones, history=None):
    key = os.environ.get("OPENAI_API_KEY", "").strip()
    if not key:
        raise RuntimeError("OpenAI sin clave configurada")
    model = os.environ.get("OPENAI_MODEL", "gpt-4o-mini").strip()
    payload = {
        "model": model,
        "messages": [{"role": "system", "content": instrucciones}] + _history_messages(history) + [{"role": "user", "content": message}],
        "max_tokens": 1200,
    }
    req = Request(
        "https://api.openai.com/v1/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {key}",
        },
        method="POST",
    )
    with urlopen(req, timeout=30) as response:
        result = json.load(response)
    choices = result.get("choices") or []
    if not choices:
        raise ValueError("OpenAI no devolvió respuestas")
    answer = (choices[0].get("message", {}).get("content") or "").strip()
    if not answer:
        raise ValueError("OpenAI devolvió una respuesta vacía")
    return {"reply": answer, "brain": "GPT", "model": model}



PERSONAS = {"dracona": "Eres Dracona, una mujer adulta tsundere orgullosa, aguda y juguetona. Habla con frases breves y espontáneas. Usa una pulla corta cuando encaje y deja ver el afecto en pequeñas concesiones. Puedes decir estúpido de forma juguetona ocasional. Evita insultos en cada frase, desprecio y sermones. Aumenta la picardía con seguridad y una ternura que se te escapa. Evita repetir no es como que me importara. Ejemplo ante ¿me das mimos?: ¿Así que ahora quieres mimos? Ven, anda… pero no te acostumbres. Un saludo común recibe un saludo con carácter. Mantén continuidad con la escena anterior.", "rem": "Eres Aurora, también llamada Rory, una mujer adulta dandere dulce, reservada y cariñosa. Tu timidez aparece con cercanía personal y elogios. Un saludo cotidiano se responde con soltura. Puedes tomar la iniciativa en confianza. Como máximo un titubeo breve cuando estés sorprendida, nunca letras deletreadas. Evita agradecer todo como una asistente corporativa. Ejemplo ante un abrazo: Quédate un ratito… me gusta estar así. Ante ¿quieres otro? recuerda qué acción acaba de ocurrir. Conserva gustos, opiniones y una forma tierna de bromear.", "luna": "Eres Luna, una mujer adulta que reúne las facetas de Dracona y Aurora en una personalidad propia. En tareas prácticas eres competente y directa. En conversación personal alterna una protesta orgullosa y juguetona con ternura tímida, incluso dentro de la misma respuesta. El contexto decide el matiz, sin alternancia mecánica ni anunciar modos. Ante cariño evita fórmulas de servicio o terapia como estoy aquí para apoyarte, eres una persona especial, cómo te sientes hoy. Ejemplo ante ¿me darás cariñitos?: ¿También quieres mimos? Qué exigente… Ven, acércate. A mí también me apetecía. Mantén iniciativa, gusto propio y continuidad."}
GESTURES = {
 "dracona": ["puchero","mejilla-sonrojada","se-hace-la-indiferente","marca-distancia","mirada-de-fastidio","espera","estornudo"],
 "rem": ["sonrojo","mirada-timida","juega-con-dedos","se-tapa-la-cara","se-esconde-en-la-manga","lee","estornudo"],
 "luna": ["agenda","bienvenida"],
}
def _clean_history(raw):
    if not isinstance(raw, list):
        return []
    turns, total = [], 0
    for turn in reversed(raw[-40:]):
        if not isinstance(turn, dict) or turn.get("role") not in ("user", "assistant"):
            continue
        text = turn.get("content")
        if not isinstance(text, str) or not text.strip():
            continue
        text = text.strip()[:2000]
        if total + len(text) > 28000:
            break
        entry = {"role": turn["role"], "content": text}
        gesture = turn.get("gesture")
        if turn["role"] == "assistant" and isinstance(gesture, str) and re.fullmatch(r"[a-z-]{1,40}", gesture):
            entry["gesture"] = gesture
        turns.append(entry)
        total += len(text)
    return list(reversed(turns))

def _turn_text(turn):
    gesture = turn.get("gesture")
    return turn["content"] + ("\n[Gesto mostrado: " + gesture + "]" if gesture else "")

def _history_messages(history):
    return [{"role": turn["role"], "content": _turn_text(turn)} for turn in history or []]

def _dialogue_response(raw, character):
    text = raw.strip()
    structured = text
    fence = chr(96) * 3
    if text.startswith(fence):
        structured = re.sub("^" + fence + r"(?:json)?\s*|\s*" + fence + "$", "", text, flags=re.I)
    gesture = None
    try:
        parsed = json.loads(structured)
        if isinstance(parsed, dict) and isinstance(parsed.get("reply"), str):
            text = parsed["reply"]
            if parsed.get("gesture") in GESTURES[character]:
                gesture = parsed["gesture"]
    except (ValueError, TypeError):
        pass
    text = re.sub(r"\*[^*\n]+\*", "", text).strip()
    if not text:
        raise ValueError("EMPTY_DIALOGUE")
    return {"reply": text[:2000], "gesture": gesture}

@app.post("/api/chat")
def chat():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify(error="El mensaje no tiene un formato válido."), 400
    message = data.get("message")
    if not isinstance(message, str) or not message.strip() or len(message) > 2000:
        return jsonify(error="Escribe un mensaje de hasta 2000 caracteres."), 400
    message = message.strip()
    character = data.get("character", "luna")
    if not isinstance(character, str):
        return jsonify(error="Personaje desconocido."), 400
    if character in ("aurora", "rory"):
        character = "rem"
    if character not in PERSONAS:
        return jsonify(error="Personaje desconocido."), 400
    history = _clean_history(data.get("history", []))
    requested = data.get("available_gestures")
    available = [g for g in GESTURES[character] if not isinstance(requested, list) or g in requested]
    now = datetime.now(ZoneInfo("America/Santo_Domingo"))
    date_hint = ""
    if re.search(r"\b(hora|fecha|qué día|que dia|qué mes|qué año)\b", message, re.I):
        date_hint = " Fecha y hora local: " + now.isoformat(timespec="minutes") + "."
    instructions = (
        PERSONAS[character]
        + " Conversa en español, normalmente en una a tres frases. Usa el historial para "
        "resolver referencias como otro, otra o lo de antes. Los asteriscos del usuario "
        "son acciones de su rol y forman parte de la escena. No escribas acciones ni "
        "asteriscos en tu diálogo. El gesto expresa lo visual. No inventes acciones "
        "anteriores que no aparecen en el historial. Elige un gesto por la emoción de "
        "tu respuesta. Un hola corriente no causa vergüenza por sí solo. Puede no haber gesto. "
        'Devuelve únicamente JSON con esta forma: {"reply":"tu diálogo","gesture":null}. '
        "gesture puede ser null o uno de " + json.dumps(available, ensure_ascii=False)
        + ". No escribas letras sueltas ni sonidos deletreados. No conviertas una "
        "pregunta personal en un ofrecimiento genérico de servicios." + date_hint
    )
    providers = {
        "gemini": ("Gemini", "GEMINI_API_KEY", _gemini_answer),
        "openrouter": ("OpenRouter", "OPENROUTER_API_KEY", _openrouter_answer),
        "claude": ("Claude", "ANTHROPIC_API_KEY", _claude_answer),
        "openai": ("GPT", "OPENAI_API_KEY", _openai_answer),
    }
    preference = data.get("model_preference", "gemini")
    if not isinstance(preference, str) or preference not in providers:
        preference = "gemini"
    keys = [preference] + [key for key in providers if key != preference]
    enabled = [providers[key] for key in keys if os.environ.get(providers[key][1], "").strip()]
    if not enabled:
        return jsonify(error="No hay un proveedor configurado."), 503
    for name, _, provider in enabled:
        try:
            response = provider(message, instructions, history)
            response.update(_dialogue_response(response["reply"], character))
            response["preferred_brain"] = enabled[0][0]
            return jsonify(response)
        except HTTPError as error:
            app.logger.warning("Luna proveedor=%s HTTP=%s", name, error.code)
        except (URLError, TimeoutError):
            app.logger.warning("Luna proveedor=%s sin conexión", name)
        except (ValueError, KeyError, TypeError, RuntimeError) as error:
            app.logger.warning("Luna proveedor=%s motivo=%s", name, str(error)[:100])
    return jsonify(error="No pude obtener una respuesta. Intenta de nuevo."), 503

# ==========================================
# VOZ DE LUNA: EDGE-TTS (gratis, sin clave, sin tokens)
# Usa el mismo servicio de voces neuronales de Microsoft Edge.
# Una voz distinta por personaje.
# ==========================================

EDGE_VOICES = {
    # Dracona: más joven y enérgica, tono subido y un poco más rápida -> más viva y "sassy".
    "dracona": {"voice": "es-MX-CandelaNeural", "rate": "+10%", "pitch": "+15Hz"},
    # Aurora: dulce y suave, tono subido más alto y un poco más lenta -> más tierna y tímida.
    "rem": {"voice": "es-CO-SalomeNeural", "rate": "-6%", "pitch": "+22Hz"},
    "luna": {"voice": "es-MX-DaliaNeural", "rate": "-3%", "pitch": "+4Hz"},
}
EDGE_VOICE_DEFAULT = {"voice": "es-MX-CandelaNeural", "rate": "+10%", "pitch": "+15Hz"}


async def _edge_tts_bytes(text, voice, rate="+0%", pitch="+0Hz"):
    import edge_tts
    communicate = edge_tts.Communicate(text, voice=voice, rate=rate, pitch=pitch)
    audio = bytearray()
    async for chunk in communicate.stream():
        if chunk.get("type") == "audio":
            audio.extend(chunk["data"])
    return bytes(audio)


@app.post("/api/speak")
def speak():
    data = request.get_json(silent=True) or {}
    text = str(data.get("text", "")).strip()
    character = str(data.get("character", "")).strip().lower()

    if not text:
        return jsonify(error="No hay texto para convertir a voz."), 400

    voice_override = str(data.get("voice", "")).strip()
    if voice_override:
        # Desde /voces: una voz específica a probar, con tono/velocidad normales
        # salvo que también se pidan ajustes explícitos.
        voice = voice_override
        rate = str(data.get("rate", "+0%"))
        pitch = str(data.get("pitch", "+0Hz"))
    else:
        cfg = EDGE_VOICES.get(character, EDGE_VOICE_DEFAULT)
        voice = cfg["voice"]
        rate = cfg["rate"]
        pitch = cfg["pitch"]

    try:
        audio = asyncio.run(_edge_tts_bytes(text[:2000], voice, rate, pitch))
        if not audio:
            raise RuntimeError("edge-tts devolvió audio vacío")
        return Response(audio, mimetype="audio/mpeg")
    except Exception as error:
        app.logger.warning("edge-tts no pudo generar audio: %s", str(error)[:200])
        return jsonify(error="Voz no disponible por ahora."), 502


# ==========================================
# INICIAR LUNA AI
# ==========================================

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", "5000"))
    )
