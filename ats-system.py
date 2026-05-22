#!/bin/python3

import pypdf
import pandas as pd
import argparse
import re


# ARGUMENTY Z TERMINALA

parser = argparse.ArgumentParser(description="Analiza CV vs słowa kluczowe")

parser.add_argument("cv_file", help="Ścieżka do pliku PDF z CV")
parser.add_argument("keywords_file", help="Plik ze słowami kluczowymi")

args = parser.parse_args()


# Wczytanie CV

reader = pypdf.PdfReader(args.cv_file)

tekst = ""
for page in reader.pages:
    tekst += page.extract_text() or ""

tekst = tekst.lower()

# czyszczenie tekstu

tekst = re.sub(r"[^\w\sąćęłńóśźż]", " ", tekst)
tekst = re.sub(r"\s+", " ", tekst).strip()


# Wczytanie słów kluczowych

with open(args.keywords_file, "r", encoding="utf-8") as f:
    zawartosc = f.read().lower()

slowa_klucze = [
    s.strip()
    for s in zawartosc.split(",")
    if s.strip()
]


# LICZENIE WYSTĄPIEŃ

liczba_wystapien = {
    slowo: tekst.count(slowo)
    for slowo in slowa_klucze
}


# DATAFRAME

df = pd.DataFrame(
    liczba_wystapien.items(),
    columns=["slowo_kluczowe", "znaleziono_razy"]
)


# DOPASOWANIE (%)

znalezione = (df["znaleziono_razy"] > 0).sum()
wszystkie = len(df)

poziom_dopasowania = (znalezione / wszystkie * 100) if wszystkie > 0 else 0


# WYNIKI

print(df)
print(f"\nPoziom dopasowania: {poziom_dopasowania:.0f}%")

if poziom_dopasowania >= 75:
    print("\033[92mKandydat dopuszczony do rekrutacji!\033[0m")
else:
    print("\033[91mKandydat nie dopuszczony do rekrutacji!\033[0m")
