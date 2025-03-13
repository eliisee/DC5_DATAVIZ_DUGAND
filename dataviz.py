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

# Avez-vous le fichier source dataset_marketing_dataviz.csv?
fichier_source = "dataset_marketing_dataviz.csv"

# Vérifier si le fichier source existe
if os.path.exists(fichier_source):
    print(f"Chargement du fichier source: {fichier_source}")
    
    # Nettoyer les données
    df = pd.read_csv(fichier_source)
    
    # Convertir la colonne Date en datetime
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Traiter les valeurs manquantes
    for col in ['Impressions', 'Clics', 'Conversions', 'Coût']:
        if df[col].isnull().sum() > 0:
            median_value = df[col].median()
            df[col] = df[col].fillna(median_value)
    
    # Supprimer la colonne inutile si elle existe
    if 'Inutile' in df.columns:
        df = df.drop('Inutile', axis=1)
    
    print("Données nettoyées avec succès")
    
    # Créer le dossier pour les visualisations
    if not os.path.exists('visualisations'):
        os.makedirs('visualisations')
        print("Dossier 'visualisations' créé")
    
    # Créer l'histogramme
    print("Création de l'histogramme des impressions par campagne...")
    
    # Regrouper les données par campagne et sommer les impressions
    impressions_par_campagne = df.groupby('Campagne')['Impressions'].sum().sort_values(ascending=False)
    
    # Créer la figure
    plt.figure(figsize=(14, 10))
    
    # Créer une palette de couleurs dégradée
    colors = sns.color_palette("viridis", len(impressions_par_campagne))
    
    # Créer le graphique
    ax = sns.barplot(x=impressions_par_campagne.index, y=impressions_par_campagne.values, palette=colors)
    
    # Ajouter les titres et labels
    plt.title('Histogramme des impressions par campagne', fontsize=20, pad=20)
    plt.xlabel('Campagne', fontsize=16, labelpad=10)
    plt.ylabel('Nombre total d\'impressions', fontsize=16, labelpad=10)
    
    # Rotation des étiquettes de l'axe x
    plt.xticks(rotation=45, ha='right', fontsize=12)
    
    # Ajouter une grille
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Ajouter les valeurs sur les barres
    for i, v in enumerate(impressions_par_campagne.values):
        ax.text(i, v + v*0.01, f'{v:,.0f}', ha='center', fontsize=12)
    
    # Améliorer le layout
    plt.tight_layout()
    
    # Sauvegarder l'image
    save_path = 'visualisations/histogramme_impressions.png'
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"Histogramme sauvegardé: {save_path}")
    plt.close()
    
    print("Histogramme des impressions par campagne créé avec succès!")
else:
    print(f"Erreur: Le fichier source {fichier_source} n'existe pas.")
    print("Assurez-vous que le fichier CSV est bien dans le même dossier que ce script.")