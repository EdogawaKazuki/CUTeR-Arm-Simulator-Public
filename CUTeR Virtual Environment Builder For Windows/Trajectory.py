# output the trajectory
# the result should be a 2d (3*n) list
# each row represents a servo, each column represents a frame using three angles for the three servo
# the robot will move frame by frame, you can change the frequency
def generate_trajectory():

    # generate angle lists
    angle_0_list = list(reversed([i for i in range(-90, 90)]))
    angle_1_list = [i for i in range(180)]
    angle_2_list = [i for i in range(-180, 0)]
    angle_0_list.append("fire")
    angle_1_list.append("fire")
    angle_2_list.append("fire")
    angle_0_list += reversed(angle_0_list)
    angle_1_list += reversed(angle_1_list)
    angle_2_list += reversed(angle_2_list)

    return [angle_0_list, angle_1_list, angle_2_list]

