class Solution:
    def findClosestNumber(self, nums: List[int]) -> int:
        closest = nums[0]
        for i in range(len(nums)):
            if abs(nums[i]) < abs(closest):
                closest = nums[i]
            elif abs(nums[i]) == abs(closest):
                closest = max(nums[i], closest)
        return closest
