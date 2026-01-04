"""
validazione.py
Contiene funzioni per la validazione di username e password.
La password deve rispettare regole di complessità (maiuscole, numeri, simboli, lunghezza).
"""
import re

def valida_password(password):
    """
    Ritorna True se la password è valida, altrimenti False.
    Regole: 8+ caratteri, Maiuscola, Minuscola, Numero, Carattere Speciale.
    """
    pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
    
    if re.match(pattern, password):
        return True
    return False

def check_username(username):
    """Esempio: lo username deve essere lungo almeno 3 caratteri"""
    return len(username.strip()) >= 3