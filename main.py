import json
from dataclasses import dataclass


@dataclass
class EnkelBruker:
    navn: str
    passord: str
    # boknavn: str
    # antall_dager: int
    # nyhetsbrev: bool = False


@dataclass
class BokReservering:
    bok_navn: str
    antall_dager_bok: int


def registrer_enkel():
    ny_bruker = EnkelBruker(
        navn=input("Brukernavn: "),
        passord=input("passord: "),
        # boknavn=input("Hva heter boken du vil låne?: "),
        # antall_dager=input("Hvor mange dager vil du låne boken?: "),
        # nyhetsbrev=False,
    )
    # nyhetsbrev = input("Vil du motta nyhetsbrev? j/n: ")
    # if nyhetsbrev == "j":
    #     ny_bruker.nyhetsbrev = True
    return ny_bruker


def lagre_brukere(liste_over_brukere):
    data = {}
    for bruker in liste_over_brukere:
        data[bruker.navn] = {}
        data[bruker.navn]["passord"] = bruker.passord
        # data[bruker.navn]["boknavn"] = bruker.boknavn
        # data[bruker.navn]["antall_dager"] = bruker.antall_dager
        # data[bruker.navn]["nyhetsbrev"] = bruker.nyhetsbrev
    with open("brukere.json", "w+") as f:
        f.write(json.dumps(data))


def last_inn_brukere():
    data = open("brukere.json", "r").read()
    data = json.loads(data)
    liste = []
    for bruker in data:
        liste.append(
            EnkelBruker(
                navn=bruker,
                passord=data[bruker]["passord"],
                # boknavn=data[bruker]["boknavn"],
                # antall_dager=data[bruker]["antall_dager"],
                # nyhetsbrev=data[bruker]["nyhetsbrev"],
            )
        )
    return liste


def reserver_bok():
    ny_bokreserering = BokReservering(
        bok_navn=input("bok_navn: "), antall_dager_bok=int(input("antall_dager_bok: "))
    )
    return ny_bokreserering


def lagre_lånt_bok(alle_bøker):
    data = {}
    for bok in alle_bøker:
        data[bok.bok_navn] = dict()
        data[bok.bok_navn]["antall_dager_bok"] = bok.antall_dager_bok

    with open("bøker.json", "w+") as f:
        f.write(json.dumps(data))


def last_inn_bøker():
    data = open("bøker.json", "r").read()
    data = json.loads(data)
    liste = []
    for bok in data:
        liste.append(
            BokReservering(
                bok_navn=bok, antall_dager_bok=data[bok]["antall_dager_bok"]
            )
        )
    return liste


if __name__ == "__main__":
    alle_brukere = last_inn_brukere()
    alle_bøker = last_inn_bøker()
    current_user = None

    # temporary cheat to avoid login
    for user in alle_brukere:
        if user.navn == "liam":
            current_user = user

    # for bruker in alle_brukere:
    #     if bruker.navn == "Svein":
    #         bruker.passord = "123"
    # lagre_brukere(alle_brukere)
    while True:
        if current_user is None:
            option = input("1: Ny bruker \n2: Logg inn\n:")
            if option == "1":
                new_user = registrer_enkel()

                # check if the book exists
                # book_exists = False
                # for bruker in alle_brukere:
                #     if new_user.boknavn == bruker.boknavn:
                #         book_exists = True
                #         break

                # # if book exixsts print message, otherwise add the booking
                # if book_exists:
                #     print("Denne boken er allerede lånt ut, prøv igjen.")
                # else:
                #     alle_brukere.append(new_user)

                # Krypter dataene
                # Enveiskryptering
                # Toveiskryptering (avansert)
                alle_brukere.append(new_user)
                lagre_brukere(alle_brukere)
                current_user = new_user

            elif option == "2":
                navn = input("Brukernavn: ")
                for bruker in alle_brukere:
                    if navn == bruker.navn:
                        password = input("Passord: ")
                        # Krypter passord
                        # Sammenlign med allerede
                        # kryptert passord.
                        if password == bruker.passord:
                            current_user = bruker
                        else:
                            print("Innlogging feilet.")
        else:
            print("Logged in as " + current_user.navn)
            option = input("1: Lån ny bok \n2: Lever inn bok \n3: Logg ut\n:")
            if option == "1":
                ny_bokreserering = reserver_bok()
                alle_bøker.append(ny_bokreserering)
                lagre_lånt_bok(alle_bøker)
                print("Du har lånt denne boken: " + ny_bokreserering.bok_navn)

            elif option == "3":
                print("Du har nå logget ut.")
                current_user = None
