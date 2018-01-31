#!/usr/bin/env python 


try:
    import bme680                
    except ImportError:
    print("unable to comply. No sensor module detected.")
    unable = True
else:
    sensor = bme680.BME680()
    unable = False

# These oversampling settings can be tweaked to
# change the balance between accuracy and noise in
    # the data.")

sensor.set_humidity_oversample(bme680.OS_2X)
sensor.set_pressure_oversample(bme680.OS_4X)
sensor.set_temperature_oversample(bme680.OS_8X)
sensor.set_filter(bme680.FILTER_SIZE_3)

def GetSensors():
    if sensor.get_sensor_data() && not unable:

        output = "{0:.2f} C,{1:.2f} hPa,{2:.3f} %RH".format(sensor.data.temperature, sensor.data.pressure, sensor.data.humidity)
        
        print(output)
        return output

