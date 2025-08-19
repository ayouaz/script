@echo off
setlocal enabledelayedexpansion

rem Script batch pour lancer le script PowerShell de copie des fichiers LiDAR

echo Copie de fichiers LiDAR (.laz et .las)
echo =====================================
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
    echo   /aide               Affiche cette aide
    echo.
    echo Exemple: %~nx0 /source:"C:\Donnees\LiDAR" /dest:"D:\Sauvegarde\LiDAR" /r
    echo.
    goto :EOF
)

rem Traitement des paramètres
:parse_params
if "%~1"=="" goto run_script

set "param=%~1"
set "param=!param:/=-!"

if /i "!param:~0,8!"=="-source:" (
    set "source=!param:~8!"
    set "params=!params! -Source '!source!'"
) else if /i "!param:~0,6!"=="-dest:" (
    set "dest=!param:~6!"
    set "params=!params! -Destination '!dest!'"
) else if /i "!param!"=="-r" (
    set "params=!params! -Recursif"
) else if /i "!param!"=="-v" (
    set "params=!params! -Verbose"
) else if /i "!param!"=="-aide" (
    set "params=!params! -Aide"
) else (
    echo Parametre inconnu: %~1
    echo Utilisez %~nx0 /aide pour afficher l'aide
    goto :EOF
)

shift
goto parse_params

:run_script
rem Vérifier si PowerShell est disponible
where powershell >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo ERREUR: PowerShell n'est pas disponible sur ce systeme.
    echo Ce script necessite PowerShell pour fonctionner.
    exit /b 1
)

rem Exécuter le script PowerShell
echo Execution du script PowerShell avec les parametres suivants: !params!
echo.

powershell -ExecutionPolicy Bypass -File "%~dp0copier_fichiers_lidar.ps1" !params!

if %ERRORLEVEL% neq 0 (
    echo.
    echo ATTENTION: Le script s'est termine avec des erreurs.
    exit /b %ERRORLEVEL%
) else (
    echo.
    echo Le script s'est execute avec succes.
    exit /b 0
)