# PlantHub - Home Assistant Integration

Eine moderne und benutzerfreundliche Home Assistant Integration für die Überwachung von Pflanzen mit einer vollständig konfigurierbaren Dashboardkarte.

## 🚀 Features

- **Moderne Architektur**: Vollständig kompatibel mit den neuesten Home Assistant Standards
- **HACS-Integration**: Einfache Installation über HACS (Home Assistant Community Store)
- **Vollständig konfigurierbare Karte**: Alle Einstellungen können über den visuellen Editor vorgenommen werden
- **Mehrere Sensoren**: Überwachung von Feuchtigkeit, Temperatur, Licht und Dünger
- **Intelligente Statusanzeige**: Automatische Bewertung des Pflanzenzustands
- **Responsive Design**: Funktioniert auf allen Geräten und Bildschirmgrößen
- **Deutsche Lokalisierung**: Vollständig auf Deutsch verfügbar

## 📋 Voraussetzungen

- Home Assistant 2023.8.0 oder höher
- HACS (Home Assistant Community Store) installiert
- JavaScript-Integration aktiviert

## 🔧 Installation

### Über HACS (Empfohlen)

1. Öffne HACS in deinem Home Assistant
2. Gehe zu "Integrations"
3. Klicke auf das "+" Symbol
4. Suche nach "PlantHub"
5. Klicke auf "Download"
6. Starte Home Assistant neu

### Manuelle Installation

1. Lade den gesamten `custom_components/planthub` Ordner in deinen `config/custom_components/` Ordner
2. Starte Home Assistant neu
3. Gehe zu "Einstellungen" → "Geräte & Dienste"
4. Klicke auf "+ Integration hinzufügen"
5. Suche nach "PlantHub" und folge der Konfiguration

## ⚙️ Konfiguration

### Integration einrichten

1. Gehe zu "Einstellungen" → "Geräte & Dienste"
2. Klicke auf "+ Integration hinzufügen"
3. Suche nach "PlantHub"
4. Gib einen Namen für deine Pflanze ein
5. Gib eine eindeutige Pflanzen-ID ein
6. Klicke auf "Absenden"

### Dashboardkarte hinzufügen

1. Öffne dein Dashboard im Bearbeitungsmodus
2. Klicke auf "+ Karte hinzufügen"
3. Wähle "PlantHub" aus der Liste
4. Konfiguriere die Karte nach deinen Wünschen

## 🎨 Kartenkonfiguration

Die PlantHub-Karte bietet umfangreiche Konfigurationsmöglichkeiten:

### Grundlegende Einstellungen

- **Entity**: Wähle den PlantHub-Sensor aus
- **Anzeigename**: Überschreibt den Standard-Namen (optional)

### Angezeigte Metriken

- **Feuchtigkeit**: Zeigt den aktuellen Feuchtigkeitswert an
- **Temperatur**: Zeigt die aktuelle Temperatur an
- **Licht**: Zeigt den aktuellen Lichtwert an
- **Dünger**: Zeigt den aktuellen Düngerwert an

### Darstellungsoptionen

- **Theme**: Wähle zwischen hellem und dunklem Design
- **Kompakte Ansicht**: Reduziert die Größe der Karte

## 📊 Verfügbare Sensoren

Nach der Integration werden folgende Sensoren erstellt:

- `sensor.planthub_status`: Gesamtstatus der Pflanze (gesund/warnung/kritisch)
- `sensor.planthub_feuchtigkeit`: Feuchtigkeitswert in Prozent
- `sensor.planthub_temperatur`: Temperatur in °C
- `sensor.planthub_licht`: Lichtintensität in Lux
- `sensor.planthub_dünger`: Düngerwert in Prozent

## 🔍 Statusbewertung

Die Integration bewertet automatisch den Zustand deiner Pflanze:

- **Gesund** (grün): Feuchtigkeit ≥ 50%
- **Warnung** (orange): Feuchtigkeit 30-49%
- **Kritisch** (rot): Feuchtigkeit < 30%

## 🎯 Verwendungsbeispiele

### Einfache Überwachung
```yaml
type: custom:planthub-card
entity: sensor.planthub_status
name: "Meine Monstera"
```

### Vollständig konfigurierte Karte
```yaml
type: custom:planthub-card
entity: sensor.planthub_status
name: "Büropflanze"
show_moisture: true
show_temperature: true
show_light: false
show_fertilizer: true
theme: dark
compact: false
```

### Kompakte Ansicht
```yaml
type: custom:planthub-card
entity: sensor.planthub_status
compact: true
show_moisture: true
show_temperature: true
```

## 🛠️ Entwicklung

### Projektstruktur
```
custom_components/planthub/
├── __init__.py          # Hauptintegration
├── manifest.json        # Metadaten
├── config_flow.py       # Konfigurationsassistent
├── const.py            # Konstanten
├── sensor.py           # Sensoren
├── translations/       # Übersetzungen
│   └── de.json
└── frontend/          # Dashboardkarte
    └── dist/
        ├── planthub-card.js
        ├── planthub-card.js.map
        └── editor.js
```

### Anpassungen

Die Integration kann einfach angepasst werden:

1. **Neue Sensoren hinzufügen**: Bearbeite `sensor.py`
2. **Kartenstyling ändern**: Bearbeite `planthub-card.js`
3. **Editor erweitern**: Bearbeite `editor.js`
4. **Übersetzungen hinzufügen**: Bearbeite `translations/de.json`

## 🐛 Fehlerbehebung

### Häufige Probleme

**Karte wird nicht angezeigt:**
- Stelle sicher, dass JavaScript-Integration aktiviert ist
- Überprüfe die Browser-Konsole auf Fehler
- Starte Home Assistant neu

**Sensoren zeigen keine Werte:**
- Überprüfe die Integration in "Geräte & Dienste"
- Schaue in die Home Assistant Logs
- Stelle sicher, dass die Entity korrekt konfiguriert ist

**Visueller Editor funktioniert nicht:**
- Überprüfe die Browser-Konsole auf JavaScript-Fehler
- Stelle sicher, dass alle Frontend-Dateien korrekt installiert sind

## 📝 Changelog

### Version 1.0.0
- Erste Veröffentlichung
- Vollständige Integration mit Config Flow
- Dashboardkarte mit visueller Bearbeitung
- Deutsche Lokalisierung
- HACS-Kompatibilität

## 🤝 Beitragen

Beiträge sind willkommen! Bitte:

1. Forke das Repository
2. Erstelle einen Feature-Branch
3. Mache deine Änderungen
4. Erstelle einen Pull Request

## 📄 Lizenz

Dieses Projekt steht unter der MIT-Lizenz. Siehe LICENSE-Datei für Details.

## 🙏 Danksagungen

- Home Assistant Community für die großartige Plattform
- HACS-Team für die einfache Integration
- Alle Mitwirkenden und Tester

## 📞 Support

Bei Fragen oder Problemen:

1. Überprüfe die [Issues](https://github.com/yourusername/planthub/issues)
2. Erstelle ein neues Issue mit detaillierten Informationen
3. Stelle sicher, dass du die neueste Version verwendest

---

**Viel Spaß mit deiner PlantHub-Integration! 🌱**
