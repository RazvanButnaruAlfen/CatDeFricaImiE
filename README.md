
# S.A.T.A. 4.0

Sistem Automat pentru Tensiunea Alexandrei.

## Rulare locală

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy pe Streamlit Community Cloud

1. Încarcă întregul conținut al arhivei în repository.
2. Verifică să existe `app.py` în rădăcina repository-ului.
3. În Streamlit Community Cloud selectează `app.py`.
4. Apasă Deploy.

Aplicația include:
- evoluție automată în funcție de dată;
- glume zilnice deterministe;
- recomandări 80% comice / 20% calde;
- „Ce știe” și „Ce nu știe” S.A.T.A.;
- declasificarea raportului;
- export JPG;
- alarme WAV;
- mod de testare a datei din sidebar.
