def reward_function(params):

    if params['is_offtrack']:
        return float(-70)

    center_variance = params["distance_from_center"] / params["track_width"]


    s1 = list(range(11)) # center
    s1_2 = list(range(11, 25)) # rechts
    s2 = list(range(25, 29)) # links
    s3 = list(range(29, 32)) # rechts
    s4 = list(range(32, 38)) # links
    s5 = list(range(38, 47)) # center
    s6 = list(range(47, 52)) # rechts
    s7 = list(range(52, 58)) # links
    s8 = list(range(58, 64)) # rechts
    s9 = list(range(64, 70)) # center
    s10 = list(range(70, 75)) # links
    s11 = list(range(75, 80)) # rechts
    s12 = list(range(80, 85)) # links

    #racing line
    left_lane = s2 + s4 + s7 + s10 + s12

    center_lane = s1 + s5 + s9

    right_lane = s1_2 + s3 + s6 + s8 + s11

    #Speed
    slow = list(range(24, 35)) + list(range(56, 72)) + list(range(77, 80)) # 1m/s

    reward = -21

    if params["closest_waypoints"][1] in left_lane and params["is_left_of_center"]:
        reward += 10
    elif params["closest_waypoints"][1] in right_lane and not params["is_left_of_center"]:
        reward += 10
    elif params["closest_waypoints"][1] in center_lane and center_variance < 0.4:
        reward += 10
    else:
        reward -= 10
    if params["closest_waypoints"][1] in slow:
        if params["speed"] == 1 :
            reward += 10
        else:
            reward -= 10
    else:
        if params["speed"] == 3 :
            reward += 10
        else:
            reward -= 10

    return float(reward)