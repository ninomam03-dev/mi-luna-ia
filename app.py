# Luna AI — Cyber Celestial UI
# Apariencia nueva. Chat, voz, dictado y cerebros conservados.
# Cerebros disponibles: Claude, GPT, Gemini, OpenRouter (con respaldo automático).

import json
import os
from datetime import datetime
from zoneinfo import ZoneInfo
from urllib.error import HTTPError, URLError
from urllib.parse import quote
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
#avimg{display:block;height:100%;width:auto;max-width:100%;object-fit:contain;transition:opacity .16s;animation:br 5s ease-in-out infinite;transform-origin:50% 100%;
 opacity:calc(1 - .5*var(--h));filter:saturate(calc(1 - .4*var(--h))) brightness(calc(1 + .15*var(--h))) contrast(calc(1 - .1*var(--h))) drop-shadow(0 0 calc(8px + 20px*var(--h)) rgba(var(--gl,176,110,255),.7)) drop-shadow(0 0 4px rgba(53,225,255,.4))}
@keyframes br{50%{transform:translateY(-5px) scale(1.01)}}
#av:before,#av:after{content:"";position:absolute;inset:26px 26px 0;-webkit-mask:var(--img) center/100% 100% no-repeat;mask:var(--img) center/100% 100% no-repeat}
#av:before{background:linear-gradient(180deg,var(--t1,#b78cff),var(--t2,#4aa8ff));mix-blend-mode:color;opacity:calc(.65*var(--h))}
#av:after{background:repeating-linear-gradient(0deg,rgba(150,100,255,.35) 0 1px,transparent 1px 3px);opacity:calc(.85*var(--h));animation:sc 6s linear infinite}
#av .fog{position:absolute;inset:26px 26px 0;-webkit-mask:var(--img) center/100% 100% no-repeat;mask:var(--img) center/100% 100% no-repeat;pointer-events:none;
 opacity:calc(.6*var(--h));background:radial-gradient(ellipse at 20% 55%,rgba(var(--gl,176,110,255),.9),transparent 55%),radial-gradient(ellipse at 82% 40%,rgba(var(--gl,176,110,255),.8),transparent 50%),radial-gradient(ellipse at 50% 95%,rgba(255,255,255,.7),transparent 60%);
 filter:blur(6px);mix-blend-mode:screen;animation:fog 7s ease-in-out infinite}
@keyframes fog{0%,100%{opacity:calc(.45*var(--h));transform:translateY(0) scale(1)}50%{opacity:calc(.8*var(--h));transform:translateY(-4px) scale(1.015)}}
@keyframes sc{to{background-position:0 60px}}
#empty{position:absolute;inset:18% 20% 28%;display:none;align-items:center;justify-content:center;text-align:center;border:1px dashed var(--ln);border-radius:16px;color:var(--mu);padding:20px}
#app[data-mode=avatar]:not(.has) #empty{display:flex}
#poses{position:absolute;left:3%;bottom:3%;display:flex;gap:6px;align-items:end;flex-wrap:wrap;max-width:60%;z-index:4}
#app:not([data-mode=avatar]) #poses{display:none}
#poses button,#poses label{width:46px;height:46px;border:1px solid var(--ln);border-radius:10px;background:rgba(14,9,34,.8);padding:0;overflow:hidden;display:grid;place-items:center;color:var(--vio);font-size:22px}
#poses button.on{border-color:#fff;box-shadow:0 0 12px var(--vio)}
#poses img{width:100%;height:100%;object-fit:cover}
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
 <div id="chars" role="group" aria-label="Personalidad"><button data-c="dracona" aria-pressed="true">Dracona</button><button data-c="rem" aria-pressed="false">Aurora</button></div>
 <label id="holo">Holograma <input type="range" id="hr" min="0" max="100" value="55" aria-label="Intensidad del holograma"></label>
 <div id="poses"><label id="load" tabindex="0" title="Cargar imágenes">+<input type="file" id="file" accept="image/*" multiple hidden></label></div>
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
function setMode(m){mode=m;modeT=performance.now();if(m==='avatar'){const v=$('#av');v.classList.remove('rev');void v.offsetWidth;v.classList.add('rev')}app.dataset.mode=m;document.querySelectorAll('.tog button').forEach(b=>b.setAttribute('aria-pressed',b.dataset.m===m))}
$('#hr').oninput=e=>app.style.setProperty('--h',e.target.value/100);
$('#pal').onclick=()=>{pal=pal?0:1};
document.querySelectorAll('.tog button').forEach(b=>b.onclick=()=>setMode(b.dataset.m));
function add(who,txt){const d=document.createElement('div');d.className='m '+who;d.textContent=txt;$('#log').append(d);$('#log').hidden=false;$('#log').scrollTop=1e5}
function pickFemaleVoice(){const vs=speechSynthesis.getVoices().filter(v=>v.lang.toLowerCase().startsWith('es'));if(!vs.length)return null;
 const fem=/female|mujer|femenin|sabina|helena|laura|monica|mónica|paulina|lucia|lucía|elvira|marisol|esperanza|isabela|camila|valentina|zira|salli|carmen/i;
 const male=/male|hombre|masculin|jorge|pablo|diego|raul|raúl|carlos|miguel|juan|george|enrique|alonso/i;
 let v=vs.find(v=>fem.test(v.name));if(v)return v;
 v=vs.find(v=>!male.test(v.name));if(v)return v;
 return vs[0]}
function speak(a){if(!('speechSynthesis' in window)){setState('speaking');setTimeout(()=>setState('idle'),2500);return}
 const u=new SpeechSynthesisUtterance(a);u.lang='es-ES';const v=pickFemaleVoice();if(v){u.voice=v;u.lang=v.lang}u.pitch=1.25;
 u.onstart=()=>setState('speaking');u.onend=u.onerror=()=>setState('idle');speechSynthesis.cancel();speechSynthesis.speak(u)}
async function ask(q){setState('thinking');let a;
 try{const r=await fetch(BACKEND,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:q,character:cur,persona:CH[cur].persona,model_preference:'gemini'})});const j=await r.json();if(!r.ok)throw new Error(j.error||'Error del servidor');a=j.reply}
 catch(e){a='No pude conectar con mi cerebro. '+(e.message||'')}
 add('luna',a);speak(a)}
$('#f').onsubmit=e=>{e.preventDefault();const q=$('#q').value.trim();if(!q)return;$('#q').value='';add('yo',q);ask(q)};
$('#mic').onclick=async()=>{const b=$('#mic');
 if(mic){mic.s.getTracks().forEach(t=>t.stop());mic=null;b.setAttribute('aria-pressed','false');setState('idle');return}
 try{const s=await navigator.mediaDevices.getUserMedia({audio:true}),ac=new AudioContext(),an=ac.createAnalyser();an.fftSize=128;ac.createMediaStreamSource(s).connect(an);
  mic={s,an,d:new Uint8Array(an.frequencyBinCount)};b.setAttribute('aria-pressed','true');setState('listening')}
 catch(e){add('luna','No tengo permiso para usar el micrófono.')}};
const CH={dracona:{name:'Dracona',t:['#b78cff','#4aa8ff'],gl:'176,110,255',ui:['#1a9850','#0a3a22','163,230,180'],pal:['#3ddc84','#1a9850','#116b36','#8fe3a3'],pm:0,core:[[61,220,132],[217,179,108]],exp:[5.2,1,'double'],persona:'Eres Dracona, una tsundere orgullosa y sarcástica. Finges indiferencia y te molestas si te halagan, pero siempre terminas ayudando y dejas ver que te importa el usuario.',p:[],sel:0},
 rem:{name:'Aurora',t:['#8fe3ff','#4a7dff'],gl:'120,210,255',ui:['#2f6fe0','#0a1f4a','150,195,255'],pal:['#7ab8ff','#2f6fe0','#15306e','#bfe0ff'],pm:1,core:[[150,100,255],[40,205,238]],exp:[9.5,0,'single'],persona:'Eres Aurora (también te dicen Rory), una dandere tímida, dulce y cariñosa. Hablas suave, te sonrojas con facilidad, y te desvives por cuidar y ayudar al usuario.',p:[],sel:0}};
let cur='dracona';
const PAL={w1:'#35e1ff',w2:'#b86bff',bar0:'#8b32fa',bar1:'#36dfff',r0:'#d455ff',r1:'#35e1ff',r2:'#8547dc'};
function setImg(u){const im=$('#avimg');im.style.opacity=0;setTimeout(()=>{im.src=u;im.style.opacity=''},160);$('#av').style.setProperty('--img','url("'+u+'")')}
function mark(){document.querySelectorAll('#poses button').forEach((x,i)=>x.classList.toggle('on',i===CH[cur].sel))}
function render(){const c=CH[cur];document.querySelectorAll('#poses button').forEach(x=>x.remove());
 c.p.forEach((u,i)=>{const b=document.createElement('button');b.type='button';b.innerHTML='<img alt="" src="'+u+'">';b.onclick=()=>{c.sel=i;setImg(u);mark()};$('#poses').insertBefore(b,$('#load'))});
 const has=c.p.length>0;$('#av').classList.toggle('has',has);app.classList.toggle('has',has);if(has)setImg(c.p[c.sel]);mark();
 $('#et').textContent=c.name;$('#mav').textContent=c.name;app.style.setProperty('--t1',c.t[0]);app.style.setProperty('--t2',c.t[1]);app.style.setProperty('--gl',c.gl);
 if(c.ui){app.style.setProperty('--acc1',c.ui[0]);app.style.setProperty('--acc2',c.ui[1]);app.style.setProperty('--accrgb',c.ui[2])}
 if(c.pal){PAL.w1=c.pal[0];PAL.w2=c.pal[1];PAL.bar0=c.pal[2];PAL.bar1=c.pal[3];PAL.r0=c.pal[4];PAL.r1=c.pal[1];PAL.r2=c.pal[2];pal=c.pm}
 if(c.ui)ACC=c.ui[2];
 if(c.core){CORE0=c.core[0];CORE1=c.core[1]}
 if(c.exp){EXPER=c.exp[0];SHARP=c.exp[1];PULSE=c.exp[2]}
 coreChar=cur;app.dataset.char=cur}
function reveal(){const v=$('#av');v.classList.remove('rev');void v.offsetWidth;v.classList.add('rev')}
function addPoses(files){const c=CH[cur],first=!c.p.length;[...files].filter(f=>f.type.startsWith('image/')).forEach(f=>c.p.push(URL.createObjectURL(f)));render();if(first&&c.p.length){setMode('avatar')}}
document.querySelectorAll('#chars button').forEach(b=>b.onclick=()=>{cur=b.dataset.c;document.querySelectorAll('#chars button').forEach(x=>x.setAttribute('aria-pressed',x===b));render();reveal()});
render();
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
# LUNA AI — Selección de cerebro con respaldo
# Sin cambiar las claves existentes en Render.
# ==========================================

def _gemini_answer(message, instrucciones):
    key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not key:
        raise RuntimeError("Gemini sin clave configurada")
    url = (
        "https://generativelanguage.googleapis.com/v1beta/"
        "models/gemini-3.1-flash-lite:generateContent"
    )
    payload = {
        "systemInstruction": {"parts": [{"text": instrucciones}]},
        "contents": [{"role": "user", "parts": [{"text": message}]}],
        "generationConfig": {"maxOutputTokens": 512},
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
        raise ValueError("Gemini devolvió una respuesta vacía")
    return {"reply": answer, "brain": "Gemini"}


def _openrouter_answer(message, instrucciones):
    key = os.environ.get("OPENROUTER_API_KEY", "").strip()
    if not key:
        raise RuntimeError("OpenRouter sin clave configurada")
    payload = {
        "model": "openrouter/free",
        "messages": [
            {"role": "system", "content": instrucciones},
            {"role": "user", "content": message},
        ],
        "max_tokens": 512,
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
        raise ValueError("OpenRouter devolvió una respuesta vacía")
    return {
        "reply": answer,
        "brain": "OpenRouter",
        "model": result.get("model", "openrouter/free"),
    }


def _claude_answer(message, instrucciones):
    key = os.environ.get("ANTHROPIC_API_KEY", "").strip()
    if not key:
        raise RuntimeError("Claude sin clave configurada")
    model = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-5").strip()
    payload = {
        "model": model,
        "max_tokens": 512,
        "system": instrucciones,
        "messages": [{"role": "user", "content": message}],
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


def _openai_answer(message, instrucciones):
    key = os.environ.get("OPENAI_API_KEY", "").strip()
    if not key:
        raise RuntimeError("OpenAI sin clave configurada")
    model = os.environ.get("OPENAI_MODEL", "gpt-4o-mini").strip()
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": instrucciones},
            {"role": "user", "content": message},
        ],
        "max_tokens": 512,
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


@app.post("/api/chat")
def chat():
    data = request.get_json(silent=True) or {}
    message = str(data.get("message", "")).strip()
    if not message or len(message) > 2000:
        return jsonify(error="Escribe un mensaje de hasta 2000 caracteres."), 400

    now = datetime.now(ZoneInfo("America/Santo_Domingo"))
    weekdays = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
    months = [
        "enero", "febrero", "marzo", "abril", "mayo", "junio",
        "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre",
    ]
    fecha = f"{weekdays[now.weekday()]} {now.day} de {months[now.month-1]} de {now.year}"
    hora = now.strftime("%H:%M")
    persona = str(data.get("persona", "")).strip()
    base_persona = persona or (
        "Eres Luna, una asistente personal femenina, amable, inteligente, "
        "tierna y comprensiva. Tu personalidad es cercana y conversacional."
    )
    instrucciones = (
        f"{base_persona} "
        "Habla naturalmente en español. Responde de forma clara y normalmente "
        "breve, sin repetir innecesariamente las respuestas. No inventes "
        "información que desconozcas. "
        f"La fecha actual en República Dominicana es {fecha}. "
        f"La hora local es {hora}. "
        "Utiliza esa fecha para responder preguntas temporales."
    )

    PROVIDERS = {
        "claude": ("Claude", _claude_answer),
        "openai": ("GPT", _openai_answer),
        "gemini": ("Gemini", _gemini_answer),
        "openrouter": ("OpenRouter", _openrouter_answer),
    }
    DEFAULT_ORDER = ["claude", "openai", "gemini", "openrouter"]
    preference = str(data.get("model_preference", "gemini")).lower()
    if preference not in PROVIDERS:
        preference = "gemini"
    order = [PROVIDERS[k] for k in [preference] + [p for p in DEFAULT_ORDER if p != preference]]

    errors = []
    for name, provider in order:
        try:
            response = provider(message, instrucciones)
            response["preferred_brain"] = order[0][0]
            return jsonify(response)
        except HTTPError as error:
            app.logger.warning("%s devolvió HTTP %s", name, error.code)
            errors.append(f"{name}: HTTP {error.code}")
        except (URLError, TimeoutError):
            app.logger.warning("No se pudo conectar con %s", name)
            errors.append(f"{name}: sin conexión")
        except (ValueError, KeyError, TypeError, RuntimeError) as error:
            app.logger.warning("%s no pudo responder: %s", name, str(error)[:160])
            errors.append(f"{name}: {str(error)[:80]}")
    return jsonify(error="Los cerebros están indisponibles. " + " | ".join(errors)), 503


# ==========================================
# VOZ DE LUNA: ELEVENLABS
# ==========================================

@app.post("/api/speak")
def speak():

    data = request.get_json(silent=True) or {}
    text = str(data.get("text", "")).strip()

    if not text:
        return jsonify(
            error="No hay texto para convertir a voz."
        ), 400

    api_key = os.environ.get(
        "ELEVENLABS_API_KEY", ""
    ).strip()

    voice_id = os.environ.get(
        "ELEVENLABS_VOICE_ID", ""
    ).strip()

    if not api_key or not voice_id:
        return jsonify(
            error="Falta configurar ElevenLabs."
        ), 503

    url = (
        "https://api.elevenlabs.io/v1/text-to-speech/"
        f"{quote(voice_id, safe='')}"
        "?output_format=mp3_44100_128"
    )

    payload = {
        "text": text[:2000],
        "model_id": "eleven_multilingual_v2"
    }

    api_request = Request(
        url,
        data=json.dumps(
            payload
        ).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Accept": "audio/mpeg",
            "xi-api-key": api_key
        },
        method="POST"
    )

    try:
        with urlopen(
            api_request,
            timeout=30
        ) as response:
            audio = response.read()

        return Response(
            audio,
            mimetype="audio/mpeg"
        )

    except HTTPError as error:

        raw = error.read().decode(
            "utf-8",
            errors="replace"
        )

        try:
            error_data = json.loads(raw)
        except json.JSONDecodeError:
            error_data = {}

        if not isinstance(error_data, dict):
            error_data = {}

        detail = error_data.get("detail", {})

        if isinstance(detail, dict):
            error_code = (
                detail.get("status")
                or detail.get("code")
                or "desconocido"
            )

            error_message = (
                detail.get("message")
                or "Sin detalles"
            )

        elif isinstance(detail, str):
            error_code = "desconocido"
            error_message = detail

        else:
            error_code = "desconocido"
            error_message = "Sin detalles"

        app.logger.error(
            "ElevenLabs HTTP %s | %s | %s",
            error.code,
            error_code,
            str(error_message)[:200]
        )

        return jsonify(
            error=f"ElevenLabs: {error_code}"
        ), 502

    except (URLError, TimeoutError):
        return jsonify(
            error="No se pudo conectar con ElevenLabs."
        ), 502


# ==========================================
# INICIAR LUNA AI
# ==========================================

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", "5000"))
    )
