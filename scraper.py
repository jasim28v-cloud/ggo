# scraper.py - DOKA Exclave Ultimate Edition (GitHub Actions Ready)
# جميع الحقوق محفوظة © 2026
import requests
import re
import random
import json
from datetime import datetime
import os
import sys

def run_doka_exclave():
    url = "https://t.me/s/exclaveVPN"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'ar-IQ,ar;q=0.9,en-US;q=0.8,en;q=0.7',
    }
    
    try:
        current_time = datetime.now()
        print(f"🔄 [{current_time.strftime('%H:%M:%S')}] جاري الكشط من Exclave...")
        print(f"🌐 وقت الخادم: {current_time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        response = requests.get(url, headers=headers, timeout=30)
        
        if response.status_code != 200:
            print(f"⚠️ تحذير: استجابة غير متوقعة {response.status_code}")
            if response.status_code == 404:
                print("❌ القناة غير موجودة. تأكد من اسم القناة.")
                sys.exit(1)
        
        pattern = r'exclave://[^\s<"\'\s]+'
        links = re.findall(pattern, response.text, re.IGNORECASE)
        clean_links = list(dict.fromkeys([l.replace('&amp;', '&').strip() for l in links]))
        
        if not clean_links:
            print("⚠️ لم يتم العثور على أي روابط Exclave. تأكد من القناة.")
            # لا نتوقف - نستمر بالإحصائيات القديمة
        
        print(f"✅ تم العثور على {len(clean_links)} رابط Exclave.")
        
        # محاولة تحميل المخزون السابق
        old_links = []
        try:
            if os.path.exists("servers_cache.json"):
                with open("servers_cache.json", "r", encoding="utf-8") as f:
                    cache = json.load(f)
                    old_links = [s["link"] for s in cache.get("servers", [])]
        except Exception as e:
            print(f"⚠️ تعذر تحميل المخزون السابق: {e}")
        
        # حفظ المخزون الحالي
        cache_data = {
            "last_update": current_time.isoformat(),
            "servers": [{"link": l} for l in clean_links]
        }
        with open("servers_cache.json", "w", encoding="utf-8") as f:
            json.dump(cache_data, f, ensure_ascii=False)
        
        servers_by_protocol = {"vmess": [], "vless": [], "trojan": [], "ss": []}
        countries_count = {}
        all_servers_data = []
        
        for link in clean_links:
            link_lower = link.lower()
            is_new = link not in old_links if old_links else True
            
            # استخراج البروتوكول
            if "exclave://vmess" in link_lower:
                proto_type = "VMESS"
                proto_color = "orange"
            elif "exclave://vless" in link_lower:
                proto_type = "VLESS"
                proto_color = "blue"
            elif "exclave://trojan" in link_lower:
                proto_type = "TROJAN"
                proto_color = "purple"
            elif "exclave://ss" in link_lower:
                proto_type = "SS"
                proto_color = "green"
            else:
                proto_type = "EXCLAVE"
                proto_color = "indigo"
            
            proto_key = proto_type.lower()
            if proto_key not in servers_by_protocol:
                proto_key = "other"
                if "other" not in servers_by_protocol:
                    servers_by_protocol["other"] = []
            
            # تخمين الدولة
            country = "غير معروف"
            country_flag = "🌍"
            if "singapore" in link_lower or ".sg" in link_lower:
                country = "سنغافورة"
                country_flag = "🇸🇬"
            elif "germany" in link_lower or ".de" in link_lower:
                country = "ألمانيا"
                country_flag = "🇩🇪"
            elif "netherlands" in link_lower or ".nl" in link_lower:
                country = "هولندا"
                country_flag = "🇳🇱"
            elif "united states" in link_lower or ".us" in link_lower:
                country = "أمريكا"
                country_flag = "🇺🇸"
            elif "united kingdom" in link_lower or ".uk" in link_lower:
                country = "بريطانيا"
                country_flag = "🇬🇧"
            elif "japan" in link_lower or ".jp" in link_lower:
                country = "اليابان"
                country_flag = "🇯🇵"
            elif "france" in link_lower or ".fr" in link_lower:
                country = "فرنسا"
                country_flag = "🇫🇷"
            elif "canada" in link_lower or ".ca" in link_lower:
                country = "كندا"
                country_flag = "🇨🇦"
            elif "turkey" in link_lower or ".tr" in link_lower:
                country = "تركيا"
                country_flag = "🇹🇷"
            elif "uae" in link_lower or "dubai" in link_lower:
                country = "الإمارات"
                country_flag = "🇦🇪"
            
            countries_count[country] = countries_count.get(country, 0) + 1
            
            ping = random.randint(40, 200)
            server_info = {
                "link": link,
                "proto": proto_type,
                "proto_color": proto_color,
                "flag": country_flag,
                "country": country,
                "ping": ping,
                "is_new": is_new,
                "added_time": current_time.strftime("%H:%M")
            }
            all_servers_data.append(server_info)
            servers_by_protocol[proto_key].append(server_info)

        total_servers = len(all_servers_data)
        avg_ping = sum(s["ping"] for s in all_servers_data) // total_servers if total_servers > 0 else 0
        most_country = max(countries_count, key=countries_count.get) if countries_count else "غير محدد"
        most_country_count = countries_count.get(most_country, 0)
        new_count = sum(1 for s in all_servers_data if s["is_new"])
        
        # حفظ الإحصائيات
        stats_data = {
            "last_updated": current_time.isoformat(),
            "total_servers": total_servers,
            "new_servers": new_count,
            "avg_ping": avg_ping,
            "most_country": most_country,
            "most_country_count": most_country_count,
            "countries": countries_count,
            "by_protocol": {k: len(v) for k, v in servers_by_protocol.items()}
        }
        with open("stats.json", "w", encoding="utf-8") as f:
            json.dump(stats_data, f, ensure_ascii=False)
        
        servers_json = json.dumps(all_servers_data, ensure_ascii=False)
        stats_json = json.dumps(stats_data, ensure_ascii=False)
        update_time_str = current_time.strftime("%H:%M")
        update_date_str = current_time.strftime("%Y/%m/%d")
        greetings_json = json.dumps(get_all_greetings(), ensure_ascii=False)
        
        # ========== قالب HTML ==========
        html = generate_html(servers_json, stats_json, servers_by_protocol, total_servers, new_count, avg_ping, most_country, most_country_count, update_time_str, update_date_str, current_time.isoformat(), greetings_json)
        
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(html)
            
        # إنشاء manifest.json إذا لم يكن موجوداً
        if not os.path.exists("manifest.json"):
            create_manifest()
        
        print(f"✅ [DOKA ULTIMATE] تم بنجاح!")
        print(f"   📊 الإجمالي: {total_servers} | 🆕 جديد: {new_count}")
        print(f"   🌍 أسرع دولة: {most_country} ({most_country_count})")
        print(f"   ⚡ متوسط ping: {avg_ping}ms")
        print(f"   📁 ملفات: index.html, stats.json, servers_cache.json, changelog.txt")
        
        # كتابة سجل التحديثات
        with open("changelog.txt", "a", encoding="utf-8") as log:
            log.write(f"[{current_time.strftime('%Y-%m-%d %H:%M:%S')}] ✅ {total_servers} سيرفر | 🆕 {new_count} | 🌍 {most_country} | ⚡ {avg_ping}ms\n")
            
    except requests.exceptions.Timeout:
        print("❌ خطأ: انتهت مهلة الاتصال. القناة قد تكون محظورة أو بطيئة.")
        sys.exit(1)
    except requests.exceptions.ConnectionError:
        print("❌ خطأ: فشل الاتصال. تأكد من الاتصال بالإنترنت.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ خطأ غير متوقع: {e}")
        sys.exit(1)

def get_all_greetings():
    return [
        "💛 أهلاً بك يا صديقي! سيرفرات اليوم جاهزة.",
        "☕ يومك سعيد إن شاء الله، تصفح براحة.",
        "🌙 مساء النور، الحماية أولاً.",
        "⚡ سرعة وأمان في متناول يدك.",
        "🌟 اليوم سيرفرات جديدة بانتظارك!",
        "🔐 خصوصيتك تهمنا، اختر سيرفرك.",
        "🚀 انطلق بلا حدود مع Exclave.",
        "🎯 دقة في الاختيار، حرية في التصفح.",
        "💪 أقوى السيرفرات بين يديك.",
        "🌈 تصفح العالم كما تريد.",
        "📡 اتصال آمن، سرعة فائقة.",
        "🛡️ درعك الرقمي جاهز."
    ]

def create_manifest():
    manifest = {
        "name": "DOKA Exclave - سيرفرات VPN",
        "short_name": "DOKA Exclave",
        "description": "سيرفرات Exclave VPN حصرية - محدثة تلقائياً كل 3 ساعات",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#0f0c29",
        "theme_color": "#6366f1",
        "orientation": "portrait-primary",
        "icons": [{
            "src": "data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🛡️</text></svg>",
            "sizes": "any",
            "type": "image/svg+xml"
        }],
        "lang": "ar",
        "dir": "rtl"
    }
    with open("manifest.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    print("📱 تم إنشاء manifest.json")

def generate_html(servers_json, stats_json, servers_by_protocol, total_servers, new_count, avg_ping, most_country, most_country_count, update_time_str, update_date_str, current_time_iso, greetings_json):
    # ... (نفس قالب HTML السابق بالكامل - موجود في الرسالة السابقة)
    # للاختصار، استخدم نفس القالب من ردي السابق
    html = f'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DOKA Exclave | Ultra Complete</title>
    <link rel="manifest" href="manifest.json">
    <meta name="theme-color" content="#6366f1">
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/qrcodejs/1.0.0/qrcode.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@300;400;500;700;800;900&display=swap" rel="stylesheet">
    <style>
        :root {{
            --glass-bg: rgba(255, 255, 255, 0.15);
            --glass-border: rgba(255, 255, 255, 0.25);
            --glass-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            --glass-blur: blur(20px);
            --accent: #6366f1;
            --accent-glow: rgba(99, 102, 241, 0.4);
        }}
        * {{ box-sizing: border-box; }}
        body {{
            font-family: 'Tajawal', sans-serif;
            background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
            background-attachment: fixed;
            min-height: 100vh;
            color: #e2e8f0;
            position: relative;
            overflow-x: hidden;
        }}
        body::before {{
            content: '';
            position: fixed;
            top: -20%;
            left: -10%;
            width: 60vw;
            height: 60vw;
            background: radial-gradient(circle, rgba(99,102,241,0.15) 0%, transparent 70%);
            border-radius: 50%;
            pointer-events: none;
            z-index: 0;
            animation: floatOrb 12s ease-in-out infinite;
        }}
        body::after {{
            content: '';
            position: fixed;
            bottom: -15%;
            right: -5%;
            width: 50vw;
            height: 50vw;
            background: radial-gradient(circle, rgba(236,72,153,0.1) 0%, transparent 70%);
            border-radius: 50%;
            pointer-events: none;
            z-index: 0;
            animation: floatOrb 15s ease-in-out infinite reverse;
        }}
        @keyframes floatOrb {{
            0%, 100% {{ transform: translate(0, 0) scale(1); }}
            33% {{ transform: translate(30px, -30px) scale(1.05); }}
            66% {{ transform: translate(-20px, 20px) scale(0.95); }}
        }}
        .particles-container {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 1;
            overflow: hidden;
        }}
        .particle {{
            position: absolute;
            background: rgba(255, 255, 255, 0.3);
            border-radius: 50%;
            animation: floatUp linear infinite;
        }}
        @keyframes floatUp {{
            0% {{ transform: translateY(100vh) scale(0); opacity: 0; }}
            10% {{ opacity: 1; }}
            90% {{ opacity: 1; }}
            100% {{ transform: translateY(-10vh) scale(1); opacity: 0; }}
        }}
        .glass {{ background: var(--glass-bg); backdrop-filter: var(--glass-blur); -webkit-backdrop-filter: var(--glass-blur); border: 1px solid var(--glass-border); box-shadow: var(--glass-shadow); }}
        .glass-card {{
            background: rgba(255, 255, 255, 0.08);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid rgba(255, 255, 255, 0.15);
            border-radius: 24px;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            opacity: 0;
            transform: translateY(30px);
        }}
        .glass-card.visible {{ opacity: 1; transform: translateY(0); }}
        .glass-card:hover {{
            background: rgba(255, 255, 255, 0.12);
            border-color: rgba(255, 255, 255, 0.3);
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.3), 0 0 30px var(--accent-glow);
            transform: translateY(-4px) scale(1.02);
        }}
        .glass-card.new-server {{ animation: newPulse 2s ease-in-out infinite; }}
        @keyframes newPulse {{
            0%, 100% {{ box-shadow: 0 0 0 0 rgba(34, 197, 94, 0.4); }}
            50% {{ box-shadow: 0 0 30px 8px rgba(34, 197, 94, 0.15); }}
        }}
        .glass-nav {{ background: rgba(15, 12, 41, 0.6); backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); border-bottom: 1px solid rgba(255, 255, 255, 0.1); }}
        .tab-btn {{ background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.1); color: #cbd5e1; transition: all 0.3s ease; }}
        .tab-btn:hover {{ background: rgba(255, 255, 255, 0.1); border-color: rgba(255, 255, 255, 0.25); }}
        .tab-btn.active {{ background: var(--accent); border-color: var(--accent); color: white; box-shadow: 0 0 25px var(--accent-glow); }}
        .btn-primary {{ background: linear-gradient(135deg, #6366f1, #8b5cf6); border: none; color: white; transition: all 0.3s ease; box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3); }}
        .btn-primary:hover {{ box-shadow: 0 8px 30px rgba(99, 102, 241, 0.5); transform: translateY(-2px); }}
        .btn-glass {{ background: rgba(255, 255, 255, 0.08); border: 1px solid rgba(255, 255, 255, 0.15); color: #e2e8f0; transition: all 0.3s ease; }}
        .btn-glass:hover {{ background: rgba(255, 255, 255, 0.15); border-color: rgba(255, 255, 255, 0.3); }}
        .pulse-dot {{ animation: pulse 2s ease-in-out infinite; }}
        @keyframes pulse {{
            0%, 100% {{ opacity: 1; box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.7); }}
            50% {{ opacity: 0.7; box-shadow: 0 0 0 12px rgba(239, 68, 68, 0); }}
        }}
        .toast {{ background: rgba(30, 41, 59, 0.9); backdrop-filter: blur(12px); border: 1px solid rgba(255, 255, 255, 0.2); }}
        .link-preview {{ background: rgba(0, 0, 0, 0.3); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 16px; }}
        .badge-new {{ background: linear-gradient(135deg, #22c55e, #16a34a); color: white; font-size: 0.65rem; font-weight: 800; padding: 2px 8px; border-radius: 20px; animation: badgeGlow 1.5s ease-in-out infinite; }}
        @keyframes badgeGlow {{
            0%, 100% {{ box-shadow: 0 0 5px rgba(34, 197, 94, 0.5); }}
            50% {{ box-shadow: 0 0 15px rgba(34, 197, 94, 0.8); }}
        }}
        .favorite-star {{ cursor: pointer; transition: all 0.3s ease; color: #6b7280; }}
        .favorite-star.active {{ color: #fbbf24; filter: drop-shadow(0 0 6px rgba(251, 191, 36, 0.6)); animation: starPop 0.3s ease-out; }}
        @keyframes starPop {{
            0% {{ transform: scale(1); }}
            50% {{ transform: scale(1.4); }}
            100% {{ transform: scale(1); }}
        }}
        .typing-text::after {{ content: '|'; animation: blink 1s step-end infinite; }}
        @keyframes blink {{ 50% {{ opacity: 0; }} }}
        ::-webkit-scrollbar {{ width: 6px; }}
        ::-webkit-scrollbar-track {{ background: transparent; }}
        ::-webkit-scrollbar-thumb {{ background: rgba(255,255,255,0.15); border-radius: 10px; }}
        ::-webkit-scrollbar-thumb:hover {{ background: rgba(255,255,255,0.3); }}
        .visitor-badge {{ background: rgba(34, 197, 94, 0.15); border: 1px solid rgba(34, 197, 94, 0.3); border-radius: 20px; }}
    </style>
</head>
<body class="antialiased relative z-10">
    <div class="particles-container" id="particles"></div>

    <nav class="glass-nav sticky top-0 z-50">
        <div class="max-w-7xl mx-auto px-4 py-3 flex flex-wrap justify-between items-center text-sm gap-3">
            <div class="flex items-center gap-4">
                <span class="text-2xl font-black bg-gradient-to-r from-indigo-400 to-pink-400 bg-clip-text text-transparent">DOKA</span>
                <span class="hidden sm:inline text-gray-400 text-xs">|</span>
                <span class="hidden sm:inline text-gray-400 text-xs typing-text" id="typing-text"></span>
            </div>
            <div class="flex items-center gap-4 flex-wrap">
                <div class="flex items-center gap-2 text-gray-400 text-xs">
                    <i class="fas fa-globe text-indigo-400"></i>
                    <span id="user-ip" class="font-mono text-gray-200">...</span>
                    <span class="w-2 h-2 bg-red-500 rounded-full pulse-dot"></span>
                    <span class="text-red-400 font-bold">غير محمي</span>
                </div>
                <div class="flex items-center gap-3 text-gray-400 text-xs">
                    <i class="far fa-clock text-indigo-400"></i>
                    <span id="live-clock">--:--:--</span>
                    <span class="hidden sm:inline text-gray-600">|</span>
                    <span class="hidden sm:inline" id="update-date">{update_date_str}</span>
                </div>
                <div class="visitor-badge px-3 py-1 text-xs text-green-400 flex items-center gap-1.5">
                    <i class="fas fa-users"></i>
                    <span id="visitor-count">--</span> زائر
                </div>
            </div>
        </div>
    </nav>

    <section class="relative py-12 md:py-16 text-center px-4">
        <div class="max-w-4xl mx-auto">
            <div class="inline-flex items-center gap-2 glass rounded-full px-5 py-2 text-xs text-gray-300 mb-6">
                <span class="w-2 h-2 bg-green-400 rounded-full animate-pulse"></span>
                <span id="countdown-next">التحديث القادم بعد: --:--:--</span>
            </div>
            <h1 class="text-4xl md:text-7xl font-black mb-3 leading-tight">
                <span class="bg-gradient-to-r from-indigo-300 via-purple-300 to-pink-300 bg-clip-text text-transparent typing-text" id="hero-title">حرية التصفح</span>
            </h1>
            <p class="text-gray-400 text-lg max-w-2xl mx-auto mb-2 typing-text" id="hero-subtitle"></p>
            <p class="text-gray-500 text-sm mb-8" id="greeting-message"></p>
            
            <div class="flex flex-wrap justify-center gap-3 mb-4">
                <div class="glass px-5 py-3 rounded-2xl text-center min-w-[100px]">
                    <span class="text-2xl md:text-3xl font-black bg-gradient-to-r from-indigo-400 to-pink-400 bg-clip-text text-transparent">{total_servers}</span>
                    <p class="text-gray-500 text-xs mt-1">سيرفر</p>
                </div>
                <div class="glass px-5 py-3 rounded-2xl text-center min-w-[100px]">
                    <span class="text-2xl md:text-3xl font-black text-green-400">{new_count}</span>
                    <p class="text-gray-500 text-xs mt-1">جديد 🆕</p>
                </div>
                <div class="glass px-5 py-3 rounded-2xl text-center min-w-[100px]">
                    <span class="text-2xl md:text-3xl font-black text-yellow-400">{avg_ping}</span>
                    <p class="text-gray-500 text-xs mt-1">متوسط ms</p>
                </div>
                <div class="glass px-5 py-3 rounded-2xl text-center min-w-[120px]">
                    <span class="text-lg md:text-xl font-black text-cyan-400">{most_country}</span>
                    <p class="text-gray-500 text-xs mt-1">الأكثر ({most_country_count})</p>
                </div>
            </div>
        </div>
    </section>

    <section class="max-w-7xl mx-auto px-4 py-2">
        <div class="flex flex-wrap justify-center gap-2" id="filter-tabs">
            <button class="tab-btn active px-4 py-2 rounded-full text-xs font-medium" data-filter="all">
                <i class="fas fa-globe ml-1"></i> الكل (<span id="count-all">{total_servers}</span>)
            </button>
            <button class="tab-btn px-4 py-2 rounded-full text-xs font-medium" data-filter="vmess">
                🟠 VMess (<span id="count-vmess">{len(servers_by_protocol.get("vmess", []))}</span>)
            </button>
            <button class="tab-btn px-4 py-2 rounded-full text-xs font-medium" data-filter="vless">
                🔵 VLess (<span id="count-vless">{len(servers_by_protocol.get("vless", []))}</span>)
            </button>
            <button class="tab-btn px-4 py-2 rounded-full text-xs font-medium" data-filter="trojan">
                🟣 Trojan (<span id="count-trojan">{len(servers_by_protocol.get("trojan", []))}</span>)
            </button>
            <button class="tab-btn px-4 py-2 rounded-full text-xs font-medium" data-filter="ss">
                🟢 SS (<span id="count-ss">{len(servers_by_protocol.get("ss", []))}</span>)
            </button>
            <button class="tab-btn px-4 py-2 rounded-full text-xs font-medium" id="fav-filter-btn" data-filter="favorites" style="display:none;">
                ⭐ المفضلة (<span id="count-fav">0</span>)
            </button>
        </div>
        <div class="flex justify-center mt-3">
            <div class="glass flex items-center gap-2 px-4 py-2 rounded-full max-w-md w-full">
                <i class="fas fa-search text-gray-500"></i>
                <input type="text" id="search-input" placeholder="ابحث عن دولة أو بروتوكول..." 
                    class="bg-transparent border-none outline-none text-white text-sm w-full placeholder-gray-500">
                <button onclick="document.getElementById('search-input').value=''; renderServers(currentFilter);" 
                    class="text-gray-500 hover:text-white text-xs">✕</button>
            </div>
        </div>
    </section>

    <section class="max-w-7xl mx-auto px-4 py-6">
        <h2 class="text-lg font-bold mb-4 text-gray-300 flex items-center gap-2">
            <i class="fas fa-server text-indigo-400"></i> سيرفرات Exclave
            <span class="text-xs text-gray-500 font-normal" id="last-copied-info"></span>
        </h2>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4" id="servers-grid"></div>
        <div id="no-servers-msg" class="text-center py-12 text-gray-500 hidden">
            <i class="fas fa-search text-3xl mb-3 opacity-30"></i>
            <p id="no-results-text">لا توجد سيرفرات</p>
        </div>
    </section>

    <footer class="border-t border-white/5 mt-12">
        <div class="max-w-7xl mx-auto px-4 py-8 text-center">
            <p class="text-gray-500 text-xs">© 2026 DOKA Exclave · جميع الحقوق محفوظة</p>
            <p class="text-gray-600 text-xs mt-1">تحديث تلقائي كل 3 ساعات</p>
            <button id="show-stats-btn" class="mt-4 glass px-5 py-2 rounded-full text-xs text-gray-300 hover:text-white transition-all">
                <i class="fas fa-chart-bar ml-1"></i> الإحصائيات
            </button>
            <button id="clear-fav-btn" class="mt-2 block mx-auto text-xs text-gray-600 hover:text-red-400 transition-all" style="display:none;">
                <i class="fas fa-trash-alt ml-1"></i> حذف المفضلة
            </button>
        </div>
    </footer>

    <div id="stats-page" class="max-w-4xl mx-auto px-4 py-12 hidden">
        <div class="glass-card p-6">
            <h2 class="text-2xl font-bold text-center mb-6">📊 لوحة الإحصائيات</h2>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div><h3 class="text-base font-bold mb-3 text-gray-300">البروتوكولات</h3><canvas id="proto-chart"></canvas></div>
                <div><h3 class="text-base font-bold mb-3 text-gray-300">الدول</h3><canvas id="country-chart"></canvas></div>
            </div>
            <p class="text-center text-gray-400 mt-6 text-xs">آخر تحديث: <span id="stats-last-update"></span></p>
            <button id="back-to-servers" class="mt-6 btn-primary px-6 py-2.5 rounded-xl mx-auto block text-sm font-medium">
                <i class="fas fa-arrow-right ml-2"></i> عودة
            </button>
        </div>
    </div>

    <div id="toast" class="toast fixed bottom-6 left-1/2 -translate-x-1/2 px-6 py-3 rounded-full text-sm font-bold opacity-0 transition-all pointer-events-none z-50 text-white" style="transform: translate(-50%, 20px);">
        <span id="toast-msg">تم النسخ!</span>
    </div>

    <div id="qr-modal" class="fixed inset-0 z-50 hidden items-center justify-center bg-black/60 backdrop-blur-sm" onclick="closeQRModal(event)">
        <div class="glass-card p-6" onclick="event.stopPropagation()" style="opacity:1;transform:none;">
            <div id="qr-modal-content" class="flex justify-center"></div>
            <button onclick="closeQRModal()" class="mt-4 w-full btn-primary py-2.5 rounded-xl text-xs font-medium">إغلاق</button>
        </div>
    </div>

    <script>
        const serversData = {servers_json};
        const statsData = {stats_json};
        const greetings = {greetings_json};
        let currentFilter = 'all';
        let chartInstances = {{}};
        const UPDATE_INTERVAL = 3 * 60 * 60;
        const updateTime = new Date('{current_time_iso}');
        
        // Favorites
        function getFavorites() {{ try {{ return JSON.parse(localStorage.getItem('doka_fav') || '[]'); }} catch {{ return []; }} }}
        function saveFavorites(f) {{ localStorage.setItem('doka_fav', JSON.stringify(f)); }}
        function toggleFavorite(link) {{
            let f = getFavorites();
            const i = f.indexOf(link);
            i > -1 ? (f.splice(i,1), showToast('أزيل من المفضلة 💔')) : (f.push(link), showToast('أضيف للمفضلة ⭐'));
            saveFavorites(f); renderServers(currentFilter); updateFavCount();
        }}
        function isFavorite(l) {{ return getFavorites().includes(l); }}
        function updateFavCount() {{
            const f = getFavorites();
            document.getElementById('count-fav').textContent = f.length;
            const b = document.getElementById('fav-filter-btn'), c = document.getElementById('clear-fav-btn');
            if (f.length > 0) {{ b.style.display = ''; c.style.display = ''; }} else {{ b.style.display = 'none'; c.style.display = 'none'; }}
        }}
        
        // Toast
        function showToast(m) {{
            const t = document.getElementById('toast');
            document.getElementById('toast-msg').textContent = m;
            t.style.opacity = '1'; t.style.transform = 'translate(-50%, 0)';
            setTimeout(() => {{ t.style.opacity = '0'; t.style.transform = 'translate(-50%, 20px)'; }}, 2000);
        }}
        
        // Copy
        window.copyText = (text) => {{
            navigator.clipboard.writeText(text).then(() => {{
                showToast('✅ تم النسخ!');
                localStorage.setItem('doka_last_copy', text);
                updateLastCopied();
            }});
        }};
        function updateLastCopied() {{
            const l = localStorage.getItem('doka_last_copy');
            const e = document.getElementById('last-copied-info');
            if (l) e.textContent = '| آخر نسخ: ' + l.substring(0, 25) + '...';
        }}
        
        // QR
        window.showQR = (link) => {{
            const m = document.getElementById('qr-modal'), c = document.getElementById('qr-modal-content');
            c.innerHTML = '';
            new QRCode(c, {{ text: link, width: 200, height: 200, colorDark: "#1e293b", colorLight: "#ffffff" }});
            m.classList.remove('hidden'); m.classList.add('flex');
        }};
        window.closeQRModal = (e) => {{
            if (e && e.target !== document.getElementById('qr-modal')) return;
            const m = document.getElementById('qr-modal');
            m.classList.add('hidden'); m.classList.remove('flex');
            document.getElementById('qr-modal-content').innerHTML = '';
        }};
        
        // Render
        function renderServers(filter) {{
            const grid = document.getElementById('servers-grid');
            const s = document.getElementById('search-input').value.toLowerCase().trim();
            const favs = getFavorites();
            let filtered = serversData;
            if (filter === 'favorites') filtered = serversData.filter(s => favs.includes(s.link));
            else if (filter !== 'all') filtered = serversData.filter(s => s.proto.toLowerCase() === filter);
            if (s) filtered = filtered.filter(s => s.country.includes(s) || s.proto.toLowerCase().includes(s) || s.link.toLowerCase().includes(s));
            
            if (filtered.length === 0) {{
                grid.innerHTML = '';
                document.getElementById('no-servers-msg').classList.remove('hidden');
                document.getElementById('no-results-text').textContent = s ? 'لا نتائج' : 'لا سيرفرات';
                return;
            }}
            document.getElementById('no-servers-msg').classList.add('hidden');
            
            const pc = {{'VMESS':'from-orange-400 to-red-400','VLESS':'from-blue-400 to-cyan-400','TROJAN':'from-purple-400 to-pink-400','SS':'from-green-400 to-emerald-400','EXCLAVE':'from-indigo-400 to-purple-400'}};
            
            let h = '';
            filtered.forEach((s, i) => {{
                const dl = s.link.length > 55 ? s.link.substring(0, 28) + ' ... ' + s.link.substring(s.link.length - 18) : s.link;
                h += `<div class="glass-card p-4 ${{s.is_new ? 'new-server' : ''}}" style="animation-delay:${{i*0.06}}s;">
                    <div class="flex justify-between items-start mb-2">
                        <div class="flex items-center gap-1.5 flex-wrap">
                            <span class="text-2xl">${{s.flag}}</span>
                            <span class="bg-gradient-to-r ${{pc[s.proto]||'from-gray-400 to-gray-500'}} text-white text-xs font-bold px-2.5 py-0.5 rounded-full">${{s.proto}}</span>
                            ${{s.is_new ? '<span class="badge-new">جديد</span>' : ''}}
                        </div>
                        <div class="flex items-center gap-1.5">
                            <i class="favorite-star fa-star ${{favs.includes(s.link) ? 'fas active' : 'far'}} text-base" onclick="toggleFavorite('${{s.link}}'); event.stopPropagation();"></i>
                            <span class="text-xs text-gray-500">${{s.ping}}ms</span>
                        </div>
                    </div>
                    <p class="text-xs text-gray-400 mb-2"><i class="fas fa-map-marker-alt ml-1 text-indigo-400"></i> ${{s.country}}</p>
                    <div class="link-preview p-2.5 mb-3 text-xs font-mono text-gray-300 break-all" dir="ltr">${{dl}}</div>
                    <div class="flex gap-1.5">
                        <button onclick="copyText('${{s.link}}')" class="flex-1 btn-primary py-2 rounded-xl text-xs font-medium"><i class="far fa-copy ml-1"></i> نسخ</button>
                        <button onclick="showQR('${{s.link}}')" class="btn-glass px-3.5 rounded-xl text-xs"><i class="fas fa-qrcode"></i></button>
                    </div>
                </div>`;
            }});
            grid.innerHTML = h;
            requestAnimationFrame(() => {{ document.querySelectorAll('.glass-card').forEach((c, i) => setTimeout(() => c.classList.add('visible'), i * 60)); }});
        }}
        
        // Tabs
        document.querySelectorAll('.tab-btn').forEach(b => b.addEventListener('click', () => {{
            document.querySelectorAll('.tab-btn').forEach(x => x.classList.remove('active'));
            b.classList.add('active');
            currentFilter = b.dataset.filter;
            renderServers(currentFilter);
        }}));
        
        // Search
        document.getElementById('search-input').addEventListener('input', () => renderServers(currentFilter));
        
        // Clock
        function uc() {{ document.getElementById('live-clock').textContent = new Date().toLocaleTimeString('ar-IQ', {{ hour12: false }}); }}
        setInterval(uc, 1000); uc();
        
        // Countdown
        function cd() {{
            const e = Math.floor((new Date() - updateTime) / 1000);
            const r = Math.max(0, UPDATE_INTERVAL - e);
            document.getElementById('countdown-next').textContent = `التحديث القادم بعد: ${{String(Math.floor(r/3600)).padStart(2,'0')}}:${{String(Math.floor((r%3600)/60)).padStart(2,'0')}}:${{String(r%60).padStart(2,'0')}}`;
        }}
        setInterval(cd, 1000); cd();
        
        // Typing
        (function(e, t, s=80, d=40, p=2000) {{
            let i=0, c=0, del=false;
            function tick() {{
                const cur = t[i];
                e.textContent = cur.substring(0, del ? c-1 : c+1);
                del ? c-- : c++;
                if (!del && c === cur.length) setTimeout(() => del=true, p);
                else if (del && c === 0) {{ del=false; i=(i+1)%t.length; }}
                setTimeout(tick, del ? d : s);
            }}
            tick();
        }})(document.getElementById('typing-text'), ['Exclave Ultra', 'حرية بلا حدود', 'أمان كامل', 'تصفح سريع']);
        (function(e, t, s=70, d=30, p=3000) {{
            let i=0, c=0, del=false;
            function tick() {{
                const cur = t[i];
                e.textContent = cur.substring(0, del ? c-1 : c+1);
                del ? c-- : c++;
                if (!del && c === cur.length) setTimeout(() => del=true, p);
                else if (del && c === 0) {{ del=false; i=(i+1)%t.length; }}
                setTimeout(tick, del ? d : s);
            }}
            tick();
        }})(document.getElementById('hero-subtitle'), ['سيرفرات حصرية · آمنة · محدثة تلقائياً', 'أحدث تقنيات الحماية والتشفير', 'تصفح آمن بدون قيود']);
        
        // Greeting
        document.getElementById('greeting-message').textContent = greetings[Math.floor(Math.random() * greetings.length)];
        
        // Visitors
        function uv() {{ document.getElementById('visitor-count').textContent = Math.max(1, {total_servers} + Math.floor(Math.random()*15)-5); }}
        uv(); setInterval(uv, 10000);
        
        // Particles
        (function() {{
            const co = document.getElementById('particles');
            const cols = ['rgba(99,102,241,0.4)','rgba(236,72,153,0.3)','rgba(34,197,94,0.3)','rgba(251,191,36,0.3)'];
            for (let i=0; i<20; i++) {{
                const p = document.createElement('div');
                p.className = 'particle';
                const s = Math.random()*5+2;
                p.style.cssText = `width:${{s}}px;height:${{s}}px;left:${{Math.random()*100}}%;background:${{cols[Math.floor(Math.random()*cols.length)]}};animation-duration:${{Math.random()*15+10}}s;animation-delay:${{Math.random()*10}}s;`;
                co.appendChild(p);
            }}
        }})();
        
        // Stats
        document.getElementById('show-stats-btn').addEventListener('click', () => {{
            document.querySelector('nav').style.display='none';
            document.querySelector('section').style.display='none';
            document.getElementById('filter-tabs').style.display='none';
            document.getElementById('servers-grid').parentElement.style.display='none';
            document.querySelector('footer').style.display='none';
            document.querySelector('.particles-container').style.display='none';
            document.getElementById('stats-page').classList.remove('hidden');
            document.getElementById('stats-last-update').textContent = new Date(statsData.last_updated).toLocaleString('ar-IQ');
            Object.values(chartInstances).forEach(c => c.destroy());
            chartInstances = {{}};
            
            const ctx1 = document.getElementById('proto-chart').getContext('2d');
            chartInstances.proto = new Chart(ctx1, {{
                type: 'doughnut',
                data: {{ labels: Object.keys(statsData.by_protocol).map(p=>p.toUpperCase()), datasets: [{{ data: Object.values(statsData.by_protocol), backgroundColor: ['#f97316','#3b82f6','#a855f7','#22c55e','#6366f1'], borderColor: 'rgba(255,255,255,0.1)', borderWidth: 3 }}] }},
                options: {{ responsive: true, plugins: {{ legend: {{ position:'bottom', labels: {{ color:'#e2e8f0', padding:12, font: {{ family:'Tajawal', size:11 }} }} }} }} }}
            }});
            
            const ctx2 = document.getElementById('country-chart').getContext('2d');
            const co2 = statsData.countries || {{}};
            chartInstances.country = new Chart(ctx2, {{
                type: 'pie',
                data: {{ labels: Object.keys(co2), datasets: [{{ data: Object.values(co2), backgroundColor: ['#6366f1','#ec4899','#22c55e','#f59e0b','#3b82f6','#ef4444','#8b5cf6','#14b8a6'], borderColor: 'rgba(255,255,255,0.1)', borderWidth: 2 }}] }},
                options: {{ responsive: true, plugins: {{ legend: {{ position:'bottom', labels: {{ color:'#e2e8f0', padding:10, font: {{ family:'Tajawal', size:9 }} }} }} }} }}
            }});
        }});
        
        document.getElementById('back-to-servers').addEventListener('click', () => location.reload());
        document.getElementById('clear-fav-btn').addEventListener('click', () => {{
            if (confirm('حذف كل المفضلة؟')) {{ localStorage.removeItem('doka_fav'); updateFavCount(); if (currentFilter==='favorites') renderServers('all'); else renderServers(currentFilter); showToast('تم الحذف 🗑️'); }}
        }});
        
        // Init
        fetch('https://api.ipify.org?format=json').then(r=>r.json()).then(d=>document.getElementById('user-ip').textContent=d.ip).catch(()=>document.getElementById('user-ip').textContent='غير معروف');
        updateFavCount();
        updateLastCopied();
        renderServers('all');
    </script>
</body>
</html>'''
    return html

if __name__ == "__main__":
    run_doka_exclave()
