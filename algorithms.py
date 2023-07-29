def find_min_missing_positive(nums):
    num_set = set(nums)
    min_positive = 1

    while min_positive in num_set:
        min_positive += 1

    return min_positive


print(find_min_missing_positive([10, -3, 5, 0, 1, 5, 3, 2]))
print(find_min_missing_positive([0, 3, 2, 1, 4]))
