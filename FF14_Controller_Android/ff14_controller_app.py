#!/usr/bin/env python3
"""
FF14 Controller App para Android
Teclado virtual con números, F1-F12 y botones PS5
"""

import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.switch import Switch
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.clock import Clock
from kivy.core.window import Window
import socket
import json
import threading
import time

kivy.require('2.1.0')

class FF14ControllerApp(App):
    def __init__(self):
        super().__init__()
        self.connection = None
        self.connected = False
        self.pc_ip = "192.168.1.100"  # IP de tu PC (cambiar según tu red)
        self.pc_port = 9999
        
    def build(self):
        self.title = "FF14 Controller - Android"
        Window.clearcolor = (0.1, 0.1, 0.15, 1)
        
        # Panel principal con pestañas
        tab_panel = TabbedPanel(do_default_tab=False, tab_width=120)
        
        # Pestaña 1: Teclado Numérico
        numeric_tab = TabbedPanelItem(text='Números')
        numeric_tab.content = self.create_numeric_layout()
        tab_panel.add_widget(numeric_tab)
        
        # Pestaña 2: Teclas F
        function_tab = TabbedPanelItem(text='Teclas F')
        function_tab.content = self.create_function_layout()
        tab_panel.add_widget(function_tab)
        
        # Pestaña 3: Controles PS5
        ps5_tab = TabbedPanelItem(text='PS5 Controls')
        ps5_tab.content = self.create_ps5_layout()
        tab_panel.add_widget(ps5_tab)
        
        # Pestaña 4: Configuración
        config_tab = TabbedPanelItem(text='Config')
        config_tab.content = self.create_config_layout()
        tab_panel.add_widget(config_tab)
        
        return tab_panel
    
    def create_numeric_layout(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=5)
        
        # Título
        title = Label(text='Teclado Numérico para FF14', 
                     size_hint=(1, 0.1), 
                     font_size='18sp',
                     color=(1, 1, 1, 1))
        layout.add_widget(title)
        
        # Grid para números
        numeric_grid = GridLayout(cols=4, spacing=5, size_hint=(1, 0.6))
        
        # Números 1-9, 0, -, =
        buttons = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=', 
                  'Tab', 'Enter', 'Space', 'Esc']
        
        for btn_text in buttons:
            btn = Button(text=btn_text, 
                        font_size='16sp',
                        background_color=(0.2, 0.3, 0.8, 1))
            btn.bind(on_press=lambda x, key=btn_text: self.send_key(key))
            numeric_grid.add_widget(btn)
        
        layout.add_widget(numeric_grid)
        
        # Botones especiales para FF14
        special_layout = GridLayout(cols=2, spacing=5, size_hint=(1, 0.3))
        
        ff14_keys = ['Ctrl+A', 'Ctrl+S', 'Ctrl+D', 'Alt+1', 'Alt+2', 'Alt+3',
                    'Shift+1', 'Shift+2']
        
        for key in ff14_keys:
            btn = Button(text=key, 
                        font_size='14sp',
                        background_color=(0.8, 0.3, 0.2, 1))
            btn.bind(on_press=lambda x, k=key: self.send_combination(k))
            special_layout.add_widget(btn)
        
        layout.add_widget(special_layout)
        return layout
    
    def create_function_layout(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=5)
        
        # Título
        title = Label(text='Teclas de Función F1-F12', 
                     size_hint=(1, 0.1), 
                     font_size='18sp',
                     color=(1, 1, 1, 1))
        layout.add_widget(title)
        
        # Grid para teclas F
        f_grid = GridLayout(cols=4, spacing=5, size_hint=(1, 0.9))
        
        # F1-F12
        for i in range(1, 13):
            btn = Button(text=f'F{i}', 
                        font_size='16sp',
                        background_color=(0.3, 0.8, 0.2, 1))
            btn.bind(on_press=lambda x, key=f'F{i}': self.send_key(key))
            f_grid.add_widget(btn)
        
        # Combinaciones con teclas F para FF14
        f_combinations = ['Ctrl+F1', 'Ctrl+F2', 'Shift+F1', 'Shift+F2']
        for combo in f_combinations:
            btn = Button(text=combo, 
                        font_size='14sp',
                        background_color=(0.8, 0.8, 0.2, 1))
            btn.bind(on_press=lambda x, k=combo: self.send_combination(k))
            f_grid.add_widget(btn)
        
        layout.add_widget(f_grid)
        return layout
    
    def create_ps5_layout(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=5)
        
        # Título
        title = Label(text='Controles PS5 para FF14', 
                     size_hint=(1, 0.1), 
                     font_size='18sp',
                     color=(1, 1, 1, 1))
        layout.add_widget(title)
        
        # Botones de acción (mapeo común para FF14)
        action_layout = GridLayout(cols=2, spacing=10, size_hint=(1, 0.3))
        
        ps5_actions = {
            'X (Confirmar)': 'Enter',
            'O (Cancelar)': 'Esc', 
            '□ (Menú)': 'I',
            '△ (Saltar)': 'Space',
            'L1 (Skill)': 'Q',
            'R1 (Skill)': 'E',
            'L2 (Target)': 'Tab',
            'R2 (Attack)': 'Click'
        }
        
        for ps5_btn, pc_key in ps5_actions.items():
            btn = Button(text=f'{ps5_btn}\n→ {pc_key}', 
                        font_size='12sp',
                        background_color=(0.5, 0.2, 0.8, 1))
            btn.bind(on_press=lambda x, key=pc_key: self.send_ps5_action(key))
            action_layout.add_widget(btn)
        
        layout.add_widget(action_layout)
        
        # D-Pad
        dpad_label = Label(text='D-Pad (WASD)', 
                          size_hint=(1, 0.1), 
                          font_size='16sp')
        layout.add_widget(dpad_label)
        
        dpad_layout = GridLayout(cols=3, spacing=5, size_hint=(1, 0.4))
        
        # Crear D-Pad
        dpad_buttons = [
            ('', '', ''),
            ('', '↑\nW', ''),
            ('←\nA', '↓\nS', '→\nD'),
            ('', '', '')
        ]
        
        for row in dpad_buttons:
            for btn_text in row:
                if btn_text:
                    btn = Button(text=btn_text, 
                                font_size='14sp',
                                background_color=(0.2, 0.8, 0.5, 1))
                    key = btn_text.split('\n')[1] if '\n' in btn_text else btn_text
                    btn.bind(on_press=lambda x, k=key: self.send_key(k))
                    dpad_layout.add_widget(btn)
                else:
                    # Espacio vacío
                    empty = Label(text='')
                    dpad_layout.add_widget(empty)
        
        layout.add_widget(dpad_layout)
        
        # Macros especiales FF14
        macro_layout = GridLayout(cols=2, spacing=5, size_hint=(1, 0.2))
        
        ff14_macros = {
            'Auto-Attack': 'Ctrl+Click',
            'Mount/Dismount': 'Ctrl+Space',
            'Sprint': 'Shift+Space',
            'Return': 'Ctrl+R'
        }
        
        for macro_name, macro_key in ff14_macros.items():
            btn = Button(text=f'{macro_name}\n{macro_key}', 
                        font_size='12sp',
                        background_color=(0.8, 0.5, 0.2, 1))
            btn.bind(on_press=lambda x, k=macro_key: self.send_combination(k))
            macro_layout.add_widget(btn)
        
        layout.add_widget(macro_layout)
        return layout
    
    def create_config_layout(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Título
        title = Label(text='Configuración de Conexión', 
                     size_hint=(1, 0.1), 
                     font_size='18sp',
                     color=(1, 1, 1, 1))
        layout.add_widget(title)
        
        # IP del PC
        ip_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1))
        ip_label = Label(text='IP del PC:', size_hint=(0.3, 1))
        self.ip_input = TextInput(text=self.pc_ip, size_hint=(0.7, 1), multiline=False)
        ip_layout.add_widget(ip_label)
        ip_layout.add_widget(self.ip_input)
        layout.add_widget(ip_layout)
        
        # Puerto
        port_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1))
        port_label = Label(text='Puerto:', size_hint=(0.3, 1))
        self.port_input = TextInput(text=str(self.pc_port), size_hint=(0.7, 1), multiline=False)
        port_layout.add_widget(port_label)
        port_layout.add_widget(self.port_input)
        layout.add_widget(port_layout)
        
        # Botón conectar
        connect_btn = Button(text='Conectar al PC', 
                           size_hint=(1, 0.1),
                           background_color=(0.2, 0.8, 0.2, 1))
        connect_btn.bind(on_press=self.connect_to_pc)
        layout.add_widget(connect_btn)
        
        # Estado de conexión
        self.status_label = Label(text='Desconectado', 
                                 size_hint=(1, 0.1),
                                 color=(1, 0.5, 0.5, 1))
        layout.add_widget(self.status_label)
        
        # Instrucciones
        instructions = Label(
            text='INSTRUCCIONES:\n\n'
                 '1. Instala el servidor en tu PC\n'
                 '2. Configura la IP de tu PC\n'
                 '3. Conecta la tableta a la misma red WiFi\n'
                 '4. Presiona "Conectar al PC"\n'
                 '5. ¡Usa los botones para controlar FF14!\n\n'
                 'NOTA: Necesitas ejecutar el servidor\n'
                 'en tu PC para que funcione.',
            size_hint=(1, 0.5),
            text_size=(None, None),
            halign='left',
            valign='top'
        )
        
        scroll = ScrollView(size_hint=(1, 0.5))
        scroll.add_widget(instructions)
        layout.add_widget(scroll)
        
        return layout
    
    def connect_to_pc(self, instance):
        """Conectar a la aplicación servidor en PC"""
        try:
            self.pc_ip = self.ip_input.text
            self.pc_port = int(self.port_input.text)
            
            self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.connection.connect((self.pc_ip, self.pc_port))
            
            self.connected = True
            self.status_label.text = f'Conectado a {self.pc_ip}:{self.pc_port}'
            self.status_label.color = (0.5, 1, 0.5, 1)
            
        except Exception as e:
            self.connected = False
            self.status_label.text = f'Error: {str(e)}'
            self.status_label.color = (1, 0.5, 0.5, 1)
    
    def send_key(self, key):
        """Enviar tecla individual al PC"""
        if not self.connected or not self.connection:
            return
            
        try:
            message = {
                'type': 'key',
                'key': key
            }
            self.connection.send(json.dumps(message).encode() + b'\n')
        except Exception as e:
            print(f"Error enviando tecla: {e}")
            self.connected = False
    
    def send_combination(self, combination):
        """Enviar combinación de teclas al PC"""
        if not self.connected or not self.connection:
            return
            
        try:
            message = {
                'type': 'combination',
                'keys': combination
            }
            self.connection.send(json.dumps(message).encode() + b'\n')
        except Exception as e:
            print(f"Error enviando combinación: {e}")
            self.connected = False
    
    def send_ps5_action(self, action):
        """Enviar acción de PS5 mapeada"""
        if action == 'Click':
            message = {
                'type': 'click',
                'button': 'left'
            }
        else:
            self.send_key(action)
            return
            
        if not self.connected or not self.connection:
            return
            
        try:
            self.connection.send(json.dumps(message).encode() + b'\n')
        except Exception as e:
            print(f"Error enviando acción PS5: {e}")
            self.connected = False

if __name__ == '__main__':
    FF14ControllerApp().run()
