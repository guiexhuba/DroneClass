from dronekit import connect, VehicleMode, LocationGlobalRelative
import time

#Se conecta y hace que el dron despegue
def arm_and_takeoff(TargetAltitude):
	print("Executing takeoff")

	while not drone.is_armable:
		print("Vehicle is not armable, waiting....")
		time.sleep(1)

	print("ready to arm")
	drone.mode = VehicleMode("GUIDED")
	drone.armed = True
	while not drone.armed:
		print("Waiting for arming....")
		time.sleep(1)

	print("Ready for takooff, taking off...")
	drone.simple_takeoff(TargetAltitude)

	while True:
		Altitude = drone.location.global_relative_frame.alt
		print("altitude: ",Altitude)
		time.sleep(1)

		if Altitude >= TargetAltitude * 0.95:
			print("Altitude reached")
			break


#Vehicle connection (Se conecta a la computadora)
drone = connect('127.0.0.1:14551', wait_ready=True)
arm_and_takeoff(20)
#Coordenadas, altitud y velocidad
drone.airspeed = 10
a_location = LocationGlobalRelative(20.736272,-103.456860,15)
b_location = LocationGlobalRelative(20.735569,-103.456921,15)
c_location = LocationGlobalRelative(20.735604,-103.457414,15)


print("Se mueve al punto a")
drone.simple_goto(a_location)
time.sleep(15)
print("Se mueve al punto b")
drone.simple_goto(b_location)
time.sleep(15)
print("Se mueve al punto c")
drone.simple_goto(c_location)
time.sleep(15)
#Regreso al punto de partida
drone.mode = VehicleMode("RTL")
#la bateria
print(drone.batery.level,"v")