#Python code
from codrone_edu.drone import *
from time import sleep
from sys import exit

def pozycja(distance):
    data_xyz = drone.get_position_data()
    temperature = drone.get_drone_temperature()
    print(f"Pozycja xyz: {data_xyz} / Temperatura: {temperature} C / {distance=}")
    return temperature

drone = Drone()
drone.pair() # pair automatically, may not always work
# drone.pair(port_name = 'COM3')    # pair with a specific port

print(f"{drone.get_color_data()}")


drone.set_drone_LED(0, 255, 0, 100) #RGB
distance = 1
pozycja(distance)
# drone.takeoff()

while True:
    drone.set_drone_LED(0, 30, 30, 100) #RGB
    temperature = pozycja(distance)
    if temperature> 60:
        print(f"Temperature {temperature} - overtemperature! Landing emergency!")
        drone.set_drone_LED(255, 0, 0, 100)  # RGB
        # drone.land()
        drone.emergency_stop()
        break

    # drone.hover(1)
    # drone.move_forward(15, "cm", 0.1)
    distance += 1
    color_data = drone.get_front_color()
    print(f"Wykryty kolor: {color_data}")
    drone.set_drone_LED(0, 50, 0, 100)  # RGB
    sleep(3.5)
    if distance > 7:
        # drone.land()
        drone.close()
        break

print("STOP")

