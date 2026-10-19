# -*- coding: utf-8 -*-
"""Lanceur G-BEPC avec affichage des erreurs au démarrage."""

import traceback
import threading


def show_crash(text):
    print(text)

    try:
        from kivy.app import App
        from kivy.core.clipboard import Clipboard
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.button import Button
        from kivy.uix.textinput import TextInput

        class CrashApp(App):
            def build(self):
                box = BoxLayout(
                    orientation="vertical",
                    padding=8,
                    spacing=8,
                )

                box.add_widget(
                    TextInput(
                        text=text,
                        readonly=True,
                        font_size="12sp",
                    )
                )

                btn = Button(
                    text="COPIER L'ERREUR",
                    size_hint_y=None,
                    height="56dp",
                )
                btn.bind(
                    on_release=lambda *_: Clipboard.copy(text)
                )

                box.add_widget(btn)
                return box

        CrashApp().run()

    except Exception:
        print(traceback.format_exc())


try:
    # Importer Pluton dans le try pour intercepter
    # les erreurs d'importation.
    from lan import pluton

    # Démarrer Pluton en arrière-plan.
    pluton_thread = threading.Thread(
        target=pluton.start_pluton,
        daemon=True,
    )
    pluton_thread.start()

    # Démarrer ensuite l'interface principale.
    import gbepc_app

    gbepc_app.MyApp().run()

except Exception:
    show_crash(traceback.format_exc())
