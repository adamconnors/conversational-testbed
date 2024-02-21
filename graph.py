import matplotlib.pyplot as plt

map = [
    [1, 2, 3],
    [2, 2, 3],
    [3, 3],
    [4, 4],
    [5, 5],
    [6, 7],
    [7, 14],
    [8, 20],
    [9, 21],
    [10, 10, 12],
    [11, 23],
    [12, 28],
    [13, 34],
    [14, 37],
    [15, 39],
    [16, 40],
    [17, 41],
    [18, 18, 28],
    [19, 18, 24],
    [20, 20],
    [21, 20],
    [22, 23],
    [24, 16],
    [25, 25],
    [26, 27, 39],
    [27, 34],
    [28, 35],
    [29, 37],
    [30, 36],
    [31, 36, 32],
    [32, 15],
    [33, 13],
    [34, 18],
    [35, 38],
    [36, 38],
    [37, 39],
    [38, 27, 28, 29],
    [39, 41],
    [40, 0],
]

for array in map:
    source = array[0]
    targets = array[1:]

    plt.plot([source] * len(targets), targets, 'o-')
    plt.title("Generated Plot Point Location vs Actual Plot Point Location")
    plt.xlabel("Generated Plot Point Location")
    plt.ylabel("Actual Plot Point Location")
plt.show()
