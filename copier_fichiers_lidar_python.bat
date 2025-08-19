@echo off
setlocal enabledelayedexpansion

rem Script batch pour lancer le script Python de copie des fichiers LiDAR

echo Copie de fichiers LiDAR (.laz et .las) - Version Python
echo ================================================
echo.

set "params="

if "%~1"=="" (
    echo Ce script permet de copier des fichiers .laz et .las d'un repertoire source vers un repertoire de destination.
    echo.
    echo Usage: %~nx0 [options]
    echo.
    echo Options:
    echo   /source:CHEMIN      Repertoire source contenant les fichiers .laz et .las
    echo   /dest:CHEMIN        Repertoire de destination pour la copie
    echo   /r                  Recherche recursive dans les sous-repertoires
    echo   /v                  Mode verbose (affiche plus d'informations)
    echo   /np                 Desactive la barre de progression
    echo   /gs                 Preserve la structure des repertoires (active par defaut)
    echo   /ps                 Ne preserve pas la structure des repertoires
    echo   /e                  Ecrase les fichiers existants sans demander de confirmation
    echo   /aide               Affiche cette aide
    echo.
    echo Exemple: %~nx0 /source:"C:\Donnees\LiDAR" /dest:"D:\Sauvegarde\LiDAR" /r
    echo.
    goto :EOF
)

rem Traitement des paramètres
:parse_params
if "%~1"=="" goto check_python

set "param=%~1"
set "param=!param:/=-!"

if /i "!param:~0,8!"=="-source:" (
    set "source=!param:~8!"
    set "params=!params! --source "!source!""
) else if /i "!param:~0,6!"=="-dest:" (
    set "dest=!param:~6!"
    set "params=!params! --destination "!dest!""
) else if /i "!param!"=="-r" (
    set "params=!params! --recursif"
) else if /i "!param!"=="-v" (
    set "params=!params! --verbose"
) else if /i "!param!"=="-np" (
    set "params=!params! --sans-progression"
) else if /i "!param!"=="-gs" (
    set "params=!params! --garde-structure"
) else if /i "!param!"=="-ps" (
    set "params=!params! --pas-structure"
) else if /i "!param!"=="-e" (
    set "params=!params! --ecraser"
) else if /i "!param!"=="-aide" (
    echo Ce script permet de copier des fichiers .laz et .las d'un repertoire source vers un repertoire de destination.
    echo.
    echo Usage: %~nx0 [options]
    echo.
    echo Options:
    echo   /source:CHEMIN      Repertoire source contenant les fichiers .laz et .las
    echo   /dest:CHEMIN        Repertoire de destination pour la copie
    echo   /r                  Recherche recursive dans les sous-repertoires
    echo   /v                  Mode verbose (affiche plus d'informations)
    echo   /np                 Desactive la barre de progression
    echo   /gs                 Preserve la structure des repertoires (active par defaut)
    echo   /ps                 Ne preserve pas la structure des repertoires
    echo   /e                  Ecrase les fichiers existants sans demander de confirmation
    echo   /aide               Affiche cette aide
    echo.
    echo Exemple: %~nx0 /source:"C:\Donnees\LiDAR" /dest:"D:\Sauvegarde\LiDAR" /r
    echo.
    goto :EOF
) else (
    echo Parametre inconnu: %~1
    echo Utilisez %~nx0 /aide pour afficher l'aide
    goto :EOF
)

shift
goto parse_params

:check_python
rem Vérifier si Python est disponible
where python >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo ERREUR: Python n'est pas disponible sur ce systeme ou n'est pas dans le PATH.
    echo Ce script necessite Python pour fonctionner.
    echo Veuillez installer Python depuis https://www.python.org/downloads/
    exit /b 1
)

rem Exécuter le script Python
echo Execution du script Python avec les parametres suivants: !params!
echo.

python "%~dp0copier_fichiers_lidar.py" !params!

if %ERRORLEVEL% neq 0 (
    echo.
    echo ATTENTION: Le script s'est termine avec des erreurs.
    exit /b %ERRORLEVEL%
) else (
    echo.
    echo Le script s'est execute avec succes.
    exit /b 0
)