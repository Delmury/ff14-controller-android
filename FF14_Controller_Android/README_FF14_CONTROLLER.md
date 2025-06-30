# FF14 Controller para Android

## Descripción
Aplicación para tableta Android que funciona como un teclado virtual especializado para Final Fantasy XIV, con:
- Números 1-9, 0, -, =
- Teclas de función F1-F12
- Controles mapeados de PS5
- Conexión WiFi con tu PC

## Archivos del Proyecto

### Para Android (Tableta)
- `ff14_controller_app.py` - Aplicación principal para Android
- `main.py` - Punto de entrada para Buildozer
- `buildozer.spec` - Configuración de compilación Android
- `requirements_ff14_android.txt` - Dependencias

### Para PC (Servidor)
- `ff14_server_pc.py` - Servidor que recibe comandos de la tableta

## Instalación

### 1. Compilar la App Android

#### Opción A: En Windows con WSL2
```bash
# Instalar WSL2 y Ubuntu
wsl --install -d Ubuntu

# En Ubuntu/WSL2:
sudo apt update
sudo apt install -y git zip unzip openjdk-8-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev

# Instalar Buildozer
pip3 install buildozer cython

# Compilar la app
cd /mnt/c/Users/angel/OneDrive/Desktop/Simulation
buildozer android debug
```

#### Opción B: Usar GitHub Actions (Recomendado)
1. Sube los archivos a un repositorio GitHub
2. Usa el workflow de GitHub Actions para compilar
3. Descarga el APK generado

### 2. Instalar en PC (Servidor)
```bash
# Instalar dependencias
pip install keyboard mouse pynput tkinter

# Ejecutar servidor
python ff14_server_pc.py
```

## Uso

### 1. Configurar el Servidor PC
1. Ejecuta `ff14_server_pc.py` en tu PC
2. Haz clic en "Iniciar Servidor"
3. Anota la IP local que se muestra

### 2. Configurar la Tableta Android
1. Instala el APK generado en tu tableta
2. Conecta la tableta a la misma red WiFi que tu PC
3. Abre la app FF14 Controller
4. Ve a la pestaña "Config"
5. Ingresa la IP de tu PC
6. Presiona "Conectar al PC"

### 3. Usar los Controles
- **Números**: Pestaña "Números" para 1-9, 0, -, =
- **Teclas F**: Pestaña "Teclas F" para F1-F12
- **Controles PS5**: Pestaña "PS5 Controls" para botones mapeados

## Mapeo de Controles PS5 para FF14

| Botón PS5 | Tecla PC | Función FF14 |
|-----------|----------|--------------|
| X | Enter | Confirmar |
| O | Esc | Cancelar |
| □ | I | Inventario |
| △ | Space | Saltar |
| L1 | Q | Skill |
| R1 | E | Skill |
| L2 | Tab | Target |
| R2 | Click | Atacar |
| D-Pad | WASD | Movimiento |

## Macros Especiales FF14

- **Auto-Attack**: Ctrl+Click
- **Mount/Dismount**: Ctrl+Space
- **Sprint**: Shift+Space
- **Return**: Ctrl+R

## Solución de Problemas

### No se conecta al PC
1. Verifica que ambos dispositivos estén en la misma red WiFi
2. Desactiva el firewall de Windows temporalmente
3. Verifica que la IP sea correcta
4. Reinicia el servidor PC

### Los controles no funcionan en FF14
1. Asegúrate de que FF14 esté en foco (ventana activa)
2. Verifica que no haya otros programas interceptando las teclas
3. Ejecuta FF14 en modo ventana para mejor compatibilidad

### Lag en los controles
1. Verifica la calidad de la red WiFi
2. Acerca la tableta al router
3. Cierra otras aplicaciones que usen internet

## Funcionalidades Avanzadas

### Personalización de Macros
Puedes modificar `ff14_server_pc.py` para agregar tus propios macros:

```python
# Ejemplo de macro personalizado
def custom_macro(self):
    keyboard.press_and_release('ctrl+1')
    time.sleep(0.1)
    keyboard.press_and_release('ctrl+2')
```

### Profiles de Teclas
La app soporta diferentes perfiles para diferentes clases de FF14.

## Licencia
Proyecto de código abierto para uso personal en FF14.

## Contribuciones
¡Las contribuciones son bienvenidas! Puedes:
- Reportar bugs
- Sugerir mejoras
- Agregar nuevas funcionalidades
- Mejorar la documentación

## Créditos
Desarrollado para mejorar la experiencia de juego en FF14 usando tabletas Android como controladores personalizados.
