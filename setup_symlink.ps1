# Instrucciones para crear el enlace simbólico a Google Drive
# Este script debe ejecutarse como Administrador en PowerShell

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "DIBIE - Configuración del Enlace Simbólico a Google Drive" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Verificar permisos de administrador
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "ERROR: Este script requiere permisos de Administrador" -ForegroundColor Red
    Write-Host "Por favor, ejecute PowerShell como Administrador y vuelva a intentar" -ForegroundColor Yellow
    Write-Host ""
    pause
    exit
}

Write-Host "Creando enlace simbólico..." -ForegroundColor Yellow

$target = "G:\.shortcut-targets-by-id\1fENbpuTdON265HSA0icoN8nHYS4gWJHF\_rafEl\aktriel\10_calidad_educativa_ud"
$link = "c:\aguila\dibie\data\google_drive"

# Verificar si el directorio destino existe
if (Test-Path $target) {
    Write-Host "✓ Directorio de Google Drive encontrado" -ForegroundColor Green
    
    # Verificar si el enlace ya existe
    if (Test-Path $link) {
        Write-Host "! El enlace simbólico ya existe" -ForegroundColor Yellow
        $response = Read-Host "¿Desea recrearlo? (S/N)"
        if ($response -eq "S" -or $response -eq "s") {
            Remove-Item $link -Force
        } else {
            Write-Host "Operación cancelada" -ForegroundColor Yellow
            pause
            exit
        }
    }
    
    # Crear el enlace simbólico
    New-Item -ItemType SymbolicLink -Path $link -Target $target
    
    if ($?) {
        Write-Host ""
        Write-Host "============================================================" -ForegroundColor Green
        Write-Host "✓ Enlace simbólico creado exitosamente!" -ForegroundColor Green
        Write-Host "============================================================" -ForegroundColor Green
        Write-Host "Ruta: $link" -ForegroundColor Cyan
        Write-Host "Apunta a: $target" -ForegroundColor Cyan
    } else {
        Write-Host ""
        Write-Host "============================================================" -ForegroundColor Red
        Write-Host "✗ ERROR: No se pudo crear el enlace simbólico" -ForegroundColor Red
        Write-Host "============================================================" -ForegroundColor Red
    }
} else {
    Write-Host ""
    Write-Host "============================================================" -ForegroundColor Red
    Write-Host "✗ ERROR: El directorio de Google Drive no existe" -ForegroundColor Red
    Write-Host "============================================================" -ForegroundColor Red
    Write-Host "Ruta esperada: $target" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Asegúrese de que Google Drive esté sincronizado correctamente" -ForegroundColor Yellow
}

Write-Host ""
pause
