"""
gestione_json.py
Gestore per serializzazione/deserializzazione degli utenti su file JSON.
Fornisce funzioni per leggere, salvare e aggiornare i dati utenti preservando
il formato originale (dict legacy o lista di oggetti).
"""
import json
import os
from typing import Any


class GestoreDati:
    def __init__(self, nome_file: str = "registro_utenti.json"):
        self.nome_file = nome_file

    def serializza(self, dati: Any) -> None:
        """Salva una struttura Python (dict o list) in JSON mantenendo indentazione e unicode.
        Usa `ensure_ascii=False` per preservare caratteri non-ASCII e `indent=4`
        per mantenere la formattazione leggibile.
        """
        try:
            with open(self.nome_file, "w", encoding="utf-8") as file:
                json.dump(dati, file, ensure_ascii=False, indent=4, separators=(",", ": "))
            print(f"Dati salvati correttamente in {self.nome_file}")
        except Exception as e:
            print(f"Errore durante il salvataggio: {e}")

    def deserializza(self) -> Any:
        """Legge il file JSON e restituisce la struttura Python (list o dict).

        Se il file non esiste restituisce una lista vuota (il progetto usa file con array top-level).
        In caso di JSON non valido stampa l'errore e restituisce una struttura vuota dello stesso tipo.
        """
        if not os.path.exists(self.nome_file):
            print("Il file non esiste. Restituisco una lista vuota.")
            return []

        try:
            with open(self.nome_file, "r", encoding="utf-8") as file:
                dati = json.load(file)
                return dati
        except json.JSONDecodeError as e:
            print(f"JSON non valido in {self.nome_file}: {e}")
            return []
        except Exception as e:
            print(f"Errore durante la lettura: {e}")
            return []

    def _is_array_utenti(self, dati: Any) -> bool:
        """Rileva se il formato è una lista di oggetti utente
        es. [{"username":..., "password":...}, ...]
        """
        if not isinstance(dati, list):
            return False
        for item in dati:
            if not isinstance(item, dict):
                return False
            if 'username' not in item or 'password' not in item:
                return False
        return True

    def get_users_dict(self) -> dict:
        """Restituisce un dizionario username->password indipendentemente
        dal formato sul disco (array o dict).
        """
        dati = self.deserializza()
        if isinstance(dati, dict):
            return dict(dati)
        if self._is_array_utenti(dati):
            return {item['username']: item['password'] for item in dati}
        return {}

    def add_user(self, username: str, password: str, conto: str = "") -> None:
        """Aggiunge o aggiorna un utente preservando il formato originale del file.

        Supporta opzionalmente anche i campi carta (numero carta, titolare, scadenza, cvv).
        Se il file è in formato dict e vengono forniti campi aggiuntivi, converte il dict
        in lista di oggetti per preservare i nuovi campi.
        """
        dati = self.deserializza()
        # Normalizzazione dei parametri opzionali non specificati
        # (funzione mantenuta compatibile con chiamate esistenti)
        # Se il file è dict e non servono campi extra, manteniamo il comportamento legacy
        if isinstance(dati, dict):
            # Non trasformiamo il formato dict in list se non servono campi extra
            dati[username] = password
            self.serializza(dati)
            return

        # list format
        if self._is_array_utenti(dati):
            # cerca utente e aggiorna
            for item in dati:
                if item.get('username') == username:
                    item['password'] = password
                    if conto:
                        item['conto'] = conto
                    self.serializza(dati)
                    return
            # non trovato -> aggiungi
            nuovo = {"username": username, "password": password, "conto": conto}
            dati.append(nuovo)
            self.serializza(dati)
            return

        # formato non riconosciuto o file vuoto -> creo lista
        lista = [{"username": username, "password": password, "conto": conto}]
        self.serializza(lista)

    def check_credentials(self, username: str, password: str) -> bool:
        """Verifica credenziali con indipendenza dal formato sottostante."""
        users = self.get_users_dict()
        return username in users and users[username] == password

    def update_user_card(self, username: str, numero_carta: str, titolare: str, scadenza: str, cvv: str) -> bool:
        """Aggiorna o aggiunge i dati della carta per l'utente specificato.

        Ritorna True se l'operazione ha avuto successo, False altrimenti.
        """
        dati = self.deserializza()
        # Se il file è dict, convertiamo in lista per poter memorizzare i campi aggiuntivi
        if isinstance(dati, dict):
            dati = [{"username": u, "password": p, "conto": ""} for u, p in dati.items()]

        if isinstance(dati, list):
            for item in dati:
                if item.get('username') == username:
                    item['numero carta'] = numero_carta
                    item['titolare carta'] = titolare
                    item['scadenza carta'] = scadenza
                    item['cvv carta'] = cvv
                    self.serializza(dati)
                    return True
            # se utente non trovato, aggiungiamo un nuovo oggetto (con password vuota)
            nuovo = {
                "username": username,
                "password": "",
                "conto": "",
                "numero carta": numero_carta,
                "titolare carta": titolare,
                "scadenza carta": scadenza,
                "cvv carta": cvv,
            }
            dati.append(nuovo)
            self.serializza(dati)
            return True

        return False

    def get_user_info(self, username: str) -> dict:
        """Restituisce il record completo dell'utente se presente, altrimenti {}."""
        dati = self.deserializza()
        if isinstance(dati, dict):
            if username in dati:
                return {"username": username, "password": dati[username]}
            return {}

        if isinstance(dati, list):
            for item in dati:
                if item.get('username') == username:
                    return item
        return {}

        

