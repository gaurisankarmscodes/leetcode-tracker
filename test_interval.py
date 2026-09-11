def get_interval_days(difficulty, revision_count):
    intervals = {
        "Hard": [7, 10, 14],
        "Medium": [10, 15, 20],
        "Easy": [14, 21, 28]
    }
    
    steps = intervals[difficulty]
    
    if revision_count <= len(steps):
        index = revision_count - 1
    else:
        index = len(steps) - 1
    
    return steps[index]


print(get_interval_days("Hard", 1))   # should print 7
print(get_interval_days("Hard", 2))   # should print 10
print(get_interval_days("Hard", 3))   # should print 14
print(get_interval_days("Hard", 5))   # should print 14 (capped)