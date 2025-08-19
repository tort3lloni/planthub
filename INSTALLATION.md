# PlantHub - Installationsanleitung

## 🚀 Schnellstart

### Über HACS (Empfohlen)

1. **HACS öffnen**
   - Gehe zu deinem Home Assistant Dashboard
   - Öffne HACS über das Seitenmenü (HACS-Symbol)

2. **PlantHub hinzufügen**
   - Klicke auf "Integrations" in HACS
   - Klicke auf das "+" Symbol oben rechts
   - Suche nach "PlantHub"
   - Klicke auf "Download"

3. **Home Assistant neu starten**
   - Nach dem Download erscheint eine Meldung
   - Klicke auf "Restart"

4. **Integration konfigurieren**
   - Gehe zu "Einstellungen" → "Geräte & Dienste"
   - Klicke auf "+ Integration hinzufügen"
   - Suche nach "PlantHub"
   - Folge der Konfiguration

## 📋 Voraussetzungen

### System-Anforderungen
- **Home Assistant**: 2025.1.0 oder höher
- **Python**: 3.11 oder höher
- **HACS**: Installiert und konfiguriert

### HACS installieren

Falls HACS noch nicht installiert ist:

1. **Über SSH/Samba**
   ```bash
   # SSH in deinen Server
   ssh root@your-home-assistant-ip
   
   # Wechsle ins config Verzeichnis
   cd /config
   
   # Erstelle custom_components Verzeichnis
   mkdir -p custom_components
   
   # Wechsle ins custom_components Verzeichnis
   cd custom_components
   
   # Klone HACS Repository
   git clone https://github.com/hacs/integration.git hacs
   
   # Setze Berechtigungen
   chmod -R 755 hacs
   
   # Starte Home Assistant neu
   ```

2. **Über Samba**
   - Öffne Samba auf deinem Home Assistant Server
   - Navigiere zu `/config/custom_components/`
   - Erstelle einen Ordner namens `hacs`
   - Lade den HACS-Code in diesen Ordner
   - Starte Home Assistant neu

### HACS konfigurieren

1. **GitHub Token erstellen**
   - Gehe zu [GitHub Settings](https://github.com/settings/tokens)
   - Klicke auf "Generate new token (classic)"
   - Wähle "repo" und "read:packages" aus
   - Kopiere den Token

2. **HACS in Home Assistant einrichten**
   - Gehe zu "Einstellungen" → "Geräte & Dienste"
   - Klicke auf "+ Integration hinzufügen"
   - Suche nach "HACS"
   - Gib deinen GitHub Token ein
   - Folge der Konfiguration

## ⚙️ Konfiguration

### Integration einrichten

1. **Schritt 1: API Token**
   - Gib deinen PlantHub API Token ein
   - Der Token muss mindestens 10 Zeichen lang sein
   - Optional: Gib einen Namen für die Integration ein

2. **Schritt 2: Pflanze hinzufügen**
   - Pflanzen-ID eingeben (z.B. "monstera_001")
   - Optional: Pflanzenname eingeben (z.B. "Monstera Deliciosa")
   - Klicke auf "Absenden"

### Weitere Pflanzen hinzufügen

1. Gehe zu "Einstellungen" → "Geräte & Dienste"
2. Klicke auf die PlantHub Integration
3. Klicke auf "Konfigurieren"
4. Folge dem Config Flow für neue Pflanzen

## 🔧 Manuelle Installation

### Über Git

```bash
# SSH in deinen Server
ssh root@your-home-assistant-ip

# Wechsle ins config Verzeichnis
cd /config

# Erstelle custom_components Verzeichnis (falls nicht vorhanden)
mkdir -p custom_components

# Wechsle ins custom_components Verzeichnis
cd custom_components

# Klone PlantHub Repository
git clone https://github.com/yourusername/planthub.git

# Setze Berechtigungen
chmod -R 755 planthub

# Starte Home Assistant neu
```

### Über Samba

1. Öffne Samba auf deinem Home Assistant Server
2. Navigiere zu `/config/custom_components/`
3. Erstelle einen Ordner namens `planthub`
4. Lade alle Dateien aus dem Repository in diesen Ordner
5. Starte Home Assistant neu

## 📊 Verfügbare Sensoren

Nach der Integration werden folgende Sensoren erstellt:

- `sensor.planthub_status`: Gesamtstatus der Pflanze
- `sensor.planthub_soil_moisture`: Bodenfeuchtigkeit in Prozent
- `sensor.planthub_air_temperature`: Lufttemperatur in °C
- `sensor.planthub_air_humidity`: Luftfeuchtigkeit in Prozent
- `sensor.planthub_light`: Helligkeit in Lux

## 🎯 Verwendungsbeispiele

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

### Automatisierung

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

## 🐛 Fehlerbehebung

### Häufige Probleme

**HACS-Installation schlägt fehl:**
- Überprüfe die Home Assistant Version (mindestens 2025.1.0)
- Stelle sicher, dass HACS korrekt installiert ist
- Starte Home Assistant nach der Installation neu

**Integration erscheint nicht:**
- Starte Home Assistant nach der Installation neu
- Überprüfe die Logs auf Fehler
- Stelle sicher, dass alle Dateien korrekt installiert sind

**API-Token ungültig:**
- Überprüfe den Token in der Integration
- Stelle sicher, dass der Token mindestens 10 Zeichen hat
- Überprüfe die Token-Gültigkeit bei PlantHub

### Debug-Logging aktivieren

```yaml
# configuration.yaml
logger:
  custom_components.planthub: debug
```

### Logs überprüfen

1. Gehe zu "Entwicklertools" → "Logs"
2. Suche nach "planthub"
3. Überprüfe auf Fehler und Warnungen

## 🔄 Updates

### Über HACS

HACS prüft automatisch auf Updates:
1. Gehe zu HACS → "Updates"
2. Klicke auf "Update" bei PlantHub
3. Starte Home Assistant neu

### Manuell

```bash
# SSH in deinen Server
ssh root@your-home-assistant-ip

# Wechsle ins Repository
cd /config/custom_components/planthub

# Hole Updates
git pull origin main

# Starte Home Assistant neu
```

## 📞 Support

### Hilfe bekommen

- **GitHub Issues**: [PlantHub Issues](https://github.com/yourusername/planthub/issues)
- **Home Assistant Forum**: [Community Forum](https://community.home-assistant.io/)
- **Discord**: [Home Assistant Discord](https://discord.gg/c5DvZ4e)

### Fehler melden

Bei Problemen bitte folgende Informationen bereithalten:
- Home Assistant Version
- PlantHub Version
- Fehlermeldungen aus den Logs
- Schritte zum Reproduzieren des Problems

---

**Viel Spaß mit deiner PlantHub Integration! 🌱**
