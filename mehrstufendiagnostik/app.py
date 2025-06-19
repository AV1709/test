# -*- coding: utf-8 -*-


import threading

import webview

from mehrstufendiagnostik.flaskr.start import startUp, create_app

def start_flask():
    startUp()
    app = create_app()
    app.run(host="localhost", port=8080)


def main():
    flask_thread = threading.Thread(target=start_flask)
    flask_thread.daemon = True
    flask_thread.start()
    print("Backend initialization completed!")

    webview.settings["ALLOW_DOWNLOADS"] = True
    window = webview.create_window(
        "Mehrstufendiagnostik von Muskel-Skelett-Erkrankungen", url="http://localhost:8080"
    )

    webview.start()


if __name__ == '__main__':
    main()
