# import libraries
import numpy as np
import time
import matplotlib.pyplot as plt
import datetime
import os

# Ask angle
angle = input('Enter the angle in degrees: ')
angle = float(angle)
# Convert angle to radians
theta = np.radians(angle)
# Ask initial velocity
v0 = input('Enter the initial velocity in m/s: ')
v0 = float(v0)
# Calculate Inicial x and y velocities
v0x = v0 * np.cos(theta)
v0y = v0 * np.sin(theta)
# Mass of the projectile
m = input('Enter the mass in kg: ')
m = float(m)
# Gravitational acceleration
g = input('Enter the gravitational acceleration constant in m/s: ')
g = float(g)
# Density of the fluid
rho = input('Enter the density of the fluid in kg/m³: ')
rho = float(rho)
# Radius of the projectile
radius = input('Enter the radius of the projectile in meters: ')
radius = float(radius)
# Cross sectional area of the projectile
A = np.pi * (radius**2)
# Calculate k
k = (1/2) * 0.47 * rho * A
# Ask Timestep
print("Enter the time step in seconds. The quality of the calculation will be better as the time step decreases.")
print("However, if you enter a value that is too small, such as 0.0000001, the program may take a long time to finish depending on the speed of your cpu:")
delta_t = input()
delta_t = float(delta_t)

# Ask initial positions
x0 = input('Enter the initial x position: ')
y0 = input('Enter the initial y position: ')

# Ask for name
name = input('Enter the name of the calculation. This will be the name of the log file. Character limit is 20: ')

# Set time to 0 seconds
t=0

print('Calculating...')
time.sleep(1)

list_of_positions = []

# Equations
u1 = 0
u2 = v0x
u3 = 0
u4 = v0y

# Important for finding approximated time to highest point
min_u4 = abs(u4)

# Start log
print("Starting the log. This is for viewing what is happening and making sure the program don't freeze.")

time.sleep(5)

print("==========< LOG START >==========")

# Log

def log(type, log):
    # Get current time
    current_time = str(datetime.datetime.now())

    # Make the log
    new_log = "»»" + current_time + ": " + type + ": " + log

    # Make the files directory
    folder_path = os.path.expandvars("%appdata%") + "\\Projectile Trajectory"
    if os.path.exists(folder_path):
        # Path exists. Create log file
        log_path = os.path.join(folder_path, name + "_log" + ".txt")

        # Wite the log to the log file
        with open(log_path, "a") as file:
            file.write(str(new_log))
            file.write("")
    else:
        os.makedirs(folder_path, exist_ok=True)
        log_path = os.path.join(folder_path, name + "_log" + ".txt")
        with open(log_path, "a") as file:
            file.write(str(new_log))
            file.write("")
    print(new_log)


while True:

    u1dot = 0
    u2dot = - (k/m) * np.sqrt(u2**2 + u4**2)*u2 * np.cos(theta)
    u3dot = u4
    u4dot = - (k/m) * np.sqrt(u2**2 + u4**2)*u4 * np.sin(theta) - g

    list_of_positions += [(u1, u3),]

    log("Info", "At time t = " + str(t) + ": x = " + str(u1) + ", y = " + str(u3) + ", x velocity = " + str(u1dot) + ", y velocity = " + str(u3dot) + ", x acceleration = " + str(u2dot) + ", y acceleration = " + str(u4dot))

    if (u3 < 0 or u3 == 0) and t != 0:
        folder_path = os.path.expandvars("%appdata%") + "\\Projectile Trajectory"
        file_path = os.path.join(folder_path, name + ".txt")
        with open(file_path, "a") as file:
            file.write(str(list_of_positions))
        log("Success", "Projectile hit the ground. All coordinates have been saved to: %appdata%\\Projectile Trajectory\\")

        break
    if abs(u4) < min_u4:  # Update min_u4 if a smaller value is found
        min_u4 = abs(u4)
    if u4 == 0:
        hp = t
        log("Success", "Found the exact time when the projectile reaches the highest point.")
        
    u1 = u1 + u1dot * delta_t
    u2 = u2 + u2dot * delta_t
    u3 = u3 + u3dot * delta_t
    u4 = u4 + u4dot * delta_t
    t += delta_t

print("Time to hit the ground: ", t)
if 'hp' in locals():
    print("Time to highest point: ", hp)
else:
    log("Warning", "Could not find the exact time when the projectile reaches the highest point. Going to print the most approximated result.")
    print("Time to highest point: ", min_u4)


# Extract x and y coordinates from the list of positions
x = [position[0] for position in list_of_positions]
y = [position[1] for position in list_of_positions]

# Create a line plot
plt.plot(x, y, marker='.')

# Add labels and title
plt.xlabel('x in meters')
plt.ylabel('y in meters')
plt.title('Trajectory of a projectile')

# Show the plot
plt.show()

