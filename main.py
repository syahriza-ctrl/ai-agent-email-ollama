from datetime import datetime, timedelta
from gmail.gmail_auth import gmail_login
from gmail.get_email_list import get
from ollama import chat
import json

def get_current_time():
    return datetime.now()

def many_weeks():
    while True:
        minggu = input("Masukkan berapa minggu mau diungkit?: ")
    
        try:
            minggu = int(minggu)
            print (f"User memasukan {minggu} minggu.")

            hari = minggu * 7
            return hari
    
        except ValueError:
            print("Input tidak valid, harus angka")

def main():
    now = get_current_time()
    print (now.strftime('%A, %d %B %Y'))

    hari = int(many_weeks())
    print(f"Jadi {hari} hari")

    tanggal_mundur = now - timedelta(days=hari)
    after_str = tanggal_mundur.strftime('%Y/%m/%d')
    print(f"Yang mau diambil: {tanggal_mundur.strftime('%A, %d %B %Y')}")

    gmail_login()
     # ambil email dari Gmail API
    emails = get(after_str)
    print(f"Ditemukan {len(emails)} email.")

    # simpan semua email ke file JSON
    with open("emails_snippet.json", "w", encoding="utf-8") as f:
        json.dump(emails, f, ensure_ascii=False, indent=4)

    print("Semua pesan berhasil disimpan ke emails_snippet.json")

    # AI
    system_prompt = f"""
Kamu adalah asisten AI yang bertugas membantu pengguna untuk membaca dan meringkas email.

Konteks:
- Jumlah email yang ditemukan: {len(emails)}.
- Data email sudah tersedia dalam variabel `emails` = {emails}.
- Setiap elemen `emails` berisi informasi seperti pengirim dan cuplikan isi.

Instruksi:
1. Jawablah pertanyaan pengguna berdasarkan data email yang diberikan.
2. Jika pengguna menanyakan "berapa" atau "berapa banyak", sebutkan jumlah email yang ditemukan dengan format yang alami.
   Contoh: "Saya menemukan {len(emails)} email minggu lalu."
3. Jika diminta "dari siapa", sebutkan nama atau alamat pengirim secara ringkas, misalnya:
   "Email tersebut dikirim oleh: [nama atau alamat pengirim]."
4. Jangan menebak data di luar yang diberikan — hanya gunakan informasi dalam variabel `emails`.
5. Gunakan bahasa yang sopan, ringkas, dan mudah dibaca.
6. Jika tidak ada email ditemukan, jawab dengan jelas:
   "Tidak ada email yang ditemukan dalam rentang waktu tersebut."

Tujuan:
Memberikan jawaban informatif, singkat, dan langsung berdasarkan data email pengguna.
"""


    stream = chat(
        model = 'llama3.2:3b',
        messages = [{
            'role' : 'system',
            'content' : system_prompt
        },
        {
            'role' : 'user',
            'content' : f'Hi AI ada berapa email saya dalam {hari} hari?. Tolong summarize isi dari cuplikan emailnya terkait apa?'
        }],
        stream = True)

    for chunk in stream:
        print(chunk['message']['content'], end='', flush=True)
 
if __name__== "__main__":
    main()