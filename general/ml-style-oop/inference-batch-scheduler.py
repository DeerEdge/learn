
# ================================================================
# ML INFERENCE BATCH SCHEDULER
# Difficulty: Medium
# Patterns: Greedy, Queues, Event-Driven Simulation
# Context: ML Systems / GPU Inference
# ================================================================
#
# You are implementing a batch scheduler for an ML inference server.
#
# The server receives inference requests at different timestamps.
# To improve GPU utilization, requests can be grouped into batches
# and processed together.
#
# Your job is to determine WHEN each batch should be dispatched
# and WHICH requests belong to each batch.
#
# INPUTS:
#
# requests: list[int]
#     A sorted list of integer request arrival times.
#     Multiple requests may arrive at the same timestamp.
#
# batch_size: int
#     Maximum number of requests allowed in one batch.
#     Guaranteed to be >= 1.
#
# max_wait: int
#     Maximum number of time units the oldest request in a
#     pending batch may wait.
#     Guaranteed to be >= 0.
#
# RULES:
#
# 1. Requests must be processed in arrival order (FIFO).
#
# 2. A batch must be dispatched as soon as EITHER:
#       a. The batch contains exactly batch_size requests.
#       b. The oldest pending request has waited max_wait units.
#
# 3. A batch may contain fewer than batch_size requests if
#    its waiting-time limit is reached.
#
# 4. Dispatching is instantaneous. There is no GPU execution
#    duration or processing delay.
#
# 5. Requests arriving at the exact dispatch timestamp must
#    be included before deciding whether to dispatch, subject
#    to batch_size.
#
# 6. Once a batch is dispatched, the next pending request
#    starts a new batch with its own waiting-time deadline.
#
# 7. If no requests are pending, jump directly to the next
#    arrival time. Do not simulate every individual time unit.
#
# OUTPUT:
#
# Return a list of tuples:
#
#     (dispatch_time, batch)
#
# where batch is a list of request arrival timestamps.
#
# EXAMPLE 1:
#
# requests = [0, 1, 2, 7, 8, 15]
# batch_size = 3
# max_wait = 4
#
# Output:
# [
#     (2,  [0, 1, 2]),
#     (11, [7, 8]),
#     (19, [15])
# ]
#
# Explanation:
# - Requests 0, 1, 2 form a full batch at t=2.
# - Requests 7, 8 remain pending until t=11.
# - Request 15 times out at t=19.
#
# EXAMPLE 2:
#
# requests = [0, 10, 20]
# batch_size = 2
# max_wait = 3
#
# Output:
# [
#     (3,  [0]),
#     (13, [10]),
#     (23, [20])
# ]
#
# EXAMPLE 3:
#
# requests = [1, 1, 1, 1]
# batch_size = 2
# max_wait = 5
#
# Output:
# [
#     (1, [1, 1]),
#     (1, [1, 1])
# ]
#
# EXAMPLE 4:
#
# requests = [0, 2, 2, 5]
# batch_size = 3
# max_wait = 2
#
# Output:
# [
#     (2, [0, 2, 2]),
#     (7, [5])
# ]
#
# CONSTRAINTS:
#
# 1 <= len(requests) <= 100000
# 0 <= requests[i] <= 10**9
# 1 <= batch_size <= 100000
# 0 <= max_wait <= 10**9
# requests is sorted in nondecreasing order.
#
# FOLLOW-UP QUESTIONS:
#
# 1. How would you handle requests arriving out of order?
# 2. What changes if requests have different model IDs and
#    only requests for the same model can share a batch?
# 3. What changes if GPU execution takes nonzero time?
# 4. How would you handle different priorities or deadlines?
#
# ================================================================

def scheduleBatches(requests: list[int], batch_size: int, max_wait: int):
    out = []
    batch = []

    for time in requests:
        if batch and time > batch[0] + max_wait:
            out.append((batch[0] + max_wait, batch))
            batch = []

        batch.append(time)

        if len(batch) == batch_size:
            out.append((time, batch))
            batch = []

    if batch:
        out.append((batch[0] + max_wait, batch))

    return out

requests = [0, 2, 2, 5]
batch_size = 3
max_wait = 2
print(scheduleBatches(requests,
                      batch_size,
                      max_wait))