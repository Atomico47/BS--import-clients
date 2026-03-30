import pandas as pd
import argparse

INPUT_FILE = "clienti-origine-ita.csv"
OUTPUT_FILE = "clienti_shopify-ita.csv"

NEWSLETTER_COL = "Iscrizione alla Newsletter e Autorizzazioni di Marketing"


def get_column_or_default(dataframe, column_name, default_value=""):
    if column_name in dataframe.columns:
        return dataframe[column_name]
    return pd.Series([default_value] * len(dataframe), index=dataframe.index, dtype="string")


def clean_text(value):
    if pd.isna(value):
        return ""
    value = str(value).strip()
    return "" if value.lower() == "nan" else value


def clean_country(value):
    value = clean_text(value).upper()
    return value if value else "IT"


def newsletter_to_yes_no(value):
    return "yes" if clean_text(value) else "no"


EXPECTED_COLUMNS = [
    "First Name",
    "Last Name",
    "Email",
    "Accepts Email Marketing",
    "Default Address Company",
    "Default Address Address1",
    "Default Address Address2",
    "Default Address City",
    "Default Address Province Code",
    "Default Address Country Code",
    "Default Address Zip",
    "Default Address Phone",
    "Phone",
    "Accepts SMS Marketing",
    "Tags",
    "Note",
    "Tax Exempt",
]


def build_shopify_dataframe(df):
    out = pd.DataFrame()
    out["First Name"] = get_column_or_default(df, "Nome").apply(clean_text)
    out["Last Name"] = get_column_or_default(df, "Cognome").apply(clean_text)
    out["Email"] = get_column_or_default(df, "Indirizzo Email").apply(clean_text)
    out["Accepts Email Marketing"] = get_column_or_default(df, NEWSLETTER_COL).apply(newsletter_to_yes_no)

    out["Default Address Company"] = ""
    out["Default Address Address1"] = get_column_or_default(df, "Indirizzo").apply(clean_text)
    out["Default Address Address2"] = ""
    out["Default Address City"] = ""
    out["Default Address Province Code"] = get_column_or_default(df, "REGION").apply(lambda v: clean_text(v).upper())
    out["Default Address Country Code"] = get_column_or_default(df, "CC").apply(clean_country)
    out["Default Address Zip"] = ""
    out["Default Address Phone"] = get_column_or_default(df, "Telefono Cellulare").apply(clean_text)
    out["Phone"] = ""

    out["Accepts SMS Marketing"] = "no"
    out["Tags"] = out["Default Address Country Code"].apply(lambda c: "ITA" if c == "IT" else "ENG")
    out["Note"] = ""
    out["Tax Exempt"] = "no"
    return out[EXPECTED_COLUMNS]


def parse_args():
    parser = argparse.ArgumentParser(description="Converte CSV clienti in formato Shopify.")
    parser.add_argument("-i", "--input", default=INPUT_FILE, help="Percorso CSV input.")
    parser.add_argument("-o", "--output", default=OUTPUT_FILE, help="Percorso CSV output.")
    return parser.parse_args()


def main():
    args = parse_args()
    df = pd.read_csv(args.input, dtype=str, keep_default_na=False)
    out = build_shopify_dataframe(df)
    out.to_csv(args.output, index=False)
    print(f"✅ CSV Shopify creato correttamente: {args.output}")


if __name__ == "__main__":
    main()
