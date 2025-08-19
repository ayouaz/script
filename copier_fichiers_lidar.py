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
import platform

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


def obtenir_espace_disque_disponible(chemin):
    """Retourne l'espace disque disponible en octets pour le chemin spécifié.
    
    Args:
        chemin (str): Chemin du répertoire
        
    Returns:
        int: Espace disque disponible en octets
    """
    if platform.system() == 'Windows':
        import ctypes
        free_bytes = ctypes.c_ulonglong(0)
        ctypes.windll.kernel32.GetDiskFreeSpaceExW(
            ctypes.c_wchar_p(chemin), None, None, ctypes.pointer(free_bytes))
        return free_bytes.value
    else:
        # Pour les systèmes Unix/Linux/MacOS
        st = os.statvfs(chemin)
        return st.f_bavail * st.f_frsize


def calculer_taille_totale_fichiers(fichiers):
    """Calcule la taille totale d'une liste de fichiers.
    
    Args:
        fichiers (list): Liste d'objets Path représentant des fichiers
        
    Returns:
        int: Taille totale en octets
    """
    return sum(fichier.stat().st_size for fichier in fichiers)


def copier_fichiers_lidar(source, destination, recursif=False, verbose=False, sans_progression=False, garde_structure=True, ecraser=False):
    """Copie les fichiers .laz et .las du répertoire source vers le répertoire destination.
    
    Args:
        source (str): Chemin du répertoire source
        destination (str): Chemin du répertoire destination
        recursif (bool): Si True, recherche récursivement dans les sous-répertoires
        verbose (bool): Si True, affiche des informations détaillées pendant la copie
        sans_progression (bool): Si True, désactive la barre de progression même si tqdm est disponible
        garde_structure (bool): Si True, préserve la structure des répertoires lors de la copie
        ecraser (bool): Si True, écrase les fichiers existants sans demander de confirmation
    
    Returns:
        tuple: (nb_fichiers_copies, nb_fichiers_echoues, taille_copiee, temps_ecoule)
    """
    # Convertir les chemins en objets Path
    source_path = Path(source).resolve()
    destination_path = Path(destination).resolve()
    
    # Vérifier si le répertoire source existe
    if not source_path.exists() or not source_path.is_dir():
        print(f"Erreur: Le répertoire source '{source_path}' n'existe pas.")
        return 0, 0, 0, 0
    
    # Créer le répertoire de destination s'il n'existe pas
    if not destination_path.exists():
        try:
            destination_path.mkdir(parents=True, exist_ok=True)
            print(f"Répertoire de destination '{destination_path}' créé avec succès.")
        except Exception as e:
            print(f"Erreur lors de la création du répertoire de destination: {e}")
            return 0, 0, 0, 0
    
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
        return 0, 0, 0, 0
    
    # Calculer la taille totale des fichiers à copier
    taille_totale = calculer_taille_totale_fichiers(fichiers)
    
    # Vérifier l'espace disque disponible
    espace_disponible = obtenir_espace_disque_disponible(str(destination_path))
    
    # Ajouter une marge de sécurité de 10%
    espace_necessaire = int(taille_totale * 1.1)
    
    if espace_disponible < espace_necessaire:
        print(f"Erreur: Espace disque insuffisant dans le répertoire de destination.")
        print(f"  - Espace nécessaire: {afficher_taille_lisible(espace_necessaire)} (incluant une marge de 10%)")
        print(f"  - Espace disponible: {afficher_taille_lisible(espace_disponible)}")
        return 0, 0, 0, 0
    
    if verbose:
        print(f"Espace disque disponible: {afficher_taille_lisible(espace_disponible)}")
        print(f"Taille totale à copier: {afficher_taille_lisible(taille_totale)}")
        print(f"Espace suffisant pour la copie.")

    
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
        if garde_structure:
            # Préserver la structure des répertoires
            chemin_relatif = fichier.relative_to(source_path)
            chemin_destination = destination_path / chemin_relatif
            
            # Créer le répertoire parent dans la destination si nécessaire
            chemin_destination.parent.mkdir(parents=True, exist_ok=True)
            
            # Vérifier si le fichier existe déjà
            if chemin_destination.exists():
                if ecraser:
                    # Écraser sans demander
                    pass
                else:
                    # Demander confirmation pour écraser
                    reponse = ''
                    if TQDM_DISPONIBLE and not sans_progression:
                        fichiers_iter.write(f"Le fichier '{chemin_relatif}' existe déjà dans la destination.")
                        # Pause la barre de progression pour l'interaction utilisateur
                        with fichiers_iter.external_write_mode():
                            reponse = input(f"Voulez-vous écraser '{chemin_relatif}'? (o/n): ").lower()
                    else:
                        print(f"Le fichier '{chemin_relatif}' existe déjà dans la destination.")
                        reponse = input(f"Voulez-vous écraser '{chemin_relatif}'? (o/n): ").lower()
                    
                    if reponse != 'o':
                        if TQDM_DISPONIBLE and not sans_progression:
                            fichiers_iter.write(f"Fichier '{chemin_relatif}' ignoré.")
                        else:
                            print(f"Fichier '{chemin_relatif}' ignoré.")
                        nb_fichiers_echoues += 1
                        continue
        else:
            # Copier directement dans le répertoire de destination sans préserver la structure
            chemin_destination = destination_path / fichier.name
            
            # Vérifier si le fichier existe déjà
            if chemin_destination.exists():
                if ecraser:
                    # Écraser sans demander
                    pass
                else:
                    # Demander confirmation pour écraser
                    reponse = ''
                    if TQDM_DISPONIBLE and not sans_progression:
                        fichiers_iter.write(f"Le fichier '{fichier.name}' existe déjà dans la destination.")
                        # Pause la barre de progression pour l'interaction utilisateur
                        with fichiers_iter.external_write_mode():
                            reponse = input(f"Voulez-vous écraser '{fichier.name}'? (o/n): ").lower()
                    else:
                        print(f"Le fichier '{fichier.name}' existe déjà dans la destination.")
                        reponse = input(f"Voulez-vous écraser '{fichier.name}'? (o/n): ").lower()
                    
                    if reponse != 'o':
                        if TQDM_DISPONIBLE and not sans_progression:
                            fichiers_iter.write(f"Fichier '{fichier.name}' ignoré.")
                        else:
                            print(f"Fichier '{fichier.name}' ignoré.")
                        nb_fichiers_echoues += 1
                        continue
        
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
    parser.add_argument("-gs", "--garde-structure", action="store_true", 
                        help="Préserve la structure des répertoires lors de la copie (activé par défaut)")
    parser.add_argument("-ps", "--pas-structure", action="store_true", 
                        help="Ne préserve pas la structure des répertoires (copie tous les fichiers directement dans le répertoire de destination)")
    parser.add_argument("-e", "--ecraser", action="store_true", 
                        help="Écrase les fichiers existants sans demander de confirmation")
    
    # Analyser les arguments
    args = parser.parse_args()
    
    # Déterminer si on garde la structure des répertoires
    # Par défaut, on garde la structure sauf si --pas-structure est spécifié
    garde_structure = not args.pas_structure
    
    # Si les deux options contradictoires sont spécifiées, afficher un avertissement
    if args.garde_structure and args.pas_structure:
        print("Attention: Les options --garde-structure et --pas-structure sont toutes les deux spécifiées.")
        print("L'option --pas-structure sera prioritaire.")
    
    # Exécuter la copie
    nb_fichiers_copies, nb_fichiers_echoues, taille_copiee, temps_ecoule = copier_fichiers_lidar(
        args.source, args.destination, args.recursif, args.verbose, args.sans_progression, garde_structure, args.ecraser
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