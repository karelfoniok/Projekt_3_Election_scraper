"""
Project3.py: třetí projekt do Engeto Online Python Akademie

author: Karel Foniok
email: karel.foniok@gmail.com
discord: karel_10181
"""

import sys
import csv
from bs4 import BeautifulSoup
import requests


def check_website(url: str) -> bool:
    """
    Kontroluje, zda li příslušná url existuje
    """
    response = requests.get(url)
    if response.status_code == 200:
        return True
    else:
        return False

def check_arguments(argv: str) -> (str, str):
    """
    Kontroluje vložené argumenty pro spuštění tohoto skriptu.
    Pokud nejsou splněny podmínky, uživatel je informován.
    """
    if len(argv) != 2:
        print("Input two arguments")
        sys.exit()

    url = str(argv[0])
    file_name = str(argv[1])

    if not url.startswith('https://volby.cz/pls/ps2017nss'):
        print("Wrong URL")
        sys.exit()

    response_check = check_website(url)

    if response_check is False:
        print("Wrong URL")
        sys.exit()
    elif not file_name.endswith('.csv'):
        print("Wrong file type")
        sys.exit()
    else:
        print(f"Downloading data from url: {url}")
        return url, file_name


def get_urls_codes_names(url: str) -> (list, list):
    """
    Procházení tagů tr a získání seznamu slovníků obsahujících kód a název každé obce.
    Získání seznamu URL výsledků voleb.
    """
    election_results_partial = []
    urls = []
    root = "https://volby.cz/pls/ps2017nss/"
    parsed_html = BeautifulSoup(requests.get(url).text, features="html.parser")
    tr_tags = parsed_html.find_all('tr')

    for tr_tag in tr_tags:
        code_and_name_row = dict()
        code = tr_tag.find('td', {'class': 'cislo'})
        for number in range(1, 4):
            name = tr_tag.find('td', {'headers': f't{number}sa1 t{number}sb2'}) or tr_tag.find('td', {'headers': 's3'})
            if code and name is not None:
                code_and_name_row["code"] = code.text
                code_and_name_row["name"] = name.text
                election_results_partial.append(code_and_name_row)
                urls.append(root + code.find('a')['href'])
                break

    return urls, election_results_partial


def get_votes_envelopes(urls: list, election_results_partial: list) -> list:
    """
    Procházení URL každé obce. Hledání tagů td a přidávání informací o volbách do seznamu slovníků.
    """
    for index, code_and_name in enumerate(election_results_partial):
        url = urls[index]
        parsed_html = BeautifulSoup(requests.get(url).text, features="html.parser")
        code_and_name["registered"] = parsed_html.find("td", {"headers": "sa2"}).text.replace("\xa0", "")
        code_and_name["envelopes"] = parsed_html.find("td", {"headers": "sa5"}).text.replace("\xa0", "")
        code_and_name["valid"] = parsed_html.find("td", {"headers": "sa6"}).text.replace("\xa0", "")
        
    return election_results_partial


def get_parties_votes(urls: list, election_results: list) -> list:
    """
    Procházení URL každé obce. Hledání tagů td a přidávání názvů volebních stran a počtu hlasů do seznamu slovníků.
    """
    for index, row_dict in enumerate(election_results):
        url = urls[index]
        parsed_html = BeautifulSoup(requests.get(url).text, features="html.parser")
        div_tags = parsed_html.find("div", {"id": "inner"})
        tr_tags = div_tags.find_all("tr")
        for tr_tag in tr_tags:
            party_name = tr_tag.find("td", {"class": "overflow_name"})
            for number in range(1, 4):
                party_votes = tr_tag.find("td", {"headers": f"t{number}sa2 t{number}sb3"})
                if party_name is not None and party_votes is not None:
                    row_dict[party_name.text] = party_votes.text.replace("\xa0", "")
                    break

    return election_results


def save_to_csv(file_name: str, election_results: list):
    """
    Tato funkce zapisuje data do souboru .csv.
    """
    with open(file_name, 'w', encoding="utf-8-sig", newline="") as elections_file:
        fieldnames = election_results[0].keys()
        writer = csv.DictWriter(elections_file, fieldnames=fieldnames, delimiter=';')
        writer.writeheader()
        writer.writerows(election_results)
        print(f"Saving to file: {file_name}",
              "Closing election scraper",
              sep="\n")
        
        
def main(argv: str):
    """
    Hlavní funkce pro stažení, zpracování a zápis dat do csv souboru.
    """

    url_to_scrape, file_name = check_arguments(argv)
    urls, partial_dict_1 = get_urls_codes_names(url_to_scrape)
    partial_dict_2 = get_votes_envelopes(urls, partial_dict_1)
    election_results_dict = get_parties_votes(urls, partial_dict_2)
    save_to_csv(file_name, election_results_dict)
      

if __name__ == "__main__":
    main(sys.argv[1:])