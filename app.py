import streamlit as st
import time
from agents import build_reader_agent, build_search_agent, get_writer_chain, get_critic_chain

st.set_page_config(
    page_title="ResearchMind · AI Research Agent",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ═══════════════════════════════════════════════════════════════════════════════
#  MASTER CSS
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cal+Sans&family=Bricolage+Grotesque:opsz,wght@12..96,200;12..96,300;12..96,400;12..96,500;12..96,600;12..96,700;12..96,800&family=JetBrains+Mono:ital,wght@0,100..800;1,100..800&family=Inter:ital,opsz,wght@0,14..32,100..900;1,14..32,100..900&display=swap');

/* ─────────────────────────────────────────────
   RESET & TOKENS
───────────────────────────────────────────── */
:root {
  --orange:      #ff6b2b;
  --orange-dim:  #cc4a10;
  --orange-glow: rgba(255,107,43,0.22);
  --orange-soft: rgba(255,107,43,0.08);
  --green:       #22d97a;
  --green-glow:  rgba(34,217,122,0.18);
  --surface-0:   #080810;
  --surface-1:   rgba(255,255,255,0.028);
  --surface-2:   rgba(255,255,255,0.055);
  --border-dim:  rgba(255,255,255,0.06);
  --border-mid:  rgba(255,255,255,0.10);
  --text-1: #f2ede4;
  --text-2: #9e9890;
  --text-3: #4a453e;
  --radius-sm: 10px;
  --radius-md: 16px;
  --radius-lg: 24px;
  --radius-xl: 32px;
}

*,*::before,*::after { box-sizing:border-box; margin:0; padding:0; }

html, body, [class*="css"] {
  font-family: 'Inter', system-ui, sans-serif;
  color: var(--text-1);
}

/* ── Layered background ── */
.stApp {
  background: var(--surface-0);
  background-image:
    radial-gradient(ellipse 120% 70% at 15% -5%,  rgba(255,107,43,0.16) 0%, transparent 55%),
    radial-gradient(ellipse  80% 60% at 85% 105%, rgba(120,40,255,0.09)  0%, transparent 50%),
    radial-gradient(ellipse  60% 40% at 50%  55%, rgba(255,107,43,0.03)  0%, transparent 60%);
  min-height: 100vh;
}

/* Animated dot-grid overlay */
.stApp::after {
  content: '';
  position: fixed;
  inset: 0;
  background-image: radial-gradient(circle, rgba(255,255,255,0.035) 1px, transparent 1px);
  background-size: 28px 28px;
  pointer-events: none;
  z-index: 0;
  mask-image: radial-gradient(ellipse 80% 80% at 50% 50%, black 0%, transparent 100%);
}

#MainMenu, footer, header { visibility: hidden; }
.block-container {
  padding: 0 2.8rem 7rem;
  max-width: 1300px;
  position: relative;
  z-index: 1;
}

/* ─────────────────────────────────────────────
   KEYFRAMES
───────────────────────────────────────────── */
@keyframes fadeSlideUp {
  from { opacity:0; transform:translateY(28px); }
  to   { opacity:1; transform:translateY(0);    }
}
@keyframes fadeIn {
  from { opacity:0; } to { opacity:1; }
}
@keyframes pulseGlow {
  0%,100% { opacity:.55; transform:scale(1);    }
  50%      { opacity:.90; transform:scale(1.06); }
}
@keyframes pulseRing {
  0%,100% { box-shadow: 0 0 0 0   rgba(255,107,43,0.5); }
  50%      { box-shadow: 0 0 0 6px rgba(255,107,43,0);   }
}
@keyframes shimmerSlide {
  0%   { background-position: -600% center; }
  100% { background-position:  600% center; }
}
@keyframes flowBar {
  0%   { background-position: 0%   center; }
  100% { background-position: 200% center; }
}
@keyframes spin {
  to { transform: rotate(360deg); }
}
@keyframes borderDance {
  0%,100% { border-color: rgba(255,107,43,0.30); }
  50%      { border-color: rgba(255,107,43,0.65); }
}
@keyframes countUp {
  from { opacity:0; transform:translateY(8px); }
  to   { opacity:1; transform:translateY(0);   }
}
@keyframes waveIn {
  0%   { clip-path: inset(0 100% 0 0); }
  100% { clip-path: inset(0 0%   0 0); }
}

/* ─────────────────────────────────────────────
   HERO SECTION
───────────────────────────────────────────── */
.hero-section {
  position: relative;
  padding: 5.5rem 0 3.5rem;
  text-align: center;
  overflow: hidden;
  animation: fadeSlideUp 0.9s cubic-bezier(.22,1,.36,1) both;
}

/* Halo orb */
.hero-section::before {
  content: '';
  position: absolute;
  top: -80px; left: 50%;
  transform: translateX(-50%);
  width: 800px; height: 500px;
  background: radial-gradient(ellipse, rgba(255,107,43,0.16) 0%, transparent 68%);
  animation: pulseGlow 5s ease-in-out infinite;
  pointer-events: none;
}

/* Decorative horizontal rule */
.hero-section::after {
  content: '';
  position: absolute;
  bottom: 0; left: 10%; right: 10%;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(255,107,43,0.25), transparent);
}

.hero-chip {
  display: inline-flex;
  align-items: center;
  gap: .55rem;
  background: rgba(255,107,43,0.09);
  border: 1px solid rgba(255,107,43,0.28);
  border-radius: 100px;
  padding: .38rem 1.1rem;
  font-family: 'JetBrains Mono', monospace;
  font-size: .62rem;
  letter-spacing: .22em;
  text-transform: uppercase;
  color: var(--orange);
  margin-bottom: 1.8rem;
  backdrop-filter: blur(8px);
}
.hero-chip-dot {
  width: 6px; height: 6px;
  border-radius: 50%;
  background: var(--orange);
  animation: pulseRing 1.8s ease-in-out infinite;
  flex-shrink: 0;
}

.hero-title {
  font-family: 'Bricolage Grotesque', sans-serif;
  font-size: clamp(3.8rem, 9vw, 7.5rem);
  font-weight: 800;
  line-height: .92;
  letter-spacing: -.04em;
  margin-bottom: 1.6rem;
}
.hero-title-plain  { color: #eee8de; display: block; }
.hero-title-accent {
  display: block;
  background: linear-gradient(110deg, #ff6b2b 0%, #ff9a6b 35%, #ff6b2b 55%, #ffba8a 80%, #ff6b2b 100%);
  background-size: 400% auto;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  animation: shimmerSlide 4s linear infinite;
}

.hero-desc {
  font-size: 1.08rem;
  font-weight: 350;
  color: var(--text-2);
  max-width: 490px;
  margin: 0 auto 2.5rem;
  line-height: 1.78;
  letter-spacing: .01em;
}

/* Agent badge row */
.badge-row {
  display: flex;
  justify-content: center;
  gap: .6rem;
  flex-wrap: wrap;
}
.agent-badge {
  display: flex;
  align-items: center;
  gap: .4rem;
  background: var(--surface-1);
  border: 1px solid var(--border-dim);
  border-radius: var(--radius-sm);
  padding: .38rem .95rem;
  font-size: .72rem;
  font-weight: 500;
  color: var(--text-3);
  transition: all .25s ease;
  cursor: default;
  letter-spacing: .02em;
}
.agent-badge:hover {
  background: var(--orange-soft);
  border-color: rgba(255,107,43,.3);
  color: #c8a080;
  transform: translateY(-2px);
}

/* ─────────────────────────────────────────────
   SECTION DIVIDER
───────────────────────────────────────────── */
.fancy-divider {
  display: flex;
  align-items: center;
  gap: 1.2rem;
  margin: 2rem 0 2.8rem;
}
.fancy-divider-line {
  flex: 1;
  height: 1px;
  background: linear-gradient(90deg, transparent, var(--border-mid), transparent);
}
.fancy-divider-node {
  width: 8px; height: 8px;
  border-radius: 50%;
  border: 1px solid rgba(255,107,43,.4);
  background: rgba(255,107,43,.15);
  position: relative;
}
.fancy-divider-node::before, .fancy-divider-node::after {
  content: '';
  position: absolute;
  top: 50%; left: 50%;
  transform: translate(-50%,-50%);
  border-radius: 50%;
  border: 1px solid rgba(255,107,43,.2);
}
.fancy-divider-node::before { width:16px; height:16px; }
.fancy-divider-node::after  { width:24px; height:24px; border-color:rgba(255,107,43,.08); }

/* ─────────────────────────────────────────────
   INPUT PANEL
───────────────────────────────────────────── */
.control-panel {
  background: linear-gradient(145deg, rgba(255,107,43,0.07) 0%, rgba(255,255,255,0.02) 100%);
  border: 1px solid rgba(255,107,43,0.2);
  border-radius: var(--radius-xl);
  padding: 2.4rem 2.6rem 2rem;
  position: relative;
  overflow: hidden;
  transition: border-color .35s;
}
.control-panel::before {
  content: '';
  position: absolute;
  top: 0; left: 8%; right: 8%;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(255,107,43,.6), transparent);
}
.control-panel::after {
  content: '';
  position: absolute;
  inset: 0;
  background: radial-gradient(ellipse 70% 40% at 50% 0%, rgba(255,107,43,.04) 0%, transparent 70%);
  pointer-events: none;
}
.control-panel:focus-within {
  border-color: rgba(255,107,43,.45);
  box-shadow: 0 0 60px rgba(255,107,43,.07);
}

.panel-eyebrow {
  font-family: 'JetBrains Mono', monospace;
  font-size: .6rem;
  letter-spacing: .28em;
  text-transform: uppercase;
  color: rgba(255,107,43,.6);
  margin-bottom: 1.4rem;
  display: flex;
  align-items: center;
  gap: .7rem;
}
.panel-eyebrow::after {
  content: '';
  flex: 1;
  height: 1px;
  background: rgba(255,107,43,.15);
}

/* ── Streamlit widget overrides ── */
.stTextInput > label,
.stSelectbox > label {
  font-family: 'JetBrains Mono', monospace !important;
  font-size: .6rem !important;
  letter-spacing: .2em !important;
  text-transform: uppercase !important;
  color: rgba(255,107,43,.7) !important;
  font-weight: 400 !important;
  margin-bottom: .4rem !important;
}

.stTextInput > div > div > input {
  background: rgba(0,0,0,.38) !important;
  border: 1px solid rgba(255,107,43,.18) !important;
  border-radius: var(--radius-md) !important;
  color: #f2ede4 !important;
  font-family: 'Inter', sans-serif !important;
  font-size: 1.02rem !important;
  font-weight: 400 !important;
  padding: .9rem 1.25rem !important;
  transition: all .25s !important;
  letter-spacing: .01em !important;
}
.stTextInput > div > div > input::placeholder { color: #2e2a24 !important; }
.stTextInput > div > div > input:focus {
  border-color: rgba(255,107,43,.6) !important;
  box-shadow: 0 0 0 4px rgba(255,107,43,.07), 0 0 40px rgba(255,107,43,.05) !important;
  background: rgba(0,0,0,.5) !important;
  outline: none !important;
}

.stSelectbox > div > div {
  background: rgba(0,0,0,.38) !important;
  border: 1px solid rgba(255,107,43,.18) !important;
  border-radius: var(--radius-md) !important;
  color: #f2ede4 !important;
  transition: all .25s !important;
}
.stSelectbox > div > div:hover {
  border-color: rgba(255,107,43,.42) !important;
}

/* ── CTA Button ── */
.stButton > button {
  background: linear-gradient(135deg, #ff6b2b 0%, #e84800 45%, #ff6b2b 100%) !important;
  background-size: 200% 200% !important;
  color: #fff !important;
  font-family: 'Bricolage Grotesque', sans-serif !important;
  font-weight: 700 !important;
  font-size: 1rem !important;
  letter-spacing: .05em !important;
  border: none !important;
  border-radius: var(--radius-md) !important;
  padding: 1rem 2.5rem !important;
  width: 100% !important;
  cursor: pointer !important;
  transition: all .3s cubic-bezier(.22,1,.36,1) !important;
  box-shadow:
    0 4px 24px rgba(255,107,43,.38),
    0 1px 0 rgba(255,255,255,.12) inset !important;
  margin-top: .6rem !important;
  position: relative !important;
  overflow: hidden !important;
}
.stButton > button::before {
  content: '' !important;
  position: absolute !important;
  inset: 0 !important;
  background: linear-gradient(105deg, transparent 35%, rgba(255,255,255,.12) 50%, transparent 65%) !important;
  transform: translateX(-100%) !important;
  transition: transform .5s ease !important;
}
.stButton > button:hover {
  transform: translateY(-3px) !important;
  box-shadow:
    0 16px 48px rgba(255,107,43,.5),
    0 1px 0 rgba(255,255,255,.15) inset !important;
}
.stButton > button:hover::before { transform: translateX(100%) !important; }
.stButton > button:active { transform: translateY(-1px) scale(.99) !important; }

/* ── Example pills ── */
.pills-wrap {
  display: flex;
  align-items: center;
  gap: .5rem;
  flex-wrap: wrap;
  margin-top: 1.4rem;
}
.pill-tag {
  font-family: 'JetBrains Mono', monospace;
  font-size: .58rem;
  color: var(--text-3);
  letter-spacing: .18em;
  text-transform: uppercase;
  margin-right: .2rem;
}
.pill {
  background: rgba(255,255,255,.03);
  border: 1px solid rgba(255,255,255,.06);
  border-radius: 100px;
  padding: .28rem .85rem;
  font-size: .72rem;
  color: #5a554e;
  font-family: 'Inter', sans-serif;
  font-weight: 450;
  cursor: default;
  transition: all .2s;
  letter-spacing: .01em;
}
.pill:hover {
  background: rgba(255,107,43,.06);
  border-color: rgba(255,107,43,.22);
  color: #b89070;
}

/* ── Stat trio ── */
.stat-trio {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: .75rem;
  margin-top: 1.2rem;
}
.stat-card {
  background: var(--surface-1);
  border: 1px solid var(--border-dim);
  border-radius: var(--radius-md);
  padding: 1.1rem 1rem;
  text-align: center;
  position: relative;
  overflow: hidden;
  transition: all .25s;
}
.stat-card::before {
  content: '';
  position: absolute;
  inset: 0;
  background: radial-gradient(ellipse 80% 60% at 50% 100%, rgba(255,107,43,.05) 0%, transparent 70%);
  opacity: 0;
  transition: opacity .25s;
}
.stat-card:hover { border-color: rgba(255,107,43,.22); transform: translateY(-2px); }
.stat-card:hover::before { opacity: 1; }
.stat-num {
  font-family: 'Bricolage Grotesque', sans-serif;
  font-size: 2rem;
  font-weight: 800;
  color: var(--orange);
  line-height: 1;
  animation: countUp .6s ease both;
}
.stat-label {
  font-family: 'JetBrains Mono', monospace;
  font-size: .55rem;
  color: var(--text-3);
  letter-spacing: .2em;
  text-transform: uppercase;
  margin-top: .35rem;
}

/* ─────────────────────────────────────────────
   PIPELINE COLUMN
───────────────────────────────────────────── */
.pipeline-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1.3rem;
}
.pipeline-title {
  font-family: 'JetBrains Mono', monospace;
  font-size: .6rem;
  letter-spacing: .26em;
  text-transform: uppercase;
  color: rgba(255,107,43,.55);
}
.pipeline-counter {
  font-family: 'JetBrains Mono', monospace;
  font-size: .62rem;
  color: var(--text-3);
  letter-spacing: .1em;
}

/* Step card */
.step-card {
  position: relative;
  background: var(--surface-1);
  border: 1px solid var(--border-dim);
  border-radius: var(--radius-md);
  padding: 1.15rem 1.4rem;
  margin-bottom: .75rem;
  overflow: hidden;
  transition: all .4s cubic-bezier(.22,1,.36,1);
}
.step-card:hover { border-color: var(--border-mid); transform: translateX(2px); }

.step-card.state-active {
  background: rgba(255,107,43,.06);
  border-color: rgba(255,107,43,.38);
  box-shadow: 0 0 40px rgba(255,107,43,.07), 0 0 0 1px rgba(255,107,43,.1);
  animation: borderDance 2s ease-in-out infinite;
  transform: translateX(4px);
}
.step-card.state-done {
  background: rgba(34,217,122,.04);
  border-color: rgba(34,217,122,.22);
}

/* Left accent */
.step-card::before {
  content: '';
  position: absolute;
  left: 0; top: 12%; bottom: 12%;
  width: 3px;
  border-radius: 0 3px 3px 0;
  background: var(--border-dim);
  transition: all .4s;
}
.step-card.state-active::before {
  background: linear-gradient(180deg, #ff9a6b, #ff6b2b, #cc4a10);
  box-shadow: 0 0 10px rgba(255,107,43,.7);
  top: 0; bottom: 0;
}
.step-card.state-done::before {
  background: linear-gradient(180deg, #6aefaa, #22d97a, #16a854);
  top: 0; bottom: 0;
}

/* Active shimmer sweep */
.step-card.state-active::after {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(100deg, transparent 30%, rgba(255,107,43,.055) 50%, transparent 70%);
  background-size: 200%;
  animation: flowBar 2s linear infinite;
}

.step-layout {
  display: flex;
  align-items: center;
  gap: .95rem;
  position: relative;
  z-index: 1;
}

.step-icon {
  width: 40px; height: 40px;
  border-radius: 12px;
  background: rgba(255,255,255,.04);
  border: 1px solid rgba(255,255,255,.07);
  display: flex; align-items: center; justify-content: center;
  font-size: 1.05rem;
  flex-shrink: 0;
  transition: all .35s;
}
.step-card.state-active .step-icon {
  background: rgba(255,107,43,.14);
  border-color: rgba(255,107,43,.32);
  box-shadow: 0 0 16px rgba(255,107,43,.2);
}
.step-card.state-done .step-icon {
  background: rgba(34,217,122,.1);
  border-color: rgba(34,217,122,.25);
}

.step-text { flex: 1; min-width: 0; }
.step-index {
  font-family: 'JetBrains Mono', monospace;
  font-size: .56rem;
  color: rgba(255,107,43,.45);
  letter-spacing: .18em;
  text-transform: uppercase;
  margin-bottom: .12rem;
}
.step-name {
  font-family: 'Bricolage Grotesque', sans-serif;
  font-size: .93rem;
  font-weight: 600;
  color: #d8d2c8;
  margin-bottom: .1rem;
  letter-spacing: -.01em;
}
.step-desc { font-size: .7rem; color: var(--text-3); font-weight: 400; }
.step-card.state-active .step-desc { color: #7a6a56; }
.step-card.state-done  .step-desc  { color: #3a6a4a; }

.step-badge {
  font-family: 'JetBrains Mono', monospace;
  font-size: .58rem;
  font-weight: 600;
  letter-spacing: .08em;
  padding: .24rem .65rem;
  border-radius: 100px;
  flex-shrink: 0;
  transition: all .3s;
}
.badge-idle    { color: #252018; background: rgba(255,255,255,.03); border: 1px solid rgba(255,255,255,.04); }
.badge-running { color: #ff6b2b; background: rgba(255,107,43,.1);  border: 1px solid rgba(255,107,43,.25); animation: pulseGlow 1.2s ease-in-out infinite; }
.badge-done    { color: #22d97a; background: rgba(34,217,122,.08); border: 1px solid rgba(34,217,122,.2);  }

/* Progress bar */
.progress-shell {
  background: var(--surface-1);
  border: 1px solid var(--border-dim);
  border-radius: var(--radius-md);
  padding: 1.1rem 1.4rem;
  margin-top: .85rem;
}
.progress-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: .65rem;
}
.progress-label {
  font-family: 'JetBrains Mono', monospace;
  font-size: .58rem;
  color: var(--text-3);
  letter-spacing: .15em;
  text-transform: uppercase;
}
.progress-pct {
  font-family: 'JetBrains Mono', monospace;
  font-size: .62rem;
  color: var(--orange);
  letter-spacing: .06em;
}
.progress-track {
  height: 5px;
  background: rgba(255,255,255,.05);
  border-radius: 5px;
  overflow: hidden;
}
.progress-fill {
  height: 100%;
  border-radius: 5px;
  background: linear-gradient(90deg, #ff6b2b, #ff9a6b, #ff6b2b);
  background-size: 200%;
  animation: flowBar 1.8s linear infinite;
  box-shadow: 0 0 10px rgba(255,107,43,.55);
  transition: width .6s cubic-bezier(.22,1,.36,1);
}

/* ─────────────────────────────────────────────
   RESULTS SECTION
───────────────────────────────────────────── */
.results-banner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin: 3.5rem 0 1.8rem;
  padding: 0 .2rem;
}
.results-title {
  font-family: 'Bricolage Grotesque', sans-serif;
  font-size: 1.9rem;
  font-weight: 800;
  color: var(--text-1);
  letter-spacing: -.03em;
}
.results-tag {
  background: rgba(34,217,122,.08);
  border: 1px solid rgba(34,217,122,.2);
  border-radius: 100px;
  padding: .35rem 1rem;
  font-family: 'JetBrains Mono', monospace;
  font-size: .58rem;
  color: var(--green);
  letter-spacing: .18em;
  text-transform: uppercase;
}

/* Expanders */
div[data-testid="stExpander"] {
  background: var(--surface-1) !important;
  border: 1px solid var(--border-dim) !important;
  border-radius: var(--radius-md) !important;
  margin-bottom: .75rem !important;
  overflow: hidden !important;
}
div[data-testid="stExpander"] summary {
  font-family: 'JetBrains Mono', monospace !important;
  font-size: .68rem !important;
  color: #5a5550 !important;
  letter-spacing: .1em !important;
  padding: .95rem 1.4rem !important;
  transition: color .2s !important;
}
div[data-testid="stExpander"] summary:hover { color: #a09080 !important; }

/* Raw output box */
.raw-box {
  background: rgba(0,0,0,.45);
  border: 1px solid rgba(255,255,255,.05);
  border-radius: 12px;
  padding: 1.4rem;
  font-family: 'JetBrains Mono', monospace;
  font-size: .72rem;
  line-height: 1.9;
  color: #5a5550;
  white-space: pre-wrap;
  word-break: break-word;
  max-height: 320px;
  overflow-y: auto;
}
.raw-box::-webkit-scrollbar { width: 3px; }
.raw-box::-webkit-scrollbar-track { background: transparent; }
.raw-box::-webkit-scrollbar-thumb { background: rgba(255,107,43,.2); border-radius: 3px; }

/* Report card */
.report-card {
  position: relative;
  background: linear-gradient(150deg, rgba(255,107,43,.07) 0%, rgba(255,255,255,.02) 50%, rgba(120,40,255,.03) 100%);
  border: 1px solid rgba(255,107,43,.22);
  border-radius: var(--radius-xl);
  padding: 2.8rem 3.2rem;
  margin-bottom: 1.2rem;
  overflow: hidden;
  animation: fadeIn .5s ease both;
}
.report-card::before {
  content: '';
  position: absolute;
  top: 0; left: 10%; right: 10%;
  height: 2px;
  background: linear-gradient(90deg, transparent, #ff6b2b, #ff9a6b, #ff6b2b, transparent);
  border-radius: 2px;
}
.report-card::after {
  content: '';
  position: absolute;
  bottom: 0; right: 0;
  width: 300px; height: 300px;
  background: radial-gradient(ellipse, rgba(255,107,43,.06) 0%, transparent 65%);
  pointer-events: none;
}
.card-eyebrow {
  font-family: 'JetBrains Mono', monospace;
  font-size: .6rem;
  letter-spacing: .25em;
  text-transform: uppercase;
  margin-bottom: 1.6rem;
  display: flex;
  align-items: center;
  gap: .75rem;
}
.card-eyebrow.orange { color: rgba(255,107,43,.75); }
.card-eyebrow.orange::after { content: ''; flex:1; height:1px; background: rgba(255,107,43,.15); }
.card-eyebrow.green  { color: rgba(34,217,122,.75); }
.card-eyebrow.green::after  { content: ''; flex:1; height:1px; background: rgba(34,217,122,.15); }

/* Critic card */
.critic-card {
  position: relative;
  background: linear-gradient(150deg, rgba(34,217,122,.05) 0%, rgba(255,255,255,.02) 100%);
  border: 1px solid rgba(34,217,122,.18);
  border-radius: var(--radius-xl);
  padding: 2.8rem 3.2rem;
  margin-bottom: 1.2rem;
  overflow: hidden;
  animation: fadeIn .5s ease both;
}
.critic-card::before {
  content: '';
  position: absolute;
  top: 0; left: 10%; right: 10%;
  height: 2px;
  background: linear-gradient(90deg, transparent, #22d97a, #6aefaa, #22d97a, transparent);
}

/* Markdown inside cards */
.report-card h1,.report-card h2,.report-card h3,
.critic-card  h1,.critic-card  h2,.critic-card  h3 {
  font-family: 'Bricolage Grotesque', sans-serif !important;
  letter-spacing: -.02em;
  color: #ede8de;
}
.report-card p, .critic-card p {
  color: #8a8278;
  line-height: 1.85;
  font-size: .94rem;
}
.report-card strong, .critic-card strong { color: #c0b8a8; }
.report-card code, .critic-card code {
  background: rgba(255,255,255,.06);
  border-radius: 5px;
  padding: .15em .4em;
  font-family: 'JetBrains Mono', monospace;
  font-size: .85em;
  color: #ff9a6b;
}

/* Download button */
.stDownloadButton > button {
  background: rgba(255,255,255,.04) !important;
  border: 1px solid rgba(255,107,43,.25) !important;
  border-radius: var(--radius-sm) !important;
  color: #ff9a6b !important;
  font-family: 'JetBrains Mono', monospace !important;
  font-size: .65rem !important;
  letter-spacing: .14em !important;
  padding: .65rem 1.6rem !important;
  text-transform: uppercase !important;
  transition: all .25s !important;
}
.stDownloadButton > button:hover {
  background: rgba(255,107,43,.09) !important;
  border-color: rgba(255,107,43,.5) !important;
  transform: translateY(-2px) !important;
  box-shadow: 0 6px 22px rgba(255,107,43,.15) !important;
}

/* Spinner */
.stSpinner > div { border-top-color: var(--orange) !important; }

/* Alerts */
.stAlert { border-radius: var(--radius-md) !important; }

/* ─────────────────────────────────────────────
   FOOTER
───────────────────────────────────────────── */
.site-footer {
  position: fixed;
  bottom: 0; left: 0; right: 0;
  height: 52px;
  background: rgba(8,8,16,.94);
  border-top: 1px solid rgba(255,255,255,.05);
  backdrop-filter: blur(24px);
  -webkit-backdrop-filter: blur(24px);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 2.8rem;
  z-index: 9999;
}
.footer-l {
  font-family: 'JetBrains Mono', monospace;
  font-size: .58rem;
  color: #22201c;
  letter-spacing: .14em;
  text-transform: uppercase;
}
.footer-r {
  font-family: 'JetBrains Mono', monospace;
  font-size: .58rem;
  color: #2a2520;
  letter-spacing: .1em;
}
.footer-r b { color: rgba(255,107,43,.5); font-weight: 500; }

/* ─────────────────────────────────────────────
   SCROLL-BAR (global)
───────────────────────────────────────────── */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(255,107,43,.18); border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: rgba(255,107,43,.35); }
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
#  SESSION STATE
# ═══════════════════════════════════════════════════════════════════════════════
_DEFAULTS = {"results": {}, "running": False, "done": False,
             "selected_model_val": "llama-3.1-8b-instant"}
for k, v in _DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ═══════════════════════════════════════════════════════════════════════════════
#  HELPERS
# ═══════════════════════════════════════════════════════════════════════════════
STEPS = [
    ("search", "01", "Search Agent",  "🔍", "Scans the live web for intelligence"),
    ("reader", "02", "Reader Agent",  "📄", "Deep-scrapes & extracts key content"),
    ("writer", "03", "Writer Chain",  "✍️", "Synthesises a structured report"),
    ("critic", "04", "Critic Chain",  "🧐", "Reviews, scores & refines quality"),
]

def _step_state(key: str) -> str:
    r, run = st.session_state.results, st.session_state.running
    if key in r: return "done"
    if run:
        for k, *_ in STEPS:
            if k not in r:
                return "running" if k == key else "idle"
    return "idle"

def render_pipeline():
    r = st.session_state.results
    done_n = len(r)
    pct = int(done_n / 4 * 100)

    st.markdown(f"""
    <div class="pipeline-header">
      <div class="pipeline-title">Pipeline Status</div>
      <div class="pipeline-counter">{done_n} / 4 complete</div>
    </div>
    """, unsafe_allow_html=True)

    for key, idx, name, icon, desc in STEPS:
        state = _step_state(key)
        card_cls  = {"running": "state-active", "done": "state-done"}.get(state, "")
        badge_cls = {"running": "badge-running", "done": "badge-done"}.get(state, "badge-idle")
        badge_txt = {"running": "● LIVE", "done": "✓ DONE"}.get(state, "IDLE")
        st.markdown(f"""
        <div class="step-card {card_cls}">
          <div class="step-layout">
            <div class="step-icon">{icon}</div>
            <div class="step-text">
              <div class="step-index">STEP {idx}</div>
              <div class="step-name">{name}</div>
              <div class="step-desc">{desc}</div>
            </div>
            <div class="step-badge {badge_cls}">{badge_txt}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="progress-shell">
      <div class="progress-meta">
        <span class="progress-label">Overall Progress</span>
        <span class="progress-pct">{pct}%</span>
      </div>
      <div class="progress-track">
        <div class="progress-fill" style="width:{pct}%"></div>
      </div>
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
#  HERO
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="hero-section">
  <div class="hero-chip">
    <div class="hero-chip-dot"></div>
    Multi-Agent AI System &nbsp;·&nbsp; v3.0
  </div>
  <div class="hero-title">
    <span class="hero-title-plain">Research</span>
    <span class="hero-title-accent">Mind.</span>
  </div>
  <p class="hero-desc">
    Four specialized AI agents collaborate in real-time —
    searching the live web, reading sources, writing reports,
    and critiquing quality — all in one seamless pipeline.
  </p>
  <div class="badge-row">
    <div class="agent-badge">🔍&nbsp; Search Agent</div>
    <div class="agent-badge">📄&nbsp; Reader Agent</div>
    <div class="agent-badge">✍️&nbsp; Writer Chain</div>
    <div class="agent-badge">🧐&nbsp; Critic Chain</div>
  </div>
</div>

<div class="fancy-divider">
  <div class="fancy-divider-line"></div>
  <div class="fancy-divider-node"></div>
  <div class="fancy-divider-line"></div>
</div>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
#  MAIN LAYOUT
# ═══════════════════════════════════════════════════════════════════════════════
col_l, _gap, col_r = st.columns([5, .35, 4])

# ── LEFT ─────────────────────────────────────────────────────────────────────
with col_l:
    st.markdown('<div class="control-panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-eyebrow">Configure Your Research</div>', unsafe_allow_html=True)

    topic = st.text_input(
        "Research Topic",
        placeholder="e.g.  Quantum computing breakthroughs in 2025 …",
        key="topic_input",
    )
    selected_model = st.selectbox(
        "Model Engine",
        options=["llama-3.1-8b-instant", "qwen/qwen3-32b", "llama-3.3-70b-versatile"],
        index=0,
        key="model_select",
    )
    run_btn = st.button("⚡  Launch Research Pipeline", use_container_width=True)

    st.markdown("""
    <div class="pills-wrap">
      <span class="pill-tag">Try →</span>
      <span class="pill">LLM agents 2025</span>
      <span class="pill">CRISPR gene editing</span>
      <span class="pill">Fusion energy</span>
      <span class="pill">Neuromorphic chips</span>
      <span class="pill">AlphaFold 3</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Stat row
    st.markdown("""
    <div class="stat-trio">
      <div class="stat-card">
        <div class="stat-num">4</div>
        <div class="stat-label">Agents</div>
      </div>
      <div class="stat-card">
        <div class="stat-num">3</div>
        <div class="stat-label">Models</div>
      </div>
      <div class="stat-card">
        <div class="stat-num">∞</div>
        <div class="stat-label">Topics</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

# ── RIGHT ────────────────────────────────────────────────────────────────────
with col_r:
    render_pipeline()


# ═══════════════════════════════════════════════════════════════════════════════
#  TRIGGER
# ═══════════════════════════════════════════════════════════════════════════════
if run_btn:
    if not topic.strip():
        st.warning("⚠️  Please enter a research topic first.")
    else:
        st.session_state.results = {}
        st.session_state.running = True
        st.session_state.done    = False
        st.session_state.selected_model_val = selected_model
        st.rerun()


# ═══════════════════════════════════════════════════════════════════════════════
#  PIPELINE EXECUTION
# ═══════════════════════════════════════════════════════════════════════════════
if st.session_state.running and not st.session_state.done:
    results   = {}
    topic_val = st.session_state.topic_input
    model_val = st.session_state.selected_model_val

    with st.spinner("🔍  Search Agent scanning the web…"):
        agent = build_search_agent(model_val)
        sr = agent.invoke({
            "messages": [("user", f"Find recent, reliable and detailed information about: {topic_val}")]
        })
        results["search"] = sr["messages"][-1].content
        st.session_state.results = dict(results)

    with st.spinner("📄  Reader Agent extracting deep content…"):
        agent = build_reader_agent(model_val)
        rr = agent.invoke({
            "messages": [("user",
                f"Based on these search results about '{topic_val}', "
                f"pick the most relevant URL and scrape it for deeper content.\n\n"
                f"Search Results:\n{results['search'][:800]}"
            )]
        })
        results["reader"] = rr["messages"][-1].content
        st.session_state.results = dict(results)

    with st.spinner("✍️  Writer Chain drafting your report…"):
        chain = get_writer_chain(model_val)
        results["writer"] = chain.invoke({
            "topic": topic_val,
            "research": f"SEARCH RESULTS:\n{results['search']}\n\nDETAILED CONTENT:\n{results['reader']}"
        })
        st.session_state.results = dict(results)

    with st.spinner("🧐  Critic Chain reviewing & scoring…"):
        chain = get_critic_chain(model_val)
        results["critic"] = chain.invoke({"report": results["writer"]})
        st.session_state.results = dict(results)

    st.session_state.running = False
    st.session_state.done    = True
    st.rerun()


# ═══════════════════════════════════════════════════════════════════════════════
#  RESULTS
# ═══════════════════════════════════════════════════════════════════════════════
r = st.session_state.results

if r:
    st.markdown("""
    <div class="fancy-divider" style="margin-top:3rem;">
      <div class="fancy-divider-line"></div>
      <div class="fancy-divider-node"></div>
      <div class="fancy-divider-line"></div>
    </div>
    <div class="results-banner">
      <div class="results-title">Results</div>
      <div class="results-tag">✓ Pipeline Complete</div>
    </div>
    """, unsafe_allow_html=True)

    # Raw outputs
    if "search" in r:
        with st.expander("🔍  Search Agent — raw intelligence", expanded=False):
            st.markdown(f'<div class="raw-box">{r["search"]}</div>', unsafe_allow_html=True)

    if "reader" in r:
        with st.expander("📄  Reader Agent — scraped content", expanded=False):
            st.markdown(f'<div class="raw-box">{r["reader"]}</div>', unsafe_allow_html=True)

    # Final report
    if "writer" in r:
        st.markdown('<div class="report-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-eyebrow orange">📝 Final Research Report</div>',
                    unsafe_allow_html=True)
        st.markdown(r["writer"])
        st.markdown('</div>', unsafe_allow_html=True)

        c1, c2 = st.columns([2, 6])
        with c1:
            st.download_button(
                label="⬇  Download .md",
                data=r["writer"],
                file_name=f"research_report_{int(time.time())}.md",
                mime="text/markdown",
            )

    # Critic feedback
    if "critic" in r:
        st.markdown('<div class="critic-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-eyebrow green">🧐 Critic Feedback & Quality Score</div>',
                    unsafe_allow_html=True)
        st.markdown(r["critic"])
        st.markdown('</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
#  FOOTER
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="site-footer">
  <div class="footer-l">ResearchMind · Multi-Agent AI · LangChain + Streamlit</div>
  <div class="footer-r">© 2026 · Built by <b>Shreeyansh Asati</b></div>
</div>
""", unsafe_allow_html=True)
