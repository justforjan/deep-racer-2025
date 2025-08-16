import math
import numpy as np

#params1 = {
#    "all_wheels_on_track": bool,        # flag to indicate if the agent is on the track
#    "x": float,                            # agent's x-coordinate in meters
#    "y": float,                            # agent's y-coordinate in meters
#    "closest_objects": [int, int],         # zero-based indices of the two closest objects to the agent's current position of (x, y).
#    "closest_waypoints": [int, int],       # indices of the two nearest waypoints.
#    "distance_from_center": float,         # distance in meters from the track center
#    "is_crashed": bool,                 # Boolean flag to indicate whether the agent has crashed.
#    "is_left_of_center": bool,          # Flag to indicate if the agent is on the left side to the track center or not.
#    "is_offtrack": bool,                # Boolean flag to indicate whether the agent has gone off track.
#    "is_reversed": bool,                # flag to indicate if the agent is driving clockwise (True) or counter clockwise (False).
#    "heading": float,                      # agent's yaw in degrees
#    "objects_distance": [float, ],         # list of the objects' distances in meters between 0 and track_length in relation to the starting line.
#    "objects_heading": [float, ],          # list of the objects' headings in degrees between -180 and 180.
#    "objects_left_of_center": [bool, ], # list of Boolean flags indicating whether elements' objects are left of the center (True) or not (False).
#    "objects_location": [(float, float),], # list of object locations [(x,y), ...].
#    "objects_speed": [float, ],            # list of the objects' speeds in meters per second.
#    "progress": float,                     # percentage of track completed
#    "speed": float,                        # agent's speed in meters per second (m/s)
#    "steering_angle": float,               # agent's steering angle in degrees
#    "steps": int,                          # number steps completed
#    "track_length": float,                 # track length in meters.
#    "track_width": float,                  # width of the track
#    "waypoints": [(float, float), ]        # list of (x,y) as milestones along the track center
#}


def reward_function(params):

    def dist2d(pos1, pos2):
        return pow(
            pow(pos1[0]-pos2[0], 2) +
            pow(pos1[1]-pos2[1], 2), 0.5)

    speed = params['speed']

    reward = speed

    x = params['x']
    y = params['y']
    pos = (x,y)
    heading = params['heading']
    waypoints = params['waypoints']
    closest_waypoints = sorted(params['closest_waypoints'])
    next_point = waypoints[closest_waypoints[1]]
    prev_point = waypoints[closest_waypoints[0]]

    NR_OF_NEXT_WAYPOINTS = 10
    upcoming_wps = [waypoints[(next_point + i + 1) % len(waypoints)] for i in range(NR_OF_NEXT_WAYPOINTS) ]
    wp_3 = upcoming_wps[0]
    target_point = next_point

    if dist2d(pos, prev_point) > dist2d(pos, next_point):
        target_point = wp_3

    track_direction = math.degrees(math.atan2(target_point[1]-y, target_point[0]-x))

    direction_diff = abs(heading-track_direction)
    direction_diff = 360 - direction_diff if direction_diff > 180 else direction_diff

    DIRECTION_DIFF_THRESHOLD = 10
    if direction_diff > DIRECTION_DIFF_THRESHOLD:
        reward *= math.exp(-direction_diff/30)

    vec_to_next_point = (next_point[0]-x, next_point[1]-y)
    vec_to_upcoming_wps = [(wp[0] - x, wp[1] - y) for wp in upcoming_wps]

    # für jeden der nächsten NR_OF_NEXT_WAYPOINTS waypoints, ob der links oder rechts zum nächsten waypoint liegt
    turns_left_from_current_position = [np.cross(vec_to_next_point, vec) > 0 for vec in vec_to_upcoming_wps]

    # Für jedes aufeinanderfolgende 3-er Paar an Wegpunkten, ob man links oder rechts muss
    turns_left_from_previous_waypoint = [np.cross(vec_to_next_point, vec_to_upcoming_wps[0]) > 0]
    # Für jedes aufeinanderfolgende 3-er Paar an Wegpunkte die absolute Graddifferenz der beiden Vektoren.
    # In Komination mit turns_left_from_previous_waypoint kann man die Strecke nachvollziehen
    abs_degree_diff_for_each_waypoint = [direction_diff]

    for i in range(len(upcoming_wps) - 2):
        start = upcoming_wps[i]
        next_wp = upcoming_wps[i + 1]
        after_next_wp = upcoming_wps[i + 2]

        vec_next = (next_wp[0] - start[0], next_wp[1] - start[1])
        vec_after = (after_next_wp[0] - start[0], after_next_wp[1] - start[1])

        degree_next = math.degrees(math.atan2(vec_next[1], vec_next[0]))
        degree_after = math.degrees(math.atan2(vec_after[1], vec_after[0]))

        abs_degree_diff = abs(degree_next - degree_after)

        left = np.cross(vec_next, vec_after) > 0

        turns_left_from_previous_waypoint.append(left)
        abs_degree_diff_for_each_waypoint.append(abs_degree_diff)


    currently_turning_left = turns_left_from_current_position[0]

    # Nun könnte man berechnen, wie stark und wie lange die Kurve ist

    # Der wievielte Waypunkt von der aktuellen Position aus markiert das Ende der Kurve
    end_of_turn = 0
    TURN_THRESSHOLD = 5
    while (turns_left_from_previous_waypoint[end_of_turn] is currently_turning_left
           and abs_degree_diff_for_each_waypoint[end_of_turn] > TURN_THRESSHOLD
           and end_of_turn < len(turns_left_from_previous_waypoint)):
        end_of_turn += 1 + 2 # + 2, da man vom letzten Wegpunkt nur

    end_of_turn += 1 + closest_waypoints[0] # oder 1?
    end_of_turn = end_of_turn % len(waypoints)


    return float(reward)