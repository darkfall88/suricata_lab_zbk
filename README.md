# Pokročilá konfigurace Suricata IPS – Streamlit dokumentace

**Autoři:** Oryna Borovyk (`bor0250`) a David Kunčík (`kun212`).

**Experimentální měření:** 17. 11. 2026.

Cíl: **jednoduchá webová dokumentace skutečného fyzického zapojení a naměřených experimentů**. Data jsou připravená pro `pandas`/Streamlit. Archiv není nová simulace a neobsahuje uměle vytvořené výsledky.

## Rychlé použití

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app_preview.py
```

V PowerShellu místo `source ...` spusťte `.venv\Scripts\Activate.ps1`.

`app_preview.py` je samostatná česká webová dokumentace experimentů. Tabulky `data/*.csv` a `data/*.json` lze případně používat také nezávisle na aplikaci.

## Obsah složky `data/`

| Soubor | Co obsahuje |
|---|---|
| `tcp_timeseries.csv` | Původní intervalové hodnoty pro 30s TCP (Linux/Windows), 600s TCP (Linux/Windows), plus 30s 1-stream Linux aktivní část; celkem 210 řádků |
| `tcp_summary.csv` | Průměry intervalů a poznámky ke známým timeoutům / zkreslenému celkovému souhrnu |
| `udp_tests.csv` | Původní a opakované UDP experimenty: `server_loss_pct` zůstává **prázdné**, pokud celý test nebyl spolehlivě vyhodnocen |
| `latency.csv` | Výsledky dvou `ping` testů, přímo z poskytnutého terminálového textu |
| `suricata_cpu_memory.csv` | 125 vzorků `pidstat` po 5 s, tj. 625 s; CPU a RSS procesu Suricata |
| `suricata_cpu_summary.csv` | Průměrné CPU/RSS z 30s TCP, tří UDP zátěží a 600s monitoringu |
| `kernel_snapshots.csv` | Jednotlivé snímky kumulativních čítačů z chatu a příznaky porovnatelnosti |
| `http_rules.csv` | 10 signatur z poskytnuté **vzorové** sady `http_v2_ips.rules` |
| `http_test_cases.csv` | 20 scénářů ze skriptu `http_advanced_v2.py`; **pozorované výsledky prázdné**, čekají na skutečné výstupy |
| `lab_setup.json` | Zadané laboratorní zapojení a jeho známé parametry |
| `metrics.json` | Krátká sada KPI pro úvodní stránku Streamlitu |
