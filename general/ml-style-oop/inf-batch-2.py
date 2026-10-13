
# ================================================================
# ML INFERENCE BATCH SCHEDULER — FOLLOW-UP
# Patterns: Hash Maps, Heaps, Greedy, Event-Driven Simulation
# ================================================================
#
# You operate ONE GPU that serves inference requests for multiple
# ML models. Requests for different models CANNOT share a batch.
#
# Implement:
#   schedule_batches(requests, batch_size, max_wait, gpu_time)
#
#
# INPUTS:
#
# requests: list[tuple[int, str]]
#   Each request is (arrival_time, model_id).
#   Requests are sorted by nondecreasing arrival time.
#   Multiple requests can arrive at the same timestamp.
#   Each request has a unique ID equal to its index in requests.
#
# batch_size: int
#   Maximum number of requests in one batch.
#
# max_wait: int
#   Maximum time the oldest request can wait for batch formation.
#
# gpu_time: int
#   Time required for the GPU to execute one batch.
#   Execution time is independent of batch size.
#
#
# RULES:
#
# 1. Each model maintains its own pending FIFO batch.
#
# 2. A batch becomes READY when either:
#      a. It reaches batch_size requests.
#      b. Its oldest request has waited max_wait units.
#
# 3. If a request arrives exactly at a batch's timeout deadline,
#    process the arrival before deciding whether to dispatch.
#
# 4. Once a batch becomes ready, it closes permanently.
#    New requests for that model start a new batch.
#
# 5. Only ONE batch can execute on the GPU at a time.
#
# 6. Among ready batches, execute the batch with the earliest
#    READY time first.
#
#    If multiple batches have the same ready time, prioritize
#    the batch with the smallest request ID.
#
# 7. GPU execution is non-preemptive.
#    Once a batch starts, it runs to completion.
#
# 8. The GPU may be busy when a batch becomes ready.
#    The batch must wait until the GPU is available.
#
# 9. max_wait applies to BATCH FORMATION, not GPU execution.
#    A batch can wait longer before actually running.
#
# 10. Do NOT simulate time unit by unit.
#     Use event-driven processing.
#
#
# OUTPUT:
#
# Return a list of tuples:
#
#   (start_time, finish_time, model_id, [request_ids])
#
# Ordered by actual GPU execution start time.
#
#
# EXAMPLE 1:
#
# requests = [(0, "A"), (1, "B"), (2, "A"), (3, "B")]
# batch_size = 2
# max_wait = 5
# gpu_time = 3
#
# Model A:
#   Request 0 arrives at t=0.
#   Request 2 arrives at t=2.
#   Batch reaches capacity at t=2.
#
# Model B:
#   Request 1 arrives at t=1.
#   Request 3 arrives at t=3.
#   Batch reaches capacity at t=3.
#
# GPU schedule:
#   Model A executes from t=2 to t=5.
#   Model B executes from t=5 to t=8.
#
# Expected:
# [
#     (2, 5, "A", [0, 2]),
#     (5, 8, "B", [1, 3])
# ]
#
#
# EXAMPLE 2:
#
# requests = [
#     (0, "A"),
#     (1, "B"),
#     (2, "A"),
#     (2, "B"),
#     (5, "A")
# ]
#
# batch_size = 3
# max_wait = 2
# gpu_time = 4
#
# At t=2:
#   Model A's batch [0, 2] times out.
#
# At t=3:
#   Model B's batch [1, 3] times out.
#
# At t=7:
#   Model A's second batch [4] times out.
#
# GPU scheduling:
#   Batch A1 executes from t=2 to t=6.
#   Batch B1 executes from t=6 to t=10.
#   Batch A2 executes from t=10 to t=14.
#
# Expected:
# [
#     (2, 6, "A", [0, 2]),
#     (6, 10, "B", [1, 3]),
#     (10, 14, "A", [4])
# ]
#
#
# EXAMPLE 3 — TIE BREAKING:
#
# requests = [(0, "B"), (0, "A")]
# batch_size = 1
# max_wait = 10
# gpu_time = 2
#
# Both batches are ready at t=0.
# Request ID 0 wins the tie.
#
# Expected:
# [
#     (0, 2, "B", [0]),
#     (2, 4, "A", [1])
# ]
#
#
# EDGE CASES TO CONSIDER:
#
# - No requests
# - batch_size = 1
# - max_wait = 0
# - Multiple models arriving simultaneously
# - Several batches becoming ready at the same timestamp
# - A GPU that remains busy while multiple batches become ready
# - Requests separated by extremely large time gaps
#
#
# CONSTRAINTS:
#
# 0 <= len(requests) <= 100000
# 0 <= arrival_time <= 10**9
# 1 <= batch_size <= 100000
# 0 <= max_wait <= 10**9
# 1 <= gpu_time <= 10**9
#
#
# OPTIONAL FOLLOW-UPS:
#
# 1. What if each model has a different GPU execution time?
# 2. What if there are two GPUs instead of one?
# 3. What if requests have priorities?
# 4. What if some batches have strict execution deadlines?
#
# ================================================================
from collections import defaultdict
def schedule_batches(
    requests: list[tuple[int, str]],
    batch_size: int,
    max_wait: int,
    gpu_time: int
) -> list[tuple[int, int, str, list[int]]]:
    if len(requests) == 0:
        return []
    
    models = defaultdict(list)
    batches = []

    for request_id, (arrival_time, model_id) in enumerate(requests):
        # processing stale requests
        model_batch = models[model_id]
        if model_batch and arrival_time > model_batch[0][0] + max_wait:
            batches.append((model_batch[0][0], model_batch[0][0] + max_wait, model_id, model_batch))  # (start_time, finish_time, model_id, [request_ids])
            models[model_id] = []

        models[model_id].append((arrival_time, request_id))
        model_batch = models[model_id]
        # what happens when a batch is full
        if model_batch and len(model_batch) == batch_size:
            batches.append((model_batch[0][0], arrival_time, model_id, model_batch))
            models[model_id] = []

    print(requests, "\n")
    print(batches, "\n")
    
    gpu_start = batches[0][1]

    # allocating gpu time
    for i in range(len(batches)):
        start, finish, id, ids = batches[i]
        batches[i] = (gpu_start, gpu_start + gpu_time, id, ids)
        gpu_start = gpu_start + gpu_time

    print("after gpu time", batches)


# arg

# TEST CASES

print(schedule_batches(
    [(0, "A"), (1, "B"), (2, "A"), (3, "B")],
    2, 5, 3
))
# Expected:
# [(2, 5, 'A', [0, 2]), (5, 8, 'B', [1, 3])]


print(schedule_batches(
    [(0, "A"), (1, "B"), (2, "A"), (2, "B"), (5, "A")],
    3, 2, 4 # b_size, wait, gpu time
))
# Expected:
# [(2, 6, 'A', [0, 2]),
#  (6, 10, 'B', [1, 3]),
#  (10, 14, 'A', [4])]


print(schedule_batches(
    [(0, "B"), (0, "A")],
    1, 10, 2
))
# Expected:
# [(0, 2, 'B', [0]), (2, 4, 'A', [1])]


print(schedule_batches([], 2, 3, 4))
# Expected: []
