import { LitElement, html, css } from 'lit';
import { property, state } from 'lit/decorators.js';
import { HomeAssistant, LovelaceCardEditor } from 'custom-card-helpers';

import './editor';

export class PlantHubCard extends LitElement {
  @property({ attribute: false }) public hass!: HomeAssistant;
  @state() private _config!: PlantHubCardConfig;

  static get properties() {
    return {
      hass: {},
      _config: {},
    };
  }

  public setConfig(config: PlantHubCardConfig): void {
    this._config = config;
  }

  static getStubConfig(): PlantHubCardConfig {
    return {
      type: 'custom:planthub-card',
      entity: 'sensor.planthub_status',
      name: 'Meine Pflanze',
      show_moisture: true,
      show_temperature: true,
      show_light: true,
      show_fertilizer: true,
      theme: 'default',
      compact: false,
    };
  }

  static getConfigElement(): Promise<LovelaceCardEditor> {
    return import('./editor');
  }

  render() {
    if (!this._config || !this.hass) {
      return html``;
    }

    const entity = this.hass.states[this._config.entity];
    if (!entity) {
      return html`
        <hui-warning>
          Entity nicht gefunden: ${this._config.entity}
        </hui-warning>
      `;
    }

    const attributes = entity.attributes;
    const moisture = attributes.moisture || 0;
    const temperature = attributes.temperature || 0;
    const light = attributes.light || 0;
    const fertilizer = attributes.fertilizer || 0;

    return html`
      <ha-card
        .header=${this._config.name || entity.attributes.friendly_name}
        class="planthub-card ${this._config.theme} ${this._config.compact ? 'compact' : ''}"
      >
        <div class="card-content">
          <div class="plant-status">
            <div class="status-indicator ${entity.state}">
              <ha-icon .icon=${this._getStatusIcon(entity.state)}></ha-icon>
              <span class="status-text">${this._getStatusText(entity.state)}</span>
            </div>
          </div>

          <div class="plant-metrics">
            ${this._config.show_moisture ? html`
              <div class="metric moisture">
                <ha-icon icon="mdi:water-percent"></ha-icon>
                <div class="metric-content">
                  <span class="metric-value">${moisture}%</span>
                  <span class="metric-label">Feuchtigkeit</span>
                </div>
                <div class="metric-bar">
                  <div class="bar-fill" style="width: ${moisture}%"></div>
                </div>
              </div>
            ` : ''}

            ${this._config.show_temperature ? html`
              <div class="metric temperature">
                <ha-icon icon="mdi:thermometer"></ha-icon>
                <div class="metric-content">
                  <span class="metric-value">${temperature}°C</span>
                  <span class="metric-label">Temperatur</span>
                </div>
              </div>
            ` : ''}

            ${this._config.show_light ? html`
              <div class="metric light">
                <ha-icon icon="mdi:white-balance-sunny"></ha-icon>
                <div class="metric-content">
                  <span class="metric-value">${light} lux</span>
                  <span class="metric-label">Licht</span>
                </div>
              </div>
            ` : ''}

            ${this._config.show_fertilizer ? html`
              <div class="metric fertilizer">
                <ha-icon icon="mdi:leaf"></ha-icon>
                <div class="metric-content">
                  <span class="metric-value">${fertilizer}%</span>
                  <span class="metric-label">Dünger</span>
                </div>
                <div class="metric-bar">
                  <div class="bar-fill" style="width: ${fertilizer}%"></div>
                </div>
              </div>
            ` : ''}
          </div>
        </div>
      </ha-card>
    `;
  }

  private _getStatusIcon(status: string): string {
    switch (status) {
      case 'gesund':
        return 'mdi:check-circle';
      case 'warnung':
        return 'mdi:alert-circle';
      case 'kritisch':
        return 'mdi:close-circle';
      default:
        return 'mdi:help-circle';
    }
  }

  private _getStatusText(status: string): string {
    switch (status) {
      case 'gesund':
        return 'Gesund';
      case 'warnung':
        return 'Warnung';
      case 'kritisch':
        return 'Kritisch';
      default:
        return 'Unbekannt';
    }
  }

  static get styles() {
    return css`
      .planthub-card {
        --planthub-primary-color: #4caf50;
        --planthub-warning-color: #ff9800;
        --planthub-critical-color: #f44336;
        --planthub-text-color: var(--primary-text-color);
        --planthub-secondary-text-color: var(--secondary-text-color);
        --planthub-background-color: var(--card-background-color);
      }

      .planthub-card.dark {
        --planthub-primary-color: #66bb6a;
        --planthub-warning-color: #ffb74d;
        --planthub-critical-color: #ef5350;
      }

      .planthub-card.compact .card-content {
        padding: 8px;
      }

      .plant-status {
        text-align: center;
        margin-bottom: 16px;
        padding: 16px;
        background: var(--planthub-background-color);
        border-radius: 8px;
      }

      .status-indicator {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
        font-size: 18px;
        font-weight: 500;
      }

      .status-indicator.gesund {
        color: var(--planthub-primary-color);
      }

      .status-indicator.warnung {
        color: var(--planthub-warning-color);
      }

      .status-indicator.kritisch {
        color: var(--planthub-critical-color);
      }

      .plant-metrics {
        display: grid;
        gap: 12px;
      }

      .metric {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 12px;
        background: var(--planthub-background-color);
        border-radius: 8px;
        border: 1px solid var(--divider-color);
      }

      .metric ha-icon {
        color: var(--planthub-primary-color);
        width: 24px;
        height: 24px;
      }

      .metric-content {
        flex: 1;
        display: flex;
        flex-direction: column;
      }

      .metric-value {
        font-size: 16px;
        font-weight: 600;
        color: var(--planthub-text-color);
      }

      .metric-label {
        font-size: 12px;
        color: var(--planthub-secondary-text-color);
        text-transform: uppercase;
        letter-spacing: 0.5px;
      }

      .metric-bar {
        width: 60px;
        height: 8px;
        background: var(--divider-color);
        border-radius: 4px;
        overflow: hidden;
      }

      .bar-fill {
        height: 100%;
        background: var(--planthub-primary-color);
        transition: width 0.3s ease;
      }

      .compact .metric {
        padding: 8px;
      }

      .compact .metric-value {
        font-size: 14px;
      }

      .compact .metric-label {
        font-size: 10px;
      }

      .compact .metric-bar {
        width: 40px;
        height: 6px;
      }
    `;
  }
}

declare global {
  interface HTMLElementTagNameMap {
    'planthub-card': PlantHubCard;
  }
}

export interface PlantHubCardConfig {
  type: 'custom:planthub-card';
  entity: string;
  name?: string;
  show_moisture?: boolean;
  show_temperature?: boolean;
  show_light?: boolean;
  show_fertilizer?: boolean;
  theme?: 'default' | 'dark';
  compact?: boolean;
}

// Registriere die Karte global
customElements.define('planthub-card', PlantHubCard);

// Registriere die Karte bei Home Assistant
if (window.customCards) {
  window.customCards.push({
    type: 'custom:planthub-card',
    name: 'PlantHub Card',
    description: 'Eine Karte zur Überwachung von Pflanzen',
    preview: true,
    documentationURL: 'https://github.com/tort3lloni/planthub',
  });
}
