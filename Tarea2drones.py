# Importan funciones de tiempo, comandos y localizaciones.
import time
from dronekit import connect, VehicleMode, LocationGlobalRelative, Command, LocationGlobal
from pymavlink import mavutil
import Tkinter as tk
#Indica la velocidad para: adelante, a los lados, arriba y abajo.
def set_velocity_body(vehicle, vx, vy, vz):
    msg = vehicle.message_factory.set_position_target_local_ned_encode(
            0,
            0, 0,
            mavutil.mavlink.MAV_FRAME_BODY_NED,
            0b0000111111000111, #-- BITMASK -> Consider only the velocities
            0, 0, 0,        #-- POSITION
            vx, vy, vz,     #-- VELOCITY
            0, 0, 0,        #-- ACCELERATIONS
            0, 0)
    vehicle.send_mavlink(msg)
    vehicle.flush()
#Empieza a ejecutar la informaci{on para despegar
def arm_and_takeoff(TargetAltitude):
	print("Executing takeoff")
#Si no está armado, decir que no esta armado y que está esperando...
	while not drone.is_armable:
		print("Vehicle is not armable, waiting....")
		time.sleep(1)
#Cuando está listo para armar, comienza a checar si los motores están listos para ser prendidos
	print("ready to arm")
	drone.mode = VehicleMode("GUIDED")
	drone.armed = True
#Cuando todavía no está listo, está esperando 
	while not drone.armed:
		print("Waiting for arming....")
		time.sleep(1)
#Cuando esté listo, va a despegar
	print("Ready for takeoff, taking off...")
	drone.simple_takeoff(TargetAltitude)
#Cuando despega el dron busca una altitud relativa, más no exacta
	while True:
		Altitude = drone.location.global_relative_frame.alt
		print("altitude: ",Altitude)
		time.sleep(1)

		if Altitude >= TargetAltitude * 0.95:
			print("Altitude reached")
			break
#Indica que con las teclas se indicará hacía dónde se moverá el dron: arriba, abajo, izquierda o derecha
def key(event):
    if event.char == event.keysym: #-- standard keys
        if event.keysym == 'r':
        	drone.mode = VehicleMode("RTL") 

    else: #-- non standard keys
        if event.keysym == 'Up':
        	set_velocity_body(drone,5,0,0)
            
        elif event.keysym == 'Down':
        	set_velocity_body(drone,-5,0,0)
            
        elif event.keysym == 'Left':
        	set_velocity_body(drone,0,-5,0)
            
        elif event.keysym == 'Right':
        	set_velocity_body(drone,0,5,0)
       



#El dron se conceta al comando que se indica
drone = connect('127.0.0.1:14551', wait_ready=True)

#Tendrá una altitud de 10m
arm_and_takeoff(10)
 
#Da la indicación de cambiar al modo RTL si se presiona r
root = tk.Tk()
print(">> Control the drone with the arrow keys. Press r for RTL mode")
root.bind_all('<Key>', key)
root.mainloop()
