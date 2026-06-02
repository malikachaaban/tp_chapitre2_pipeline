# TP Chapitre 2 — Pipelines agiles avec dlt, dbt et Dagster

> Module : MLOps & DataOps — Master d'Excellence Intelligence Artificielle  
> Auteure : Malika CHAABAN | Année Universitaire : 2025-2026

## Description

Pipeline de données agile et versionné, couvrant l'ingestion, la validation, la transformation et l'orchestration, avec intégration continue via GitHub Actions.

**Stack technique :** Python · DuckDB · dbt · Dagster · GitHub Actions

---

## Structure du projet

```
tp_chapitre2_pipeline/
├── data/
│   └── ventes.csv               # Données source
├── pipeline/
│   ├── ingest.py                # Étape 1 : Ingestion CSV → DuckDB
│   ├── validate.py              # Étape 2 : Validation du schéma et qualité
│   └── orchestrate.py           # Étape 5 : Orchestration Dagster
├── dbt_pipeline/
│   ├── dbt_project.yml
│   ├── profiles.yml
│   └── models/
│       ├── ventes_clean.sql     # Transformation et calcul du CA
│       ├── ventes_resume.sql    # Agrégation par catégorie
│       └── schema.yml           # Tests dbt
├── .github/
│   └── workflows/
│       └── ci.yml               # CI GitHub Actions
├── requirements.txt
└── .gitignore
```

---

## Installation

```bash
# Cloner le dépôt
git clone https://github.com/malikachaaban/tp_chapitre2_pipeline.git
cd tp_chapitre2_pipeline

# Créer et activer l'environnement virtuel
python3 -m venv .venv
source .venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt
```

---

## Exécution du pipeline

### Étape 1 — Ingestion
Charge le fichier CSV dans DuckDB sous forme de table `ventes_raw`.
```bash
python pipeline/ingest.py
```

### Étape 2 — Validation
Vérifie la présence des colonnes requises et l'absence de valeurs nulles.
```bash
python pipeline/validate.py
```

### Étape 3 — Transformation avec dbt
Crée les tables `ventes_clean` (avec calcul du chiffre d'affaires) et `ventes_resume` (agrégation par catégorie).
```bash
cd dbt_pipeline
dbt run --profiles-dir .
cd ..
```

### Étape 4 — Tests dbt
Vérifie les contraintes `not_null` sur les colonnes critiques.
```bash
cd dbt_pipeline
dbt test --profiles-dir .
cd ..
```

### Étape 5 — Orchestration avec Dagster
Lance l'interface web Dagster pour exécuter et monitorer le pipeline complet.
```bash
dagster dev -f pipeline/orchestrate.py
# Interface disponible sur http://127.0.0.1:3000
```

---

## Schéma du pipeline

```
CSV local → Ingestion (dlt) → Validation (DuckDB) → Transformation (dbt) → Orchestration (Dagster)
```

---

## CI / Intégration Continue

Un workflow GitHub Actions se déclenche à chaque push ou pull request sur `main`. Il effectue :
- Installation des dépendances
- Vérification syntaxique des scripts Python (`py_compile`)

---

## Données source

Le fichier `data/ventes.csv` contient des ventes fictives avec les colonnes :

| date | produit | categorie | quantite | prix_unitaire | ville |
|------|---------|-----------|----------|---------------|-------|
| 2026-01-01 | Clavier | Informatique | 2 | 300 | Casablanca |
| ... | ... | ... | ... | ... | ... |

---

## Modèles dbt

| Modèle | Description |
|--------|-------------|
| `ventes_clean` | Filtre les lignes valides, calcule `quantite * prix_unitaire` |
| `ventes_resume` | Agrège le total quantité et chiffre d'affaires par catégorie |
