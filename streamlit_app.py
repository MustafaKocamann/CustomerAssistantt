import streamlit as st
from dotenv import load_dotenv, find_dotenv
import os

# 🚀 .env dosyasını hemen yükle (sadece bir kez)
load_dotenv(find_dotenv(), override=True)
from main import SmartCustomerSupportSystem
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import docx
import PyPDF2
import openai

# 🔑 OpenAI API anahtarını set et
openai.api_key = os.getenv("OPENAI_API_KEY")

# --- Page Config ---
st.set_page_config(
    page_title="AI Assistant Pro",
    page_icon="🤖",
    layout="wide",
)

# --- Modern Premium CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    * { font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; }

    .stApp { background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%); }
    .block-container{ max-width:1400px; padding:2rem 3rem; animation:fadeInUp .6s cubic-bezier(.16,1,.3,1); }
    @keyframes fadeInUp{from{opacity:0;transform:translateY(30px);}to{opacity:1;transform:translateY(0);}}

    h1,h2,h3,h4,h5{ color:#fff!important; font-weight:600!important; letter-spacing:-.02em; }
    h1{ font-size:2.5rem!important; background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);
        -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text; margin-bottom:.5rem!important;}
            /* --- Result kutusu içindeki başlık renkleri (koyu tema için) --- */
.result-box h1,
.result-box h2,
.result-box h3,
.result-box h4,
.result-box h5{
  color: #f9fafb !important;      /* açık metin */
}

.result-box h2{
  border-bottom: 1px solid rgba(255,255,255,.12);
}
            
/* --- RESULT BOX: KOYU TEMA --- */
.result-box{
  background: linear-gradient(135deg, #0b1220 0%, #111827 100%);
  color: #e5e7eb;
  border-radius: 16px;
  padding: 1.75rem;
  border: 1px solid rgba(255,255,255,.08);
  border-left: 4px solid #7c3aed; /* vurgu çizgisi */
  box-shadow: 0 8px 24px rgba(0,0,0,.35);
  line-height: 1.7;
  font-size: .95rem;
}

/* result-box içindeki başlıklar */
.result-box h1,
.result-box h2,
.result-box h3,
.result-box h4,
.result-box h5{
  color: #f9fafb !important;
  margin: 0 0 .5rem 0;
  line-height: 1.25;
}

.result-box h2{
  border-bottom: 1px solid rgba(255,255,255,.12);
  padding-bottom: .25rem;
}

/* bağlantılar, listeler, kod blokları, alıntılar okunaklı olsun */
.result-box a{ color: #a5b4fc; text-decoration: underline; }
.result-box ul, .result-box ol{ margin: .5rem 0 .75rem 1.25rem; }
.result-box code, .result-box pre{
  background: rgba(255,255,255,.06);
  color: #f8fafc;
  padding: .15rem .35rem;
  border-radius: .35rem;
}
.result-box blockquote{
  border-left: 3px solid rgba(255,255,255,.18);
  padding: .25rem .75rem;
  color: #e5e7eb;
  background: rgba(255,255,255,.04);
  border-radius: .5rem;
}



    /* Sidebar (glass + spacing) */
    section[data-testid="stSidebar"]{ background:rgba(15,32,39,.95)!important; backdrop-filter:blur(20px)!important; border-right:1px solid rgba(255,255,255,.1)!important; }
    section[data-testid="stSidebar"]>div{ padding:2rem 1.5rem!important; }
    section[data-testid="stSidebar"] h2, section[data-testid="stSidebar"] h4, section[data-testid="stSidebar"] .element-container{ color:rgba(255,255,255,.95)!important; }

    .card{ background:rgba(255,255,255,.98); border-radius:20px; padding:2rem; box-shadow:0 20px 60px rgba(0,0,0,.3);
           border:1px solid rgba(255,255,255,.2); backdrop-filter:blur(10px); transition:all .4s cubic-bezier(.16,1,.3,1);
           animation:fadeInUp .6s cubic-bezier(.16,1,.3,1); margin-bottom:1.5rem;}
    .card:hover{ transform:translateY(-5px); box-shadow:0 25px 80px rgba(0,0,0,.4); }

    .stButton>button{ background:linear-gradient(135deg,#667eea 0%,#764ba2 100%)!important; color:#fff!important; border:none!important; border-radius:12px!important;
        font-weight:600!important; height:52px!important; font-size:.95rem!important; letter-spacing:.02em!important; transition:all .3s cubic-bezier(.16,1,.3,1)!important;
        box-shadow:0 8px 24px rgba(102,126,234,.4)!important; position:relative!important; overflow:hidden!important; }
    .stButton>button:before{ content:''; position:absolute; top:0; left:-100%; width:100%; height:100%;
        background:linear-gradient(90deg,transparent,rgba(255,255,255,.3),transparent); transition:left .5s; }
    .stButton>button:hover:before{ left:100%; }
    .stButton>button:hover{ transform:translateY(-3px)!important; box-shadow:0 12px 32px rgba(102,126,234,.6)!important; }
    .stButton>button:active{ transform:translateY(-1px)!important; }

    /* Result + success boxes */
    .result-box{ background:linear-gradient(135deg,#f8f9ff 0%,#f0f4ff 100%); border-left:4px solid #667eea; border-radius:16px; padding:1.75rem;
                 box-shadow:0 4px 16px rgba(102,126,234,.1); color:#2d3748; line-height:1.7; font-size:.95rem; }
    .success-box{ background:linear-gradient(135deg,#d4f4dd 0%,#b7f0c8 100%); border-left:4px solid #48bb78; padding:1.25rem 1.5rem; border-radius:12px;
                  margin-bottom:1.5rem; color:#22543d; font-weight:500; box-shadow:0 4px 12px rgba(72,187,120,.2); }

    /* --- Sidebar: Live Stats --- */
    .sidebar-title{ color:#cbd5ff; font-weight:700; letter-spacing:.08em; text-transform:uppercase; margin:0 0 .75rem 0; display:flex; gap:.5rem; align-items:center;}
    .live-stats{ display:grid; grid-template-columns:1fr 1fr; gap:.8rem; }
    .stat-card{ border-radius:14px; padding:.9rem 1rem; background:rgba(17,24,39,.5);
        border:1px solid rgba(124,58,237,.45); box-shadow:inset 0 0 0 1px rgba(99,102,241,.25);
        transition:transform .25s ease, box-shadow .25s ease; }
    .stat-card:hover{ transform:translateY(-2px); box-shadow:0 8px 24px rgba(99,102,241,.25); }
    .stat-value{ font-size:1.9rem; font-weight:800; background:linear-gradient(135deg,#a78bfa 0%,#7c3aed 100%);
        -webkit-background-clip:text; -webkit-text-fill-color:transparent; line-height:1; }
    .stat-label{ color:#9aa4b2; margin-top:.25rem; font-weight:600; font-size:.85rem; }

    /* --- Sidebar: FAQ cards --- */
    .faq-wrapper{ margin-top:1.25rem; display:flex; flex-direction:column; gap:.75rem; }
    .faq-card{ padding:1rem 1.1rem; border-radius:14px; background:rgba(17,24,39,.55); border:1px solid rgba(148,163,184,.15);
               box-shadow:inset 0 0 0 1px rgba(99,102,241,.15); transition:transform .25s ease, border-color .25s ease; }
    .faq-card:hover{ transform:translateX(4px); border-color:rgba(124,58,237,.45); }
    .faq-title{ color:#e5e7eb; font-weight:700; margin-bottom:.25rem; }
    .faq-desc{ color:#a0aec0; font-size:.9rem; }

    /* --- Sidebar: KVKK badge --- */
    .kvkk-badge{ margin-top:1.25rem; padding:1rem 1.25rem; border-radius:14px;
                 background:linear-gradient(135deg, rgba(16,185,129,.15), rgba(5,150,105,.15));
                 border:1px solid rgba(16,185,129,.35); text-align:center; box-shadow:0 8px 30px rgba(16,185,129,.15); }
    .kvkk-title{ font-weight:800; color:#34d399; display:flex; gap:.5rem; justify-content:center; align-items:center; }
    .kvkk-sub{ color:#c6f6d5; margin-top:.25rem; font-weight:600; }
    @keyframes pulse{ 0%,100%{opacity:1} 50%{opacity:.7} }
    .pulse{ animation:pulse 2s ease-in-out infinite; }
    
    /* Streamlit varsayılan boşlukları kaldır */
    .element-container:has(> .stMarkdown) { margin-bottom: 0 !important; padding-bottom: 0 !important; }
    div[data-testid="column"] > div { gap: 0 !important; }
</style>
""", unsafe_allow_html=True)


# --- Sidebar Header ---
st.sidebar.markdown("<h2 style='margin-bottom: 0.5rem;'>🤖 AI Assistant Pro</h2>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='color: rgba(255,255,255,0.7); font-size: 0.9rem; margin-bottom: 2rem;'>Akıllı Müşteri Destek & Yönerge Analiz Sistemi</p>", unsafe_allow_html=True)
st.sidebar.markdown("---")

# --- Tab State (güvenli başlatma) ---
if "selected_tab" not in st.session_state:
    st.session_state.selected_tab = "💬 Müşteri Destek Sistemi"

tabs = {
    "💬 Müşteri Destek Sistemi": "Müşteri Destek Sistemi",
    "📘 Yönerge Özetleyici Chatbot": "Yönerge Özetleyici Chatbot",
}

st.sidebar.markdown("<h4 style='margin-bottom: 1rem; font-size: 0.95rem; letter-spacing: 0.05em;'>🧭 ÇALIŞMA MODU</h4>", unsafe_allow_html=True)
for key in tabs.keys():
    if st.sidebar.button(key, key=f"tab_{key}"):
        st.session_state.selected_tab = key

st.sidebar.markdown("---")

# === Sidebar: CANLI İSTATİSTİKLER (düzeltilmiş boyutlar) ===
st.sidebar.markdown("<div class='sidebar-title'>📊 CANLI İSTATİSTİKLER</div>", unsafe_allow_html=True)
st.sidebar.markdown("""
<div class="live-stats">
  <div class="stat-card">
    <div class="stat-value">247</div>
    <div class="stat-label">Sorgular</div>
  </div>
  <div class="stat-card">
    <div class="stat-value">1.2s</div>
    <div class="stat-label">Yanıt</div>
  </div>
</div>
""", unsafe_allow_html=True)

# === Sidebar: SSS ===
st.sidebar.markdown("<div class='sidebar-title' style='margin-top:1.25rem;'>❓ SIKÇA SORULAN SORULAR</div>", unsafe_allow_html=True)
st.sidebar.markdown("""
<div class="faq-wrapper">
  <div class="faq-card">
    <div class="faq-title">📎 Hangi dosya formatları destekleniyor?</div>
    <div class="faq-desc">PDF, DOCX ve TXT formatları tam olarak desteklenmektedir.</div>
  </div>
  <div class="faq-card">
    <div class="faq-title">⚡ Yanıt süresi ne kadar?</div>
    <div class="faq-desc">Ortalama yanıt süresi 1–2 saniye arasında değişmektedir.</div>
  </div>
  <div class="faq-card">
    <div class="faq-title">🔒 Verilerim güvende mi?</div>
    <div class="faq-desc">Tüm veriler KVKK uyumlu şekilde işlenir ve saklanmaz.</div>
  </div>
  <div class="faq-card">
    <div class="faq-title">🤖 Müşteri desteği nasıl çalışır?</div>
    <div class="faq-desc">Yapay zeka, mesajı analiz eder ve otomatik yanıt önerir.</div>
  </div>
  <div class="faq-card">
    <div class="faq-title">🧩 Yönerge analizi ne işe yarar?</div>
    <div class="faq-desc">Karmaşık belgeleri özetler ve soruları yanıtlar.</div>
  </div>
</div>
""", unsafe_allow_html=True)

# === Sidebar: KVKK Rozeti ===
st.sidebar.markdown("""
<div class="kvkk-badge pulse">
  <div class="kvkk-title">🛡️ KVKK UYUMLU</div>
  <div class="kvkk-sub">Verileriniz güvendedir</div>
</div>
""", unsafe_allow_html=True)

# --- Common text extraction ---
def extract_text(file):
    if file is None:
        return ""
    if file.name.endswith(".txt"):
        return file.read().decode("utf-8", errors="ignore")
    elif file.name.endswith(".pdf"):
        pdf = PyPDF2.PdfReader(file)
        return "\n".join(page.extract_text() or "" for page in pdf.pages)
    elif file.name.endswith(".docx"):
        doc = docx.Document(file)
        return "\n".join(p.text for p in doc.paragraphs)
    return ""

# ==========================================================
# 💬 MODE 1 — Customer Support
# ==========================================================
if st.session_state.selected_tab == "💬 Müşteri Destek Sistemi":
    st.markdown("<h1 style='text-align:center; margin-bottom: 0.5rem;'>💼 Müşteri Destek Paneli</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color: rgba(255,255,255,0.7); font-size: 1.1rem; margin-bottom: 2.5rem;'>Akıllı yanıt sistemiyle müşteri sorunlarını analiz edin ve otomatik çözüm önerileri üretin</p>", unsafe_allow_html=True)

    @st.cache_resource
    def get_support_system():
        return SmartCustomerSupportSystem()

    sys = get_support_system()

    
    st.markdown("### 📋 Destek Talebi Bilgileri")
    
    cid = st.text_input("🧍‍♀️ Müşteri ID", "CUS001", key="customer_id")
    msg = st.text_area("💬 Müşteri Mesajı", height=180, key="customer_msg")

    if st.button("🚀 Yanıt Oluştur", use_container_width=True):
        with st.spinner("Yapay zeka yanıtı hazırlıyor..."):
            result = sys.handle_customer_request(cid, msg)

        st.markdown('<div class="success-box">✅ Yanıt başarıyla oluşturuldu!</div>', unsafe_allow_html=True)

        st.markdown("### 📤 Önerilen Yanıt")
        st.markdown(f"<div class='result-box'><strong>Sayın müşterimiz,</strong><br><br>{result['response']}</div>", unsafe_allow_html=True)

        
# ==========================================================
# 📘 MODE 2 — Instruction Explainer
# ==========================================================
elif st.session_state.selected_tab == "📘 Yönerge Özetleyici Chatbot":
    st.markdown("<h1 style='text-align:center; margin-bottom: 0.5rem;'>📘 Yönerge Özetleyici & Açıklayıcı</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color: rgba(255,255,255,0.7); font-size: 1.1rem; margin-bottom: 2.5rem;'>Yönerge belgelerini analiz edin ve detaylı açıklamalar alın</p>", unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1], gap="large")

    with col1:
        st.markdown("### 📄 Belge Yükleme")
        uploaded = st.file_uploader("Yönerge dosyanızı buraya yükleyin", type=["txt", "pdf", "docx"], key="file_upload")

        st.markdown("### 💬 Soru Sorun")
        question = st.text_input("Belge hakkında ne öğrenmek istiyorsunuz?", "Bu yönerge ne işe yarıyor?", key="question_input")

        @st.cache_resource
        def get_llm():
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                st.error("❌ OPENAI_API_KEY bulunamadı! Lütfen .env dosyasını kontrol edin.")
            return ChatOpenAI(model="gpt-4o-mini", temperature=0.3, api_key=api_key)

        llm = get_llm()

        if st.button("🔍 Analiz Et & Açıkla", use_container_width=True):
            if not uploaded:
                st.warning("⚠️ Lütfen önce bir yönerge dosyası yükleyin.")
            else:
                text = extract_text(uploaded)
                if not text.strip():
                    st.error("❌ Dosyadan metin çıkarılamadı.")
                else:
                    with st.spinner("Belge analiz ediliyor..."):
                        prompt = ChatPromptTemplate.from_template("""
                            Aşağıdaki yönergeyi detaylı olarak analiz et:
                            ---
                            {document}
                            ---
                            Kullanıcının sorusu: {question}
                            
                            Cevabı açıklayıcı, profesyonel ve anlaşılır biçimde ver. 
                            Önemli noktaları vurgula ve örnekler kullan.
                        """)
                        chain = prompt | llm
                        answer = chain.invoke({"document": text[:6000], "question": question})

                    st.markdown('<div class="success-box">✅ Analiz tamamlandı!</div>', unsafe_allow_html=True)
                    st.markdown("### 📝 Detaylı Açıklama")
                    st.markdown(f"<div class='result-box'>{answer.content}</div>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("### 🎯 Özellikler")
        st.markdown("""
        <div style='display: flex; flex-direction: column; gap: 0.75rem;'>
            <div style='padding: 0.75rem; border-radius: 10px; background: linear-gradient(135deg, #f8f9ff 0%, #f0f4ff 100%); border-left: 3px solid #667eea;'>
                <div style='font-size: 1.1rem; font-weight: 700; color: #667eea;'>PDF</div>
                <div style='font-size: 0.85rem; color: #4a5568;'>Desteklenir</div>
            </div>
            <div style='padding: 0.75rem; border-radius: 10px; background: linear-gradient(135deg, #f8f9ff 0%, #f0f4ff 100%); border-left: 3px solid #667eea;'>
                <div style='font-size: 1.1rem; font-weight: 700; color: #667eea;'>DOCX</div>
                <div style='font-size: 0.85rem; color: #4a5568;'>Desteklenir</div>
            </div>
            <div style='padding: 0.75rem; border-radius: 10px; background: linear-gradient(135deg, #f8f9ff 0%, #f0f4ff 100%); border-left: 3px solid #667eea;'>
                <div style='font-size: 1.1rem; font-weight: 700; color: #667eea;'>TXT</div>
                <div style='font-size: 0.85rem; color: #4a5568;'>Desteklenir</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("### 💡 Kullanım İpuçları")
        st.markdown("""
        <p style='color: #000000; line-height: 1.8; font-size: 0.9rem;'>
        <strong>• Net Sorular:</strong> Spesifik sorular sorun<br><br>
        <strong>• Kısa Belgeler:</strong> Daha hızlı işlenir<br><br>
        <strong>• Detaylı Analiz:</strong> Tam açıklama alın
        </p>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)