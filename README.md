# Genesis Trade

Un'applicazione desktop di simulazione trading di criptovalute scritta in Python con interfaccia grafica moderna.

## Descrizione

**Genesis Trade** è una piattaforma di trading simulato che consente agli utenti di esercitarsi nel trading di criptovalute in un ambiente virtuale sicuro. L'applicazione simula il comportamento di mercato di 4 asset digitali utilizzando il modello **Geometric Brownian Motion (GBM)**, uno dei modelli più accurati per la simulazione di serie storiche finanziarie.

### Caratteristiche principali

- **Autenticazione utente**: Registrazione e login sicuri con validazione delle credenziali
- **Gestione portafoglio**: Acquisto e vendita di criptovalute con tracciamento del bilancio
- **Simulazione di mercato realistica**: Utilizzo di GBM per generare movimenti di prezzo naturalistici
- **Interfaccia grafica intuitiva**: Dashboard moderna con grafici a candele (candlestick)
- **Gestione carta di credito**: Registrazione e gestione dei metodi di pagamento
- **Persistenza dei dati**: Salvataggio automatico su file JSON di utenti, portafogli e transazioni

## Tecnologie utilizzate

- **Python 3.x**: Linguaggio di programmazione
- **CustomTkinter**: Libreria GUI moderna per Tkinter
- **Matplotlib**: Generazione e visualizzazione di grafici
- **NumPy**: Calcoli numerici e generazione di valori casuali
- **JSON**: Persistenza dati

## Prerequisiti

- Python 3.7 o superiore
- pip (gestore pacchetti Python)

## Installazione

### 1. Clona o scarica il repository

```bash
git clone https://github.com/user/genesis-trade.git
cd genesis-trade
```

### 2. Installa le dipendenze

```bash
pip install -r requirements.txt
```

Le dipendenze richieste sono:
- `matplotlib` - per i grafici
- `customtkinter` - per l'interfaccia grafica
- `numpy` - per i calcoli numerici

## Utilizzo

### Avvio dell'applicazione

```bash
python main.py
```

L'applicazione si avvierà in modalità fullscreen e mostrerà la schermata di login.

### Workflow utente

1. **Registrazione**: 
   - Clicca su "REGISTRATI"
   - Inserisci username (minimo 3 caratteri) e password robusta
   - La password deve contenere: maiuscole, minuscole, numeri e simboli speciali (@$!%*?&) con lunghezza minima di 8 caratteri
   - Registra i dati della tua carta

2. **Login**:
   - Inserisci credenziali
   - Accedi all'area trading

3. **Trading**:
   - Seleziona un asset cliccando i pulsanti: VTX, ATE, OBS, ZPH
   - Visualizza il grafico in tempo reale con aggiornamento dei prezzi
   - Clicca **BUY** per acquistare o **SELL** per vendere
   - Monitora il tuo portafoglio e saldo

## Struttura del progetto

```
genesis-trade/
├── main.py                    # Punto di ingresso dell'applicazione
├── schermata_iniziale.py      # Schermata di login e registrazione
├── registrati.py              # Frame di registrazione nuovo utente
├── registrazione_carta.py     # Frame di registrazione carta di credito
├── area_trading.py            # Dashboard principale di trading
├── gbm.py                     # Generatore prezzi con Geometric Brownian Motion
├── gestione_json.py           # Gestore persistenza dati utenti
├── inserisci_saldo.py         # Frame per l'inserimento del saldo
├── validazione.py             # Funzioni di validazione input
├── registro_utenti.json       # Database utenti e portafogli
├── registro_crypto.json       # Configurazione degli asset
├── requirements.txt           # Dipendenze Python
├── README.md                  # Questo file
└── LICENSE                    # Licenza del progetto
```

## Descrizione dei file principali

### `gbm.py`
Implementa il modello Geometric Brownian Motion per la simulazione realistica dei prezzi delle criptovalute:
- `genera_prossimo_prezzo()`: Genera il prossimo prezzo basato sul trend e volatilità
- `generate_price_series()`: Genera una serie di prezzi storica

### `gestione_json.py`
Gestisce la persistenza dei dati:
- Lettura e scrittura su JSON
- Gestione utenti, portafogli e carte di credito
- Supporto per formati legacy e nuovi

### `area_trading.py`
Interfaccia principale con:
- Menu di selezione asset
- Grafico a candele in tempo reale
- Pulsanti Buy/Sell
- Visualizzazione portafoglio e saldo

## Asset disponibili

| Nome | Simbolo | Prezzo iniziale | Descrizione |
|------|---------|-----------------|-------------|
| Vortex Coin | VTX | $1926.00 | Crescita organica, volatilità controllata (20%) |
| Aetherius | ATE | $569.43 | Alta crescita speculativa, trend rialzista |
| Obsidian | OBS | $1264.69 | Asset stabile, riserva di valore, volatilità bassa |
| Zephyr | ZPH | $842.15 | Asset speculativo, alta instabilità, bias ribassista |

## Validazione input

### Password
- Lunghezza minima: 8 caratteri
- Deve contenere: maiuscole, minuscole, numeri, simboli speciali

### Carta di credito
- Numero carta: 12 cifre numeriche
- Scadenza: formato MM/AA (es. 12/26)
- CVV: esattamente 3 cifre

## Note tecniche

### Geometric Brownian Motion (GBM)
La formula utilizzata è:
$$dS = \mu S \, dt + \sigma S \, dW$$

Dove:
- $S$ = prezzo dell'asset
- $\mu$ = drift (trend)
- $\sigma$ = volatilità
- $dW$ = incremento browniano (numero casuale gaussiano)

### Persistenza dati
I dati vengono salvati in JSON con la seguente struttura:

**registro_utenti.json**:
```json
[
  {
    "username": "user",
    "password": "hash",
    "numero carta": "XXXX",
    "titolare carta": "Nome",
    "scadenza carta": "MM/AA",
    "cvv carta": "XXX",
    "conto": "1000.00",
    "holdings": {"VTX": 5, "ATE": 2}
  }
]
```

## Possibili miglioramenti futuri

- [ ] Autenticazione con hash delle password (bcrypt/argon2)
- [ ] Database relazionale (SQLite/PostgreSQL) al posto di JSON
- [ ] Storico transazioni completo
- [ ] Export dati in CSV/Excel
- [ ] Grafici candlestick più avanzati con indicatori tecnici (RSI, MACD, etc.)
- [ ] API per dati reali
- [ ] Sistema di leaderboard
- [ ] Notifiche e alert di prezzo

## Licenza

Vedi il file [LICENSE](LICENSE) per dettagli.

## Autore

Sviluppato come progetto di simulazione trading educativo.

---

**Nota**: Questa è un'applicazione di simulazione. I dati e i prezzi non riflettono dati reali di mercato.
