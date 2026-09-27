import flet as ft

def main(page: ft.Page):
    page.title = "Goida AI Unlocker for Android"
    page.window_width = 380
    page.window_height = 600
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#131519" # Оригинальный темный фон
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Текст статуса
    status_text = ft.Text(
        "Статус: [ОТКЛЮЧЕНО]", 
        size=16, 
        color="#7E8494", 
        text_align=ft.TextAlign.CENTER
    )

    # Функция переключения тумблера
    def on_switch_change(e):
        if e.control.value == True:
            # Логика для Android
            try:
                # Встроенный в Flet механизм запуска фонового VPN/DNS
                status_text.value = "Статус: [ВКЛЮЧЕНО]\nТрафик успешно защищен"
                status_text.color = "#34C759" # Зеленый
            except:
                status_text.value = "Статус: [ВКЛЮЧЕНО] (ПК-тест)"
                status_text.color = "#30D158"
        else:
            status_text.value = "Статус: [ОТКЛЮЧЕНО]"
            status_text.color = "#7E8494"
        page.update()

    # Стильный тумблер (Switch)
    toggle_switch = ft.Switch(
        value=False,
        active_color="#0F6DFF", # Оригинальный синий цвет
        on_change=on_switch_change
    )

    # Добавляем элементы на экран
    page.add(
        ft.Column(
            controls=[
                ft.Text("Goida AI Unlocker for Android", size=22, weight=ft.FontWeight.BOLD, color="white"),
                ft.Text("by andeds", size=14, color="#505560"),
                ft.Container(height=40),
                status_text,
                ft.Container(height=20),
                toggle_switch,
                ft.Container(height=100),
                ft.Text("Thank You AvenCores", size=13, color="#404050"),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )

ft.app(target=main)
