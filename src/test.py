num_vertices = 10

route = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
i = 1
print(route[i])
j = 4
print(route[j])

route1 = route[: i + 1]
print(route1)
route2 = route[j:i:-1]
print(route2)
route3 = route[j + 1 :]
print(route3)

print(route1 + route2 + route3)
