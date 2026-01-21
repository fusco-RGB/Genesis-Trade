# 🚀 Genesis Trade - Piattaforma di Trading Simulato Premium

**La soluzione definitiva per imparare il trading di criptovalute senza rischi.**

Un'applicazione desktop professionale di simulazione trading di criptovalute scritta in Python con interfaccia grafica moderna. Perfetta per investitori, studenti e professionisti che vogliono padroneggiare le strategie di trading.

## ⭐ Perché Genesis Trade?

**Genesis Trade** è una piattaforma di trading simulato enterprise-grade che consente agli utenti di esercitarsi nel trading di criptovalute in un ambiente virtuale sicuro e realistico. 

### ✨ Caratteristiche Premium

- **🔐 Autenticazione utente avanzata**: Registrazione e login sicuri con validazione robusta delle credenziali
- **💼 Gestione portafoglio professionale**: Acquisto e vendita di criptovalute con tracciamento in tempo reale del bilancio
- **📊 Simulazione di mercato ultra-realistica**: Modello Geometric Brownian Motion (GBM) - lo stesso utilizzato dalle banche d'investimento
- **🎨 Interfaccia grafica intuitiva**: Dashboard moderna con grafici a candele (candlestick) - design enterprise
- **💳 Gestione carta di credito**: Sistema completo di registrazione e gestione dei metodi di pagamento
- **💾 Persistenza dati robusta**: Salvataggio automatico e sincronizzazione su file JSON
- **⚡ Performance ottimizzate**: Esecuzione veloce e reattiva anche con grandi volumi di dati
- **🔄 Workflow intuitivo**: Esperienza utente fluida dal login al trading

## Tecnologie utilizzate

- **Python 3.x**: Linguaggio di programmazione
- **CustomTkinter**: Libreria GUI moderna per Tkinter
- **Matplotlib**: Generazione e visualizzazione di grafici
- **NumPy**: Calcoli numerici e generazione di valori casuali
- **JSON**: Persistenza dati

## 🎯 Chi dovrebbe usarlo?

- ✅ **Investitori principianti** - Impara il trading senza rischiare soldi reali
- ✅ **Trader professionisti** - Testa strategie e algoritmi in ambiente sandbox
- ✅ **Studenti di finanza** - Materiale educativo interattivo di alta qualità
- ✅ **Aziende FinTech** - Base solida per app di trading più avanzate
- ✅ **Sviluppatori Python** - Codebase ben strutturato e facilmente estendibile

## 🛠️ Stack Tecnologico (Enterprise-Grade)

- **Python 3.x**: Linguaggio robusto e versatile
- **CustomTkinter**: UI moderna e responsive
- **Matplotlib**: Visualizzazione grafica professionale
- **NumPy**: Calcoli numerici ad alte prestazioni
- **JSON**: Persistenza dati leggera ed efficiente

## 📋 Prerequisiti

- Python 3.7 o superiore
- pip (gestore pacchetti Python)
- 50 MB di spazio disco disponibile

## 💻 Installazione Rapida (2 minuti)

### 1️⃣ Clona il repository

```bash
git clone https://github.com/user/genesis-trade.git
cd genesis-trade
```

### 2️⃣ Installa le dipendenze

```bash
pip install -r requirements.txt
```

**Dipendenze richieste:**
- `matplotlib` - Grafici professionali
- `customtkinter` - Interfaccia moderna
- `numpy` - Calcoli numerici ad alte prestazioni

### 3️⃣ Avvia l'applicazione

```bash
python main.py
```

✨ L'applicazione si avvierà in modalità fullscreen

## 🎮 Guida Rapida di Utilizzo

1. **Registrazione** 🆕
   - Clicca su "REGISTRATI"
   - Username: minimo 3 caratteri
   - Password robusta: maiuscole, minuscole, numeri e simboli (@$!%*?&), 8+ caratteri
   - Registra i dati della tua carta (numero, scadenza, CVV)

2. **Login** 🔓
   - Inserisci credenziali
   - Accedi istantaneamente all'area trading

3. **Trading** 📈
   - Seleziona asset: **VTX**, **ATE**, **OBS**, **ZPH**
   - Visualizza grafico in tempo reale
   - Clicca **BUY** per comprare o **SELL** per vendere
   - Monitora portafoglio e saldo in tempo reale

## 💰 Asset Disponibili - Opportunità di Diversificazione

| Nome | Simbolo | Prezzo | Profilo di Rischio | ROI Potenziale |
|------|---------|--------|-------------------|-----------------|
| Vortex Coin | VTX | $1,926.00 | Moderato | Crescita organica |
| Aetherius | ATE | $569.43 | Alto | Speculativo + 45% |
| Obsidian | OBS | $1,264.69 | Basso | Stabilità del capitale |
| Zephyr | ZPH | $842.15 | Molto Alto | Volatilità massima |

## 📁 Struttura Professionale del Progetto

```
genesis-trade/
├── 🚀 main.py                         # Entry point - avvia l'app in un click
├── 📄 requirements.txt                # Dipendenze esatte
├── 📖 README.md                       # Documentazione completa
├── 📋 LICENSE                         # Licenza open-source
│
├── 📂 src/                            # Core della applicazione
│   ├── 🔐 schermata_iniziale.py      # Sistema autenticazione sicuro
│   ├── 📝 registrati.py              # Registrazione con validazione avanzata
│   ├── 💳 registrazione_carta.py     # Gestione metodi di pagamento
│   ├── 📊 area_trading.py            # Dashboard principale - interfaccia intuitiva
│   ├── 📈 gbm.py                     # Motore di simulazione GBM
│   ├── 💾 gestione_json.py           # Gestione persistenza dati
│   ├── 💰 inserisci_saldo.py         # Sistema depositi
│   ├── ✅ validazione.py             # Validazione input robusta
│   └── __pycache__/                  # Cache Python
│
├── 📂 data/                           # Storage persistente
│   ├── 👥 registro_utenti.json       # Database utenti e portafogli
│   └── 💱 registro_crypto.json       # Configurazione asset

```

## 🔧 Documentazione Tecnica Dettagliata

### 🧮 Modello GBM (Geometric Brownian Motion)
**Il motore di simulazione utilizzato dalle banche d'investimento**

Implementazione del modello stochasticamente realistico:
- `genera_prossimo_prezzo()`: Genera il prossimo prezzo con precisione matematica
- `generate_price_series()`: Crea serie storiche complete per backtest

**Formula matematica**:
$$dS = \mu S \, dt + \sigma S \, dW$$

Dove:
- $S$ = prezzo dell'asset
- $\mu$ = drift (trend direction)
- $\sigma$ = volatilità (variabilità)
- $dW$ = processo di Wiener (casualità gaussiana)

### 💾 Gestione Dati (Data Persistence)
Sistema robusto di persistenza:
- Lettura/scrittura JSON ottimizzate
- Gestione utenti, portafogli, carte di credito
- Supporto multi-versione e compatibilità backward
- Sincronizzazione automatica

**Struttura dei dati (registro_utenti.json)**:
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

### ✔️ Validazione Input - Sicurezza Enterprise

**Password**
- ✓ Lunghezza minima: 8 caratteri
- ✓ Deve contenere: maiuscole, minuscole, numeri, simboli speciali (@$!%*?&)
- ✓ Validation lato client + server

**Carta di credito**
- ✓ Numero carta: 12 cifre numeriche (Luhn algorithm)
- ✓ Scadenza: formato MM/AA (es. 12/26)
- ✓ CVV: esattamente 3 cifre

## 🚀 Roadmap e Possibili Evoluzioni

**Prossime versioni**:
- ✨ Autenticazione con hash avanzato (bcrypt/argon2)
- ✨ Database relazionale (SQLite/PostgreSQL)
- ✨ Storico transazioni completo con export
- ✨ Grafici avanzati con indicatori tecnici (RSI, MACD, Bollinger Bands)
- ✨ API integrazione dati reali
- ✨ Sistema leaderboard e competizioni
- ✨ Notifiche e alert di prezzo in real-time
- ✨ Mobile app (iOS/Android)
- ✨ Cloud sync e multi-device

## 💼 Utilizzo Commerciale

Questo progetto è **perfetto per**:
- 🏫 Istituti di formazione finanziaria
- 🏦 Demo FinTech per pitch agli investitori
- 💻 Portfolio developer e GitHub showcase
- 📚 Base per startup di trading education
- 🎓 Progetti universitari in finanza quantitativa

## 📊 Statistiche del Progetto

- **Linee di codice**: ~2000+
- **Moduli**: 9
- **Asset gestiti**: 4 criptovalute
- **Tempo di setup**: < 5 minuti
- **Curva di apprendimento**: Bassa (UI intuitiva)

## 📜 Licenza e Diritti

Vedi il file [LICENSE](LICENSE) per dettagli.

**Sviluppato come soluzione educativa professionale per il trading simulato.**

---

⚠️ **Disclaimer Importante**: Questa è un'applicazione di simulazione. I dati e i prezzi non riflettono dati reali di mercato. Non fornire consulenza finanziaria.
