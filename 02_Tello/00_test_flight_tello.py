from tello_solectric_pl import TelloEDU
from djitellopy import Tello
import matplotlib.pyplot as plt
from time import sleep

print("Początek testów... tworzymy obiekt i próbujemy połączyć się, a potem wystartować...")
dron = TelloEDU(info_all=True)

# próbujemy inicjować połączenie - bez tego nic nie działa
print("Teraz wykonamy połączenie z dronem")
if not dron.connect():
    # ten blok kodu działa w przypadku błędu
    print("Połączenie nie udało się - KONIEC.")
    # kończymy działanie programu, przekazując do systemu operacyjnego
    # kod błędu 2
    exit(2)

# Jest OK - działamy dalej
print("Połączenie udane - start...")
dron.takeoff()
sleep(2)
# pobieramy informacje o statusie drona
height = dron.get_height()
battery = dron.get_battery()
print(f"Dron na wysokości {height}; bateria naładowana: {battery}")
dron.flip_left()
#
dron.streamon()
frames = dron.get_frame_read()
sleep(3)
one_frame = frames.frame
dron.streamoff()
plt.imshow(one_frame)
plt.axis('off')  # Hide axes
plt.show()
print("I lądujemy...")
dron.land()
print("Koniec testu")