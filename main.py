from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.utils import platform

# Настройка размера окна только для тестов на ПК
if platform not in ['android', 'ios']:
    Window.size = (360, 640)

class GoidaApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=30, spacing=20)
        
        self.status_label = Label(
            text="Goida AI Unlocker\n[Статус: Отключено]", 
            font_size='20sp',
            halign='center'
        )
        layout.add_widget(self.status_label)
        
        self.btn = Button(
            text="Включить разблокировку", 
            background_color=(0.1, 0.6, 0.2, 1),
            font_size='18sp'
        )
        self.btn.bind(on_press=self.toggle_unlock)
        layout.add_widget(self.btn)
        
        return layout

    def toggle_unlock(self, instance):
        if "Отключено" in self.status_label.text:
            # Если код запущен на смартфоне Android
            if platform == 'android':
                try:
                    from jnius import autoclass
                    
                    # 1. Получаем доступ к текущему контексту Android
                    PythonActivity = autoclass('org.kivy.android.PythonActivity')
                    current_activity = PythonActivity.mActivity
                    
                    # 2. Инициализируем системный класс VpnService
                    VpnService = autoclass('android.net.VpnService')
                    
                    # 3. Проверяем, разрешил ли пользователь VPN-туннель
                    intent = VpnService.prepare(current_activity)
                    if intent is not None:
                        # Показываем системный запрос Android на включение VPN
                        current_activity.startActivityForResult(intent, 0)
                        self.status_label.text = "Предоставьте разрешение\nна VPN в системе!"
                        return
                    
                    # 4. Если разрешение уже есть, создаем туннель и подменяем DNS
                    builder = VpnService.Builder(current_activity)
                    builder.addAddress("10.0.0.2", 32)
                    
                    # Задаем DNS-сервер, который умеет обходить блокировки ИИ
                    builder.addDnsServer("176.103.130.130") 
                    builder.addDnsServer("176.103.130.131")
                    builder.setSession("GoidaAIUnlocker")
                    
                    # Запуск туннеля
                    self.vpn_interface = builder.establish()
                    self.status_label.text = "Goida AI Unlocker\n[Статус: АКТИВИРОВАНО]"
                    
                except Exception as e:
                    self.status_label.text = f"Ошибка Android API:\n{str(e)}"
            else:
                # Логика для теста на ПК (оставляем старую)
                self.status_label.text = "Goida AI Unlocker\n[Статус: АКТИВИРОВАНО (ПК-Тест)]"
            
            self.btn.text = "Выключить"
            self.btn.background_color = (0.8, 0.2, 0.2, 1)
        else:
            # Выключение обхода
            if platform == 'android' and hasattr(self, 'vpn_interface') and self.vpn_interface:
                try:
                    self.vpn_interface.close()
                except:
                    pass
            
            self.status_label.text = "Goida AI Unlocker\n[Статус: Отключено]"
            self.btn.text = "Включить разблокировку"
            self.btn.background_color = (0.1, 0.6, 0.2, 1)

if __name__ == '__main__':
    GoidaApp().run()
