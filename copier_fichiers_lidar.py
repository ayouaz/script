#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script pour copier les fichiers .laz et .las d'un répertoire source vers un répertoire de destination.

Ce script permet de copier tous les fichiers avec extension .laz ou .las d'un répertoire
source vers un répertoire de destination, avec option de recherche récursive.
"""

import os
import sys
import shutil
import argparse
from pathlib import Path
import time

try:
    from tqdm import tqdm
    TQDM_DISPONIBLE = True
except ImportError:
    TQDM_DISPONIBLE = False
    print("Info: La bibliothèque tqdm n'est pas installée. La barre de progression ne sera pas disponible.")
    print("Pour l'installer, exécutez: pip install tqdm")
    print()


def afficher_taille_lisible(taille_octets):
    """Convertit une taille en octets en format lisible (Ko, Mo, Go)."""
    suffixes = ['o', 'Ko', 'Mo', 'Go', 'To']
    indice = 0
    taille = float(taille_octets)
    while taille >= 1024 and indice < len(suffixes) - 1:
        taille /= 1024.0
        indice += 1
    return f"{taille:.2f} {suffixes[indice]}"


def copier_fichiers_lidar(source, destination, recursif=False, verbose=False, sans_progression=False):
    """Copie les fichiers .laz et .las du répertoire source vers le répertoire destination.
    
    Args:
        source (str): Chemin du répertoire source
        destination (str): Chemin du répertoire destination
        recursif (bool): Si True, recherche récursivement dans les sous-répertoires
        verbose (bool): Si True, affiche des informations détaillées pendant la copie
        sans_progression (bool): Si True, désactive la barre de progression même si tqdm est disponible
    
    Returns:
        tuple: (nb_fichiers_copies, nb_fichiers_echoues, taille_copiee, temps_ecoule)
    """
    # Convertir les chemins en objets Path
    source_path = Path(source).resolve()
    destination_path = Path(destination).resolve()
    
    # Vérifier si le répertoire source existe
    if not source_path.exists() or not source_path.is_dir():
        print(f"Erreur: Le répertoire source '{source_path}' n'existe pas.")
        return 0, 0, 0
    
    # Créer le répertoire de destination s'il n'existe pas
    if not destination_path.exists():
        try:
            destination_path.mkdir(parents=True, exist_ok=True)
            print(f"Répertoire de destination '{destination_path}' créé avec succès.")
        except Exception as e:
            print(f"Erreur lors de la création du répertoire de destination: {e}")
            return 0, 0, 0
    
    # Compteurs pour les statistiques
    nb_fichiers_copies = 0
    nb_fichiers_echoues = 0
    taille_copiee = 0
    
    # Rechercher les fichiers .laz et .las
    pattern = "**/*.la[sz]" if recursif else "*.la[sz]"
    fichiers = list(source_path.glob(pattern))
    
    # Vérifier si des fichiers ont été trouvés
    if not fichiers:
        print("Aucun fichier .laz ou .las trouvé dans le répertoire source.")
        return 0, 0, 0
    
    print(f"Début de la copie de {len(fichiers)} fichiers...")
    debut_temps = time.time()
    
    # Préparer l'itérateur avec ou sans barre de progression
    if TQDM_DISPONIBLE and not sans_progression:
        # Utiliser tqdm pour afficher une barre de progression
        fichiers_iter = tqdm(
            fichiers,
            desc="Copie en cours",
            unit="fichier",
            ncols=100,
            bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]"
        )
    else:
        fichiers_iter = fichiers
    
    # Copier les fichiers
    for fichier in fichiers_iter:
        # Déterminer le chemin relatif par rapport au répertoire source
        chemin_relatif = fichier.relative_to(source_path)
        chemin_destination = destination_path / chemin_relatif
        
        # Créer le répertoire parent dans la destination si nécessaire
        chemin_destination.parent.mkdir(parents=True, exist_ok=True)
        
        # Copier le fichier
        try:
            shutil.copy2(fichier, chemin_destination)
            taille_fichier = fichier.stat().st_size
            taille_copiee += taille_fichier
            nb_fichiers_copies += 1
            
            # Mettre à jour la description de la barre de progression si tqdm est disponible et utilisé
            if TQDM_DISPONIBLE and not sans_progression and verbose:
                fichiers_iter.set_postfix({
                    "fichier": fichier.name,
                    "taille": afficher_taille_lisible(taille_fichier)
                }, refresh=True)
            elif verbose:
                print(f"Copié: {fichier} -> {chemin_destination} ({afficher_taille_lisible(taille_fichier)})")
        except Exception as e:
            if TQDM_DISPONIBLE and not sans_progression:
                fichiers_iter.write(f"Erreur lors de la copie de '{fichier}': {e}")
            else:
                print(f"Erreur lors de la copie de '{fichier}': {e}")
            nb_fichiers_echoues += 1
    
    temps_ecoule = time.time() - debut_temps
    
    return nb_fichiers_copies, nb_fichiers_echoues, taille_copiee, temps_ecoule


def main():
    # Configurer l'analyseur d'arguments
    parser = argparse.ArgumentParser(
        description="Copie les fichiers .laz et .las d'un répertoire source vers un répertoire destination.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    parser.add_argument("-s", "--source", required=True, 
                        help="Chemin du répertoire source contenant les fichiers .laz et .las")
    parser.add_argument("-d", "--destination", required=True, 
                        help="Chemin du répertoire de destination où copier les fichiers")
    parser.add_argument("-r", "--recursif", action="store_true", 
                        help="Recherche récursivement dans les sous-répertoires")
    parser.add_argument("-v", "--verbose", action="store_true", 
                        help="Affiche des informations détaillées pendant la copie")
    parser.add_argument("-np", "--sans-progression", action="store_true", 
                        help="Désactive la barre de progression (même si tqdm est disponible)")
    
    # Analyser les arguments
    args = parser.parse_args()
    
    # Exécuter la copie
    nb_fichiers_copies, nb_fichiers_echoues, taille_copiee, temps_ecoule = copier_fichiers_lidar(
        args.source, args.destination, args.recursif, args.verbose, args.sans_progression
    )
    
    # Afficher les statistiques
    print("\nOpération terminée avec les résultats suivants:")
    print(f"  - Fichiers copiés avec succès: {nb_fichiers_copies}")
    print(f"  - Fichiers en échec: {nb_fichiers_echoues}")
    print(f"  - Taille totale copiée: {afficher_taille_lisible(taille_copiee)}")
    print(f"  - Temps écoulé: {temps_ecoule:.2f} secondes")
    
    # Sortir avec un code d'erreur si des fichiers ont échoué
    if nb_fichiers_echoues > 0:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()