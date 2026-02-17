class AppConfig:
    # ACHTUNG: Hier vorne müssen 4 Leerzeichen sein!
    APP_NAME = "Bremer Baumwollbörse – Data Bridge"
    VERSION = "7.0 Final"

    ZIEL_SPALTEN = [
        'Order code',
        'Attendee name',
        'Attendee name: Given name',
        'Attendee name: Family name',
        'Product',
        'Price',
        'Checked in',
        'Checked out',
        'Automatically checked in',
        'E-mail',
        'Phone number',
        'Your country:',
        'City',
        'Company',
        'Voucher code',
        'Order date',
        'Order time',
        'I acknowledge being registered in the list of participants'
    ]

    SMART_CASING_COLUMNS = [
        'Attendee name',
        'Attendee name: Given name',
        'Attendee name: Family name',
        'City'
    ]

    STATUS_COL_SEARCH = ['payment status', 'bezahlstatus', 'status', 'order status']
    STATUS_PAID_VALUES = ['paid', 'bezahlt', 'komplett bezahlt', 'c']
    STATUS_IGNORE_VALUES = ['canceled', 'storniert', 'expired', 'abgelaufen', 'abgebrochen']
    EMPTY_CELL_COLOR = "FFFF00"

    SUCH_MAPPING = {
        'Order code':       ['order code', 'bestellnummer', 'auftragsnummer', 'order'],
        'Attendee name':    ['attendee name', 'teilnehmername', 'teilnehmer'],
        'Attendee name: Given name': ['given name', 'vorname', 'first name'],
        'Attendee name: Family name': ['family name', 'nachname', 'surname', 'last name'],
        'Product':          ['product', 'produkt', 'ticket', 'artikel'],
        'Price':            ['price', 'preis', 'wert'],
        'Checked in':       ['checked in', 'eingecheckt', 'check-in'],
        'Checked out':      ['checked out', 'ausgecheckt'],
        'Automatically checked in': ['automatically', 'automatisch'],
        'E-mail':           ['e-mail', 'email', 'mail', 'e-post'],
        'Phone number':     ['phone', 'telefon', 'mobil', 'tel.', 'mobile'],
        'Your country:':    ['country', 'land', 'staat', 'invoice address: country', 'rechnungsadresse: land', 'nation'],
        'City':             ['city', 'stadt', 'ort', 'town', 'invoice address: city', 'rechnungsadresse: stadt', 'location'],
        'Company':          ['company', 'firma', 'unternehmen', 'business', 'invoice address: company', 'rechnungsadresse: firma'],
        'Voucher code':     ['voucher', 'gutschein', 'coupon'],
        'Order date':       ['order date', 'bestelldatum', 'date', 'datum'],
        'Order time':       ['order time', 'uhrzeit', 'time', 'zeit'],
        'I acknowledge being registered in the list of participants': ['acknowledge', 'registered', 'participants', 'liste', 'einverstanden', 'list of participants']
    }