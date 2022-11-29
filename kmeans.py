import matplotlib.pyplot as plt
import numpy as np
import math
import copy as cp

data = [(1,2), (2, 2), (2, 1), (-1, 5), (-2, -1), (-1, -1)]
centers = [(1,2), (-1, 5)]

# calculates the distance between a point and a center
def calc_dist(point, center):
    return np.linalg.norm(np.array(point) - np.array(center))

# calculates a parallel array to the data points array
# representing the index of their closest center
def assign_centers(data, centers):
    assigned = list()

    for point in data:
        cent = 0
        min_dist = math.inf
        for cent_ind in range(len(centers)):
            cur_dist = calc_dist(point, centers[cent_ind])
            if cur_dist < min_dist:
                cent = cent_ind
                min_dist = cur_dist
    
        assigned.append(cent)

    return assigned
        
# calculate the total distance between all of the 
# #data points and their respective centers
def total_difs(data, centers, asgnmts):
    # sum go through assigned values and sum their differences
    cum_sum = 0

    for point_ind in range(len(data)):
        cum_sum += calc_dist(data[point_ind], centers[asgnmts[point_ind]])

    return cum_sum

# calculates the average position between a list of points
def calculate_sing_avg(points):
    point_sum = np.array([0] * len(points[0]))

    for point in points:
        point_sum += np.array(point)
    
    point_sum = point_sum / len(points)

    return list(point_sum)

def calculate_center_group(data, centers, asgnmts):
    cent_groups = [[] for _ in range(len(centers))]

    # make the group
    for point_ind in range(len(data)):
        cent_groups[asgnmts[point_ind]].append(data[point_ind])
    
    return cent_groups

# calculates the average position in between data assigned to specific centers
def calculate_new_cents(data, centers, asgnmts, cent_groups):
    # for each group, make a new center
    for group_ind in range(len(cent_groups)):
        cent_groups[group_ind] = calculate_sing_avg(cent_groups[group_ind])
    
    # return our new group
    return list(cent_groups)

# I am going to write this assuming k = 2 so I can make
# a nicer color scheme for the graph
def display_clusters(data, centers, cent_groups):
    # we need to separate clusters nicer
    groups_prep = list()
    for group in cent_groups:
        point_x = list()
        point_y = list()
        for point in group:
            point_x.append(point[0])
            point_y.append(point[1])
        groups_prep.append((point_x, point_y,))

    # we need to prepare the clusters of data
    centers_prep = list()
    for point in centers:
        center_x = [point[0]]
        center_y = [point[1]]
        centers_prep.append((center_x, center_y,))

    plt.plot(groups_prep[0][0], groups_prep[0][1], 'bo')
    plt.plot(centers_prep[0][0], centers_prep[0][1], 'bx')
    plt.plot(groups_prep[1][0], groups_prep[1][1], 'ro')
    plt.plot(centers_prep[1][0], centers_prep[1][1], 'rx')

    plt.show()


def train_points(data, orig_centers):
    dif_change = -1
    last_dif = -1

    cur_centers = cp.deepcopy(orig_centers)
    while dif_change != 0:
        # make an assignment
        assignments = assign_centers(data, cur_centers)
        print(assignments)

        # make the groups based on assignment
        cent_groups = calculate_center_group(data, cur_centers, assignments)

        # new centers
        new_cents = calculate_new_cents(data, cur_centers, assignments, cent_groups)

        # check differences
        cur_dif = total_difs(data, new_cents, assignments)

        # move forward in the calculation of differences
        dif_change = last_dif - cur_dif
        last_dif = cur_dif

        cur_centers = new_cents
    
    return cur_centers, last_dif

new_cents, difference = train_points(data, [[-.5, 2], [1, 3]])
assignments = assign_centers(data, new_cents)
groups = calculate_center_group(data, new_cents, assignments)
display_clusters(data, new_cents, groups)


# TODO Nevermind this was a waste of time. Kill yourself I guess.