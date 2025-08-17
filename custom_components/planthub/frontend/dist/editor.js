import { LitElement, html, css } from 'lit';
import { property, state } from 'lit/decorators.js';
import { HomeAssistant, LovelaceCardEditor } from 'custom-card-helpers';
import { fireEvent } from 'custom-card-helpers/internal';

import { PlantHubCardConfig } from './planthub-card';

export class PlantHubCardEditor extends LitElement implements LovelaceCardEditor {
  @property({ attribute: false }) public hass!: HomeAssistant;
  @state() private _config!: PlantHubCardConfig;

  public setConfig(config: PlantHubCardConfig): void {
    this._config = config;
  }

  static get styles() {
    return css`
      .form-row {
        margin-bottom: 16px;
      }

      .form-row label {
        display: block;
        margin-bottom: 4px;
        font-weight: 500;
        color: var(--primary-text-color);
      }

      .form-row ha-textfield,
      .form-row ha-select {
        width: 100%;
      }

      .form-row ha-formfield {
        margin-top: 8px;
      }

      .checkbox-group {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 8px;
        margin-top: 8px;
      }

      .theme-selector {
        display: flex;
        gap: 8px;
        margin-top: 8px;
      }

      .theme-option {
        flex: 1;
        padding: 8px;
        border: 2px solid var(--divider-color);
        border-radius: 4px;
        text-align: center;
        cursor: pointer;
        transition: all 0.2s ease;
      }

      .theme-option:hover {
        border-color: var(--primary-color);
      }

      .theme-option.selected {
        border-color: var(--primary-color);
        background: var(--primary-color);
        color: white;
      }

      .compact-toggle {
        display: flex;
        align-items: center;
        gap: 8px;
        margin-top: 8px;
      }
    `;
  }

  render() {
    if (!this.hass) {
      return html``;
    }

    return html`
      <div class="card-config">
        <div class="form-row">
          <label for="entity">Entity:</label>
          <ha-entity-picker
            .hass=${this.hass}
            .value=${this._config?.entity}
            @value-changed=${this._valueChanged}
            .configValue=${'entity'}
            include-domains='["sensor"]'
            placeholder="Wähle eine Entity aus"
          ></ha-entity-picker>
        </div>

        <div class="form-row">
          <label for="name">Anzeigename (optional):</label>
          <ha-textfield
            .value=${this._config?.name || ''}
            .configValue=${'name'}
            @input=${this._valueChanged}
            placeholder="Überschreibt den Standard-Namen"
          ></ha-textfield>
        </div>

        <div class="form-row">
          <label>Angezeigte Metriken:</label>
          <div class="checkbox-group">
            <ha-formfield label="Feuchtigkeit">
              <ha-checkbox
                .checked=${this._config?.show_moisture !== false}
                .configValue=${'show_moisture'}
                @change=${this._valueChanged}
              ></ha-checkbox>
            </ha-formfield>
            
            <ha-formfield label="Temperatur">
              <ha-checkbox
                .checked=${this._config?.show_temperature !== false}
                .configValue=${'show_temperature'}
                @change=${this._valueChanged}
              ></ha-checkbox>
            </ha-formfield>
            
            <ha-formfield label="Licht">
              <ha-checkbox
                .checked=${this._config?.show_light !== false}
                .configValue=${'show_light'}
                @change=${this._valueChanged}
              ></ha-checkbox>
            </ha-formfield>
            
            <ha-formfield label="Dünger">
              <ha-checkbox
                .checked=${this._config?.show_fertilizer !== false}
                .configValue=${'show_fertilizer'}
                @change=${this._valueChanged}
              ></ha-checkbox>
            </ha-formfield>
          </div>
        </div>

        <div class="form-row">
          <label>Theme:</label>
          <div class="theme-selector">
            <div
              class="theme-option ${this._config?.theme === 'default' || !this._config?.theme ? 'selected' : ''}"
              @click=${() => this._themeChanged('default')}
            >
              Hell
            </div>
            <div
              class="theme-option ${this._config?.theme === 'dark' ? 'selected' : ''}"
              @click=${() => this._themeChanged('dark')}
            >
              Dunkel
            </div>
          </div>
        </div>

        <div class="form-row">
          <div class="compact-toggle">
            <ha-formfield label="Kompakte Ansicht">
              <ha-switch
                .checked=${this._config?.compact || false}
                .configValue=${'compact'}
                @change=${this._valueChanged}
              ></ha-switch>
            </ha-formfield>
          </div>
        </div>
      </div>
    `;
  }

  private _valueChanged(ev: CustomEvent): void {
    if (!this._config || !this.hass) {
      return;
    }

    const target = ev.target as any;
    if (target.configValue) {
      let value: any = target.value;
      
      if (target.type === 'checkbox') {
        value = target.checked;
      }

      if (this._config[target.configValue] === value) {
        return;
      }

      this._config = {
        ...this._config,
        [target.configValue]: value,
      };
    }

    fireEvent(this, 'config-changed', { config: this._config });
  }

  private _themeChanged(theme: 'default' | 'dark'): void {
    if (!this._config || !this.hass) {
      return;
    }

    this._config = {
      ...this._config,
      theme: theme,
    };

    fireEvent(this, 'config-changed', { config: this._config });
  }
}

customElements.define('planthub-card-editor', PlantHubCardEditor);
