#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DOKA PRO - Exclave Ultimate Edition 2025 ✨
Source: Exclave VPN (Single Channel)
Features: Light/Dark Mode, PWA, REAL Ping for Exclave, Glassmorphism
"""

from __future__ import annotations

import json
import re
import random
import socket
import time
import base64
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from typing import Final

import requests

# ==================== الثوابت ====================
SOURCES: Final[dict[str, str]] = {
    "exclave": "https://t.me/s/exclaveVPN",
}

OUTPUT_FILE: Final[Path] = Path("index.html")
DATA_FILE: Final[Path] = Path("stats.json")
MANIFEST_FILE: Final[Path] = Path("manifest.json")

SUPPORTED_PROTOCOLS: Final[tuple[str, ...]] = ("vmess", "vless", "trojan", "ss", "hysteria2")

REQUEST_HEADERS: Final[dict[str, str]] = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

COUNTRY_HINTS: Final[dict[str, str]] = {
    "singapore": "🇸🇬", "germany": "🇩🇪", "netherlands": "🇳🇱",
    "united states": "🇺🇸", "usa": "🇺🇸", "united kingdom": "🇬🇧",
    "japan": "🇯🇵", "france": "🇫🇷", "canada": "🇨🇦",
    "hong kong": "🇭🇰", "uae": "🇦🇪", "turkey": "🇹🇷",
    "india": "🇮🇳", "brazil": "🇧🇷", "russia": "🇷🇺",
    "australia": "🇦🇺", "south korea": "🇰🇷",
}

PROTOCOL_COLORS: Final[dict[str, str]] = {
    "vmess": "#8b5cf6", "vless": "#06b6d4", "trojan": "#f59e0b",
    "ss": "#10b981", "hysteria2": "#ec4899", "unknown": "#6366f1",
}

PROTOCOL_ICONS: Final[dict[str, str]] = {
    "vmess": "fa-bolt", "vless": "fa-feather", "trojan": "fa-shield-haltered",
    "ss": "fa-ghost", "hysteria2": "fa-fire", "unknown": "fa-cube",
}


# ==================== دوال Ping (تم إصلاح Exclave) ====================
def extract_host(url: str) -> str | None:
    """استخراج الهوست - تم إصلاحه لروابط Exclave المشفرة."""
    try:
        if "://" not in url:
            return None
        
        # ✅ معالجة خاصة لروابط Exclave المشفرة
        if url.startswith("exclave://"):
            # محاولة فك تشفير base64
            base64_match = re.search(r'\?(eNp[a-zA-Z0-9+/=]+)', url)
            if base64_match:
                try:
                    decoded = base64.b64decode(base64_match.group(1)).decode("utf-8", errors="ignore")
                    host_match = re.search(r'([a-zA-Z0-9][-a-zA-Z0-9]*\.)+[a-zA-Z]{2,}', decoded)
                    if host_match:
                        return host_match.group(0)
                except:
                    pass
            
            # محاولة استخراج الهوست من الـ SNI
            sni_match = re.search(r'[&?]sni=([^&]+)', url)
            if sni_match:
                return sni_match.group(1)
            
            # أي دومين في الرابط
            domain_match = re.search(r'([a-zA-Z0-9][-a-zA-Z0-9]*\.)+[a-zA-Z]{2,}', url)
            if domain_match:
                return domain_match.group(0)
            
            return None
        
        # للروابط العادية
        encoded = url.split("://", 1)[1]
        if "?" in encoded:
            encoded = encoded.split("?")[1]
        
        if url.startswith("vmess://"):
            decoded = base64.b64decode(encoded).decode("utf-8", errors="ignore")
            return json.loads(decoded).get("add")
        
        for part in encoded.split("@"):
            c = part.split(":")[0]
            if "." in c and not c.startswith(("http", "tcp", "ws", "grpc", "hysteria", "exclave")):
                return c
        
        sni = re.search(r'sni=([^&]+)', encoded)
        if sni:
            return sni.group(1)
        
        return None
    except:
        return None


def tcp_ping(host: str) -> int | None:
    """فحص اتصال TCP للبو 443."""
    try:
        start = time.monotonic()
        with socket.create_connection((host, 443), timeout=2.0):
            return int((time.monotonic() - start) * 1000)
    except:
        return None


def ping_server(url: str) -> tuple[int | None, bool]:
    """فحص سيرفر مع محاولتين."""
    host = extract_host(url)
    if not host:
        return None, False
    for _ in range(2):
        r = tcp_ping(host)
        if r:
            return r, True
    return None, False


def measure_pings(servers: list[dict]) -> list[dict]:
    """فحص جميع السيرفرات بالتوازي."""
    print(f"🧪 جاري فحص {len(servers)} سيرفر...")
    with ThreadPoolExecutor(max_workers=30) as ex:
        futures = {ex.submit(ping_server, s["url"]): i for i, s in enumerate(servers)}
        for f in as_completed(futures):
            i = futures[f]
            p, a = f.result()
            servers[i]["ping"] = p if p else random.randint(200, 400)
            servers[i]["alive"] = a
    
    alive = sum(1 for s in servers if s["alive"])
    print(f"   ✅ {alive}/{len(servers)} سيرفر حي")
    return servers


# ==================== دوال الجلب ====================
def fetch_page(url: str, name: str) -> str:
    """جلب صفحة تيليجرام."""
    print(f"📥 جاري جلب {name}...")
    try:
        r = requests.get(url, headers=REQUEST_HEADERS, timeout=30)
        r.raise_for_status()
        return r.text
    except Exception as e:
        print(f"❌ {name}: {e}")
        return ""


def extract_links(html: str, source: str) -> list[str]:
    """استخراج روابط Exclave من HTML."""
    if source == "exclave":
        pattern = r'exclave://[^\s<"\'\s]+'
    else:
        protocols = "|".join(SUPPORTED_PROTOCOLS)
        pattern = rf"(?:{protocols})://[^\s<>\"'\n\r\t]+"
    
    matches = re.findall(pattern, html, re.IGNORECASE)
    seen, clean = set(), []
    for link in matches:
        cleaned = link.replace("&amp;", "&").split("<")[0].split('"')[0].strip()
        if cleaned and cleaned not in seen:
            seen.add(cleaned)
            clean.append(cleaned)
    return clean


def extract_proto(url: str) -> str:
    """استخراج نوع البروتوكول من الرابط."""
    url_lower = url.lower()
    
    if "exclave://" in url_lower:
        match = re.match(r'exclave://([a-z0-9]+)[?/]', url_lower)
        if match and match.group(1) in SUPPORTED_PROTOCOLS:
            return match.group(1).upper()
        for proto in SUPPORTED_PROTOCOLS:
            if f"exclave://{proto}" in url_lower:
                return proto.upper()
        return "UNKNOWN"
    
    for proto in SUPPORTED_PROTOCOLS:
        if f"{proto}://" in url_lower:
            return proto.upper()
    return "UNKNOWN"


def detect_country(url: str) -> str:
    """تخمين الدولة من الرابط."""
    for hint, flag in COUNTRY_HINTS.items():
        if hint in url.lower():
            return flag
    return "🌍"


def build_servers(links: list[str], source: str) -> list[dict]:
    """بناء قائمة السيرفرات."""
    servers = []
    for link in links:
        proto = extract_proto(link)
        servers.append({
            "url": link,
            "proto": proto,
            "country": detect_country(link),
            "ping": random.randint(100, 300),
            "alive": False,
            "source": source,
        })
    return servers


# ==================== توليد Manifest ====================
def gen_manifest() -> str:
    """توليد manifest.json لـ PWA."""
    m = {
        "name": "DOKA PRO - Exclave VPN",
        "short_name": "DOKA PRO",
        "description": "سيرفرات Exclave VPN حصرية - محدثة تلقائياً",
        "start_url": "/index.html",
        "display": "standalone",
        "orientation": "portrait",
        "background_color": "#0f172a",
        "theme_color": "#8b5cf6",
        "lang": "ar",
        "dir": "rtl",
        "icons": [{
            "src": "data:image/svg+xml," + (
                "%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 512 512'%3E"
                "%3Cdefs%3E%3ClinearGradient id='bg' x1='0%25' y1='0%25' x2='100%25' y2='100%25'%3E"
                "%3Cstop offset='0%25' style='stop-color:%238b5cf6'/%3E%3Cstop offset='100%25' style='stop-color:%234f46e5'/%3E"
                "%3C/linearGradient%3E%3C/defs%3E"
                "%3Crect width='512' height='512' rx='120' fill='url(%23bg)'/%3E"
                "%3Ctext x='256' y='320' text-anchor='middle' font-family='Arial' font-size='220' fill='white'%3E🌐%3C/text%3E"
                "%3Ctext x='256' y='400' text-anchor='middle' font-family='Arial' font-weight='bold' font-size='60' fill='white'%3EDOKA%3C/text%3E"
                "%3C/svg%3E"
            ),
            "sizes": "512x512",
            "type": "image/svg+xml",
            "purpose": "any maskable"
        }]
    }
    return json.dumps(m, indent=2, ensure_ascii=False)


# ==================== توليد HTML ====================
def gen_html(servers: list[dict], total: int, src_counts: dict) -> str:
    """توليد صفحة HTML كاملة."""
    now = datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d %H:%M")
    servers_json = json.dumps(servers, ensure_ascii=False)
    alive = sum(1 for s in servers if s["alive"])

    counts: dict[str, int] = {}
    for s in servers:
        p = s["proto"].lower()
        counts[p] = counts.get(p, 0) + 1

    stats = {
        "last_updated": datetime.now(timezone.utc).isoformat(),
        "total": total,
        "alive": alive,
        "by_protocol": counts,
    }
    DATA_FILE.write_text(json.dumps(stats, indent=2, ensure_ascii=False), encoding="utf-8")
    MANIFEST_FILE.write_text(gen_manifest(), encoding="utf-8")

    proto_btns = ""
    for proto in SUPPORTED_PROTOCOLS:
        cnt = counts.get(proto, 0)
        if cnt > 0:
            color = PROTOCOL_COLORS[proto]
            proto_btns += f"""<button class="chip" data-filter="{proto}" style="--c:{color}">{proto.upper()} <span class="cnt">{cnt}</span></button>"""

    return f"""\
<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
<meta name="theme-color" content="#8b5cf6"><meta name="apple-mobile-web-app-capable" content="yes"><meta name="apple-mobile-web-app-title" content="DOKA PRO"><title>DOKA PRO • Exclave</title>
<link rel="manifest" href="manifest.json"><link rel="apple-touch-icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 512 512'%3E%3Crect width='512' height='512' rx='120' fill='%238b5cf6'/%3E%3Ctext x='256' y='320' text-anchor='middle' font-size='220' fill='white'%3E🌐%3C/text%3E%3C/svg%3E">
<link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap" rel="stylesheet"><link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css"><script src="https://cdnjs.cloudflare.com/ajax/libs/qrcodejs/1.0.0/qrcode.min.js"></script><script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<style>
:root{{--bg:#f8fafc;--surface:#fff;--border:#e2e8f0;--text:#1e293b;--sub:#64748b;--pri:#8b5cf6;--suc:#10b981;--dan:#ef4444;--shadow:0 1px 3px rgba(0,0,0,.06);--card-bg:#fff;--url-bg:#f1f5f9;--header-bg:rgba(255,255,255,.85);--gradient:linear-gradient(135deg,#8b5cf6,#6366f1)}}
.dark{{--bg:#0b1120;--surface:#1a2332;--border:#2a3a4f;--text:#f1f5f9;--sub:#94a3b8;--shadow:0 1px 3px rgba(0,0,0,.3);--card-bg:#1a2332;--url-bg:#0f172a;--header-bg:rgba(26,35,50,.9)}}
*{{margin:0;padding:0;box-sizing:border-box}}body{{font-family:'Cairo',sans-serif;background:var(--bg);color:var(--text);min-height:100vh;transition:all .3s;padding:12px 12px 32px;padding-top:max(12px,env(safe-area-inset-top))}}.container{{max-width:480px;margin:0 auto}}
.header{{display:flex;align-items:center;justify-content:space-between;margin-bottom:20px;background:var(--header-bg);backdrop-filter:blur(20px);-webkit-backdrop-filter:blur(20px);padding:14px 18px;border-radius:24px;border:1px solid var(--border);position:sticky;top:12px;z-index:50}}
.logo{{font-size:1.4rem;font-weight:900;background:var(--gradient);-webkit-background-clip:text;-webkit-text-fill-color:transparent}}
.header-actions{{display:flex;align-items:center;gap:8px}}
.theme-btn{{width:40px;height:40px;border-radius:50%;border:1px solid var(--border);background:var(--surface);color:var(--text);cursor:pointer;font-size:1.1rem;display:flex;align-items:center;justify-content:center;transition:all .2s}}
.theme-btn:hover{{transform:scale(1.05)}}
.stats-row{{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:20px}}
.stat{{background:var(--surface);border:1px solid var(--border);border-radius:20px;padding:18px 14px;text-align:center;box-shadow:var(--shadow)}}
.stat-num{{font-size:2rem;font-weight:900;line-height:1}}
.stat-lbl{{font-size:.7rem;color:var(--sub);margin-top:4px}}
.section-title{{font-size:.7rem;color:var(--sub);margin-bottom:8px;font-weight:600}}
.filters{{display:flex;gap:6px;overflow-x:auto;padding-bottom:8px;margin-bottom:16px;-webkit-overflow-scrolling:touch;scrollbar-width:none}}
.filters::-webkit-scrollbar{{display:none}}
.chip{{padding:9px 18px;border-radius:50px;border:1px solid var(--border);background:var(--surface);color:var(--sub);font-family:'Cairo',sans-serif;font-weight:700;font-size:.78rem;white-space:nowrap;cursor:pointer;transition:all .2s;display:flex;align-items:center;gap:6px;box-shadow:var(--shadow)}}
.chip.active{{background:var(--gradient);color:white;border-color:transparent;box-shadow:0 4px 15px rgba(139,92,246,.3)}}
.cnt{{font-size:.65rem;background:rgba(255,255,255,.2);padding:2px 6px;border-radius:50px}}
.card{{background:var(--card-bg);border:1px solid var(--border);border-radius:20px;padding:18px;margin-bottom:12px;box-shadow:var(--shadow);transition:all .2s}}
.card:active{{transform:scale(.98)}}
.card-row{{display:flex;justify-content:space-between;align-items:center;margin-bottom:10px}}
.badge{{display:flex;align-items:center;gap:6px}}
.flag{{font-size:1.4rem}}.tag{{padding:5px 10px;border-radius:50px;font-size:.65rem;font-weight:700;color:white}}
.status{{font-size:.65rem;font-weight:600;display:flex;align-items:center;gap:3px}}
.dot{{width:6px;height:6px;border-radius:50%}}.dot-up{{background:var(--suc)}}.dot-down{{background:var(--dan)}}
.url-box{{background:var(--url-bg);padding:11px 13px;border-radius:14px;font-family:monospace;font-size:.63rem;color:var(--sub);direction:ltr;text-align:left;word-break:break-all;margin-bottom:12px;border:1px solid var(--border)}}
.actions{{display:flex;gap:8px}}
.btn{{flex:1;padding:12px;border-radius:14px;border:none;font-family:'Cairo',sans-serif;font-weight:700;font-size:.78rem;cursor:pointer;transition:all .2s;display:flex;align-items:center;justify-content:center;gap:6px;color:white}}
.btn:hover{{opacity:.9}}.btn:active{{transform:scale(.96)}}
.btn-qr{{width:44px;height:44px;border-radius:14px;border:1px solid var(--border);background:var(--surface);color:var(--text);cursor:pointer;font-size:1rem;flex-shrink:0;display:flex;align-items:center;justify-content:center}}
.qr-box{{margin-top:10px;padding:16px;background:#fff;border-radius:14px;display:none;justify-content:center}}
.toast{{position:fixed;bottom:30px;left:50%;transform:translateX(-50%) translateY(100px);background:#10b981;color:white;padding:12px 24px;border-radius:50px;font-weight:700;font-size:.85rem;z-index:999;opacity:0;transition:all .3s;box-shadow:0 10px 30px rgba(16,185,129,.3)}}
.toast.on{{opacity:1;transform:translateX(-50%) translateY(0)}}
.stats-page{{max-width:480px;margin:40px auto;padding:16px;text-align:center}}
.stats-card{{background:var(--surface);border:1px solid var(--border);border-radius:24px;padding:32px 20px;box-shadow:var(--shadow)}}
.footer{{text-align:center;padding:24px;color:var(--sub);font-size:.7rem}}
@media(min-width:768px){{.container{{max-width:600px}}}}
</style></head><body>
<div class="container">
<div class="header"><div class="logo">⬡ DOKA EXCLAVE</div><div class="header-actions"><button class="theme-btn" id="theme-btn" title="تغيير الوضع">🌙</button></div></div>
<div class="stats-row">
<div class="stat"><div class="stat-num" style="background:var(--gradient);-webkit-background-clip:text;-webkit-text-fill-color:transparent">{total}</div><div class="stat-lbl">🔰 إجمالي السيرفرات</div></div>
<div class="stat"><div class="stat-num" style="color:#10b981;">{alive}</div><div class="stat-lbl">⚡ أونلاين الآن</div></div>
</div>
<div class="section-title">🧩 فلترة بالبروتوكول</div><div class="filters"><button class="chip active" data-filter="all" style="--c:#8b5cf6">🌐 الكل <span class="cnt">{total}</span></button>{proto_btns}</div>
<div id="list"></div><div id="empty" style="display:none;text-align:center;color:var(--sub);padding:40px;">😴 لا توجد سيرفرات</div>
</div>
<div class="toast" id="toast">✅ تم نسخ الرابط!</div>
<div class="stats-page" id="stats-pg" style="display:none;"><div class="stats-card"><h2 style="margin-bottom:20px;">📊 الإحصائيات</h2><canvas id="chart" style="max-height:300px;"></canvas><p style="color:var(--sub);margin-top:16px;">آخر تحديث: <span id="last-up"></span></p><button onclick="location.reload()" style="margin-top:20px;padding:14px 40px;border-radius:50px;border:none;background:var(--gradient);color:white;font-family:'Cairo',sans-serif;font-weight:700;cursor:pointer;">⬅️ عودة</button></div></div>
<div class="footer">© 2026 <strong>DOKA PRO</strong> • Exclave VPN • <button id="stats-btn" style="background:none;border:none;color:var(--pri);cursor:pointer;font-family:'Cairo',sans-serif;font-weight:600;">📊 إحصائيات</button></div>
<script>
const data={servers_json};
const colors={json.dumps(PROTOCOL_COLORS)};
const icons={json.dumps(PROTOCOL_ICONS)};
let filter='all',chartInst=null;

const themeBtn=document.getElementById('theme-btn');
const isDark=localStorage.getItem('doka-theme')==='dark';
if(isDark){{document.body.classList.add('dark');themeBtn.innerHTML='☀️';}}else{{themeBtn.innerHTML='🌙';}}
themeBtn.addEventListener('click',()=>{{document.body.classList.toggle('dark');const dark=document.body.classList.contains('dark');localStorage.setItem('doka-theme',dark?'dark':'light');themeBtn.innerHTML=dark?'☀️':'🌙';}});

function render(f){{
filter=f;const list=document.getElementById('list');let filtered=f==='all'?data:data.filter(s=>s.proto.toLowerCase()===f);
if(!filtered.length){{list.innerHTML='';document.getElementById('empty').style.display='block';return}}
document.getElementById('empty').style.display='none';
list.innerHTML=filtered.map((s,i)=>{{const c=colors[s.proto.toLowerCase()]||'#8b5cf6';const ic=icons[s.proto.toLowerCase()]||'fa-link';const up=s.alive;
return`<div class="card"><div class="card-row"><div class="badge"><span class="flag">${{s.country}}</span><span class="tag" style="background:${{c}}"><i class="fas ${{ic}}"></i> ${{s.proto}}</span><span class="status" style="color:${{up?'var(--suc)':'var(--dan)'}}"><span class="dot ${{up?'dot-up':'dot-down'}}"></span> ${{up?'حي':'ميت'}}</span></div><span style="font-size:.65rem;color:var(--sub);">${{up?s.ping+'ms':'---'}}</span></div><div class="url-box">${{s.url}}</div><div class="actions"><button class="btn" style="background:${{c}}" onclick="cp('${{s.url.replace(/'/g,"\\'")}}')"><i class="far fa-copy"></i> نسخ</button><button class="btn-qr" onclick="qr('q${{i}}','${{s.url.replace(/'/g,"\\'")}}')"><i class="fas fa-qrcode"></i></button></div><div class="qr-box" id="q${{i}}"></div></div>`;}}).join('');}}

document.querySelectorAll('.chip').forEach(c=>c.addEventListener('click',function(){{document.querySelectorAll('.chip').forEach(b=>b.classList.remove('active'));this.classList.add('active');render(this.dataset.filter);}}));
window.cp=t=>{{navigator.clipboard.writeText(t);const toast=document.getElementById('toast');toast.classList.add('on');clearTimeout(toast._t);toast._t=setTimeout(()=>toast.classList.remove('on'),2000);}};
window.qr=(id,link)=>{{const el=document.getElementById(id);if(el.style.display==='flex'){{el.style.display='none';return}}if(!el.innerHTML)new QRCode(el,{{text:link,width:140,height:140,colorDark:'#1e293b'}});el.style.display='flex';}};
document.getElementById('stats-btn').addEventListener('click',async()=>{{document.querySelector('.header').style.display='none';document.querySelectorAll('.stats-row,.section-title,.filters').forEach(e=>e.style.display='none');document.getElementById('list').style.display='none';document.querySelector('.footer').style.display='none';document.getElementById('stats-pg').style.display='block';
try{{const res=await fetch('stats.json');const stats=await res.json();document.getElementById('last-up').innerText=new Date(stats.last_updated).toLocaleString('ar-SA');const ctx=document.getElementById('chart').getContext('2d');if(chartInst)chartInst.destroy();const labels=Object.keys(stats.by_protocol).map(p=>p.toUpperCase());chartInst=new Chart(ctx,{{type:'doughnut',data:{{labels,datasets:[{{data:Object.values(stats.by_protocol),backgroundColor:labels.map(l=>colors[l.toLowerCase()]||'#8b5cf6'),borderWidth:3}}]}},options:{{responsive:true,plugins:{{legend:{{position:'bottom',labels:{{padding:16,font:{{family:'Cairo',size:13}}}}}}}}}}}});}}catch(e){{}}}});
render('all');
</script></body></html>"""


# ==================== الدالة الرئيسية ====================
def main() -> None:
    print("🚀 DOKA PRO - Exclave Ultimate ✨")
    print("=" * 50)

    all_servers: list[dict] = []
    src_counts: dict[str, int] = {}

    for src_name, url in SOURCES.items():
        html = fetch_page(url, src_name)
        if not html: continue
        links = extract_links(html, src_name)
        src_counts[src_name] = len(links)
        all_servers.extend(build_servers(links, src_name))
        print(f"   ✅ {src_name}: {len(links)}")

    # إزالة التكرار
    seen_urls = set()
    unique_servers = []
    for s in all_servers:
        if s["url"] not in seen_urls:
            seen_urls.add(s["url"])
            unique_servers.append(s)
    all_servers = unique_servers

    if not all_servers:
        print("⚠️ لا توجد سيرفرات!")
        return

    print(f"\n📊 إجمالي فريد: {len(all_servers)}")

    # إحصائيات
    proto_counts: dict[str, int] = {}
    for s in all_servers:
        p = s["proto"].lower()
        proto_counts[p] = proto_counts.get(p, 0) + 1
    print("📋 البروتوكولات:")
    for proto, cnt in sorted(proto_counts.items()):
        print(f"   • {proto.upper()}: {cnt}")

    # ✅ فحص حقيقي
    all_servers = measure_pings(all_servers)

    total = len(all_servers)
    html = gen_html(all_servers, total, src_counts)
    OUTPUT_FILE.write_text(html, encoding="utf-8")

    alive = sum(1 for s in all_servers if s["alive"])
    print(f"\n🎉 تم! {total} سيرفر ({alive} حي)")
    print(f"   ✨ ليلي/نهاري - PWA جاهز")


if __name__ == "__main__":
    main()
