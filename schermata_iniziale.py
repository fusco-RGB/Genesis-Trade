"""
schermata_iniziale.py
Finestra principale dell'applicazione: login, registrazione e accesso all'area trading.
"""
import customtkinter as ctk 
import registrati   
import gestione_json as gj
import area_trading
import inserisci_saldo

class schermata_inizale (ctk.CTk):

    def __init__(self):
        super().__init__()
        # Aspetto e titolo applicazione
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self.title("CryptoSim - Demo")
        self.configure(fg_color="#0b0b0b")
        self.geometry("800x600")
        self.after(100, lambda: self.state("zoomed"))
        self.frame_login = ctk.CTkFrame(self, 
                                        width=360, 
                                        height=480, 
                                        fg_color="#121216", 
                                        corner_radius=14)
        self.frame_login.place(relx=0.5, rely=0.5, anchor="center")
        self.setup_login_widgets()
    def setup_login_widgets(self):
            self.title_label = ctk.CTkLabel(self.frame_login, 
                                        text="BENVENUTO", 
                                        text_color="#FFFFFF",
                                        font=("Helvetica", 26, "bold"))
            self.title_label.pack(pady=(40, 20))
        # Campo Username
            self.user_entry = ctk.CTkEntry(self.frame_login, 
                                       placeholder_text="Username",
                                       width=250,
                                       fg_color="#1b1b1b",
                                       text_color="#FFFFFF",
                                       border_color="#333333")

            self.user_entry.pack(pady=10)

        # Campo Password (con show="*")
            self.pass_entry = ctk.CTkEntry(self.frame_login, 
                                       placeholder_text="Password",
                                       show="*",
                                       width=250,
                                       fg_color="#1b1b1b",
                                       text_color="#FFFFFF",
                                       border_color="#333333")
            self.pass_entry.pack(pady=10)
        # Bottone toggle password
            self.toggle_btn = ctk.CTkButton(self.frame_login, 
                                              text='Mostra', 
                                              command=self.toggle_password,
                                              fg_color="#1f6feb",
                                              hover_color="#1665c1",
                                              width=100)
            self.toggle_btn.pack(pady=(10))
# Bottone Accedi
            self.login_button = ctk.CTkButton(self.frame_login, 
                                          text="ACCEDI", 
                                          command=self.azione_login,
                                          fg_color="#1f6feb",
                                          hover_color="#1665c1",
                                          width=200,
                                          corner_radius=12)
            self.login_button.pack(pady=(30, 5))

            self.login_button = ctk.CTkButton(self.frame_login, 
                                          text="REGISTRATI", 
                                          fg_color="#2b2b2b",
                                          hover_color="#3b3b3b",
                                          command=self.passa_a_registrati,
                                          width=200,
                                          corner_radius=12)
            self.login_button.pack(pady=30)        
    def passa_a_registrati(self):
        # Nascondi il frame del login
        self.frame_login.place_forget() 
    
        # Crea e mostra il frame di registrazione dal file esterno
        self.frame_reg = registrati.Registrazione(self) 
        self.frame_reg.place(relx=0.5, rely=0.5, anchor="center")
    def toggle_password(self):
        if self.pass_entry.cget('show') == '*':
              self.pass_entry.configure(show='')
              self.toggle_btn.configure(text='Nascondi')
        else:
              self.pass_entry.configure(show='*')
              self.toggle_btn.configure(text='Mostra')

    def azione_login(self):
        print(f"Tentativo di login per: {self.user_entry.get()}")
        # Qui puoi aggiungere la logica di autenticazione
        username = self.user_entry.get().strip()
        password = self.pass_entry.get()
        dati = gj.GestoreDati().deserializza()

        login_ok = False
        # Supporta sia il formato legacy dict che la lista di oggetti
        if isinstance(dati, dict):
            if username in dati and dati[username] == password:
                login_ok = True
        elif isinstance(dati, list):
            match = next((e for e in dati if e.get("username") == username and e.get("password") == password), None)
            if match:
                login_ok = True

        if login_ok:
            print("Login riuscito!")
            # Nascondi il frame del login
            self.frame_login.place_forget()

            # Mostra il frame che chiede quanto prelevare dalla carta
            self.frame_next = inserisci_saldo.InserisciSaldo(self, username=username, on_confirm=self._mostra_area_trading)
            self.frame_next.place(relx=0.5, rely=0.5, anchor="center")
        else:
            print("Credenziali non valide.")

    def _mostra_area_trading(self, username):
        # dopo aver inserito il saldo, mostra l'area trading (frame, non nuova finestra)
        try:
            if hasattr(self, 'frame_next'):
                self.frame_next.place_forget()
        except Exception:
            pass
        self.frame_reg = area_trading.App(self, username=username)
        self.frame_reg.place(relx=0.0, rely=0.5, anchor="w")
