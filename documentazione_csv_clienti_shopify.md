# Documentazione – CSV Clienti Shopify

## Installazione
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt


## Scopo del file

Questo file CSV serve per **importare clienti in Shopify** a partire da un file sorgente (es. Magento, CRM, mailing list), garantendo:

- compatibilità completa con l’import clienti Shopify
- gestione corretta dei campi mancanti
- tagging automatico per segmentazione (ITA / ENG)
- valorizzazione del **metafield compleanno**

Il file è pensato per essere **importato direttamente da Admin → Clienti → Importa**.

---

## Struttura del file finale

Il CSV finale contiene **esattamente le seguenti colonne**:

```
First Name
Last Name
Email
Accepts Email Marketing
Country Code
Accepts SMS Marketing
Tags
customer.metafields.custom.compleanno
```

⚠️ La colonna **Tax Exempt non è presente** (gestione fiscale demandata a logiche successive).

---

## Descrizione dettagliata delle colonne

### 1. Email

- **Obbligatoria**
- Usata da Shopify come identificativo univoco del cliente
- Viene importata così com’è dal file sorgente

---

### 2. First Name

- Nome del cliente
- Può essere **vuoto**
- Se mancante o nullo nel file origine → lasciato vuoto

---

### 3. Last Name

- Cognome del cliente
- Può essere **vuoto**
- Se mancante o nullo nel file origine → lasciato vuoto

---

### 4. Accepts Email Marketing

- Valore fisso: `TRUE`
- Indica che il cliente accetta comunicazioni email

---

### 5. Accepts SMS Marketing

- Valore fisso: `FALSE`
- Nessun consenso SMS viene importato

---

### 6. Country Code

- Codice paese ISO-2 (2 lettere)
- Regole applicate:
  - valore convertito in **maiuscolo**
  - se il campo è vuoto o mancante → impostato a `IT`

Esempi:

| Valore origine | Country Code |
| -------------- | ------------ |
| it             | IT           |
| fr             | FR           |
| (vuoto)        | IT           |

---

### 7. Tags

- Tag automatici per segmentazione clienti
- Regola:
  - `Country Code = IT` → `ITA`
  - qualsiasi altro paese → `ENG`

Esempi:

| Country Code | Tag |
| ------------ | --- |
| IT           | ITA |
| FR           | ENG |
| US           | ENG |

---

### 8. customer.metafields.custom.compleanno

- Metafield cliente Shopify
- Namespace: `custom`
- Key: `compleanno`
- Tipo: **Date**

#### Regole di valorizzazione

- Formato accettato: `YYYY-MM-DD`
- Valori vuoti, nulli o `0000-00-00` → campo lasciato vuoto

Esempi:

| Valore origine | Metafield  |
| -------------- | ---------- |
| 1985-07-21     | 1985-07-21 |
| (vuoto)        | (vuoto)    |
| 0000-00-00     | (vuoto)    |

---

## Logica di trasformazione (riassunto)

- Email: obbligatoria
- Nome / Cognome: opzionali
- Country:
  - fallback automatico a `IT`
- Tag:
  - IT → ITA
  - non-IT → ENG
- Compleanno:
  - solo date valide

Il file risultante è **sempre importabile**, anche in presenza di dati incompleti.

---

## Prerequisiti Shopify

Prima dell’import:

1. Creare il metafield cliente:

   - **Admin → Impostazioni → Dati personalizzati → Clienti**
   - Namespace: `custom`
   - Key: `compleanno`
   - Tipo: `Date`

2. Salvare

Shopify mapperà automaticamente la colonna `customer.metafields.custom.compleanno`.

---

## Modalità di import

1. Accedere a **Shopify Admin**
2. Andare in **Clienti → Importa**
3. Caricare il file CSV
4. Disabilitare l’invio automatico delle email di invito (consigliato)
5. Avviare l’import

---

## Note operative

- Shopify non importa password né storico ordini
- I clienti verranno creati come **account inattivi**
- Le automazioni (compleanno, sconti, email) possono essere gestite via:
  - Shopify Flow
  - n8n
  - Klaviyo

---

## Versionamento

- Versione file: **1.0**
- Uso previsto: import clienti iniziale / migrazione Magento → Shopify

---

## Contatti / manutenzione

Questo file è pensato per essere rigenerato automaticamente tramite script Python. Qualsiasi modifica alla struttura deve essere replicata nello script di conversione.

