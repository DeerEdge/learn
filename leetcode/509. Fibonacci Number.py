class Solution:
    def fib(self, n: int) -> int:
        # Base Cases
        if (n == 0): return 0
        elif (n == 1): return 1
        
        # Intead of creating recursive calls we build from bottom up
        dp = [0] * (n + 1)
        dp[1] = 1
        dp[2] = 2

        for i in range(2, n + 1):
            dp[i] = dp[i-1] + dp[i-2]
        
        return dp[n]
