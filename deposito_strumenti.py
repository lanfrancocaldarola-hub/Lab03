from operator import attrgetter


class Strumento:
    def __init__(self, codice, tipo, marca, anno_acquisto, valore):
        self.codice = codice
        self.tipo = tipo
        self.marca = marca
        self.anno_acquisto = int(anno_acquisto)
        self.valore = float(valore)

    def __str__(self):
        return f"[{self.codice}] {self.tipo} - {self.marca} ({self.anno_acquisto}) - {self.valore:.2f}€"


class Prestito:
    def __init__(self, codice, data, id_strumento, cognome_allievo):
        self.codice = codice
        self.data = data
        self.id_strumento = id_strumento
        self.cognome_allievo = cognome_allievo

    def __str__(self):
        return f"[{self.codice}] Strumento {self.id_strumento} in prestito a {self.cognome_allievo} dal {self.data}"


class DepositoStrumenti:
    def __init__(self, nome, responsabile):
        """Inizializza gli attributi e le strutture dati"""
        self.nome = nome
        self.responsabile = responsabile
        self.strumenti = []
        self.prestiti = []
        self.ultimo_id_strumento = 0
        self.ultimo_id_prestito = 0

    def carica_file_strumenti(self, file_path):
        """Carica gli strumenti dal file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for riga in f:
                    riga = riga.strip()
                    if not riga:
                        continue

                    parti = riga.split(',')
                    if len(parti) == 5:
                        codice, tipo, marca, anno, valore = parti
                        strumento = Strumento(codice, tipo, marca, anno, valore)
                        self.strumenti.append(strumento)

                        if codice.startswith('S'):
                            num = int(codice[1:])
                            if num > self.ultimo_id_strumento:
                                self.ultimo_id_strumento = num
        except FileNotFoundError:
            raise FileNotFoundError(f"Errore: il file {file_path} non è stato trovato.")

    def aggiungi_strumento(self, tipo, marca, anno_acquisto, valore):
        """Aggiunge uno strumento nel deposito: aggiunge solo nel sistema e non aggiorna il file"""
        self.ultimo_id_strumento += 1
        codice = f"S{self.ultimo_id_strumento}"

        nuovo_strumento = Strumento(codice, tipo, marca, anno_acquisto, valore)
        self.strumenti.append(nuovo_strumento)
        return nuovo_strumento

    def strumenti_ordinati_per_marca(self):
        """Ordina gli strumenti per marca in ordine alfabetico"""
        return sorted(self.strumenti, key=attrgetter('marca'))

    def nuovo_prestito(self, data, id_strumento, cognome_allievo):
        """Crea un nuovo prestito"""
        strumento_trovato = False
        for s in self.strumenti:
            if s.codice == id_strumento:
                strumento_trovato = True
                break

        if not strumento_trovato:
            raise Exception(f"Errore: lo strumento con ID {id_strumento} non esiste nel deposito.")

        for p in self.prestiti:
            if p.id_strumento == id_strumento:
                raise Exception(f"Errore: lo strumento {id_strumento} è già in prestito.")

        self.ultimo_id_prestito += 1
        codice_prestito = f"P{self.ultimo_id_prestito}"

        prestito = Prestito(codice_prestito, data, id_strumento, cognome_allievo)
        self.prestiti.append(prestito)
        return prestito

    def termina_prestito(self, id_prestito):
        """Termina un prestito in atto"""
        prestito_da_rimuovere = None
        for p in self.prestiti:
            if p.codice == id_prestito:
                prestito_da_rimuovere = p
                break

        if prestito_da_rimuovere is None:
            raise Exception(f"Errore: nessun prestito trovato con ID {id_prestito}.")

        self.prestiti.remove(prestito_da_rimuovere)