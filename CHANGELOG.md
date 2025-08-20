# PlantHub Integration - Changelog

## [1.1.5] - 2024-01-15

### 🐛 **Bugfix: Config Flow Fehler behoben**

#### **KeyError: 'name' behoben**
- **Problem**: Config Flow warf KeyError beim ersten Schritt
- **Ursache**: Referenz auf nicht existierenden `self._config_data["name"]`
- **Lösung**: Entfernung der ungültigen Referenz aus `description_placeholders`
- **Status**: ✅ Behoben

#### **Stabiler Config Flow**
- **Erster Schritt**: Funktioniert jetzt ohne Fehler
- **Automatische Namensgebung**: Läuft korrekt durch
- **Direkte Pflanzenverwaltung**: Funktioniert einwandfrei

### 🔧 **Technische Verbesserungen**

#### **Config Flow Optimierung**
- **description_placeholders**: Leere Dictionary für ersten Schritt
- **Fehlerbehandlung**: Robuste Behandlung aller Schritte
- **Stabilität**: Config Flow läuft ohne Abstürze

---

## [1.1.4] - 2024-01-15

### ✨ **Vollständige Home Assistant UI Integration**

#### **Automatische Namensgebung**
- **Neue Funktion**: Integration-Name wird automatisch als "PlantHub | Pflanzenname" gesetzt
- **Keine manuelle Eingabe**: Benutzer wird nicht mehr nach dem Namen gefragt
- **Konsistente Benennung**: Alle Integrationen folgen dem gleichen Namensschema
- **Benutzerfreundlich**: Minimaler Konfigurationsaufwand

#### **Direkte Pflanzenverwaltung**
- **Erste Pflanze**: Wird direkt beim Integration-Setup hinzugefügt
- **Keine Zwischenschritte**: Direkter Weg von Integration zu Pflanze
- **Vereinfachter Workflow**: Weniger Konfigurationsschritte nötig

#### **Verbesserte UI-Integration**
- **Standard-Home-Assistant-UI**: Alle Funktionen über die Standard-UI
- **Geräte umbenennen**: Funktioniert korrekt über "Einstellungen" → "Geräte & Dienste" → "Geräte"
- **Entitäten umbenennen**: Funktioniert korrekt über "Einstellungen" → "Geräte & Dienste" → "Entitäten"
- **Keine speziellen Menüs**: Alles über vertraute Home Assistant Workflows

### 🔧 **Technische Verbesserungen**

#### **Config Flow Optimierung**
- **Vereinfachter erster Schritt**: Keine Namenseingabe mehr nötig
- **Automatische Titelgenerierung**: `f"PlantHub | {plant_name}"`
- **Direkte Pflanzenverwaltung**: Erste Pflanze wird sofort hinzugefügt
- **Verbesserte Übersetzungen**: Klarere Anweisungen und Fehlermeldungen

#### **Sensor-Architektur verbessert**
- **has_entity_name=True**: Korrekt gesetzt für UI-Umbenennung
- **Entity Registry Integration**: Namen werden korrekt aus der Entity Registry gelesen
- **Device Registry Support**: Gerätenamen können über die UI geändert werden
- **Standard-Home-Assistant-Patterns**: Folgt allen aktuellen Best Practices

### 📚 **Dokumentation**

#### **Neue Anleitungen**
- Automatische Namensgebung erklärt
- Direkte Pflanzenverwaltung dokumentiert
- Vollständige UI-Integration beschrieben
- Standard-Home-Assistant-Workflows erklärt

#### **Aktualisierte Übersetzungen**
- Deutsche Übersetzungen verbessert
- Englische Übersetzungen aktualisiert
- Klarere Fehlermeldungen
- Benutzerfreundlichere Beschreibungen

### 🎯 **Benutzerfreundlichkeit**

#### **Vereinfachte Konfiguration**
- **Weniger Schritte**: Integration-Setup in nur 2 Schritten
- **Keine manuellen Eingaben**: Automatische Namensgebung
- **Direkte Pflanzenverwaltung**: Erste Pflanze sofort hinzufügen
- **Standard-UI**: Alle Funktionen über vertraute Home Assistant Workflows

#### **Verbesserte Benutzerführung**
- **Klare Anweisungen**: Bessere Beschreibungen in allen Schritten
- **Automatische Prozesse**: Weniger manuelle Konfiguration nötig
- **Konsistente Benennung**: Alle Integrationen folgen dem gleichen Schema
- **Intuitive Workflows**: Standard-Home-Assistant-Patterns

---

## [1.1.3] - 2024-01-15

### ✨ **Automatische Synchronisation mit Home Assistant UI**

#### **Geräte und Entitäten automatisch entfernen**
- **Neue Funktion**: Automatische Synchronisation zwischen Home Assistant UI und PlantHub-Konfiguration
- **Device Registry Listener**: Überwacht das Entfernen von Geräten über die UI
- **Entity Registry Listener**: Überwacht das Entfernen von Entitäten über die UI
- **Automatische Bereinigung**: Entfernte Pflanzen werden automatisch aus der Konfiguration gelöscht

#### **Intelligente Synchronisation**
- **Gerät entfernen**: Pflanze wird automatisch aus der PlantHub-Konfiguration entfernt
- **Entität entfernen**: Zugehörige Pflanze wird automatisch aus der Konfiguration entfernt
- **Coordinator-Update**: PlantHubDataUpdateCoordinator wird automatisch aktualisiert
- **Saubere Bereinigung**: Alle zugehörigen Daten werden konsistent entfernt

### 🔧 **Technische Verbesserungen**

#### **Registry Listener Integration**
- Neue `_register_device_registry_listener()` Funktion für Device Registry Überwachung
- Neue `_register_entity_registry_listener()` Funktion für Entity Registry Überwachung
- Automatische Registrierung und Entfernung der Listener beim Setup/Unload
- Robuste Fehlerbehandlung für alle Listener-Operationen

#### **Konfigurationssynchronisation**
- Neue `_remove_plant_from_config()` Funktion für automatische Pflanzenentfernung
- Neue `_update_plant_config_from_entity()` Funktion für Entitäts-basierte Updates
- Automatische Aktualisierung der `config_entry.data`
- Synchronisation mit dem `PlantHubDataUpdateCoordinator`

### 📚 **Dokumentation**

#### **Neue Anleitungen**
- Schritt-für-Schritt-Anleitung zum Entfernen von Geräten über die UI
- Detaillierte Anweisungen zum Entfernen von Entitäten über die UI
- Erklärung der automatischen Synchronisation
- Vorteile der neuen Funktionalität

### 🎯 **Benutzerfreundlichkeit**

#### **Vereinfachte Verwaltung**
- **Keine manuellen Schritte**: Entfernen über die Standard-Home-Assistant-UI
- **Automatische Synchronisation**: UI und Konfiguration bleiben immer konsistent
- **Intelligente Bereinigung**: Alle zugehörigen Daten werden automatisch entfernt
- **Keine Inkonsistenzen**: PlantHub-Integration bleibt immer synchron mit der UI

---

## [1.1.2] - 2024-01-15

### ✨ **Verbesserte Umbenennungsfunktionalität**

#### **Geräte und Entitäten über Home Assistant UI umbenennen**
- **Neue Funktion**: Alle PlantHub Geräte und Entitäten können über die Standard-Home-Assistant-UI umbenannt werden
- **Geräte umbenennen**: Über "Einstellungen" → "Geräte & Dienste" → "Geräte"
- **Entitäten umbenennen**: Über "Einstellungen" → "Geräte & Dienste" → "Entitäten"
- **Sofortige Aktualisierung**: Neue Namen werden sofort in der gesamten UI angezeigt

#### **Flexible Namensverwaltung**
- **Keine festen Namen**: Geräte- und Entitätsnamen sind nicht mehr fest codiert
- **Entity Registry Integration**: Namen werden dynamisch aus der Entity Registry gelesen
- **Device Registry Support**: Gerätenamen können über die Device Registry UI geändert werden
- **has_entity_name=True**: Alle Sensoren unterstützen die Standard-Home-Assistant-Umbenennung

### 🔧 **Technische Verbesserungen**

#### **Sensor-Architektur überarbeitet**
- Neue `name` Property in `BasePlantHubSensor` für dynamische Namensverwaltung
- Integration mit Home Assistant Entity Registry für Umbenennungen
- Fallback auf Standardnamen aus `SensorEntityDescription`
- Verbesserte Fehlerbehandlung bei Registry-Zugriffen

#### **Device Registry Optimierung**
- Geräte werden mit Standardnamen erstellt, können aber über UI geändert werden
- Keine festen Namen mehr, die die Umbenennung blockieren
- Vollständige Integration mit Home Assistant Device Registry UI

### 📚 **Dokumentation**

#### **Neue Anleitungen**
- Schritt-für-Schritt-Anleitung zum Umbenennen von Geräten
- Detaillierte Anweisungen zum Umbenennen von Entitäten
- Hinweise zur sofortigen Aktualisierung in der gesamten UI

---

## [1.1.1] - 2024-01-15

### 🔧 **Home Assistant 2025 Kompatibilität**

#### **Deprecation-Warnung behoben**
- **Behoben**: `self.config_entry` wird nicht mehr explizit in OptionsFlow gesetzt
- **Kompatibilität**: Vollständig kompatibel mit Home Assistant 2025.12+
- **Zukunftssicher**: Keine veralteten Patterns mehr im Code

### 📚 **Technische Verbesserungen**

#### **OptionsFlow-Refactoring**
- Entfernung des veralteten `__init__`-Konstruktors
- Verwendung der modernen Home Assistant 2025 OptionsFlow-API
- Automatische `config_entry`-Bereitstellung über Basis-Klasse

---

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
