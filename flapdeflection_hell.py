import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from math import *

# Algorithm for the visualisation of the 3D positions of the paticles in time
#sad and lonely

max_snapshot = [100, 3626, 3626]

file_no = 0  # input("Select .dat file to import [integer between 0 and 2]: ")

f = open("data\Case" + str(file_no) + ".dat", 'r')

data = np.zeros((5001, 20001, 3))  # (snapshot, trackID, values)
times = np.array([])
snapshot = -1
no_part = 0
time = -1

for line in f.readlines():
    if line.startswith("TITLE") or line.startswith("VARIABLES") or line.startswith("DATAPACKING") or line.startswith(
            "I="):
        continue
    if line.startswith("ZONE"):
        snapshot = int(line.split(' ')[2][:-2])
        # print(f"Snapshot = {snapshot}")
        continue
    if line.startswith("STRANDID"):
        time = float(line.split('=')[2])
        times = np.append(times, time)
        # print(f"Time = {time}")
        continue
    values = line.split(' ')
    tid = int(values[8])  # trackID
    #    print(tid)
    data[snapshot][tid][0] = values[0]  # x-position
    data[snapshot][tid][1] = values[1]  # y-position
    data[snapshot][tid][2] = values[2]  # z-position
    # data[snapshot][tid][3] = values[4]  # x-velocity (u)
    # data[snapshot][tid][4] = values[5]  # y-velocity (v)
    # data[snapshot][tid][5] = values[6]  # z-velocity (w)
    # data[snapshot][tid][6] = values[7]  # Speed magnitude (|V|)
    # data[snapshot][tid][7] = values[9]  # x-acceleration (ax)
    # data[snapshot][tid][8] = values[10]  # y-acceleration (ay)
    # data[snapshot][tid][9] = values[11]  # z-acceleration (az)
    # data[snapshot][tid][10] = values[12]  # acceleration magnitude (|a|)

g = open("data\TrackIDupdate" + str(file_no) + ".dat", 'r')

marker_groups = []
for line in g.readlines():
    curr_marker = list(map(int, line[:-2].split(' ')))
    marker_groups.append(curr_marker)

g.close()
# print(marker_groups)

x_avg = []

for marker in marker_groups:
    no_x = 0
    for snapshot in range(max_snapshot[file_no]):
        for tid in marker:
            x_pos = data[snapshot][tid][0]
            y_pos = data[snapshot][tid][1]
            if x_pos < 0:
                no_x += 1
    if no_x < 20:
        for snapshot in range(max_snapshot[file_no]):
            for tid in marker:
                data[snapshot][tid] = 0
                # data[snapshot][tid] = 0
                # data[snapshot][tid]

f.close()

f0 = open("data\Case0.dat", 'r')

data0 = np.zeros((101, 20001, 3))  # (snapshot, trackID, values)
times0 = np.array([])
snapshot0 = -1
no_part0 = 0
time0 = -1

for line0 in f0.readlines():
    if line0.startswith("TITLE") or line0.startswith("VARIABLES") or line0.startswith(
            "DATAPACKING") or line0.startswith(
            "I="):
        continue
    if line0.startswith("ZONE"):
        snapshot0 = int(line0.split(' ')[2][:-2])
        # print(f"Snapshot = {snapshot}")
        continue
    if line0.startswith("STRANDID"):
        time0 = float(line0.split('=')[2])
        times0 = np.append(times0, time0)
        # print(f"Time = {time}")
        continue
    values0 = line0.split(' ')
    tid0 = int(values0[8])  # trackID
    #    print(tid)
    data0[snapshot0][tid0][0] = values0[0]  # x-position
    data0[snapshot0][tid0][1] = values0[1]  # y-position
    data0[snapshot0][tid0][2] = values0[2]  # z-position
    # data0[snapshot][tid][3] = values[4]  # x-velocity (u)
    # data0[snapshot][tid][4] = values[5]  # y-velocity (v)
    # data0[snapshot][tid][5] = values[6]  # z-velocity (w)
    # data0[snapshot][tid][6] = values[7]  # Speed magnitude (|V|)
    # data0[snapshot][tid][7] = values[9]  # x-acceleration (ax)
    # data0[snapshot][tid][8] = values[10]  # y-acceleration (ay)
    # data0[snapshot][tid][9] = values[11]  # z-acceleration (az)
    # data0[snapshot][tid][10] = values[12]  # acceleration magnitude (|a|)

f0.close()

k = 0
x_value_lst0 = []
y_value_lst0 = []
z_value_lst0 = []
# time_lst0 = []

while k < 20001:
    if data0[0][k][0] < int(-1):
        x_value_lst0.append(data0[0][k][0])
        y_value_lst0.append(data0[0][k][1])
        z_value_lst0.append(data0[0][k][2])
        # time_lst0.append(times0[k])
        k += 1
    else:
        k += 1

A_mat0 = np.zeros((int(len(x_value_lst0)), 3))
z_mat0 = np.zeros(int(len(x_value_lst0)))

for l in range(len(x_value_lst0)):
    A_mat0[l][0] = 1
    A_mat0[l][1] = x_value_lst0[l]
    A_mat0[l][2] = y_value_lst0[l]
    z_mat0[l] = z_value_lst0[l]

A_mat_T0 = A_mat0.transpose()
ATA0 =  A_mat_T0.dot(A_mat0)
ATy0 = A_mat_T0.dot(z_mat0)
ATA_inv0 = np.linalg.inv(ATA0)

a0 = ATA_inv0.dot(ATy0)
# z = a0 + a1x +a2y

x0 = np.outer(np.linspace(-1000, -600, 30), np.ones(30))
y0 = x0.copy().T  # transpose
z0 = a0[0] + a0[1] * x0 + a0[2] * y0

parameter = max_snapshot[file_no] #int(input('Which snapshot do you want to observe '))

alpha_lst = []
mega_e = np.array([])
for p in range(parameter):
    i = 0
    x_value_lst = []
    y_value_lst = []
    z_value_lst = []
    time_lst = []

    while i < 20001:
        if data[p][i][0] < int(-1):
            x_value_lst.append(data[p][i][0])
            y_value_lst.append(data[p][i][1])
            z_value_lst.append(data[p][i][2])
            i += 1
        else:
            i += 1

    A_mat = np.zeros((int(len(x_value_lst)), 3))
    z_mat = np.zeros(int(len(x_value_lst)))
    Qz = np.eye(int(len(x_value_lst)))

    for j in range(len(x_value_lst)):
        A_mat[j][0] = 1
        A_mat[j][1] = x_value_lst[j]
        A_mat[j][2] = y_value_lst[j]
        z_mat[j] = z_value_lst[j]

    A_mat_T = A_mat.transpose()
    ATA = A_mat_T.dot(A_mat)
    ATy = A_mat_T.dot(z_mat)
    ATA_inv = np.linalg.inv(ATA)

    Qz_inv = np.linalg.inv(Qz)
    Qx = np.linalg.inv(A_mat_T.dot(Qz_inv.dot(A_mat)))
    Qe = Qz - A_mat.dot(Qx.dot(A_mat_T))

    sigma_e = np.zeros(Qe.shape[0])
    for i in range(Qe.shape[0]):
        sigma_e[i] = np.sqrt(Qe[i, i])

    a = ATA_inv.dot(ATy)
    # z = a0 + a1x +a2y

    e_vec = z_mat - A_mat.dot(a)
    e_norm = np.zeros(len(e_vec))

    for i in range(len(e_vec)):
        e_norm[i] = abs(e_vec[i] / sigma_e[i])


    print(e_vec[0], e_norm[0])

    x = np.outer(np.linspace(-1000, -600, 30), np.ones(30))
    y = x.copy().T  # transpose
    z = a[0] + a[1] * x + a[2] * y

    cos_alpha = abs(a0[1] * a[1] + a0[2] * a[2] + 1 * 1) / (
                sqrt(a0[1] ** 2 + a0[2] ** 2 + 1 ** 2) * sqrt(a[1] ** 2 + a[2] ** 2 + 1 ** 2))

    # if a0[1] * a[1] + a0[2] * a[2] + 1 * 1 > 0:
    #     alpha = acos(cos_alpha)
    # else:
    #     alpha = -acos(cos_alpha)
    
    alpha = acos(cos_alpha)
    alpha_lst.append(degrees(alpha))
    if degrees(alpha) > 60:
        print(p)
    # print(cos_alpha)
    # print('angle between two planes is: ', degrees(alpha))
snapshot
        

plt.hist(mega_e, bins=20)
plt.show()

plt.plot(alpha_lst)
#plt.title('Angle of attack vs time for case 1')
plt.xlabel('Time [s]')
plt.ylabel('Angle of attack [degrees]')
plt.grid(True, which='both')
plt.show()