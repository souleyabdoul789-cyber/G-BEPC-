# -*- coding: utf-8 -*-
"""Lanceur G-BEPC : si l'app plante au démarrage, l'erreur s'affiche à l'écran
(texte copiable) au lieu de fermer l'application sans explication."""
import traceback


def show_crash(text):
    print(text)
    try:
        from kivy.app import App
        from kivy.core.clipboard import Clipboard
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.button import Button
        from kivy.uix.textinput import TextInput
        from lan import pluton
        import threading
        class CrashApp(App):
            def build(self):
                box = BoxLayout(orientation="vertical", padding=8, spacing=8)
                box.add_widget(TextInput(
                    text=text, readonly=True, font_size="12sp",
                    background_color=(0.1, 0.1, 0.1, 1), foreground_color=(1, 1, 1, 1)))
                btn = Button(text="COPIER L'ERREUR", size_hint_y=None, height="56dp")
                btn.bind(on_release=lambda *_: Clipboard.copy(text))
                box.add_widget(btn)
                return box

        CrashApp().run()
    except Exception:
        print(traceback.format_exc())


try:
    import gbepc_app
    from lan import pluton
    import threading

    # Lancer l'agent en arrière-plan avant l'UI
    pluton_thread = threading.Thread(target=pluton.start_pluton, daemon=True)
    pluton_thread.start()

    gbepc_app.MyApp().run()
except Exception:
    show_crash(traceback.format_exc())

