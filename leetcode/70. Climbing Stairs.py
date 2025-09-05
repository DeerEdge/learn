class Solution:
    def climbStairs(self, n: int) -> int:
        if (n == 0): return 1
        elif (n == 1): return 1
        
        dp = [0] * (n + 1)
        dp[0] = 1
        dp[1] = 1

        for i in range(2, n + 1):
            dp[i] = dp[i-1] + dp[i-2]
        
        return dp[n]

        # Brute force solution
        if (n == 0): return 1
        elif (n == 1): return 1
        else:
            return self.climbStairs(n-1) + self.climbStairs(n-2)

        # Continuing input size: 
        # n = 4
        #
        # 1 + 1 + 1 + 1
        # 1 + 2 + 1
        # 1 + 1 + 2
        # 2 + 1 + 1
        # 2 + 2
        #
        # Total ways to climb to the top is 5. Follows the pattern of fib.
