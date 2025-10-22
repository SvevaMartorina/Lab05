import flet as ft

import automobile
from alert import AlertManager
from autonoleggio import Autonoleggio

FILE_AUTO = "automobili.csv"

def main(page: ft.Page):
    page.title = "Lab05"
    page.horizontal_alignment = "center"
    page.theme_mode = ft.ThemeMode.DARK

    # --- ALERT ---
    alert = AlertManager(page)

    # --- LA LOGICA DELL'APPLICAZIONE E' PRESA DALL'AUTONOLEGGIO DEL LAB03 ---
    autonoleggio = Autonoleggio("Polito Rent", "Alessandro Visconti")
    try:
        autonoleggio.carica_file_automobili(FILE_AUTO) # Carica il file
    except Exception as e:
        alert.show_alert(f"❌ {e}") # Fa apparire una finestra che mostra l'errore

    # --- UI ELEMENTI ---

    # Text per mostrare il nome e il responsabile dell'autonoleggio
    txt_titolo = ft.Text(value=autonoleggio.nome, size=38, weight=ft.FontWeight.BOLD)
    txt_responsabile = ft.Text(
        value=f"Responsabile: {autonoleggio.responsabile}",
        size=16,
        weight=ft.FontWeight.BOLD
    )

    # TextField per responsabile
    input_responsabile = ft.TextField(value=autonoleggio.responsabile, label="Responsabile")

    # ListView per mostrare la lista di auto aggiornata
    lista_auto = ft.ListView(expand=True, spacing=5, padding=10, auto_scroll=True)

    # Tutti i TextField per le info necessarie per aggiungere una nuova automobile (marca, modello, anno, contatore posti)
    input_marca = ft.TextField(label = "Marca",width=150)
    input_modello = ft.TextField(label = "Modello",width=150 )
    input_anno = ft.TextField(label = "Anno",width=150)

    def aggiungi_posto(e): #funzione per aggiungere un posto
        valore_attuale = int(txtOut.value)
        txtOut.value = valore_attuale + 1 #aggiorno il contatore
        txtOut.update() #aggiorno la pagine

    def rimuovi_posto(e): #funzione per rimuovere un posto
        valore_attuale = int(txtOut.value)
        txtOut.value = valore_attuale - 1 #aggiorno il contatore
        txtOut.update() #aggiorno la pagina

    #creo il bottone con l'icona meno
    bottone_meno = ft.IconButton( icon = ft.Icons.REMOVE,
                                  icon_color = 'red',
                                  icon_size = 24,
                                  on_click = rimuovi_posto)
    #creo il bottone con l'icona più
    bottone_piu = ft.IconButton( icon = ft.Icons.ADD,
                                 icon_color = 'green',
                                 icon_size = 24,
                                 on_click = aggiungi_posto)
    #creo lo spazio centrale in cui trovo il valore (val_iniziale = 0)
    txtOut = ft.TextField( width = 150, disabled=True,
                          value = 0,
                          border_color = 'white',
                          text_align = ft.TextAlign.CENTER)
    #assemblo i tre componenti del bottone di aggiunta auto, creando una riga
    pulsante_aggiunta_auto = ft.Row([bottone_meno, txtOut, bottone_piu])

    #


    # --- FUNZIONI APP ---
    def aggiorna_lista_auto():
        lista_auto.controls.clear()
        for auto in autonoleggio.automobili_ordinate_per_marca():
            stato = "✅" if auto.disponibile else "⛔"
            lista_auto.controls.append(ft.Text(f"{stato} {auto}"))
        page.update()

    # --- HANDLERS APP ---
    def cambia_tema(e):
        page.theme_mode = ft.ThemeMode.DARK if toggle_cambia_tema.value else ft.ThemeMode.LIGHT
        toggle_cambia_tema.label = "Tema scuro" if toggle_cambia_tema.value else "Tema chiaro"
        page.update()

    def conferma_responsabile(e):
        autonoleggio.responsabile = input_responsabile.value
        txt_responsabile.value = f"Responsabile: {autonoleggio.responsabile}"
        page.update()

    # Handlers per la gestione dei bottoni utili all'inserimento di una nuova auto
    #funzione per la conferma dell'azione di aggiunta della nuova auto
    def conferma_nuova_auto(e):
        marca = input_marca.value
        modello = input_modello.value
        if marca == '' or modello == '':
            alert.show_alert('ERRORE: Inserisci valori per marca e modello')
            return
        #controllo i campi numerici
        if str(input_anno.value).isdigit() and str(txtOut.value).isdigit():
            anno = int(input_anno.value)
            posti = int(txtOut.value)
        else:
            alert.show_alert('ERRORE: inserisci valori numerici per anno e posti')
            return
        #dopo aver effettuato i controlli aggiungo l'automobile alla struttura dati dell'autonoleggio
        autonoleggio.aggiungi_automobile(marca, modello, anno, posti)
        aggiorna_lista_auto()

        input_marca.value = ''
        input_modello.value = ''
        input_anno.value = ''
        txtOut.value = 0
        alert.show_alert('Automobile inserita con successo')
        page.update()

    # --- EVENTI ---
    toggle_cambia_tema = ft.Switch(label="Tema scuro", value=True, on_change=cambia_tema)
    pulsante_conferma_responsabile = ft.ElevatedButton("Conferma", on_click=conferma_responsabile)

    # Bottoni per la gestione dell'inserimento di una nuova auto
    pulsante_conferma_nuova_auto = ft.ElevatedButton("Conferma", on_click=conferma_nuova_auto)
    page.update()

    # --- LAYOUT ---
    page.add(
        toggle_cambia_tema,

        # Sezione 1
        txt_titolo,
        txt_responsabile,
        ft.Divider(),

        # Sezione 2
        ft.Text("Modifica Informazioni", size=20),
        ft.Row(spacing=200,
               controls=[input_responsabile, pulsante_conferma_responsabile],
               alignment=ft.MainAxisAlignment.CENTER),

        # Sezione 3, interfaccia per aggiungere una nuova automobile
        ft.Text("Aggiungi nuova automobile", size=20),
        ft.Row(spacing=100,
               controls = [input_marca, input_modello, input_anno, pulsante_aggiunta_auto, pulsante_conferma_nuova_auto],
               alignment=ft.MainAxisAlignment.CENTER),

        # Sezione 4
        ft.Divider(),
        ft.Text("Automobili", size=20),
        lista_auto,
    )
    aggiorna_lista_auto()

ft.app(target=main)
