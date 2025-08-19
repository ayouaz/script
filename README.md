# Utilitaire de Copie de Fichiers LiDAR

Cet utilitaire permet de copier facilement des fichiers LiDAR (avec extensions `.laz` et `.las`) d'un répertoire source vers un répertoire de destination.

## Contenu

### Version PowerShell
- `copier_fichiers_lidar.ps1` : Script PowerShell principal
- `copier_fichiers_lidar.bat` : Script batch pour faciliter l'exécution sous Windows

### Version Python
- `copier_fichiers_lidar.py` : Script Python principal
- `copier_fichiers_lidar_python.bat` : Script batch pour faciliter l'exécution sous Windows

## Fonctionnalités

- Copie des fichiers avec extensions `.laz` et `.las`
- Option de recherche récursive dans les sous-répertoires
- Option de préservation ou non de la structure des dossiers lors de la copie
- Confirmation avant écrasement des fichiers existants (avec option pour désactiver)
- Création automatique des répertoires de destination si nécessaire
- Statistiques détaillées après la copie (nombre de fichiers, taille totale)
- Version Python : Barre de progression pendant la copie (via la bibliothèque tqdm)
- Version Python : Vérification de l'espace disque disponible avant la copie

### Préservation de la structure des répertoires

Par défaut, le script préserve la structure des répertoires lors de la copie. Cela signifie que si un fichier se trouve dans un sous-répertoire du répertoire source, il sera copié dans le même sous-répertoire relatif dans le répertoire de destination.

Vous pouvez désactiver ce comportement en utilisant l'option `/ps` (version batch) ou `--pas-structure` (version Python). Dans ce cas, tous les fichiers seront copiés directement dans le répertoire de destination, sans tenir compte de leur emplacement d'origine.

### Gestion des fichiers existants

Par défaut, lorsqu'un fichier à copier existe déjà dans le répertoire de destination, le script demande à l'utilisateur s'il souhaite écraser le fichier existant. L'utilisateur peut répondre 'o' pour écraser ou toute autre touche pour ignorer le fichier.

Vous pouvez désactiver cette confirmation et écraser automatiquement tous les fichiers existants en utilisant l'option `/e` (version batch) ou `--ecraser` (version Python).

## Utilisation

## Version PowerShell

### Via le script batch (recommandé pour les utilisateurs Windows)

```
copier_fichiers_lidar.bat /source:"C:\Chemin\Source" /dest:"D:\Chemin\Destination" [/r] [/v]
```

Options :
- `/source:CHEMIN` : Répertoire source contenant les fichiers .laz et .las
- `/dest:CHEMIN` : Répertoire de destination pour la copie
- `/r` : Recherche récursive dans les sous-répertoires (optionnel)
- `/v` : Mode verbose - affiche plus d'informations pendant la copie (optionnel)
- `/np` : Désactive la barre de progression (optionnel)
- `/gs` : Préserve la structure des répertoires (activé par défaut)
- `/ps` : Ne préserve pas la structure des répertoires (copie tous les fichiers directement dans le répertoire de destination)
- `/e` : Écrase les fichiers existants sans demander de confirmation (optionnel)
- `/aide` : Affiche l'aide

### Via PowerShell directement

```powershell
.\copier_fichiers_lidar.ps1 -Source "C:\Chemin\Source" -Destination "D:\Chemin\Destination" [-Recursif] [-Verbose]
```

Options :
- `-Source` : Chemin du répertoire source contenant les fichiers .laz et .las
- `-Destination` : Chemin du répertoire de destination où copier les fichiers
- `-Recursif` : Recherche récursivement dans les sous-répertoires (optionnel)
- `-Verbose` : Affiche des informations détaillées pendant la copie (optionnel)
- `-Aide` : Affiche l'aide

## Version Python

### Via le script batch (recommandé pour les utilisateurs Windows)

```
copier_fichiers_lidar_python.bat /source:"C:\Chemin\Source" /dest:"D:\Chemin\Destination" [/r] [/v]
```

Options :
- `/source:CHEMIN` : Répertoire source contenant les fichiers .laz et .las
- `/dest:CHEMIN` : Répertoire de destination pour la copie
- `/r` : Recherche récursive dans les sous-répertoires (optionnel)
- `/v` : Mode verbose - affiche plus d'informations pendant la copie (optionnel)
- `/aide` : Affiche l'aide

### Via Python directement

```
python copier_fichiers_lidar.py --source "C:\Chemin\Source" --destination "D:\Chemin\Destination" [--recursif] [--verbose]
```

Options :
- `--source` ou `-s` : Chemin du répertoire source contenant les fichiers .laz et .las
- `--destination` ou `-d` : Chemin du répertoire de destination où copier les fichiers
- `--recursif` ou `-r` : Recherche récursivement dans les sous-répertoires (optionnel)
- `--verbose` ou `-v` : Affiche des informations détaillées pendant la copie (optionnel)
- `--sans-progression` ou `-np` : Désactive la barre de progression (optionnel)
- `--garde-structure` ou `-gs` : Préserve la structure des répertoires (activé par défaut)
- `--pas-structure` ou `-ps` : Ne préserve pas la structure des répertoires (copie tous les fichiers directement dans le répertoire de destination)
- `--ecraser` ou `-e` : Écrase les fichiers existants sans demander de confirmation (optionnel)

## Exemples

### Version PowerShell

#### Exemple 1 : Copie simple

```
copier_fichiers_lidar.bat /source:"C:\Donnees\LiDAR" /dest:"D:\Sauvegarde\LiDAR"
```

#### Exemple 2 : Copie récursive avec mode verbose

```
copier_fichiers_lidar.bat /source:"C:\Donnees\LiDAR" /dest:"D:\Sauvegarde\LiDAR" /r /v
```

#### Exemple 3 : Utilisation directe du script PowerShell

```powershell
.\copier_fichiers_lidar.ps1 -Source "C:\Donnees\LiDAR" -Destination "D:\Sauvegarde\LiDAR" -Recursif
```

### Version Python

#### Exemple 1 : Copie simple

```
copier_fichiers_lidar_python.bat /source:"C:\Donnees\LiDAR" /dest:"D:\Sauvegarde\LiDAR"
```

#### Exemple 2 : Copie récursive avec mode verbose

```
copier_fichiers_lidar_python.bat /source:"C:\Donnees\LiDAR" /dest:"D:\Sauvegarde\LiDAR" /r /v
```

#### Exemple 3 : Utilisation directe du script Python

```
python copier_fichiers_lidar.py --source "C:\Donnees\LiDAR" --destination "D:\Sauvegarde\LiDAR" --recursif
```

#### Exemple 4 : Copie récursive sans barre de progression

```
copier_fichiers_lidar_python.bat /source:"C:\Donnees\LiDAR" /dest:"D:\Sauvegarde\LiDAR" /r /np
```

#### Exemple 5 : Copie sans préservation de la structure des répertoires

```
copier_fichiers_lidar_python.bat /source:"C:\Donnees\LiDAR" /dest:"D:\Sauvegarde\LiDAR" /r /ps
```

Cette commande copie tous les fichiers .laz et .las du répertoire C:\Donnees\LiDAR et ses sous-répertoires vers D:\Sauvegarde\LiDAR, sans préserver la structure des répertoires (tous les fichiers seront copiés directement dans le répertoire de destination).

#### Exemple 6 : Copie avec écrasement automatique des fichiers existants

```
copier_fichiers_lidar_python.bat /source:"C:\Donnees\LiDAR" /dest:"D:\Sauvegarde\LiDAR" /r /e
```

Cette commande copie tous les fichiers .laz et .las du répertoire C:\Donnees\LiDAR et ses sous-répertoires vers D:\Sauvegarde\LiDAR, en écrasant automatiquement les fichiers existants sans demander de confirmation.

## Remarques

- Le script préserve la structure des dossiers lors de la copie récursive
- Les statistiques affichées à la fin incluent le nombre de fichiers copiés et la taille totale
- En cas d'erreur lors de la copie d'un fichier, le script continue avec les fichiers suivants
- La version Python utilise la bibliothèque tqdm pour afficher une barre de progression
  - Si tqdm n'est pas installée, le script fonctionnera quand même mais sans barre de progression
  - Pour installer tqdm : `pip install tqdm`
- La version Python vérifie l'espace disque disponible avant de commencer la copie
  - Une marge de sécurité de 10% est ajoutée à la taille totale des fichiers
  - Si l'espace est insuffisant, le script s'arrête et affiche un message d'erreur