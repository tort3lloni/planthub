# PlantHub - Home Assistant Integration

Disclaimer: Komplett KI erstellt, ich spiele hier nur etwas rum.

Eine moderne und benutzerfreundliche Home Assistant Integration für die Überwachung von Pflanzen mit Webhook-API-Integration.

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)
[![maintainer](https://img.shields.io/badge/maintainer-%40yourusername-blue.svg)](https://github.com/yourusername)
[![homeassistant](https://img.shields.io/badge/home--assistant-2025.1.0+-blue.svg)](https://home-assistant.io/)
[![python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/)
[![version](https://img.shields.io/badge/version-1.1.5-green.svg)](https://github.com/yourusername/planthub/releases)

## 🚀 Features

- **Moderne Architektur**: Vollständig kompatibel mit den neuesten Home Assistant Standards (2025)
- **Webhook-Integration**: Automatische Datenabfrage über PlantHub API
- **HACS-Integration**: Einfache Installation über HACS (Home Assistant Community Store)
- **Device Registry**: Jede Pflanze wird als separates Gerät angelegt
- **Vollständige Sensor-Überwachung**: Alle wichtigen Pflanzen-Metriken
- **Intelligente Fehlerbehandlung**: Robuste Fallback-Mechanismen bei API-Fehlern
- **Deutsche und englische Lokalisierung**: Vollständig übersetzt
- **Config Flow**: Benutzerfreundliche Konfiguration über die Home Assistant UI

## 📋 Voraussetzungen

### System-Anforderungen
- **Home Assistant**: 2025.1.0 oder höher
- **Python**: 3.11 oder höher
- **HACS**: Installiert und konfiguriert

### HACS Installation
Falls HACS noch nicht installiert ist, folge der [offiziellen HACS-Installationsanleitung](https://hacs.xyz/docs/installation/installation/).

### API-Anforderungen
- PlantHub API Token
- Internetverbindung für API-Aufrufe

## 🔧 Installation

### Über HACS (Empfohlen)

1. **HACS öffnen**
   - Gehe zu deinem Home Assistant Dashboard
   - Öffne HACS über das Seitenmenü

2. **Integration hinzufügen**
   - Klicke auf "Integrations" in HACS
   - Klicke auf das "+" Symbol oben rechts
   - Suche nach "PlantHub"
   - Klicke auf "Download"

3. **Home Assistant neu starten**
   - Nach dem Download erscheint eine Meldung
   - Klicke auf "Restart" um Home Assistant neu zu starten

4. **Integration konfigurieren**
   - Gehe zu "Einstellungen" → "Geräte & Dienste"
   - Klicke auf "+ Integration hinzufügen"
   - Suche nach "PlantHub"
   - Folge der Konfiguration

### Manuelle Installation

1. **Repository klonen**
   ```bash
   cd config/custom_components
   git clone https://github.com/yourusername/planthub.git
   ```

2. **Home Assistant neu starten**

3. **Integration konfigurieren**
   - Gehe zu "Einstellungen" → "Geräte & Dienste"
   - Klicke auf "+ Integration hinzufügen"
   - Suche nach "PlantHub"

## ⚙️ Konfiguration

### Voraussetzung: API Token in configuration.yaml

**Wichtig**: Der API Token muss zuerst in der `configuration.yaml` konfiguriert werden, bevor die Integration über die UI hinzugefügt werden kann.

Füge folgende Zeilen zu deiner `configuration.yaml` hinzu:

```yaml
# PlantHub Integration Konfiguration
planthub:
  token: "dein_api_token_hier_einfuegen"
```

**Beispiel:**
```yaml
# Vollständige configuration.yaml
homeassistant:
  name: Home
  latitude: 52.520008
  longitude: 13.404954
  elevation: 0
  unit_system: metric
  time_zone: Europe/Berlin

# PlantHub Integration
planthub:
  token: "abc123def456ghi789jkl012mno345pqr678stu901vwx234yz"

# Weitere Integrationen...
```

### Integration einrichten

1. **Schritt 1: Integration hinzufügen**
   - Gehe zu "Einstellungen" → "Geräte & Dienste"
   - Klicke auf "+ Integration hinzufügen"
   - Suche nach "PlantHub"
   - **Keine Namenseingabe nötig** - der Name wird automatisch gesetzt
   - Klicke auf "Absenden"

2. **Schritt 2: Erste Pflanze hinzufügen**
   - Pflanzen-ID eingeben (z.B. "monstera_001")
   - Optional: Pflanzenname eingeben (z.B. "Monstera Deliciosa")
   - Klicke auf "Absenden"
   - **Integration wird automatisch als "PlantHub | Pflanzenname" benannt**

### Weitere Pflanzen hinzufügen

1. Gehe zu "Einstellungen" → "Geräte & Dienste"
2. Klicke auf die PlantHub Integration
3. Klicke auf "Konfigurieren"
4. Folge dem Options Flow für neue Pflanzen

### Geräte und Entitäten umbenennen

Alle PlantHub Geräte und Entitäten können über die Standard-Home-Assistant-UI umbenannt werden:

#### **Geräte umbenennen:**
1. Gehe zu "Einstellungen" → "Geräte & Dienste"
2. Klicke auf "Geräte"
3. Suche nach deinem PlantHub Gerät
4. Klicke auf das Gerät
5. Klicke auf "Einstellungen" (Zahnrad-Symbol)
6. Ändere den "Gerätenamen" und klicke auf "Speichern"

#### **Entitäten umbenennen:**
1. Gehe zu "Einstellungen" → "Geräte & Dienste"
2. Klicke auf "Entitäten"
3. Suche nach der PlantHub Entität (z.B. "sensor.monstera_001_soil_moisture")
4. Klicke auf die Entität
5. Klicke auf "Einstellungen" (Zahnrad-Symbol)
6. Ändere den "Entitätsnamen" und klicke auf "Speichern"

**Hinweis**: Nach dem Umbenennen werden die neuen Namen sofort in der gesamten Home Assistant UI angezeigt, einschließlich Dashboards und Automatisierungen.

### 🎯 **Vollständige Home Assistant UI Integration**

Die PlantHub-Integration ist **vollständig in die Home Assistant UI integriert**:

#### **✅ Automatische Namensgebung:**
- **Integration-Name**: Wird automatisch als "PlantHub | Pflanzenname" gesetzt
- **Keine manuelle Eingabe**: Der Benutzer wird nicht nach dem Namen gefragt
- **Konsistente Benennung**: Alle Integrationen folgen dem gleichen Namensschema

#### **✅ Direkte Pflanzenverwaltung:**
- **Erste Pflanze**: Wird direkt beim Integration-Setup hinzugefügt
- **Keine Zwischenschritte**: Direkter Weg von Integration zu Pflanze
- **Benutzerfreundlich**: Minimaler Konfigurationsaufwand

#### **✅ Standard-Home-Assistant-UI:**
- **Geräte umbenennen**: Über "Einstellungen" → "Geräte & Dienste" → "Geräte"
- **Entitäten umbenennen**: Über "Einstellungen" → "Geräte & Dienste" → "Entitäten"
- **Keine speziellen Menüs**: Alles über die Standard-Home-Assistant-UI
- **Vertraute Workflows**: Benutzer kennen die Standard-Funktionen

### Automatische Synchronisation

Die PlantHub-Integration synchronisiert sich automatisch mit der Home Assistant UI:

#### **Geräte entfernen:**
- **Über UI**: Gehe zu "Einstellungen" → "Geräte & Dienste" → "Geräte" → Wähle PlantHub-Gerät → "Entfernen"
- **Automatisch**: Die Pflanze wird automatisch aus der PlantHub-Konfiguration entfernt
- **Synchronisation**: Alle zugehörigen Entitäten werden ebenfalls entfernt

#### **Entitäten entfernen:**
- **Über UI**: Gehe zu "Einstellungen" → "Geräte & Dienste" → "Entitäten" → Wähle PlantHub-Entität → "Entfernen"
- **Automatisch**: Die entsprechende Pflanze wird aus der Konfiguration entfernt
- **Synchronisation**: Das zugehörige Gerät wird ebenfalls entfernt

#### **Vorteile der automatischen Synchronisation:**
- ✅ **Keine Inkonsistenzen**: UI und Konfiguration bleiben immer synchron
- ✅ **Einfache Verwaltung**: Entfernen über die Standard-Home-Assistant-UI
- ✅ **Automatische Updates**: Coordinator wird automatisch aktualisiert
- ✅ **Saubere Bereinigung**: Alle zugehörigen Daten werden entfernt

## 🌐 Webhook-API-Integration

### API-Endpunkte

Die Integration ruft automatisch folgende Endpunkte auf:

- **Basis-URL**: `https://api.planthub.com/v1`
- **Einzelne Pflanze**: `/plants/{plant_id}`
- **Alle Pflanzen**: `/plants`

### Authentifizierung

- **Token-basiert**: Bearer Token aus der Konfiguration
- **Headers**: Automatisch gesetzt mit User-Agent
- **Timeout**: 30 Sekunden pro Anfrage

### Datenabfrage

- **Intervall**: Standardmäßig alle 5 Minuten (konfigurierbar)
- **Automatisch**: Läuft im Hintergrund ohne Benutzerinteraktion
- **Fehlerbehandlung**: Robuste Fallback-Mechanismen bei API-Fehlern

## 📊 Verfügbare Sensoren

Nach der Integration werden folgende Sensoren erstellt:

- `sensor.planthub_status`: Gesamtstatus der Pflanze (healthy/warning/critical/unknown)
- `sensor.planthub_soil_moisture`: Bodenfeuchtigkeit in Prozent
- `sensor.planthub_air_temperature`: Lufttemperatur in °C
- `sensor.planthub_air_humidity`: Luftfeuchtigkeit in Prozent
- `sensor.planthub_light`: Helligkeit in Lux
- `sensor.planthub_plant_id`: Versteckte Entität für interne Zwecke

## 🔍 Statusbewertung

Die Integration bewertet automatisch den Zustand deiner Pflanze:

- **Healthy** (grün): Bodenfeuchtigkeit ≥ 50%
- **Warning** (orange): Bodenfeuchtigkeit 30-49%
- **Critical** (rot): Bodenfeuchtigkeit < 30%
- **Unknown**: Keine Daten verfügbar

## 🛡️ Fehlerbehandlung

### API-Fehler

Die Integration behandelt verschiedene API-Fehler intelligent:

- **401 Unauthorized**: Token ungültig oder abgelaufen
- **403 Forbidden**: Unzureichende Berechtigungen
- **404 Not Found**: Pflanze nicht gefunden
- **429 Too Many Requests**: Rate Limit überschritten
- **5xx Server Errors**: Server-seitige Probleme

### Fallback-Mechanismen

Bei API-Fehlern:
- Sensoren zeigen `unavailable` an
- Fallback-Daten werden geloggt
- Integration bleibt funktionsfähig
- Automatische Wiederherstellung bei nächstem Update

### Logging

Alle API-Aufrufe und Fehler werden sauber geloggt:
- **Debug**: Erfolgreiche API-Aufrufe
- **Warning**: Rate Limits, Verbindungsprobleme
- **Error**: Authentifizierungsfehler, Server-Fehler

## 🎯 Verwendungsbeispiele

### Einfache Überwachung

```yaml
# Automatisch erstellt nach der Integration
sensor.planthub_status: "healthy"
sensor.planthub_soil_moisture: 65
sensor.planthub_air_temperature: 22.5
```

### Automatisierung bei kritischem Zustand

```yaml
automation:
  - alias: "Pflanze gießen bei kritischer Feuchtigkeit"
    trigger:
      platform: state
      entity_id: sensor.planthub_status
      to: "critical"
    action:
      - service: notify.mobile_app
        data:
          title: "Pflanze braucht Wasser!"
          message: "Die Bodenfeuchtigkeit ist kritisch niedrig."
```

### Dashboard-Integration

```yaml
# Lovelace Dashboard
views:
  - title: "Pflanzen-Überwachung"
    cards:
      - type: entities
        title: "Pflanzen-Status"
        entities:
          - entity: sensor.planthub_status
          - entity: sensor.planthub_soil_moisture
          - entity: sensor.planthub_air_temperature
          - entity: sensor.planthub_air_humidity
          - entity: sensor.planthub_light
```

## 🛠️ Entwicklung

### Projektstruktur

```
custom_components/planthub/
├── __init__.py          # Hauptintegration mit Device Registry
├── manifest.json        # Metadaten für Home Assistant 2025
├── config_flow.py       # Config Flow mit Token + Geräte-Management
├── const.py            # Konstanten und Webhook-Konfiguration
├── sensor.py           # Alle Sensoren mit Webhook-Integration
├── webhook.py          # Webhook-Funktionalität und API-Handler
├── translations/       # Deutsche und englische Lokalisierung
│   ├── de.json
│   └── en.json
├── repository.json     # HACS-Konfiguration
├── requirements.txt   # Abhängigkeiten (aiohttp)
└── test_webhook.py    # Unit-Tests
```

### Webhook-Architektur

- **PlantHubWebhook**: Hauptklasse für API-Aufrufe
- **Async Context Manager**: Automatische Session-Verwaltung
- **Fehlerbehandlung**: Spezifische Exceptions für verschiedene Fehlertypen
- **Datenvalidierung**: Plausibilitätsprüfung der API-Antworten

### Anpassungen

Die Integration kann einfach angepasst werden:

1. **API-Endpunkte ändern**: Bearbeite `const.py`
2. **Fehlerbehandlung erweitern**: Bearbeite `webhook.py`
3. **Neue Sensoren hinzufügen**: Bearbeite `sensor.py`
4. **Übersetzungen hinzufügen**: Bearbeite `translations/`

## 🧪 Tests

### Test-Suite ausführen

```bash
# Im custom_components/planthub Verzeichnis
pytest test_webhook.py -v

# Mit Coverage
pytest test_webhook.py --cov=. --cov-report=html
```

### Test-Abhängigkeiten

```bash
pip install pytest pytest-asyncio pytest-cov
```

## 🐛 Fehlerbehebung

### Häufige Probleme

**API-Token ungültig:**
- Überprüfe den Token in der Integration
- Stelle sicher, dass der Token mindestens 10 Zeichen hat
- Überprüfe die Token-Gültigkeit bei PlantHub

**Verbindungsfehler:**
- Überprüfe die Internetverbindung
- Stelle sicher, dass die API-URL erreichbar ist
- Überprüfe Firewall-Einstellungen

**Rate Limit überschritten:**
- Reduziere das Update-Intervall
- Kontaktiere PlantHub für höhere Limits

**Sensoren zeigen keine Werte:**
- Überprüfe die Home Assistant Logs
- Stelle sicher, dass die Integration läuft
- Überprüfe die API-Antworten im Debug-Log

**HACS-Installation schlägt fehl:**
- Stelle sicher, dass HACS korrekt installiert ist
- Überprüfe die Home Assistant Version (mindestens 2025.1.0)
- Starte Home Assistant nach der Installation neu

### Debug-Logging aktivieren

```yaml
# configuration.yaml
logger:
  custom_components.planthub: debug
```

## 📝 Changelog

### Version 1.0.0
- Erste Veröffentlichung
- Vollständige Integration mit Config Flow
- Webhook-API-Integration
- Device Registry Support
- Robuste Fehlerbehandlung
- Deutsche und englische Lokalisierung
- HACS-Kompatibilität
- Vollständige Test-Suite
- Moderne Home Assistant 2025 Standards

## 🤝 Beitragen

Beiträge sind willkommen! Bitte:

1. Forke das Repository
2. Erstelle einen Feature-Branch
3. Mache deine Änderungen
4. Erstelle einen Pull Request

### Entwicklungsrichtlinien

- Folge den Home Assistant Developer Guidelines
- Verwende Type Hints für alle Funktionen
- Schreibe Tests für neue Funktionalitäten
- Halte den Code sauber und gut dokumentiert

## 📄 Lizenz

Dieses Projekt steht unter der MIT-Lizenz. Siehe [LICENSE](LICENSE) Datei für Details.

## 🙏 Danksagungen

- Home Assistant Community für die großartige Plattform
- HACS-Team für die einfache Integration
- PlantHub für die API
- Alle Mitwirkenden und Tester

## 📞 Support

Bei Fragen oder Problemen:

1. Überprüfe die [Issues](https://github.com/yourusername/planthub/issues)
2. Erstelle ein neues Issue mit detaillierten Informationen
3. Stelle sicher, dass du die neueste Version verwendest
4. Überprüfe die Home Assistant Logs für Fehlerdetails

### Community-Support

- **GitHub Issues**: [PlantHub Issues](https://github.com/yourusername/planthub/issues)
- **Home Assistant Forum**: [Community Forum](https://community.home-assistant.io/)
- **Discord**: [Home Assistant Discord](https://discord.gg/c5DvZ4e)

---

## ⭐ Bewertung

Falls dir diese Integration gefällt, gib ihr gerne einen Stern auf GitHub! 🌟

**Viel Spaß mit deiner PlantHub Integration! 🌱**

---

*Diese Integration ist nicht offiziell von Home Assistant und wird von der Community entwickelt und gewartet.*
