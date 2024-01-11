import users
from colorama import Fore, Style
import time
import richieste


# MENU:
# 1. Creazione nuovo utente -> richiesta info per creare new user
# 2. Log in utente
# SUBMENU: [S o R]
# S: fare richieste pagamento, visualizzare richieste e fare conteggio ore
# R: Selezionare una richiesta e accettarla/rifiutarla

# Funzioni per colorare output
def red(x): return f"{Fore.RED}{x}{Style.RESET_ALL}"
def verde(x): return f"{Fore.GREEN}{x}{Style.RESET_ALL}"
def to_key(x): return x.strip().lower().replace(" ", "")


contenitore_utenti = {}
ceo = users.Responsabile("Fronk von", 5000, 40)
contenitore_utenti['fronkvon'] = ceo

while True:
    # user_selected = False
    print(verde("\tMENU:"))
    main_menu_choice = input(verde("""
                                   
1. Creazione nuovo utente
2. Log in utente 
                            
"""))
    if main_menu_choice == '1':
        # Logica creazione nuovo utente
        nominativo = input("Inserisci nome e cognome: ")
        stipendio = int(input("Inserisci stipendio: "))
        orario = int(input("Inserisci il tuo orario: "))
        ruolo = input("Inserisci il tuo ruolo: (s) o (r): ").lower()
        if ruolo == 's':
            # Controllo Esistenza responsabile
            responsabile = input("Inserisci il nome del tuo responsabile: ")
            responsabile_key = to_key(responsabile)
            if responsabile_key in contenitore_utenti:
                selected_user = users.Subordinato(
                    nominativo, stipendio, orario, responsabile)
            else:
                print(red("\nResponsabile inesistente, processo interrotto...\n"))
                continue

        elif ruolo == 'r':
            selected_user = users.Responsabile(nominativo, stipendio, orario)
    elif main_menu_choice == '2':
        login_nominativo = input("Inserisci nominativo per il login: ")
        login_key = to_key(login_nominativo)
        if login_key in contenitore_utenti:
            selected_user = contenitore_utenti[login_key]
        else:
            print(red("\nUtente inesistente...\n"))
            continue
    else:
        print(red("\nScelta inesistente...\n"))
        continue

    # variabile per determinare se rimanere nel sottomenu o tornare al menu principale
    stay_on_menu = False
    # Seconda parte del menu in base alla scelta dell'utente attuale
    while not stay_on_menu:

        # Menu user subordinato:
        if isinstance(selected_user, users.Subordinato):
            print(
                verde(f"\nBentornato {selected_user.nominativo} cosa vuoi fare?\n"))
            user_choice = input(
                "1. Nuova Richiesta di pagamento\n2. Visualizzare Cronologia richieste\n3. Visualizzare Resoconto ore\n")
            # possibili scelte:
            if user_choice == '1':
                richieste.new_richiesta_pagamento(selected_user)
            elif user_choice == '2':
                richieste.cronologia_richieste(selected_user)
            elif user_choice == '3':
                lista_importi, ore_totali = richieste.ore_importo_complessivi(
                    selected_user)
                if lista_importi:
                    print(verde("Richieste di pagamento accettate: "))
                    for richiesta in lista_importi:
                        print(richiesta)
                    print(
                        verde(f"Ore totali dalle richieste: {Fore.WHITE}{ore_totali}{Style.RESET_ALL}"))
            else:
                print(red("\nScelta invalida, interruzione servizio...\n"))
                continue

        # Menu Responsabile
        elif isinstance(selected_user, users.Responsabile):
            print(
                verde(f"\nBentornato {selected_user.nominativo} cosa vuoi fare?\n"))
            user_choice = input(
                "1. Visualizzare le richieste dei subordinati\n2. Modificare Richieste esistenti")
            if user_choice == '1':
                print(verde("Richieste dei subordinati: "))
                richieste.richieste_subordinati(selected_user)
            elif user_choice == '2':
                approvare_rifiutare = input(
                    "Vuoi approvare (a) o rifiutare (r) una richiesta? ")
                subordinato = input("Per quale subordinato: ")
                id_richiesta = int(input("ID della richiesta: "))
                index = contenitore_utenti[subordinato].get_index(id_richiesta)
                richieste.modifica_richiesta(selected_user, index, approvare_rifiutare,
                                             contenitore_utenti, subordinato)

            else:
                print(red("\nScelta invalida, interruzione servizio...\n"))
                continue

        # caso in cui non ci sia una istanza valida di User
        else:
            print(red("\nQualcosa è andato storto... terminazione in corso...\n"))
            time.sleep(1)
            break