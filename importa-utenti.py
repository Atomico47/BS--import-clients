import pandas as pd

INPUT_FILE = "clienti-origine-ita.csv"
OUTPUT_FILE = "clienti_shopify-ita.csv"

df = pd.read_csv(INPUT_FILE)

out = pd.DataFrame()

# -----------------------------
# UTIL
# -----------------------------
def clean_and_capitalize(val):
    """
    - NaN / vuoto -> ""
    - normalizza spazi
    - capitalizza ogni parola
    """
    if pd.isna(val):
        return ""
    val = str(val).strip()
    if val == "" or val.lower() == "nan":
        return ""
    return val.title()

def normalize_country(c):
    if pd.isna(c):
        return "IT"
    c = str(c).strip()
    return "IT" if c == "" else c.upper()

def clean_date(d):
    if pd.isna(d):
        return ""
    d = str(d).strip()
    return "" if d in ("", "0000-00-00") else d

def clean_phone(p):
    """
    - NaN / vuoto -> ""
    - strip spazi
    - mantiene il numero così com'è (Shopify accetta +39 ecc.)
    """
    if pd.isna(p):
        return ""
    p = str(p).strip()
    return "" if p.lower() == "nan" else p

def choose_country_series(dataframe):
    """
    Usa prima la colonna CC (presente nel tracciato fornito),
    altrimenti fallback su Country.
    Se nessuna colonna esiste, ritorna una serie vuota (gestita poi come IT).
    """
    if "CC" in dataframe.columns:
        return dataframe["CC"]
    if "Country" in dataframe.columns:
        return dataframe["Country"]
    return pd.Series([""] * len(dataframe))

# -----------------------------
# MAPPING BASE
# -----------------------------
out["Email"] = df["Indirizzo Email"].astype(str).str.strip()
out["First Name"] = df["Nome"].apply(clean_and_capitalize)
out["Last Name"] = df["Cognome"].apply(clean_and_capitalize)

# -----------------------------
# PHONE
# -----------------------------
out["Phone"] = df["Telefono Cellulare"].apply(clean_phone)

# -----------------------------
# EMAIL MARKETING
# -----------------------------
newsletter_col = "Iscrizione alla Newsletter e Autorizzazioni di Marketing"
out["Accepts Email Marketing"] = df[newsletter_col].apply(
    lambda v: "TRUE" if (not pd.isna(v) and str(v).strip() != "") else "FALSE"
)

# -----------------------------
# COUNTRY
# -----------------------------
country_source = choose_country_series(df)
out["Default Address Country Code"] = country_source.apply(normalize_country)

# -----------------------------
# TAG ITA / ENG
# -----------------------------
out["Tags"] = out["Default Address Country Code"].apply(
    lambda c: "ITA" if c == "IT" else "ENG"
)

# -----------------------------
# EXPORT
# -----------------------------
out.to_csv(OUTPUT_FILE, index=False)

print(f"✅ CSV Shopify creato correttamente: {OUTPUT_FILE}")
