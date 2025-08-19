# HACS Installation für PlantHub

## 🚀 Schnellstart über HACS

### Voraussetzungen
- Home Assistant 2025.1.0 oder höher
- HACS installiert und konfiguriert
- Internetverbindung

### Installation in 3 Schritten

#### 1. HACS öffnen
- Gehe zu deinem Home Assistant Dashboard
- Öffne HACS über das Seitenmenü (HACS-Symbol)
- Stelle sicher, dass HACS korrekt funktioniert

#### 2. PlantHub hinzufügen
- Klicke auf "Integrations" in HACS
- Klicke auf das "+" Symbol oben rechts
- Suche nach "PlantHub"
- Klicke auf "Download"

#### 3. Integration konfigurieren
- Nach dem Download erscheint eine Meldung
- Klicke auf "Restart" um Home Assistant neu zu starten
- Gehe zu "Einstellungen" → "Geräte & Dienste"
- Klicke auf "+ Integration hinzufügen"
- Suche nach "PlantHub" und folge der Konfiguration

## 🔧 Detaillierte Installation

### HACS installieren (falls noch nicht vorhanden)

#### Option 1: HACS über Samba/SSH
```bash
# SSH in deinen Home Assistant Server
ssh root@your-home-assistant-ip

# Wechsle ins config Verzeichnis
cd /config

# Erstelle custom_components Verzeichnis (falls nicht vorhanden)
mkdir -p custom_components

# Wechsle ins custom_components Verzeichnis
cd custom_components

# Klone HACS Repository
git clone https://github.com/hacs/integration.git hacs

# Setze Berechtigungen
chmod -R 755 hacs

# Starte Home Assistant neu
```

#### Option 2: HACS über Samba
1. Öffne Samba auf deinem Home Assistant Server
2. Navigiere zu `/config/custom_components/`
3. Erstelle einen Ordner namens `hacs`
4. Lade den HACS-Code in diesen Ordner
5. Starte Home Assistant neu

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

3. **HACS Repository hinzufügen**
   - Öffne HACS
   - Gehe zu "Settings" → "Repositories"
   - Klicke auf das "+" Symbol
   - Füge `yourusername/planthub` hinzu
   - Klicke auf "Add"

## 📋 Repository-Konfiguration

### HACS repository.json

```json
{
  "name": "PlantHub",
  "render_readme": true,
  "domains": ["sensor"],
  "homeassistant": "2025.1.0",
  "iot_class": "Local Polling",
  "zip_release": false,
  "filename": "custom_components/planthub.zip",
  "version": "1.0.0",
  "url": "https://github.com/yourusername/planthub",
  "maintainer": "Your Name <your.email@example.com>",
  "country": ["DE", "EN"],
  "tags": [
    "plant",
    "monitoring",
    "sensor",
    "garden",
    "automation",
    "climate",
    "humidity",
    "temperature",
    "light"
  ],
  "requirements": [
    "aiohttp>=3.8.0"
  ],
  "dependencies": [],
  "codeowners": [
    "@yourusername"
  ],
  "config_flow": true,
  "documentation": "https://github.com/yourusername/planthub",
  "issue_tracker": "https://github.com/yourusername/planthub/issues"
}
```

### Wichtige Felder

- **`name`**: Name der Integration in HACS
- **`domains`**: Verwendete Home Assistant Domains
- **`homeassistant`**: Minimale Home Assistant Version
- **`iot_class`**: IoT-Klasse der Integration
- **`requirements`**: Python-Abhängigkeiten
- **`config_flow`**: Ob die Integration einen Config Flow hat

## 🐛 Häufige HACS-Probleme

### Installation schlägt fehl

**Problem**: "Could not install PlantHub"
- **Lösung**: Überprüfe die Home Assistant Version (mindestens 2025.1.0)
- **Lösung**: Stelle sicher, dass HACS korrekt installiert ist
- **Lösung**: Überprüfe die Internetverbindung

**Problem**: "Repository not found"
- **Lösung**: Überprüfe den Repository-Namen in HACS
- **Lösung**: Stelle sicher, dass das Repository öffentlich ist
- **Lösung**: Überprüfe die GitHub-Berechtigungen

**Problem**: "Requirements not met"
- **Lösung**: Überprüfe die Python-Version (mindestens 3.11)
- **Lösung**: Stelle sicher, dass alle Abhängigkeiten installiert sind
- **Lösung**: Starte Home Assistant neu

### Integration funktioniert nicht

**Problem**: Integration erscheint nicht in der Liste
- **Lösung**: Starte Home Assistant nach der Installation neu
- **Lösung**: Überprüfe die Logs auf Fehler
- **Lösung**: Stelle sicher, dass alle Dateien korrekt installiert sind

**Problem**: Config Flow funktioniert nicht
- **Lösung**: Überprüfe die `config_flow.py` Datei
- **Lösung**: Stelle sicher, dass alle Imports korrekt sind
- **Lösung**: Überprüfe die Logs auf Python-Fehler

## 🔄 Updates

### Automatische Updates

HACS prüft automatisch auf Updates:
- Gehe zu HACS → "Updates"
- Klicke auf "Update" bei PlantHub
- Starte Home Assistant neu

### Manuelle Updates

```bash
# SSH in deinen Server
ssh root@your-home-assistant-ip

# Wechsle ins Repository
cd /config/custom_components/planthub

# Hole Updates
git pull origin main

# Starte Home Assistant neu
```

## 📊 HACS-Status

### Quality Scale

PlantHub hat den Status **"Platinum"**:
- ✅ Vollständige Dokumentation
- ✅ Vollständige Test-Suite
- ✅ Type Hints
- ✅ Config Flow
- ✅ Device Registry Integration
- ✅ Moderne Home Assistant Standards

### IoT Class

**"Local Polling"** bedeutet:
- Integration läuft lokal auf deinem Home Assistant Server
- Daten werden in regelmäßigen Abständen abgefragt
- Keine Cloud-Abhängigkeiten
- Datenschutzfreundlich

## 🌟 Best Practices

### Für Benutzer

1. **Immer über HACS installieren**
   - Einfacher als manuelle Installation
   - Automatische Updates
   - Bessere Fehlerbehandlung

2. **Nach Installation neu starten**
   - Stellt sicher, dass alle Komponenten geladen werden
   - Vermeidet Konfigurationsprobleme

3. **Logs überwachen**
   - Aktiviert Debug-Logging für die Integration
   - Überwacht Fehler und Warnungen

### Für Entwickler

1. **Repository-Struktur einhalten**
   - Alle Dateien im richtigen Verzeichnis
   - Korrekte Dateinamen und -endungen

2. **HACS-Metadaten aktuell halten**
   - Version regelmäßig aktualisieren
   - Requirements aktuell halten
   - Dokumentation aktuell halten

3. **Tests schreiben**
   - Unit-Tests für alle Funktionen
   - Integration-Tests für End-to-End-Szenarien
   - Test-Coverage überwachen

## 📞 Support

### HACS-spezifische Hilfe

- **HACS Dokumentation**: [hacs.xyz](https://hacs.xyz/)
- **HACS Discord**: [Discord Server](https://discord.gg/c5DvZ4e)
- **HACS GitHub**: [GitHub Repository](https://github.com/hacs/integration)

### PlantHub Support

- **GitHub Issues**: [PlantHub Issues](https://github.com/yourusername/planthub/issues)
- **Home Assistant Forum**: [Community Forum](https://community.home-assistant.io/)
- **Discord**: [Home Assistant Discord](https://discord.gg/c5DvZ4e)

---

**Viel Erfolg bei der HACS-Installation! 🚀**
