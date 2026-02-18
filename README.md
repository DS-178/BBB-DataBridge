# BBB DataBridge 🌉

![Version](https://img.shields.io/github/v/release/DS-178/BBB-DataBridge?label=Version&color=green)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux-blue)
![Python](https://img.shields.io/badge/Python-3.11%2B-yellow)

**BBB DataBridge** ist ein spezialisiertes Export-Tool, das die Brücke zwischen **Pretix** und **Datacool** schlägt. Es konvertiert komplexe Pretix-CSV-Exporte in ein sauberes, formatiertes Excel-Format, das direkt weiterverarbeitet werden kann.

## ✨ Features

* **GUI-basiert:** Einfache und moderne Benutzeroberfläche (basierend auf CustomTkinter).
* **Intelligente Filterung:**
    * Filter nach Status (Nur Bezahlt, Nur Offen oder Alle).
    * Automatische Entfernung von stornierten Tickets.
* **Formatierung:** Erstellt automatisch `.xlsx` Dateien mit korrekten Spalten für Datacool.
* **Auto-Update:** Prüft beim Start automatisch auf GitHub, ob eine neue Version verfügbar ist.
* **Cross-Platform:** Verfügbar als `.exe` für Windows und als Binary für Linux.

## 🚀 Installation & Nutzung

### Für Windows Nutzer
1.  Gehe zu den [Releases](https://github.com/DS-178/BBB-DataBridge/releases/latest).
2.  Lade die Datei `BBB-Export-Tool.exe` herunter.
3.  Doppelklicke die Datei zum Starten (keine Installation notwendig).

### Für Linux Nutzer (Kubuntu, Ubuntu, etc.)
1.  Gehe zu den [Releases](https://github.com/DS-178/BBB-DataBridge/releases/latest).
2.  Lade die Datei `BBB-Export-Tool_Linux` herunter.
3.  **Wichtig:** Mache die Datei ausführbar:
    * *Rechtsklick -> Eigenschaften -> Berechtigungen -> "Ausführbar" ankreuzen.*
    * Oder per Terminal: `chmod +x BBB-Export-Tool_Linux`
4.  Doppelklick zum Starten.

## 🛠 Entwicklung

Möchtest du am Code arbeiten? Hier ist das Setup.

### Voraussetzungen
* Python 3.10 oder höher
* Git

### Setup

1.  **Repository klonen:**
    ```bash
    git clone [https://github.com/DS-178/BBB-DataBridge.git](https://github.com/DS-178/BBB-DataBridge.git)
    cd BBB-DataBridge
    ```

2.  **Virtuelle Umgebung erstellen:**
    ```bash
    python -m venv .venv
    # Windows:
    .venv\Scripts\activate
    # Linux:
    source .venv/bin/activate
    ```

3.  **Abhängigkeiten installieren:**
    ```bash
    pip install -r requirements.txt
    ```
    *Hinweis für Linux:* Du benötigst zusätzlich `python3-tk` (`sudo apt install python3-tk`).

4.  **Starten:**
    ```bash
    python main.py
    ```

## 📦 Build (Executable erstellen)

Das Projekt nutzt **GitHub Actions**, um automatisch Releases zu erstellen. Um lokal zu bauen:

**Windows:**
```powershell
python -m PyInstaller --noconsole --onefile --clean --icon="logo.ico" --name "BBB-Export-Tool" --collect-all customtkinter main.py
