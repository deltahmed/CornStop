@echo off

set "batch_path=%~dp0"
set "program_name=shut_p.exe"
set "startup_folder=%AppData%\Microsoft\Windows\Start Menu\Programs\Startup"
set "program_path=%startup_folder%\%program_name%"

if exist "%program_path%" (
    del %program_path%
    echo ancien programme delete reussi
)

move "%batch_path%%program_name%" "%startup_folder%\%program_name%"


if exist "%program_path%" (
    echo Installation reussie.
) else (
    echo Problème !!!!.
    pause
)

pause
