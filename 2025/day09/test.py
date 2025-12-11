class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __repr__(self):
        return f"({self.x}, {self.y})"
    def __hash__(self):
        return hash((self.x, self.y))

# Checking if a point is inside a polygon
def point_in_polygon(point, polygon):
    num_vertices = len(polygon)
    x, y = point.x, point.y
    inside = False

    # Store the first point in the polygon and initialize the second point
    p1 = polygon[0]

    # Loop through each edge in the polygon
    for i in range(1, num_vertices + 1):
        # Get the next point in the polygon
        p2 = polygon[i % num_vertices]

        # Check if the point is above the minimum y coordinate of the edge
        if y > min(p1.y, p2.y):
            # Check if the point is below the maximum y coordinate of the edge
            if y <= max(p1.y, p2.y):
                # Check if the point is to the left of the maximum x coordinate of the edge
                if x <= max(p1.x, p2.x):
                    # Calculate the x-intersection of the line connecting the point to the edge
                    x_intersection = (y - p1.y) * (p2.x - p1.x) / (p2.y - p1.y) + p1.x

                    # Check if the point is on the same line as the edge or to the left of the x-intersection
                    if p1.x == p2.x or x <= x_intersection:
                        # Flip the inside flag
                        inside = not inside

        # Store the current point as the first point for the next iteration
        p1 = p2

    # Return the value of the inside flag
    return inside

# Driver code
if __name__ == "__main__":
    # Define a point to test
    points_to_test = [
        Point(x, y)
        for (x, y) in [
            # points found not found by part2.py
            (8, 2), # inside
            (2, 1),
            (9, 2), # inside
            (7, 7),
            (2, 6),
            (10, 6), # inside
            (9, 3), # inside
            (3, 4), # inside
        ]
    ]

    # Define a polygon
    polygon = [
        Point(7,1),
        Point(11,1),
        Point(11,7),
        Point(9,7),
        Point(9,5),
        Point(2,5),
        Point(2,3),
        Point(7,3),
    ]

    result = []
    for point in points_to_test:
        # Check if the point is inside the polygon
        if point in polygon or point_in_polygon(point, polygon):
            result.append(point)
            print("Point", point, "is inside the polygon")

    print(result)
        # else:
        #     print("Point", point, "is outside the polygon")
