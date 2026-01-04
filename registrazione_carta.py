"""
registrazione_carta.py
Frame per l'inserimento dei dati della carta associata a un utente appena registrato.
Contiene validazioni sul numero, scadenza e CVV.
"""
import customtkinter as ctk
import gestione_json as gj
import tkinter.messagebox as mb
import tkinter as tk


class Registrazione_carta(ctk.CTkFrame):
    """Frame di registrazione carta.

    Accetta opzionalmente `username` e `titolare` per salvare i dati della carta
    associati all'utente appena registrato.
    """

    def __init__(self, master, username: str = None, titolare: str = None, **kwargs):
        super().__init__(master, width=350, height=450, fg_color="#FFFFFF", corner_radius=20, **kwargs)
        self.master = master
        self.username = username
        self.titolare = titolare
        self.setup_Registrazione_carta_widgets()

    def setup_Registrazione_carta_widgets(self):
        """Configura i widget all'interno del frame di registrazione carta."""
        # Titolo
        title_text = "Registra carta"
        if self.username:
            title_text += f" per {self.username}"
        self.title_label = ctk.CTkLabel(self, text=title_text, text_color="#000000", font=("Helvetica", 16, "bold"))
        self.title_label.pack(pady=(30, 10))

        # 1. Numero Carta (Lungo)
        self.entry_numero = ctk.CTkEntry(self, placeholder_text="numero carta", width=250,
                                         fg_color="#f0f0f0", text_color="#000000", border_color="#cccccc")
        self.entry_numero.pack(pady=10)
        # bind per limitare a 12 cifre e formattare in gruppi di 4 (mantiene placeholder)
        self.entry_numero.bind("<KeyRelease>", lambda e: self._on_numero_key())

        # Creiamo un frame per contenere i due campi piccoli
        self.row_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.row_frame.pack(pady=10)

        # Scadenza (MM/AA) con limitazione live
        self.entry_scadenza = ctk.CTkEntry(self.row_frame, placeholder_text="MM/AA", width=120,
                                           fg_color="#f0f0f0", text_color="#000000", border_color="#cccccc")
        self.entry_scadenza.pack(side="left", padx=5)
        self.entry_scadenza.bind("<KeyRelease>", lambda e: self._on_scadenza_key())

        # CVV
        self.entry_civ = ctk.CTkEntry(self.row_frame, placeholder_text="CVV", width=120,
                          fg_color="#f0f0f0", text_color="#000000", border_color="#cccccc")
        self.entry_civ.pack(side="left", padx=5)
        self.entry_civ.bind("<KeyRelease>", lambda e: self._on_cvv_key())

        # Titolare carta
        self.entry_titolare = ctk.CTkEntry(self, placeholder_text="titolare carta", width=250,
                                   fg_color="#f0f0f0", text_color="#000000", border_color="#cccccc")
        self.entry_titolare.pack(pady=10)
        # Pulsante per registrare la carta
        self.register_button = ctk.CTkButton(self, text="REGISTRA CARTA",
                                             command=self.azione_registrazione_carta,
                                             fg_color="#000000",
                                             hover_color="#333333",
                                             width=200)
        self.register_button.pack(pady=20)

    def azione_registrazione_carta(self):
        """Salva i dati della carta nel JSON e torna al login/area principale."""
        numero_carta = self.entry_numero.get().strip()
        scadenza = self.entry_scadenza.get().strip()
        civ = self.entry_civ.get().strip()

        if not self.username:
            mb.showerror("Errore", "Nome utente non specificato. Impossibile salvare la carta.")
            return

        # Validazione centralizzata
        ok, msg = self._validate_card_fields(numero_carta, scadenza, civ)
        if not ok:
            mb.showerror("Errore", msg)
            return

        numero_pulito = numero_carta.replace(" ", "")

        gestore = gj.GestoreDati()
        success = gestore.update_user_card(self.username, numero_pulito, self.titolare or "", scadenza, civ)
        if success:
            mb.showinfo("OK", "Dati carta salvati con successo.")
            # Torna al login (se presente) o rimuovi il frame
            try:
                self.place_forget()
                if hasattr(self.master, "frame_login"):
                    self.master.frame_login.place(relx=0.5, rely=0.5, anchor="center")
            except Exception:
                pass
        else:
            mb.showerror("Errore", "Impossibile salvare i dati della carta.")

    def _validate_card_fields(self, numero_carta: str, scadenza: str, civ: str):
        """Verifica che i campi carta rispettino i limiti:
        - numero carta: 12 cifre numeriche (spazi permessi, vengono rimossi)
        - scadenza: formato MM/AA dove MM 01-12 e AA due cifre
        - CVV: esattamente 3 cifre
        Restituisce (True, '') se OK, altrimenti (False, messaggio).
        """
        if not numero_carta:
            return False, "Inserisci il numero della carta"
        numero_pulito = numero_carta.replace(" ", "")
        if not numero_pulito.isdigit():
            return False, "Il numero della carta deve contenere solo cifre (spazi consentiti)"
        if len(numero_pulito) != 12:
            return False, "Il numero carta deve contenere esattamente 12 cifre"

        if not scadenza:
            return False, "Inserisci la data di scadenza nel formato MM/AA"
        import re
        if not re.match(r'^(0[1-9]|1[0-2])\/\d{2}$', scadenza):
            return False, "La scadenza deve essere nel formato MM/AA (es. 08/26)"

        if not civ:
            return False, "Inserisci il CVV (3 cifre)"
        if not civ.isdigit() or len(civ) != 3:
            return False, "Il CVV deve contenere esattamente 3 cifre numeriche"

        return True, ""

    def _on_scadenza_change(self):
        v = self.entry_scadenza.get()
        # prendi solo cifre
        digits = ''.join(ch for ch in v if ch.isdigit())
        if len(digits) > 4:
            digits = digits[:4]
        # inserisci slash dopo MM
        if len(digits) <= 2:
            formatted = digits
        else:
            formatted = digits[:2] + '/' + digits[2:]
        # se primo valore mese > 12, limitiamo a 12
        if len(digits) >= 2:
            try:
                mm = int(digits[:2])
                if mm < 1:
                    mm = 1
                if mm > 12:
                    mm = 12
                mm_str = f"{mm:02d}"
                if len(digits) <= 2:
                    formatted = mm_str
                else:
                    formatted = mm_str + '/' + digits[2:]
            except Exception:
                pass
        if formatted != v:
            self.entry_scadenza.delete(0, 'end')
            self.entry_scadenza.insert(0, formatted)

    def _on_numero_change(self):
        v = self.entry_numero.get()
        # estrai solo cifre
        digits = ''.join(ch for ch in v if ch.isdigit())
        # tronca a 12 cifre
        if len(digits) > 12:
            digits = digits[:12]
        # formatta in gruppi di 4 per leggibilità: 1234 5678 9012
        parts = [digits[i:i+4] for i in range(0, len(digits), 4)]
        formatted = ' '.join(parts)
        if formatted != v:
            self.entry_numero.delete(0, 'end')
            self.entry_numero.insert(0, formatted)

    def _on_cvv_change(self):
        v = self.entry_civ.get()
        digits = ''.join(ch for ch in v if ch.isdigit())
        if len(digits) > 3:
            digits = digits[:3]
        if digits != v:
            self.entry_civ.delete(0, 'end')
            self.entry_civ.insert(0, digits)

    # wrapper per bind
    def _on_numero_key(self):
        self._on_numero_change()

    def _on_cvv_key(self):
        self._on_cvv_change()

    def _on_scadenza_key(self):
        self._on_scadenza_change()
        