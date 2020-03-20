"""The tests for open weather map."""

#from asynctest import patch

from homeassistant.components.openweathermap.sensor import OpenWeatherMapSensor, WeatherData

from unittest.mock import patch
from pyowm import OWM

async def test_rain_not_available(hass):
    """Test rain condition not available."""
    with patch.object(OWM, '__init__', return_value=True):
        owm = OWM(None, None)
        wd = WeatherData(owm,None,None,None)
        sensor = OpenWeatherMapSensor("test", wd, "rain", None)

    with patch.object(OWM, 'weather_at_coords', return_value=True):
        # First it should have no data    
        with patch.object(OpenWeatherMapSensor.owa_client.data, 'get_rain', return_value={"test": None}):
            sensor.update()
            assert sensor._state == None

        # Second it should have a value
        with patch.object(OpenWeatherMapSensor.owa_client.data, 'get_rain', return_value={"3h": 5}):
            sensor.update()
            assert sensor._state == 5
    
        # Then it should have no data again
        with patch.object(OpenWeatherMapSensor.owa_client.data, 'get_rain', return_value={"test": None}):
            sensor.update()
            assert sensor._state == None
