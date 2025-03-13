import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Configuration pour de meilleurs graphiques
plt.style.use('seaborn-v0_8-darkgrid')
sns.set(font_scale=1.2)
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.family'] = 'sans-serif'

def nettoyer_dataset(csv_path, output_path=None):
    """
    Nettoie le dataset marketing et retourne un DataFrame propre
    
    Args:
        csv_path: Chemin vers le fichier CSV
        output_path: Chemin où sauvegarder le fichier nettoyé (optionnel)
        
    Returns:
        DataFrame pandas nettoyé
    """
    print(f"Chargement du fichier: {csv_path}")
    
    # Vérifier si le fichier existe
    if not os.path.exists(csv_path):
        print(f"Erreur: Le fichier {csv_path} n'existe pas")
        return None
    
    try:
        # Charger le dataset
        df = pd.read_csv(csv_path)
        
        # Afficher les informations initiales
        print("\n--- INFORMATIONS INITIALES ---")
        print(f"Dimensions: {df.shape}")
        print("\nAperçu des données:")
        print(df.head())
        print("\nTypes de données:")
        print(df.dtypes)
        print("\nStatistiques descriptives:")
        print(df.describe())
        print("\nValeurs manquantes:")
        print(df.isnull().sum())
        
        print("\n--- NETTOYAGE DES DONNÉES ---")
        
        # 1. Convertir la colonne Date en datetime
        print("Conversion de la colonne Date en format datetime...")
        df['Date'] = pd.to_datetime(df['Date'])
        
        # 2. Extraire des composantes de date utiles
        print("Extraction des composantes de date...")
        df['Jour'] = df['Date'].dt.date
        df['Heure'] = df['Date'].dt.hour
        df['Mois'] = df['Date'].dt.month
        df['Année'] = df['Date'].dt.year
        
        # 3. Traiter les valeurs manquantes
        print("Traitement des valeurs manquantes...")
        colonnes_numeriques = ['Impressions', 'Clics', 'Conversions', 'Coût']
        for col in colonnes_numeriques:
            missing_count = df[col].isnull().sum()
            if missing_count > 0:
                median_val = df[col].median()
                print(f"  - {missing_count} valeurs manquantes dans '{col}', remplacées par la médiane ({median_val:.2f})")
                df[col] = df[col].fillna(median_val)
        
        # 4. Créer des métriques dérivées
        print("Création de métriques dérivées...")
        # Taux de clics (CTR)
        df['CTR'] = (df['Clics'] / df['Impressions']) * 100
        # Taux de conversion (CVR)
        df['CVR'] = (df['Conversions'] / df['Clics']) * 100
        # Coût par clic (CPC)
        df['CPC'] = df['Coût'] / df['Clics']
        # Coût par conversion (CPA)
        df['CPA'] = df['Coût'] / df['Conversions']
        
        # 5. Remplacer les valeurs infinies par NaN puis par 0
        print("Traitement des valeurs infinies...")
        df = df.replace([np.inf, -np.inf], np.nan)
        inf_count = df.isna().sum().sum() - df.isna().sum().sum()
        if inf_count > 0:
            print(f"  - {inf_count} valeurs infinies remplacées")
        df = df.fillna(0)
        
        # 6. Supprimer la colonne inutile
        print("Suppression de la colonne 'Inutile'...")
        if 'Inutile' in df.columns:
            df = df.drop('Inutile', axis=1)
        
        # 7. Vérifier les doublons
        duplicates = df.duplicated().sum()
        if duplicates > 0:
            print(f"Suppression de {duplicates} lignes dupliquées...")
            df = df.drop_duplicates()
        
        # 8. Vérifier les valeurs aberrantes (outliers)
        print("Vérification des valeurs aberrantes...")
        for col in colonnes_numeriques:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            outliers = ((df[col] < lower_bound) | (df[col] > upper_bound)).sum()
            if outliers > 0:
                print(f"  - {outliers} valeurs aberrantes détectées dans '{col}'")
                # Note: On garde les outliers pour l'instant, mais on peut les traiter si nécessaire
        
        # Afficher des informations sur le dataset nettoyé
        print("\n--- RÉSULTAT DU NETTOYAGE ---")
        print(f"Dimensions finales: {df.shape}")
        print("\nNouvelles colonnes:")
        print(df.columns.tolist())
        print("\nAperçu des données nettoyées:")
        print(df.head())
        
        # Sauvegarder le fichier nettoyé si demandé
        if output_path:
            print(f"\nSauvegarde du dataset nettoyé dans: {output_path}")
            df.to_csv(output_path, index=False)
        
        return df
        
    except Exception as e:
        print(f"Erreur lors du nettoyage des données: {str(e)}")
        return None

# Si exécuté directement
if __name__ == "__main__":
    # Remplacez par le chemin de votre fichier
    fichier_csv = "dataset_marketing_dataviz.csv"
    fichier_nettoye = "dataset_marketing_clean.csv"
    
    # Nettoyer le dataset
    df_clean = nettoyer_dataset(fichier_csv, fichier_nettoye)
    
    if df_clean is not None:
        print("✅ Nettoyage terminé avec succès!")
    else:
        print("❌ Échec du nettoyage des données")
        

