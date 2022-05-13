from sqlite3 import Time
import time
import socket
import threading
import math

# flag for connect to real robot
import Trajectory

# 0.0.0.0 means bind all available IPv4 address
host = "0.0.0.0"
# IP port
port = 22000
# max packet size
max_length = 65000
# create the server socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((host, port))


# executing trajectory robot flag
is_playing = False


# init robot angle
robot_joint_angle = [90, 180, 10]
fire = False 

# control robot arm according to the trajectory list
def process_trajectory():
    global fire
    # get generated trajectory
    angle_lists = Trajectory.generate_trajectory()
    # set the angle of robots
    for i in range(len(angle_lists[0])):
        if is_playing:
            if angle_lists[0][i] == "fire":
                fire = True
                continue
            for j in range(3):
                robot_joint_angle[j] = angle_lists[j][i]
            time.sleep(1/50)
        else:
            break

last_time = time.time()
# handle request from application
def handle_request():
    global last_time
    global robot_joint_angle
    global is_playing
    global fire
    while True:
        try:
            data, address = sock.recvfrom(max_length)
            # uncomment the print if you want to check the request
            # print(data)
            # the data will be in format:
            # <request type>,<request data 1>,...,<request data n>,end
            data = data.decode('UTF-8').split(',')
            if data[0] == "get":
                if fire:
                    angle_str = "fire," + str(robot_joint_angle[0]) + "," + str(robot_joint_angle[1]) + \
                                "," + str(robot_joint_angle[2]) + ",end"
                    fire = False
                else:
                    angle_str = "" + str(robot_joint_angle[0]) + "," + str(robot_joint_angle[1]) + \
                            "," + str(robot_joint_angle[2]) + ",end"
                # print("send:", angle_str)
                sock.sendto(angle_str.encode('UTF-8'), address)
            elif data[0] == "post":
                # print("receive:", data[1], data[2], data[3])
                robot_joint_angle[0] = data[1]
                robot_joint_angle[1] = data[2]
                robot_joint_angle[2] = data[3]
            elif data[0] == "play":
                is_playing = True
                trajectory_thread = threading.Thread(target=process_trajectory)
                trajectory_thread.start()
            elif data[0] == "stop":
                is_playing = False
        except Exception as err:
            print(err)


# start the server thread
server_thread = threading.Thread(target=handle_request)
server_thread.start()
print("server started")
trajectories = Trajectory.generate_trajectory()
return_str = ''
for trajectory in trajectories:
    return_str += ",".join([str(i) for i in trajectory]) + ";"
print(return_str)
with open('trajectory.txt', 'w') as f:
    f.write(return_str)







