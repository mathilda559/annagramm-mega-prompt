import streamlit as st
import pdfplumber
from collections import Counter
import itertools
import re
import random

# -------------------------------
# PDF WORTLISTE LADEN
# -------------------------------

@st.cache_data
def lade_wortliste():
    woerter = set()

    with pdfplumber.open("Goethe Wortliste.pdf") as pdf:
        for seite in pdf.pages:
            text = seite.extract_text()
            if text:
                for wort in re.findall(r"[A-Za-zäöüÄÖÜß]+", text):
                    woerter.add(wort.lower())

    return woerter

wortliste = lade_wortliste()

# -------------------------------
# ANAGRAMM HILFSFUNKTIONEN
# -------------------------------

def ist_moeglich(wort, buchstaben):
    return not (Counter(wort) - buchstaben)

def finde_anagramme(eingabe, wortliste, max_ergebnisse=10):
    eingabe = eingabe.lower().replace(" ", "")
    buchstaben = Counter(eingabe)

    passende_woerter = [
        w for w in wortliste
        if len(w) > 1 and ist_moeglich(w, buchstaben)
    ]

    ergebnisse = set()

    for anzahl in range(1, 5):
        for kombi in itertools.combinations(passende_woerter, anzahl):
            gesamtes_wort = "".join(kombi)
            if ist_moeglich(gesamtes_wort, buchstaben):
                ergebnisse.add(" ".join(kombi))
                if len(ergebnisse) >= max_ergebnisse:
                    return list(ergebnisse)

    return list(ergebnisse)

# -------------------------------
# STREAMLIT UI
# -------------------------------

st.set_page_config(page_title="Anagramm Generator", page_icon="💗")

st.markdown("""
<style>
.stApp {
    background-color: #ffc0cb;
}
h1, h2, h3, label, p, div {
    color: red;
}
</style>
""", unsafe_allow_html=True)

st.title("💗 Deutscher Anagramm Generator")

eingabe = st.text_input("Satz eingeben:")

# Session-State vorbereiten
if "anagramme" not in st.session_state:
    st.session_state.anagramme = []

if eingabe:
    if st.button("Anagramme generieren"):
        st.session_state.anagramme = finde_anagramme(eingabe, wortliste)
        random.shuffle(st.session_state.anagramme)

    if st.session_state.anagramme:
        st.subheader("Gefundene Anagramme:")

        if st.button("🔀 Neu mischen"):
            random.shuffle(st.session_state.anagramme)

        for e in st.session_state.anagramme:
            st.write("👉", e)
    else:
        st.write("Keine Anagramme gefunden.")

# -------------------------------
# INFO
# -------------------------------

st.caption(f"Wörter geladen: {len(wortliste)}")
