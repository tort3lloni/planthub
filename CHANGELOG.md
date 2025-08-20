# PlantHub Integration - Changelog

## [1.1.0] - 2024-01-15

### 🔄 **Wichtige Änderungen**

#### **Token-Konfiguration überarbeitet**
- **Breaking Change**: Der API Token wird nicht mehr über die UI abgefragt
- **Neue Konfiguration**: Token muss in `configuration.yaml` unter `planthub: token:` konfiguriert werden
- **Verbesserte Sicherheit**: Token wird zentral in `hass.data[DOMAIN][CONF_TOKEN]` gespeichert

#### **ConfigFlow vereinfacht**
- **Entfernt**: Token-Abfrage und -Validierung aus dem ConfigFlow
- **Fokus**: Nur noch Pflanzenverwaltung über UI
- **Prüfung**: Token-Verfügbarkeit wird vor Integration-Setup validiert

### ✨ **Neue Features**

#### **Zentrale Token-Verwaltung**
- Token wird beim Home Assistant Start aus `configuration.yaml` geladen
- Automatische Validierung der Token-Konfiguration
- Bessere Fehlerbehandlung bei fehlendem Token

#### **Verbesserte Benutzerführung**
- Klare Anweisungen zur Token-Konfiguration
- Neue Fehlermeldung: "token_not_configured"
- Aktualisierte Übersetzungen (DE/EN)

### 🔧 **Technische Verbesserungen**

#### **Code-Refactoring**
- `PlantHubDataUpdateCoordinator` verwendet jetzt `hass.data[DOMAIN][CONF_TOKEN]`
- Entfernung aller `entry.data["token"]` Referenzen
- Saubere Trennung zwischen Konfiguration und Laufzeit-Daten

#### **Konfigurationsstruktur**
- Neue Konstante: `CONF_TOKEN = "token"`
- Vereinfachte `async_setup()` Funktion
- Token-Validierung in `async_setup_entry()`

### 📚 **Dokumentation**

#### **Neue Dateien**
- `configuration.yaml.example` - Beispiel-Konfiguration
- `CHANGELOG.md` - Diese Datei

#### **Aktualisierte Dateien**
- `README.md` - Neue Konfigurationsanleitung
- `translations/de.json` - Deutsche Übersetzungen aktualisiert
- `translations/en.json` - Englische Übersetzungen aktualisiert

### 🚨 **Breaking Changes**

1. **Token-Konfiguration**: Der API Token muss jetzt in `configuration.yaml` konfiguriert werden
2. **ConfigFlow**: Keine Token-Abfrage mehr in der UI
3. **Setup-Reihenfolge**: Token muss vor Integration-Setup konfiguriert sein

### 📋 **Migration von v1.0.0**

1. **Token in configuration.yaml hinzufügen:**
   ```yaml
   planthub:
     token: "dein_bestehender_api_token"
   ```

2. **Home Assistant neu starten**

3. **Integration über UI neu konfigurieren** (nur Name und erste Pflanze)

### 🔍 **Fehlerbehebung**

- **Fehler**: "PlantHub Token nicht verfügbar"
  - **Lösung**: Token in `configuration.yaml` unter `planthub: token:` konfigurieren

- **Fehler**: "Token nicht in configuration.yaml gefunden"
  - **Lösung**: Überprüfe die YAML-Syntax und stelle sicher, dass der Token korrekt konfiguriert ist

### 🎯 **Nächste Versionen**

- **v1.2.0**: Erweiterte Token-Validierung und API-Tests
- **v1.3.0**: Mehrere Token-Unterstützung für verschiedene PlantHub-Instanzen
- **v2.0.0**: Vollständige YAML-basierte Konfiguration

---

**Hinweis**: Diese Version ist vollständig kompatibel mit Home Assistant 2025.1.0+ und Python 3.11+.
