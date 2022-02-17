import Trajectory

trajectories = Trajectory.generate_trajectory()
return_str = ''
for trajectory in trajectories:
    return_str += ",".join([str(i) for i in trajectory]) + ";"
print(return_str)
with open('trajectory.txt', 'w') as f:
    f.write(return_str)