# Web scrapper
Tento projekt je urcen ke scrappovani webove stranky www.volby.cz a to specificky te casti, ktera se venuje roku 2017. Uzivatel musi programu zadat dva argumenty a to url adresy, ktera povede k vybranemu uzemnimu celku, ktery si uzivatel preje scrappovat a nazev finalniho csv souboru.
## Priklad pouziti
```bash
python main.py "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2104" "soubor.csv"
```
Tento program pouziva mimo jine i knihovny BeautifulSoup a lxml, ktere jsou tedy ke spravnemu chodu nutne nainstalovat.
## Instalace pouzitych knihoven
```bash
pip install -r requirements.txt
```
Vysledny soubor je ve formate UTF8.