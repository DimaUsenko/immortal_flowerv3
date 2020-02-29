import datetime
import pytz
import random
import os
import pandas as pd
import paho.mqtt.client as mqtt
import flw_project_functions as flw
import flw_project_class as flwCl


client = mqtt.Client()
client.on_connect = flw.on_connect
client.on_message = flw.on_message


client.username_pw_set("njelhmbg", "FLLRBnPB4UiD")
client.connect("hairdresser.cloudmqtt.com", 16008, 60)

client.loop_start()


time_zone = pytz.timezone("Europe/Moscow")
date = datetime.datetime(2020, 2, 28, 11, 0, 0, 0, time_zone)
'''date = datetime.datetime.now(datetime.timezone.utc)'''


latitude = 57.57
longitude = 37.37
number_of_clouds = 30  # how much clouds u want
cloud_list = list()


for i in range(number_of_clouds):

    center_of_cloud_x = random.randint(-150, 150)
    center_of_cloud_y = random.randint(-150, 150)
    height_cloud = random.randint(50, 150)
    speed_x = random.randint(-7, 7)
    speed_y = random.randint(-7, 7)
    const_x = random.randint(10, 40)
    const_y = random.randint(10, 40)
    cloud_list.append(flwCl.Cloud(center_of_cloud_x, center_of_cloud_y, height_cloud, speed_x, speed_y, const_x, const_y))


flower = flwCl.Flower(x0=0, y0=0, z0=0) # the coordinates of the flower
lamp = flwCl.Lamp()
lamp_zero_status = lamp.check() # initially the lamp has the OFF status

work_time = list()
status = list()


client.publish("immortal_flower", 'The starting time of simulation and the initial status of the lamp:')
client.publish("immortal_flower", str(date.strftime("%Y-%m-%d-%H:%M")+' '+lamp_zero_status.lower()))
client.publish("immortal_flower",  '----------------------------------------------------------------- ')


number_of_simulated_hours = 1


for t in range(number_of_simulated_hours*60):

    checking = list()
    sun = flwCl.Sun(latitude, longitude, date)
    work_time.append(date.strftime("%Y-%m-%d-%H:%M"))

    for i in range(number_of_clouds):

        cloud = cloud_list[i]

        if flw.is_intersection(sun, cloud, flower) or sun.vec()[2] < 0:

            checking.append(True)

        else:

            checking.append(False)

    if True in checking:

        lamp.on()

    else:

        lamp.off()

    flw.plotting(sun, cloud_list, flower, t,number_of_clouds)  # plotting function for each time point

    status.append(lamp.check())
    lamp_curr_status = lamp.check()

    if lamp_curr_status != lamp_zero_status:

        client.publish("immortal_flower", str(date.strftime("%Y-%m-%d-%H:%M")+' '+lamp.check()))

    lamp_zero_status = lamp_curr_status

    flw.update_field(cloud_list, sun,number_of_clouds)
    date += datetime.timedelta(minutes=1)
    #time.sleep(60) if u wanna modeling irl time


client.publish("immortal_flower",  '----------------------------------------------------------------- ')
client.publish("immortal_flower", 'The end time of the simulation and the final lamp status:')
client.publish("immortal_flower", str(date.strftime("%Y-%m-%d-%H:%M")+' '+lamp_zero_status.lower()))


client.loop_stop()
client.disconnect()

flw.modeling(number_of_simulated_hours)

os.startfile("MODELING.mp4")
df = pd.DataFrame({'Time since start': work_time, 'Lamp Status': status})
df.to_excel('WORK_TABLE.xlsx')
flw.path_clear()