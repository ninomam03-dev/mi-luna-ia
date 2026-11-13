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

from flask import Flask, Response, jsonify, render_template_string, request

app = Flask(__name__)

# ==========================================
# LUNA AI - INTERFAZ
# ==========================================

PAGE = r"""
<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#0b0812">
<title>Luna AI</title>
<style>
  :root {
    color-scheme: dark;
    --motion-play: running;
    --bg:#060812; --panel:#0f1322; --panel2:#15182d;
    --line:rgba(103,232,249,.16); --line-hi:rgba(232,102,255,.42);
    --soft:#96a4c7; --white:#f5f7ff; --violet:#d186ff; --pink:#ff87d7;
    --cyan:#69f0ff; --blue:#58b4ff; --magenta:#ff53c8; --ink:#05070e;
  }
  * { box-sizing:border-box; }
  body { margin:0; min-width:320px; color:var(--white); font:14px/1.5 "Segoe UI",system-ui,sans-serif;
    background:radial-gradient(circle at top,#12162b 0,#090b15 38%,#05060c 100%); }
  button,textarea,input { font:inherit; }
  button { cursor:pointer; }
  button:disabled { cursor:not-allowed; opacity:.48; }
  button:focus-visible,textarea:focus-visible,input:focus-visible { outline:2px solid var(--violet); outline-offset:3px; }
  .shell { height:100vh; height:100dvh; min-height:0; display:grid; grid-template-rows:67px minmax(0,1fr);
    isolation:isolate; background:
      radial-gradient(circle at 25% 20%,rgba(255,83,200,.13),transparent 20%),
      radial-gradient(circle at 75% 18%,rgba(105,240,255,.12),transparent 22%),
      radial-gradient(circle at 50% 45%,rgba(104,76,255,.11),transparent 30%),
      linear-gradient(180deg,#090b16 0%,#05060d 100%);
    position:relative; overflow:hidden; }
  .shell:before { content:""; pointer-events:none; position:absolute; inset:0; z-index:-1; opacity:.30;
    background-image:
      radial-gradient(rgba(255,255,255,.6) 0.7px,transparent 1px),
      radial-gradient(rgba(148,224,255,.45) 0.6px,transparent 1px);
    background-size:101px 107px,163px 151px; background-position:11px 34px,55px 91px; }
  .shell:after { content:""; pointer-events:none; position:absolute; inset:0; z-index:-1; opacity:.14;
    background:repeating-linear-gradient(180deg,transparent 0 3px,rgba(105,240,255,.06) 3px 4px);
    mix-blend-mode:screen; animation:scan 12s linear infinite; animation-play-state:var(--motion-play); }
  .topbar { display:flex;align-items:center;justify-content:space-between;gap:14px;padding:0 23px;
    border-bottom:1px solid rgba(105,240,255,.14); background:linear-gradient(180deg,rgba(7,10,19,.92),rgba(8,10,18,.66));
    box-shadow:0 2px 20px rgba(0,0,0,.25),0 0 24px rgba(105,240,255,.05); backdrop-filter:blur(10px); }
  .identity { display:flex;align-items:center;gap:9px;white-space:nowrap; letter-spacing:3px;
    font-size:17px; font-weight:700; color:#f1f6ff; text-shadow:0 0 10px rgba(105,240,255,.12); }
  .identity svg { width:27px;height:27px;filter:drop-shadow(0 0 8px rgba(105,240,255,.45)) drop-shadow(0 0 16px rgba(255,83,200,.18)); }
  .identity em { font-style:normal;color:var(--cyan); animation:flicker 4.8s infinite; animation-play-state:var(--motion-play); }
  .top-center { display:flex; gap:8px; align-items:center; justify-content:center;flex-wrap:wrap; }
  .pill { display:inline-flex; align-items:center;gap:8px; border:1px solid rgba(105,240,255,.18);
    border-radius:999px; padding:7px 11px; font-size:11px; color:#d8e7ff;background:rgba(18,25,42,.68); white-space:nowrap;
    box-shadow:inset 0 0 15px rgba(105,240,255,.03), 0 0 20px rgba(255,83,200,.03); }
  .pill b {font-weight:700;color:#ffd0f8;} .online-dot {width:7px;height:7px;border-radius:100%;background:#8dffcb;box-shadow:0 0 9px #7feeb1;display:inline-block;}
  .top-actions {display:flex;gap:8px;align-items:center;}
  .icon-button {width:34px;height:34px;display:grid;place-items:center;background:rgba(16,20,35,.45);color:#d8d9ff;
    border:1px solid rgba(105,240,255,.15);border-radius:10px;font-size:17px;box-shadow:0 0 18px rgba(105,240,255,.03)}
  .icon-button:hover {border-color:var(--line-hi);background:rgba(180,121,235,.11);box-shadow:0 0 18px rgba(255,83,200,.12)}
  .workspace {display:grid; grid-template-columns:78px minmax(250px,1.05fr) minmax(310px,1fr); min-height:0; height:100%; overflow:hidden;}
  .rail { display:flex;flex-direction:column;align-items:center;gap:10px;padding:23px 8px 14px;
    border-right:1px solid rgba(105,240,255,.10);background:linear-gradient(180deg,rgba(5,8,16,.72),rgba(8,9,17,.5)); backdrop-filter:blur(8px); }
  .rail-btn {display:flex;flex-direction:column;justify-content:center;align-items:center;gap:4px;
    min-height:59px;width:60px;border:1px solid transparent;border-radius:13px;color:#afa1c0;background:transparent;}
  .rail-btn svg {width:21px;height:21px;stroke-width:1.7;}
  .rail-btn span {font-size:10px;line-height:1.1;}
  .rail-btn:hover,.rail-btn.active {border-color:rgba(105,240,255,.28);color:#f8deff;
    background:linear-gradient(145deg,rgba(255,83,200,.14),rgba(58,121,255,.08));
    box-shadow:inset 0 0 22px rgba(190,108,232,.10), 0 0 16px rgba(105,240,255,.08);}
  .rail-btn.muted {opacity:.45;cursor:default;}
  .rail-bottom {margin-top:auto;color:#746583;font-size:10px;text-align:center;}
  .stage {min-width:0;min-height:0;display:flex;align-items:center;justify-content:center;flex-direction:column;padding:15px 16px 14px;position:relative;overflow:hidden;}
  .stage:before {content:"";position:absolute;width:min(650px,100%);aspect-ratio:1;border-radius:50%;
    background:radial-gradient(circle,rgba(255,83,200,.12),transparent 45%), radial-gradient(circle at 40% 60%,rgba(105,240,255,.16),transparent 56%);filter:blur(3px);pointer-events:none;}
  .stage:after {content:"";position:absolute;inset:auto 7% 6% 7%;height:180px;pointer-events:none;opacity:.28;
    background:linear-gradient(180deg,transparent 0%,rgba(105,240,255,.18) 100%);
    clip-path:polygon(0 100%,50% 0,100% 100%);
    filter:blur(28px);}
  .eyebrow {font-size:10px;color:#9bc2ff;letter-spacing:4px;position:relative;margin-bottom:6px;text-shadow:0 0 8px rgba(105,240,255,.18);}
  .orb {position:relative;width:min(405px,100%,46vh);aspect-ratio:1;display:grid;place-items:center;flex-shrink:0; filter:drop-shadow(0 0 24px rgba(105,240,255,.12)) drop-shadow(0 0 30px rgba(255,83,200,.10));}
  .halo {position:absolute;inset:2%;border:1px solid rgba(204,147,255,.10);border-radius:50%;}
  .orb::before {content:"";position:absolute;inset:4%;border-radius:50%;
    background:radial-gradient(circle,rgba(255,255,255,.06) 0,rgba(105,240,255,.05) 26%,rgba(255,83,200,.04) 42%,transparent 70%);
    filter:blur(18px);animation:pulseGlow 4.5s ease-in-out infinite; animation-play-state:var(--motion-play);}
  .orb::after {content:"";position:absolute;inset:0;border-radius:50%;
    background:conic-gradient(from 0deg,transparent 0deg 36deg,rgba(105,240,255,.55) 42deg 48deg,transparent 54deg 130deg,rgba(255,83,200,.6) 134deg 138deg,transparent 142deg 270deg,rgba(105,240,255,.32) 276deg 282deg,transparent 286deg 360deg);
    mask:radial-gradient(circle,transparent 72%,#000 73% 74%,transparent 75%);
    animation:orbit 14s linear infinite; animation-play-state:var(--motion-play); opacity:.75;}
  .halo.outer {inset:7%;border:1px solid rgba(105,240,255,.24);
    border-top:2px solid rgba(105,240,255,.95);border-right:2px solid transparent;border-bottom:1px dashed rgba(255,83,200,.58);
    transform:rotate(7deg);animation:orbit 18s linear infinite; animation-play-state:var(--motion-play);filter:drop-shadow(0 0 8px rgba(105,240,255,.5));}
  .halo.middle {inset:15%;border:1px dashed rgba(214,163,249,.45);border-left:2px solid var(--magenta);
    border-bottom:2px solid rgba(105,240,255,.18);animation:orbit 30s linear infinite reverse; animation-play-state:var(--motion-play);}
  .halo.inner {inset:24%;border:1px solid rgba(197,141,255,.22);border-top:2px solid rgba(255,190,255,.84);
    border-right:2px solid transparent;animation:orbit 12s linear infinite; animation-play-state:var(--motion-play);}
  .halo.ticks {inset:10%;border:none;background:repeating-conic-gradient(from 4deg,rgba(105,240,255,.70) 0deg 1deg,transparent 1deg 13deg);
    mask:radial-gradient(circle,transparent 66%,#000 67% 68%,transparent 69%);opacity:.45;animation:orbit 60s linear infinite; animation-play-state:var(--motion-play);}
  .orb-star {position:absolute;width:5px;height:5px;background:#fff0ff;transform:rotate(45deg);box-shadow:0 0 15px 3px rgba(220,166,255,.65)}
  .orb-star.one {top:18%;left:28%;}.orb-star.two {right:14%;top:48%;width:3px;height:3px;}.orb-star.three {left:23%;bottom:22%;width:3px;height:3px;}
  .moon-svg {width:53%;height:53%;overflow:visible;filter:drop-shadow(0 0 14px rgba(255,83,200,.42)) drop-shadow(0 0 24px rgba(105,240,255,.25));animation:breathe 3.8s ease-in-out infinite; animation-play-state:var(--motion-play);}
  .orbit-curve {position:absolute;inset:13%;width:74%;height:74%;pointer-events:none;opacity:.8;transform:rotate(-17deg);animation:orbit 22s linear infinite reverse; animation-play-state:var(--motion-play);}
  .waveform {display:flex;align-items:center;justify-content:center;gap:4px;height:34px;margin-top:-5px;z-index:1;filter:drop-shadow(0 0 8px rgba(105,240,255,.16));}
  .waveform i {width:2px;height:5px;background:linear-gradient(var(--cyan),var(--magenta));border-radius:3px;box-shadow:0 0 7px rgba(105,240,255,.55);}
  .shell[data-state="listening"] .waveform i,.shell[data-state="speaking"] .waveform i {animation:wave .8s ease-in-out infinite alternate;}
  .waveform i:nth-child(2n){animation-delay:-.32s}.waveform i:nth-child(3n){animation-delay:-.55s}.waveform i:nth-child(5n){animation-delay:-.72s}
  .shell[data-state="thinking"] .halo.outer {animation-duration:5s;}.shell[data-state="speaking"] .moon-svg {animation-duration:1.6s;}
  .core-status {text-align:center;z-index:1;margin-top:22px;min-height:64px;}
  .core-status strong {font-size:17px;font-weight:600;color:#ebd1fb;display:block;}
  .core-status span {font-size:12px;color:#a89ab4;display:block;margin-top:6px;max-width:310px;}
  .voice-trigger {margin-top:15px;border:1px solid rgba(228,170,255,.65);border-radius:999px;
    padding:10px 25px;display:flex;gap:9px;align-items:center;color:#f5dcff;
    background:linear-gradient(115deg,rgba(142,64,201,.2),rgba(225,141,235,.13));z-index:1;
    box-shadow:0 0 24px rgba(140,69,198,.13);}
  .voice-trigger:hover {background:rgba(205,137,253,.25);}
  .voice-trigger svg {width:17px;height:17px;}
  .ambient-line {width:85%;height:1px;background:linear-gradient(90deg,transparent,rgba(208,153,255,.45),transparent);margin-top:25px;}
  /* Modo demostración de voz: el holograma responde al volumen del archivo local. */
  .demo-topbar {border:1px solid var(--l-border,rgba(189,70,255,.4));background:linear-gradient(125deg,rgba(180,92,255,.19),rgba(90,235,255,.08));
    border-radius:11px;color:var(--l-text,#f8edff);font-size:12px;letter-spacing:.3px;white-space:nowrap;padding:9px 12px;
    box-shadow:0 0 17px rgba(173,70,255,.10);}
  .demo-topbar:hover,.demo-topbar.demo-active{box-shadow:0 0 20px rgba(var(--l-primary-rgb,189,70,255),.36);border-color:var(--l-primary,#d186ff);}
  .shell[data-demo="playing"] .orb {transition:transform .07s ease-out;}
  .shell[data-demo="playing"] .luna-art {filter:drop-shadow(0 0 22px rgba(var(--l-primary-rgb,189,70,255),.70));}
  .shell[data-demo="playing"] .waveform {height:45px;}
  .shell[data-demo="playing"] .waveform i {animation:none !important;transition:height .06s linear;}
  .demo-overlay {z-index:60;}
  .demo-dialog {width:min(480px,100%);max-height:92vh;overflow-y:auto;border-color:var(--l-primary,#ba70fb);}
  .demo-label {display:block;margin:16px 0 7px;color:var(--l-text,#f8eeff);font-size:12px;font-weight:650;}
  .demo-file {display:block;width:100%;min-width:0;color:var(--l-text,#f8eeff);font-size:12px;padding:12px;
    background:rgba(130,89,177,.11);border-radius:12px;border:1px solid rgba(205,164,240,.35);}
  .demo-file::file-selector-button {cursor:pointer;border:1px solid rgba(205,164,240,.45);border-radius:8px;
    padding:7px 12px;color:var(--l-text,#f8eeff);background:rgba(135,76,193,.24);margin-right:10px;}
  .demo-file-status {font-size:11px;margin-top:6px;color:#bbaacf;overflow-wrap:anywhere;}
  .demo-transcript {width:100%;background:rgba(25,13,40,.88);border:1px solid rgba(205,164,240,.37);border-radius:12px;
    color:#faf1ff;padding:11px;resize:vertical;font-size:12px;line-height:1.45;}
  .demo-actions {display:flex;gap:9px;margin-top:15px;}
  .demo-btn {flex:1;min-height:42px;border-radius:11px;border:1px solid rgba(180,140,240,.40);color:#f4e8ff;background:rgba(102,58,148,.25);font-weight:600;}
  .demo-play {color:#180e24;background:linear-gradient(115deg,var(--l-primary,#bd46ff),var(--l-secondary,#ff52cd));border:none;}
  .demo-privacy {font-size:11px !important;line-height:1.55;opacity:.85;margin:15px 0 0;}
  .demo-error {color:#ffd2df !important;margin-bottom:0;}
  @media(max-width:720px){.demo-topbar{padding:8px;}.demo-topbar span{display:none;}}
  .conversation {display:flex;flex-direction:column;min-width:0;min-height:0;max-height:100%;overflow:hidden;border-left:1px solid var(--line);
    background:linear-gradient(145deg,rgba(18,13,31,.84),rgba(9,8,16,.83));}
  .conversation-head {height:64px;flex:none;display:flex;align-items:center;justify-content:space-between;
    gap:12px;padding:0 21px;border-bottom:1px solid var(--line);}
  .conversation-head strong {font-weight:600;font-size:15px;}.conversation-head small {color:#ad9fb8;font-size:11px;}
  .thread {flex:1 1 0;min-height:0;overflow-y:auto;overscroll-behavior:contain;display:flex;flex-direction:column;gap:16px;padding:22px 20px 18px;
    scrollbar-color:#5f3e75 transparent;scrollbar-width:thin;}
  .bubble {padding:13px 17px;max-width:91%;border-radius:18px;font-size:14px;line-height:1.58;
    overflow-wrap:anywhere;white-space:pre-wrap;box-shadow:0 8px 30px rgba(0,0,0,.12);}
  .bubble.luna {align-self:flex-start;background:linear-gradient(140deg,rgba(86,47,107,.69),rgba(50,34,71,.66));
    border:1px solid rgba(223,167,255,.39);border-bottom-left-radius:5px;}
  .bubble.user {align-self:flex-end;background:linear-gradient(135deg,#2e2840,#231d34);border:1px solid rgba(189,158,224,.28);border-bottom-right-radius:5px;}
  .bubble.system {align-self:center;background:rgba(116,54,96,.21);border:1px solid rgba(235,145,204,.25);font-size:12px;color:#efd4e6;}
  .bubble-label {display:flex;align-items:center;gap:8px;margin-bottom:7px;font-size:10px;font-weight:600;letter-spacing:.5px;color:#edc0ff;}
  .bubble.user .bubble-label {justify-content:flex-end;color:#bfb1d7;}
  .composer {flex:none;display:flex;align-items:end;gap:8px;padding:13px 16px;border-top:1px solid var(--line);background:rgba(12,9,21,.88);z-index:2;}
  .composer textarea {resize:none;min-height:48px;max-height:130px;flex:1;min-width:0;color:#f8e8ff;
    border:1px solid rgba(212,155,255,.42);border-radius:13px;background:rgba(14,10,24,.96);padding:12px 14px;}
  .composer textarea::placeholder {color:#8e829e;}
  .send {height:48px;padding:0 15px;display:flex;align-items:center;gap:6px;border:0;border-radius:13px;
    background:linear-gradient(135deg,#ae77ee,#e5a5e7);color:#1a1021;font-weight:700;}
  .send:hover {filter:brightness(1.12)}
  .send svg{width:17px;height:17px;}
  .overlay {position:fixed;z-index:30;inset:0;background:rgba(2,2,8,.72);display:grid;place-items:center;padding:20px;backdrop-filter:blur(5px);}
  .overlay[hidden] {display:none}
  .dialog {width:min(420px,100%);border:1px solid #9165b0;border-radius:20px;padding:23px;
    background:linear-gradient(145deg,#21142e,#100d19);box-shadow:0 25px 80px #0008;}
  .dialog h2 {margin:0 0 12px;font-size:19px;}.dialog p {color:#b5a4c4;font-size:12px;}
  .setting {display:flex;align-items:center;gap:12px;padding:13px 0;border-bottom:1px solid var(--line);}
  .setting input {accent-color:#c487ff; width:17px;height:17px;}
  .close-dialog {margin-top:20px;padding:10px 20px;border:1px solid #af7bd2;border-radius:11px;
    background:#422651;color:#f2d9ff;}
  @keyframes orbit {to {transform:rotate(360deg)}}
  @keyframes breathe {50% {opacity:.8;transform:scale(.96)}}
  @keyframes wave {to {height:27px;opacity:.55}}
  @keyframes pulseGlow {50% {transform:scale(1.04); opacity:.86}}
  @keyframes sweep {to {transform:translateX(520%)}}
  @keyframes scan {from {transform:translateY(-8%)} to {transform:translateY(8%)}}
  @keyframes flicker {0%,19%,21%,63%,65%,100% {opacity:1} 20%,64% {opacity:.6}}
  @keyframes messageIn {from {transform:translateY(8px); opacity:0} to {transform:translateY(0); opacity:1}}
  @media(max-width:1050px) {.top-center .pill:last-child{display:none}.workspace{grid-template-columns:65px minmax(0,.97fr) minmax(300px,1fr)}.rail-btn{width:50px}.stage{padding:12px}.orb{width:min(330px,100%)}}
  @media(max-width:740px) {.shell{grid-template-rows:58px minmax(0,1fr)}.topbar{padding:0 13px}.identity{font-size:14px}.top-center{display:none}
    .workspace{grid-template-columns:57px minmax(0,1fr);grid-template-rows:minmax(148px,.48fr) minmax(0,1fr);height:100%;overflow:hidden}
    .rail{grid-row:1 / 3;padding:14px 3px;}.rail-btn{width:49px;min-height:56px}
    .stage{min-height:0;padding:7px 10px;overflow:hidden}.eyebrow{display:none}.orb{width:min(156px,45vw,20vh)}
    .waveform{height:18px}.core-status{margin-top:3px;min-height:34px}.core-status strong{font-size:13px}.core-status span{font-size:10px}
    .voice-trigger{margin-top:4px;padding:7px 13px;font-size:11px}.ambient-line{display:none}
    .conversation{grid-column:2;grid-row:2;min-height:0;max-height:100%;border-left:0;border-top:1px solid var(--line)}
    .conversation-head{height:44px}.thread{max-height:none;min-height:0;padding:12px}.composer{padding:9px}
    .bubble{max-width:95%}}
  @media(max-height:600px) and (min-width:741px) {
    .stage{padding:4px 9px}.orb{width:min(235px,100%,38vh)}.core-status{margin-top:3px;min-height:40px}
    .ambient-line{display:none}.voice-trigger{margin-top:5px;padding:8px 13px}.eyebrow{display:none}
  }
  /* Animaciones controladas por el ajuste de Luna, no anuladas globalmente por el sistema. */

  /* ==========================================================
     LUNA AI: ANIMACIONES VIVAS (ligeras, CSS/SVG + audio real)
     Los estados idle / listening / thinking / speaking controlan todo.
     ========================================================== */
  .shell {--activity:0;}
  .stage{isolation:isolate;}
  .stage>*{position:relative;z-index:2;}
  .stage::before{animation:breathSky 5s ease-in-out infinite;animation-play-state:var(--motion-play);}
  .starfield{position:absolute;inset:0;overflow:hidden;z-index:0;pointer-events:none;}
  .starfield .spark{position:absolute;width:2px;height:2px;border-radius:50%;background:#e5faff;
    box-shadow:0 0 7px 1px rgba(118,221,255,.75);animation:starTwinkle 3s ease-in-out infinite;animation-play-state:var(--motion-play);}
  .starfield .spark.magenta{background:#ffd4f8;box-shadow:0 0 8px 1px rgba(255,90,214,.7);}
  .constellation-sky{position:absolute;inset:4% 4% auto 4%;width:92%;height:91%;z-index:1;opacity:.7;
    pointer-events:none;filter:drop-shadow(0 0 4px rgba(105,240,255,.3));}
  .constellation-sky .constellation{stroke:#8adeff;stroke-width:1.15;fill:none;stroke-linecap:round;stroke-linejoin:round;
    animation:constellationCycle 36s ease-in-out infinite;animation-play-state:var(--motion-play);opacity:0;}
  .constellation-sky .constellation:nth-child(2){stroke:#f3a3e7;animation-delay:-24s;}
  .constellation-sky .constellation:nth-child(3){stroke:#d3a5ff;animation-delay:-12s;}
  .constellation-sky .point{fill:#fcf4ff;stroke:none;filter:drop-shadow(0 0 4px #aefbff);}
  .constellation-sky .path{stroke-dasharray:3 4;}
  .stage .eyebrow{color:#b5eaff;animation:techShimmer 4.5s ease-in-out infinite;animation-play-state:var(--motion-play);}
  .orb{transition:filter .3s ease;will-change:transform;animation:floatCore 5.5s ease-in-out infinite;animation-play-state:var(--motion-play);}
  .orb::before{opacity:.9;animation:coreGlow 3s ease-in-out infinite;animation-play-state:var(--motion-play);}
  .orb::after{opacity:1;animation-duration:8s;}
  .halo.outer{animation-duration:12s;border-top-width:3px;box-shadow:0 0 19px rgba(95,240,255,.20),inset 0 0 15px rgba(95,240,255,.05);}
  .halo.middle{animation-duration:18s;box-shadow:0 0 14px rgba(255,83,200,.10);}
  .halo.inner{animation-duration:8s;}
  .halo.ticks{animation-duration:27s;opacity:.72;}
  .orb-star{animation:beacon 2.2s ease-in-out infinite;animation-play-state:var(--motion-play);}
  .orb-star.two{animation-delay:-.7s;}.orb-star.three{animation-delay:-1.4s;}
  .moon-svg{animation:moonAlive 3.2s ease-in-out infinite;animation-play-state:var(--motion-play);}
  .orbit-curve{animation-duration:14s;}
  .waveform{height:72px;gap:5px;width:min(360px,92%);margin-top:-8px;
    transition:filter .2s ease;filter:drop-shadow(0 0 9px rgba(105,240,255,.4));}
  .waveform i{display:block;flex:1 1 0;max-width:5px;min-width:2px;height:100%;border-radius:999px;
    transform-origin:center center;transform:scaleY(.16);opacity:.65;
    background:linear-gradient(180deg,#b8fbff 0%,#78dbff 28%,#c181fa 65%,#ff68cc 100%);
    box-shadow:0 0 7px rgba(105,240,255,.5);animation:idlePulse 1.8s ease-in-out infinite alternate;
    animation-play-state:var(--motion-play);will-change:transform;}
  .waveform i:nth-child(2n){animation-delay:-.43s;}.waveform i:nth-child(3n){animation-delay:-1.12s;}
  .waveform i:nth-child(5n){animation-delay:-.85s;}.waveform i:nth-child(7n){animation-delay:-.16s;}
  .shell[data-state="listening"] .waveform{filter:drop-shadow(0 0 16px rgba(93,239,255,.9));}
  .shell[data-state="listening"] .waveform i{opacity:1;animation:listenPulse .52s ease-in-out infinite alternate;animation-play-state:var(--motion-play);}
  .shell[data-state="listening"] .orb{filter:drop-shadow(0 0 26px rgba(105,240,255,.4)) drop-shadow(0 0 42px rgba(255,83,200,.24));}
  .shell[data-state="listening"] .halo.outer{animation-duration:5s;}
  .shell[data-state="listening"] .moon-svg{animation-duration:1.6s;}
  .shell[data-state="thinking"] .waveform i{opacity:.85;animation:thinkPulse .66s ease-in-out infinite alternate;animation-play-state:var(--motion-play);}
  .shell[data-state="thinking"] .halo.outer{animation-duration:2.5s;}
  .shell[data-state="thinking"] .halo.inner{animation-duration:3s;}
  .shell[data-state="thinking"] .orb::before{animation-duration:1.4s;}
  .shell[data-state="speaking"] .waveform{filter:drop-shadow(0 0 15px rgba(255,83,200,.7));}
  .shell[data-state="speaking"] .waveform i{opacity:1;animation:speechPulse .42s ease-in-out infinite alternate;animation-play-state:var(--motion-play);}
  .shell[data-state="speaking"] .moon-svg{animation-duration:1.15s;}
  /* El analizador Web Audio reemplaza la simulación solamente durante captura real. */
  .shell[data-mic-live="true"][data-state="listening"] .waveform i{animation:none!important;}
  .shell[data-mic-live="true"][data-state="listening"] .waveform i{transition:transform .06s linear;}
  .voice-trigger{position:relative;overflow:hidden;transition:background .2s,border-color .2s,box-shadow .2s;
    border-color:rgba(105,240,255,.65);box-shadow:0 0 22px rgba(105,240,255,.15),inset 0 0 15px rgba(255,83,200,.10);}
  .voice-trigger::after{content:"";position:absolute;inset:0;transform:translateX(-130%);pointer-events:none;
    background:linear-gradient(90deg,transparent,rgba(191,248,255,.24),transparent);
    animation:glide 3.3s ease-in-out infinite;animation-play-state:var(--motion-play);}
  .shell[data-state="listening"] .voice-trigger{box-shadow:0 0 24px rgba(105,240,255,.28),0 0 46px rgba(255,83,200,.13);}
  .core-status strong{text-shadow:0 0 9px rgba(201,125,255,.20);}
  .bubble{animation:messageEntry .32s ease both;}
  .online-dot{animation:beacon 2.6s ease-in-out infinite;animation-play-state:var(--motion-play);}
  .ambient-line{height:2px;overflow:hidden;position:relative;opacity:.95;
    background:linear-gradient(90deg,transparent,rgba(105,240,255,.6),rgba(255,83,200,.9),transparent);}
  .ambient-line::after{content:"";position:absolute;top:0;left:0;height:100%;width:30%;
    background:linear-gradient(90deg,transparent,#fff,transparent);animation:glide 3.1s linear infinite;animation-play-state:var(--motion-play);}
  .motion-off *, .motion-off *::before, .motion-off *::after {animation:none!important;transition:none!important;}
  .motion-off .waveform i{transform:scaleY(.17)!important;}
  @keyframes floatCore {0%,100%{transform:translateY(-5px)}50%{transform:translateY(8px)}}
  @keyframes moonAlive {0%,100%{transform:scale(.98);opacity:.90;filter:drop-shadow(0 0 7px rgba(255,83,200,.45))}
    50%{transform:scale(1.05);opacity:1;filter:drop-shadow(0 0 21px rgba(105,240,255,.62))}}
  @keyframes breathSky {0%,100%{transform:scale(.98);opacity:.65}50%{transform:scale(1.07);opacity:1}}
  @keyframes coreGlow {0%,100%{transform:scale(.92);opacity:.5}50%{transform:scale(1.12);opacity:1}}
  @keyframes idlePulse {0%{transform:scaleY(.09)}100%{transform:scaleY(.26)}}
  @keyframes listenPulse {0%{transform:scaleY(.14)}100%{transform:scaleY(.89)}}
  @keyframes speechPulse {0%{transform:scaleY(.20)}100%{transform:scaleY(1)}}
  @keyframes thinkPulse {0%{transform:scaleY(.20)}100%{transform:scaleY(.64)}}
  @keyframes constellationCycle {0%,7%{opacity:0}12%,29%{opacity:.8}35%,100%{opacity:0}}
  @keyframes starTwinkle {0%,100%{opacity:.17;transform:scale(.7)}50%{opacity:.9;transform:scale(1.5)}}
  @keyframes techShimmer {0%,100%{opacity:.6}50%{opacity:1}}
  @keyframes beacon {0%,100%{opacity:.5;filter:brightness(1)}50%{opacity:1;filter:brightness(1.7)}}
  @keyframes glide {to{transform:translateX(390%)}}
  @keyframes messageEntry {from{opacity:0;transform:translateY(9px)}to{opacity:1;transform:translateY(0)}}
  @media(max-width:740px){.waveform{height:37px;margin-top:-12px;gap:3px}.waveform i{max-width:3px}.constellation-sky{opacity:.4}}
  @media(max-height:610px) and (min-width:741px){.waveform{height:43px}.orb{width:min(320px,100%,43vh)}}


/* LUNA 5.0 | Cyber Celestial — temas, efectos y optimizaciones */
:root {
  --l-primary:#bd46ff;--l-secondary:#ff52cd;--l-accent:#8a4cff;
  --l-primary-rgb:189,70,255;--l-secondary-rgb:255,82,205;
  --l-base:#070611;--l-panel:#110b20;--l-panel2:#1c1230;
  --l-text:#fbf4ff;--l-muted:#b8a5cd;--l-border:rgba(210,130,255,.27);
  --l-moon1:#fff2ff;--l-moon2:#e9a9ff;--l-moon3:#9227de;
}
html{color-scheme:dark}
body {color:var(--l-text);background:var(--l-base)}
.shell {
 background:
   radial-gradient(ellipse at 29% 22%,rgba(var(--l-primary-rgb),.20),transparent 33%),
   radial-gradient(ellipse at 83% 79%,rgba(var(--l-secondary-rgb),.10),transparent 44%),
   radial-gradient(ellipse at 50% 68%,rgba(var(--l-primary-rgb),.09),transparent 58%),
   var(--l-base);
 color:var(--l-text);
}
.shell:before {
 opacity:.5;
 background-image:radial-gradient(var(--l-moon1) .8px,transparent 1px),radial-gradient(var(--l-primary) .8px,transparent 1px);
}
.shell:after {background:repeating-linear-gradient(180deg,transparent 0 3px,rgba(var(--l-primary-rgb),.05) 3px 4px)}
.topbar {
 border-bottom:1px solid var(--l-border);
 background:linear-gradient(180deg,color-mix(in srgb,var(--l-panel) 92%,transparent),color-mix(in srgb,var(--l-panel) 70%,transparent));
 box-shadow:0 2px 28px rgba(var(--l-primary-rgb),.07),inset 0 -1px rgba(var(--l-primary-rgb),.08);
}
.identity{color:var(--l-text);text-shadow:0 0 18px rgba(var(--l-primary-rgb),.18)}
.identity em{color:var(--l-primary)}
.identity svg{filter:drop-shadow(0 0 10px var(--l-primary))}
.identity svg path{fill:var(--l-primary)}
.pill,.icon-button {
 background:color-mix(in srgb,var(--l-panel2) 70%,transparent);
 color:var(--l-text);border-color:var(--l-border);
 box-shadow:inset 0 0 12px rgba(var(--l-primary-rgb),.07);
}
.pill b{color:var(--l-primary)}
.icon-button:hover,.icon-button:focus-visible{border-color:var(--l-primary);background:rgba(var(--l-primary-rgb),.15)}
.rail {
 background:linear-gradient(180deg,color-mix(in srgb,var(--l-base) 92%,transparent),color-mix(in srgb,var(--l-panel) 73%,transparent));
 border-right:1px solid var(--l-border);
}
.rail-btn{color:var(--l-muted)}
.rail-btn.active,.rail-btn:hover{
 background:linear-gradient(130deg,rgba(var(--l-primary-rgb),.22),rgba(var(--l-secondary-rgb),.08));
 color:var(--l-text);border-color:var(--l-border);box-shadow:inset 0 0 20px rgba(var(--l-primary-rgb),.12),0 0 12px rgba(var(--l-primary-rgb),.08);
}
.rail-bottom{color:var(--l-muted)}
.stage:before{
 background:radial-gradient(circle,rgba(var(--l-primary-rgb),.22) 0,rgba(var(--l-secondary-rgb),.08) 34%,transparent 68%);
 animation:breathingFog 10s ease-in-out infinite;animation-play-state:var(--motion-play);
}
.stage:after{background:linear-gradient(180deg,transparent,rgba(var(--l-primary-rgb),.22))}
.eyebrow{color:var(--l-primary);text-shadow:0 0 10px var(--l-primary);font-size:11px;font-weight:600;letter-spacing:4px}
.orb{filter:drop-shadow(0 0 28px rgba(var(--l-primary-rgb),.20)) drop-shadow(0 0 42px rgba(var(--l-secondary-rgb),.12))}
.orb::before{background:radial-gradient(circle,rgba(var(--l-primary-rgb),.18),rgba(var(--l-secondary-rgb),.11) 28%,transparent 66%)}
.orb::after{
 background:conic-gradient(from 0deg,transparent 0 31deg,var(--l-primary) 40deg 46deg,transparent 51deg 128deg,var(--l-secondary) 133deg 141deg,transparent 146deg 271deg,var(--l-primary) 282deg 289deg,transparent 293deg 360deg);
}
.halo.outer{border-color:rgba(var(--l-primary-rgb),.25);border-top:3px solid var(--l-primary);border-bottom:1px dashed var(--l-secondary);filter:drop-shadow(0 0 11px var(--l-primary))}
.halo.middle{border-color:rgba(var(--l-primary-rgb),.45);border-left:3px solid var(--l-secondary)}
.halo.inner{border-color:rgba(var(--l-primary-rgb),.26);border-top:3px solid var(--l-primary)}
.halo.ticks{background:repeating-conic-gradient(from 4deg,var(--l-primary) 0deg 1deg,transparent 1deg 11deg)}
.moon-svg{filter:drop-shadow(0 0 15px rgba(var(--l-primary-rgb),.72)) drop-shadow(0 0 35px rgba(var(--l-secondary-rgb),.3))}
#moonshade stop:nth-child(1){stop-color:var(--l-moon1)}
#moonshade stop:nth-child(2){stop-color:var(--l-moon2)}
#moonshade stop:nth-child(3){stop-color:var(--l-primary)}
#moonshade stop:nth-child(4){stop-color:var(--l-moon3)}
.orbit-curve ellipse{stroke:var(--l-primary)}
.orbit-curve circle{fill:var(--l-secondary)}
.orb-star{background:var(--l-moon1);box-shadow:0 0 19px 4px rgba(var(--l-primary-rgb),.8)}
.constellation-sky .path{stroke:var(--l-primary)}
.constellation-sky .point{fill:var(--l-moon1);filter:drop-shadow(0 0 6px var(--l-primary))}
.spark{background:var(--l-primary);box-shadow:0 0 9px var(--l-primary)}
.spark.magenta{background:var(--l-secondary);box-shadow:0 0 10px var(--l-secondary)}
.waveform{filter:drop-shadow(0 0 12px rgba(var(--l-primary-rgb),.3))}
.waveform i{
 background:linear-gradient(180deg,var(--l-moon1),var(--l-primary),var(--l-secondary));
 box-shadow:0 0 12px rgba(var(--l-primary-rgb),.46);
}
.shell[data-state="listening"] .waveform{filter:drop-shadow(0 0 16px var(--l-primary))}
.shell[data-state="speaking"] .waveform{filter:drop-shadow(0 0 15px var(--l-secondary))}
.shell[data-state="listening"] .orb{filter:drop-shadow(0 0 38px var(--l-primary))}
.core-status strong{color:var(--l-text);text-shadow:0 0 14px rgba(var(--l-primary-rgb),.40)}
.core-status span{color:var(--l-muted)}
.voice-trigger{border-color:var(--l-primary);color:var(--l-text);
 background:linear-gradient(130deg,rgba(var(--l-primary-rgb),.21),rgba(var(--l-secondary-rgb),.09));
 box-shadow:0 0 22px rgba(var(--l-primary-rgb),.25),inset 0 0 15px rgba(var(--l-primary-rgb),.08)}
.voice-trigger:hover{background:rgba(var(--l-primary-rgb),.25);border-color:var(--l-moon1)}
.ambient-line{background:linear-gradient(90deg,transparent,var(--l-primary),var(--l-secondary),transparent);box-shadow:0 0 10px rgba(var(--l-primary-rgb),.45)}
.conversation{border-color:var(--l-border);
 background:linear-gradient(160deg,color-mix(in srgb,var(--l-panel) 95%,transparent),color-mix(in srgb,var(--l-base) 92%,transparent));
}
.conversation-head{border-bottom:1px solid var(--l-border);color:var(--l-text)}
.conversation-head small{color:var(--l-muted)}
.thread{background-image:linear-gradient(rgba(var(--l-primary-rgb),.045) 1px,transparent 1px),linear-gradient(90deg,rgba(var(--l-primary-rgb),.045) 1px,transparent 1px);background-size:32px 32px;}
.bubble.luna{background:linear-gradient(145deg,color-mix(in srgb,var(--l-panel2) 94%,transparent),color-mix(in srgb,var(--l-panel) 94%,transparent));border:1px solid var(--l-border);color:var(--l-text)}
.bubble.user{background:linear-gradient(135deg,rgba(var(--l-primary-rgb),.19),rgba(var(--l-secondary-rgb),.13));border:1px solid var(--l-border);color:var(--l-text)}
.bubble.system{background:color-mix(in srgb,var(--l-panel2) 86%,transparent);border-color:var(--l-border);color:var(--l-text)}
.bubble-label{color:var(--l-primary)}
.composer{border-top:1px solid var(--l-border);background:var(--l-panel)}
.composer textarea{background:var(--l-base);border:1px solid var(--l-border);color:var(--l-text);box-shadow:inset 0 0 12px rgba(var(--l-primary-rgb),.03)}
.composer textarea:focus{outline:1px solid var(--l-primary);box-shadow:0 0 15px rgba(var(--l-primary-rgb),.15)}
.composer textarea::placeholder{color:var(--l-muted)}
.send{background:linear-gradient(130deg,var(--l-primary),var(--l-secondary));color:#fff;box-shadow:0 0 25px rgba(var(--l-primary-rgb),.22)}
.overlay{background:rgba(3,3,10,.80)}
.dialog{width:min(690px,100%);max-height:min(88vh,770px);overflow:auto;border:1px solid var(--l-border);background:linear-gradient(165deg,var(--l-panel2),var(--l-panel));color:var(--l-text);box-shadow:0 28px 80px rgba(0,0,0,.65),0 0 35px rgba(var(--l-primary-rgb),.09)}
.dialog h2{font-size:22px;letter-spacing:.4px}
.dialog p{color:var(--l-muted)}
.dialog .subhead{font-size:10px;letter-spacing:3px;text-transform:uppercase;color:var(--l-primary);font-weight:700;margin:22px 0 11px}
.setting{border-bottom:1px solid var(--l-border);font-size:13px;justify-content:space-between}
.setting input[type=checkbox]{accent-color:var(--l-primary)}
.close-dialog{border-color:var(--l-primary);color:var(--l-text);background:rgba(var(--l-primary-rgb),.22)}
.theme-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px}
.theme-tile{min-width:0;min-height:90px;display:flex;flex-direction:column;align-items:flex-start;justify-content:space-between;text-align:left;gap:9px;
 border:1px solid var(--l-border);border-radius:15px;color:var(--l-text);padding:11px;background:var(--l-panel);transition:transform .2s,border-color .2s,box-shadow .2s}
.theme-tile:hover{transform:translateY(-2px);border-color:var(--l-primary)}
.theme-tile[aria-pressed="true"]{border-color:var(--l-primary);box-shadow:0 0 0 1px var(--l-primary),0 0 18px rgba(var(--l-primary-rgb),.18)}
.theme-swatches{height:25px;width:100%;display:flex;align-items:center;gap:7px}
.theme-dot{width:22px;height:22px;border-radius:50%;border:1px solid rgba(255,255,255,.5);box-shadow:0 0 15px currentColor}
.theme-tile small{font-size:11px;font-weight:600;color:inherit}
.custom-row{display:flex;gap:12px;align-items:center;justify-content:space-between;margin-top:12px;padding:12px;border:1px solid var(--l-border);border-radius:13px}
.custom-row label{font-size:12px}
.custom-row input[type=color]{width:42px;height:32px;padding:2px;border:1px solid var(--l-border);background:var(--l-panel);border-radius:8px;cursor:pointer}
.custom-btn{border:1px solid var(--l-border);border-radius:11px;background:rgba(var(--l-primary-rgb),.18);color:var(--l-text);padding:8px 10px;font-size:11px}
.brain-select{border:1px solid var(--l-border);border-radius:10px;color:var(--l-text);background:var(--l-base);padding:7px;width:min(220px,100%)}
.dialog-note{font-size:11px;line-height:1.5;margin:8px 0}
.tech-chip{position:absolute;z-index:1;bottom:11%;left:6%;color:var(--l-muted);font-size:9px;letter-spacing:2px;opacity:.6;pointer-events:none}
.tech-chip.right{left:auto;right:6%}
.cosmic-ring{position:absolute;inset:1%;border-radius:50%;pointer-events:none;
 background:conic-gradient(from 0deg,transparent 0deg 42deg,rgba(var(--l-primary-rgb),.14) 43deg 61deg,transparent 62deg 185deg,rgba(var(--l-secondary-rgb),.17) 188deg 198deg,transparent 199deg 360deg);
 mask:radial-gradient(circle,transparent 64%,#000 65% 66%,transparent 67%);
 animation:orbit 32s linear infinite reverse;animation-play-state:var(--motion-play)
}
.cosmic-mist{position:absolute;inset:7%;border-radius:50%;pointer-events:none;
 background:conic-gradient(from -12deg,transparent 0deg 70deg,rgba(var(--l-primary-rgb),.28) 101deg,transparent 145deg 230deg,rgba(var(--l-secondary-rgb),.24) 254deg,transparent 311deg 360deg);
 filter:blur(28px);opacity:.7;animation:cosmicSpin 25s linear infinite;animation-play-state:var(--motion-play)
}
.stage-corners{position:absolute;inset:18px;z-index:0;pointer-events:none;opacity:.4;
 background:linear-gradient(var(--l-primary),var(--l-primary)) top left/27px 1px no-repeat,
 linear-gradient(var(--l-primary),var(--l-primary)) top left/1px 27px no-repeat,
 linear-gradient(var(--l-secondary),var(--l-secondary)) bottom right/27px 1px no-repeat,
 linear-gradient(var(--l-secondary),var(--l-secondary)) bottom right/1px 27px no-repeat;}
@keyframes cosmicSpin{to{transform:rotate(360deg)}}
@keyframes breathingFog{50%{transform:scale(1.13);opacity:.55}}
@media(max-width:750px){.theme-grid{grid-template-columns:repeat(2,minmax(0,1fr))}.tech-chip{display:none}.dialog{padding:15px}}
@media(max-width:430px){.custom-row{gap:7px;flex-wrap:wrap}.theme-grid{gap:7px}.theme-tile{min-height:76px;padding:9px}.dialog{max-height:90vh}}
/* Tema blanco auténtico; no solo neón blanco sobre fondo negro. */
html.theme-light{color-scheme:light}
html.theme-light .identity{color:#1c2033}
html.theme-light .pill,html.theme-light .icon-button{color:#303347}
html.theme-light .rail-btn.active,html.theme-light .rail-btn:hover{color:#242439}
html.theme-light .online-dot{background:#149b6e}
html.theme-light .voice-trigger{color:#24243a}
html.theme-light .topbar{background:rgba(255,255,255,.91)}
html.theme-light .bubble.luna{background:rgba(255,255,255,.88)}
html.theme-light .bubble.user{background:rgba(216,222,244,.90)}
html.theme-light .theme-tile{background:#eef0f8}
html.theme-light .theme-tile small{color:#31364a}
html.theme-light .close-dialog,html.theme-light .custom-btn{color:#27273b}
html.theme-light .send{color:#1f1e2f}
html.theme-light .stage:before{opacity:.25}
html.eco .shell:after, html.eco .cosmic-mist,html.eco .stage:after{display:none}
html.eco .orb,html.eco .moon-svg,html.eco .stage:before{filter:none}
html.eco .spark:nth-child(n+22){display:none}
html.eco .halo.outer{animation-duration:25s}
html.sky-off .starfield,html.sky-off .constellation-sky{display:none}
</style>
</head>
<body>
<div class="shell" id="shell" data-state="idle">
  <header class="topbar">
    <div class="identity" aria-label="Luna AI">
      <svg viewBox="0 0 40 40" aria-hidden="true"><path d="M20 3a17 17 0 1 0 17 24A16 16 0 0 1 20 3Z" fill="#ddafff"/></svg>
      <span>LUNA <em>AI</em></span>
    </div>
    <div class="top-center"><span class="pill"><span class="online-dot"></span> En línea</span>
      <span class="pill" id="brainChip">✧ Gemini <b>principal</b></span>
    </div>
    <div class="top-actions">
      <button class="demo-topbar" id="voiceDemoOpen" type="button" title="Probar una grabación con la animación de Luna">♫ <span id="voiceDemoTopLabel">Probar voz</span></button>
      <button class="icon-button" id="quickTheme" title="Cambiar color de Luna" aria-label="Cambiar tema de color">◈</button>
      <button class="icon-button" id="settingsButton" title="Configuración" aria-label="Configuración">⚙</button>
    </div>
  </header>
  <main class="workspace">
    <nav class="rail" aria-label="Menú de Luna">
      <button class="rail-btn active" id="navChat" title="Chat" aria-label="Chat">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M4 5h16v12H9l-5 4V5Z"/></svg><span>Chat</span>
      </button>
      <button class="rail-btn" id="navVoice" title="Hablar con Luna" aria-label="Hablar con Luna">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><rect x="9" y="3" width="6" height="12" rx="3"/><path d="M5 11a7 7 0 0 0 14 0M12 18v3M9 21h6"/></svg><span>Voz</span>
      </button>
      <button class="rail-btn muted" title="Funciones creativas próximamente" disabled aria-label="Crear: próximamente">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="m12 2 1.8 7.2L21 11l-7.2 1.8L12 20l-1.8-7.2L3 11l7.2-1.8L12 2Z"/></svg><span>Crear</span>
      </button>
      <button class="rail-btn muted" title="Organización próximamente" disabled aria-label="Organizar: próximamente">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><rect x="3" y="5" width="18" height="16" rx="2"/><path d="M7 3v4M17 3v4M3 10h18"/></svg><span>Agenda</span>
      </button>
      <button class="rail-btn" id="navSettings" title="Ajustes" aria-label="Ajustes">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><circle cx="12" cy="12" r="3"/><path d="M9 2h6l1 3 3 2 3-1v6l-3 1-1 3 2 3-5 3-2-3-3 0-2 3-5-3 2-3-1-3-3-1V6l3 1 3-2 1-3Z"/></svg><span>Ajustes</span>
      </button>
      <div class="rail-bottom">LUNA · CELESTIAL</div>
    </nav>
    <section class="stage" aria-label="Núcleo visual de Luna">
      <div class="starfield" id="starfield" aria-hidden="true"></div>
      <svg class="constellation-sky" viewBox="0 0 480 440" preserveAspectRatio="none" aria-hidden="true">
        <g class="constellation"><polyline class="path" points="90,105 138,76 175,122 236,150 270,227 322,181 373,250"/>
          <circle class="point" cx="90" cy="105" r="2.5"/><circle class="point" cx="138" cy="76" r="3.5"/>
          <circle class="point" cx="175" cy="122" r="2.5"/><circle class="point" cx="236" cy="150" r="3"/>
          <circle class="point" cx="270" cy="227" r="2.5"/><circle class="point" cx="322" cy="181" r="3"/>
          <circle class="point" cx="373" cy="250" r="2.5"/></g>
        <g class="constellation"><polyline class="path" points="65,294 123,244 185,277 242,215 300,259"/>
          <circle class="point" cx="65" cy="294" r="3"/><circle class="point" cx="123" cy="244" r="2.5"/>
          <circle class="point" cx="185" cy="277" r="3.5"/><circle class="point" cx="242" cy="215" r="2.5"/>
          <circle class="point" cx="300" cy="259" r="3"/></g>
        <g class="constellation"><polyline class="path" points="86,170 147,132 207,162 254,212 317,197 380,144 405,102"/>
          <circle class="point" cx="86" cy="170" r="3"/><circle class="point" cx="147" cy="132" r="3.5"/>
          <circle class="point" cx="207" cy="162" r="2.5"/><circle class="point" cx="254" cy="212" r="3"/>
          <circle class="point" cx="317" cy="197" r="3.5"/><circle class="point" cx="380" cy="144" r="3"/>
          <circle class="point" cx="405" cy="102" r="2.5"/></g>
      </svg>
      <div class="stage-corners" aria-hidden="true"></div>
      <span class="tech-chip" aria-hidden="true">LUNA / SYNC 03</span>
      <span class="tech-chip right" aria-hidden="true">CELESTIAL · ACTIVE</span>
      <div class="eyebrow">✦  LUNA CORE  ·  CELESTIAL  ✦</div>
      <div class="orb" aria-hidden="true">
        <div class="cosmic-mist"></div><div class="cosmic-ring"></div>
        <div class="halo outer"></div><div class="halo middle"></div><div class="halo inner"></div><div class="halo ticks"></div>
        <svg class="orbit-curve" viewBox="0 0 300 300"><ellipse cx="150" cy="150" rx="145" ry="40" transform="rotate(-23 150 150)" stroke="#c08bfa" stroke-width=".8" fill="none" opacity=".55"/><circle cx="278" cy="106" r="2.5" fill="#ffe5ff"/></svg>
        <svg class="moon-svg" viewBox="0 0 240 240">
          <defs>
            <linearGradient id="moonshade" x1="0%" y1="0%" x2="75%" y2="100%"><stop offset="0" stop-color="#fff4ff"/><stop offset=".35" stop-color="#ddabfc"/><stop offset=".8" stop-color="#bd7dec"/><stop offset="1" stop-color="#7e4ead"/></linearGradient>
            <filter id="moontexture" x="-10%" y="-10%" width="120%" height="120%"><feTurbulence type="fractalNoise" baseFrequency=".07" numOctaves="3" seed="6" result="noise"/><feColorMatrix in="noise" type="saturate" values="0" result="gray"/><feBlend in="SourceGraphic" in2="gray" mode="soft-light"/></filter>
            <mask id="crescentmask"><rect width="240" height="240" fill="black"/><circle cx="120" cy="120" r="87" fill="white"/><circle cx="161" cy="77" r="85" fill="black"/></mask>
          </defs>
          <circle cx="120" cy="120" r="87" fill="url(#moonshade)" mask="url(#crescentmask)" filter="url(#moontexture)"/>
          <circle cx="120" cy="120" r="87" stroke="#f2ceff" stroke-width=".7" fill="none" mask="url(#crescentmask)"/>
        </svg>
        <span class="orb-star one"></span><span class="orb-star two"></span><span class="orb-star three"></span>
      </div>
      <div class="waveform" id="visualizer" aria-hidden="true">
        <i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i>
      </div>
      <div class="core-status" role="status" aria-live="polite"><strong id="stateTitle">Luna está lista</strong><span id="stateMessage">Escribe o pulsa el botón para hablar.</span></div>
      <button id="micButton" class="voice-trigger" type="button">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><rect x="9" y="3" width="6" height="12" rx="3"/><path d="M5 11a7 7 0 0 0 14 0M12 18v3"/></svg><span id="micButtonText">Hablar con Luna</span>
      </button>
      <div class="ambient-line"></div>
    </section>
    <section class="conversation" aria-label="Chat con Luna">
      <div class="conversation-head"><strong>Conversación</strong><small id="brainInfo">Gemini</small></div>
      <div class="thread" id="thread" role="log" aria-label="Mensajes de Luna" aria-live="polite">
        <div class="bubble luna"><span class="bubble-label">☾ LUNA</span>Hola, soy Luna. Ya estoy en línea. ¿Qué deseas hacer conmigo esta noche?</div>
      </div>
    </section>
    <div class="overlay demo-overlay" id="demoOverlay" hidden>
      <section class="dialog demo-dialog" role="dialog" aria-modal="true" aria-labelledby="demoTitle">
        <div class="settings-heading"><h2 id="demoTitle">☾ Probar voz de Luna</h2>
          <button class="settings-close" id="demoClose" type="button" aria-label="Cerrar la prueba">×</button></div>
        <p class="dialog-note">Elige el audio WAV que generaste con Qwen3-TTS. Luna reproducirá la muestra mientras el núcleo y las barras reaccionan al sonido real.</p>
        <label class="demo-label" for="demoVoiceFile">1 · Selecciona tu grabación</label>
        <input class="demo-file" type="file" id="demoVoiceFile" accept="audio/*,.wav,.mp3,.ogg,.m4a">
        <div class="demo-file-status" id="demoFileStatus">Ningún audio seleccionado.</div>
        <label class="demo-label" for="demoVoiceText">2 · Texto que escucharás (opcional)</label>
        <textarea class="demo-transcript" id="demoVoiceText" rows="3" maxlength="600">Hola, ¿cómo estás? Soy Luna. Hoy estoy un poquito cansada, pero me alegra hablar contigo. Cuéntame cómo te fue.</textarea>
        <div class="demo-actions">
          <button class="demo-btn demo-play" id="demoPlay" type="button" disabled>▶ Reproducir y animar</button>
          <button class="demo-btn demo-cancel" id="demoCancel" type="button">Cancelar</button>
        </div>
        <p class="demo-privacy">🔒 El audio se reproduce localmente en tu navegador: no se sube a GitHub ni a nuestro servidor. Es una prueba, no clonación en tiempo real.</p>
        <p class="demo-error" id="demoError" role="alert" hidden></p>
      </section>
    </div>
    <div class="overlay" id="settingsOverlay" hidden>
      <section class="dialog" role="dialog" aria-modal="false" aria-labelledby="settingsTitle">
        <div class="settings-heading"><h2 id="settingsTitle">⚙ Ajustes de Luna</h2>
          <button class="settings-close" id="closeSettings" type="button" aria-label="Cerrar ajustes">×</button></div>
        <div class="settings-tabs" role="tablist" aria-label="Secciones de configuración">
          <button type="button" class="settings-tab" data-settings-tab="general" role="tab" aria-selected="false">☷ General</button>
          <button type="button" class="settings-tab" data-settings-tab="theme" role="tab" aria-selected="true">◈ Tema</button>
          <button type="button" class="settings-tab" data-settings-tab="voice" role="tab" aria-selected="false">♬ Voz</button>
        </div>
        <div class="settings-pane" data-settings-pane="theme" role="tabpanel">
          <div class="subhead">Tema de color</div>
          <p class="dialog-note">Personaliza el universo de Luna. Elige uno de los 25 colores o crea el tuyo.</p>
          <div class="theme-grid" id="themeGrid" role="group" aria-label="Temas de color"></div>
          <div class="custom-row">
            <label for="customColor">✦ Mi color</label>
            <input type="color" id="customColor" value="#bd46ff" aria-label="Elegir color principal">
            <button class="custom-btn" id="customApply" type="button">Aplicar</button>
          </div>
        </div>
        <div class="settings-pane" data-settings-pane="general" role="tabpanel" hidden>
          <div class="subhead">Inteligencia</div>
          <p class="dialog-note">Elige qué cerebro responde primero. Los demás quedarán como respaldo automático si falla.</p>
          <label class="setting" for="brainChoice">Cerebro principal
            <select id="brainChoice" class="brain-select">
              <option value="claude">Claude primero</option>
              <option value="openai">GPT primero</option>
              <option value="gemini">Gemini primero</option>
              <option value="openrouter">OpenRouter primero</option>
            </select>
          </label>
          <div class="subhead">Experiencia holográfica</div>
          <label class="setting">Animaciones del núcleo <input type="checkbox" id="motionToggle" checked></label>
          <label class="setting">Estrellas y constelaciones <input type="checkbox" id="skyToggle" checked></label>
          <label class="setting">Modo ligero <input type="checkbox" id="ecoToggle"></label>
        </div>
        <div class="settings-pane" data-settings-pane="voice" role="tabpanel" hidden>
          <div class="subhead">Voz de Luna</div>
          <label class="setting">Leer respuestas en voz alta <input type="checkbox" id="voiceToggle" checked></label>
          <p class="dialog-note">Luna utiliza ElevenLabs si está disponible. En caso contrario, intenta usar Microsoft Sabina y después responde por escrito.</p>
          <p class="dialog-note">Al dictar, tus palabras se acumulan. Luna solo envía la pregunta cuando pulsas «Terminar y enviar».</p>
        </div>
      </section>
    </div>
      <form class="composer" id="chatForm">
        <textarea id="userInput" rows="2" maxlength="2000" placeholder="Escribe o habla con Luna..." aria-label="Mensaje para Luna"></textarea>
        <button class="send" id="sendButton" type="submit"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 2 11 13M22 2l-7 20-4-9-9-4Z"/></svg><span>Enviar</span></button>
      </form>
  </main>
</div>
<script>
(function () {
  "use strict";
  const shell = document.getElementById("shell");
  const form = document.getElementById("chatForm");
  const input = document.getElementById("userInput");
  const thread = document.getElementById("thread");
  const stateTitle = document.getElementById("stateTitle");
  const stateMessage = document.getElementById("stateMessage");
  const brainInfo = document.getElementById("brainInfo");
  const sendButton = document.getElementById("sendButton");
  const micButton = document.getElementById("micButton");
  const micText = document.getElementById("micButtonText");
  const settings = document.getElementById("settingsOverlay");
  const voiceToggle = document.getElementById("voiceToggle");
  const motionToggle = document.getElementById("motionToggle");
  const skyToggle = document.getElementById("skyToggle");
  const ecoToggle = document.getElementById("ecoToggle");
  const brainChoice = document.getElementById("brainChoice");
  const brainChip = document.getElementById("brainChip");
  const themeGrid = document.getElementById("themeGrid");
  const customColor = document.getElementById("customColor");
  const themeQuick = document.getElementById("quickTheme");
  const demoOpen = document.getElementById("voiceDemoOpen");
  const demoTopLabel = document.getElementById("voiceDemoTopLabel");
  const demoOverlay = document.getElementById("demoOverlay");
  const demoClose = document.getElementById("demoClose");
  const demoCancel = document.getElementById("demoCancel");
  const demoFile = document.getElementById("demoVoiceFile");
  const demoFileStatus = document.getElementById("demoFileStatus");
  const demoText = document.getElementById("demoVoiceText");
  const demoPlay = document.getElementById("demoPlay");
  const demoError = document.getElementById("demoError");
  let demoAudio = new Audio();
  let demoObjectUrl = null;
  let demoCtx = null;
  let demoAnalyser = null;
  let demoBuffer = null;
  let demoRaf = null;
  let demoPlaying = false;
  let demoLastDraw = 0;
  let busy = false;
  let rec = null;
  let elevenUnavailable = false;
  // La pregunta no se enviara hasta pulsar «Terminar y enviar».
  let dictando = false;
  let textoAnterior = "";
  let segmentosGuardados = [];
  let finalesActuales = "";
  let parcialActual = "";
  let reintentosMicrofono = 0;
  let reinicioMicrofono = null;
  let enviandoDictado = false;
  let esperaCierre = null;


  // Preferencias de Luna: solo se guardan en el navegador, nunca las claves API.
  const preferenceKey = "luna-ai-prefs-v5";
  const themes = [
    {id:"violet",label:"Violeta Lunar",primary:"#bd46ff",secondary:"#ff52cd",base:"#070611",panel:"#110b20",panel2:"#1c1230",text:"#fbf4ff",muted:"#b8a5cd",light:false},
    {id:"scarlet",label:"Cyber Red",primary:"#ff355b",secondary:"#ff944c",base:"#100609",panel:"#200b12",panel2:"#34111c",text:"#fff3f5",muted:"#d6a9b3",light:false},
    {id:"azure",label:"Azul Estelar",primary:"#39a5ff",secondary:"#46eaff",base:"#050d18",panel:"#0a1728",panel2:"#10213a",text:"#eff9ff",muted:"#a0c1d9",light:false},
    {id:"solar",label:"Ámbar Solar",primary:"#ffbd35",secondary:"#ff7b35",base:"#120e06",panel:"#201808",panel2:"#352309",text:"#fff9ec",muted:"#d7c6a0",light:false},
    {id:"white",label:"Blanco Lunar",primary:"#8b70f5",secondary:"#80c5ff",base:"#f4f5fb",panel:"#ffffff",panel2:"#e7eaf5",text:"#20253a",muted:"#606982",light:true},
    {id:"obsidian",label:"Obsidiana",primary:"#929aae",secondary:"#d1d7e9",base:"#050508",panel:"#0e0e15",panel2:"#191923",text:"#f0f0f7",muted:"#a2a2b5",light:false},
    {id:"emerald",label:"Verde Quantum",primary:"#30efb7",secondary:"#58e3e7",base:"#03100d",panel:"#08231c",panel2:"#0e3429",text:"#e9fff7",muted:"#97c7b4",light:false},
    {id:"rose",label:"Rosa Nebulosa",primary:"#f961ac",secondary:"#d596ff",base:"#140813",panel:"#210e23",panel2:"#341637",text:"#fff1fb",muted:"#d4acce",light:false},
    {id:"plasma",label:"Plasma",primary:"#a129ff",secondary:"#ff1ef2",base:"#0b0415",panel:"#160921",panel2:"#220a32",text:"#fff1ff",muted:"#c5a7da",light:false},
    {id:"fuchsia",label:"Fucsia Cósmico",primary:"#ff28de",secondary:"#b12aff",base:"#130613",panel:"#250a25",panel2:"#360d37",text:"#fff0fb",muted:"#dfaad3",light:false},
    {id:"amethyst",label:"Amatista",primary:"#9769ff",secondary:"#d991ff",base:"#090618",panel:"#120c26",panel2:"#21133e",text:"#f8f2ff",muted:"#bcafdb",light:false},
    {id:"indigo",label:"Índigo",primary:"#6c60ff",secondary:"#b057ff",base:"#060617",panel:"#0c0e2c",panel2:"#17184a",text:"#f4f4ff",muted:"#acacdc",light:false},
    {id:"sapphire",label:"Zafiro",primary:"#176bff",secondary:"#55aeff",base:"#040a18",panel:"#0a1632",panel2:"#0d2250",text:"#edf4ff",muted:"#aac3e9",light:false},
    {id:"aqua",label:"Aqua Galáctico",primary:"#11edec",secondary:"#4abfff",base:"#031219",panel:"#06222a",panel2:"#0c3844",text:"#e7ffff",muted:"#8abdc8",light:false},
    {id:"mint",label:"Menta Astral",primary:"#76ffcb",secondary:"#53c8ff",base:"#061410",panel:"#0b251c",panel2:"#103a2c",text:"#effff9",muted:"#a5dac7",light:false},
    {id:"jade",label:"Jade",primary:"#00d78b",secondary:"#6affd2",base:"#04120c",panel:"#092217",panel2:"#0c3523",text:"#effff7",muted:"#99d1b3",light:false},
    {id:"lime",label:"Lima Nuclear",primary:"#b3ff46",secondary:"#4bff9d",base:"#0b1204",panel:"#162009",panel2:"#24340e",text:"#f5ffe9",muted:"#b6d19e",light:false},
    {id:"ruby",label:"Rubí",primary:"#ff215e",secondary:"#ff6294",base:"#16040a",panel:"#270813",panel2:"#3d0a1c",text:"#fff0f6",muted:"#e0a7b8",light:false},
    {id:"coral",label:"Coral",primary:"#ff6e77",secondary:"#ffb17b",base:"#170a0d",panel:"#281216",panel2:"#3b1c22",text:"#fff6f4",muted:"#dfb8b4",light:false},
    {id:"sunset",label:"Atardecer",primary:"#ff753b",secondary:"#fc45aa",base:"#16090a",panel:"#2a1111",panel2:"#3e1b17",text:"#fff4e9",muted:"#ddafa5",light:false},
    {id:"copper",label:"Cobre",primary:"#cc824a",secondary:"#ffc38c",base:"#120b07",panel:"#21140e",panel2:"#352015",text:"#fff5e9",muted:"#d2b7a3",light:false},
    {id:"pearl",label:"Perla",primary:"#a09bcc",secondary:"#decfff",base:"#faf8ff",panel:"#ffffff",panel2:"#efebfa",text:"#29243b",muted:"#746d85",light:true},
    {id:"midnight",label:"Medianoche",primary:"#5476bb",secondary:"#8f6db8",base:"#03060f",panel:"#080d1b",panel2:"#121a2e",text:"#f0f4ff",muted:"#9ca9c0",light:false},
    {id:"graphite",label:"Grafito",primary:"#c0c0cb",secondary:"#7d8da6",base:"#090a0d",panel:"#15161b",panel2:"#23252d",text:"#f7f7fb",muted:"#b1b3c0",light:false},
    {id:"lilac",label:"Lavanda",primary:"#c69fff",secondary:"#f2c2ff",base:"#100b18",panel:"#1b1228",panel2:"#2b1c3b",text:"#fdf6ff",muted:"#cab8dc",light:false}
  ];
  let prefs = {theme:"violet",custom:"#bd46ff",brain:"gemini",motion:true,sky:true,eco:false,voice:true};
  try {
    const previousPrefs = JSON.parse(localStorage.getItem(preferenceKey) || "{}");
    if (previousPrefs && typeof previousPrefs === "object" && !Array.isArray(previousPrefs)) {
      for (const key of Object.keys(prefs)) {
        if (Object.prototype.hasOwnProperty.call(previousPrefs,key)) prefs[key] = previousPrefs[key];
      }
    }
  } catch (_) {} // En modo privado puede estar bloqueado.
  function savePrefs(){try{localStorage.setItem(preferenceKey,JSON.stringify(prefs));}catch(_){}}
  function validHex(value){return typeof value === "string" && /^#[0-9a-fA-F]{6}$/.test(value);}
  function rgbOf(hex){return [1,3,5].map(i=>parseInt(hex.slice(i,i+2),16)).join(",");}
  function lightenHex(hex,amount){
    return "#"+[1,3,5].map(i=>Math.round(parseInt(hex.slice(i,i+2),16)+(255-parseInt(hex.slice(i,i+2),16))*amount).toString(16).padStart(2,"0")).join("");
  }
  function darkenHex(hex,amount){
    return "#"+[1,3,5].map(i=>Math.round(parseInt(hex.slice(i,i+2),16)*(1-amount)).toString(16).padStart(2,"0")).join("");
  }
  function hexHue(hex){
    const r=parseInt(hex.slice(1,3),16)/255, g=parseInt(hex.slice(3,5),16)/255, b=parseInt(hex.slice(5,7),16)/255;
    const max=Math.max(r,g,b), min=Math.min(r,g,b), diff=max-min;
    if(diff===0) return 0;
    let h=max===r ? ((g-b)/diff)%6 : max===g ? (b-r)/diff+2 : (r-g)/diff+4;
    return (h*60+360)%360;
  }
  function colorTheme(id){
    if (id==="custom") {
      const primary = validHex(prefs.custom) ? prefs.custom : "#bd46ff";
      return {id:"custom",label:"Personalizado",primary,secondary:lightenHex(primary,.38),base:"#060810",panel:"#0d1220",panel2:"#191d31",text:"#f7f9ff",muted:"#aebcd2",light:false};
    }
    return themes.find(t=>t.id===id) || themes[0];
  }
  function applyTheme(id,save=true){
    const theme = colorTheme(id);
    const root = document.documentElement;
    root.dataset.theme = theme.id;
    root.classList.toggle("theme-light",theme.light);
    root.style.setProperty("--l-hue",((hexHue(theme.primary)-hexHue("#bd46ff")+360)%360)+"deg");
    root.style.setProperty("--l-primary",theme.primary);
    root.style.setProperty("--l-secondary",theme.secondary);
    root.style.setProperty("--l-accent",theme.primary);
    root.style.setProperty("--l-primary-rgb",rgbOf(theme.primary));
    root.style.setProperty("--l-secondary-rgb",rgbOf(theme.secondary));
    root.style.setProperty("--l-base",theme.base);
    root.style.setProperty("--l-panel",theme.panel);
    root.style.setProperty("--l-panel2",theme.panel2);
    root.style.setProperty("--l-text",theme.text);
    root.style.setProperty("--l-muted",theme.muted);
    root.style.setProperty("--l-border",`rgba(${rgbOf(theme.primary)},${theme.light?.37:.27})`);
    root.style.setProperty("--l-moon1",theme.light?"#fcffff":lightenHex(theme.primary,.90));
    root.style.setProperty("--l-moon2",lightenHex(theme.primary,.63));
    root.style.setProperty("--l-moon3",darkenHex(theme.primary,.35));
    document.querySelector('meta[name="theme-color"]').setAttribute("content",theme.base);
    document.querySelectorAll(".theme-tile").forEach(btn=>btn.setAttribute("aria-pressed",String(btn.dataset.themeId===theme.id)));
    themeQuick.title = "Tema actual: " + theme.label + " · Cambiar color";
    if(save){prefs.theme=theme.id;savePrefs();}
  }
  function makeThemeButtons(){
    for(const theme of themes){
      const btn=document.createElement("button");
      btn.type="button";btn.className="theme-tile";btn.dataset.themeId=theme.id;
      btn.setAttribute("aria-label","Activar tema "+theme.label);
      const colors=document.createElement("span");colors.className="theme-swatches";
      const dot=document.createElement("span");dot.className="theme-dot";
      dot.style.setProperty("--swatch-main",theme.primary);
      dot.style.setProperty("--swatch-secondary",theme.secondary);
      colors.appendChild(dot);
      const name=document.createElement("small");name.textContent=theme.label;
      btn.append(colors,name);btn.addEventListener("click",()=>applyTheme(theme.id));themeGrid.appendChild(btn);
    }
    const custom=document.createElement("button");custom.type="button";custom.className="theme-tile";custom.dataset.themeId="custom";
    custom.setAttribute("aria-label","Activar último color personalizado");
    custom.innerHTML='<span class="theme-swatches"><span class="theme-dot" id="customDot"></span></span><small>Mi color</small>';
    custom.addEventListener("click",()=>applyTheme("custom"));themeGrid.appendChild(custom);
  }
  makeThemeButtons();
  const settingsTabs = Array.from(document.querySelectorAll("[data-settings-tab]"));
  const settingsPanes = Array.from(document.querySelectorAll("[data-settings-pane]"));
  function showSettingsTab(name){
    for (const tab of settingsTabs) tab.setAttribute("aria-selected", String(tab.dataset.settingsTab === name));
    for (const pane of settingsPanes) pane.hidden = pane.dataset.settingsPane !== name;
  }
  for (const tab of settingsTabs) tab.addEventListener("click",()=>showSettingsTab(tab.dataset.settingsTab));
  showSettingsTab("theme");
  if(!validHex(prefs.custom)) prefs.custom="#bd46ff";
  customColor.value=prefs.custom;
  const customDot=document.getElementById("customDot");
  function refreshCustomDot(){customDot.style.setProperty("--swatch-main",prefs.custom);customDot.style.setProperty("--swatch-secondary",lightenHex(prefs.custom,.35));}
  refreshCustomDot();
  document.getElementById("customApply").addEventListener("click",()=>{
    prefs.custom=customColor.value;refreshCustomDot();applyTheme("custom");
  });
  const themeSequence=themes.map(t=>t.id);
  themeQuick.addEventListener("click",()=>{
    const index=themeSequence.indexOf(prefs.theme);
    applyTheme(themeSequence[(index+1)%themeSequence.length]);
  });
  applyTheme(prefs.theme,false);
  motionToggle.checked=prefs.motion!==false;
  skyToggle.checked=prefs.sky!==false;
  ecoToggle.checked=prefs.eco===true;
  voiceToggle.checked=prefs.voice!==false;
  brainChoice.value = ["claude","openai","gemini","openrouter"].includes(prefs.brain) ? prefs.brain : "gemini";
  document.documentElement.classList.toggle("motion-off",!motionToggle.checked);
  document.documentElement.classList.toggle("sky-off",!skyToggle.checked);
  document.documentElement.classList.toggle("eco",ecoToggle.checked);
  document.documentElement.style.setProperty("--motion-play",motionToggle.checked?"running":"paused");
  const BRAIN_NAMES = {claude:"Claude",openai:"GPT",gemini:"Gemini",openrouter:"OpenRouter"};
  function updateBrainBadge(){
    const name = BRAIN_NAMES[brainChoice.value] || "Gemini";
    brainChip.textContent = "✧ " + name + " principal · con respaldo automático";
    brainInfo.textContent = "Preferido: " + name;
  }
  updateBrainBadge();
  brainChoice.addEventListener("change",()=>{prefs.brain=brainChoice.value;savePrefs();updateBrainBadge();});
  skyToggle.addEventListener("change",()=>{prefs.sky=skyToggle.checked;document.documentElement.classList.toggle("sky-off",!prefs.sky);savePrefs();});
  ecoToggle.addEventListener("change",()=>{prefs.eco=ecoToggle.checked;document.documentElement.classList.toggle("eco",prefs.eco);savePrefs();});
  voiceToggle.addEventListener("change",()=>{prefs.voice=voiceToggle.checked;savePrefs();});
  // El usuario controla por completo la activación de las animaciones.
  motionToggle.addEventListener("change",()=>{prefs.motion=motionToggle.checked;savePrefs();});

  // Estrellas de fondo, distribuidas una sola vez. Sin Canvas ni dependencias externas.
  const starfield = document.getElementById("starfield");
  for (let index = 0; index < 42; index++) {
    const spark = document.createElement("span");
    spark.className = "spark" + (index % 6 === 0 ? " magenta" : "");
    spark.style.left = ((index * 37 + 13) % 97 + 1) + "%";
    spark.style.top = ((index * 29 + (index * index) % 23) % 89 + 4) + "%";
    spark.style.animationDelay = -(index % 17) * .31 + "s";
    spark.style.animationDuration = (2.2 + (index % 7) * .51) + "s";
    starfield.appendChild(spark);
  }
  const waveBars = Array.from(document.querySelectorAll("#visualizer i"));
  let audioStream = null;
  let audioContext = null;
  let audioAnalyser = null;
  let frequencies = null;
  let audioAnimationId = null;
  let audioSessionId = 0;
  let audioLastFrame = 0;

  function stopMicrophoneVisualization() {
    audioSessionId++;
    if (audioAnimationId !== null) cancelAnimationFrame(audioAnimationId);
    audioAnimationId = null;
    shell.dataset.micLive = "false";
    for (const bar of waveBars) bar.style.removeProperty("transform");
    if (audioStream) {
      for (const track of audioStream.getTracks()) track.stop();
      audioStream = null;
    }
    if (audioContext) {
      audioContext.close().catch(() => {});
      audioContext = null;
    }
    audioAnalyser = null;
    frequencies = null;
  }

  // Web Audio muestra el volumen real del micrófono cuando Chrome lo permite.
  // Si el navegador bloquea una segunda captura, continúa la animación CSS.
  async function startMicrophoneVisualization() {
    if (audioStream || audioContext || !dictando || !motionToggle.checked) return;
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) return;
    const AudioCtx = window.AudioContext || window.webkitAudioContext;
    if (!AudioCtx) return;
    const sessionId = ++audioSessionId;
    let stream;
    try {
      stream = await navigator.mediaDevices.getUserMedia({audio:{echoCancellation:true,noiseSuppression:true}});
      if (sessionId !== audioSessionId || !dictando || !motionToggle.checked) {
        for (const track of stream.getTracks()) track.stop();
        return;
      }
      audioStream = stream;
      audioContext = new AudioCtx();
      const source = audioContext.createMediaStreamSource(audioStream);
      audioAnalyser = audioContext.createAnalyser();
      audioAnalyser.fftSize = 256;
      audioAnalyser.smoothingTimeConstant = .68;
      source.connect(audioAnalyser);
      frequencies = new Uint8Array(audioAnalyser.frequencyBinCount);
      await audioContext.resume();
      if (sessionId !== audioSessionId || !dictando) {stopMicrophoneVisualization();return;}
      shell.dataset.micLive = "true";
      function draw(now) {
        if (sessionId !== audioSessionId || !dictando || !audioAnalyser || !motionToggle.checked) return;
        audioAnimationId = requestAnimationFrame(draw);
        if (now - audioLastFrame < 45) return; // unas 22 actualizaciones/s
        audioLastFrame = now;
        audioAnalyser.getByteFrequencyData(frequencies);
        const count = waveBars.length;
        for (let i = 0; i < count; i++) {
          // Combinación de bandas bajas y medias de voz, con rango mínimo visible.
          const bin = Math.min(frequencies.length-1, 2+Math.floor(i*1.2));
          const v = (frequencies[bin] + frequencies[Math.min(frequencies.length-1,bin+2)]) / 510;
          const center = 1-Math.abs(i-(count-1)/2)/((count-1)/2);
          const amp = Math.min(.98, .1 + Math.pow(v, .72)*1.8*(.6+.4*center));
          waveBars[i].style.transform = "scaleY(" + amp.toFixed(3) + ")";
        }
      }
      audioAnimationId = requestAnimationFrame(draw);
    } catch (_) {
      // Fallo visual no afecta al dictado: las barras CSS siguen animadas.
      if (stream && stream !== audioStream) for (const track of stream.getTracks()) track.stop();
      stopMicrophoneVisualization();
    }
  }

  // Reproducción de una muestra LOCAL: jamás se envía al backend.
  // Se conecta el reproductor al analizador Web Audio para animar las barras reales.
  function resetDemoBars() {
    for (const bar of waveBars) {bar.style.removeProperty("height");bar.style.removeProperty("transform");}
    const orb = document.querySelector(".orb");
    if (orb) orb.style.removeProperty("transform");
  }
  function stopDemo() {
    if (!demoPlaying && demoAudio.paused) return;
    demoPlaying = false;
    demoAudio.pause();
    try {demoAudio.currentTime = 0;} catch (_) {}
    if (demoRaf !== null) cancelAnimationFrame(demoRaf);
    demoRaf = null;
    if (demoCtx && demoCtx.state === "running") demoCtx.suspend().catch(() => {});
    shell.dataset.demo = "off";
    demoTopLabel.textContent = "Probar voz";
    demoOpen.classList.remove("demo-active");
    resetDemoBars();
    setState("idle", "Luna está lista", "La prueba terminó. Puedes continuar conversando.");
  }
  function drawDemo(now) {
    if (!demoPlaying) return;
    demoRaf = requestAnimationFrame(drawDemo);
    if (!motionToggle.checked || !demoAnalyser || !demoBuffer || now - demoLastDraw < 50) return;
    demoLastDraw = now;
    demoAnalyser.getByteFrequencyData(demoBuffer);
    let sum = 0;
    for (let i = 0; i < waveBars.length; i++) {
      const bin = Math.min(demoBuffer.length-2, 2+Math.floor(i*1.6));
      const v = (demoBuffer[bin] + demoBuffer[bin+1]) / 510;
      sum += v;
      const center = 1-Math.abs(i-(waveBars.length-1)/2)/((waveBars.length-1)/2);
      const height = Math.round(5 + Math.min(1,v*3.3)*(24+17*center));
      waveBars[i].style.height = height + "px";
      waveBars[i].style.transform = "scaleY(1)";
    }
    const level = sum / waveBars.length;
    const orb = document.querySelector(".orb");
    if (orb) orb.style.transform = "scale("+(1+Math.min(.075,level*.29)).toFixed(3)+")";
  }
  function hideDemo() {demoOverlay.hidden = true;}
  function openDemo() {
    if (busy || enviandoDictado) return;
    if (demoPlaying) {stopDemo();return;}
    if (dictando) stopRecognition(); // No envía el dictado de manera automática.
    demoError.hidden = true;
    demoOverlay.hidden = false;
    demoFile.focus({preventScroll:true});
  }
  demoOpen.addEventListener("click",openDemo);
  demoClose.addEventListener("click",hideDemo);
  demoCancel.addEventListener("click",hideDemo);
  demoOverlay.addEventListener("click",e=>{if(e.target===demoOverlay)hideDemo();});
  demoFile.addEventListener("change",()=>{
    if (demoPlaying) stopDemo();
    const file = demoFile.files && demoFile.files[0];
    if (demoObjectUrl) {URL.revokeObjectURL(demoObjectUrl);demoObjectUrl=null;}
    demoAudio.removeAttribute("src");demoAudio.load();
    demoError.hidden = true;
    if (!file) {demoFileStatus.textContent="Ningún audio seleccionado.";demoPlay.disabled=true;return;}
    if (file.size > 30*1024*1024) {
      demoFileStatus.textContent="Archivo demasiado grande (máximo 30 MB).";
      demoPlay.disabled=true;return;
    }
    demoObjectUrl=URL.createObjectURL(file);
    demoAudio.src=demoObjectUrl;
    demoFileStatus.textContent="Listo: "+file.name+" · "+(file.size/1024/1024).toFixed(2)+" MB";
    demoPlay.disabled=false;
  });
  demoAudio.addEventListener("ended",stopDemo);
  demoAudio.addEventListener("error",()=>{
    if (!demoPlaying) return;
    stopDemo();
    setState("idle","Audio no compatible","Selecciona un WAV o MP3 que se reproduzca en Chrome.");
  });
  demoPlay.addEventListener("click",async()=>{
    if (busy || enviandoDictado || !demoObjectUrl || !demoAudio.src) return;
    demoError.hidden=true;
    try {
      const AudioCtx=window.AudioContext || window.webkitAudioContext;
      if (!demoCtx && AudioCtx) {
        demoCtx=new AudioCtx();
        const source=demoCtx.createMediaElementSource(demoAudio);
        demoAnalyser=demoCtx.createAnalyser();
        demoAnalyser.fftSize=256;
        demoAnalyser.smoothingTimeConstant=.65;
        demoBuffer=new Uint8Array(demoAnalyser.frequencyBinCount);
        source.connect(demoAnalyser);
        demoAnalyser.connect(demoCtx.destination);
      }
      if (demoCtx && demoCtx.state!=="running") await demoCtx.resume();
      demoAudio.currentTime=0;
      await demoAudio.play();
      demoPlaying=true;
      hideDemo();
      shell.dataset.demo="playing";
      demoTopLabel.textContent="Detener demo";
      demoOpen.classList.add("demo-active");
      setState("speaking","Luna está hablando · DEMO","Observa cómo el núcleo responde a la grabación.");
      const sampleText=demoText.value.trim();
      if(sampleText) addBubble("luna","🎧 [Prueba de voz] "+sampleText);
      if(demoRaf!==null)cancelAnimationFrame(demoRaf);
      demoRaf=requestAnimationFrame(drawDemo);
    } catch (err) {
      if(demoCtx && demoCtx.state==="running") demoCtx.suspend().catch(()=>{});
      demoError.textContent="No se pudo reproducir el archivo. Prueba con un WAV o MP3 diferente. "+(err?.message||"");
      demoError.hidden=false;
      demoPlaying=false;
      shell.dataset.demo="off";
      resetDemoBars();
    }
  });
  function setState(mode, title, detail) {
    shell.dataset.state = mode;
    stateTitle.textContent = title;
    stateMessage.textContent = detail;
  }
  function addBubble(type, message) {
    const bubble = document.createElement("div");
    bubble.className = "bubble " + type;
    if (type !== "system") {
      const label = document.createElement("span");
      label.className = "bubble-label";
      label.textContent = type === "luna" ? "☾ LUNA" : "TÚ";
      bubble.appendChild(label);
    }
    const content = document.createElement("span");
    content.textContent = message;
    bubble.appendChild(content);
    thread.appendChild(bubble);
    thread.scrollTop = thread.scrollHeight;
  }
  function buttons() {
    sendButton.disabled = busy;
    micButton.disabled = busy;
    demoOpen.disabled = busy;
    demoPlay.disabled = busy || !demoObjectUrl;
  }
  function actualizarDictado() {
    input.value = [textoAnterior, ...segmentosGuardados, finalesActuales, parcialActual]
      .map(t => t.trim()).filter(Boolean).join(" ").slice(0, 2000);
    input.scrollTop = input.scrollHeight;
  }
  function stopRecognition() {
    stopMicrophoneVisualization();
    dictando = false;
    enviandoDictado = false;
    if (reinicioMicrofono !== null) {
      clearTimeout(reinicioMicrofono);
      reinicioMicrofono = null;
    }
    if (esperaCierre !== null) {
      clearTimeout(esperaCierre);
      esperaCierre = null;
    }
    if (rec) {
      const previous = rec;
      rec = null;
      previous.onresult = null;
      previous.onend = null;
      previous.onerror = null;
      try { previous.abort(); } catch (_) {}
    }
    micText.textContent = "Hablar con Luna";
    buttons();
  }

  // Finalizar sin perder la última parte reconocida por Chrome.
  // Esta es la ÚNICA ruta del dictado que puede enviar la pregunta.
  function finalizarDictado() {
    if (!enviandoDictado) return;
    const fragmento = [finalesActuales, parcialActual].filter(Boolean).join(" ").trim();
    if (fragmento) segmentosGuardados.push(fragmento);
    finalesActuales = "";
    parcialActual = "";
    actualizarDictado();
    const pregunta = input.value.trim();
    stopRecognition();
    if (pregunta) {
      askLuna(pregunta);
    } else {
      setState("idle", "Luna está lista", "No se escuchó ninguna pregunta. Inténtalo de nuevo.");
    }
  }

  function terminarYEnviar() {
    if (!dictando || enviandoDictado || busy) return;
    stopMicrophoneVisualization();
    dictando = false;
    enviandoDictado = true;
    if (reinicioMicrofono !== null) {
      clearTimeout(reinicioMicrofono);
      reinicioMicrofono = null;
    }
    micText.textContent = "Terminando...";
    micButton.disabled = true;
    setState("listening", "Terminando dictado", "Guardando las últimas palabras antes de enviar...");
    if (rec) {
      // Respaldo por si el navegador no dispara el evento onend.
      esperaCierre = setTimeout(finalizarDictado, 1800);
      try { rec.stop(); } catch (_) { finalizarDictado(); }
    } else {
      finalizarDictado();
    }
  }
  function speakWithSabina(text) {
    return new Promise(resolve => {
      if (!("speechSynthesis" in window)) return resolve(false);
      const voices = window.speechSynthesis.getVoices();
      const voice = voices.find(v => v.lang.toLowerCase().startsWith("es") && v.name.toLowerCase().includes("sabina"));
      if (!voice) return resolve(false);
      const speech = new SpeechSynthesisUtterance(text);
      speech.voice = voice;
      speech.lang = voice.lang;
      speech.rate = .95;
      speech.pitch = 1.05;
      speech.onend = () => resolve(true);
      speech.onerror = () => resolve(false);
      window.speechSynthesis.cancel();
      window.speechSynthesis.speak(speech);
    });
  }
  function playAudio(blob) {
    return new Promise((resolve, reject) => {
      const url = URL.createObjectURL(blob);
      const audio = new Audio(url);
      const clean = () => URL.revokeObjectURL(url);
      audio.onended = () => { clean(); resolve(); };
      audio.onerror = () => { clean(); reject(new Error("No se pudo reproducir la voz.")); };
      audio.play().catch(e => { clean(); reject(e); });
    });
  }
  async function voice(text) {
    if (!voiceToggle.checked) return "off";
    if (!elevenUnavailable) {
      try {
        const response = await fetch("/api/speak", {
          method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify({text})
        });
        if (response.ok) {
          await playAudio(await response.blob());
          return "played";
        }
        elevenUnavailable = true;
      } catch (_) { elevenUnavailable = true; }
    }
    const spoken = await speakWithSabina(text);
    return spoken ? "played" : "unavailable";
  }
  async function askLuna(raw) {
    const message = String(raw || "").trim();
    if (!message || busy) return;
    busy = true;
    if (demoPlaying) stopDemo();
    stopRecognition();
    buttons();
    addBubble("user", message);
    input.value = "";
    setState("thinking", "Luna está pensando", "Conectando con su cerebro...");
    try {
      const response = await fetch("/api/chat", {
        method:"POST", headers:{"Content-Type":"application/json"},
        body:JSON.stringify({message,model_preference:brainChoice.value})
      });
      let data;
      try { data = await response.json(); } catch (_) { throw new Error("El servidor devolvió una respuesta inesperada."); }
      if (!response.ok) throw new Error(data.error || "No se pudo obtener respuesta.");
      if (typeof data.reply !== "string" || !data.reply.trim()) throw new Error("Luna no recibió una respuesta de texto.");
      addBubble("luna", data.reply);
      const brain = data.brain || "IA";
      brainInfo.textContent = "Respondió: " + brain;
      setState("speaking", "Luna respondió", "Respuesta generada con " + brain);
      const audioState = await voice(data.reply);
      setState("idle", "Luna está lista",
        audioState === "unavailable"
          ? "Respuesta escrita lista. No se encontró una voz femenina disponible."
          : "Puedes seguir conversando.");
    } catch (error) {
      addBubble("system", "No se pudo completar la solicitud: " + (error.message || "Error desconocido"));
      setState("idle", "Luna está disponible", "Prueba nuevamente cuando quieras.");
    } finally { busy = false; buttons(); }
  }
  form.addEventListener("submit", event => {
    event.preventDefault();
    if (dictando) { terminarYEnviar(); return; }
    if (!enviandoDictado) askLuna(input.value);
  });
  input.addEventListener("keydown", event => {
    if (event.key === "Enter" && !event.shiftKey && !event.isComposing) {
      event.preventDefault();
      if (dictando) terminarYEnviar();
      else if (!enviandoDictado) askLuna(input.value);
    }
  });
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

  function comenzarSesionVoz() {
    if (!dictando || busy) return;
    const recognition = new SpeechRecognition();
    rec = recognition;
    finalesActuales = "";
    parcialActual = "";
    recognition.lang = "es-DO";
    recognition.continuous = true;
    recognition.interimResults = true;
    recognition.maxAlternatives = 1;
    recognition.onstart = () => {
      if (rec !== recognition) return;
      startMicrophoneVisualization();
      micText.textContent = "Terminar y enviar";
      setState("listening", "Luna te escucha", "Habla sin prisa. Pulsa «Terminar y enviar» cuando acabes.");
    };
    recognition.onresult = event => {
      if (rec !== recognition || busy || (!dictando && !enviandoDictado)) return;
      const finales = [];
      const parciales = [];
      for (let i = 0; i < event.results.length; i++) {
        const resultado = event.results[i];
        const fragmento = resultado[0].transcript.trim();
        if (resultado.isFinal) finales.push(fragmento);
        else parciales.push(fragmento);
      }
      finalesActuales = finales.join(" ").trim();
      parcialActual = parciales.join(" ").trim();
      actualizarDictado();
    };
    recognition.onerror = event => {
      if (rec !== recognition || !dictando) return;
      if (["not-allowed", "service-not-allowed", "audio-capture", "network"].includes(event.error)) {
        actualizarDictado();
        stopRecognition();
        setState("idle", "Micrófono no disponible", "El navegador informó: " + event.error + ". Puedes enviar el texto escrito.");
      }
    };
    recognition.onend = () => {
      if (rec !== recognition) return;
      rec = null;
      if (enviandoDictado) { finalizarDictado(); return; }
      const fragmento = [finalesActuales, parcialActual].filter(Boolean).join(" ").trim();
      if (fragmento) segmentosGuardados.push(fragmento);
      finalesActuales = "";
      parcialActual = "";
      actualizarDictado();
      if (!dictando || busy) return;
      // Una sesión puede terminar sola. Reiniciamos SIN enviar la pregunta.
      reintentosMicrofono = fragmento ? 0 : reintentosMicrofono + 1;
      if (reintentosMicrofono > 7) {
        stopRecognition();
        setState("idle", "Dictado pausado", "Chrome interrumpió varias sesiones. Tu texto se conserva; revisa y pulsa Enviar.");
        return;
      }
      reinicioMicrofono = setTimeout(() => {
        reinicioMicrofono = null;
        if (dictando && !busy) comenzarSesionVoz();
      }, 350);
    };
    try {
      recognition.start();
    } catch (_) {
      rec = null;
      stopRecognition();
      setState("idle", "Micrófono no disponible", "No se pudo iniciar el reconocimiento. Puedes escribir tu pregunta.");
    }
  }

  function listen() {
    if (busy || enviandoDictado) return;
    if (demoPlaying) stopDemo();
    if (dictando) { terminarYEnviar(); return; }
    if (!SpeechRecognition) {
      setState("idle", "Micrófono no disponible", "Utiliza Chrome con reconocimiento de voz o escribe tu mensaje.");
      return;
    }
    dictando = true;
    textoAnterior = input.value.trim();
    segmentosGuardados = [];
    finalesActuales = "";
    parcialActual = "";
    reintentosMicrofono = 0;
    micText.textContent = "Terminar y enviar";
    setState("listening", "Luna te escucha", "Puedes hablar una frase larga. Pulsa «Terminar y enviar» cuando acabes.");
    comenzarSesionVoz();
  }
  micButton.addEventListener("click",listen);
  document.getElementById("navVoice").addEventListener("click",listen);
  document.getElementById("navChat").addEventListener("click",()=>input.focus());
  function showSettings(){settings.hidden=false;showSettingsTab("theme");document.getElementById("closeSettings").focus({preventScroll:true});}
  function hideSettings(){settings.hidden=true;document.getElementById("settingsButton").focus();}
  document.getElementById("settingsButton").addEventListener("click",showSettings);
  document.getElementById("navSettings").addEventListener("click",showSettings);
  document.getElementById("closeSettings").addEventListener("click",hideSettings);
  settings.addEventListener("click",e=>{if(e.target===settings)hideSettings();});
  document.addEventListener("keydown",e=>{
    if(e.key==="Escape"&&!demoOverlay.hidden)hideDemo();
    else if(e.key==="Escape"&&!settings.hidden)hideSettings();
  });
  motionToggle.addEventListener("change",()=>{
    document.documentElement.classList.toggle("motion-off", !motionToggle.checked);
    document.documentElement.style.setProperty("--motion-play", motionToggle.checked ? "running" : "paused");
    if (!motionToggle.checked) stopMicrophoneVisualization();
    else if (dictando) startMicrophoneVisualization();
  });
  // Respetar la elección guardada del usuario desde el primer render.
})();
</script>
</body>
</html>
"""


# ==========================================
# PÁGINA PRINCIPAL
# ==========================================

@app.get("/")
def home():
    return render_template_string(PAGE)


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
    instrucciones = (
        "Eres Luna, una asistente personal femenina, amable, inteligente, "
        "tierna y comprensiva. Habla naturalmente en español. "
        "Responde de forma clara y normalmente breve. "
        "No repitas innecesariamente las respuestas. "
        "Tu personalidad es cercana y conversacional. "
        "No inventes información que desconozcas. "
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
