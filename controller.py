import time
import flet as ft

import model as md

class SpellChecker:

    def __init__(self, view):
        self._multiDic = md.MultiDictionary()
        self._view = view

    def handleSentence(self, txtIn, language, modality):
        txtIn = replaceChars(txtIn.lower())

        words = txtIn.split()
        paroleErrate = " - "

        match modality:
            case "Default":
                t1 = time.time()
                parole = self._multiDic.searchWord(words, language)
                for parola in parole:
                    if not parola.corretta:
                        paroleErrate = paroleErrate + str(parola) + " - "
                t2 = time.time()
                return paroleErrate, t2 - t1

            case "Linear":
                t1 = time.time()
                parole = self._multiDic.searchWordLinear(words, language)
                for parola in parole:
                    if not parola.corretta:
                        paroleErrate = paroleErrate + str(parola) + " "
                t2 = time.time()
                return paroleErrate, t2 - t1

            case "Dichotomic":
                t1 = time.time()
                parole = self._multiDic.searchWordDichotomic(words, language)
                for parola in parole:
                    if not parola.corretta:
                        paroleErrate = paroleErrate + str(parola) + " - "
                t2 = time.time()
                return paroleErrate, t2 - t1
            case _:
                return None


    def handleLinguaChange(self, e):
        '''Conotrlla il corretto selezionamento della lingua'''
        lingua = e.control.value
        if lingua:
            self._view._ddPrint.controls.append(
                ft.Text(f"Lingua selezionota: {lingua}.")
            )

    def handleRicercaChange(self, e):
        '''Controlla che l'utente abbia selezionato il metodo di ricerca'''

        scelta = e.control.value
        if scelta:
            self._view._ddPrint.controls.append(
                ft.Text(f"Modalità di ricerca impostata su '{scelta}'.")
            )
            self._view.update()

    def handleSpellCheck(self, e):
        '''Effettua lo spell checker'''
        testo = self._view.txtInput.value
        lingua = self._view._ddLingua.value
        mod = self._view._ddRicerca.value

        if not lingua or not mod or not testo or testo.strip() == "": return

        try:
            # La funzione handleSentence restituisce una tupla: (stringa_errori, tempo)
            risultato = self.handleSentence(testo, lingua, mod)

            # Gestione del punto cieco (se modality non corrisponde a nessun case)
            if risultato is None:
                self._view._ddPrint.controls.append(ft.Text("Errore: Modalità di ricerca non supportata.", color="red"))
                self._view.update()
                return

            parole_errate, tempo = risultato

            # 4. Output Formattato nella ListView (Row 3)
            # La traccia chiede: 1. Frase inserita, 2. Parole errate, 3. Tempo richiesto.
            self._view._ddPrint.controls.append(
                ft.Text(
                    f"1. Frase inserita: {testo}\n2. Parole errate: {parole_errate}\n3. Tempo richiesto: {tempo:.6f} secondi")
            )
            self._view._ddPrint.controls.append(ft.Divider())  # Separatore visivo per la prossima ricerca

        except Exception as ex:
            self._view._ddPrint.controls.append(ft.Text(f"Errore di sistema durante l'analisi: {ex}", color="red"))

            # 5. Pulizia (Requisito di traccia: "svuotare il TextField")
        self._view.txtInput.value = ""

        # 6. Aggiornamento finale dell'interfaccia
        self._view.update()




    def printMenu(self):
        print("______________________________\n" +
              "      SpellChecker 101\n"+
              "______________________________\n " +
              "Seleziona la lingua desiderata\n"
              "1. Italiano\n" +
              "2. Inglese\n" +
              "3. Spagnolo\n" +
              "4. Exit\n" +
              "______________________________\n")




def replaceChars(text):
    chars = "\\`*_{}[]()>#+-.!$?%^;,=_~"
    for c in chars:
        text = text.replace(c, "")
    return text








