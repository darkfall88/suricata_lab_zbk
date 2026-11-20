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

## Důležitá metodická omezení

1. **TCP 600 s:** 60 desetisekundových hodnot je kompletních na obou stranách. Windows konečný souhrn `944 Mbit/s / 603,08 s` obsahuje také ukončování spojení a `tcp recv failed: Connection timed out`. Pro graf dlouhodobého přenosu používejte **0–600 s**, nikoli závěrečný souhrn 0–603,08 s.
2. **TCP jedno spojení:** klientský souhrn `471 Mbit/s / 60,35 s` je zkreslen dlouhým ukončováním; aktivních prvních 30 s odpovídá téměř gigabitu.
3. **UDP 250M a 500M:** Windows rozdělil přenos do více relací. **Nezobrazujte** jejich velké lokální procento ztrát jako ztrátovost celého testu. Místo neznámé hodnoty je v CSV prázdno.
4. **UDP 100M:** pro výchozí Windows UDP buffer (~64 KiB) došlo ke ztrátě 1 136 z 327 684 datagramů (0,3467 %); s 1 MiB bufferem byl 0% loss.
5. **AF_PACKET:** při UDP 250M s 1MiB bufferem přibylo 27 030 `capture.kernel_drops`. Při opakovaných 100/150/200M experimentech žádné nové drops. V `kernel_snapshots.csv` se **nesmějí** odečítat snímky z neporovnatelných skupin.
6. **Stabilitní čítače:** mezi snapshoty `stability_before` a `stability_after` klesla hodnota `kernel_drops` z 196 101 na 2 800, zatímco `kernel_packets` z jiného základu výrazně vzrostla. Měření neprokazuje záporné drops ani přesný počet ztrát; příčina nesouladu nebyla doložena. Graf ze snímků proto neprezentujte jako spojitou časovou řadu.
7. **Latence:** ping pod zátěží trval ~40 s, TCP přenos ~30 s. Rozdíl RTT je popisný; neslouží jako důkaz, že IPS zlepšilo latenci oproti baseline bez IPS.
8. **CPU:** `pidstat %CPU` je procento jednoho logického CPU, nikoliv procento celých 12 CPU. 125 vzorků monitoringu zahrnuje i okrajová období mimo vlastní maximální zátěž.
9. **Bezpečnostní testy:** nahrané `.rules` a `.py` prokazují existenci připravené sady pravidel/testů, **nikoliv**, že přesně tato pravidla byla po celou dobu aktivní nebo jak dopadlo každé jednotlivé měření. Pro věrohodné výsledky doplňte originální `eve.json`, případně `scan_results/*.json`.

## Co ještě přidat

- **Fotografie fyzického zapojení: HOTOVO.** Tři fotografie z 17. 11. 2026 jsou přiloženy v `assets/photos/`, s popisky v `photos.json`; úvodní stránka je zobrazuje automaticky. Na třetím snímku je také zachycen funkční EveBox.
- **Konfigurace:** `suricata.yaml` a zaslané `.rules` už byly doplněny; `systemctl cat suricata-ips` a provozně potvrzený obsah `suricata.rules` stále chybí.
- **Události:** archivní kopie `eve.json` pro EveBox (originál raději v soukromém archivu). Pro Streamlit lze později vytvořit anonymizovaný JSONL výřez.
- **Výsledky HTTP:** konkrétní záznamy ze skriptu pro 20 pokusů, nikoliv jen jejich seznam.

## Zdroje a bezpečnost publikace

- `sources/original_upload_*.txt`: kopie poskytnutých terminálových příloh, bez úprav.
- `sources/http_advanced_v2.py`, `sources/http_v2_ips.rules`, `sources/http_v2_ids.rules`: původní experimentální podklady.
- Část UDP výsledků a všechny ping/kernelové snapshoty pocházejí z textu konverzace, nikoliv z nově pořízeného logu.
- **Složku `sources/` nepublikujte bez kontroly**: obsahuje názvy stanic a interní síťové adresy. Na veřejný Streamlit Cloud doporučuji nasazovat jen očištěná data a fotografie bez citlivých detailů.

## Doplněná fotodokumentace

Archiv nyní obsahuje `20261117_093447.jpg`, `20261117_093500.jpg`, `20261117_103908.jpg`. Síťovým infrastrukturním prvkem je dle laboratorního popisu **Cisco Catalyst C3850 – 24portový L3 switch** (nikoli obecně označený router). Fotografie dokumentují reálné propojení a práci s EveBox; u jednotlivých portů a VLAN se neopírejte pouze o obrazové důkazy.

## Aktualizace: dodaná konfigurace a pravidla (18. 11. 2026)

- `data/suricata_config_summary.json` – skutečné parametry YAML, včetně mapování AF_PACKET rozhraní a logování.
- `data/suricata_config_excerpt.yaml` – bezpečnější, krátký výňatek důležitých nastavení pro dokumentaci.
- `data/pravidla_inventar.csv` – přehled SID, akcí a zakomentovaných pravidel z poskytnutých souborů.
- `private_archive/config/` – **originální zaslané konfigurační soubory; NEVEŘEJNÉ**, `.gitignore` je vylučuje z Git repozitáře.
- `KONFIGURACE_A_METODIKA.md` – popis konfigurace a omezení, na která je potřeba upozornit při obhajobě.
- `assets/schema_zapojeni_vlan10_vlan20_16.png` – česky popsané grafické schéma sítě, obě VLAN mají masku /16.
- `app_preview.py` – doplněna sekce **Konfigurace IPS** a katalog skutečně nahraných pravidel.

**Pozor:** kompletní rule-set `suricata.rules` a soubor služby `suricata-ips.service` stále chybějí; `eve.json` již byl doplněn. Samotný YAML neprokazuje aktivní verzi pravidel během každé historické fáze testování.

## Aktualizace: dodaná konfigurace a pravidla (18. 11. 2026)

- `data/suricata_config_summary.json` – skutečné parametry YAML, včetně mapování AF_PACKET rozhraní a logování.
- `data/suricata_config_excerpt.yaml` – bezpečnější, krátký výňatek důležitých nastavení pro dokumentaci.
- `data/pravidla_inventar.csv` – přehled SID, akcí a zakomentovaných pravidel z poskytnutých souborů.
- `private_archive/config/` – **originální zaslané konfigurační soubory; NEVEŘEJNÉ**, `.gitignore` je vylučuje z Git repozitáře.
- `KONFIGURACE_A_METODIKA.md` – popis konfigurace a omezení, na která je potřeba upozornit při obhajobě.
- `assets/schema_zapojeni_vlan10_vlan20_16.png` – česky popsané grafické schéma sítě, obě VLAN mají masku /16.
- `app_preview.py` – doplněna sekce **Konfigurace IPS** a katalog skutečně nahraných pravidel.

**Pozor:** kompletní rule-set `suricata.rules` a soubor služby `suricata-ips.service` stále chybějí; `eve.json` již byl doplněn. Samotný YAML neprokazuje aktivní verzi pravidel během každé historické fáze testování.


## Doplnění 18. 11. 2026 — skutečná EVE data a EveBox

- `data/eve_prehled.json` obsahuje statistiky skutečného souboru `eve.json` (41 157 událostí, 27 105 alertů, 288 alertů s akcí blocked).
- `data/eve_alerty_laboratorni.csv` obsahuje 470 vlastních laboratorních alertů ze dne 17. 11. 2026 (217 blocked, 253 allowed).
- `data/eve_signatury_laboratorni.csv`, `data/eve_udalosti_typy.csv`, `data/eve_laboratorni_v_case.csv` a `data/eve_http_priklady.csv` obsahují podklady pro Streamlit.
- `evebox_demo/laboratorni_udalosti_2026-11-17.json` je filtrovaný výběr skutečných událostí pro rychlý EveBox oneshot.
- `private_archive/logs/eve.json` je původní archivní soubor, nesmí se publikovat.
- Screenshoty ukládejte do `assets/screenshots_evebox/`, automaticky se zobrazí na stránce EveBox.

Přibližně 25 794 alertů jsou opakované diagnostické události `SURICATA Ethertype unknown`; v demonstračním souboru jsou vynechané. Pozor: událost `allowed` u konkrétního alertu sama o sobě neurčuje výsledný stav celé HTTP transakce.

**Pro místní demonstraci:** `evebox oneshot evebox_demo/laboratorni_udalosti_2026-11-17.json`, potom `http://localhost:5636`.

## Doplnění 18. 11. 2026 – screenshoty EveBoxu

Čtyři skutečné screenshoty byly přidány do `assets/screenshots_evebox/` a jejich české popisy do `screenshots.json`.

Ve Streamlitu otevřete sekci **EveBox a screenshoty** a přepínejte záložky Přehled, ICMP, TCP skenování a SQL injection.

Na obrázcích je doložena konkrétní blokovací akce `blocked` u vybraných alertů (SID 1000001, 1000011, 1000121). Screenshoty nedokládají úspěšnost všech testovacích scénářů.

**Poznámka k počtům:** screenshot přehledu uvádí 924 událostí a 477 alertů ve filtrovaném EveBox souboru, zatímco Streamlit základní stránka počítá 470 laboratorních alertů ze dne 17. 11. při odlišném filtru SID. Tyto ukazatele nejsou totožné množiny.

## Úprava dokumentace – 18. 11. 2026

- Ze stránky **Konfigurace IPS** byla odstraněna interpretační poznámka k `tpacket-v3`; původní YAML zůstal beze změny.
- `data/pravidla_inventar.csv` neobsahuje sloupce `stav_v_souboru`, `uvedeno_v_yaml` a `runtime_overeni`. Stav pravidel se během experimentů měnil.
- HTTP testování je ve stránce **Pravidla a útoky** zobrazeno ve dvou fázích: nejprve IDS (`alert`), potom IPS (9 × `drop`, 1 × kontrolní `alert`).
- Nový soubor `data/http_sady_porovnani.csv` umožňuje přímé srovnání akcí všech deseti signatur ze skutečně zaslaných IDS a IPS pravidel.
- U IDS fáze je uvedena pozorovaná výjimka bez nepodloženého vysvětlení příčiny.

## Doplnění 18. 11. 2026 – úvod a realizace

- Stránka **Přehled**: úvod, cíl, stručný současný stav, průběh řešení, vlastní přínos a omezení měření.
- Stránka **Topologie a fotografie**: skutečné zapojení Cisco C3850, VLAN 10/20 (obě `/16`), porty 10 a 20, IP adresace, hardware, konfigurace průchozího AF_PACKET IPS a autentické fotografie.
- Autoři Oryna Borovyk (`bor0250`) a David Kunčík (`kun212`) jsou uvedeni na webu i v `data/lab_setup.json`.
- Ostatní stránky, dřívější analýzy a screenshoty EveBoxu jsou zachovány.


## Aktualizace 18. 11. 2026 – závěr a metodika útoků

- V `app_preview.py` na stránce **Pravidla a útoky** je popsána simulace provozu pomocí Python skriptů, bezpečný testovací HTTP server a rozdělení HTTP testů na IDS/IPS.
- Stránka **Závěr a zdroje** nyní obsahuje souvislé vyhodnocení dosažených cílů, klíčová čísla, metodická omezení, vlastní přínos a další možné kroky.
- `ZAVER_A_METODIKA.md` je samostatný český text vhodný jako podklad do závěrečné dokumentace.
- Originální testovací skripty jsou archivovány v `private_archive/testovaci_skripty/` pro reprodukovatelnost. Nepublikujte je bez kontroly.
- `data/pravidla_inventar.csv` byl nahrazen poslední uživatelskou verzí s čistými názvy souborů.


## Doplnění 18. 11. 2026 – metodika se skutečnými ukázkami Python kódu

- Nová stránka **Metodika testování** popisuje reprodukovatelný postup a uvádí autentické výňatky funkcí z `http_advanced_v2.py`, `tcp_scanner_v4.py` a `windows_http_lab_server.py`.
- Soubory `assets/ukazky_kodu/*.py` jsou **doslovné výňatky** z originálních skriptů, nikoliv samostatně spustitelné aplikace. Komentáře a názvy proměnných pocházejí ze zdrojového kódu; česká interpretace je přímo na webu.
- Detailně je popsáno párování testovacích HTTP požadavků s `eve.json`: časové okno, adresy, porty, `rid`, `labcase` a kontrola akce `blocked`.
- Průběh testování se nyní vysvětluje na samostatné stránce; katalog pravidel zůstal přehlednější.
- Pro veřejné nasazení **nepublikujte `private_archive/`, `sources/` ani původní `eve.json`**. Publikované tabulky a screenshoty stále obsahují laboratorní adresaci; před zveřejněním zvažte, zda ji chcete ponechat.


## Aktuální členění webu (18. 11. 2026)

1. **Přehled** – úvod, cíle, kontext a hlavní výsledky.
2. **Topologie a konfigurace IPS** – síťové zapojení, VLAN, skutečná fotografie, parametry AF_PACKET, HOME_NET, logování a výňatek YAML.
3. **Pravidla Suricaty** – katalog dodaných signatur, akce `alert`/`drop` a porovnání HTTP IDS/IPS sad.
4. **Simulace útoků** – scénáře HTTP, TCP skenování, Python skripty, skutečné výňatky kódu, párování s EVE a omezení interpretace.
5. **Výkon a stabilita** – TCP, UDP, odezva, CPU/RAM.
6. **Analýza EVE** – vlastní interaktivní vyhodnocení logů.
7. **EveBox a screenshoty** – autentické ukázky detekce a blokování.
8. **Závěr a zdroje** – splnění cílů, přínos autorů, omezení a literatura.

Samostatná krátká stránka „Konfigurace IPS“ je **sloučená s topologií**.
Tabulka testovacích HTTP scénářů se přesunula z pravidel do simulace útoků; nic z výsledků, kódu, fotografií ani screenshotů se neodstranilo.
