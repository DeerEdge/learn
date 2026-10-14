
# PROBLEM: GPU Credit Manager
#
# Each GPU credit grant has:
# - amount: number of credits
# - timestamp: when credits become active
# - ttl: how long the credits remain valid
#
# Credits are active during [timestamp, timestamp + ttl).
#
# Implement:
# 1. add_credit(amount, timestamp, ttl)
# 2. get_balance(timestamp)
#
# Assume operation timestamps are nondecreasing.
# Amounts and TTLs are positive integers.
#
# EXAMPLE:
# gpu = GPUCredits()
# gpu.add_credit(100, 10, 20)
# gpu.add_credit(50, 15, 10)
#
# gpu.get_balance(20)  # 150
# gpu.get_balance(25)  # 100
# gpu.get_balance(30)  # 0
#
# FOLLOW-UPS (do not implement yet):
# Part 2: Spend credits, consuming earliest-expiring grants first.
# Part 3: Handle insufficient credits and possible debt.

from collections import defaultdict
class GPUCredits:
    def __init__(self):
        self.records = []
        self.debt = 0

    def add_credit(self, amount, timestamp, ttl):
        # if self.records["GPU 1"]:
        #     prev_amount, prev_start, prev_expiry = self.records["GPU 1"][-1]
        #     if prev_expiry > timestamp:
        #         amount += prev_amount
        filled = min(self.debt, amount)
        if self.debt > 0:
            self.debt -= filled
            amount -= filled

        if amount > 0:
            self.records.append((amount, timestamp, timestamp + ttl))

    def get_balance(self, timestamp):
        balance = 0

        for amount, start, expiry in self.records:
            if start <= timestamp < expiry:
                balance += amount
       
        print(balance)
        return balance

    def spend(self, spend_amount, timestamp):
        if spend_amount < 0:
            return False

        if spend_amount == 0:
            return True
        
        # if self.get_balance(timestamp) < spend_amount:
        #     return False

        self.records.sort(key=lambda x: x[2])

        for i in range(len(self.records)):
            amount, start, expiry = self.records[i]

            if start <= timestamp < expiry:
                used = min(amount, spend_amount)
                self.records[i] = (amount - used, start, expiry)
                spend_amount -= used

        if spend_amount == 0:
            return True
        else:
            self.debt += spend_amount
            return True

        

# gpu = GPUCredits()

# gpu.add_credit(100, 10, 20)  # Expires at 30
# gpu.add_credit(50, 15, 10)   # Expires at 25

# gpu.spend(70, 20)            # True
# gpu.get_balance(20)          # 80

# gpu.get_balance(25)          # 80
# gpu.get_balance(30)          # 0

# gpu.spend(100, 20)           # False, unchanged

gpu = GPUCredits()

# 1. Create debt
assert gpu.spend(100, 0) == True
assert gpu.get_balance(0) == 0
# Debt: 100

# 2. Partially repay debt
gpu.add_credit(40, 5, 10)      # Expires at 15
assert gpu.get_balance(5) == 0
# Debt: 60

# 3. Fully repay debt
gpu.add_credit(100, 10, 20)    # Expires at 30
assert gpu.get_balance(10) == 40
# Debt: 0

# 4. Add another grant
gpu.add_credit(50, 12, 8)      # Expires at 20
assert gpu.get_balance(12) == 90

# 5. Spend 60, earliest expiry first
assert gpu.spend(60, 13) == True
assert gpu.get_balance(13) == 30

# Expected remaining:
# Grant expiring at 20: 0
# Grant expiring at 30: 30

# 6. Spend more than available
assert gpu.spend(50, 14) == True
assert gpu.get_balance(14) == 0
assert gpu.debt == 20

# 7. New credits repay debt
gpu.add_credit(70, 16, 10)
assert gpu.get_balance(16) == 50
assert gpu.debt == 0

# 8. Credits expire
assert gpu.get_balance(26) == 0

print("passed the freaking tests")