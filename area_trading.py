"""
area_trading.py
Interfaccia principale per area trading: mostra menu a sinistra e grafico a candele al centro.
Commenti e testi in questo file sono in italiano per chiarezza.
"""
import customtkinter as ctk
import gbm
import gestione_json as gj
import tkinter.messagebox as mb
import json
from datetime import datetime, timedelta
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import Rectangle
 


class App(ctk.CTkFrame):
    def __init__(self, master, username: str = None, **kwargs):
        super().__init__(master, width=350, height=450, fg_color="#FFFFFF", corner_radius=20, **kwargs)
        self.master = master
        self.username = username
        self.chart_toplevel = None
        self.current_symbol = None
        self.last_price = None
        self._load_registry()
        self.create_widgets()

    def _load_registry(self):
        try:
            with open('registro_crypto.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception:
            data = []
        # map symbol -> entry
        self.registry = {item.get('symbol'): item for item in data}

    def create_widgets(self):
        # Left column for buttons, aligned to left and smaller width
        left = ctk.CTkFrame(self, width=220, fg_color="#121212")
        left.pack(side='left', anchor='w', padx=12, pady=12, fill='y')

        # app title / logo area
        self.app_label = ctk.CTkLabel(left, text="CryptoSim", text_color="white", font=("Helvetica", 16, "bold"))
        self.app_label.pack(pady=(8,18))

        btn_kwargs = dict(fg_color="#000000", hover_color="#871515ff", width=140, corner_radius=8)

        self.vtx_btn = ctk.CTkButton(left, text="VTX", command=lambda: self.open_chart('VTX'), **btn_kwargs)
        self.vtx_btn.pack(pady=8, anchor='w')

        self.ate_btn = ctk.CTkButton(left, text="ATE", command=lambda: self.open_chart('ATE'), **btn_kwargs)
        self.ate_btn.pack(pady=8, anchor='w')

        self.obs_btn = ctk.CTkButton(left, text="OBS", command=lambda: self.open_chart('OBS'), **btn_kwargs)
        self.obs_btn.pack(pady=8, anchor='w')

        self.zph_btn = ctk.CTkButton(left, text="ZPH", command=lambda: self.open_chart('ZPH'), **btn_kwargs)
        self.zph_btn.pack(pady=8, anchor='w')


        # Center area: wrapper to center the chart while keeping left menu
        center_wrapper = ctk.CTkFrame(self, fg_color="transparent")
        center_wrapper.pack(side='left', fill='both', expand=True)

        # header above chart: shows selected symbol and live price
        header = ctk.CTkFrame(center_wrapper, fg_color="transparent")
        header.pack(fill='x', pady=(12,4))
        self.symbol_label = ctk.CTkLabel(header, text="Seleziona asset", font=("Helvetica", 18, "bold"))
        self.symbol_label.pack(side='left', padx=12)
        self.price_label = ctk.CTkLabel(header, text="--", font=("Helvetica", 14))
        self.price_label.pack(side='left', padx=8)

        # chart container centered inside center_wrapper
        self.chart_container = ctk.CTkFrame(center_wrapper, fg_color="#0b0b0b", corner_radius=12)
        self.chart_container.pack(padx=20, pady=6, anchor='center', expand=True, fill='both')

        # control area under the chart (Buy/Sell)
        self.control_frame = ctk.CTkFrame(center_wrapper, fg_color="transparent")
        self.control_frame.pack(pady=(6,12))

        self.buy_btn = ctk.CTkButton(self.control_frame, text="⬆ BUY", fg_color="#007f3d", hover_color="#009f4d", command=self.buy_crypto, width=140, corner_radius=12, font=("Helvetica", 12, "bold"))
        self.buy_btn.pack(side='left', padx=10)
        self.sell_btn = ctk.CTkButton(self.control_frame, text="⬇ SELL", fg_color="#8b0000", hover_color="#aa0000", command=self.sell_crypto, width=140, corner_radius=12, font=("Helvetica", 12, "bold"))
        self.sell_btn.pack(side='left', padx=10)

        # footer showing user balance and holdings with stylized cards
        footer = ctk.CTkFrame(self, height=90, fg_color="transparent")
        footer.pack(side='bottom', fill='x', padx=12, pady=8)
        left_card = ctk.CTkFrame(footer, fg_color="#1e1e1e", corner_radius=12)
        left_card.pack(side='left', padx=12, pady=6, ipadx=8, ipady=8)
        self.balance_label = ctk.CTkLabel(left_card, text="Saldo: --", text_color="#ffffff", anchor='w', font=("Helvetica", 12, "bold"))
        self.balance_label.pack()
        right_card = ctk.CTkFrame(footer, fg_color="#1e1e1e", corner_radius=12)
        right_card.pack(side='right', padx=12, pady=6, ipadx=8, ipady=8)
        self.holdings_label = ctk.CTkLabel(right_card, text="Holdings: --", text_color="#ffffff", anchor='e', font=("Helvetica", 12))
        self.holdings_label.pack()

        # prepare matplotlib figure embedded in the frame (initially empty)
        fig = Figure(figsize=(6, 4), dpi=100)
        ax = fig.add_subplot(111)
        ax.set_facecolor('#0b0b0b')
        fig.patch.set_facecolor('#0b0b0b')
        # nicer default styling
        ax.grid(True, color='#1f1f1f', linestyle='--', linewidth=0.5, alpha=0.6)
        ax.spines['bottom'].set_color('#444444')
        ax.spines['left'].set_color('#444444')
        ax.tick_params(colors='#cccccc')

        canvas = FigureCanvasTkAgg(fig, master=self.chart_container)
        canvas.get_tk_widget().pack(fill='both', expand=True)

        # store references for later updates
        self.chart_fig = fig
        self.chart_ax = ax
        self.chart_canvas = canvas
        self._running = False

        # refresh user info display
        self.refresh_user_portfolio()

    def open_chart(self, symbol):
        """
        Apre un riquadro rettangolare al centro con il grafico a candele Plotly.
        Il grafico viene aggiornato periodicamente generando nuovi dati GBM.
        """
        params = self.registry.get(symbol)
        if not params:
            return

        # stop any previous update loop
        self._running = False

        # clear previous canvas widget inside chart_container and recreate canvas
        try:
            for child in list(self.chart_container.children.values()):
                try:
                    child.destroy()
                except Exception:
                    pass
        except Exception:
            pass

        # recreate figure and canvas for the selected symbol
        fig = Figure(figsize=(6, 4), dpi=100)
        ax = fig.add_subplot(111)
        ax.set_facecolor('#0b0b0b')
        fig.patch.set_facecolor('#0b0b0b')
        ax.grid(True, color='#1f1f1f', linestyle='--', linewidth=0.5, alpha=0.6)
        ax.spines['bottom'].set_color('#444444')
        ax.spines['left'].set_color('#444444')
        ax.tick_params(colors='#cccccc')

        canvas = FigureCanvasTkAgg(fig, master=self.chart_container)
        canvas.get_tk_widget().pack(fill='both', expand=True)

        self.chart_fig = fig
        self.chart_ax = ax
        self.chart_canvas = canvas

        # remember current symbol and set running to start update loop (embedded in same frame)
        self.current_symbol = symbol
        self._running = True
        # set title once to keep the selected symbol fixed
        try:
            self.chart_ax.set_title(f"{symbol} — realtime (simulato)", color='white')
        except Exception:
            pass
        # initialize a stable y-range holder (will expand only when needed)
        self._y_min = None
        self._y_max = None
        self._start_update_loop(symbol, params)

    def _start_update_loop(self, symbol, params):
        # generate and update every 1.5 seconds
        def loop():
            if not getattr(self, '_running', False):
                return
            # create data
            initial = params.get('initial_price', 100.0)
            mu = params.get('mu', 0.0)
            sigma = params.get('sigma', 0.1)

            # generate a sequence of closes
            closes = gbm.generate_price_series(initial, mu, sigma, steps=60)

            # create OHLC from closes (simple method: open=prev close, high/low with small jitter)
            opens = [closes[0]] + closes[:-1]
            highs = []
            lows = []
            for o, c in zip(opens, closes):
                hi = max(o, c) * (1 + abs(0.02 * random_factor()))
                lo = min(o, c) * (1 - abs(0.02 * random_factor()))
                highs.append(round(hi,2))
                lows.append(round(lo,2))

            # timestamps for x axis
            now = datetime.now()
            times = [(now - timedelta(seconds=(len(closes)-i)*5)).strftime('%H:%M:%S') for i in range(len(closes))]

            # draw candlestick on Matplotlib axes
            ax = self.chart_ax
            fig = self.chart_fig
            ax.clear()
            ax.set_facecolor('#111111')
            ax.tick_params(colors='white')

            # compute min/max and update stable y-range
            new_min = min(lows) if lows else min(closes)
            new_max = max(highs) if highs else max(closes)
            # use tighter padding and allow gradual contraction to lower the visible scale
            if self._y_min is None or self._y_max is None:
                self._y_min = new_min * 0.999
                self._y_max = new_max * 1.001
            else:
                # immediate expansion if data exceeds current bounds
                if new_min < self._y_min:
                    self._y_min = new_min * 0.999
                if new_max > self._y_max:
                    self._y_max = new_max * 1.001
                # gradual contraction towards tighter bounds to reduce excessive height
                target_min = new_min * 0.999
                target_max = new_max * 1.001
                alpha = 0.15
                if target_min > self._y_min:
                    self._y_min = self._y_min + (target_min - self._y_min) * alpha
                if target_max < self._y_max:
                    self._y_max = self._y_max + (target_max - self._y_max) * alpha

            # draw candlesticks
            for i, (o, h, l, c) in enumerate(zip(opens, highs, lows, closes)):
                color = '#00ff00' if c >= o else '#ff3333'
                # wick
                ax.plot([i, i], [l, h], color='white', linewidth=0.8)
                # body
                lower = min(o, c)
                height = max(0.0001, abs(c - o))
                rect = Rectangle((i - 0.3, lower), 0.6, height, facecolor=color, edgecolor='black')
                ax.add_patch(rect)

            # store last price for buy/sell actions
            try:
                self.last_price = float(closes[-1])
            except Exception:
                self.last_price = None
            # aggiorna etichetta prezzo in header (UI più gradevole)
            try:
                if self.last_price is not None:
                    self.price_label.configure(text=f"{self.last_price:.2f} $")
                else:
                    self.price_label.configure(text="--")
            except Exception:
                pass

            ax.set_xlim(-1, len(closes))
            # place time labels sparsely
            step = max(1, len(times)//8)
            ax.set_xticks([i for i in range(0, len(times), step)])
            ax.set_xticklabels([times[i] for i in range(0, len(times), step)], rotation=45, color='white')
            ax.set_ylabel('Prezzo', color='white')
            # apply the stable y-limits to avoid jittering of y-axis
            try:
                if self._y_min is not None and self._y_max is not None:
                    ax.set_ylim(self._y_min, self._y_max)
            except Exception:
                pass
                # subtle background for chart container
                try:
                    self.chart_container.configure(fg_color="#071018")
                except Exception:
                    pass
            fig.tight_layout()
            try:
                self.chart_canvas.draw_idle()
            except Exception:
                try:
                    self.chart_canvas.draw()
                except Exception:
                    pass

            # update displayed user portfolio (balance / holdings)
            try:
                self.refresh_user_portfolio()
            except Exception:
                pass

            # schedule next using the frame's after (embedded view)
            if getattr(self, '_running', False):
                try:
                    # call again after 1500 ms
                    self.after(1500, loop)
                except Exception:
                    pass

        # start once
        loop()

    def _get_user_record(self):
        if not self.username:
            return None, None
        gest = gj.GestoreDati()
        dati = gest.deserializza()
        # normalize dict format -> list of objects so callers always get a mutable record dict
        if isinstance(dati, dict):
            lista = []
            for u, p in dati.items():
                lista.append({"username": u, "password": p, "conto": ""})
            # find the record in the normalized list
            rec = next((it for it in lista if it.get('username') == self.username), None)
            return lista, rec
        if isinstance(dati, list):
            rec = next((it for it in dati if it.get('username') == self.username), None)
            return dati, rec
        return dati, None

    def _save_user_record(self, all_data):
        gest = gj.GestoreDati()
        gest.serializza(all_data)

    def refresh_user_portfolio(self):
        # Read user info and update footer labels
        all_data, record = self._get_user_record()
        balance = "--"
        holdings_text = "--"
        if record:
            # record may be dict (from list) or password string (from dict format)
            if isinstance(record, dict):
                # try several common keys
                bal = record.get('conto') or record.get('conto $') or record.get('balance')
                try:
                    balance = f"Saldo: {float(bal):.2f}" if bal is not None and str(bal).strip() != '' else "Saldo: 0.00"
                except Exception:
                    balance = f"Saldo: {bal}"
                # holdings: expect a dict under 'holdings' mapping symbol->qty
                holdings = record.get('holdings') or {}
                if isinstance(holdings, dict) and holdings:
                    holdings_text = ', '.join([f"{k}:{v}" for k, v in holdings.items()])
                else:
                    holdings_text = 'Nessuna crypto'
        self.balance_label.configure(text=balance)
        self.holdings_label.configure(text=holdings_text)

    def buy_crypto(self):
        # simple buy 1 unit of current symbol at last_price
        if not self.username:
            mb.showerror('Errore', 'Utente non disponibile')
            return
        if not self.current_symbol or not self.last_price:
            mb.showerror('Errore', 'Seleziona un asset prima di comprare')
            return
        all_data, record = self._get_user_record()
        if record is None:
            mb.showerror('Errore', 'Record utente non trovato')
            return
        # ensure numeric balance
        bal = record.get('conto') or record.get('conto $') or record.get('balance') or 0
        try:
            bal_val = float(bal)
        except Exception:
            bal_val = 0.0
        price = float(self.last_price)
        if bal_val < price:
            mb.showerror('Saldo insufficiente', 'Non hai abbastanza saldo per comprare 1 unità')
            return
        bal_val -= price
        # update holdings
        holdings = record.get('holdings') or {}
        if not isinstance(holdings, dict):
            holdings = {}
        holdings[self.current_symbol] = holdings.get(self.current_symbol, 0) + 1
        record['holdings'] = holdings
        # store balance under 'conto'
        record['conto'] = f"{bal_val:.2f}"
        # save back
        self._save_user_record(all_data)
        mb.showinfo('Compra', f'Comprato 1 {self.current_symbol} @ {price:.2f}')
        self.refresh_user_portfolio()

    def sell_crypto(self):
        # simple sell 1 unit of current symbol at last_price
        if not self.username:
            mb.showerror('Errore', 'Utente non disponibile')
            return
        if not self.current_symbol or not self.last_price:
            mb.showerror('Errore', 'Seleziona un asset prima di vendere')
            return
        all_data, record = self._get_user_record()
        if record is None:
            mb.showerror('Errore', 'Record utente non trovato')
            return
        holdings = record.get('holdings') or {}
        if not isinstance(holdings, dict) or holdings.get(self.current_symbol, 0) < 1:
            mb.showerror('Errore', 'Non possiedi unità da vendere')
            return
        holdings[self.current_symbol] = holdings.get(self.current_symbol, 0) - 1
        if holdings[self.current_symbol] <= 0:
            del holdings[self.current_symbol]
        record['holdings'] = holdings
        # add cash
        bal = record.get('conto') or record.get('conto $') or record.get('balance') or 0
        try:
            bal_val = float(bal)
        except Exception:
            bal_val = 0.0
        price = float(self.last_price)
        bal_val += price
        record['conto'] = f"{bal_val:.2f}"
        self._save_user_record(all_data)
        mb.showinfo('Vendita', f'Venduto 1 {self.current_symbol} @ {price:.2f}')
        self.refresh_user_portfolio()


def random_factor():
    # small helper to generate gaussian factor without importing at top-level within Tkinter UI
    try:
        import random as _r
        return _r.gauss(0,1)
    except Exception:
        return 0
 
                 
                 
                 