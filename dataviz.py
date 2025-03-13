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

    # Créer le graphique d'évolution des clics au fil du temps
print("Création du graphique d'évolution des clics au fil du temps...")

# Importer la bibliothèque pour formater les dates
import matplotlib.dates as mdates

# Regrouper les données par jour et sommer les clics
df_daily = df.groupby(df['Date'].dt.date).agg({'Clics': 'sum'}).reset_index()

# Créer la figure
plt.figure(figsize=(16, 8))

# Créer le graphique
plt.plot(df_daily['Date'], df_daily['Clics'], marker='o', linestyle='-', 
         color='#1f77b4', linewidth=2, markersize=8)

# Ajouter les titres et labels
plt.title('Évolution des clics au fil du temps', fontsize=20, pad=20)
plt.xlabel('Date', fontsize=16, labelpad=10)
plt.ylabel('Nombre de clics', fontsize=16, labelpad=10)

# Configurer l'axe des dates
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=2))  # Ajuster l'intervalle selon vos données
plt.xticks(rotation=45, ha='right', fontsize=12)

# Ajouter une grille
plt.grid(True, linestyle='--', alpha=0.7)

# Ajouter une ligne de tendance
z = np.polyfit(range(len(df_daily['Date'])), df_daily['Clics'], 1)
p = np.poly1d(z)
plt.plot(df_daily['Date'], p(range(len(df_daily['Date']))), "r--", linewidth=2, 
         label=f'Tendance: {z[0]:.2f}x + {z[1]:.2f}')

# Ajouter une légende
plt.legend(fontsize=12)

# Améliorer le layout
plt.tight_layout()

# Sauvegarder l'image
save_path = 'visualisations/evolution_clics.png'
plt.savefig(save_path, dpi=300, bbox_inches='tight')
print(f"Graphique d'évolution sauvegardé: {save_path}")
plt.close()

print("Graphique d'évolution des clics au fil du temps créé avec succès!")