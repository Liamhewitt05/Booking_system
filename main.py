import json
from dataclasses import dataclass


@dataclass
class EnkelBruker:
    navn: str
    passord: str
    boknavn: str
    antall_dager: int
    nyhetsbrev: bool = False


def registrer_enkel():
    ny_bruker = EnkelBruker(
        navn=input("Brukernavn: "),
        passord=input("passord: "),
        boknavn=input("Hva heter boken du vil låne?: "),
        antall_dager=input("Hvor mange dager vil du låne boken?: "),
        nyhetsbrev=False,
    )
    nyhetsbrev = input("Vil du motta nyhetsbrev? j/n: ")
    if nyhetsbrev == "j":
        ny_bruker.nyhetsbrev = True
    return ny_bruker


def lagre_brukere(liste_over_brukere):
    data = {}
    for bruker in liste_over_brukere:
        data[bruker.navn] = {}
        data[bruker.navn]["passord"] = bruker.passord
        data[bruker.navn]["boknavn"] = bruker.boknavn
        data[bruker.navn]["antall_dager"] = bruker.antall_dager
        data[bruker.navn]["nyhetsbrev"] = bruker.nyhetsbrev
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
                boknavn=data[bruker]["boknavn"],
                antall_dager=data[bruker]["antall_dager"],
                nyhetsbrev=data[bruker]["nyhetsbrev"],
            )
        )
    return liste


if __name__ == "__main__":
    alle_brukere = last_inn_brukere()
    current_user = None
    # for bruker in alle_brukere:
    #     if bruker.navn == "Svein":
    #         bruker.passord = "123"
    # lagre_brukere(alle_brukere)
    while True:
        print("1: Ny bruker, 2: Logg inn, 3: Reserver bok")
        option = input("$: ")
        if option == "1":
            new_user = registrer_enkel()

            # check if the book exists
            book_exists = False
            for bruker in alle_brukere:
                if new_user.boknavn == bruker.boknavn:
                    book_exists = True
                    break

            # if book exixsts print message, otherwise add the booking
            if book_exists:
                print("Denne boken er allerede lånt ut, prøv igjen.")
            else:
                alle_brukere.append(new_user)

            # Krypter dataene
            # Enveiskryptering
            # Toveiskryptering (avansert)
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
                        print(
                            "Du har lånt boken "
                            + bruker.boknavn
                            + ", du har x mange dager igjen før innlevering."
                        )
                        current_user = bruker
                    else:
                        print("Innlogging feilet.")
        elif option == "3":
            if current_user is not None:
                print("succes")
            else:
                print("You must log in first")
