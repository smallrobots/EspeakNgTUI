# ESpeak-ng TUI

**Descrizione**: Questo progetto mira a creare un'applicazione TUI (Text-based User Interface) rapida basata su la libreria Textual (di Textualize) per testare e configurare in modo interattivo i parametri del motore TTS eSpeak-NG. L'interfaccia sarà interamente testuale nel terminale e fornirà controlli per regolare i parametri della sintesi vocale, inserire messaggi di testo da sintetizzare e riprodurli, oltre a visualizzare e gestire frasi predefinite da riutilizzare durante demo o prove.

## Funzionalità Principali
- **Pannello Controlli Parametri**: Sul lato sinistro dell'interfaccia verranno presentati controlli per impostare i parametri di eSpeak-NG (come volume, velocità, pitch, voce, etc.). L'utente potrà regolare questi valori prima di sintetizzare il testo.

- **Inserimento Testo e Riproduzione**: Nella parte inferiore sinistra sarà disponibile una casella di testo in cui scrivere il messaggio da sintetizzare e un pulsante _Riproduci_ per avviare la sintesi vocale con i parametri correnti. Premendo il pulsante, l'app eseguirà espeak-ng con le opzioni selezionate per far ascoltare l'audio generato.

- **Anteprima Comando**: Al fondo della schermata verrà mostrata la stringa di comando espeak-ng generata (comprensiva di parametri e testo). Questo permette di vedere esattamente quale comando verrebbe eseguito – utile per copiare il comando o eseguirlo manualmente se necessario. Nota: Grazie a Textual è possibile avere elementi fissi in cima o in fondo allo schermo (header/footer) per scopi come questo

- **Elenco Messaggi Predefiniti**: Sul lato destro dell'interfaccia verrà visualizzata una lista di frasi di esempio o predefinite. Ciascuna voce in elenco potrà essere selezionata per caricare rapidamente quel testo (e potenzialmente i relativi parametri salvati) nei controlli a sinistra, in modo da poterlo riprodurre al volo. Ciò funge da libreria di messaggi utili per le demo: ad esempio, si potrà preparare un set di frasi tipiche e richiamarle con un click durante una presentazione.

- **Interfaccia Interattiva e Responsive**: L'app si aggiornerà dinamicamente. Modificando i parametri, l'anteprima del comando verrà aggiornata in tempo reale. Analogamente, selezionando una voce dall'elenco di destra, il testo verrà inserito nella casella a sinistra e pronto per la sintesi. L'interfaccia TUI sarà cross-platform (funzionante su Windows, Linux, macOS in un normale terminale) e non richiede GUI grafiche.

## Tecnologia e Libreria Textual
Useremo la libreria Textual di Textualize per costruire l'interfaccia testuale. Textual fornisce una ricca collezione di widget interattivi (come pulsanti, alberi, tabelle, campi di input testo, aree di testo, ecc.) ed un sistema di layout flessibile, che permette di realizzare interfacce utente testuali di qualsiasi complessità

In particolare, sfrutteremo queste caratteristiche di Textual:
- Layout a Colonne: Organizzeremo la finestra principale in due colonne (sinistra e destra) usando i contenitori di layout di Textual. In pratica, un contenitore orizzontale conterrà due contenitori verticali, ottenendo così una riga con due colonne affiancate

- La colonna sinistra ospiterà i controlli e l'input testo, mentre la colonna destra mostrerà la lista di messaggi predefiniti. Si potrà assegnare un rapporto di larghezza (es. colonna sinistra più ampia della destra) utilizzando le unità flessibili di Textual (fractions fr) nelle regole CSS, ad esempio impostando il primo pannello al 66% e il secondo al 34% circa della larghezza totale (p.e. grid-columns: 2fr 1fr).


## Widget di Input e Pulsanti
Per i controlli interattivi useremo widget forniti da Textual come:
 - Input: campi di input sia per testo (messaggio da sintetizzare) che per valori numerici (parametri). Textual offre widget di input testuale semplici e mascherati, nonché selezioni e liste
- Button: un pulsante "Riproduci" per avviare la sintesi TTS.
- Label/Static Text: etichette per i nomi dei parametri e widget testuali statici per mostrare l'anteprima del comando.
- ListView / DataTable: per implementare la lista dei messaggi predefiniti, si può impiegare un widget di lista (list view) fornito dalla libreria, che permetta la selezione tramite tastiera o mouse.
- Stili e Temi: Textual supporta CSS per personalizzare l'aspetto della TUI. Potremo ad esempio evidenziare la selezione corrente nella lista di messaggi, o usare colori per separare visivamente le sezioni. Inoltre, Textual include temi predefiniti che garantiscono un look gradevole di default.
- Gestione Eventi e Reattività: La logica dell'app utilizzerà il modello event-driven di Textual. Ad esempio, premendo il pulsante di riproduzione verrà catturato un evento che attiverà la chiamata al comando espeak-ng. I campi di input per i parametri potranno essere collegati a variabili reactive per aggiornare automaticamente l'anteprima comando in basso quando cambiano.

Grazie all'architettura asincrona di Textual, l'app potrà eseguire il comando di sintesi senza bloccare l'interfaccia (usando magari thread o coroutines async se necessario).

## Parametri TTS Configurabili
L'app consentirà di regolare i principali parametri di eSpeak-NG tramite l'interfaccia. I parametri previsti includono:
 - Volume (-a): amplitude/volume dell'audio, in range 0–200 (default 100)
 - Velocità (-s): velocità di parlato in parole per minuto. Default ~175 wpm; minimo ~80, massimo pratico ~500
 - Pitch (-p): tono della voce, range 0–99 (default 50)
 - Voce/Lingua (-v): selezione della voce (lingua o accent specifico). Si potranno elencare le voci disponibili (ad es. output di espeak-ng --voices) e scegliere quella desiderata. In eSpeak, le voci sono identificate da codici (es. en per English, it per Italiano, es per Español, ecc.) e si possono aggiungere varianti di timbro dopo il +. Ad esempio -v it+f2 seleziona la voce italiana con variante femminile
 - Sono disponibili varianti predefinite da +m1 a +m7 (maschili di tono via via più basso) e +f1 a +f4 (femminili, tono più alto)
- Oltre a varianti speciali come +whisper (sussurro) o +croak
 - Pausa tra parole (-g): eventuale pausa aggiuntiva tra le parole, in intervalli di 10 millisecondi
 - Questo controllo permette di scandire più chiaramente frasi lente inserendo piccole pause.
(Nota: Altri parametri di eSpeak-NG potrebbero essere aggiunti in futuro – ad esempio indicatore di maiuscole -k, formato SSML -m, ecc. – ma i sopracitati sono i principali per l'uso comune.)

## Requisiti
- Python 3.10+ (per eseguire l'app Textual).
- Libreria Textual versione recente (installabile via pip). Ad esempio: pip install textual textual-dev.
- eSpeak-NG installato sul sistema e accessibile nel PATH come comando espeak-ng. (Su Debian/Ubuntu sudo apt install espeak-ng, su Windows l'eseguibile disponibile, ecc.)
- Ambiente Terminale Compatibile: l'app gira in un terminale con supporto UTF-8. Per un'esperienza ottimale, usare dimensioni di finestra adeguate (min. 80x24 caratteri). Textual è cross-platform, quindi funzionerà su sistemi Unix, Windows (PowerShell/CMD/WSL), e macOS.
## Installazione e Avvio
Installare Textual: Assicurarsi di avere la libreria Textual installata. Esempio:

```bash
pip install textual textual-dev
```
(Il pacchetto textual-dev non è obbligatorio ma fornisce strumenti di debug utili durante lo sviluppo.)

Clonare o Scaricare il Progetto: Ottenere il codice sorgente di questo repository (via git clone o download ZIP).
Installare eSpeak-NG: Verificare che il comando espeak-ng funzioni nel terminale. Provare ad eseguire espeak-ng "ciao" per test.
Lanciare l'App: Eseguire lo script principale (ad esempio python espeak_tui.py). Si aprirà la UI testuale nel terminale. In caso di problemi di rendering, assicurarsi che il terminale supporti colori ANSI e Unicode.
## Utilizzo dell'Applicazione
- Navigazione: Usare i tasti Tab/Shift+Tab per muoversi tra i controlli (parametri, campo testo, lista messaggi, pulsante). La lista di messaggi a destra è scrollabile con freccia su/giù e selezionabile con Invio.
- Impostazione Parametri: Modificare i valori desiderati nei campi dedicati (es. digitare un numero per volume, scegliere una voce dall'elenco se implementato, ecc.). Ogni variazione aggiornerà l'anteprima del comando in basso.
- Inserire Testo: Scrivere la frase da sintetizzare nel campo di input in basso a sinistra.
- Riprodurre Audio: Premere il pulsante Riproduci (o usare un tasto scorciatoia, ad es. Ctrl+P se previsto) per eseguire eSpeak-NG. Verrà riprodotto l'audio corrispondente al testo con i parametri impostati. Il comando esatto eseguito verrà mostrato nella barra inferiore.
- Usare Messaggi Predefiniti: Navigare nella colonna di destra e selezionare un messaggio per caricarlo. Il testo apparirà nel campo di input e i parametri potrebbero adeguarsi (se la funzionalità di salvare parametri per preset è implementata). Poi premere "Riproduci" normalmente. Questo consente di provare velocemente diverse frasi senza doverle digitare ogni volta.
- Uscita: Per chiudere l'app TUI, premere Ctrl+C oppure un comando dedicato (se implementato, ad esempio Ctrl+Q). In alternativa, usare il comando palette di Textual (Ctrl+P) e digitare "quit".
## Roadmap di Sviluppo
Di seguito una pianificazione delle fasi di sviluppo del progetto, che funge da roadmap:
1. Struttura Base dell'App: Creare un'app Textual minima (App) con uno screen principale. Definire il layout di massima: un contenitore orizzontale per dividere lo schermo in due colonne (sinistra/destra)
2. Implementare i widget segnaposto per le sezioni: ad es. un pannello sinistro per controlli (vuoto) e uno destro per la lista messaggi (vuoto), più un'area inferiore per l'anteprima comando (può essere un widget Footer di Textual o uno Static dockato in basso)
3. Verificare che la UI di base compaia e la finestra si possa ridimensionare mantenendo il layout (colonne che si dividono lo spazio).
4. Implementazione Controlli Parametri: Inserire nel pannello sinistro i widget effettivi per i parametri:
    - Label + Input per Volume (numerico 0-200).
    - Label + Input per Velocità (numerico 80-500).
    - Label + Input per Pitch (numerico 0-99).
    - Label + Input/Select per Voce (testuale o menu a tendina con codici lingua/voce disponibili).
    - Eventuali altri parametri (checkbox o slider per funzionalità booleane/graduali, es. pausa parole).

5. Organizzare questi controlli verticalmente (ad es. usando un container verticale interno o semplicemente più elementi uno sotto l'altro). In questa fase ci si può concentrare sul rendering corretto dei widget e associare ad ognuno una variabile reattiva nel codice (usando reactive() di Textual) per conservare il valore corrente.
6. Casella di Testo e Pulsante Riproduci: Sotto ai controlli dei parametri (sempre nel pannello sinistro) aggiungere un widget di input multilinea o singola linea per il testo da sintetizzare e un pulsante "Riproduci". All'attivazione del pulsante (gestire l'evento on_button_pressed), l'app dovrà leggere i valori correnti dei parametri e del testo e chiamare il comando espeak-ng. Inizialmente, per sviluppo, si può fare in modo che premendo il pulsante venga semplicemente stampato (nel log o nel footer) il comando che sarebbe eseguito. Successivamente, integreremo l'esecuzione reale.
7. Esecuzione del Comando TTS: Implementare la funzione che esegue realmente espeak-ng con i parametri selezionati. Si può usare Python subprocess.run in modalità non-bloccante o l'API asincrona di Textual per evitare freeze dell'interfaccia durante la riproduzione. Dato che l'audio verrà riprodotto sul sistema, assicurarsi di gestire correttamente l'avvio del processo. (Opzionalmente, catturare l'output o codici di errore da subprocess per mostrare eventuali errori nella UI.)
8. Anteprima del Comando: Implementare l'aggiornamento dinamico della stringa di comando mostrata nel footer/in basso. Ogni volta che un parametro cambia o il testo cambia, costruire la stringa equivalente (es: espeak-ng -v it+f2 -s 180 -p 70 -a 150 "Testo da sintetizzare"). Mostrare tale stringa nell'area di anteprima. Textual permetterà di aggiornare facilmente un widget di testo; si può farlo reagire tramite le proprietà reactive o tramite evento on_change dei campi input.
9. Lista dei Messaggi Predefiniti: Popolare la colonna di destra con un elenco (ListView) di messaggi esempio. In fase iniziale, può essere hard-coded (es. una lista di frasi tipiche). Implementare la selezione: quando l'utente seleziona una frase (evento on_list_view_selected), caricare quel testo nel campo di input principale e magari settare parametri associati (se decidiamo di memorizzare anche parametri per ogni frase). Questa funzionalità consente di preparare demo: prima della presentazione si impostano varie frasi con diverse voci/pitch, e durante la demo basta selezionarle e premere riproduci.
10. Salvataggio/Caricamento Configurazioni (Opzionale): Prevedere una struttura dati per salvare preset di configurazione (testo + parametri). Ciò potrebbe essere implementato salvando su file JSON o YAML una lista di preset. In un secondo momento, aggiungere comandi nell'app per salvare l'attuale configurazione come nuovo preset e per caricare preset esistenti. Questo andrebbe oltre il minimum viable product ma risulterebbe utile.
11. Refinimenti UI e UX: Migliorare la presentazione estetica utilizzando le funzionalità di Textual:
    - Aggiungere titoli o bordi alle sezioni (es. riquadro attorno ai controlli con titolo "Parametri", riquadro attorno alla lista con titolo "Frasi Salvate").
    - Colorare in modo diverso le etichette dei parametri vs i valori, per renderli distinguibili.
    - Introdurre shortcut da tastiera (es. tasto per focalizzare subito il campo testo, tasto rapido per play, ecc.) sfruttando il sistema di binding/command palette di Textual
    - Testare in diversi terminali e risoluzioni, ed eventualmente usare il layout responsive di Textual (ad esempio, se la larghezza è troppo poca per due colonne, passare temporaneamente a un layout verticale impilando le sezioni).
    - Testing e Debug: Sfruttare il framework di testing di Textual e/o textual-dev per intercettare problemi. Verificare che l'app non crashi se espeak-ng non è presente (magari mostrando un messaggio di errore gentile), o se vengono inseriti valori fuori range nei parametri (potremmo aggiungere validazione input).
12. Documentazione e Esempi: Completare il README (questo documento) con eventuali screenshot ASCII o diagrammi se utili, e aggiungere una breve guida all'utente finale. Fornire esempi di comandi e magari un elenco di voci consigliate da provare. Considerare aggiunta di una sezione FAQ (ad es. "Come aggiungo nuove frasi predefinite?", "Come salvo i preset?", "Perché l'audio non si sente su Windows?" ecc. con relative risposte).

Ogni fase della roadmap qui descritta potrà essere implementata e testata incrementalmente. Contributi e suggerimenti sono benvenuti: l'obiettivo è avere uno strumento semplice ma efficace per configurare la sintesi vocale di eSpeak-NG in modo interattivo e rapido, sfruttando la potenza di Textual per le UI testuali moderne.

## Riferimenti
- Textual Documentation – Textual widgets and layout
- Textual How-To – Designing Layouts with Horizontal/Vertical containers
- Textual Guide – Using Header/Footer for fixed layout elements
- eSpeak-NG Manual – Command line options and parameter ranges
