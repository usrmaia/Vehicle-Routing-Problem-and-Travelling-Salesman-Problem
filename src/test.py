num_vertices = 10

route = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
i = 3
print(route[i])
j = 5
print(route[j])

route1 = route[:i]
route2 = route[i + 1 : j]
route3 = route[j + 1 :]

print(route1 + [route[j]] + route2 + [route[i]] + route3)
