import os
import pandas as pd
from datetime import datetime
from sklearn.externals import joblib
from prophet import Prophet
import shutil

# Chemins vers les fichiers et dossiers du projet
data_folder = "./data/"
scripts_folder = "./scripts/"
models_folder = "./models/"
visualizations_folder = "./visualizations/"


# 1. Mettre à jour les données (exemple avec un fichier CSV)
def update_data():
    print(f"[{datetime.now()}] Mise à jour des données...")

    # Charger les nouvelles données (exemple avec le fichier ventes.csv)
    new_data = pd.read_csv(os.path.join(data_folder, "ventes.csv"))

    # Traitement des données (nettoyage, agrégation, etc.)
    # Ici tu peux appeler une fonction de nettoyage ou de préparation
    cleaned_data = clean_data(new_data)

    # Sauvegarder les données nettoyées
    cleaned_data.to_csv(os.path.join(data_folder, "ventes_cleaned.csv"), index=False)
    print(f"[{datetime.now()}] Données mises à jour et nettoyées.")


# Fonction de nettoyage de données
def clean_data(data):
    # Exemple de nettoyage basique : suppression des valeurs manquantes
    return data.dropna()


# 2. Actualiser les modèles de prédiction
def update_models():
    print(f"[{datetime.now()}] Mise à jour des modèles...")

    # Exemple d'entraînement du modèle Prophet
    model_file = os.path.join(models_folder, "prophet_model.pkl")

    # Charger les nouvelles données pour entraîner le modèle
    data = pd.read_csv(os.path.join(data_folder, "ventes_cleaned.csv"))
    df = data[["date", "ventes"]]  # Assurez-vous que les colonnes existent
    df["date"] = pd.to_datetime(df["date"])

    # Créer un modèle Prophet
    model = Prophet()
    model.fit(df)

    # Sauvegarder le modèle
    joblib.dump(model, model_file)
    print(f"[{datetime.now()}] Modèle mis à jour et sauvegardé.")


# 3. Actualiser les visualisations (si applicable)
def update_visualizations():
    print(f"[{datetime.now()}] Mise à jour des visualisations Power BI...")

    # Exemple de création d'un graphique ou d'un tableau
    # Ici, tu pourrais automatiser l'export de nouvelles données ou résultats de prédiction vers Power BI

    # Copier un fichier de visualisation actualisé dans le dossier approprié (ex. Power BI .pbix)
    shutil.copy(
        "path/to/updated_dashboard.pbix",
        os.path.join(visualizations_folder, "dashboard.pbix"),
    )
    print(f"[{datetime.now()}] Visualisations mises à jour.")


# 4. Exécution complète du script
def main():
    update_data()  # Mettre à jour les données
    update_models()  # Mettre à jour les modèles de prédiction
    update_visualizations()  # Mettre à jour les visualisations Power BI


if __name__ == "__main__":
    main()
