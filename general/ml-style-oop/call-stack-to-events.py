# PROBLEM: Convert Call-Stack Samples Into Events
#
# A CPU profiler periodically records snapshots of the functions currently
# executing. Each snapshot contains:
#   (timestamp, call_stack)
#
# The call stack is ordered from outermost to innermost function.
#
# Implement stack_samples_to_events(samples), which converts these snapshots
# into chronological START and END events.
#
# Each output event should have the format:
#   (timestamp, "START" or "END", function_name)
#
# RULES:
# 1. Assume no functions are running before the first snapshot.
# 2. Emit START events for newly appearing functions.
# 3. Emit END events for functions that disappear between snapshots.
# 4. END events must go from innermost to outermost function.
# 5. START events must go from outermost to innermost function.
# 6. Function names may repeat due to recursion.
# 7. Do not emit END events for functions still active in the final snapshot.
#
# EXAMPLE:
# samples = [
#     (1, ["main"]),
#     (2, ["main", "foo"]),
#     (3, ["main", "foo", "bar"]),
#     (5, ["main", "baz"])
# ]
#
# EXPECTED OUTPUT:
# [
#     (1, "START", "main"),
#     (2, "START", "foo"),
#     (3, "START", "bar"),
#     (5, "END", "bar"),
#     (5, "END", "foo"),
#     (5, "START", "baz")
# ]
#
# TARGET: O(total number of stack frames processed) time.

def stack_samples_to_events(samples):
    events = []
    prev = []

    for stamp, call_stack in samples:
        i = 0
        while i < min(len(prev), len(call_stack)):
            if prev[i] == call_stack[i]:
                i += 1
            else:
                break

        # END any missing ones
        for j in range(len(prev) - 1, i - 1, -1):
            events.append((stamp, "END", prev[j]))

        # START new ones
        for j in range(i, len(call_stack)):
            events.append((stamp, "START", call_stack[j]))

        prev = call_stack

    print(events)
    return events

samples = [
    (1, ["main"]),
    (2, ["main", "foo"]),
    (3, ["main", "foo", "bar"]),
    (5, ["main", "baz"])
]
res = stack_samples_to_events(samples)

        

        