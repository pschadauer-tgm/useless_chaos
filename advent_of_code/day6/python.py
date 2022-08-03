file = open("input.txt")
nums = [int(x) for x in file.readlines()[0].split(",")]
from collections import Counter
nums = Counter(nums)


for _ in range(256):
    nums[9] = nums[0]
    nums[7] += nums[0]
    nums[0] = 0
    for i in range(9):
        nums[i] = nums[i+1]
    nums[9] = 0

print(sum([nums[i] for i in range(9)]))
