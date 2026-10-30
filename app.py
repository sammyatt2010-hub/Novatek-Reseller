"""
Novalink Telephony Partner Programme - standalone showcase site.

Pages: Programme (the offer) and Quote builder (live demo of the partner price book + quote tool).
Run locally:  streamlit run app.py
Deploy:       push this folder to its own GitHub repo, then point Streamlit Community Cloud at app.py.
No secrets needed. All prices in the demos are illustrative.
"""
import base64
import html as html_lib
import inspect
import math
import zlib
from pathlib import Path

import pandas as pd
import streamlit as st

st.set_page_config(page_title="Novalink · Telephony Partners", page_icon="◆", layout="wide",
                   initial_sidebar_state="collapsed")

CONTACT_EMAIL = "info@novalinkhardware.co.uk"

CSS = r"""
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
:root{--bg:#0A0E1A;--surface:#111827;--surface-2:#161F33;--surface-3:#1C2740;--border:rgba(148,163,184,.14);--border-strong:rgba(148,163,184,.26);--text:#E7EAF3;--muted:#8C98B0;--faint:#5E6A82;--accent:#7C83FF;--accent-2:#38D6F5;--accent-soft:rgba(124,131,255,.14);--good:#34D399;--warn:#FBBF24;--risk:#FB923C;--bad:#F87171;--radius:14px;--grad:linear-gradient(135deg,#7C83FF 0%,#38D6F5 100%);}
html,body,[class*="css"],.stApp,button,input,textarea,select{font-family:'Inter',system-ui,-apple-system,'Segoe UI',sans-serif!important}
.stApp{background:radial-gradient(1200px 500px at 85% -10%,rgba(56,214,245,.07),transparent 60%),radial-gradient(900px 500px at 10% -20%,rgba(124,131,255,.10),transparent 60%),var(--bg)}
[data-testid="stHeader"]{background:transparent;pointer-events:none}
[data-testid="stHeader"] [data-testid="stToolbar"],[data-testid="stHeader"] button,[data-testid="stHeader"] a{pointer-events:auto}[data-testid="stDecoration"]{display:none}footer{visibility:hidden}
[data-testid="stSidebar"],[data-testid="stSidebarCollapsedControl"]{display:none}
.block-container{padding-top:4.2rem!important;padding-bottom:3rem!important;max-width:1360px}
[data-testid="stWidgetLabel"] p{font-size:.76rem!important;font-weight:600!important;color:var(--muted)!important;text-transform:uppercase;letter-spacing:.06em}
[data-testid="stCaptionContainer"]{color:var(--muted)!important}
[class*="st-key-card-"]{background:linear-gradient(180deg,rgba(22,31,51,.85) 0%,rgba(17,24,39,.85) 100%);border:1px solid var(--border)!important;border-radius:var(--radius);padding:22px 22px 18px;box-shadow:0 1px 0 rgba(255,255,255,.03) inset,0 20px 40px -24px rgba(0,0,0,.6);margin-bottom:6px}
[data-baseweb="input"],[data-baseweb="select"]>div,[data-baseweb="textarea"]{background:var(--surface)!important;border:1px solid var(--border-strong)!important;border-radius:10px!important}
[data-baseweb="input"]:focus-within,[data-baseweb="select"]>div:focus-within{border-color:var(--accent)!important;box-shadow:0 0 0 3px var(--accent-soft)!important}
[data-baseweb="input"]>div,[data-baseweb="base-input"]{background:transparent!important}
.stButton button,.stDownloadButton button,.stLinkButton a{border-radius:10px!important;font-weight:600!important;border:1px solid var(--border-strong)!important;background:var(--surface-2)!important;color:var(--text)!important;transition:all .15s ease}
.stButton button:hover,.stDownloadButton button:hover,.stLinkButton a:hover{border-color:var(--accent)!important;transform:translateY(-1px)}
.stButton button[kind="primary"],.stDownloadButton button[kind="primary"],[data-testid="stBaseButton-primary"],[data-testid="stBaseLinkButton-primary"],.stLinkButton a[data-testid="stBaseLinkButton-primary"]{background:var(--grad)!important;border:none!important;color:#0A0E1A!important;box-shadow:0 8px 24px -10px rgba(124,131,255,.8)}
.stButton button[kind="primary"] p,[data-testid="stBaseButton-primary"] p,[data-testid="stBaseLinkButton-primary"] p,.stLinkButton a[data-testid="stBaseLinkButton-primary"] p{color:#0A0E1A!important;font-weight:700!important}
[data-testid="stTabs"] [role="tablist"],[data-baseweb="tab-list"]{gap:4px;background:var(--surface);padding:4px;border-radius:12px;border:1px solid var(--border);width:fit-content}
[data-testid="stTabs"] [role="tab"],[data-baseweb="tab"]{border-radius:9px!important;padding:8px 16px!important;color:var(--muted)!important;background:transparent!important}
[data-testid="stTabs"] [role="tab"][aria-selected="true"],[data-baseweb="tab"][aria-selected="true"]{background:var(--surface-3)!important;color:var(--text)!important}
[data-baseweb="tab-highlight"],[data-baseweb="tab-border"],[data-testid="stTabs"] .react-aria-SelectionIndicator{display:none!important}
[data-testid="stDataFrame"]{border:1px solid var(--border);border-radius:12px;overflow:hidden}
[data-testid="stExpander"] details{background:var(--surface);border:1px solid var(--border)!important;border-radius:12px!important}

/* ---------- top nav ---------- */
.st-key-topnav{border-bottom:1px solid var(--border);padding-bottom:12px;margin-bottom:8px}
.st-key-topnav .stButton button{padding:6px 14px!important;min-height:38px}
.nv-brand{display:flex;align-items:center;gap:12px}
.nv-brand .t{font-weight:800;font-size:1.08rem;letter-spacing:-.02em;color:var(--text);line-height:1.1}
.nv-brand .s{font-size:.72rem;color:var(--muted);letter-spacing:.08em;text-transform:uppercase;font-weight:600}
.pe-logo{width:40px;height:40px;border-radius:12px;background:var(--grad);display:grid;place-items:center;color:#0A0E1A;box-shadow:0 10px 24px -10px rgba(124,131,255,.9);flex:none}

/* ---------- typography ---------- */
.pe-eyebrow{display:inline-flex;align-items:center;gap:8px;font-size:.72rem;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--accent-2);margin-bottom:10px}
.pe-eyebrow .dot{width:7px;height:7px;border-radius:50%;background:var(--good);box-shadow:0 0 0 4px rgba(52,211,153,.15)}
.nv-hero-t{font-size:clamp(2.2rem,4.4vw,3.6rem);font-weight:800;letter-spacing:-.045em;line-height:1.02;color:var(--text);margin:4px 0 16px}
.nv-hero-t span,.pe-title span,.nv-h2 span{background:var(--grad);-webkit-background-clip:text;background-clip:text;color:transparent}
.nv-hero-s{color:var(--muted);font-size:1.08rem;line-height:1.6;max-width:560px;margin-bottom:22px}
.nv-h2{font-size:clamp(1.5rem,2.6vw,2.05rem);font-weight:800;letter-spacing:-.035em;color:var(--text);line-height:1.15;margin-bottom:8px}
.nv-lead{color:var(--muted);font-size:.98rem;max-width:720px;line-height:1.6;margin-bottom:22px}
.nv-sec{margin:56px 0 0}
.pe-title{font-size:2.05rem;font-weight:800;letter-spacing:-.035em;line-height:1.1;color:var(--text)}
.pe-sub{color:var(--muted);font-size:.95rem;margin-top:8px;max-width:640px}

/* ---------- hero mock ---------- */
.nv-mock{position:relative;background:linear-gradient(180deg,#141C30 0%,#0F1526 100%);border:1px solid var(--border-strong);border-radius:18px;padding:18px;box-shadow:0 40px 80px -30px rgba(56,214,245,.25),0 30px 60px -30px rgba(0,0,0,.8);transform:perspective(1400px) rotateY(-6deg) rotateX(3deg)}
.nv-mock .bar{display:flex;align-items:center;gap:6px;margin-bottom:14px}
.nv-mock .bar i{width:9px;height:9px;border-radius:50%;background:#2A3550;display:block}
.nv-mock .bar .ttl{margin-left:10px;font-size:.78rem;color:var(--muted);font-weight:600}
.nv-mock .kp{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-bottom:14px}
.nv-mock .kp div{background:var(--surface);border:1px solid var(--border);border-top:2px solid var(--accent);border-radius:10px;padding:10px 12px}
.nv-mock .kp b{display:block;font-size:1.25rem;color:var(--text);letter-spacing:-.03em}
.nv-mock .kp span{font-size:.62rem;color:var(--muted);text-transform:uppercase;letter-spacing:.08em;font-weight:700}
.nv-mock .chart{display:flex;align-items:flex-end;gap:7px;height:120px;padding:12px;background:var(--surface);border:1px solid var(--border);border-radius:10px}
.nv-mock .chart div{flex:1;border-radius:5px 5px 2px 2px;background:var(--grad);opacity:.9}
.nv-mock .chart div.m{background:linear-gradient(180deg,#F87171,#FB923C)}
.nv-mock .alert{margin-top:12px;display:flex;gap:10px;align-items:center;background:rgba(248,113,113,.10);border:1px solid rgba(248,113,113,.3);border-radius:10px;padding:10px 12px;font-size:.8rem;color:#FCA5A5}
.nv-float{position:absolute;right:-14px;bottom:-22px;background:var(--surface-2);border:1px solid var(--border-strong);border-radius:12px;padding:10px 14px;font-size:.78rem;color:var(--text);box-shadow:0 20px 40px -18px rgba(0,0,0,.8);display:flex;gap:10px;align-items:center}
.nv-float .g{width:26px;height:26px;border-radius:8px;background:rgba(52,211,153,.15);color:var(--good);display:grid;place-items:center}

/* ---------- tiles & grids ---------- */
.nv-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:16px}
.nv-grid.g3{grid-template-columns:repeat(auto-fit,minmax(290px,1fr))}
.nv-tile{background:linear-gradient(180deg,rgba(22,31,51,.85) 0%,rgba(17,24,39,.85) 100%);border:1px solid var(--border);border-radius:var(--radius);padding:22px;position:relative;overflow:hidden}
.nv-tile .ic{width:42px;height:42px;border-radius:12px;background:var(--accent-soft);border:1px solid rgba(124,131,255,.3);display:grid;place-items:center;color:var(--accent);margin-bottom:16px}
.nv-tile .ic.c{background:rgba(56,214,245,.12);border-color:rgba(56,214,245,.3);color:var(--accent-2)}
.nv-tile .h{font-size:1.02rem;font-weight:700;color:var(--text);margin-bottom:6px;letter-spacing:-.01em}
.nv-tile .p{font-size:.88rem;color:var(--muted);line-height:1.55}
.nv-tile .num{position:absolute;right:18px;top:14px;font-size:2.6rem;font-weight:800;letter-spacing:-.05em;color:rgba(124,131,255,.12)}
.nv-step-line{height:2px;background:var(--grad);border-radius:2px;margin:-2px 0 18px;opacity:.6}
.nv-stats{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-top:40px}@media(max-width:640px){.nv-stats{grid-template-columns:1fr}}
.nv-stat{border-left:2px solid var(--accent);padding:4px 0 4px 16px}
.nv-stat b{display:block;font-size:1.25rem;font-weight:800;letter-spacing:-.03em;color:var(--text)}
.nv-stat span{font-size:.84rem;color:var(--muted)}

/* app showcase cards */
.nv-app .top{display:flex;justify-content:space-between;align-items:flex-start;gap:10px}
.nv-app .lbl{font-size:.68rem;font-weight:700;text-transform:uppercase;letter-spacing:.1em;color:var(--faint);margin:14px 0 4px}
.nv-app .out{margin-top:14px;padding:10px 12px;border-radius:10px;background:rgba(52,211,153,.08);border:1px solid rgba(52,211,153,.25);color:#A7F3D0;font-size:.84rem;line-height:1.45}

/* compare */
.nv-cmp{display:grid;grid-template-columns:1fr 1fr;gap:16px}
@media(max-width:760px){.nv-cmp{grid-template-columns:1fr}.nv-mock{transform:none}}
.nv-cmp ul{list-style:none;padding:0;margin:10px 0 0}
.nv-cmp li{display:flex;gap:10px;padding:8px 0;border-bottom:1px solid var(--border);font-size:.9rem;color:var(--text)}
.nv-cmp li:last-child{border:none}
.nv-cmp .x{color:var(--bad)}.nv-cmp .y{color:var(--good)}

/* CTA band */
[class*="st-key-ctaband"]{margin-top:56px;padding:36px 40px 40px;border-radius:20px;background:radial-gradient(600px 200px at 80% 0%,rgba(56,214,245,.18),transparent 70%),linear-gradient(135deg,rgba(124,131,255,.18),rgba(56,214,245,.06));border:1px solid rgba(124,131,255,.35)}

/* chips */
.pe-chip{display:inline-flex;align-items:center;gap:6px;padding:4px 10px;border-radius:999px;font-size:.74rem;font-weight:600;background:var(--surface-3);color:var(--text);border:1px solid var(--border);white-space:nowrap}
.pe-chip.accent{background:var(--accent-soft);color:#B9BDFF;border-color:rgba(124,131,255,.3)}
.pe-chip.good{background:rgba(52,211,153,.12);color:var(--good);border-color:rgba(52,211,153,.3)}
.pe-chip.warn{background:rgba(251,191,36,.12);color:var(--warn);border-color:rgba(251,191,36,.3)}
.pe-chip.bad{background:rgba(248,113,113,.12);color:var(--bad);border-color:rgba(248,113,113,.3)}

/* stepper hero */
.pe-hero{display:flex;align-items:center;justify-content:space-between;gap:24px;flex-wrap:wrap;padding:14px 2px 22px;margin-bottom:18px;border-bottom:1px solid var(--border)}
.pe-stepper{display:flex;align-items:center;gap:6px;background:var(--surface);border:1px solid var(--border);border-radius:999px;padding:6px;flex-wrap:wrap}
.pe-step{display:flex;align-items:center;gap:8px;padding:7px 14px 7px 7px;border-radius:999px;font-size:.82rem;font-weight:600;color:var(--faint);white-space:nowrap}
.pe-step .num{width:24px;height:24px;border-radius:50%;display:grid;place-items:center;font-size:.72rem;font-weight:700;border:1px solid var(--border-strong)}
.pe-step.done{color:var(--muted)}.pe-step.done .num{background:rgba(52,211,153,.14);border-color:rgba(52,211,153,.45);color:var(--good)}
.pe-step.active{background:var(--surface-3);color:var(--text)}.pe-step.active .num{background:var(--grad);border:none;color:#0A0E1A}
.pe-step-sep{width:14px;height:1px;background:var(--border-strong)}
.pe-section{display:flex;align-items:center;gap:12px;margin-bottom:16px}
.pe-section .badge{width:34px;height:34px;border-radius:10px;display:grid;place-items:center;background:var(--accent-soft);color:var(--accent);font-weight:800;font-size:.85rem;border:1px solid rgba(124,131,255,.3)}
.pe-section .t{font-size:1.08rem;font-weight:700;color:var(--text)}.pe-section .s{font-size:.82rem;color:var(--muted);margin-top:2px}

/* scenario picker cards */
[class*="st-key-scn-"]{background:var(--surface);border:1px solid var(--border)!important;border-radius:var(--radius);padding:18px 18px 14px;transition:all .15s ease;height:100%}
[class*="st-key-scn-"]:hover{border-color:var(--border-strong)!important}
[class*="st-key-scn-on-"]{border-color:rgba(56,214,245,.55)!important;box-shadow:0 0 0 3px rgba(56,214,245,.10),0 20px 40px -24px rgba(56,214,245,.45);background:linear-gradient(180deg,rgba(28,39,64,.9),rgba(17,24,39,.9))}
.nv-scn .h{font-weight:700;color:var(--text);margin:12px 0 4px}.nv-scn .p{font-size:.82rem;color:var(--muted);line-height:1.45;min-height:58px}

/* KPI tiles */
.nv-kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:14px;margin:6px 0 18px}
.pe-kpi{background:var(--surface);border:1px solid var(--border);border-top:2px solid var(--accent);border-radius:14px;padding:16px 18px}
.pe-kpi.b{border-top-color:var(--bad)}.pe-kpi.g{border-top-color:var(--good)}.pe-kpi.c{border-top-color:var(--accent-2)}
.pe-kpi .l{font-size:.72rem;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}
.pe-kpi .v{font-size:1.8rem;font-weight:800;letter-spacing:-.03em;color:var(--text);margin-top:6px}
.pe-kpi .s{font-size:.8rem;color:var(--faint);margin-top:2px}

/* observations */
.nv-obs{display:flex;gap:12px;padding:12px 0;border-bottom:1px solid var(--border);font-size:.9rem;line-height:1.5;color:var(--text)}
.nv-obs:last-child{border:none}
.nv-obs .d{width:8px;height:8px;border-radius:50%;margin-top:7px;flex:none}
.nv-rec{display:flex;gap:12px;padding:9px 0;font-size:.88rem;color:var(--text);line-height:1.5}
.nv-rec b{width:24px;height:24px;border-radius:7px;background:var(--accent-soft);color:var(--accent);display:grid;place-items:center;font-size:.75rem;flex:none}

/* transcript */
.nv-tr{display:flex;flex-direction:column;gap:10px;max-height:520px;overflow:auto;padding-right:6px}
.nv-msg{max-width:86%;padding:10px 14px;border-radius:14px;font-size:.88rem;line-height:1.5;border:1px solid var(--border)}
.nv-msg .meta{font-size:.68rem;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);margin-bottom:3px;display:flex;gap:8px;align-items:center}
.nv-msg.a{align-self:flex-start;background:var(--surface-3)}
.nv-msg.a.weak{border-color:rgba(251,191,36,.45);background:rgba(251,191,36,.06)}
.nv-msg.c{align-self:flex-end;background:rgba(124,131,255,.10);border-color:rgba(124,131,255,.25)}
.nv-coach{border:1px solid var(--border);border-radius:12px;padding:14px 16px;margin-bottom:12px;background:var(--surface)}
.nv-coach .q{font-size:.86rem;color:#FCD34D;margin:8px 0;font-style:italic}
.nv-coach .t{font-size:.86rem;color:var(--muted);line-height:1.5}
.nv-coach .try{margin-top:10px;padding:10px 12px;border-radius:10px;background:rgba(52,211,153,.08);border:1px solid rgba(52,211,153,.25);color:#A7F3D0;font-size:.86rem}

/* upload zone (illustrative) */
.nv-drop{border:1.5px dashed var(--border-strong);border-radius:14px;padding:18px;display:flex;gap:14px;align-items:center;color:var(--muted);font-size:.86rem;background:rgba(17,24,39,.5)}
.nv-drop .ic{width:40px;height:40px;border-radius:12px;background:var(--accent-soft);color:var(--accent);display:grid;place-items:center;flex:none}
.nv-empty{text-align:center;padding:40px 20px}
.nv-empty .ic{width:56px;height:56px;border-radius:16px;margin:0 auto 14px;background:var(--accent-soft);color:var(--accent);display:grid;place-items:center}
.nv-empty .h{font-weight:700;color:var(--text);font-size:1.05rem}
.nv-empty ol{display:inline-block;text-align:left;color:var(--muted);font-size:.88rem;margin-top:10px}
/* telephony partners */
.st-key-card-teaser{margin-top:36px!important;border-color:rgba(56,214,245,.3)!important}
.nv-abtn{display:flex;align-items:center;justify-content:center;min-height:40px;border-radius:10px;font-weight:600;font-size:.9rem;
border:1px solid var(--border-strong);background:var(--surface-2);color:var(--text)!important;text-decoration:none!important;transition:all .15s ease}
.nv-abtn:hover{border-color:var(--accent);transform:translateY(-1px)}
.nv-bigstats{display:grid;grid-template-columns:repeat(4,1fr);gap:1px;background:var(--border);border:1px solid var(--border);border-radius:16px;overflow:hidden;margin:34px 0 0}
.nv-bigstats div{background:var(--surface);padding:22px 22px 20px}
.nv-bigstats b{display:block;font-size:2.3rem;font-weight:800;letter-spacing:-.045em;line-height:1;background:var(--grad);-webkit-background-clip:text;background-clip:text;color:transparent}
.nv-bigstats span{display:block;margin-top:8px;font-size:.86rem;color:var(--muted);line-height:1.45}
@media(max-width:900px){.nv-bigstats{grid-template-columns:1fr 1fr}}
.nv-frow{display:grid;grid-template-columns:1fr 1fr;gap:44px;align-items:center;margin-top:52px}
.nv-frow.flip .img{order:2}
.nv-frow .img img{width:100%;display:block;border-radius:16px;border:1px solid var(--border-strong);box-shadow:0 30px 60px -30px rgba(0,0,0,.8),0 0 0 6px rgba(124,131,255,.05)}
.nv-frow .tx .h{font-size:1.6rem;font-weight:800;letter-spacing:-.035em;color:var(--text);margin:6px 0 10px;line-height:1.15}
.nv-frow .tx .p{color:var(--muted);font-size:.96rem;line-height:1.6}
.nv-ticks{list-style:none;padding:0;margin:16px 0 0}
.nv-ticks li{display:flex;gap:10px;align-items:flex-start;padding:6px 0;color:var(--text);font-size:.92rem}
.nv-ticks li span{color:var(--good);margin-top:2px}
@media(max-width:820px){.nv-frow{grid-template-columns:1fr;gap:20px}.nv-frow.flip .img{order:0}}
.nv-timeline{display:grid;grid-template-columns:repeat(5,1fr);gap:14px;position:relative}
@media(max-width:1000px){.nv-timeline{grid-template-columns:1fr 1fr}}
@media(max-width:600px){.nv-timeline{grid-template-columns:1fr}}
.nv-tl{background:var(--surface);border:1px solid var(--border);border-radius:14px;padding:18px;position:relative}
.nv-tl .n{width:30px;height:30px;border-radius:50%;display:grid;place-items:center;background:var(--grad);color:#0A0E1A;font-weight:800;font-size:.8rem;margin-bottom:12px}
.nv-tl .who{font-size:.66rem;font-weight:700;letter-spacing:.1em;text-transform:uppercase;margin-bottom:4px}
.nv-tl .who.us{color:var(--accent-2)}.nv-tl .who.you{color:#B9BDFF}.nv-tl .who.both{color:var(--good)}
.nv-tl .h{font-weight:700;color:var(--text);font-size:.95rem;margin-bottom:6px}
.nv-tl .p{font-size:.83rem;color:var(--muted);line-height:1.5}
.nv-tl.gate{border-color:rgba(52,211,153,.45);background:linear-gradient(180deg,rgba(52,211,153,.08),var(--surface))}
.nv-split{display:grid;grid-template-columns:1fr 1fr;gap:16px}
@media(max-width:760px){.nv-split{grid-template-columns:1fr}}
.nv-prods{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:14px}
.nv-prod{background:var(--surface);border:1px solid var(--border);border-radius:14px;overflow:hidden}
.nv-prod .stage{height:150px;display:grid;place-items:center;background:radial-gradient(120% 90% at 50% 20%,#FFFFFF 0%,#EEF1F8 70%,#E3E8F2 100%)}
.nv-prod .stage img{max-height:124px;max-width:80%;filter:drop-shadow(0 10px 12px rgba(10,14,26,.25))}
.nv-prod .b{padding:12px 14px 14px}
.nv-prod .br{font-size:.66rem;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--faint)}
.nv-prod .nm{font-weight:700;color:var(--text);font-size:.95rem;margin:2px 0 4px}
.nv-prod .d{font-size:.78rem;color:var(--muted);line-height:1.45}
.nv-qmock .nv-float{top:-20px;bottom:auto;right:-16px}
.nv-qmock .row{display:flex;justify-content:space-between;padding:9px 0;border-bottom:1px solid var(--border);font-size:.84rem;color:var(--muted)}
.nv-qmock .row b{color:var(--text)}
.nv-qmock .tot{display:flex;justify-content:space-between;align-items:baseline;margin-top:12px}
.nv-qmock .tot b{font-size:1.5rem;letter-spacing:-.03em;color:var(--text)}
.nv-sum .big{font-size:2.2rem;font-weight:800;letter-spacing:-.04em;color:var(--text);line-height:1.1}
.nv-sum .lab{font-size:.7rem;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);margin-top:14px}
.nv-sum .hl{background:linear-gradient(135deg,rgba(52,211,153,.14),rgba(56,214,245,.08));border:1px solid rgba(52,211,153,.35);border-radius:14px;padding:16px;margin-top:16px}
.nv-sum .hl .big{color:var(--good)}
[data-testid="stColumn"]:has(.st-key-card-calcsum){position:sticky;top:1rem;align-self:flex-start}
/* customer quote "paper" */
.nv-paper{background:#fff;color:#1F2433;border-radius:14px;overflow:hidden;box-shadow:0 30px 60px -30px rgba(0,0,0,.8);max-width:960px}
.nv-paper .hd{background:var(--b);color:#fff;padding:22px 26px;display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap}
.nv-paper .bn{font-size:1.35rem;font-weight:800;letter-spacing:-.02em}.nv-paper .bs{opacity:.85;font-size:.85rem}
.nv-paper .rf{text-align:right;font-size:.85rem;opacity:.95}
.nv-paper .bd{padding:8px 26px 20px}
.nv-paper .tl{font-weight:800;color:var(--b);margin:18px 0 6px;font-size:.95rem}
.nv-paper table{width:100%;border-collapse:collapse;font-size:.85rem;table-layout:fixed}.nv-paper th:first-child{width:58%}
.nv-paper th{text-align:left;font-size:.7rem;text-transform:uppercase;letter-spacing:.06em;color:#6B7385;border-bottom:2px solid #E2E6EF;padding:6px 4px}
.nv-paper td{border-bottom:1px solid #EEF0F5;padding:7px 4px;vertical-align:top;color:#1F2433}
.nv-paper .r{text-align:right;white-space:nowrap}.nv-paper .n{font-size:.74rem;color:#6B7385}
.nv-paper .sm{font-size:.76rem;color:#6B7385;margin-top:6px}
.nv-paper .tots{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-top:20px}
.nv-paper .t{border-top:3px solid var(--b);background:#F6F7FB;border-radius:8px;padding:10px 12px}
.nv-paper .t span{display:block;font-size:.7rem;text-transform:uppercase;letter-spacing:.06em;color:#6B7385;font-weight:700}
.nv-paper .t b{font-size:1.25rem;color:#1F2433}
.nv-paper .inc{margin-top:14px;font-size:.8rem;color:#475069}
.nv-paper .ft{background:#F6F7FB;color:#6B7385;font-size:.76rem;padding:10px 26px}
.nv-foot{margin-top:60px;padding-top:20px;border-top:1px solid var(--border);display:flex;justify-content:space-between;flex-wrap:wrap;gap:10px;color:var(--faint);font-size:.8rem}
"""
st.markdown(f"<style>{CSS}</style>", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def esc(v):
    return html_lib.escape(str(v if v is not None else ""), quote=True)


def render_html(markup, target=None):
    (target or st).markdown(" ".join(l.strip() for l in markup.splitlines()), unsafe_allow_html=True)


def chip(text, tone=""):
    return f'<span class="pe-chip {tone}">{esc(text)}</span>'


def section_header(num, title, subtitle=""):
    render_html(f'<div class="pe-section"><div class="badge">{num}</div><div><div class="t">{esc(title)}</div>'
                + (f'<div class="s">{esc(subtitle)}</div>' if subtitle else "") + "</div></div>")


def _kw(fn):
    try:
        if "width" in inspect.signature(fn).parameters:
            return {"width": "stretch"}
    except (TypeError, ValueError):
        pass
    return {"use_container_width": True}


BTN_W, DF_W = _kw(st.button), _kw(st.dataframe)


def show_fig(fig):
    st.plotly_chart(fig, config={"displayModeBar": False}, **_kw(st.plotly_chart))


def show_df(df, height=None, **kw):
    if height:
        kw["height"] = height
    st.dataframe(df, hide_index=True, **DF_W, **kw)


ASSETS = Path(__file__).parent / "assets"


@st.cache_data(show_spinner=False)
def img_uri(name):
    """Embed an image from the assets folder (returns '' if it's missing, so the page never breaks)."""
    f = ASSETS / name
    if not f.exists():
        return ""
    mime = {"jpg": "jpeg", "jpeg": "jpeg", "png": "png", "webp": "webp"}.get(f.suffix.lower().lstrip("."), "png")
    return f"data:image/{mime};base64," + base64.b64encode(f.read_bytes()).decode()


def go_to(page, scenario=None):
    st.session_state.page = page
    if scenario:
        st.session_state.scenario = scenario


# Feather-style icons
I = {
    "logo": '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M4 20V4l16 16V4"/></svg>',
    "phone": '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/></svg>',
    "mic": '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2"/><line x1="12" y1="19" x2="12" y2="23"/></svg>',
    "pound": '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 7a4 4 0 0 0-7-2.6C9.8 5.6 10 8 10 10v4c0 2-1 4-3 5h11"/><line x1="6" y1="12" x2="15" y2="12"/></svg>',
    "trend": '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/><polyline points="17 6 23 6 23 12"/></svg>',
    "calc": '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="2" width="16" height="20" rx="2"/><line x1="8" y1="6" x2="16" y2="6"/><line x1="8" y1="11" x2="8" y2="11"/><line x1="12" y1="11" x2="12" y2="11"/><line x1="16" y1="11" x2="16" y2="11"/><line x1="8" y1="15" x2="8" y2="15"/><line x1="12" y1="15" x2="12" y2="15"/><line x1="16" y1="15" x2="16" y2="18"/></svg>',
    "clip": '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><rect x="8" y="2" width="8" height="4" rx="1"/><polyline points="9 14 11 16 15 12"/></svg>',
    "upload": '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>',
    "chat": '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>',
    "code": '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/></svg>',
    "bulb": '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 18h6"/><path d="M10 22h4"/><path d="M12 2a7 7 0 0 0-4 12.7c.6.5 1 1.3 1 2.3h6c0-1 .4-1.8 1-2.3A7 7 0 0 0 12 2z"/></svg>',
    "shield": '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>',
    "table": '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2"/><line x1="3" y1="9" x2="21" y2="9"/><line x1="3" y1="15" x2="21" y2="15"/><line x1="9" y1="3" x2="9" y2="21"/></svg>',
    "clock": '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>',
    "puzzle": '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 12h-2a2 2 0 1 0-4 0h-2V8a2 2 0 1 0 0-4V2H4v8h2a2 2 0 1 1 0 4H4v8h8v-2a2 2 0 1 1 4 0v2h4z"/></svg>',
    "check": '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>',
    "x": '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>',
    "alert": '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M10.3 3.9 1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12" y2="17"/></svg>',
}

TONE_COL = {"good": "#34D399", "warn": "#FBBF24", "bad": "#F87171", "accent": "#7C83FF"}
COL = dict(a="#7C83FF", c="#38D6F5", g="#34D399", w="#FBBF24", b="#F87171", r="#FB923C", m="#8C98B0")


def style_fig(fig, h=330, title=None):
    fig.update_layout(
        template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, system-ui, sans-serif", color="#C9D1E3", size=12), height=h,
        margin=dict(l=8, r=8, t=46 if title else 16, b=8 if len(fig.data) < 2 else 30),
        title=dict(text=f"<b>{title}</b>" if title else None, x=0, font=dict(size=14, color="#E7EAF3")),
        legend=dict(orientation="h", y=-0.16, yanchor="top", x=0, xanchor="left", font=dict(size=11),
                    traceorder="normal"),
        hoverlabel=dict(bgcolor="#161F33", bordercolor="#2A3550", font=dict(family="Inter")),
        bargap=0.28)
    fig.update_xaxes(gridcolor="rgba(148,163,184,.08)", zeroline=False, linecolor="rgba(148,163,184,.2)")
    fig.update_yaxes(gridcolor="rgba(148,163,184,.08)", zeroline=False)
    return fig



ss = st.session_state
ss.setdefault("page", "Programme")
PAGES = ["Programme", "Quote builder"]

with st.container(key="topnav"):
    cols = st.columns([3.2, 1.05, 1.15, 1.25])
    render_html(f'''<div class="nv-brand"><div class="pe-logo">{I["logo"]}</div>
        <div><div class="t">Novalink</div><div class="s">Telephony partner programme</div></div></div>''', cols[0])
    for c, pg in zip(cols[1:3], PAGES):
        c.button(pg, key=f"nav-{pg}", on_click=go_to, args=(pg,), type="primary" if ss.page == pg else "secondary", **BTN_W)
    cols[3].link_button("Become a partner", f"mailto:{CONTACT_EMAIL}?subject=Telephony%20partner%20enquiry",
                        **_kw(st.link_button))


# ===========================================================================
# PAGE: TELEPHONY PARTNERS
# ===========================================================================
# Illustrative prices for the on-page deal calculator ONLY.
# Change these to whatever you're happy to show publicly - they are not
# your price book and nothing here is linked to the real quote tools.
DEMO_LICENCES = {"Essentials": 11.95, "Professional": 16.95, "Contact Centre": 27.95}
DEMO_HANDSETS = {"Yealink T73W": 95, "Fanvil V62 Pro": 110, "Yealink T85W": 165, "Yealink T87W": 210,
                 "Yealink W74P cordless": 120}
DEMO_SETUP_PER_USER = 15.00

HANDSETS = [
    ("Yealink", "T73W", "Yealink_T73W.png", "Compact everyday desk phone with colour screen and built-in Wi-Fi."),
    ("Fanvil", "V62 Pro", "Fanvil_V62_Pro.png", "Affordable desk phone with a cordless Bluetooth handset."),
    ("Yealink", "T85W", "Yealink_T85W.png", "Tilting 5.5-inch screen with AI noise cancellation."),
    ("Yealink", "T87W", "Yealink_T87W.png", "7-inch touchscreen, ideal for managers and reception."),
    ("Yealink", "W74P", "Yealink_W74P.png", "DECT cordless system that grows with the team."),
    ("Yealink", "UH36", "Yealink_UH36_Mono_Headset_UC.png", "Comfortable single-ear USB / 3.5mm headset."),
]


def page_partners():
    # ---------- hero
    left, right = st.columns([1.1, 1], gap="large")
    with left:
        render_html(f'''<div style="padding-top:22px"><div class="pe-eyebrow"><span class="dot"></span>Telephony partner programme</div>
            <div class="nv-hero-t" style="font-size:clamp(2rem,3.8vw,3.1rem)">Your brand.<br>Your customers.<br><span>Our engine room.</span></div>
            <div class="nv-hero-s">With over 40 years of combined experience delivering telephony to UK businesses, we give IT providers,
            security installers and telecoms resellers one place to order hosted UC phone systems. We build, customise and deploy
            every system for you, and equip you with the sales tools to grow.</div></div>''')
        b1, b2, _ = st.columns([1.1, 1.25, 0.5])
        b1.link_button("Become a partner", f"mailto:{CONTACT_EMAIL}?subject=Telephony%20partner%20enquiry",
                       type="primary", **_kw(st.link_button))
        b2.button("Try the quote builder  →", key="p-hero-qb", on_click=go_to, args=("Quote builder",), **BTN_W)
    with right:
        render_html(f'''<div style="padding:26px 20px 40px 10px"><div class="nv-mock nv-qmock">
            <div class="bar"><i></i><i></i><i></i><span class="ttl">Your Brand Telecoms · Quote Q-1042</span></div>
            <div class="row"><span>12 × Professional user licence</span><b>£203.40 /mo</b></div>
            <div class="row"><span>8 × Yealink T85W · 4 × Fanvil V62 Pro</span><b>£1,760</b></div>
            <div class="row"><span>Number porting · IVR · call flows</span><b>Included</b></div>
            <div class="row"><span>Build, test & go-live</span><b style="color:var(--good)">Handled by Novalink</b></div>
            <div class="tot"><span style="color:var(--muted);font-size:.8rem">Your profit over 60 months</span><b style="color:#34D399">£4,243</b></div>
            <div class="nv-float"><div class="g">{I["check"]}</div><div><b>Build sheet sent</b><br><span style="color:#8C98B0">Engineers notified · 12 users</span></div></div>
            </div></div>''')
    render_html('''<div class="nv-bigstats">
        <div><b>40+</b><span>years of combined experience providing telephony solutions to businesses</span></div>
        <div><b>1</b><span>place to order every licence, handset, number and change</span></div>
        <div><b>100%</b><span>built, customised and tested by us before anything goes live</span></div>
        <div><b>Your brand</b><span>on the quotes, the proposals and the customer relationship</span></div></div>''')

    # ---------- who it's for
    render_html(f'''<div class="nv-sec"><div class="pe-eyebrow">Who it's for</div>
        <div class="nv-h2">Already trusted by your customers? <span>Now be their phone provider too.</span></div>
        <div class="nv-lead">Your customers already rely on you. Telephony adds monthly recurring revenue to every account,
        without you hiring engineers, learning a platform or carrying the risk of a bad install.</div>
        <div class="nv-grid g3">
        <div class="nv-tile"><div class="ic">{I["code"]}</div><div class="h">IT & managed service providers</div>
        <div class="p">Complete the stack. Add phones to the desktops, networks and Microsoft 365 you already look after.</div></div>
        <div class="nv-tile"><div class="ic c">{I["shield"]}</div><div class="h">Security & CCTV installers</div>
        <div class="p">You're already on site and on the network. Phones are a natural next sale for the same customer.</div></div>
        <div class="nv-tile"><div class="ic">{I["phone"]}</div><div class="h">Telecoms & connectivity resellers</div>
        <div class="p">Offer a modern hosted UC platform without running your own, and keep the customer relationship.</div></div>
        </div></div>''')

    # ---------- the platform (content mirrors the Fortlox phones page)
    render_html('''<div class="nv-sec"><div class="pe-eyebrow">The platform</div>
        <div class="nv-h2">A complete, modern phone system <span>your customers will love.</span></div>
        <div class="nv-lead">A cloud UC platform that brings calls, messaging, contact-centre tools and team collaboration together.
        Customers keep their numbers and answer from desk phones, mobiles or laptops.</div></div>''')

    def frow(tag, title, text, ticks, img, alt, flip=False):
        ticks_html = "".join(f'<li><span>{I["check"]}</span>{esc(t)}</li>' for t in ticks)
        src = img_uri(img)
        img_html = f'<div class="img"><img src="{src}" alt="{esc(alt)}"></div>' if src else '<div class="img"></div>'
        render_html(f'''<div class="nv-frow {"flip" if flip else ""}">{img_html}<div class="tx">
            <div class="pe-eyebrow">{esc(tag)}</div><div class="h">{esc(title)}</div><div class="p">{esc(text)}</div>
            <ul class="nv-ticks">{ticks_html}</ul></div></div>''')

    frow("Omnichannel", "Every channel, included as standard",
         "Voice, video, messaging and email in one system, so customers can reach your clients however suits them, "
         "with nothing extra to buy.",
         ["Voice, video, messaging and email together", "SMS, WhatsApp, Facebook and live chat",
          "No bolt-ons: everything is included"],
         "Telephony_Omnichannel.jpg", "Calls, WhatsApp, Facebook, live chat, SMS and email connected in one system")
    frow("Contact centre", "A full contact centre, built in",
         "Call queues, smart routing, live statistics and supervisor tools come as standard, "
         "so busy teams never lose track of a caller.",
         ["Live queue panel and wallboard", "Skills-based and intelligent call routing",
          "Supervisor listen, whisper and barge"],
         "Telephony_Wallboard.jpg", "Live wallboard showing waiting calls, answer rates and agents available", flip=True)
    frow("Collaboration", "Their whole team, connected",
         "Messaging, meetings, presence and content sharing sit alongside calls, "
         "so everyone can see who's free and get answers faster.",
         ["Team chat and video meetings in one app", "See who's available at a glance",
          "Share screens and files during calls"],
         "Telephony_Collaboration.jpg", "Team directory showing each colleague's availability")
    also = ["Call recording", "Voicemail to email", "CRM integrations", "Desktop and mobile apps",
            "Visual call-flow builder", "Keep existing numbers", "Hot-desking", "Call reporting"]
    render_html('<div style="display:flex;flex-wrap:wrap;gap:10px;align-items:center;margin-top:36px">'
                '<span style="color:var(--muted);font-size:.85rem;font-weight:600;margin-right:4px">Also included:</span>'
                + "".join(chip(a, "accent") for a in also) + "</div>")

    # ---------- how it works / handover gate
    render_html(f'''<div class="nv-sec"><div class="pe-eyebrow">How the partnership works</div>
        <div class="nv-h2">You sell. We build, test and deploy. <span>Then we hand over.</span></div>
        <div class="nv-lead">Support is only handed over to you once the system is in, fully tested and working seamlessly.
        Your customer's first experience is a smooth go-live, every time.</div>
        <div class="nv-timeline">
        <div class="nv-tl"><div class="n">1</div><div class="who you">You</div><div class="h">Sell & quote</div>
        <div class="p">Price the deal in your own branded quote tool and capture the customer's requirements as you go.</div></div>
        <div class="nv-tl"><div class="n">2</div><div class="who us">Novalink</div><div class="h">Order & design</div>
        <div class="p">One order to us covers licences, numbers, porting and handsets. We plan the build from your build sheet.</div></div>
        <div class="nv-tl"><div class="n">3</div><div class="who us">Novalink</div><div class="h">Build & customise</div>
        <div class="p">Users, extensions, IVRs, opening hours, call groups and handsets configured exactly to the brief.</div></div>
        <div class="nv-tl"><div class="n">4</div><div class="who us">Novalink</div><div class="h">Deploy & test</div>
        <div class="p">Numbers ported, handsets provisioned and every call path tested end to end before go-live.</div></div>
        <div class="nv-tl gate"><div class="n">5</div><div class="who both">Together</div><div class="h">Seamless handover</div>
        <div class="p">Only once it's live, tested and working do we hand ongoing support to you, fully documented.</div></div>
        </div></div>''')
    render_html(f'''<div class="nv-split" style="margin-top:18px">
        <div class="nv-tile" style="border-color:rgba(124,131,255,.35)"><div class="h" style="color:#B9BDFF">What you do</div><ul class="nv-ticks">
        <li><span>{I["check"]}</span>Own the customer relationship and your brand</li>
        <li><span>{I["check"]}</span>Sell and quote with your own price book</li>
        <li><span>{I["check"]}</span>Provide day-to-day support after handover</li>
        <li><span>{I["check"]}</span>Keep the margin, every month, for the life of the contract</li></ul></div>
        <div class="nv-tile" style="border-color:rgba(56,214,245,.35)"><div class="h" style="color:var(--accent-2)">What we do</div><ul class="nv-ticks">
        <li><span>{I["check"]}</span>Platform, licensing and system management</li>
        <li><span>{I["check"]}</span>Build, customisation, porting and handset provisioning</li>
        <li><span>{I["check"]}</span>End-to-end testing and go-live</li>
        <li><span>{I["check"]}</span>Expert back-up behind you, plus one place for every change</li></ul></div></div>''')

    # ---------- sales tools
    render_html(f'''<div class="nv-sec"><div class="pe-eyebrow">Sales tools included</div>
        <div class="nv-h2">We don't just supply the phones. <span>We build your sales engine.</span></div>
        <div class="nv-lead">Using our bespoke app expertise, every partner gets a branded price book and quotation tool,
        so anyone on your team can produce a professional telephony quote in minutes.</div>
        <div class="nv-grid">
        <div class="nv-tile"><div class="ic">{I["calc"]}</div><div class="h">Your price book</div>
        <div class="p">Licences, handsets, setup and deployment, loaded with your margins. Set your own prices from your admin panel.</div></div>
        <div class="nv-tile"><div class="ic c">{I["clip"]}</div><div class="h">Branded quotes & proposals</div>
        <div class="p">Your logo, your colours, your terms. Polished PDF proposals ready to send while you're still with the customer.</div></div>
        <div class="nv-tile"><div class="ic">{I["table"]}</div><div class="h">Build sheet capture</div>
        <div class="p">Users, numbers, opening hours, IVR and call routing captured at quote stage, so our engineers build it right first time.</div></div>
        <div class="nv-tile"><div class="ic c">{I["trend"]}</div><div class="h">Grow from there</div>
        <div class="p">Add prospecting, pipeline tracking or customer reporting apps from our bespoke range as you scale.</div></div>
        </div></div>''')

    # ---------- deal calculator
    render_html('<div class="nv-sec" id="calc"></div>')
    section_header("£", "What could one deal be worth to you?",
                   "Illustrative pricing. Your own price book is built on your real buy prices and margins.")
    c1, c2 = st.columns([1.35, 1], gap="medium")
    with c1:
        with st.container(key="card-calc"):
            a1, a2 = st.columns(2)
            users = a1.number_input("Users", min_value=1, max_value=500, value=12, step=1, key="p_users")
            lic = a2.selectbox("Licence", list(DEMO_LICENCES), index=1, key="p_lic")
            h1, h2 = st.columns([1.4, 1])
            hs = h1.selectbox("Handset", list(DEMO_HANDSETS), index=2, key="p_hs")
            hq = h2.number_input("Handsets", min_value=0, max_value=500, value=int(users), step=1, key="p_hq")
            t1, t2 = st.columns(2)
            term = t1.select_slider("Contract term (months)", [12, 24, 36, 48, 60], value=60, key="p_term")
            margin = t2.slider("Your margin %", 10, 50, 30, step=5, key="p_margin")
            render_html(f'''<div class="nv-drop" style="margin-top:10px"><div class="ic">{I["clip"]}</div>
                <div>In your own quote tool this would also capture the <b style="color:var(--text)">build sheet</b>:
                numbers to port, opening hours, IVR options and call routing, sent straight to our engineers.</div></div>''')
    monthly = users * DEMO_LICENCES[lic]
    hw = hq * DEMO_HANDSETS[hs]
    setup = users * DEMO_SETUP_PER_USER
    m = margin / 100
    p_month = monthly * m
    p_upfront = (hw + setup) * m
    p_total = p_month * term + p_upfront
    with c2:
        with st.container(key="card-calcsum"):
            render_html(f'''<div class="nv-sum"><div class="lab" style="margin-top:0">Customer pays</div>
                <div class="big">{gbp(monthly, 2)}<span style="font-size:1rem;color:var(--muted);font-weight:600"> /month</span></div>
                <div style="color:var(--muted);font-size:.85rem">plus {gbp(hw + setup)} one-off for handsets & setup</div>
                <div class="lab">Your recurring profit</div>
                <div class="big" style="font-size:1.6rem">{gbp(p_month, 2)} /month</div>
                <div class="lab">Your upfront profit</div>
                <div class="big" style="font-size:1.6rem">{gbp(p_upfront)}</div>
                <div class="hl"><div class="lab" style="margin-top:0;color:var(--good)">Total profit over {term} months</div>
                <div class="big">{gbp(p_total)}</div>
                <div style="color:var(--muted);font-size:.82rem;margin-top:4px">From one {users}-user customer. Build, testing and
                deployment handled by Novalink.</div></div></div>''')

    # ---------- handsets
    render_html('''<div class="nv-sec"><div class="pe-eyebrow">The range</div>
        <div class="nv-h2">Leading handsets, <span>supplied and provisioned.</span></div>
        <div class="nv-lead">Yealink and Fanvil desk phones, cordless handsets and headsets, configured by us and delivered ready to plug in.</div></div>''')
    cards = []
    for brand, name, img, desc in HANDSETS:
        src = img_uri(img)
        cards.append(f'''<div class="nv-prod"><div class="stage">{f'<img src="{src}" alt="{esc(brand)} {esc(name)}">' if src else ""}</div>
            <div class="b"><div class="br">{esc(brand)}</div><div class="nm">{esc(name)}</div><div class="d">{esc(desc)}</div></div></div>''')
    render_html('<div class="nv-prods">' + "".join(cards) + "</div>")

    # ---------- CTA
    with st.container(key="ctaband-partners"):
        render_html('''<div class="pe-eyebrow"><span class="dot"></span>Become a partner</div>
            <div class="nv-h2">Add telephony to your business, <span>without the headaches.</span></div>
            <div class="nv-lead" style="margin-bottom:10px">Tell us a little about your business and customers. We'll show you the platform,
            your branded quote tool and how the first deployment would work.</div>''')
        b1, b2, _ = st.columns([1, 1, 2.2])
        b1.link_button("Talk to us about partnering", f"mailto:{CONTACT_EMAIL}?subject=Telephony%20partner%20enquiry",
                       type="primary", **_kw(st.link_button))
        b2.button("Try the quote builder", key="p-to-qb", on_click=go_to, args=("Quote builder",), **BTN_W)



# ===========================================================================
# PAGE: QUOTE BUILDER DEMO
# ===========================================================================
# EXAMPLE price book. "Buy" is what a partner would pay Novalink, "RRP" is the
# suggested starting sell price. All figures are ILLUSTRATIVE - change them
# to whatever you are happy to show publicly.
#            item                         category      unit        buy      rrp     image / note
PRICE_BOOK = [
    ("Essentials user licence",         "Licences",   "per month", 7.50,  11.95, "Calls, voicemail to email, mobile & desktop apps"),
    ("Professional user licence",       "Licences",   "per month", 10.50, 16.95, "Everything in Essentials plus recording, CRM & collaboration"),
    ("Contact Centre agent licence",    "Licences",   "per month", 17.50, 27.95, "Queues, wallboards, supervisor tools & omnichannel"),
    ("Call recording (unlimited)",      "Add-ons",    "per month", 1.50,  3.50,  "Per user, searchable recordings"),
    ("Additional phone number",         "Add-ons",    "per month", 0.75,  2.00,  "Extra local or non-geographic number"),
    ("Live wallboard",                  "Add-ons",    "per month", 6.00,  12.00, "Large-screen queue and agent statistics"),
    ("Yealink T73W",                    "Hardware",   "one-off",   58.00, 95.00, "Yealink_T73W.png"),
    ("Fanvil V62 Pro",                  "Hardware",   "one-off",   66.00, 110.00, "Fanvil_V62_Pro.png"),
    ("Yealink T85W",                    "Hardware",   "one-off",   104.00, 165.00, "Yealink_T85W.png"),
    ("Yealink T87W",                    "Hardware",   "one-off",   132.00, 210.00, "Yealink_T87W.png"),
    ("Yealink W74P cordless",           "Hardware",   "one-off",   74.00, 120.00, "Yealink_W74P.png"),
    ("Yealink UH36 headset",            "Hardware",   "one-off",   24.00, 45.00, "Yealink_UH36_Mono_Headset_UC.png"),
    ("System build & setup (per user)", "Services",   "one-off",   8.00,  15.00, "Configured and tested by our engineers"),
    ("Number porting (per number)",     "Services",   "one-off",   5.00,  12.00, "Keep existing numbers"),
    ("On-site installation day",        "Services",   "one-off",   250.00, 395.00, "Optional engineer visit"),
]
PB_COLS = ["Item", "Category", "Billing", "Your buy price", "Your sell price", "Note"]


def gbp(x, dp=2):
    sign = "-" if x < 0 else ""
    return f"{sign}£{abs(x):,.{dp}f}"


def _default_book():
    return pd.DataFrame([dict(zip(PB_COLS, r)) for r in PRICE_BOOK])


def _round_price(x):
    """Round up to the nearest 5p so prices look like real list prices."""
    return math.ceil(round(x * 20, 6)) / 20


def page_builder():
    ss.setdefault("pb", _default_book())
    ss.setdefault("pb_ver", 0)
    ss.setdefault("qb_brand", "Your Brand Telecoms")

    render_html('''<div class="pe-hero"><div><div class="pe-eyebrow"><span class="dot"></span>Partner quote builder · live demo</div>
        <div class="pe-title">Set your prices. <span>Build a quote in minutes.</span></div>
        <div class="pe-sub">This is the kind of tool every partner receives. Set your own sell prices, build a system for a customer,
        and see exactly what they receive alongside the profit only you can see. All prices here are illustrative.</div></div></div>''')

    # ---------------------------------------------------------------- 01 brand
    with st.container(key="card-qb-brand"):
        section_header("01", "Your brand", "Everything the customer sees carries your name, not ours")
        c1, c2, c3, c4 = st.columns([1.4, 0.6, 1.2, 1])
        brand = c1.text_input("Your company name", key="qb_brand", max_chars=40).strip() or "Your Brand Telecoms"
        colour = c2.color_picker("Brand colour", "#1F4FD8", key="qb_colour")
        email = c3.text_input("Quote contact email", "sales@yourbrand.co.uk", key="qb_email", max_chars=60)
        phone = c4.text_input("Quote contact phone", "01234 567890", key="qb_phone", max_chars=20)

    # ---------------------------------------------------------------- 02 price book
    st.write("")
    with st.container(key="card-qb-pb"):
        section_header("02", "Your price book",
                       "Edit any sell price. You can go as high as you like, but never below your buy price.")
        m1, m2, m3, _ = st.columns([1.2, 0.8, 0.8, 1.2], vertical_alignment="bottom")
        mk = m1.slider("Quick set: markup on everything", 10, 100, 60, step=5, format="%d%%", key="qb_mk",
                       help="Markup on your buy price, rounded up to the nearest 5p")
        if m2.button("Apply markup", key="qb_apply", **BTN_W):
            b = ss.pb.copy()
            b["Your sell price"] = [_round_price(x * (1 + mk / 100)) for x in b["Your buy price"]]
            ss.pb, ss.pb_ver = b, ss.pb_ver + 1
            st.rerun()
        if m3.button("Reset to RRP", key="qb_reset", **BTN_W):
            ss.pb, ss.pb_ver = _default_book(), ss.pb_ver + 1
            st.rerun()

        edited = st.data_editor(
            ss.pb, key=f"pb_editor_{ss.pb_ver}", hide_index=True, disabled=["Item", "Category", "Billing", "Your buy price"],
            column_order=["Item", "Category", "Billing", "Your buy price", "Your sell price"],
            column_config={
                "Your buy price": st.column_config.NumberColumn(format="£%.2f", help="What you pay Novalink"),
                "Your sell price": st.column_config.NumberColumn(format="£%.2f", min_value=0.0, step=0.05,
                                                                 help="What your customer pays. Click to edit."),
            }, height=560, **DF_W)
        book = edited.copy()
        low = book[book["Your sell price"] < book["Your buy price"]]
        if len(low):
            book.loc[low.index, "Your sell price"] = book.loc[low.index, "Your buy price"]
            st.warning("Sell price raised to your buy price for: " + ", ".join(low["Item"]) +
                       ". The tool never lets a quote go out below cost.")
        ss.pb_live = book
        mon = book[book.Billing == "per month"]
        blended = ((mon["Your sell price"] - mon["Your buy price"]) / mon["Your buy price"]).mean() * 100
        render_html('<div style="display:flex;gap:10px;flex-wrap:wrap;margin-top:10px">'
                    + chip(f"Average monthly markup {blended:.0f}%", "good")
                    + chip("Price floors protected", "accent") + chip("Changes apply to every quote instantly", "") + "</div>")

    price = dict(zip(book.Item, book["Your sell price"]))
    cost = dict(zip(book.Item, book["Your buy price"]))
    note = dict(zip(book.Item, book.Note))

    # ---------------------------------------------------------------- 03 build
    st.write("")
    with st.container(key="card-qb-build"):
        section_header("03", "Build the customer's system", "Pick licences, handsets and services, just as you would in front of a customer")
        a1, a2, a3 = st.columns([1.3, 1, 1])
        customer = a1.text_input("Customer name", "Harbour Dental Ltd", key="qb_cust", max_chars=50).strip() or "Customer"
        term = a2.select_slider("Contract term (months)", [12, 24, 36, 48, 60], value=36, key="qb_term")
        hw_mode = a3.radio("Hardware", ["Pay upfront", "Spread over the term"], key="qb_hw", horizontal=False)

        tabs = st.tabs(["Licences & add-ons", "Handsets", "Services"])
        qty = {}
        with tabs[0]:
            cols = st.columns(3)
            defaults = {"Essentials user licence": 4, "Professional user licence": 8, "Contact Centre agent licence": 0,
                        "Call recording (unlimited)": 8, "Additional phone number": 2, "Live wallboard": 0}
            for i, item in enumerate([r[0] for r in PRICE_BOOK if r[1] in ("Licences", "Add-ons")]):
                with cols[i % 3]:
                    qty[item] = st.number_input(item, 0, 999, defaults.get(item, 0), key=f"q_{item}",
                                                help=f"{note[item]} · {gbp(price[item])} per month")
        with tabs[1]:
            hw_items = [r for r in PRICE_BOOK if r[1] == "Hardware"]
            cols = st.columns(6)
            hdef = {"Yealink T73W": 6, "Yealink T85W": 4, "Yealink T87W": 1, "Yealink W74P cordless": 1, "Yealink UH36 headset": 2}
            for c, (item, *_r, img) in zip(cols, hw_items):
                with c:
                    src = img_uri(img)
                    render_html(f'''<div class="nv-prod" style="margin-bottom:8px"><div class="stage" style="height:110px">
                        {f'<img src="{src}" style="max-height:92px">' if src else ""}</div>
                        <div class="b" style="padding:8px 10px"><div class="nm" style="font-size:.84rem">{esc(item)}</div>
                        <div class="d">{gbp(price[item])}</div></div></div>''')
                    qty[item] = st.number_input("Qty", 0, 999, hdef.get(item, 0), key=f"q_{item}",
                                                label_visibility="collapsed")
        with tabs[2]:
            users = sum(qty[i] for i in ("Essentials user licence", "Professional user licence", "Contact Centre agent licence"))
            cols = st.columns(3)
            qty["System build & setup (per user)"] = cols[0].number_input("System build & setup (users)", 0, 999, users,
                                                                          key=f"q_setup_{users}")
            qty["Number porting (per number)"] = cols[1].number_input("Numbers to port", 0, 999, 3, key="q_port")
            qty["On-site installation day"] = cols[2].number_input("On-site installation days", 0, 20, 0, key="q_inst")

        with st.expander("Build sheet: captured for the Novalink engineers"):
            b1, b2 = st.columns(2)
            b1.text_input("Opening hours", "Mon-Fri 08:30-17:30", key="bs_hours")
            b1.text_input("Main number(s) to port", "01632 960000", key="bs_nums")
            b2.text_area("Call flow / IVR", "Press 1 Reception, 2 Treatment co-ordinator, 3 Accounts. "
                                            "Out of hours to voicemail with email alert.", key="bs_ivr", height=104)
            render_html(chip("Sent to Novalink with the order, so the system is built right first time", "good"))

    # ---------------------------------------------------------------- totals
    lines = [(i, q) for i, q in qty.items() if q > 0]
    mon_l = [(i, q) for i, q in lines if book.set_index("Item").loc[i, "Billing"] == "per month"]
    hw_l = [(i, q) for i, q in lines if i in {r[0] for r in PRICE_BOOK if r[1] == "Hardware"}]
    svc_l = [(i, q) for i, q in lines if i in {r[0] for r in PRICE_BOOK if r[1] == "Services"}]
    monthly = sum(price[i] * q for i, q in mon_l)
    hw_total = sum(price[i] * q for i, q in hw_l)
    svc_total = sum(price[i] * q for i, q in svc_l)
    hw_monthly = hw_total / term if hw_mode == "Spread over the term" else 0
    cust_monthly = monthly + hw_monthly
    cust_upfront = svc_total + (hw_total if hw_mode == "Pay upfront" else 0)
    p_month = sum((price[i] - cost[i]) * q for i, q in mon_l)
    p_hw = sum((price[i] - cost[i]) * q for i, q in hw_l)
    p_svc = sum((price[i] - cost[i]) * q for i, q in svc_l)
    p_total = p_month * term + p_hw + p_svc
    c_month = sum(cost[i] * q for i, q in mon_l)

    # ---------------------------------------------------------------- 04 output
    st.write("")
    section_header("04", "What your customer sees, and what only you see")
    t1, t2 = st.tabs(["Customer quote", "Your margin (private)"])
    with t1:
        qref = f"Q-{1000 + zlib.crc32(customer.encode()) % 9000}"
        render_html(customer_quote_html(brand, colour, email, phone, customer, qref, term, hw_mode,
                                        mon_l, hw_l, svc_l, price, note, cust_monthly, cust_upfront, hw_monthly))
        st.write("")
        d1, d2, _ = st.columns([1.2, 1.3, 1.5])
        powered = d2.checkbox("Show 'Powered by Novalink' on the quote", value=False, key="qb_powered")
        pdf = quote_pdf(brand, colour, email, phone, customer, qref, term, hw_mode, mon_l, hw_l, svc_l, price,
                        cust_monthly, cust_upfront, hw_monthly, powered)
        d1.download_button("Download the PDF quote", pdf, file_name=f"{qref}_{customer.replace(' ', '_')}.pdf",
                           mime="application/pdf", type="primary", **_kw(st.download_button))
    with t2:
        render_html(f'''<div class="nv-kpis">
            <div class="pe-kpi"><div class="l">Monthly profit</div><div class="v">{gbp(p_month)}</div>
            <div class="s">{gbp(monthly)} billed · {gbp(c_month)} cost</div></div>
            <div class="pe-kpi c"><div class="l">Hardware profit</div><div class="v">{gbp(p_hw, 0)}</div><div class="s">One-off</div></div>
            <div class="pe-kpi c"><div class="l">Services profit</div><div class="v">{gbp(p_svc, 0)}</div><div class="s">One-off</div></div>
            <div class="pe-kpi g"><div class="l">Total over {term} months</div><div class="v" style="color:var(--good)">{gbp(p_total, 0)}</div>
            <div class="s">From this one customer</div></div></div>''')
        rows = []
        for i, q in lines:
            rows.append({"Item": i, "Qty": q, "Your buy": cost[i], "Your sell": price[i], "Profit per unit": price[i] - cost[i],
                         "Line profit": (price[i] - cost[i]) * q,
                         "Margin %": round((price[i] - cost[i]) / price[i] * 100, 1) if price[i] else 0,
                         "Billing": book.set_index("Item").loc[i, "Billing"]})
        show_df(pd.DataFrame(rows), column_config={
            **{k: st.column_config.NumberColumn(format="£%.2f") for k in ["Your buy", "Your sell", "Profit per unit", "Line profit"]},
            "Margin %": st.column_config.NumberColumn(format="%.1f%%")})
        st.caption("This view is never shown on the customer quote or PDF.")

    with st.container(key="ctaband-builder"):
        render_html('''<div class="pe-eyebrow"><span class="dot"></span>Your own version</div>
            <div class="nv-h2">Want this tool <span>with your logo on it?</span></div>
            <div class="nv-lead" style="margin-bottom:10px">Every partner gets their own branded quote builder and price book, set up with
            real pricing and an admin panel to manage it.</div>''')
        b1, b2, _ = st.columns([1, 1, 2.2])
        b1.link_button("Talk to us about partnering", f"mailto:{CONTACT_EMAIL}?subject=Telephony%20partner%20enquiry",
                       type="primary", **_kw(st.link_button))
        b2.button("Back to the programme", key="qb-back", on_click=go_to, args=("Programme",), **BTN_W)


def _hex_ok(c):
    return c if isinstance(c, str) and len(c) == 7 and c.startswith("#") else "#1F4FD8"


def customer_quote_html(brand, colour, email, phone, customer, qref, term, hw_mode, mon_l, hw_l, svc_l, price, note,
                        cust_monthly, cust_upfront, hw_monthly):
    colour = _hex_ok(colour)

    def rows(ls, unit):
        return "".join(f'<tr><td><b>{esc(i)}</b><div class="n">{esc(note[i]) if not note[i].endswith(".png") else ""}</div></td>'
                       f'<td class="r">{q}</td><td class="r">{gbp(price[i])}</td><td class="r">{gbp(price[i] * q)}{unit}</td></tr>'
                       for i, q in ls)

    hw_rows = rows(hw_l, "")
    if hw_mode == "Spread over the term" and hw_l:
        hw_note = f'<div class="sm">Hardware spread over {term} months: {gbp(hw_monthly)} per month, included in your monthly total.</div>'
    else:
        hw_note = ""
    return f'''<div class="nv-paper" style="--b:{colour}">
      <div class="hd"><div><div class="bn">{esc(brand)}</div><div class="bs">Business telephony proposal</div></div>
      <div class="rf"><div>{esc(qref)}</div><div>Prepared for <b>{esc(customer)}</b></div></div></div>
      <div class="bd">
        <div class="tl">Monthly services</div>
        <table><tr><th>Item</th><th class="r">Qty</th><th class="r">Unit</th><th class="r">Total</th></tr>{rows(mon_l, "")}</table>
        <div class="tl">Hardware</div>
        <table><tr><th>Item</th><th class="r">Qty</th><th class="r">Unit</th><th class="r">Total</th></tr>{hw_rows}</table>{hw_note}
        <div class="tl">Setup & services</div>
        <table><tr><th>Item</th><th class="r">Qty</th><th class="r">Unit</th><th class="r">Total</th></tr>{rows(svc_l, "")}</table>
        <div class="tots"><div class="t"><span>Monthly (ex VAT)</span><b>{gbp(cust_monthly)}</b></div>
        <div class="t"><span>One-off (ex VAT)</span><b>{gbp(cust_upfront)}</b></div>
        <div class="t"><span>Term</span><b>{term} months</b></div></div>
        <div class="inc">Includes full system build, number porting, testing and go-live. Keep your existing numbers.</div>
      </div>
      <div class="ft">{esc(brand)} · {esc(email)} · {esc(phone)}</div></div>'''


def quote_pdf(brand, colour, email, phone, customer, qref, term, hw_mode, mon_l, hw_l, svc_l, price,
              cust_monthly, cust_upfront, hw_monthly, powered):
    from io import BytesIO
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.units import mm
    from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

    B = colors.HexColor(_hex_ok(colour))
    INK, MUTED, LINE = colors.HexColor("#1F2433"), colors.HexColor("#6B7385"), colors.HexColor("#E2E6EF")
    W, H = A4
    e = lambda s: html_lib.escape(str(s), quote=False)

    def page(c, doc):
        c.saveState()
        c.setFillColor(B)
        c.rect(0, H - 34 * mm, W, 34 * mm, stroke=0, fill=1)
        c.setFillColor(colors.white)
        c.setFont("Helvetica-Bold", 18)
        c.drawString(16 * mm, H - 17 * mm, brand[:40])
        c.setFont("Helvetica", 9.5)
        c.drawString(16 * mm, H - 24 * mm, "Business telephony proposal")
        c.setFont("Helvetica-Bold", 10)
        c.drawRightString(W - 16 * mm, H - 17 * mm, qref)
        c.setFont("Helvetica", 9)
        c.drawRightString(W - 16 * mm, H - 24 * mm, f"Prepared for {customer[:50]}")
        c.setFont("Helvetica", 7.5)
        c.setFillColor(MUTED)
        c.drawString(16 * mm, 10 * mm, f"{brand}  ·  {email}  ·  {phone}")
        if powered:
            c.drawRightString(W - 16 * mm, 10 * mm, "Powered by Novalink")
        c.restoreState()

    buf = BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4, leftMargin=16 * mm, rightMargin=16 * mm, topMargin=44 * mm,
                            bottomMargin=18 * mm, title=f"{brand} quote {qref}")
    h2 = ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=11, textColor=B, spaceBefore=10, spaceAfter=5)
    cell = ParagraphStyle("c", fontName="Helvetica", fontSize=8.6, leading=11, textColor=INK)
    cellb = ParagraphStyle("cb", parent=cell, fontName="Helvetica-Bold", textColor=colors.white)
    small = ParagraphStyle("s", fontName="Helvetica", fontSize=8, leading=11, textColor=MUTED)
    cw = [(W - 32 * mm) * f for f in (0.52, 0.12, 0.18, 0.18)]

    def table(ls):
        cellbr = ParagraphStyle("cbr", parent=cellb, alignment=2)
        data = [[Paragraph("Item", cellb)] + [Paragraph(x, cellbr) for x in ("Qty", "Unit price", "Total")]]
        for i, q in ls:
            data.append([Paragraph(e(i), cell), str(q), gbp(price[i]), gbp(price[i] * q)])
        t = Table(data, colWidths=cw)
        t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), B), ("ALIGN", (1, 0), (-1, -1), "RIGHT"),
                               ("FONTSIZE", (0, 1), (-1, -1), 8.6), ("LINEBELOW", (0, 0), (-1, -1), 0.4, LINE),
                               ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F6F7FB")]),
                               ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                               ("VALIGN", (0, 0), (-1, -1), "MIDDLE")]))
        return t

    story = []
    for title, ls in (("Monthly services", mon_l), ("Hardware", hw_l), ("Setup & services", svc_l)):
        if ls:
            story += [Paragraph(title, h2), table(ls)]
            if title == "Hardware" and hw_mode == "Spread over the term":
                story.append(Paragraph(f"Hardware spread over {term} months: {gbp(hw_monthly)} per month, "
                                       f"included in the monthly total.", small))
    tot = Table([["Monthly (ex VAT)", gbp(cust_monthly)], ["One-off (ex VAT)", gbp(cust_upfront)],
                 ["Contract term", f"{term} months"]], colWidths=[(W - 32 * mm) * 0.7, (W - 32 * mm) * 0.3])
    tot.setStyle(TableStyle([("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"), ("FONTSIZE", (0, 0), (-1, -1), 11),
                             ("ALIGN", (1, 0), (1, -1), "RIGHT"), ("TEXTCOLOR", (1, 0), (1, 0), B),
                             ("LINEABOVE", (0, 0), (-1, 0), 1.2, B), ("TOPPADDING", (0, 0), (-1, -1), 6)]))
    story += [Spacer(1, 12), tot, Spacer(1, 10),
              Paragraph("Includes full system build, number porting, end-to-end testing and go-live. "
                        "Keep your existing numbers. Prices exclude VAT. Quote valid for 30 days.", small)]
    doc.build(story, onFirstPage=page, onLaterPages=page)
    return buf.getvalue()


def footer():
    render_html(f'''<div class="nv-foot"><div>© Novalink · Telephony partner programme</div>
        <div>All prices shown in demos are illustrative.</div><div>{esc(CONTACT_EMAIL)}</div></div>''')


{"Programme": page_partners, "Quote builder": page_builder}[ss.page]()
footer()
