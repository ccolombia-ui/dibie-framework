@echo off
REM Instrucciones para crear el enlace simbólico a Google Drive
REM Este script debe ejecutarse como Administrador

echo ============================================================
echo DIBIE - Configuración del Enlace Simbólico a Google Drive
echo ============================================================
echo.
echo IMPORTANTE: Este script debe ejecutarse como Administrador
echo.
echo Presione Ctrl+C para cancelar si no tiene permisos de administrador
echo Presione cualquier tecla para continuar...
pause > nul

echo.
echo Creando enlace simbólico...
mklink /D "c:\aguila\dibie\data\google_drive" "G:\.shortcut-targets-by-id\1fENbpuTdON265HSA0icoN8nHYS4gWJHF\_rafEl\aktriel\10_calidad_educativa_ud"

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ============================================================
    echo Enlace simbólico creado exitosamente!
    echo ============================================================
) else (
    echo.
    echo ============================================================
    echo ERROR: No se pudo crear el enlace simbólico
    echo Asegúrese de ejecutar este script como Administrador
    echo ============================================================
)

echo.
pause
