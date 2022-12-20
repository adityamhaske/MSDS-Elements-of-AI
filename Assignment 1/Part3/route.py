#!/usr/local/bin/python3
# route.py : Find routes through maps
#
# Code by: Deveshwari Pujari (dpujari)
#
# Based on skeleton code by V. Mathur and D. Crandall, Fall 2022


# !/usr/bin/env python3
import sys
from math import tanh
from math import dist
from math import radians, cos, sin, asin, sqrt


def value_map(filename):
    value_dict = {}  # initiate a dictionary that stores, city->key : connected nodes-> values
    with open(filename, "r") as f:  # read
        for i in f.read().split('\n'):
            a = i.split(' ')  # store elements

            if (2>len(a)):  # len > 2 has no use hence can be neglected
                continue
            if a[0] not in value_dict.keys():
                value_dict[a[0]] = {a[1]: {'distance': int(a[2]), 'speed': int(a[3]), 'highway': a[4]}}
                value_dict[a[1]] = {a[0]: {'distance': int(a[2]), 'speed': int(a[3]), 'highway': a[4]}}
            else:
                value_dict[a[0]][a[1]] = {'distance': int(a[2]), 'speed': int(a[3]), 'highway': a[4]}
                if a[1] in value_dict.keys():
                    value_dict[a[1]][a[0]] = {'distance': int(a[2]), 'speed': int(a[3]), 'highway': a[4]}
                else:
                    value_dict[a[1]] = {a[0]: {'distance': int(a[2]), 'speed': int(a[3]), 'highway': a[4]}}
    return value_dict

dict1 = value_map('road-segments.txt')

def value_map2(filename):
    dict2 = {}
    with open(filename, "r") as f:  # read
        for i in f.read().split('\n'):
            a = i.split(' ')
            if (2<=len(a)):  # len > 2 has no use hence can be neglected
                dict2[a[0]] = [float(a[1]), float(a[2])]
        return dict2


d2 = value_map2('city-gps.txt')

# haversine distance formula referenced from
# https://stackoverflow.com/questions/4913349/haversine-formula-in-python-bearing-and-distance-between-two-gps-points

def haversine(longitude1, latitude1, longitude2, latitude2):
    # converting decimal degrees values -> radians
    longitude1, latitude1, longitude2, latitude2 = map(radians, [longitude1, latitude1, longitude2, latitude2])
    dlongitude = longitude2 - longitude1
    dlatitude = latitude2 - latitude1
    A = sin(dlatitude / 2) ** 2 + cos(latitude1) * cos(latitude2) * sin(dlongitude / 2) ** 2
    C = 2 * asin(sqrt(A))
    R = 3959.87433  # Radius of the Earth is 3960 miles
    return C * R

def heuristic(city, end):
    if city not in d2.keys():
        distance = 0
    else:
        distance = haversine(d2[end][0], d2[end][1], d2[city][0], d2[city][1])
    return distance


def segments(start, previous, city, end):
    main_list = ()
    for i in dict1[previous].items():
        if i[0]==city:
            main_list = ((i[0], (i[1]['distance'] / i[1]['speed']), i[1]['distance']),
                         (heuristic(city, end) / haversine(d2[start][0], d2[start][1], d2[end][0], d2[end][1])) + 1)
            break
    return main_list


def distance(start, prev, city, end):
    t_distance = 100000000
    dist_list = ()
    for i in dict1[prev].items():
        if i[0]!=city:
            continue
        dist_list = ((i[0], (i[1]['distance'] / i[1]['speed'], i[1]['distance'])),
                     30 * (heuristic(city, end) / haversine(d2[start][0], d2[start][1], d2[end][0], d2[end][1])) + i[1][
                         'distance'])
        break
    return dist_list


def time(start, prev, city, end):
    for i in dict1[prev].items():
        if i[0]!=city:
            continue
        main_list = ((i[0], (i[1]['distance'] / i[1]['speed']), i[1]['distance']), 40 * (heuristic(city, end) / haversine(d2[start][0], d2[start][1], d2[end][0],d2[end][1])) + (i[1]['distance'] / i[1]['speed']))
    return main_list


def delivery(start, prev, city, end, trip):
    time = 0
    for i in dict1[prev].items():
        if i[0]==city:
            if i[1]['speed']>=50:
                time = (i[1]['distance'] / i[1]['speed']) + 2 * tanh(i[1]['distance'] / 1000) * (
                        (i[1]['distance'] / i[1]['speed']) + trip)
                main_list = ((i[0], time, i[1]['distance']), 40 * (
                        heuristic(city, end) / haversine(d2[start][0], d2[start][1], d2[end][0],
                                                         d2[end][1])) + time)
            else:
                time = i[1]['distance'] / i[1]['speed']
                main_list = ((i[0], time, i[1]['distance']), 40 * (
                        heuristic(city, end) / haversine(d2[start][0], d2[start][1], d2[end][0],
                                                         d2[end][1])) + time)
    return main_list


def cost_fn(cost, start, c_node, succ, end, trip):
    if cost=='distance':
        a = distance(start, c_node, succ, end)
    elif cost=='segments':
        a = segments(start, c_node, succ, end)
    elif cost=='time':
        a = time(start, c_node, succ, end)
    elif cost=='delivery':
        a = delivery(start, c_node, succ, end, trip)
    return a


def successors(city):
    return [i for i in dict1[city].keys()]


def get_route(start, end, cost):
    fringe = [((start, 0, 0), 0)]  # Initialising the fringe with ((start_city,time,distance),h(s)+g(s))
    paths = [[(start, 0, 0, '', 0)]]
    visited_node = [start]

    while fringe:
        fringe = sorted(fringe, key=lambda x: x[1])
        c_node = fringe.pop(0)

        for succ in successors(c_node[0][0]):
            # pdb.set_trace()
            if succ==end:
                count = 1
                for i in paths:

                    for j in i:
                        if c_node[0][0] in i[i.index(j)] and i.index(j)==len(i) - 1:
                            for k in dict1[c_node[0][0]].keys():
                                if k==succ:
                                    paths[paths.index(i)].append((succ, dict1[c_node[0][0]][k]['distance'] /
                                                                  dict1[c_node[0][0]][k]['speed'],
                                                                  dict1[c_node[0][0]][k]['distance'],
                                                                  dict1[c_node[0][0]][k]['highway'],
                                                                  dict1[c_node[0][0]][k]['speed']))
                            temp_paths = paths
                            ans_path = i
                            count = 0
                            break

                        elif c_node[0][0] in i[i.index(j)] and i.index(j)!=len(i) - 1:
                            l = i[:i.index(j) + 1]
                            for k in dict1[c_node[0][0]].keys():
                                if k==succ:
                                    l.append((succ,
                                              dict1[c_node[0][0]][k]['distance'] / dict1[c_node[0][0]][k][
                                                  'speed'], dict1[c_node[0][0]][k]['distance'],
                                              dict1[c_node[0][0]][k]['highway'],
                                              dict1[c_node[0][0]][k]['speed']))
                            temp_paths = paths
                            temp_paths.append(l)
                            ans_path = l
                            count = 0
                            break
                    if count==0:
                        break

                paths = temp_paths
                total_time = 0
                total_dist = 0.0
                route_taken = []
                delivery_time = 0

                t_trip = 0
                for i in range(len(ans_path)):
                    # pdb.set_trace()
                    if i!=0:
                        delivery_time += delivery(start, ans_path[i - 1][0], ans_path[i][0], end, t_trip)[0][1]
                    t_trip += ans_path[i][1]

                for i in range(len(ans_path)):
                    total_time += ans_path[i][1]
                    total_dist += ans_path[i][2]
                    if i!=0:
                        route_taken.append((f'{ans_path[i][0]}', f'{ans_path[i][3]} for {ans_path[i][2]} miles'))

                return {"total-segments": len(route_taken),
                        "total-miles": total_dist,
                        "total-hours": total_time,
                        "total-delivery-hours": delivery_time,
                        "route-taken": route_taken}

            else:

                if succ not in visited_node:

                    count = 1

                    for i in paths:
                        for j in i:

                            if c_node[0][0] in i[i.index(j)] and i.index(j)==len(i) - 1:
                                for k in dict1[c_node[0][0]].keys():
                                    if k==succ:
                                        paths[paths.index(i)].append((succ, dict1[c_node[0][0]][k]['distance'] /
                                                                      dict1[c_node[0][0]][k]['speed'],
                                                                      dict1[c_node[0][0]][k]['distance'],
                                                                      dict1[c_node[0][0]][k]['highway'],
                                                                      dict1[c_node[0][0]][k]['speed']))
                                temp_paths = paths
                                t_trip_path = i
                                t_trip = 0
                                for i in t_trip_path[:-1]:
                                    t_trip += i[1]

                                hsgs = 0
                                for y in range(1, len(t_trip_path)):
                                    # pdb.set_trace()
                                    r = t_trip_path[y][0]
                                    s = t_trip_path[y - 1][0]
                                    infos, hs = cost_fn(cost, start, s, r, end, t_trip)
                                    hsgs += hs
                                infos1, hs1 = cost_fn(cost, start, c_node[0][0], succ, end, t_trip)
                                fringe.append((infos1, hsgs))

                                count = 0
                                break
                            elif c_node[0][0] in i[i.index(j)] and i.index(j)!=len(i) - 1:
                                l = i[:i.index(j) + 1]

                                for k in dict1[c_node[0][0]].keys():
                                    if k==succ:
                                        l.append((succ, dict1[c_node[0][0]][k]['distance'] /
                                                  dict1[c_node[0][0]][k]['speed'],
                                                  dict1[c_node[0][0]][k]['distance'],
                                                  dict1[c_node[0][0]][k]['highway'],
                                                  dict1[c_node[0][0]][k]['speed']))
                                temp_paths = paths
                                temp_paths.append(l)
                                t_trip_path = l
                                t_trip = 0
                                for i in t_trip_path[:-1]:
                                    t_trip += i[1]
                                hsgs = 0
                                for i in range(1, len(l)):
                                    r = l[i][0]
                                    s = l[i - 1][0]
                                    infos, hs = cost_fn(cost, start, s, r, end, t_trip)
                                    hsgs += hs
                                infos1, hs1 = cost_fn(cost, start, c_node[0][0], succ, end, t_trip)
                                fringe.append((infos1, hsgs))

                                count = 0
                                break
                        if count==0:
                            break
                    paths = temp_paths
                else:
                    continue

                visited_node.append(succ)


"""
    Find shortest driving route between start city and end city
    based on a cost function.

    1. Your function should return a dictionary having the following keys:
        -"route-taken" : a list of pairs of the form (next-stop, segment-info), where
           next-stop is a string giving the next stop in the route, and segment-info is a free-form
           string containing information about the segment that will be displayed to the user.
           (segment-info is not inspected by the automatic testing program).
        -"total-segments": an integer indicating number of segments in the route-taken
        -"total-miles": a float indicating total number of miles in the route-taken
        -"total-hours": a float indicating total amount of time in the route-taken
        -"total-delivery-hours": a float indicating the expected (average) time 
                                   it will take a delivery driver who may need to return to get a new package
    2. Do not add any extra parameters to the get_route() function, or it will break our grading and testing code.
    3. Please do not use any global variables, as it may cause the testing code to fail.
    4. You can assume that all test cases will be solvable.
    5. The current code just returns a dummy solution.
    """

# route_taken = [("Martinsville,_Indiana","IN_37 for 19 miles"),
#                ("Jct_I-465_&_IN_37_S,_Indiana","IN_37 for 25 miles"),
#                ("Indianapolis,_Indiana","IN_37 for 7 miles")]

# return {"total-segments" : len(route_taken),
#         "total-miles" : 51.,
#         "total-hours" : 1.07949,
#         "total-delivery-hours" : 1.1364,
#         "route-taken" : route_taken}

# Please don't modify anything below this line
#
if __name__=="__main__":
    if len(sys.argv)!=4:
        raise (Exception("Error: expected 3 arguments"))

    (_, start_city, end_city, cost_function) = sys.argv
    if cost_function not in ("segments", "distance", "time", "delivery"):
        raise (Exception("Error: invalid cost function"))

    result = get_route(start_city, end_city, cost_function)

    # Pretty print the route
    print("Start in %s" % start_city)
    for step in result["route-taken"]:
        print("   Then go to %s via %s" % step)

    print("\n          Total segments: %4d" % result["total-segments"])
    print("             Total miles: %8.3f" % result["total-miles"])
    print("             Total hours: %8.3f" % result["total-hours"])
    print("Total hours for delivery: %8.3f" % result["total-delivery-hours"])
