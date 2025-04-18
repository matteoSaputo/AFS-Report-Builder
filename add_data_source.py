import pandas as pd
from rapidfuzz import process, fuzz

# Load both files
apps = pd.read_csv("./App_Data/Sales-Apps.csv", low_memory=False)
sources = pd.read_csv("./App_Data/data_sources.csv")
advances = pd.read_csv("./App_Data/advances.csv")

GENERIC_TERMS = {
    "LLC", "INC", "CORP", "COMPANY", "GROUP", "ENTERPRISES", "SERVICES",
    "THE", "AND", "&", "CO", "LTD"
}

def normalize(name, max_tokens=3):
    clean = str(name).upper().replace(",", "").replace(".", "").strip()
    tokens = [token for token in clean.split() if token not in GENERIC_TERMS]
    return " ".join(tokens[:max_tokens])

# Normalize all names
apps['Business_clean'] = apps['Business'].apply(normalize)
sources['Business Name_clean'] = sources['Business Name'].apply(normalize)
advances['Business Name_clean'] = advances['Business Name'].apply(normalize)
advances['Business Name_clean'] = advances['Business Name_clean'].str.extract(r'^(.+?)\s+\d+$', expand=False).fillna(advances['Business Name_clean'])

# Ensure Business column is string before filtering
apps['Business'] = apps['Business'].astype(str)

# Now filter out empty or "nan" string values
apps = apps[apps['Business'].str.strip().str.upper() != "NAN"]
apps = apps[apps['Business'].str.strip() != ""]

# === Create Two Source Dictionaries ===

# 1. Filtered to businesses that have advances
# Only keep sources with advances AND filled data source
sources_with_advances = sources[
    sources['Business Name_clean'].isin(advances['Business Name_clean']) &
    sources['Data Source'].notna() &
    (sources['Data Source'].str.strip() != '')
]

# Then deduplicate
sources_adv_unique = sources_with_advances.drop_duplicates(subset='Business Name_clean')

adv_lookup = dict(zip(sources_adv_unique['Business Name_clean'], sources_adv_unique['Data Source']))

# 2. Full source dictionary (fallback)
sources_full_unique = sources.drop_duplicates(subset='Business Name_clean')
full_lookup = dict(zip(sources_full_unique['Business Name_clean'], sources_full_unique['Data Source']))

# === Step 1: exact match (advance-filtered only) ===
apps['Matched Source'] = apps['Business_clean'].map(adv_lookup)

# === Step 2: fuzzy match with fallback ===
def fuzzy_match_fallback(row):
    if pd.notna(row['Matched Source']):
        return pd.Series([None, None, None])

    # First: try fuzzy match from advance-filtered source
    match = process.extractOne(
        row['Business_clean'],
        adv_lookup.keys(),
        scorer=fuzz.token_sort_ratio
    )
    if match and match[1] >= 90:
        return pd.Series([match[0], adv_lookup[match[0]], match[1]])

    # Fallback: try fuzzy match from full data_sources
    match = process.extractOne(
        row['Business_clean'],
        full_lookup.keys(),
        scorer=fuzz.token_sort_ratio
    )
    if match and match[1] >= 90:
        return pd.Series([match[0], full_lookup[match[0]], match[1]])

    # print(f"{row['Business_clean']} : {match}")
    return pd.Series([None, None, None])

# Apply and store results
apps[['Fuzzy Match', 'Fuzzy Data Source', 'Fuzzy Score']] = apps.apply(fuzzy_match_fallback, axis=1)

# === Step 3: Fill Data Source (preserving existing values) ===
# 1. Start with existing
apps['Final Data Source'] = apps['Data Source']

# 2. Fill from exact match
apps['Final Data Source'] = apps['Final Data Source'].fillna(apps['Matched Source'])

# 3. Fill from fuzzy match
apps['Final Data Source'] = apps['Final Data Source'].fillna(apps['Fuzzy Data Source'])

# 4. Set to 'Manual Entry' if fuzzy match exists but matched file had no source
apps.loc[
    (apps['Final Data Source'].isna()) &
    (apps['Fuzzy Match'].notna()) &
    (apps['Fuzzy Data Source'].isna() | (apps['Fuzzy Data Source'].str.strip() == '')),
    'Final Data Source'
] = 'Manual Entry'

# Assign final result
apps['Data Source'] = apps['Final Data Source']

# Filter only apps that are still missing a Data Source and had no prior fuzzy match
needs_loose_match = apps[
    (apps['Data Source'].isna()) &
    (apps['Fuzzy Match'].isna())
]

# Save output
apps.drop(columns=['Business_clean', 'Matched Source', 'Final Data Source'], inplace=True)
apps.to_csv("Sales-Apps-FuzzyMatched.csv", index=False)

print("Match complete — Saved to Sales-Apps-FuzzyMatched.csv")
