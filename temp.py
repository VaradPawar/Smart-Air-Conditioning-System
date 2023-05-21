import paho.mqtt.client as mqtt
import random
import time
import os

# Define mapping of hot pixels to number of people
hot_pixel_mapping = {1: (1, 3),
                     2: (4, 8),
                     3: (9, 13),
                     4: (14, 18),
                     5: (19, 23),
                     6: (24, 28),
                     7: (29, 30)}

# Set up MQTT client
client = mqtt.Client()

# Set up connection to broker
broker_address = "broker.hivemq.com"
client.connect(broker_address, 1883)

# Define constants
#room_temp = 27
hot_temp = 30
num_pixels = 64
grid_size = 8

# Set up initial room temperature as a range from 25 to 27
room_temp = range(25, 28)

# Generate random number of people
num_people = random.randint(1, 30)

# Generate random hot pixels
hot_pixels = random.sample(range(num_pixels), num_people)

# Initialize grid with room temperature
grid = [[random.uniform(25, 28) for _ in range(grid_size)] for _ in range(grid_size)]

# Set hot pixel temperatures
for pixel in hot_pixels:
    x = pixel // grid_size
    y = pixel % grid_size
    grid[x][y] = hot_temp

# Print grid and room temperature
print("Grid: ")
for row in grid:
    print(row)

print("Room temperature: ", room_temp)

# Publish room temperature and number of people to MQTT topic
client.publish("room/people", num_people)

# Calculate number of people based on hot pixel mapping
hot_pixel_count = sum([1 for row in grid for temp in row if temp == hot_temp])
if hot_pixel_count in hot_pixel_mapping:
    people_range = hot_pixel_mapping[hot_pixel_count]
    num_people = random.randint(people_range[0], people_range[1])
else:
    num_people = random.randint(1, 30)

# Print number of people
print("Number of people: ", num_people)

duration = 5 * 60 * 60  # 5 hours in seconds

start_time = time.time()

Air_condition_temp = random.randint(16, 25)
Room_Temp = random.randint(25, 31)
People = random.randint(0, 30)

# Set up forever loop to generate room temperature every 10 seconds
while (time.time() - start_time) < duration:
    # Wait for 10 seconds
    time.sleep(10)

    # Generate random hot pixels
    hot_pixels = random.sample(range(num_pixels), num_people)

    # Initialize grid with room temperature
    grid = [[random.uniform(25, 28) for _ in range(grid_size)] for _ in range(grid_size)]

    # Set hot pixel temperatures
    for pixel in hot_pixels:
        x = pixel // grid_size
        y = pixel % grid_size
        grid[x][y] = hot_temp

    # Print grid and room temperature
    print("Grid: ")
    for row in grid:
        print(row)


    # Calculate number of people based on hot pixel mapping
    hot_pixel_count = sum([1 for row in grid for temp in row if temp == hot_temp])
    if hot_pixel_count in hot_pixel_mapping:
        people_range = hot_pixel_mapping[hot_pixel_count]
        num_people = random.randint(people_range[0], people_range[1])
    else:
        num_people = random.randint(1, 30)

    # Print number of people
    print("Number of people: ", num_people)

    # Calculate the air conditioning setting temperature based on the number of people
    if num_people <= 5:
        ac_temp = 25
    elif num_people <= 10:
        ac_temp = 22
    elif num_people <= 15:
        ac_temp = 20
    elif num_people <= 20:
        ac_temp = 18
    else:
        ac_temp = 16

    # Print the air conditioning setting temperature
    print("Setting temperature: ", str(ac_temp), "degrees Celsius")

    client.publish("room/air_con", "t"+str(ac_temp))

    total_sum = 0
    num_elem = 0
    for row in grid:
        for elem in row:
            total_sum += elem
            num_elem +=1

    avg = total_sum/ num_elem

    Air_condition_temp = ac_temp
    Room_Temp = avg
    #Room_Temp = random.randint(25, 31)
    People = num_people

    air_con_temp = f'mosquitto_pub -d -q 1 -h "demo.thingsboard.io" -p "1883" -t "v1/devices/me/telemetry" -u "iCtTz85JvIAclMIxRDUF" -m {{"Air_condition_temp":{Air_condition_temp}}}'
    os.system(air_con_temp)

    room_temp = f'mosquitto_pub -d -q 1 -h "demo.thingsboard.io" -p "1883" -t "v1/devices/me/telemetry" -u "5Vq8UCd60cMXnVoE0sEz" -m {{"Room_Temp":{Room_Temp}}}'
    os.system(room_temp)

    people = f'mosquitto_pub -d -q 1 -h "demo.thingsboard.io" -p "1883" -t "v1/devices/me/telemetry" -u "INhSKnZWRZBQoM55SpTk" -m {{"People":{People}}}'
    os.system(people)
