
def generate_obj_trajectory():

    # generate position lists
    x_pos_list = list(reversed([i for i in range(-90, 90)]))
    y_pos_list = [0 for i in range(180)]
    z_pos_list = [0 for i in range(-180, 0)]
    x_pos_list += reversed(x_pos_list)
    y_pos_list += reversed(y_pos_list)
    z_pos_list += reversed(z_pos_list)
    
    # generate eular angle lists
    x_rot_list = list(reversed([i for i in range(-90, 90)]))
    y_rot_list = [0 for i in range(180)]
    z_rot_list = [0 for i in range(-180, 0)]
    x_rot_list += reversed(x_rot_list)
    y_rot_list += reversed(y_rot_list)
    z_rot_list += reversed(z_rot_list)

    return [x_pos_list, y_pos_list, z_pos_list, x_rot_list, y_rot_list, z_rot_list]

trajectories = generate_obj_trajectory()
return_str = ''
for trajectory in trajectories:
    return_str += ",".join([str(i) for i in trajectory]) + ";"
with open('objTraj.txt', 'w') as f:
    f.write(return_str)