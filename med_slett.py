import pandas as pd
import mysql.connector

def conn(_host="localhost", _user="root", _password="", _database="telefondb"):
    global mydb, mycursor

    mydb = mysql.connector.connect(
        host=_host,
        user=_user,
        password=_password,
        database=_database
    )

    mycursor = mydb.cursor()

conn()

mycursor.execute("SELECT * FROM telefonkatalog")

myresult = mycursor.fetchall()

kjorer = True

telefonkatalog = pd.DataFrame(myresult, columns=['id', 'fornavn', 'etternavn', 'telefonnummer'])

def printMeny():
    print("--------------- Telefonkatalog ---------------")
    print("| 1. Legg til ny person                      |")
    print("| 2. Søk opp person eller telefonnummer      |") 
    print("| 3. Vis alle personer                       |") 
    print("| 4. Slett personer                          |") 
    print("| 5. Avslutt                                 |")
    print("----------------------------------------------") 


def registrerPerson ():
    global telefonkatalog
    
    fornavn = input("Skriv inn fornavn:")
    etternavn = input ("Skriv inn etternavn:")
    telefonnummer = input("Skriv inn telefonnummer:")
    
    sql = "INSERT INTO telefonkatalog (fornavn, etternavn, telefonnummer) VALUES (%s, %s, %s)"
    val = (fornavn, etternavn, telefonnummer)
    mycursor.execute(sql, val)
    
    mydb.commit()    

    nyRegistrering = {
        "id": [int(mycursor.lastrowid)],
        "fornavn": [fornavn],
        "etternavn": [etternavn],
        "telefonnummer": [telefonnummer]
        }
    
    newdf = pd.DataFrame(nyRegistrering, columns=["id", "fornavn", "etternavn", "telefonnummer"])
    
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


def visAllePersoner(form="erik"): 
    if telefonkatalog.empty:
        print("Det er ingen registrerte personer i katalogen")
        
        return
    
    if form == "panda":
        print(telefonkatalog)
    
    elif form == "medid":
        print("************************************************************************************")
        for index, personer in telefonkatalog.iterrows():
            
            print("*Fornavn: {:15s} Etternavn: {:15s} Telefonnummer: {:8s} Id: {:2s} *".format(personer["fornavn"], personer["etternavn"], personer["telefonnummer"], str(personer["id"])))
        print("************************************************************************************")
    
    elif form == "erik":
        print("************************************************************************************")
        for index, personer in telefonkatalog.iterrows():
            
            print("*Fornavn: {:15s} Etternavn: {:15s} Telefonnummer: {:8s} *".format(personer["fornavn"], personer["etternavn"], personer["telefonnummer"]))
        print("************************************************************************************")
    else:
        print("Du har gitt en feil form")
        
        

def sletting(df):
    global telefonkatalog
    
    telefonkatalog = telefonkatalog.drop(df.index)
    
    mycursor.execute("DELETE FROM telefonkatalog WHERE id = '" + str(df.iat[0, 0]) + "'")
    mydb.commit()
    
        

def velgPersonSletting():
    
    visAllePersoner("medid")
    
    slettId = input("Skriv inn id på den du vil slette, eller skriv N for å gå ut: ")
    
    if slettId == "N" or slettId == "n":
        return
    elif not slettId.isnumeric():
        print("Id kan ikke være bokstaver")
        return

    slettdf = telefonkatalog.loc[telefonkatalog["id"] == int(slettId)]
    
    if slettdf.empty:
        print("fant ingen info med den id-en")
        return
    
    sletting(slettdf)
        

def utfoerMenyvalg(valgtTall):
    global kjorer
    
    #input returnerer string
    if valgtTall == "1":
        registrerPerson()

    elif valgtTall == "2":
        sokPerson()

    elif valgtTall == "3":
        visAllePersoner()
        input("Trykk en tast for å gå tilbake til menyen")

    elif valgtTall == "4":
        velgPersonSletting()
    
    elif valgtTall == "5":
        bekreftelse = input("Er du sikker på at du ivl avslutte? J/N")
        if bekreftelse == "J" or bekreftelse == "j":
            kjorer = False
            
        else:
            return
    else:
        nyttForsoek = input("Ugyldig valg. Velg et tall mellom 1-5")
        utfoerMenyvalg(nyttForsoek)


def mainloop():    
    while kjorer:
        printMeny()
        
        menyvalg = input("Skriv inn tall for å velge fra menyen:")
        utfoerMenyvalg(menyvalg)


mainloop()
exit()
    