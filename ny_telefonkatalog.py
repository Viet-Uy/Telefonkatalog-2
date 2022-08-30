import pandas as pd

kjorer = True

raw_data = {
    'fornavn': [],
    'etternavn': [],
    'telefonnummer': []
}

telefonkatalog = pd.DataFrame(raw_data, columns=['fornavn', 'etternavn', 'telefonnummer'])


def printMeny():
    print("--------------- Telefonkatalog ---------------")
    print("| 1.Legg til ny person                       |")
    print("| 2. Søk opp person eller telefonnummer      |") 
    print("| 3. Vis alle personer                       |") 
    print("| 4. Avslutt                                 |") 
    print("----------------------------------------------") 


def registrerPerson ():
    global telefonkatalog
    
    fornavn = input("Skriv inn fornavn:")
    etternavn = input ("Skriv inn etternavn:")
    telefonnummer = input("Skriv inn telefonnummer:")

    nyRegistrering = {
        "fornavn": [fornavn],
        "etternavn": [etternavn],
        "telefonnummer": [telefonnummer]
        }
    
    newdf = pd.DataFrame(nyRegistrering, columns=["fornavn", "etternavn", "telefonnummer"])
    
    telefonkatalog = pd.concat([telefonkatalog, newdf])
    telefonkatalog = telefonkatalog.drop_duplicates()

    print("{0} {1} er registrert med telefonnummer {2}".format (fornavn, etternavn, telefonnummer))
    input("Trykk en tast for å gå tilbake til menyen")


def sok(sokeTekst):
    data_fornavn = telefonkatalog.loc[telefonkatalog["fornavn"] == sokeTekst]
    data_etternavn = telefonkatalog.loc[telefonkatalog["etternavn"] == sokeTekst]   
    data_tlf = telefonkatalog.loc[telefonkatalog["telefonnummer"] == sokeTekst]   
    
    df = pd.concat([data_fornavn, data_etternavn, data_tlf])
    df = df.drop_duplicates()
    
    return df


def sokPerson():
    
    if telefonkatalog.empty:
        print("Det er ingen registrerte perosner i katalogen")
        return
        
    else:
        tekst = input("Skriv søkeord her: ")
        
        sokRes = sok(tekst)
        
        if sokRes.empty:
            print("Fant ingenting ved det søket.")
        else:
            for person in sokRes.iterrows():
                
                print("{0} {1} har telefonnummer {2}".format(
                    person[1]["fornavn"], person[1]["etternavn"], person[1]["telefonnummer"]
                ))
    input("Trykk en tast for å gå tilbake til menyen")


def visAllePersoner(pandaForm=False): 
    if telefonkatalog.empty:
        print("Det er ingen registrerte personer i katalogen")
        input("Trykk en tast for å gå tilbake til menyen")
        return
    
    if pandaForm:
        print(telefonkatalog)
        input("Trykk en tast for å gå tilbake til menyen")
    else:
        print("************************************************************************************")
        for index, personer in telefonkatalog.iterrows():
            
            print("*Fornavn: {:15s} Etternavn: {:15s} Telefonnummer: {:8s}".format(personer["fornavn"], personer["etternavn"], personer["telefonnummer"]))
        print("************************************************************************************")
        
        input("Trykk en tast for å gå tilbake til menyen")


def utfoerMenyvalg(valgtTall):
    global kjorer
    
    #input returnerer string
    if valgtTall == "1":
        registrerPerson()

    elif valgtTall == "2":
        sokPerson()

    elif valgtTall == "3":
        visAllePersoner()

    elif valgtTall == "4":
        bekreftelse = input("Er du sikker på at du ivl avslutte? J/N")
        if bekreftelse == "J" or bekreftelse == "j":
            kjorer = False
            
        else:
            return

    else:
        nyttForsoek = input("Ugyldig valg. Velg et tall mellom 1-4")
        utfoerMenyvalg(nyttForsoek)


def mainloop():    
    while kjorer:
        printMeny()
        
        menyvalg = input("Skriv inn tall for å velge fra menyen:")
        utfoerMenyvalg(menyvalg)


mainloop()
exit()
    