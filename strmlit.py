import streamlit as st
from datetime import datetime, timedelta
from gmail.gmail_auth import gmail_login
from gmail.get_email_list import get
from ollama import chat
import json

# --- Fungsi Waktu ---
def get_current_time():
    return datetime.now()

# --- Streamlit Layout ---
st.set_page_config(page_title="AI Email Assistant", page_icon="📧")
st.title("📧 AI Email Summarizer dengan Ollama + Gmail API")

# Input minggu dari user
minggu = st.number_input("Masukkan berapa minggu mau diungkit:", min_value=1, step=1)

# Tombol jalankan
if st.button("🔍 Ambil dan Ringkas Email"):
    with st.spinner("Mengambil data email dari Gmail..."):
        now = get_current_time()
        hari = minggu * 7
        tanggal_mundur = now - timedelta(days=hari)
        after_str = tanggal_mundur.strftime('%Y/%m/%d')

        st.write(f"📅 Rentang waktu: {tanggal_mundur.strftime('%A, %d %B %Y')} - {now.strftime('%A, %d %B %Y')}")

        # Login Gmail
        gmail_login()

        # Ambil email
        emails = get(after_str)
        st.success(f"✅ Ditemukan {len(emails)} email dalam {hari} hari terakhir.")

        # Simpan ke file JSON
        with open("emails_snippet.json", "w", encoding="utf-8") as f:
            json.dump(emails, f, ensure_ascii=False, indent=4)

        # Jika tidak ada email
        if len(emails) == 0:
            st.warning("Tidak ada email yang ditemukan dalam rentang waktu tersebut.")
        else:
            # --- AI Summarization ---
            system_prompt = f"""
Kamu adalah asisten AI yang bertugas membantu pengguna untuk membaca dan meringkas email.

Konteks:
- Jumlah email yang ditemukan: {len(emails)}.
- Data email sudah tersedia dalam variabel `emails` = {emails}.
- Setiap elemen `emails` berisi informasi seperti pengirim dan cuplikan isi.

Instruksi:
1. Jawablah pertanyaan pengguna berdasarkan data email yang diberikan.
2. Jika pengguna menanyakan "berapa" atau "berapa banyak", sebutkan jumlah email yang ditemukan dengan format alami.
3. Jika diminta "dari siapa", sebutkan nama atau alamat pengirim secara ringkas.
4. Jangan menebak data di luar yang diberikan — hanya gunakan informasi dalam variabel `emails`.
5. Gunakan bahasa yang sopan dan mudah dibaca.
6. Jika tidak ada email ditemukan, jawab dengan jelas.
"""

            st.info("💬 Meminta AI untuk meringkas isi email...")

            full_response = ""
            response = chat(
                model='llama3.2:3b',
                messages=[
                    {'role': 'system', 'content': system_prompt},
                    {'role': 'user', 'content': f'Ada berapa email saya dalam {hari} hari terakhir? Tolong ringkas cuplikannya.'}
                ],
                stream=True
            )

            message_placeholder = st.empty()
            for chunk in response:
                content = chunk["message"]["content"]
                full_response += content
                message_placeholder.markdown(full_response + "▌")

            message_placeholder.markdown(full_response)
            st.success("🎯 Ringkasan selesai!")

