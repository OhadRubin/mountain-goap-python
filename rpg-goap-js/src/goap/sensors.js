export class Sensor {
  static _onSensorRun = [];

  static onSensorRun(agent, sensor) {
    Sensor._onSensorRun.forEach((h) => h(agent, sensor));
  }

  static registerOnSensorRun(h) {
    Sensor._onSensorRun.push(h);
  }

  constructor(runCallback, name = null) {
    this.name = name ?? `Sensor`;
    this._runCallback = runCallback;
  }

  run(agent) {
    Sensor.onSensorRun(agent, this);
    if (this._runCallback) {
      this._runCallback(agent);
    }
  }
}
