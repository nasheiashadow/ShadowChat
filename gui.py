# ==========================================
# SHADOWCHAT GUI
# Version 2.0
# By Nasheiashadow
# ==========================================

import tkinter as tk


class ShadowChatGUI:

    def __init__(self):

        self.window = tk.Tk()

        # Window Title
        self.window.title("ShadowChat")

        # Window Size
        self.window.geometry("900x600")

        # Minimum Size
        self.window.minsize(800, 500)

        # Background Colour
        self.window.configure(bg="#202123")

        # ==================================
        # TITLE
        # ==================================

        title = tk.Label(
            self.window,
            text="SHADOWCHAT",
            font=("Arial", 28, "bold"),
            fg="white",
            bg="#202123"
        )

        title.pack(pady=20)

        # ==================================
        # SUBTITLE
        # ==================================

        subtitle = tk.Label(
            self.window,
            text="Welcome to ShadowChat Desktop v2.0",
            font=("Arial", 14),
            fg="lightgray",
            bg="#202123"
        )

        subtitle.pack()

        # ==================================
        # LOGIN BUTTON
        # ==================================

        login_button = tk.Button(
            self.window,
            text="Login",
            font=("Arial", 14),
            width=20,
            height=2,
            bg="#4CAF50",
            fg="white"
        )

        login_button.pack(pady=20)

        # ==================================
        # REGISTER BUTTON
        # ==================================

        register_button = tk.Button(
            self.window,
            text="Register",
            font=("Arial", 14),
            width=20,
            height=2,
            bg="#2196F3",
            fg="white"
        )

        register_button.pack()

        # ==================================
        # FOOTER
        # ==================================

        footer = tk.Label(
            self.window,
            text="Developed by Nasheiashadow",
            font=("Arial", 10),
            fg="gray",
            bg="#202123"
        )

        footer.pack(side="bottom", pady=20)

    def run(self):

        self.window.mainloop()


if __name__ == "__main__":

    app = ShadowChatGUI()

    app.run()