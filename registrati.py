"""
registrati.py
Frame per la registrazione di un nuovo utente. Contiene la validazione della password e
invia i dati a `gestione_json.GestoreDati` per la persistenza su file.
"""
import customtkinter as ctk
import gestione_json
import validazione
import tkinter.messagebox as mb
import registrazione_carta




class Registrazione(ctk.CTkFrame):
    """Frame di registrazione che può essere inserito nella schermata principale."""

    def __init__(self, master, **kwargs):
        super().__init__(master, width=350, height=450, fg_color="#FFFFFF", corner_radius=20, **kwargs)
        self.master = master
        self.setup_registrazione_widgets()

    def setup_registrazione_widgets(self):
        self.title_label = ctk.CTkLabel(self, text="registrati", text_color="#000000",
                                        font=("Helvetica", 24, "bold"))
        self.title_label.pack(pady=(40, 20))

        self.user_entry = ctk.CTkEntry(self, placeholder_text="Username", width=250,
                                       fg_color="#f0f0f0", text_color="#000000", border_color="#cccccc")
        self.user_entry.pack(pady=10)

        self.pass_entry = ctk.CTkEntry(self, placeholder_text="Password", width=250,
                                       fg_color="#f0f0f0", text_color="#000000", border_color="#cccccc", show="*")
        self.pass_entry.pack(pady=10)

        # Label per mostrare errori di validazione della password (sotto il campo)
        self.pw_error_label = ctk.CTkLabel(self, text="""Caratteristiche password : 
almeno 8 caratteri,
maiuscole,
minuscole,
numeri,
simboli""", text_color="#000000",
                           font=("Helvetica", 10))
        self.pw_error_label.pack(pady=(0, 8))
        # Bottone per mostrare/nascondere la password
        self.toggle_btn = ctk.CTkButton(self,
                         text='Mostra',
                         command=self.toggle_password,
                         fg_color="#000000",
                         hover_color="#333333",
                         width=100)
        self.toggle_btn.pack(pady=(10))
       

        # Bottone Registrati (usiamo questo frame come parent)
        self.register_button = ctk.CTkButton(self, text="REGISTRATI",
                                             command=self.azione_registrazione,
                                             fg_color="#000000",
                                             hover_color="#333333",
                                             width=200)
        self.register_button.pack(pady=20)

        # Bottone Annulla: torna al login senza registrare
        self.annulla_button = ctk.CTkButton(self, text="ANNULLA",
                                            command=self.torna_al_login,
                                            fg_color="#777777",
                                            hover_color="#555555",
                                            width=120)
        self.annulla_button.pack(pady=(0, 10))

    def azione_registrazione(self):
        """Validazione -> salvataggio -> ritorno al login se tutto OK."""
        username = self.user_entry.get().strip()
        password = self.pass_entry.get()

        # reset label di errore password
        self.pw_error_label.configure(text="")

        # 1. Validazione Username
        if not validazione.check_username(username):
            print("Errore: Username troppo corto!")
            return

        # 2. Validazione Password tramite il file esterno
        if not validazione.valida_password(password):
            # Mostro l'errore direttamente sotto il campo password
            self.pw_error_label.configure(text="""Caratteristiche password : 
almeno 8 caratteri,
maiuscole,
minuscole,
numeri,
simboli""", text_color="#FF0000")
            return

        # 3. Se tutto è OK, procedi al salvataggio
        try:
            self.registra_utente(username, password)
        except Exception as e:
            print(f"Errore durante la registrazione: {e}")
            mb.showerror("Registrazione", f"Errore durante la registrazione: {e}")
            return

        # Pulisco eventuali messaggi di errore
        self.pw_error_label.configure(text="")
        print(f"Utente {username} registrato con successo!")
        mb.showinfo("Registrazione", f"Utente {username} registrato con successo! Ora registra la carta.")

        # Mostro la schermata per registrare la carta, passando username e titolare
        try:
            # Nascondo il frame di registrazione corrente
            self.place_forget()
            titolare = self.entry_titolare.get().strip() if hasattr(self, 'entry_titolare') else ""
            frame_carta = registrazione_carta.Registrazione_carta(self.master, username=username, titolare=titolare)
            frame_carta.place(relx=0.5, rely=0.5, anchor="center")
        except Exception as e:
            print(f"Errore aprendo registrazione carta: {e}")
            # fallback: torno al login
            try:
                self.master.after(100, self.torna_al_login)
            except Exception:
                self.torna_al_login()

    def registra_utente(self, username, password):
        gestore = gestione_json.GestoreDati()
        # Use the provided add_user helper which preserves on-disk format and handles list/dict
        # Generate a new unique conto (10 digits) when stored in list format
        dati = gestore.deserializza()
        max_conto = 0
        if isinstance(dati, list):
            for entry in dati:
                try:
                    c = int(entry.get("conto", "0"))
                    if c > max_conto:
                        max_conto = c
                except Exception:
                    continue
        new_conto = str(max_conto + 1).zfill(10)

        # Delegate to GestoreDati.add_user which will serialize appropriately
        try:
            gestore.add_user(username, password, conto=new_conto)
            print(f"Utente {username} registrato con successo!")
        except Exception as e:
            raise RuntimeError(f"Impossibile salvare l'utente: {e}")
    def toggle_password(self):
        if self.pass_entry.cget('show') == '*':
              self.pass_entry.configure(show='')
              self.toggle_btn.configure(text='Nascondi')
        else:
              self.pass_entry.configure(show='*')
              self.toggle_btn.configure(text='Mostra')
    def torna_al_login(self):
        """Rimuove il frame di registrazione e mostra di nuovo il frame di login
        della finestra principale (master)."""
        try:
            # Rimuovo il frame di registrazione
            self.place_forget()
            # Se il master ha il frame_login, lo mostro
            if hasattr(self.master, "frame_login"):
                self.master.frame_login.place(relx=0.5, rely=0.5, anchor="center")
        except Exception as e:
            print(f"Errore tornando al login: {e}")