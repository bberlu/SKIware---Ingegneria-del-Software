SKIware - Gestionale per il noleggio sci - Leonardo Berluti - S1125457

Che cos’è?
----------
SKIware e' un gestionale per un negozio di noleggio sci.
Permette di gestire: clienti, attrezzatura (sci, snowboard, scarponi,
caschi, armadietti), carnet a ingressi o stagionali, prenotazioni
e assegnamenti (noleggi) con emissione automatica della ricevuta.

Come si avvia
-------------
1. Installare i programmi indicati nel file requisiti.txt
2. Aprire il terminale nella cartella SKIware/app
3. Eseguire:  python3 main.py

All'avvio compare la finestra di accesso: il sistema e' riservato
al personale (amministratori e ski-man); i clienti non accedono.
Al primo avvio viene creato automaticamente un amministratore
predefinito con cui entrare:
    codice utente: 0
    password:      Admin2027
Solo l’amministratore è in grado di vedere tutte le gestioni

Dopo l'accesso si apre il menu principale con cinque sezioni:
- Gestione Utenti         -> inserire, consultare ed eliminare clienti,
                             ski-man e amministratori
- Gestione Attrezzatura   -> inserire e gestire sci, snowboard, scarponi,
                             caschi e armadietti
- Gestione Carnet         -> vendere carnet a un cliente
- Gestione Prenotazioni   -> prenotare (almeno 24h prima); disdetta con
                             rimborso solo fino a 48h prima dell'inizio
- Gestione Assegnamenti   -> registrare i noleggi, impostare il valore DIN
                             (obbligatorio per gli sci), consegna e ritiro

Come si eseguono i test
-----------------------
Dalla cartella SKIware/app eseguire:
    python3 -m unittest discover -s Tests

Struttura del progetto
----------------------
SKIware/
    README.txt      -> questo file
    requisiti.txt   -> requisiti per l'installazione
    app/
        main.py     -> punto di ingresso dell'applicazione
        Models/     -> le entita' (Cliente, Sci, Carnet, ...)
        Repos/      -> salvataggio e caricamento dei dati (file json)
        Services/   -> la logica del programma (i "gestori")
        Views/      -> le finestre grafiche (PyQt6)
        Tests/      -> i test automatici (unittest)
        Data/       -> i file json con i dati salvati

I dati vengono salvati automaticamente nella cartella app/Data
a ogni operazione: alla riapertura del programma si ritrovano
tutti i dati inseriti.