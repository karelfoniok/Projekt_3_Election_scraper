# Projekt_3_Election_scraper

## Popis projektu
Třetí projekt na Python slouží k extrahování výsledků parlamentních voleb z roku 2017 za jednotlivé územní celky.

## Instalace knihoven
Použité knihovny jsou v souboru requirements.txt.
Pro instalaci vytvořte nové virtuální prostředí a s nainstalovaným manažerem spusťte:

    $ pip --version                # ověří verzi manažeru
    $ pip install -r requirements  # nainstalují se knihovny

## Spuštění projektu
Pro spuštění souboru projekt_3_election_scraper jsou nutné v příkazovém řádku zadat dva povinné argumenty:
1. url územního celku
2. název souboru CSV, který se vygeneruje

Spuštění souboru v příkazovém řádku vypadá následovně:

    python projekt_3_election_scraper.py <odkaz-územního-celku> <výsledný-soubor>

Výsledek se stáhne jako soubor ve formátu .csv

## Ukázka projektu
Výsledky hlasování pro okres Karviná:
1. argument: https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=14&xnumnuts=8103
2. argument: karvina.csv

## Spuštění programu
    python projekt3_election_scraper.py 'https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=14&xnumnuts=8103' 'karvina.csv'

## Průběh stahování
    Dowloading data from url: https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=14&xnumnuts=8103
    Saving to file: karvina.csv
    Closing election scraper

## Ukázka výstupu
```bash
code;name;registered;envelopes;valid;Občanská demokratická strana;Řád národa - Vlastenecká unie;CESTA ODPOVĚDNÉ SPOLEČNOSTI;Česká str.sociálně demokrat.;Radostné Česko;STAROSTOVÉ A NEZÁVISLÍ;Komunistická str.Čech a Moravy;Strana zelených;ROZUMNÍ-stop migraci
598925;Albrechtice;3173;1955;1944;109;4;2;181;2;131;211;15;22;12;1;3;139;0;5;25;635;1;1;174;0;10;1;0;255;5
599051;Bohumín;17613;9036;8973;579;12;4;1241;9;133;821;85;91;87;7;6;641;0;12;119;3157;18;33;305;3;55;14;25;1478;38
```



