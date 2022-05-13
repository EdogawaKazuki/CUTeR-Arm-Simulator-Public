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
is_playing = -1


# init robot angle
robot_joint_angle = [0, 180, -170]
fire = False 
prefix = ''


# control robot arm according to the trajectory list
def process_trajectory():
    global prefix
    global fire
    global is_playing
    # get generated trajectory
    if Trajectory.using_cartesian_point:
        angle_lists = Trajectory.generate_trajectory_cartesian_point()
        prefix = 'point,'
    else:
        angle_lists = Trajectory.generate_trajectory()
    # set the angle of robots
    for i in range(len(angle_lists[0])):
        if is_playing == 1:
            if angle_lists[0][i] == "fire":
                fire = True
                continue
            for j in range(3):
                robot_joint_angle[j] = angle_lists[j][i]
            time.sleep(1/50)
        elif is_playing == 0:
            while is_playing == 0:
                pass
        elif is_playing == -1:
            break
    if is_playing == 1:
        prefix = 'end,'
        is_playing = -1


# handle request from application
def handle_request():
    global robot_joint_angle
    global is_playing
    global fire
    global prefix
    while True:
        try:
            data, address = sock.recvfrom(max_length)
            # uncomment the print if you want to check the request
            # print(data)
            # the data will be in format:
            # <request type>,<request data 1>,...,<request data n>,end
            data = data.decode('UTF-8').split(',')
            if data[0] == "get":
                print(robot_joint_angle)
                if fire:
                    angle_str = prefix + "fire," + str(robot_joint_angle[0]) + "," + str(robot_joint_angle[1]) + \
                                "," + str(robot_joint_angle[2]) + ",end"
                    fire = False
                else:
                    angle_str = prefix + str(robot_joint_angle[0]) + "," + str(robot_joint_angle[1]) + \
                            "," + str(robot_joint_angle[2]) + ",end"
                # print("send:", angle_str)
                sock.sendto(angle_str.encode('UTF-8'), address)
            elif data[0] == "post":
                # print("receive:", data[1], data[2], data[3])
                robot_joint_angle[0] = data[1]
                robot_joint_angle[1] = data[2]
                robot_joint_angle[2] = data[3]
                prefix = ''
            elif data[0] == "play":
                if is_playing == 0:
                    is_playing = 1
                elif is_playing == -1:
                    is_playing = 1
                    trajectory_thread = threading.Thread(target=process_trajectory)
                    trajectory_thread.start()
            elif data[0] == "stop":
                prefix = ''
                robot_joint_angle[0] = data[1]
                robot_joint_angle[1] = data[2]
                robot_joint_angle[2] = data[3]
                is_playing = -1
            elif data[0] == "pause":
                is_playing = 0

        except Exception as err:
            print(err)


# start the server thread
server_thread = threading.Thread(target=handle_request)
server_thread.start()
print("server started")






