from goap.sensors import Sensor


def dummy(agent):
    agent.ran = True


def test_sensor_run_event():
    sensor = Sensor(dummy, name="Dummy")
    class Agent: pass
    agent = Agent()
    Sensor.register_on_sensor_run(lambda a, s: setattr(a, 'ran', False))
    sensor.run(agent)
    assert hasattr(agent, 'ran')
