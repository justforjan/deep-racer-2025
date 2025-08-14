import math
import numpy

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

    speed = 5 # params['speed']

    reward = speed

    x = params['x']
    y = params['y']
    pos = (x,y)
    heading = params['heading']
    waypoints = params['waypoints']
    closest_waypoints = sorted(params['closest_waypoints'])
    next_point = waypoints[closest_waypoints[1]]
    prev_point = waypoints[closest_waypoints[0]]
    wp_3 = waypoints[(closest_waypoints[1]+1) % len(waypoints)]
    target_point = next_point

    if dist2d(pos, prev_point) > dist2d(pos, next_point):
        target_point = wp_3

    track_direction = math.degrees(math.atan2(target_point[1]-y, target_point[0]-x))

    direction_diff = abs(heading-track_direction)
    direction_diff = 360 - direction_diff if direction_diff > 180 else direction_diff

    if direction_diff > 10:
        reward *= pow(1 - direction_diff/180, 4)

    vec_to_next_point = (next_point[0]-x, next_point[1]-y)
    vec_to_wp_3 = (wp_3[0]-x, wp_3[1]-y)

    turn_left = numpy.cross(vec_to_next_point, vec_to_wp_3) > 0

    return reward