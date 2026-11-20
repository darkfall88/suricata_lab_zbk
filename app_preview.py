from pathlib import Path
import json
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent
D = ROOT / "data"
st.set_page_config(page_title="Suricata IPS – reálná laboratoř", page_icon="🛡️", layout="wide")
st.title("Pokročilá konfigurace Suricata IPS")
st.caption("Praktická realizace transparentního inline IPS, testování útoků a analýza výsledků")
st.markdown("**Autoři:** Oryna Borovyk (bor0250), David Kunčík (kun212)")

metrics = json.loads((D / "metrics.json").read_text(encoding="utf-8"))
eve = json.loads((D / "eve_prehled.json").read_text(encoding="utf-8"))
choices = ["Přehled", "Topologie a konfigurace IPS", "Pravidla Suricaty", "Simulace útoků", "Výkon a stabilita", "Analýza EVE", "EveBox a screenshoty", "Závěr a zdroje"]
panel = st.sidebar.radio("Obsah projektu", choices)

if panel == "Přehled":
    st.header("Úvod a cíl projektu")
    st.markdown("""
    Cílem projektu bylo vytvořit a prakticky ověřit systém prevence průniků (IPS)
    s využitím nástroje Suricata. Nepracovali jsme pouze se simulací: sestavili jsme
    skutečnou laboratorní síť, vložili zařízení se Suricatou přímo do komunikační cesty,
    připravili vlastní detekční a blokovací pravidla a provedli bezpečnostní i výkonnostní testy.

    Základním rozdílem je, že IDS síťovou komunikaci vyhodnocuje a vytváří upozornění,
    zatímco inline IPS může vybraný provoz na základě pravidel také zablokovat.
    V laboratoři jsme si tento rozdíl ověřili zejména na skenování portů,
    ICMP a HTTP požadavcích připomínajících SQL injection, XSS a průchod adresářů.
    """)

    st.subheader("Co jsme chtěli ověřit")
    st.markdown("""
    - Zda Suricata dokáže transparentně předávat provoz mezi dvěma fyzickými rozhraními, aniž by na nich potřebovala IP adresu
    - Jak se liší chování detekčních (alert) a blokovacích (drop) pravidel při skutečných testech
    - Jaké události lze doložit pomocí EVE JSON a EveBoxu
    - Jak nasazení ovlivňuje TCP/UDP propustnost, latenci, spotřebu CPU a RAM a stabilitu
    """)

    st.subheader("Současný stav a použité technologie")
    st.markdown("""
    Suricata je otevřený systém pro analýzu síťového provozu, který podporuje
    IDS i IPS. V našem řešení využíváme režim AF_PACKET pro transparentní
    přenos a kontrolu paketů přímo v síťové cestě. Události Suricata zapisuje
    do EVE JSON; pro detailní procházení alertů používáme EveBox.
    """)

    st.subheader("Praktický postup projektu")
    st.markdown("""
    **1. Realizace sítě:** Cisco L3 switch, útočný Linux, cílový Windows a
    dvourozhranový Linux se Suricatou

    **2. Nasazení IPS:** konfigurace obousměrného předávání AF_PACKET, vymezení
    chráněné sítě, zapnutí logování a příprava vlastních pravidel

    **3. Bezpečnostní ověřování:** připravenými Python skripty jsme řízeně
    simulovali TCP skenování a různé HTTP požadavky. HTTP testy proběhly nejprve
    s detekční sadou IDS a následně s blokovací sadou IPS; samostatně jsme
    ověřovali také blokování ICMP

    **4. Měření a analýza:** testy iPerf2, ping, sledování CPU/RAM a kontrola
    výstupů Suricaty i EveBoxu
    """)
    st.info("**Vlastní přínos:** reálné zapojení a konfigurace IPS, vlastní laboratorní pravidla a testy, vyhodnocení naměřených dat a jejich přehledná prezentace ve Streamlitu.")

    with st.expander("Rozsah výsledků a metodická omezení"):
        st.markdown("""
        Výsledky se vztahují k této konkrétní laboratorní sestavě, nikoli ke všem
        možným konfiguracím Suricaty. Při vyšší UDP zátěži vznikaly ztráty
        v zachytávací vrstvě; u TCP se vyskytly timeouty při ukončování
        některých spojení. Přímý srovnávací experiment se stejnou sítí bez IPS
        nebyl proveden. Z těchto důvodů nevyvozujeme univerzální výkonový limit
        ani přesné zpoždění způsobené samotnou Suricatou.
        """)

elif panel == "Topologie a konfigurace IPS":
    st.header("Topologie, realizace a konfigurace IPS")
    st.markdown("""
    Laboratoř byla sestavena ze tří fyzických notebooků a
    24portového L3 switche Cisco Catalyst C3850. Switch rozdělil síť do
    dvou VLAN a zajišťoval směrování mezi nimi. Útočný počítač byl umístěn
    do simulované vnější sítě, Windows do chráněné vnitřní sítě.

    Suricata IPS ležela fyzicky mezi portem 10 switche a cílovým počítačem.
    Neprováděla směrování mezi VLAN; na svých dvou síťových rozhraních
    neměla IP adresu. Komunikaci obousměrně kontrolovala a předávala
    pomocí AF_PACKET v režimu `copy-mode: ips`.
    """)

    st.subheader("IP Adresace/VLAN")
    st.table(pd.DataFrame([
        {"VLAN": 20, "Síť": "Simulovaná vnější síť", "Subnet": "10.20.0.0/16", "Port switche": "20", "Koncové zařízení": "Linux 10.20.0.100"},
        {"VLAN": 10, "Síť": "Chráněná vnitřní síť", "Subnet": "10.10.0.0/16", "Port switche": "10", "Koncové zařízení": "Windows 10.10.0.100 přes IPS"},
    ]))

    st.subheader("Cesta testovacího provozu")
    st.code(
        "Útočný Linux 10.20.0.100 (VLAN 20)\n"
        "   ↓ port 20\n"
        "Cisco Catalyst C3850 – směrování mezi VLAN 20 a VLAN 10\n"
        "   ↓ port 10\n"
        "Suricata IPS: enx6c6e071f144e ↔ enp2s0 (bez IP adres)\n"
        "   ↓\n"
        "Cílový Windows 10.10.0.100 (VLAN 10)",
        language="text"
    )
    st.caption("Zpětná komunikace prochází stejnou cestou opačným směrem. Jde o simulaci hranice vnější/vnitřní sítě, nikoli o napojení na skutečný internet.")

    st.image(
        str(ROOT / "assets" / "schema_zapojeni_vlan10_vlan20_16.png"),
        caption="Schéma skutečné laboratorní topologie. VLAN 10 i VLAN 20 používají masku /16.",
        use_container_width=True,
    )

    st.subheader("Použitá zařízení")
    st.dataframe(pd.DataFrame([
        {"Zařízení": "Cisco Catalyst C3850", "Systém": "L3 switch", "Úloha": "VLAN 10 a 20, SVI brány a směrování"},
        {"Zařízení": "Lenovo ThinkPad L380", "Systém": "Linux Mint", "Úloha": "Útočný / testovací počítač, 10.20.0.100"},
        {"Zařízení": "Lenovo IdeaPad Gaming 3 15ACH6", "Systém": "Linux Mint + Suricata 8.0.7", "Úloha": "Transparentní inline IPS bez IP na průchozích rozhraních"},
        {"Zařízení": "Lenovo V310-15IKB", "Systém": "Windows 10", "Úloha": "Chráněný cíl, 10.10.0.100"},
    ]), hide_index=True, use_container_width=True)

    st.subheader("Konfigurace transparentního inline IPS")
    st.markdown("""
    Samotné směrování mezi VLAN 20 a VLAN 10 provádí Cisco Catalyst C3850.
    Po směrování do VLAN 10 prochází komunikace dvěma fyzickými rozhraními
    počítače se Suricatou. Ta provoz nesměruje ani nepřekládá adresy:
    kontroluje pakety a v režimu AF_PACKET IPS je předává na druhé rozhraní,
    pokud je aktivní pravidlo nezablokuje.

    Průchozí síťová rozhraní nemají vlastní IP adresy. Suricata tedy stojí
    přímo v cestě k chráněnému zařízení, nikoli na samostatném monitorovacím portu.
    """)
    cfg = json.loads((D / "suricata_config_summary.json").read_text(encoding="utf-8"))
    m1, m2 = st.columns(2)
    m1.metric("Verze Suricaty", cfg["generovana_verze_v_komentari"].replace("Suricata ", ""))
    m2.metric("Režim", "AF_PACKET IPS")

    st.subheader("Nastavení síťových rozhraní")
    interface_roles = {
        "enx6c6e071f144e": "Směrem ke switchi (port 10 / VLAN 10)",
        "enp2s0": "Směrem k cílovému Windows",
    }
    st.dataframe(pd.DataFrame([
        {
            "Rozhraní": item["rozhrani"],
            "Zapojení": interface_roles.get(item["rozhrani"], ""),
            "Předávání do": item["preposila_do"],
            "Režim": item["rezim"],
            "Vlákna": item["vlaken"],
            "Cluster ID": item["cluster_id"],
            "Typ clusteru": item["typ_clusteru"],
        }
        for item in cfg["af_packet_interfaces"]
    ]), hide_index=True, use_container_width=True)
    st.markdown("""
    Pro každé rozhraní je v YAML definováno `copy-mode: ips` a jako
    `copy-iface` druhá síťová karta. Příjem a předávání proto fungují
    obousměrně. Nastavení `threads: 1` určuje jedno zachytávací vlákno
    na každé straně, `cluster-type: cluster_flow` přiřazuje pakety toku
    ke stejnému zpracování.
    """)

    st.subheader("Síťové skupiny, logování a načítání pravidel")
    net_tab, log_tab, rules_tab = st.tabs(["Síťové proměnné", "Výstupní logy", "Pravidla a soubory"])
    with net_tab:
        st.code(
            'vars:\n  address-groups:\n'
            '    HOME_NET: "[10.10.0.0/16]"\n'
            '    EXTERNAL_NET: "!$HOME_NET"',
            language="yaml",
        )
        st.write("`HOME_NET` vymezuje chráněnou vnitřní síť VLAN 10. "
                 "`EXTERNAL_NET` představuje adresy mimo tuto síť, tedy také "
                 "testovací Linux ve VLAN 20. Členění do VLAN ale zajišťuje "
                 "switch, nikoli samotné proměnné v Suricatě.")
    with log_tab:
        st.dataframe(pd.DataFrame([
            {"Soubor": "eve.json", "Účel": "Strukturované bezpečnostní i provozní události pro analýzu a EveBox"},
            {"Soubor": "fast.log", "Účel": "Stručný čitelný přehled alertů"},
            {"Soubor": "stats.log", "Účel": "Statistiky zpracování paketů a čítače zachytávání"},
        ]), hide_index=True, use_container_width=True)
        st.write(f"Výstupy se ukládají do `{cfg['logovaci_slozka']}`; "
                 f"interval statistik je {cfg['statistiky_interval_s']} sekund. "
                 "Detailní laboratorní alerty zobrazujeme na stránkách "
                 "Analýza EVE a EveBox a screenshoty.")
    with rules_tab:
        st.markdown("""
        `suricata.yaml` odkazuje na standardní a vlastní soubory signatur.
        V průběhu testování jsme přepínali sady IDS/IPS i jednotlivé
        signatury; dodaný YAML je proto snímek konfigurace, nikoli
        doklad stejného aktivního stavu během všech experimentů.
        """)
        st.code("\n".join(f"- {name}" for name in cfg["pravidla_v_yaml"]), language="text")
        st.write("Soubory `classification.config` a `reference.config` poskytují "
                 "metadata pravidel; `threshold.config` slouží k případné "
                 "konfiguraci omezení četnosti upozornění. Podrobnosti "
                 "vlastních signatur uvádí stránka **Pravidla Suricaty**.")

    with st.expander("Zobrazit výňatek skutečného souboru suricata.yaml"):
        st.code((D / "suricata_config_excerpt.yaml").read_text(encoding="utf-8"), language="yaml")
        st.caption("Výňatek je převzat z dodané kopie konfigurace; aktivace "
                   "jednotlivých sad se během testů měnila.")

    st.subheader("Jak jsme ověřili funkčnost")
    st.markdown("""
    Nejprve jsme ověřili síťovou komunikaci přes vložené IPS. Následovaly
    testy ICMP, skenování TCP portů a dvě fáze HTTP testování:
    IDS s upozorněními, následně IPS s blokováním vybraných požadavků.
    Reálné zásahy potvrzují události `blocked` v exportu EVE a screenshoty
    EveBoxu. Nakonec jsme pomocí iPerf2 a `ping` měřili propustnost,
    odezvu a stabilitu při dlouhodobé TCP zátěži.
    """)

    st.subheader("Fotodokumentace fyzického zapojení")
    photos = json.loads((ROOT / "assets" / "photos" / "photos.json").read_text(encoding="utf-8"))
    cols = st.columns(2)
    for i, p in enumerate(photos):
        with cols[i % 2]:
            st.image(
                str(ROOT / "assets" / "photos" / p["file"]),
                caption=p["caption"],
                use_container_width=True,
            )
    st.caption("Fotografie dokládají skutečně sestavenou laboratoř; konkrétní čísla portů a VLAN vycházejí z dokumentace zapojení.")

elif panel == "Simulace útoků":
    st.header("Simulace útoků a testovací Python skripty")
    st.markdown("""
    Tato část vysvětluje, jak vznikala testovací síťová komunikace, jak jsme
    zajistili opakovatelnost jednotlivých pokusů a jak jsme porovnávali odpověď
    klienta s bezpečnostními událostmi Suricaty. Všechny pokusy proběhly
    ve fyzické laboratoři: Linux `10.20.0.100` odesílal provoz
    přes L3 switch a transparentní IPS na Windows `10.10.0.100`.

    HTTP server na Windows naslouchal na portu `8080` a neprováděl žádnou SQL
    operaci, nevykonával JavaScript ani neotevíral testované souborové cesty.
    Generované HTTP požadavky proto představují vzory pro ověření signatur,
    nikoli úspěšné zneužití zranitelné webové aplikace.
    """)

    st.subheader("Postup a použité nástroje")
    st.markdown("""
    Testování probíhalo v naší izolované laboratorní síti. Na útočném
    Linuxu jsme spouštěli připravené Python skripty, které odesílaly přesně
    definované TCP nebo HTTP požadavky na cílový Windows. Na Windows běžel
    jednoduchý testovací HTTP server na portu 8080, který přijatý obsah
    nevykonával jako skutečný útok. Tím jsme mohli bezpečně porovnávat,
    co IDS pouze zaznamená a co IPS skutečně zablokuje.

    Skripty zaznamenávaly výsledky pokusů; jejich interpretaci jsme ověřovali
    proti logům EVE JSON a rozhraní EveBox. Samotný timeout klienta
    jsme nepovažovali za dostatečný důkaz blokování.
    """)
    st.dataframe(pd.DataFrame([
        {"Typ testu":"TCP skenování", "Použitý skript":"tcp_scanner_v4.py", "Princip":"Řízené TCP connect pokusy na 12 vybraných portů; rychlé/pomalé profily a kontrola obnovy komunikace"},
        {"Typ testu":"Základní HTTP", "Použitý skript":"http_attack_lab_v1.py", "Princip":"Série známých HTTP požadavků pro porovnání reakcí IDS a IPS"},
        {"Typ testu":"Pokročilé HTTP", "Použitý skript":"http_advanced_v2.py", "Princip":"20 postupných scénářů: neškodné požadavky, SQLi/XSS/traversal vzory, varianty kódování a GET/POST (formulář/JSON)"},
        {"Typ testu":"HTTP cíl", "Použitý skript":"windows_http_lab_server.py", "Princip":"Kontrolovaný HTTP server pro GET/POST, bez vykonávání testovaných vstupů"},
    ]), hide_index=True, use_container_width=True)
    
    st.subheader("Testovací scénáře HTTP")
    cases=pd.read_csv(D/"http_test_cases.csv")
    columns=[c for c in ["index", "case", "family", "method", "expected_match", "expected_sid"]
             if c in cases.columns]
    st.dataframe(cases[columns],use_container_width=True,hide_index=True)
    st.caption("Tabulka uvádí 20 připravených scénářů a očekávané signatury. "
               "Individuální pozorované výsledky nevyvozujeme pouze z očekávání nebo "
               "z poslední dodané konfigurace; ty vyžadují párování s testovacími záznamy.")


    st.subheader("Ukázky ze skutečných zdrojových kódů")
    st.caption("Výňatky pocházejí z původních skriptů a jsou bez úprav samotného kódu. "
               "Jde o vybrané části funkcí, nikoli o samostatně spustitelné programy. "
               "Pro přehlednost uvádíme jen jejich podstatnou logiku.")
    snippets = ROOT / "assets" / "ukazky_kodu"
    http_tab, eve_tab, tcp_tab, server_tab = st.tabs([
        "HTTP požadavky", "Párování s EVE", "TCP skener", "Server na Windows"
    ])
    with http_tab:
        st.markdown("""
        **Zdroj:** `http_advanced_v2.py`, funkce `run()`.

        Skript postupně prochází definované scénáře. Do URL každého požadavku
        vkládá náhodný identifikátor běhu (`rid`) a jméno scénáře (`labcase`).
        Následně naváže HTTP spojení, odešle požadavek `GET` nebo `POST`,
        zaznamená odpověď či chybu a uloží výsledek do JSON.
        Tyto identifikátory usnadňují pozdější spojení konkrétního testu s
        událostí zaznamenanou Suricatou.
        """)
        st.code((snippets / "http_odesilani.py").read_text(encoding="utf-8"), language="python")
        st.markdown("""
        **Příklady reálných scénářů:** `baseline` (neškodný vstup),
        `sql_encoded` (URL-kódovaný SQLi vzor), `xss_encoded` (XSS vzor),
        `trav_encoded` (průchod adresářů), dále `POST` s formulářovým nebo JSON tělem.
        Skript obsahuje **20 připravených scénářů** včetně kontrolních požadavků.
        """)
    with eve_tab:
        st.markdown("""
        **Zdroj:** `http_advanced_v2.py`, funkce `match_event()` a `analyze()`.

        Při analýze se kontroluje zdrojová a cílová IP adresa, cílový port a
        časové okno. Pokud je ve výpisu dostupná HTTP URL, skript hledá shodu
        `rid`/`labcase`; alternativně používá zdrojový TCP port.
        Tím omezuje riziko, že bude náhodný alert přiřazen nesprávnému pokusu.
        """)
        st.code((snippets / "http_parovani_eve.py").read_text(encoding="utf-8"), language="python")
        st.markdown("""
        Výsledek klienta (`HTTP_RESPONSE`, `TIMEOUT` či `NETWORK_ERROR`) je
        **odlišný od závěru o zásahu IPS**. Ten skript vyhodnocuje až z
        odpovídajícího EVE alertu a pole `alert.action`.
        """)
        st.code((snippets / "http_vyhodnoceni.py").read_text(encoding="utf-8"), language="python")
        st.caption("`blocked` = potvrzený blokovací alert; `allowed` = upozornění na povolený provoz; "
                   "bez odpovídajícího alertu zůstává daný výsledek neověřený. "
                   "Jeden alert s akcí allowed však nemusí sám o sobě znamenat, "
                   "že byla povolena celá HTTP transakce.")
    with tcp_tab:
        st.markdown("""
        **Zdroj:** `tcp_scanner_v4.py`, funkce `attempt()`.

        Nejde o nízkoúrovňový SYN skener. Skript se pokouší navázat běžná
        **TCP spojení pomocí `socket.connect()`** na předem určené porty.
        Rozlišuje úspěšné spojení (`OPEN`), aktivní odmítnutí (`CLOSED`),
        timeout (`TIMEOUT`) a další chyby. Ukládá také čas zahájení,
        dobu trvání, zdrojový port a identifikátor pokusu.
        """)
        st.code((snippets / "tcp_pokus.py").read_text(encoding="utf-8"), language="python")
        st.write("Časování portových pokusů řídí okolní funkce `run_scan()` a zvolený "
                 "profil `fast`/`slow`. Samotný stav `TIMEOUT` nelze bez dalších "
                 "záznamů přisuzovat zásahu IPS.")
    with server_tab:
        st.markdown("""
        **Zdroj:** `windows_http_lab_server.py`, třída `Handler`.

        Server přijímá požadavky `GET` a `POST`. U `POST` pouze přečte
        přijaté tělo a při běžném zpracování odpoví stavem HTTP `200`.
        Odeslané SQLi, XSS ani traversal řetězce nijak neinterpretuje.
        Tím slouží jako kontrolovaný cíl pro testování **síťové inspekce**.
        """)
        st.code((snippets / "http_server_windows.py").read_text(encoding="utf-8"), language="python")

    st.subheader("Jak číst výsledek konkrétního testu")
    st.markdown("""
    1. **Odeslání:** například `sql_encoded` vytvoří HTTP požadavek z Linuxu
       `10.20.0.100` na Windows `10.10.0.100:8080` a přidá identifikátory testu.
    2. **Kontrola:** Suricata na průchozím IPS porovná požadavek s právě
       aktivní sadou pravidel. Ve fázi IDS používala HTTP sada `alert`,
       ve fázi IPS měla odpovídající signatura akci `drop`.
    3. **Záznam:** skript zaznamená odpověď nebo timeout; Suricata nezávisle
       zapíše detekci do `eve.json`.
    4. **Vyhodnocení:** oba záznamy se spárují podle testovacích identifikátorů,
       adres, portů a času. **Blokování potvrdí až odpovídající
       `alert.action=blocked`**, případně další nezávislé ověření.

    Konkrétní příklad signatury **SID `1000121`** a blokované události je
    zachycen na stránce **EveBox a screenshoty**. Úplný přehled testovacích
    scénářů, obě varianty HTTP pravidel a jejich SID jsou na stránce
    **Pravidla Suricaty**.
    """)

elif panel == "Pravidla Suricaty":
    st.header("Detekční a blokovací pravidla Suricaty")
    st.write("Pravidla se během experimentů měnila a jednotlivé sady se aktivovaly postupně. "
             "Přehled proto popisuje použité varianty, nikoli stav všech pravidel v jediném okamžiku.")

    st.markdown("""
    Každé pravidlo je identifikováno číslem SID a určuje podmínku,
    při které má Suricata reagovat. Akce `alert` vytvoří upozornění,
    zatímco `drop` je v inline IPS určena k blokování odpovídajícího provozu.
    Níže uvádíme skutečné dodané signatury, nikoli jen ilustrační příklady.
    """)

    st.subheader("HTTP testování: IDS/IPS")
    t_ids, t_ips, t_compare = st.tabs(["1. fáze: IDS", "2. fáze: IPS", "Srovnání signatur"])
    with t_ids:
        st.markdown("**IDS sada (`http_lab_ids.rules`)** – všechny dodané HTTP signatury "
                    "používají akci `alert`. Účelem bylo nejdříve ověřit detekci bez "
                    "blokování samotnými HTTP pravidly.")
        st.write("Podle průběhu laboratorních testů tato fáze převážně pouze upozorňovala; "
                 "vyskytla se jedna výjimka v pozorovaném chování. Protože všechny "
                 "signatury v dodané IDS sadě mají akci `alert`, nelze bez konkrétního "
                 "protokolu příčinu této výjimky připsat právě IDS sadě.")
    with t_ips:
        st.markdown("**IPS sada (`http_lab_ips.rules`)** – devět pravidel pro SQLi, XSS "
                    "a průchod adresářů bylo změněno z `alert` na `drop`. "
                    "Kontrolní pravidlo SID `1000100` zůstalo typu `alert`.")
        st.write("Ve druhé fázi se ověřovalo skutečné blokování vybraných "
                 "HTTP požadavků. Důkazem jsou také autentické záznamy s akcí "
                 "`blocked` v EVE JSON a screenshot z EveBoxu u SID `1000121`.")
    with t_compare:
        st.dataframe(pd.read_csv(D/"http_sady_porovnani.csv"),
                     hide_index=True,use_container_width=True)
        st.caption("Srovnání je odvozeno přímo ze dvou předaných souborů pravidel; "
                   "nepotvrzuje současnou aktivaci obou sad.")

    st.subheader("Katalog použitých pravidel")
    df=pd.read_csv(D/"pravidla_inventar.csv")
    files=sorted(df["soubor"].dropna().unique().tolist())
    choice=st.selectbox("Soubor s pravidly", files)
    sub=df[df["soubor"]==choice]
    st.dataframe(sub[["sid", "akce", "protokol", "zprava"]],
                 use_container_width=True,hide_index=True)
    with st.expander("Zobrazit text pravidel z vybraného souboru"):
        st.code("\n".join(sub["puvodni_pravidlo"].fillna("").tolist()), language="text")


elif panel == "Výkon a stabilita":
    st.header("Výkonové testy na skutečném zapojení")
    tab1, tab2, tab3, tab4 = st.tabs(["TCP", "UDP", "Latence", "CPU a RAM"])

    with tab1:
        tcp = pd.read_csv(D / "tcp_timeseries.csv")
        sel = st.selectbox(
            "TCP experiment",
            sorted(tcp.experiment.dropna().unique().tolist()),
            index=0,
        )
        d = tcp[tcp.experiment == sel]
        st.subheader("Propustnost TCP v čase")
        st.line_chart(
            d.pivot_table(index="end_sec", columns="device", values="mbps").sort_index(),
            x_label="Čas od začátku experimentu [s]",
            y_label="Propustnost [Mbit/s]",
        )
        st.dataframe(
            pd.read_csv(D / "tcp_summary.csv").query("experiment == @sel"),
            hide_index=True,
            use_container_width=True,
        )
        st.caption("Závěrečný Windows report obsahoval timeouty při ukončování TCP; hlavní 600s přenos byl stabilní")

    with tab2:
        udp = pd.read_csv(D / "udp_tests.csv")
        st.dataframe(udp, use_container_width=True, hide_index=True)
        st.subheader("Skutečná odesílaná rychlost UDP")
        st.bar_chart(
            udp.set_index("id")["actual_send_mbps"],
            x_label="Test UDP (identifikátor pokusu)",
            y_label="Odesílaná rychlost [Mbit/s]",
        )
        st.warning("U vysoké UDP zátěže nelze spolehlivě určit celkovou ztrátovost kvůli rozděleným reportům")

    with tab3:
        latency = pd.read_csv(D / "latency.csv")
        st.subheader("Průměrná a maximální odezva ICMP")
        rtt = latency.set_index("label")[["rtt_avg_ms", "rtt_max_ms"]].rename(
            columns={"rtt_avg_ms": "Průměrná RTT", "rtt_max_ms": "Maximální RTT"}
        )
        st.bar_chart(
            rtt,
            x_label="Podmínky měření",
            y_label="Doba odezvy RTT [ms]",
        )
        st.dataframe(latency, use_container_width=True, hide_index=True)

    with tab4:
        cpu = pd.read_csv(D / "suricata_cpu_memory.csv")
        st.subheader("Využití CPU Suricaty")
        st.line_chart(
            cpu.set_index("elapsed_sec")["cpu_total_pct"],
            x_label="Čas od začátku měření [s]",
            y_label="Využití CPU [% jednoho logického CPU]",
        )
        st.subheader("Spotřeba operační paměti Suricaty")
        st.line_chart(
            cpu.set_index("elapsed_sec")["rss_mib"],
            x_label="Čas od začátku měření [s]",
            y_label="Paměť RSS [MiB]",
        )
        st.caption("CPU podle pidstat je vyjádřeno jako procento jednoho logického CPU")

elif panel == "Analýza EVE":
    st.header("Vlastní analýza laboratorních událostí")
    st.caption("Reálná data z dodaného eve.json; filtrujeme laboratorní pravidla SID 1000000–1000999 ze dne 17. 11. 2026. Jde o počty alertů, ne počet unikátních útoků.")
    a,b,c=st.columns(3)
    a.metric("Lab alerty",eve["pocet_laboratornich_alertu"])
    b.metric("S akcí blocked",eve["laboratorni_akce"].get("blocked",0))
    c.metric("S akcí allowed",eve["laboratorni_akce"].get("allowed",0))
    df=pd.read_csv(D/"eve_alerty_laboratorni.csv")
    sigs=pd.read_csv(D/"eve_signatury_laboratorni.csv")
    st.subheader("Nejčastější laboratorní signatury")
    st.bar_chart(sigs.head(12).set_index("signatura")["celkem"])
    cas=pd.read_csv(D/"eve_laboratorni_v_case.csv")
    st.subheader("Alerty v čase")
    st.bar_chart(cas.set_index("hodina")["pocet"])
    x,y=st.columns(2)
    with x:
        akce=st.multiselect("Akce",sorted(df.akce.unique().tolist()),default=sorted(df.akce.unique().tolist()))
    with y:
        sid=st.selectbox("Signatura",["Všechny"]+[f"{r.sid} – {r.signatura}" for r in sigs.itertuples(index=False)])
    filtered=df[df.akce.isin(akce)]
    if sid!="Všechny":filtered=filtered[filtered.sid==int(sid.split(" ")[0])]
    st.write(f"Zobrazeno **{len(filtered)}** laboratorních alertů")
    st.dataframe(filtered,use_container_width=True,hide_index=True)
    st.caption("Historický export má více než 25 tisíc opakovaných diagnostických alertů `SURICATA Ethertype unknown`; přehled se proto zaměřuje na vlastní laboratorní SID.")
    with st.expander("Rozdělení všech typů událostí v původním EVE"):
        st.dataframe(pd.read_csv(D/"eve_udalosti_typy.csv"),use_container_width=True,hide_index=True)

elif panel == "EveBox a screenshoty":
    st.header("EveBox – důkazy skutečné detekce a blokování")
    st.write("EveBox využíváme jako hotové rozhraní pro detailní zkoumání událostí Suricaty. "
             "Vlastní část projektu tvoří fyzické IPS, testování a vyhodnocení ve Streamlitu.")
    st.info("Screenshoty byly pořízeny nad filtrovaným archivním výřezem EVE JSON ze 17. 11. 2026; "
            "zobrazované počty nejsou počty útoků ani statistikou celého původního logu")
    imgdir = ROOT / "assets" / "screenshots_evebox"
    descriptions = json.loads((imgdir / "screenshots.json").read_text(encoding="utf-8"))
    available = [item for item in descriptions if (imgdir / item["filename"]).is_file()]
    if available:
        tabs = st.tabs([item["tab"] for item in available])
        for tab, item in zip(tabs, available):
            with tab:
                st.subheader(item["title"])
                st.write(item["description"])
                st.image(str(imgdir / item["filename"]), use_container_width=True,
                         caption=f"Screenshot EveBoxu: {item['filename']}")
    else:
        st.warning("Screenshoty nejsou k dispozici ve složce assets/screenshots_evebox/.")

else:
    st.header("Závěrečné vyhodnocení projektu")
    st.success("Hlavní cíl byl splněn: sestavili jsme reálné síťové zapojení, zprovoznili transparentní inline Suricata IPS a experimentálně ověřili detekci, blokování i výkon.")

    st.subheader("Vyhodnocení dosažených cílů")
    st.markdown("""
    **Praktická realizace:** Na fyzických zařízeních Lenovo a switchi Cisco Catalyst C3850
    jsme vytvořili dvě oddělené sítě VLAN 20 (simulované vnější prostředí)
    a VLAN 10 (chráněná síť). Switch směroval provoz mezi VLAN a Suricata
    jej kontrolovala na cestě k Windows jako **transparentní dvourozhranový bridge
    bez IP adres na průchozích rozhraních**. Funkčnost zapojení dokládá
    fotodokumentace, konfigurace a provedené experimenty.

    **Detekce a blokování:** Pomocí připravených Python skriptů jsme simulovali
    TCP skenování a řízené HTTP požadavky představující příklady SQL injection,
    XSS a průchodu adresářů. HTTP testování proběhlo nejprve s pravidly
    **IDS (`alert`)**, následně s pravidly **IPS (`drop`)**. Záznamy v EVE JSON
    a ukázky v EveBoxu potvrzují skutečně blokované události, mimo jiné u ICMP,
    skenování portů a HTTP požadavků. Ne všechny varianty HTTP vstupu však
    vlastní signatury zachytily; ukázalo se omezení jednoduchých pravidel.

    **Výkon:** Při čtyřech souběžných TCP spojeních jsme během desetiminutového
    experimentu naměřili přibližně **949 Mbit/s** bez dlouhodobého poklesu
    propustnosti. V opakovaném 30sekundovém UDP testu byla potvrzena nulová
    ztrátovost při **210 Mbit/s**. Při vyšší zátěži kolem **262 Mbit/s** však
    přibylo **27 030 `capture.kernel_drops`**, takže výsledek nelze zobecnit
    jako bezchybný provoz při libovolné frekvenci paketů.

    **Latence a provozní stabilita:** Ping testy nevykázaly ztráty ICMP
    paketů ani výrazný nárůst RTT při současném TCP provozu. Paměť procesu
    Suricata se v dlouhodobém monitoringu držela okolo **450 MiB**;
    služba po testu zůstala aktivní a systemd nehlásil automatický restart.
    """)

    st.subheader("Hlavní naměřené výsledky")
    a, b, c, d = st.columns(4)
    a.metric("TCP – 10 minut", "≈ 949 Mbit/s")
    b.metric("UDP – bez ztrát", "210 Mbit/s")
    c.metric("ICMP ztráty", "0 %")
    d.metric("RAM Suricaty", "≈ 450 MiB")
    st.caption("TCP: 4 spojení, 600 s. UDP: 30 s, 1200B datagramy a 1MiB buffer příjemce. Hodnoty platí pro konkrétní laboratorní sestavu.")

    st.subheader("Omezení experimentů")
    st.markdown("""
    - **UDP:** při vyšší zátěži vznikaly ztráty.
      Rozdělené reporty Windows iPerf2 neumožňují určit spolehlivou celkovou
      ztrátovost nejvyšších UDP testů.
    - **TCP:** při ukončování některých spojení iPerf2 hlásil timeouty,
      ačkoliv vlastní desetiminutový přenos měl stabilní propustnost.
    - **Latence:** druhý ping test částečně přesahoval interval TCP zátěže.
      Chybí také samostatné referenční měření stejné sítě bez vloženého IPS;
      nelze tedy vyčíslit přesnou režii způsobenou Suricatou.
    - **Bezpečnostní testy:** HTTP požadavky byly laboratorními vzory,
      nikoliv útoky proti skutečně zranitelné webové aplikaci. Počty alertů
      navíc nejsou počty unikátních útoků a pravidla nejsou univerzální
      ochranou před všemi variantami SQLi, XSS nebo traversal.
    """)

    st.subheader("Vlastní přínos a názor autorů")
    st.markdown("""
    Za hlavní přínos považujeme **kompletní realizaci a ověření fyzického IPS**:
    návrh VLAN a zapojení zařízení, konfiguraci obousměrného AF_PACKET,
    přípravu a střídání sad pravidel IDS/IPS, použití Python skriptů
    k reprodukovatelnému generování testovacího provozu a společné
    vyhodnocení výsledků z Linuxu, Windows a Suricaty. Pro samostatnou technickou dokumentaci
    jsme připravili **Streamlit web** s grafy a výběrem laboratorních událostí;
    pro detailnější prohlížení logů jsme použili existující nástroj **EveBox**.

    Na základě testů považujeme Suricatu za vhodný nástroj pro demonstrační
    inline ochranu i pro výuku síťové bezpečnosti: umožnila nám názorně
    porovnat detekci a skutečné blokování. Zároveň se ukázalo, že účinné
    pravidlo musí být dobře navržené a otestované a že výkon IPS závisí
    nejen na datové propustnosti, ale také na charakteru provozu
    a počtu zpracovávaných paketů.
    """)

    st.subheader("Použité zdroje")
    st.markdown("""
    - [Oficiální dokumentace Suricata](https://docs.suricata.io/)
    - [EveBox – dokumentace](https://evebox.org/docs/)
    - [Streamlit – dokumentace](https://docs.streamlit.io/)
    - Vlastní laboratorní konfigurace, pravidla, Python skripty, fotografie, EVE JSON a výsledky testů ze 17. 11. 2026.
    """)

st.divider()
