#!/usr/bin/env python3
"""
Servidor PC para FF14 Controller App
Recibe comandos de la tableta Android y los ejecuta como teclas
"""

import socket
import json
import threading
import time
import keyboard
import mouse
from pynput import keyboard as pynput_key
from pynput.keyboard import Key, Listener
import tkinter as tk
from tkinter import ttk, scrolledtext
import sys

class FF14ServerPC:
    def __init__(self):
        self.server_socket = None
        self.running = False
        self.clients = []
        self.port = 9999
        
        # Mapeo de teclas especiales
        self.key_mapping = {
            'Enter': Key.enter,
            'Esc': Key.esc,
            'Space': Key.space,
            'Tab': Key.tab,
            'Shift': Key.shift,
            'Ctrl': Key.ctrl,
            'Alt': Key.alt,
            'Up': Key.up,
            'Down': Key.down,
            'Left': Key.left,
            'Right': Key.right
        }
        
        # Crear interfaz gráfica
        self.create_gui()
        
    def create_gui(self):
        """Crear interfaz gráfica del servidor"""
        self.root = tk.Tk()
        self.root.title("FF14 Controller Server")
        self.root.geometry("500x400")
        self.root.configure(bg='#2b2b2b')
        
        # Título
        title = tk.Label(self.root, text="FF14 Controller Server", 
                        font=('Arial', 16, 'bold'),
                        bg='#2b2b2b', fg='white')
        title.pack(pady=10)
        
        # Estado del servidor
        self.status_frame = tk.Frame(self.root, bg='#2b2b2b')
        self.status_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(self.status_frame, text="Estado:", 
                bg='#2b2b2b', fg='white').pack(side='left')
        
        self.status_label = tk.Label(self.status_frame, text="Detenido", 
                                   bg='#2b2b2b', fg='red')
        self.status_label.pack(side='left', padx=10)
        
        # Puerto
        port_frame = tk.Frame(self.root, bg='#2b2b2b')
        port_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(port_frame, text="Puerto:", 
                bg='#2b2b2b', fg='white').pack(side='left')
        
        self.port_entry = tk.Entry(port_frame, width=10)
        self.port_entry.insert(0, str(self.port))
        self.port_entry.pack(side='left', padx=10)
        
        # IP local
        ip_frame = tk.Frame(self.root, bg='#2b2b2b')
        ip_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(ip_frame, text="IP Local:", 
                bg='#2b2b2b', fg='white').pack(side='left')
        
        local_ip = self.get_local_ip()
        self.ip_label = tk.Label(ip_frame, text=local_ip, 
                               bg='#2b2b2b', fg='yellow')
        self.ip_label.pack(side='left', padx=10)
        
        # Botones
        button_frame = tk.Frame(self.root, bg='#2b2b2b')
        button_frame.pack(fill='x', padx=10, pady=10)
        
        self.start_btn = tk.Button(button_frame, text="Iniciar Servidor", 
                                  command=self.start_server,
                                  bg='green', fg='white')
        self.start_btn.pack(side='left', padx=5)
        
        self.stop_btn = tk.Button(button_frame, text="Detener Servidor", 
                                 command=self.stop_server,
                                 bg='red', fg='white', state='disabled')
        self.stop_btn.pack(side='left', padx=5)
        
        # Log de actividad
        tk.Label(self.root, text="Log de Actividad:", 
                bg='#2b2b2b', fg='white').pack(anchor='w', padx=10, pady=(10,0))
        
        self.log_text = scrolledtext.ScrolledText(self.root, height=12, 
                                                 bg='#1e1e1e', fg='white',
                                                 insertbackground='white')
        self.log_text.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Instrucciones
        instructions = (
            "INSTRUCCIONES:\n"
            "1. Haz clic en 'Iniciar Servidor'\n"
            "2. Conecta tu tableta Android a la misma red WiFi\n"
            "3. En la tableta, usa la IP mostrada arriba\n"
            "4. ¡Disfruta controlando FF14 desde tu tableta!\n\n"
            "NOTA: Asegúrate de que FF14 esté en foco cuando uses los controles."
        )
        
        info_label = tk.Label(self.root, text=instructions, 
                            bg='#2b2b2b', fg='lightgray',
                            justify='left', font=('Arial', 9))
        info_label.pack(fill='x', padx=10, pady=5)
        
    def get_local_ip(self):
        """Obtener IP local de la máquina"""
        try:
            # Conectar a un servidor externo para obtener la IP local
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "127.0.0.1"
    
    def log(self, message):
        """Agregar mensaje al log"""
        timestamp = time.strftime("%H:%M:%S")
        log_message = f"[{timestamp}] {message}\n"
        
        self.log_text.insert(tk.END, log_message)
        self.log_text.see(tk.END)
        self.root.update()
        
    def start_server(self):
        """Iniciar el servidor"""
        try:
            self.port = int(self.port_entry.get())
            
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind(('0.0.0.0', self.port))
            self.server_socket.listen(5)
            
            self.running = True
            self.status_label.config(text="Ejecutándose", fg='green')
            self.start_btn.config(state='disabled')
            self.stop_btn.config(state='normal')
            
            self.log(f"Servidor iniciado en puerto {self.port}")
            self.log(f"Esperando conexiones en {self.get_local_ip()}:{self.port}")
            
            # Iniciar hilo para aceptar conexiones
            threading.Thread(target=self.accept_connections, daemon=True).start()
            
        except Exception as e:
            self.log(f"Error iniciando servidor: {e}")
    
    def stop_server(self):
        """Detener el servidor"""
        self.running = False
        
        if self.server_socket:
            self.server_socket.close()
            
        for client in self.clients:
            client.close()
        self.clients.clear()
        
        self.status_label.config(text="Detenido", fg='red')
        self.start_btn.config(state='normal')
        self.stop_btn.config(state='disabled')
        
        self.log("Servidor detenido")
    
    def accept_connections(self):
        """Aceptar conexiones de clientes"""
        while self.running:
            try:
                client_socket, addr = self.server_socket.accept()
                self.clients.append(client_socket)
                self.log(f"Cliente conectado desde {addr[0]}:{addr[1]}")
                
                # Iniciar hilo para manejar este cliente
                threading.Thread(target=self.handle_client, 
                               args=(client_socket, addr), daemon=True).start()
                
            except Exception as e:
                if self.running:
                    self.log(f"Error aceptando conexión: {e}")
                break
    
    def handle_client(self, client_socket, addr):
        """Manejar comandos de un cliente"""
        buffer = ""
        
        while self.running:
            try:
                data = client_socket.recv(1024).decode()
                if not data:
                    break
                    
                buffer += data
                
                # Procesar comandos completos (terminados en \n)
                while '\n' in buffer:
                    line, buffer = buffer.split('\n', 1)
                    if line.strip():
                        self.process_command(line.strip(), addr)
                        
            except Exception as e:
                self.log(f"Error con cliente {addr[0]}: {e}")
                break
        
        # Limpiar al desconectar
        if client_socket in self.clients:
            self.clients.remove(client_socket)
        client_socket.close()
        self.log(f"Cliente {addr[0]} desconectado")
    
    def process_command(self, command_str, addr):
        """Procesar comando recibido del cliente"""
        try:
            command = json.loads(command_str)
            cmd_type = command.get('type')
            
            if cmd_type == 'key':
                key = command.get('key')
                self.send_key(key)
                self.log(f"Tecla enviada: {key}")
                
            elif cmd_type == 'combination':
                keys = command.get('keys')
                self.send_key_combination(keys)
                self.log(f"Combinación enviada: {keys}")
                
            elif cmd_type == 'click':
                button = command.get('button', 'left')
                self.send_mouse_click(button)
                self.log(f"Click enviado: {button}")
                
        except Exception as e:
            self.log(f"Error procesando comando: {e}")
    
    def send_key(self, key):
        """Enviar tecla individual"""
        try:
            if key in self.key_mapping:
                # Tecla especial
                keyboard_controller = pynput_key.Controller()
                keyboard_controller.press(self.key_mapping[key])
                keyboard_controller.release(self.key_mapping[key])
            else:
                # Tecla normal o letra
                if len(key) == 1:
                    keyboard.press_and_release(key.lower())
                else:
                    # Teclas F (F1, F2, etc.)
                    keyboard.press_and_release(key.lower())
                    
        except Exception as e:
            self.log(f"Error enviando tecla {key}: {e}")
    
    def send_key_combination(self, combination):
        """Enviar combinación de teclas"""
        try:
            # Dividir la combinación (ej: "Ctrl+A")
            keys = combination.split('+')
            
            if len(keys) == 2:
                modifier = keys[0].lower()
                key = keys[1].lower()
                
                # Usar keyboard library para combinaciones
                if modifier == 'ctrl':
                    keyboard.press_and_release(f'ctrl+{key}')
                elif modifier == 'alt':
                    keyboard.press_and_release(f'alt+{key}')
                elif modifier == 'shift':
                    keyboard.press_and_release(f'shift+{key}')
                else:
                    keyboard.press_and_release(combination.lower())
            else:
                keyboard.press_and_release(combination.lower())
                
        except Exception as e:
            self.log(f"Error enviando combinación {combination}: {e}")
    
    def send_mouse_click(self, button):
        """Enviar click del mouse"""
        try:
            if button == 'left':
                mouse.click('left')
            elif button == 'right':
                mouse.click('right')
            elif button == 'middle':
                mouse.click('middle')
                
        except Exception as e:
            self.log(f"Error enviando click {button}: {e}")
    
    def run(self):
        """Ejecutar la aplicación"""
        try:
            self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
            self.root.mainloop()
        except KeyboardInterrupt:
            self.stop_server()
    
    def on_closing(self):
        """Manejar cierre de la aplicación"""
        self.stop_server()
        self.root.destroy()

def main():
    print("FF14 Controller Server - Iniciando...")
    server = FF14ServerPC()
    server.run()

if __name__ == '__main__':
    main()
