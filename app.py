import streamlit as st
import os
import sys

st.title("🔍 Mode Debugger: Mencari 'Penyusup'")

# 1. Cek isi file app.py itu sendiri (Apakah ada kode tersembunyi?)
st.subheader("1. Isi File app.py")
try:
    with open(__file__, "r") as f:
        content = f.read()
        if "DB_USERNAME" in content:
            st.error("🚨 DITEMUKAN: Ada kata 'DB_USERNAME' di dalam kode app.py kamu!")
        else:
            st.success("Aman: Tidak ada kata 'DB_USERNAME' di dalam kode app.py.")
except Exception as e:
    st.write(f"Gagal baca file: {e}")

# 2. Cek Environment Variables (Apakah Streamlit maksa cari DB?)
st.subheader("2. Cek Environment Variables")
env_keys = list(os.environ.keys())
db_keys = [k for k in env_keys if "DB" in k or "USER" in k]
if db_keys:
    st.warning(f"Ada variabel lingkungan terkait DB: {db_keys}")
else:
    st.write("Environment bersih dari variabel DB.")

# 3. Cek Streamlit Secrets
st.subheader("3. Cek Streamlit Secrets")
try:
    if st.secrets:
        st.write("Isi Secrets yang terdeteksi:")
        st.json(list(st.secrets.keys()))
    else:
        st.write("Secrets kosong.")
except Exception:
    st.write("Tidak ada file secrets.toml yang terdeteksi.")

# 4. Tes Import Library (Biasanya error muncul pas import)
st.subheader("4. Tes Import Library")
try:
    import google.generativeai as genai
    st.success("Import Google AI: BERHASIL")
except Exception as e:
    st.error(f"Import Google AI: GAGAL ({e})")

st.info("💡 Tolong screenshot hasil dari halaman ini dan kasih tahu aku bagian mana yang warnanya MERAH.")
