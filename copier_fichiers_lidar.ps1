# Script PowerShell pour copier les fichiers .laz et .las d'un répertoire source vers un répertoire de destination

# Fonction pour afficher l'aide
function Afficher-Aide {
    Write-Host "Usage: .\copier_fichiers_lidar.ps1 -Source <chemin_source> -Destination <chemin_destination> [-Recursif] [-Verbose]"
    Write-Host ""
    Write-Host "Options:"
    Write-Host "  -Source        : Chemin du répertoire source contenant les fichiers .laz et .las"
    Write-Host "  -Destination   : Chemin du répertoire de destination où copier les fichiers"
    Write-Host "  -Recursif      : Recherche récursivement dans les sous-répertoires (optionnel)"
    Write-Host "  -Verbose       : Affiche des informations détaillées pendant la copie (optionnel)"
    Write-Host ""
    Write-Host "Exemple: .\copier_fichiers_lidar.ps1 -Source 'C:\Donnees\LiDAR' -Destination 'D:\Sauvegarde\LiDAR' -Recursif"
    exit
}

# Paramètres du script
param(
    [Parameter(Mandatory=$false)]
    [string]$Source,
    
    [Parameter(Mandatory=$false)]
    [string]$Destination,
    
    [Parameter(Mandatory=$false)]
    [switch]$Recursif,
    
    [Parameter(Mandatory=$false)]
    [switch]$Aide
)

# Afficher l'aide si demandé ou si les paramètres obligatoires sont manquants
if ($Aide -or [string]::IsNullOrEmpty($Source) -or [string]::IsNullOrEmpty($Destination)) {
    Afficher-Aide
}

# Vérifier si le répertoire source existe
if (-not (Test-Path -Path $Source -PathType Container)) {
    Write-Error "Le répertoire source '$Source' n'existe pas."
    exit 1
}

# Créer le répertoire de destination s'il n'existe pas
if (-not (Test-Path -Path $Destination -PathType Container)) {
    try {
        New-Item -Path $Destination -ItemType Directory -Force | Out-Null
        Write-Host "Répertoire de destination '$Destination' créé avec succès."
    }
    catch {
        Write-Error "Impossible de créer le répertoire de destination '$Destination': $_"
        exit 1
    }
}

# Définir les options de recherche pour Get-ChildItem
$getChildItemParams = @{
    Path = $Source
    Include = @("*.laz", "*.las")
    File = $true
}

# Ajouter l'option récursive si spécifiée
if ($Recursif) {
    $getChildItemParams.Add("Recurse", $true)
}

# Rechercher les fichiers .laz et .las
try {
    $fichiers = Get-ChildItem @getChildItemParams
}
catch {
    Write-Error "Erreur lors de la recherche des fichiers: $_"
    exit 1
}

# Vérifier si des fichiers ont été trouvés
if ($fichiers.Count -eq 0) {
    Write-Warning "Aucun fichier .laz ou .las trouvé dans le répertoire source."
    exit 0
}

# Compteurs pour les statistiques
$nbFichiersCopies = 0
$nbFichiersEchoues = 0
$tailleCopiee = 0

# Copier les fichiers
Write-Host "Début de la copie de $($fichiers.Count) fichiers..."

foreach ($fichier in $fichiers) {
    # Déterminer le chemin de destination
    $cheminRelatif = $fichier.FullName.Substring($Source.Length).TrimStart('\')
    $cheminDestination = Join-Path -Path $Destination -ChildPath $cheminRelatif
    
    # Créer le répertoire parent dans la destination si nécessaire
    $repertoireParent = Split-Path -Path $cheminDestination -Parent
    if (-not (Test-Path -Path $repertoireParent -PathType Container)) {
        try {
            New-Item -Path $repertoireParent -ItemType Directory -Force | Out-Null
            if ($VerbosePreference -eq 'Continue') {
                Write-Verbose "Répertoire créé: $repertoireParent"
            }
        }
        catch {
            Write-Error "Impossible de créer le répertoire '$repertoireParent': $_"
            $nbFichiersEchoues++
            continue
        }
    }
    
    # Copier le fichier
    try {
        Copy-Item -Path $fichier.FullName -Destination $cheminDestination -Force
        $nbFichiersCopies++
        $tailleCopiee += $fichier.Length
        
        if ($VerbosePreference -eq 'Continue') {
            Write-Verbose "Copié: $($fichier.FullName) -> $cheminDestination"
        }
    }
    catch {
        Write-Error "Erreur lors de la copie de '$($fichier.FullName)': $_"
        $nbFichiersEchoues++
    }
}

# Afficher les statistiques
Write-Host ""
Write-Host "Opération terminée avec les résultats suivants:"
Write-Host "  - Fichiers copiés avec succès: $nbFichiersCopies"
Write-Host "  - Fichiers en échec: $nbFichiersEchoues"
Write-Host "  - Taille totale copiée: $([math]::Round($tailleCopiee / 1MB, 2)) MB"

# Sortir avec un code d'erreur si des fichiers ont échoué
if ($nbFichiersEchoues -gt 0) {
    exit 1
}
else {
    exit 0
}