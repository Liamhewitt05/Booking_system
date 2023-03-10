"""Booking systej"""
import json
import hashlib
from dataclasses import dataclass


@dataclass
class EnkelBruker:
    """klasse som holder brukere"""

    navn: str
    passord: str


@dataclass
class Bok:
    """klasse som holder bok navn og antall"""

    navn: str
    antall: int


@dataclass
class BokReservering:
    """klasse som holder reserveringer"""

    user: str
    bok_navn: str
    antall_dager_bok: int


allowed_chars = set(("0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_-"))


def create_sha(value):
    """kryptering"""
    hash_instance = hashlib.sha256(value.encode())
    string_hash = hash_instance.hexdigest()
    return string_hash


def registrer_bruker():
    """registrerer bruker"""
    ny_bruker = EnkelBruker(
        navn=input("Brukernavn: "),
        passord=input("passord: "),
    )
    return ny_bruker


def lagre_brukere(liste_over_brukere):
    """lagrer alle brukerene"""
    data = {}
    for bruker in liste_over_brukere:
        data[bruker.navn] = {}
        data[bruker.navn]["passord"] = bruker.passord
    with open("brukere.json", "w+") as f:
        f.write(json.dumps(data))


def last_inn_brukere():
    """leser alle brukerene"""
    data = open("brukere.json", "r").read()
    data = json.loads(data)
    liste = []
    for bruker in data:
        liste.append(
            EnkelBruker(
                navn=bruker,
                passord=data[bruker]["passord"],
            )
        )
    return liste


def reserver_bok(user):
    """setter reservasjon"""
    ny_bokreserering = BokReservering(
        user=user,
        bok_navn=input(": "),
        antall_dager_bok=int(input("Hvor mange dager vil du låne den: ")),
    )
    return ny_bokreserering


def lagre_reservasjoner(reservasjoner):
    """lagrer reservasjonen"""
    data = {}
    for reservasjon in reservasjoner:
        data[reservasjon.user] = dict()
        data[reservasjon.user]["bok_navn"] = reservasjon.bok_navn
        data[reservasjon.user]["antall_dager_bok"] = reservasjon.antall_dager_bok

    with open("reservasjoner.json", "w+") as f:
        f.write(json.dumps(data))


def last_inn_reservasjoner():
    """leser alle reservasjonene"""
    data = open("reservasjoner.json", "r").read()
    data = json.loads(data)
    liste = []
    for reservasjon in data:
        liste.append(
            BokReservering(
                user=reservasjon,
                bok_navn=data[reservasjon]["bok_navn"],
                antall_dager_bok=data[reservasjon]["antall_dager_bok"],
            )
        )
    return liste


def lagre_ledige_bøker(ledige_bøker):
    """lagrer ledige bøker"""
    data = {"alle_boker": {}}
    for bok in ledige_bøker:
        data["alle_boker"][bok.navn] = {"antall": bok.antall}

    with open("Ledige_bøker.json", "w+") as f:
        f.write(json.dumps(data))


def last_inn_ledige_bøker():
    """leser ledige bøker"""
    data = open("Ledige_bøker.json", "r").read()
    data = json.loads(data)
    liste = []
    for bok_navn, value in data["alle_boker"].items():
        liste.append(Bok(navn=bok_navn, antall=value["antall"]))
    return liste


def bok_innlevering(ledige_bøker, navn):
    """fjerner boken fra reservasjoner"""
    lagre_ledige_bøker(ledige_bøker)
    data = open("reservasjoner.json", "r").read()
    data = json.loads(data)
    data.pop(navn)
    with open("reservasjoner.json", "w+") as f:
        f.write(json.dumps(data))


if __name__ == "__main__":
    alle_brukere = last_inn_brukere()

    current_user = None

    # temporary cheat to avoid login
    # for user in alle_brukere:
    #     if user.navn == "liam":
    #         current_user = user

    while True:
        alle_reservasjoner = last_inn_reservasjoner()
        if current_user is None:
            option = input("1: Ny bruker \n2: Logg inn\n:")
            if option == "1":
                new_user = registrer_bruker()

                ugyldig_brukenavn = False
                for user in alle_brukere:
                    if new_user.navn == user.navn:
                        print("\nBrukernavn eksisterer allerede\n")
                        ugyldig_brukenavn = True

                validation = set((new_user.navn))
                if validation.issubset(allowed_chars):
                    pass
                else:
                    print("\nUgyldig navn\n")
                    ugyldig_brukenavn = True

                if ugyldig_brukenavn == False:
                    encrypted = create_sha(new_user.passord)
                    new_user.passord = encrypted
                    alle_brukere.append(new_user)
                    lagre_brukere(alle_brukere)
                    current_user = new_user

            elif option == "2":
                navn = input("Brukernavn: \n")
                for bruker in alle_brukere:
                    if navn == bruker.navn:
                        password = input("Passord: \n")
                        if create_sha(password) == bruker.passord:
                            current_user = bruker
                        else:
                            print("Innlogging feilet.\n")
        else:
            print("\nLogged in as " + current_user.navn + "\n")
            option = input(
                "1: Lån ny bok \n2: Lever inn bok \n3: Vis reserverte bøker \n4: Logg ut\n:"
            )
            if option == "1":
                bruker_har_lånt = False
                for user in alle_reservasjoner:
                    if user.user == current_user.navn:
                        bruker_har_lånt = True
                if bruker_har_lånt:
                    print(
                        "Du kan kun låne en bok om gangen. Du har allerede lånt bok '"
                        + user.bok_navn
                        + "'"
                    )
                else:
                    ledige_bøker = last_inn_ledige_bøker()
                    print("\nLedige bøker:\n")
                    for bok in ledige_bøker:
                        print(bok.navn + "\nTilgjengelige Kopier: " + str(bok.antall) + "\n")

                    ny_bokreservering = reserver_bok(current_user.navn)
                    found_book = None
                    for bok in ledige_bøker:
                        if bok.antall < 1:
                            ingen_ledige = found_book
                        else:
                            if bok.navn == ny_bokreservering.bok_navn:
                                bok.antall -= 1
                                found_book = bok
                                alle_reservasjoner.append(ny_bokreservering)
                                lagre_reservasjoner(alle_reservasjoner)
                                lagre_ledige_bøker(ledige_bøker)
                    if found_book is not None:
                        print("Du har lånt denne boken: " + ny_bokreservering.bok_navn)
                    elif found_book is ingen_ledige:
                        print("Ingen flere ledige kopier\n")
                    else:
                        print("Ingen bok med dette navnet\n")
            elif option == "2":
                ledige_bøker = last_inn_ledige_bøker()
                innlevering = input("Hva heter boken du vil lever inn?\n")
                for user in alle_reservasjoner:
                    if current_user.navn == (user.user):
                        if user.bok_navn != innlevering:
                            print(
                                "Du har ingen bøker ved navnet '"
                                + innlevering
                                + "' registrert på din bruker '\n"
                                + current_user.navn
                                + "'"
                            )
                        for bok in ledige_bøker:
                            if bok.navn == innlevering:
                                bok.antall += 1
                                bok_innlevering(ledige_bøker, current_user.navn)
                                print("\nDu har nå levert inn boken '" + innlevering + "'\n")

            elif option == "3":
                ledige_bøker = last_inn_ledige_bøker()
                reserverte_bøker = False
                for reservasjon in alle_reservasjoner:
                    if current_user.navn == (reservasjon.user):
                        print("\nReserverte bøker:\n" + reservasjon.bok_navn)
                        reserverte_bøker = True
                if reserverte_bøker == False:
                    print("\nDu har ingen reservasjoner")

            elif option == "4":
                print("Du har nå logget ut.")
                current_user = None
