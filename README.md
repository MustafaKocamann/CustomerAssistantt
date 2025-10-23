# 🤖 AI Assistant Pro
# Akıllı Müşteri Destek ve Yönerge Analiz Sistemi

## 📘 Proje Özeti
* AI Assistant Pro, OpenAI ve LangChain tabanlı bir yapay zeka destekli müşteri destek ve belge analiz platformudur.
* Kullanıcı mesajlarını analiz eder, otomatik yanıtlar üretir ve PDF/DOCX/TXT belgelerindeki yönergeleri özetleyip açıklar.
* Uygulama, modern bir Streamlit arayüzü ve KVKK uyumlu veri işleme yaklaşımıyla tasarlanmıştır.

## 🚀 Özellikler
* 💬 Müşteri Destek Sistemi — Müşteri mesajlarını analiz eder, uygun yapay zeka yanıtı üretir.
* 📘 Yönerge Özetleyici Chatbot — PDF, DOCX ve TXT belgelerini yükleyip doğal dilde sorular sorabilirsiniz.
* 🔍 OpenAI GPT Entegrasyonu — gpt-4o-mini modeliyle yüksek doğrulukta metin analizi.
* 🧠 LangChain Prompt Pipeline — Dinamik prompt yönetimi ve LLM zincirleme işlemleri.
* 🖥️ Streamlit UI — Modern, duyarlı, koyu temalı bir kullanıcı arayüzü.
*🔒 KVKK Uyumlu — Veriler anlık olarak işlenir, sistemde saklanmaz.

| Katman                   | Teknoloji                             |
| ------------------------ | ------------------------------------- |
| **Frontend**             | Streamlit, HTML, CSS (custom styling) |
| **Backend / LLM**        | OpenAI API (`gpt-4o-mini`), LangChain |
| **Veri İşleme**          | PyPDF2, python-docx                   |
| **Yapılandırma**         | python-dotenv                         |
| **Destekleyici Araçlar** | Pandas, Numpy, Tiktoken               |

## 🧠 Modüller
### 💼 1. Müşteri Destek Sistemi
* Kullanıcı mesajını alır (text_input, text_area).
* SmartCustomerSupportSystem sınıfı ile analiz eder.
* GPT tabanlı önerilen yanıt üretir.
* Yanıtı şık bir kutuda (result-box) gösterir.

### 📘 2. Yönerge Özetleyici Chatbot
* Kullanıcıdan PDF, DOCX veya TXT yüklemesi alır.
* Dosyadan metni çıkarır (extract_text fonksiyonu).
* Sorulan soruya göre yönergeyi özetleyip detaylı açıklama verir.
* Yanıt ChatPromptTemplate → ChatOpenAI zinciriyle üretilir.

## 🔐 KVKK & Güvenlik
* Veriler yalnızca geçici bellekte işlenir.
* Hiçbir kullanıcı içeriği sistemde saklanmaz.
* API anahtarı .env içinde gizli tutulur.
