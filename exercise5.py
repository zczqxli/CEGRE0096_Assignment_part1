a = [int(x) for x in input('please inset the numbers:').split()]
b = len(a)

def nmax(x):
    max = 0
    for i in range(x):
        if a[i] >= max:
            max = a[i]
        else: max = max
    return max

def nmin(x):
    min = a[0]
    for i in range(x):
        if a[i] <= min:
            min = a[i]
        else: min = min
    return min

def naverge(x):
    sum = 0
    for i in range(x):
        sum = sum + a[i]
    average = sum / x
    return average

def ndup(x):
    n_dictionary = {}
    for i in range(x):
        if a[i] not in n_dictionary.keys():
            n_dictionary[a[i]] = 1
        else:
            n_dictionary[a[i]] = n_dictionary[a[i]] + 1
    return n_dictionary

print("max",nmax(b))
print("min:",nmin(b))
print("duplicate number: time is:", ndup(b))
