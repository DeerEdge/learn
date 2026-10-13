# ============================================================
# CPU-CYCLE TIME SERIES ALIGNMENT
# Difficulty: Medium, with Medium-Hard follow-ups
# ============================================================
#
# Two CPU monitoring systems collect statistics at different
# timestamps. The measurements must be aligned to compare
# CPU behavior across the systems.
#
# Each time series contains sorted pairs:
#
#     (timestamp, value)
#
# Timestamps within each series are strictly increasing.
# Between any two adjacent samples, assume the value changes
# linearly.
#
#
# PART 1 — ALIGN MISALIGNED TIME SERIES
#
# Implement:
#
#     align_cpu_cycles(a, b)
#
# 1. Create a unified, sorted collection of timestamps from
#    both time series.
#
# 2. At each timestamp, determine the value of both series.
#
# 3. If a series has no sample at that timestamp, interpolate
#    linearly between its surrounding samples.
#
# 4. Only include timestamps within the sampled range of
#    BOTH series. Do not extrapolate.
#
# 5. Return:
#
#     [(timestamp, value_a, value_b), ...]
#
#
# EXAMPLE:
#
# a = [(0, 10.0), (10, 30.0), (20, 20.0)]
# b = [(5, 40.0), (15, 20.0)]
#
# Unified timestamps:
#     [0, 5, 10, 15, 20]
#
# Common supported time range:
#     [5, 15]
#
# Expected output:
# [
#     (5, 20.0, 40.0),
#     (10, 30.0, 30.0),
#     (15, 25.0, 20.0)
# ]
#
#
# EDGE CASES:
#
# - Empty input
# - Single measurement
# - No overlapping time range
# - Identical timestamps
# - Large timestamp gaps
# - Constant-valued segments
#
# PART 2 — FIXED-WIDTH WINDOWS (FOLLOW-UP)
#
# Extend your solution to support:
#
#     align_windows(a, b, window_size)
#
# Windows have the form:
#
#     [0, W), [W, 2W), [2W, 3W), ...
#
# For each window fully supported by BOTH series, compute
# the TIME-WEIGHTED AVERAGE value of each series.
#
# Return:
#
#     [(window_start, window_end, avg_a, avg_b), ...]
#
# Do not use nearest-neighbor sampling as a substitute for
# the average. Assume piecewise-linear signals.
#
# Discuss how to avoid rescanning the entire input for
# each window.
#
#
# PART 3 — DISCUSSION ONLY
#
# How would you modify this algorithm if:
#
# - Measurements arrive as live streams?
# - One series has missing or delayed samples?
# - Timestamp values can wrap around?
# - Windows need the maximum instead of average?
#
# ============================================================
from collections import defaultdict
def align_cpu_cycles(a, b):
    i = j = 0
    combined = []

    while i < len(a) or j < len(b):
        if i >= len(a):
            combined.append(b[j][0])
            j += 1
        elif j >= len(b):
            combined.append(a[i][0])
            i += 1
        else:
            if a[i][0] > b[j][0]:
                combined.append(b[j][0])
                j += 1
            elif b[j][0] > a[i][0]:
                combined.append(a[i][0])
                i += 1 
            else:
                combined.append(a[i][0])
                i += 1
                j += 1     

    print("COMBINED STAMP: ", combined)

    interpolated = []
    for time in combined:
        # a = [(0, 10.0), (10, 30.0), (20, 20.0)]
        # b = [(5, 40.0), (15, 20.0)]

        # need to add (5, 20.0), (15, 25.0) to a
        # need to add (10, 30.0) to b 
        first_a = a[0][0]
        last_a = a[-1][0]

        if time > first_a and time < last_a:
            for i in range(len(a)):
                print("iter_a: ", a[i][0])
                if a[i][0] == time:
                    continue
                if a[i][0] > time:
                    l_stamp, l_val = a[i - 1]
                    r_stamp, r_val = a[i]

                    slope = (r_val - l_val)/(r_stamp - l_stamp)
                    intercept = l_val - slope * l_stamp
                    m_val = slope * time + intercept
                    print("interp_a:", slope, intercept, m_val)
                    interpolated.append((time, m_val))
                    break

                    # (0, 10.0), (10, 30.0)
                    # slope = 2 
                    # b = y - mx
                    # y = mx + b 

        first_b = b[0][0]
        last_b = b[-1][0]

        if time > first_b and time < last_b:
            for j in range(len(b)):
                print("iter_b: ", a[i][0])
                if b[j][0] == time:
                    continue
                if a[j][0] > time:
                    l_stamp, l_val = b[j - 1]
                    r_stamp, r_val = b[j]

                    slope = (r_val - l_val)/(r_stamp - l_stamp)
                    intercept = l_val - slope * l_stamp
                    m_val = slope * time + intercept
                    print("interp_b:", slope, intercept, m_val)
                    interpolated.append((time, m_val))
                    break

        print("INTERPOLATED:", interpolated)

    map = defaultdict(list)
    for stamp, val in a:
        if stamp == combined[0] or stamp == combined[-1]: continue
        map[stamp].append(val)
    for stamp, val in interpolated:
            map[stamp].append(val)
    for stamp, val in b:
        if stamp == combined[0] or stamp == combined[-1]: continue
        map[stamp].append(val)

    out = []
    for key, value in map.items():
        tup = [key] + value
        out.append(tuple(tup))
    out.sort(key=lambda x: x[0])
    print(out)
    return out
    # Expected output:
# [
#     (5, 20.0, 40.0),
#     (10, 30.0, 30.0),
#     (15, 25.0, 20.0)
# ]

def align_windows(a, b, window_size):
    pass


# TEST — PART 1

a = [(0, 10.0), (10, 30.0), (20, 20.0)]
b = [(5, 40.0), (15, 20.0)]

assert align_cpu_cycles(a, b) == [
    (5, 20.0, 40.0),
    (10, 30.0, 30.0),
    (15, 25.0, 20.0)
]
