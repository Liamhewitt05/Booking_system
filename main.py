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
        user=user, bok_navn=input("bok_navn: "), antall_dager_bok=int(input("antall_dager_bok: "))
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


def bok_innlevering():
    """fjerner boken fra reservasjoner"""
    lagre_ledige_bøker(ledige_bøker)
    data = open("reservasjoner.json", "r").read()
    data = json.loads(data)
    data.pop(current_user.navn)
    with open("reservasjoner.json", "w+") as f:
        f.write(json.dumps(data))


if __name__ == "__main__":
    alle_brukere = last_inn_brukere()
    alle_reservasjoner = last_inn_reservasjoner()
    current_user = None

    # temporary cheat to avoid login
    for user in alle_brukere:
        if user.navn == "liam":
            current_user = user

    while True:
        if current_user is None:
            option = input("1: Ny bruker \n2: Logg inn\n:")
            if option == "1":
                new_user = registrer_bruker()
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
            option = input("1: Lån ny bok \n2: Lever inn bok \n3: Logg ut\n:")
            if option == "1":
                ledige_bøker = last_inn_ledige_bøker()
                print("Ledige bøker:")
                for bok in ledige_bøker:
                    print(bok.navn)

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
                            print(ledige_bøker)
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
                                + "' registrert på ditt navn '\n"
                                + current_user.navn
                                + "'"
                            )
                        for bok in ledige_bøker:
                            if bok.navn == innlevering:
                                bok.antall += 1
                                bok_innlevering()
                                print("Du har nå levert inn boken '" + innlevering + "'\n")

            elif option == "3":
                print("Du har nå logget ut.")
                current_user = None
