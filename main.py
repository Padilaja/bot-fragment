import openai
import requests
import json
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
import re
import time
import os
import threading
from flask import Flask
import sys

# =====================================================================
# ⚙️ SERVER WEB MINI (Agar Bisa Gratis di Render Web Service)
# =====================================================================
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot Fragment Pemburu Aktif & Berjalan di Latar Belakang!", 200

# =====================================================================
# 🔑 KONFIGURASI KUNCI AKSES
# =====================================================================
BLUEMINDS_BASE_URL = os.environ.get("BLUEMINDS_BASE_URL", "https://api.blueminds.ai/v1")
BLUEMINDS_API_KEY = os.environ.get("BLUEMINDS_API_KEY", "sk-ddCqqRZW0lEkTNd0kjG5erjX4YHAP5UEkeRKldZ02T05FmqX")

client = openai.OpenAI(api_key=BLUEMINDS_API_KEY, base_url=BLUEMINDS_BASE_URL)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"
}

# Fungsi print khusus agar log langsung keluar ke Render tanpa tertahan buffer
def cetak_log(teks):
    print(teks, flush=True)
    sys.stdout.flush()

def dapatkan_topik_viral_dan_data_pasar():
    cetak_log("\n📰 Robot sedang melakukan scraping data tren pasar global...")
    try:
        respon = requests.get("https://cointelegraph.com/rss/tag/altcoin", headers=HEADERS, timeout=10)
        titles = re.findall(r'<title><!\[CDATA\[(.*?)\]\]></title>', respon.text)
        berita_gabungan = " ".join(titles[:5]) if titles else "AI, TON Ecosystem, DeFi Layer 2"
    except Exception:
        berita_gabungan = "TON Network expansion, Telegram Mini Apps, AI Automated Agents"
    return f"Narasi viral hari ini: {berita_gabungan}."

def generate_target_usernames():
    prefix = ["ton", "ai", "tele", "dex", "pay", "sol", "tg", "web3", "bot", "nod"]
    suffix = ["vault", "yield", "remit", "stake", "secure", "alpha", "pump", "hub", "node", "labs", "core", "swap"]
    daftar_nama = []
    for p in prefix:
        for s in suffix:
            daftar_nama.append(f"{p}_{s}")
            daftar_nama.append(f"{p}{s}")
    return list(set(daftar_nama))

def cek_ketersediaan_satu_username(username):
    url_cek = f"https://fragment.com/username/{username}"
    try:
        time.sleep(0.3)  # Ditambah sedikit agar tidak terkena blokir cloudflare server
        respon_web = requests.get(url_cek, headers=HEADERS, timeout=7)
        if respon_web.status_code == 200 and ("Available" in respon_web.text or "An auction" in respon_web.text):
            return username, "HIJAU"
        else:
            return username, "MERAH"
    except Exception:
        return username, "ERROR"

def jalankan_super_agent_maksimal():
    tren_pasar = dapatkan_topik_viral_dan_data_pasar()
    kandidat_username = generate_target_usernames()
    total_nama = len(kandidat_username)
    
    cetak_log(f"⚡ Menemukan {total_nama} kombinasi premium dari Kamus Kata Internal.")
    cetak_log("⚡ Mengecek ketersediaan nama secara bersamaan...")
    
    username_kosong_terpilih = []
    
    with ThreadPoolExecutor(max_workers=5) as executor:
        tugas_paralel = {executor.submit(cek_ketersediaan_satu_username, nama): nama for nama in kandidat_username}
        for index, future in enumerate(as_completed(tugas_paralel), start=1):
            try:
                nama, status = future.result()
                if status == "HIJAU":
                    username_kosong_terpilih.append(nama)
                    cetak_log(f"  [{index}/{total_nama}] 🟢 KOSONG: @{nama}")
            except Exception:
                pass

    cetak_log(f"\n🔍 Pemindaian Selesai. Menemukan {len(username_kosong_terpilih)} nama kosong.")
    
    if not username_kosong_terpilih:
        cetak_log("ℹ️ Tidak ada kombinasi yang kosong saat ini. Beres-beres...")
        return

    cetak_log("🧠 Menghubungkan ke Otak AI Blueminds (gpt-5.5) untuk Kurasi Berperingkat Tinggi...")
    prompt_analisis = (
        "Anda adalah sistem AI Senior Data Analyst khusus pasar Fragment Telegram.\n"
        f"Konteks Tren Berita Global Hari Ini: {tren_pasar}\n"
        f"Daftar Username yang VALID KOSONG: {username_kosong_terpilih}\n\n"
        "Tugas Utama: Pilih maksimal 3 username dari daftar kosong di atas yang PALING BERPOTENSI LAKU MAHAL.\n"
        "Berikan output dalam format JSON Array objek murni yang rapi tanpa penjelasan pembuka/penutup:\n"
        '[{"username": "nama", "alasan": "jelaskan faktor fundamentalnya", "audiens": "siapa kelompok yang butuh"}]'
    )
    
    try:
        respon_ai = client.chat.completions.create(
            model="gpt-5.5",
            messages=[{"role": "user", "content": prompt_analisis}]
        )
        teks_jawaban = respon_ai.choices[0].message.content
        
        if "```json" in teks_jawaban:
            teks_jawaban = teks_jawaban.split("```json")[1].split("```")[0].strip()
        elif "```" in teks_jawaban:
            teks_jawaban = teks_jawaban.split("```")[1].split("```")[0].strip()
            
        rekomendasi_final = json.loads(teks_jawaban.strip())
        cetak_log("✅ AI Sukses Merespons dan Memotong Kredit!")
    except Exception as e:
        cetak_log(f"⚠️ Gagal parsing AI ({e}), mengaktifkan mode aman.")
        rekomendasi_final = [{"username": username_kosong_terpilih[0], "alasan": "Struktur utilitas tinggi.", "audiens": "Whale Investor"}]

    keranjang_excel = []
    cetak_log("\n👑 MEMPROSES IDE EMAS PILIHAN AI:")
    for item in rekomendasi_final:
        nama_fix = item.get('username', username_kosong_terpilih[0])
        alasan_fix = item.get('alasan', 'N/A')
        audiens_fix = item.get('audiens', 'N/A')
        
        cetak_log(f"💎 @{nama_fix} -> Lolos Angka Kelayakan Jual!")
        
        keranjang_excel.append({
            "Username": f"@{nama_fix}",
            "Status Kelangkaan": "Tersedia",
            "Analisis Komersial AI": alasan_fix,
            "Estimasi Target Pembeli": audiens_fix,
            "Link Jual Langsung": f"https://fragment.com/username/{nama_fix}"
        })

    df_hasil = pd.DataFrame(keranjang_excel)
    df_hasil.to_excel("Harta_Karun_Fragment_Harian.xlsx", index=False)
    cetak_log("💾 SUKSES! File laporan diperbarui.")

# =====================================================================
# 🔄 LOOP UTAMA AGENT
# =====================================================================
def loop_pemburu_otomatis():
    # Menunggu 10 detik di awal agar server Flask benar-benar siap dan Live
    time.sleep(10)
    cetak_log("🚀 MESIN PEMBURU FRAGMENT OTOMATIS AKTIF DI BACKGROUND...")
    while True:
        try:
            jalankan_super_agent_maksimal()
        except Exception as e:
            cetak_log(f"⚠️ Gangguan: {e}. Mengulang kembali...")
        
        MENIT_JEDA = 5
        cetak_log(f"\n🕒 Tugas selesai. Tidur {MENIT_JEDA} menit...")
        time.sleep(MENIT_JEDA * 60)

if __name__ == "__main__":
    # Menjalankan thread latar belakang
    t = threading.Thread(target=loop_pemburu_otomatis)
    t.daemon = True
    t.start()
    
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
