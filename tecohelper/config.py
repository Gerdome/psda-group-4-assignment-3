RIGHT = "CE:DB:55:5F:37:4E"
LEFT = "D2:E9:B3:C0:BC:BE"
HIP = "E5:05:6B:A0:49:4B"
RIGHT_OLD_MACS = [f"IMU c8:e7:19:be:c8:80",
                  f"IMU fb:81:8a:61:af:ef",
                  f"IMU fb:51:83:d4:9a:8c",
                  f"IMU fa:24:ac:f5:51:2e"]
LEFT_OLD = "fd:81:6a:2b:83:7d"
HIP_OLD = "d2:e9:b3:c0:bc:be"
RTLS = "70b3d587900101ad"
LEFT_SENSOR = f"IMU {LEFT}"
RIGHT_SENSOR = f"IMU {RIGHT}"
HIP_SENSOR = f"IMU {HIP}"
LEFT_SENSOR_OLD = f"IMU {LEFT_OLD}"
HIP_SENSOR_OLD = f"IMU {HIP_OLD}"
RTLS_SENSOR = f"RTLS {RTLS}"

LABELS = [
    'low-level.hand-extend:direction_of_extention',
    'low-level.take-piece:piece_direction_on_table',
    'low-level.drop-piece:bin_number',
    'low-level.hand-retract:hand_specification',
    'low-level.switch-hand:from_to_hand_spec',
    'movement.stand',
    'movement.walk'
]
