import Trajectory

# generate trajectory file
if Trajectory.using_cartesian_point:
    trajectories = Trajectory.generate_trajectory_cartesian_point()
    return_str = 'point;'
else:
    trajectories = Trajectory.generate_trajectory()
    return_str = 'angle;'
for trajectory in trajectories:
    return_str += ",".join([str(i) for i in trajectory]) + ";"
with open('trajectory.txt', 'w') as f:
    f.write(return_str)

