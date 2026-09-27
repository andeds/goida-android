from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.utils import platform
from kivy.graphics import Color, RoundedRectangle, Ellipse
from kivy.animation import Animation
from kivy.properties import BooleanProperty

# Настройка размера окна на ПК
if platform not in ['android', 'ios']:
    Window.size = (380, 600)

# Кастомный стильный переключатель (Toggle Switch)
class ModernSwitch(Widget):
    active = BooleanProperty(False)

    def __init__(self, **kwargs):
        super(ModernSwitch, self).__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (70, 36)
        self.thumb_pos_x = self.x + 4
        
        with self.canvas.before:
            self.bg_color = Color(0.22, 0.24, 0.30, 1)
            self.bg_rect = RoundedRectangle(size=self.size, pos=self.pos, radius=18)
            self.thumb_color = Color(1, 1, 1, 1)
            self.thumb_ellipse = Ellipse(size=(28, 28), pos=(self.thumb_pos_x, self.y + 4))
            
        self.bind(pos=self.update_canvas, size=self.update_canvas)

    def update_canvas(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
        if not self.active:
            self.thumb_ellipse.pos = (self.x + 4, self.y + 4)
        else:
            self.thumb_ellipse.pos = (self.x + self.width - 32, self.y + 4)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.active = not self.active
            self.animate_switch()
            return True
        return super(ModernSwitch, self).on_touch_down(touch)

    def animate_switch(self):
        if self.active:
            target_x = self.x + self.width - 32
            anim = Animation(pos=(target_x, self.y + 4), duration=0.2, t='out_quad')
            anim.start(self.thumb_ellipse)
            self.bg_color.rgba = (0.15, 0.42, 0.85, 1)
        else:
            target_x = self.x + 4
            anim = Animation(pos=(target_x, self.y + 4), duration=0.2, t='out_quad')
            anim.start(self.thumb_ellipse)
            self.bg_color.rgba = (0.22, 0.24, 0.30, 1)


class GoidaApp(App):
    def build(self):
        # Главный контейнер
        main_layout = BoxLayout(orientation='vertical', padding=(30, 40, 30, 20), spacing=15)
        
        with main_layout.canvas.before:
            Color(0.13, 0.15, 0.19, 1) # Глубокий темный фон
            self.rect = RoundedRectangle(size=main_layout.size, pos=main_layout.pos)
        main_layout.bind(size=self._update_rect, pos=self._update_rect)

        # 1. Блок заголовков (Название и автор)
        header_box = BoxLayout(orientation='vertical', size_hint_y=None, height=90, spacing=5)
        
        title_label = Label(
            text="Goida AI Unlocker for Android",
            font_size='22sp',
            bold=True,
            color=(1, 1, 1, 1),
            halign='center',
            valign='middle'
        )
        title_label.bind(size=title_label.setter('text_size'))
        
        author_label = Label(
            text="by andeds",
            font_size='14sp',
            color=(0.5, 0.5, 0.6, 1),
            halign='center',
            valign='top'
        )
        author_label.bind(size=author_label.setter('text_size'))
        
        header_box.add_widget(title_label)
        header_box.add_widget(author_label)
        main_layout.add_widget(header_box)

        # 2. Информационный статус-текст по центру
        self.status_label = Label(
            text="Статус: [ОТКЛЮЧЕНО]",
            font_size='16sp',
            color=(0.5, 0.5, 0.6, 1),
            halign='center',
            size_hint_y=0.4
        )
        main_layout.add_widget(self.status_label)

        # 3. Контейнер для центрирования переключателя
        switch_container = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
        switch_container.add_widget(Widget(size_hint_x=0.5))
        
        self.toggle = ModernSwitch()
        self.toggle.bind(active=self.on_switch_trigger)
        switch_container.add_widget(self.toggle)
        
        switch_container.add_widget(Widget(size_hint_x=0.5))
        main_layout.add_widget(switch_container)

        # Прослойка-заполнитель
        main_layout.add_widget(Widget(size_hint_y=0.3))

        # 4. Нижняя панель (Футер с благодарностью слева)
        footer_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=30)
        
        thanks_label = Label(
            text="Thank You AvenCores",
            font_size='13sp',
            color=(0.4, 0.4, 0.5, 1),
            halign='left',
            valign='bottom',
            size_hint_x=0.7
        )
        thanks_label.bind(size=thanks_label.setter('text_size'))
        
        footer_box.add_widget(thanks_label)
        footer_box.add_widget(Widget(size_hint_x=0.3))
        
        main_layout.add_widget(footer_box)

        return main_layout

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def on_switch_trigger(self, instance, value):
        if value:
            if platform == 'android':
                try:
                    from jnius import autoclass
                    PythonActivity = autoclass('org.kivy.android.PythonActivity')
                    current_activity = PythonActivity.mActivity
                    VpnService = autoclass('android.net.VpnService')
                    
                    intent = VpnService.prepare(current_activity)
                    if intent is not None:
                        current_activity.startActivityForResult(intent, 0)
                        self.status_label.text = "Ожидание разрешения VPN..."
                        self.toggle.active = False
                        self.toggle.animate_switch()
                        return
                    
                    builder = VpnService.Builder(current_activity)
                    builder.addAddress("10.0.0.2", 32)
                    builder.addDnsServer("176.103.130.130")
                    builder.setSession("GoidaAI")
                    self.vpn_interface = builder.establish()
                    
                    self.status_label.text = "Статус: [ВКЛЮЧЕНО]\nТрафик успешно защищен"
                    self.status_label.color = (0.2, 0.8, 0.2, 1)
                except Exception as e:
                    self.status_label.text = f"Ошибка системы:\n{str(e)[:30]}"
                    self.toggle.active = False
                    self.toggle.animate_switch()
            else:
                self.status_label.text = "Статус: [ВКЛЮЧЕНО] (ПК-тест)"
                self.status_label.color = (0.2, 0.8, 0.4, 1)
        else:
            if platform == 'android' and hasattr(self, 'vpn_interface') and self.vpn_interface:
                try:
                    self.vpn_interface.close()
                except:
                    pass
            
            self.status_label.text = "Статус: [ОТКЛЮЧЕНО]"
            self.status_label.color = (0.5, 0.5, 0.6, 1)

if __name__ == '__main__':
    GoidaApp().run()
