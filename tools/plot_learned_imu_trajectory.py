#! /usr/bin/env python
# coding: utf-8

import csv
import matplotlib
import matplotlib.pyplot as plt

tmp_folder = "tmp_imu_during_standup"

def construct_list_of_pairs(filename, roll_or_pitch):
    indices = compute_indices(filename, roll_or_pitch)

    res = [[] for _ in indices]

    with open(tmp_folder + "/" + filename,"rb") as f:
        reader = csv.reader(f, delimiter=",")

        # comutes the nb of trajectories
        row = next(reader)
        while "#" in row[0] or "time" in row[0]:
            row = next(reader)

        for row in reader:
            for i in range(len(indices)):
                res[i].append(float(row[indices[i]]))
        f.close()
    return res

def compute_indices(filename, roll_or_pitch):
    assert(roll_or_pitch=="roll" or roll_or_pitch=="pitch")

    # 0 correspond to time
    res = [0]

    with open(tmp_folder + "/" + filename,"rb") as f:
        reader = csv.reader(f, delimiter=",")

        row = next(reader)
        while "#" in row[0]:
            row = next(reader)

        for i in range(len(row)):
            if roll_or_pitch in row[i]:
                res.append(i)
        f.close()
    return res

tol_imu_pitch = 2
tol_imu_roll= 2

#Pitch
trajectories= construct_list_of_pairs("imu_trajectories.csv", "pitch")
model= construct_list_of_pairs("imu_model.csv", "pitch")
model[2] = map(lambda x:tol_imu_pitch*x,model[2])
plt.errorbar(model[0], model[1], model[2], linestyle='None')
for i in range(1, len(trajectories)):
    plt.plot(trajectories[0], trajectories[i])#, linestyle='None', marker='o', markersize='1')

plt.show()

plt.clf()

#Roll
trajectories= construct_list_of_pairs("imu_trajectories.csv", "roll")
model= construct_list_of_pairs("imu_model.csv", "roll")
model[2] = map(lambda x:tol_imu_roll*x,model[2])
plt.errorbar(model[0], model[1], model[2], linestyle='None')
for i in range(1, len(trajectories)):
    plt.plot(trajectories[0], trajectories[i])#, linestyle='None', marker='o')

plt.show()
