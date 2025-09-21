class Solution:
    def mergeAlternately(self, word1: str, word2: str) -> str:
        min_length = min(len(word1), len(word2))
        max_length = max(len(word1), len(word2))
        merged = ""
        for i in range(min_length):
            merged += word1[i]
            merged += word2[i]
        
        for i in range(min_length, max_length):
            if len(word1) > len(word2):
                merged += word1[i]
            else:
                merged += word2[i]

        return merged
