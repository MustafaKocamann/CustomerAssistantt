# Smart Customer Support System (LangChain-Ready) — Python 3.13 Safe

**Teslim tarihi:** 2025-10-22

Bu repo, ödevdeki tüm gereksinimleri karşılayan ve **Python 3.13** ile sorunsuz çalışacak şekilde
sürüm-pinned edilen bir örnek projedir. Varsayılan olarak kurallar _LLM bağımlılığını minimuma indirir_;
isterseniz LangChain/OpenAI entegrasyonlarını kolayca devreye alabilirsiniz.

## Özellikler
- Multi-Chain akışı: **Analysis ➜ Response ➜ Quality**
- Hibrit memory (özet + pencere + metadata)
- Custom Tools: ticket, knowledge base, customer DB
- Basit streaming handler (token token yazdırır)
- Testler (unit + integration)
- Streamlit için hazır (opsiyonel UI eklemeniz kolay)

## Kurulum (Python 3.13)
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
python -V  # 3.13.x olmalı
pip install --upgrade pip
pip install -r requirements.txt -c constraints.txt
cp .env.example .env
```

> **Not:** Eğer ARM/M1/M2 macOS kullanıyorsanız ve eski `pip` yüzünden source build'e düşüyorsanız
> `pip install --upgrade pip wheel setuptools` komutu yardımcı olur.

## Çalıştırma
```bash
python main.py
```

## Streamlit (opsiyonel)
Basit bir UI için aşağıdaki dosyayı oluşturup çalıştırabilirsiniz:
`streamlit_app.py`
```python
import streamlit as st
from main import SmartCustomerSupportSystem

st.set_page_config(page_title="Smart Support", page_icon="🤖")
st.title("🤖 Smart Customer Support")

sys = SmartCustomerSupportSystem()
cid = st.text_input("Customer ID", "CUS001")
msg = st.text_area("Message", "Uygulamanız sürekli çöküyor, nasıl çözebilirim?")

if st.button("Send"):
    out = sys.handle_customer_request(cid, msg)
    st.json(out)
```

```bash
streamlit run streamlit_app.py
```

### Streamlit Cloud
- Kök dizine `runtime.txt` ekleyin: `python-3.13`
- Eğer pyarrow kaynaklı bir uyarı alırsanız `constraints.txt` içindeki `pyarrow<18` sınırını kaldırabilirsiniz.

## LangChain/OpenAI'ı devreye alma
Kod şablonu kasıtlı olarak hafif tutuldu. Aşağıdaki noktadan itibaren LLM ekleyebilirsiniz:
- `chains/response_chain.py` içinde `ResponseGenerationChain.__call__` gövdesi
- Örnek (pseudo):
```python
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model=os.getenv("OPENAI_MODEL","gpt-4o-mini"))
resp = llm.invoke("...prompt...")
```

## Testler
```bash
pytest -q
```

## Dosya Yapısı
(ödevde verilen yapı birebir)

## Sürüm Notları
- `numpy>=2.1` Python 3.13 için zorunludur.
- `pandas 2.2.3` 3.13 tekerlekleri sağlar.
- `streamlit 1.39+` 3.13 desteği bildirir.
- `langchain 0.3.x` split paket mimarisiyle çalışır.

## Sorun Giderme
- **`Failed building wheel for ...`**: `pip install --upgrade pip wheel setuptools`
- **`numpy 1.x` ile build'e düşüyor**: Eski paket pin’i; `pip show numpy` → 2.1+ olmalı.
- **`openai` hataları**: `.env` içindeki `OPENAI_API_KEY` değerini kontrol edin.
- **Çakışan bağımlılıklar**: `pip install -r requirements.txt -c constraints.txt` kullanın.

## Lisans
Eğitim amaçlı örnek.
