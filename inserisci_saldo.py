import customtkinter as ctk
import gestione_json as gj
import tkinter.messagebox as mb


class InserisciSaldo(ctk.CTkFrame):
    def __init__(self, master, username: str, on_confirm=None, **kwargs):
        super().__init__(master, width=400, height=200, fg_color="#FFFFFF", corner_radius=12, **kwargs)
        self.master = master
        self.username = username
        self.on_confirm = on_confirm
        self.setup_ui()

    def setup_ui(self):
        title = ctk.CTkLabel(self, text="Inserisci importo da addebitare dalla carta", font=("Helvetica", 15, "bold"), text_color="#FFFFFF")
        title.pack(pady=(20, 10))

        self.amount_entry = ctk.CTkEntry(self, placeholder_text="Importo (es. 50.00)", width=250, fg_color="#1b1b1b", text_color="#FFFFFF", border_color="#333333")
        self.amount_entry.pack(pady=8)

        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=(10, 20))

        self.confirm_btn = ctk.CTkButton(btn_frame, text="Conferma", fg_color="#006600", hover_color="#008800", command=self.confirm)
        self.confirm_btn.pack(side='left', padx=8)

        self.cancel_btn = ctk.CTkButton(btn_frame, text="Annulla", fg_color="#800000", hover_color="#aa0000", command=self.cancel)
        self.cancel_btn.pack(side='left', padx=8)

    def confirm(self):
        val = self.amount_entry.get().strip()
        if not val:
            mb.showerror('Errore', 'Inserisci un importo valido')
            return
        try:
            amt = float(val.replace(',','.'))
        except Exception:
            mb.showerror('Errore', 'Importo non valido')
            return

        # Aggiorna il file utenti con il nuovo saldo aggiunto
        gest = gj.GestoreDati()
        dati = gest.deserializza()

        # normalize to list of dicts
        if isinstance(dati, dict):
            dati = [{ 'username': u, 'password': p, 'conto': "0" } for u, p in dati.items()]

        updated = False
        if isinstance(dati, list):
            for item in dati:
                if item.get('username') == self.username:
                    bal = item.get('conto') or item.get('conto $') or item.get('balance') or 0
                    try:
                        bal_val = float(str(bal).replace(',','.'))
                    except Exception:
                        bal_val = 0.0
                    bal_val += amt
                    item['conto'] = f"{bal_val:.2f}"
                    updated = True
                    break

        if updated:
            gest.serializza(dati)
            mb.showinfo('Saldo', f'Importo aggiunto: {amt:.2f}')
            # chiudi questo frame e chiama la callback
            try:
                self.place_forget()
            except Exception:
                pass
            if callable(self.on_confirm):
                try:
                    self.on_confirm(self.username)
                except Exception:
                    pass
        else:
            mb.showerror('Errore', 'Utente non trovato')

    def cancel(self):
        try:
            self.place_forget()
        except Exception:
            pass
        # Ri-mostra il frame di login se presente
        try:
            if hasattr(self.master, 'frame_login'):
                self.master.frame_login.place(relx=0.5, rely=0.5, anchor="center")
        except Exception:
            pass
