#Python code
from codrone_edu.drone import *
from time import sleep
from sys import exit

colors = {
        "black": (0, 0, 0),
        "yellow": (255, 255, 0),
        "red": (255, 0, 0),
        "green": (0, 255, 0),
        "purple": (128, 0, 128),
        "pink": (255, 192, 203),
        "bright_cyan": (0, 255, 255)
    }

flip = {
    "black": "left",
    "yellow": "right",
    "green": "back",
}


def drone_display_led(led_color_name):

    if led_color_name == "start":
        print("Set color to pink", sep=" ")
        r, g, b = colors["pink"]
        drone.set_drone_LED(r, g, b, 100)
        sleep(2)
        print("Set color to bright_cyan")
        r, g, b = colors["bright_cyan"]
        drone.set_drone_LED(r, g, b, 100)
        sleep(2)
        return

    if led_color_name in colors:
        r, g, b = colors[color_name]
        drone.set_drone_LED(r,g,b,100)
        print(f"Set color to: {led_color_name=} / {r=} {g=} {b=}")
        return

    return False


def pos_drone():
    data_xyz = drone.get_position_data()
    actual_temperature = drone.get_drone_temperature()
    actual_battery = drone.get_battery()
    print(f"Pos xyz: {data_xyz} / Temp: {actual_temperature} C / Battery: {actual_battery}")
    return actual_temperature, actual_battery


def test_temp_batt():
    flight_temperature, flight_battery = pos_drone()
    if flight_temperature > 60 or flight_battery < 50:
        print(f"WARNING: {flight_temperature=} / {flight_battery=}")
        drone.set_drone_LED(255, 0, 0, 100)  # RGB
        drone.land()
        drone.emergency_stop()
        exit("Temp or batt")

try:
    drone = Drone()
    drone.pair()  # pair automatically, may not always work
    # drone.pair(port_name = 'COM3')    # pair with a specific port
    data = drone.get_position_data()
    print(f"Drone at: {data=}")

except Exception as e:
    print(f"Err: {e=}")
    exit("Pair error")

# ok - let's run
color = drone.get_color_data()
index_color = color[9]
color_name = index_color.name.lower()
print(f"Color detected: {color_name=}")
if color_name in colors:
    drone_display_led(color_name)
else:
    drone_display_led("start")

sleep(3)
drone.takeoff()

# do code

for _ in range(4):
    drone.hover(1)
    drone.move_forward(15, "cm", 0.1)
    test_temp_batt()

if color_name in flip:
    test_temp_batt()
    drone.set_drone_LED(0, 0, 100, 100)  # RGB
    drone.flip(flip[color_name])
    drone.hover(2)
    test_temp_batt()
else:
    drone.set_drone_LED(100, 0, 0, 100)  # RGB
    drone.hover(2)
    drone.set_drone_LED(0, 100, 0, 100)  # RGB
    drone.hover(2)

for _ in range(4):
    drone.hover(1)
    drone.move_backward(15, "cm", 0.1)
    test_temp_batt()


drone.land()
flight_time = drone.get_flight_time()
drone.stop_motors()
print(f"Drone flight time: {flight_time}")