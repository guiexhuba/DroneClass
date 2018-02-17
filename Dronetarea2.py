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
#Empieza a ejecutar la informacion para despegar (20 y 21)
def arm_and_takeoff(TargetAltitude):
	print("Executing takeoff")
#Si no esta listo, mandar mensaje de esperando
	while not drone.is_armable:
		print("Vehicle is not armable, waiting....")
		time.sleep(1)
#Si la informacion ya esta lista, el dron esta listo para armar 
	print("ready to arm")
	drone.mode = VehicleMode("GUIDED")
	drone.armed = True 
#Si no esta lista, mandara el mensaje de esperando
	while not drone.armed:
		print("Waiting for arming....")
		time.sleep(1)
#Cuando este armado, va a despegar
	print("Ready for takeoff, taking off...")
	drone.simple_takeoff(TargetAltitude)
#Al despegar buscara una altitud relativa a la que se indico, mas no exacta 
	while True:
		Altitude = drone.location.global_relative_frame.alt
		print("altitude: ",Altitude)
		time.sleep(1)

		if Altitude >= TargetAltitude * 0.95:
			print("Altitude reached")
			break
#Indica que las teclas indicaran la direccion del dron: adelante, atras, izquierda o derecha
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

#Indica la altitud
arm_and_takeoff(10)
#Da la indicacion de cambiar a modo RTL , si se presiona r
root = tk.Tk()
print(">> Control the drone with the arrow keys. Press r for RTL mode")
root.bind_all('<Key>', key)
root.mainloop()
