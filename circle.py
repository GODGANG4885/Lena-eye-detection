from PIL import Image, ImageDraw
from math import pi, cos, sin
from canny import canny_edge_detector
from collections import defaultdict

# Load image:
input_image = Image.open("Lena.jpg")

# Output image:
output_image = Image.new("RGB", input_image.size)
output_image.paste(input_image)
draw_result = ImageDraw.Draw(output_image)

# Find circles
rmin = 7
rmax = 15
steps = 360
threshold = 0.44

points = []
for r in range(rmin, rmax + 1):
    for t in range(steps):
        points.append((r, int(r * cos(2 * pi * t / steps)), int(r * sin(2 * pi * t / steps))))

acc = defaultdict(int)
for x, y in canny_edge_detector(input_image):
    for r, dx, dy in points:
        a = x - dx
        b = y - dy
        acc[(a, b, r)] += 1

circles = []
for k, v in sorted(acc.items(), key=lambda i: -i[1]):
    x, y, r = k                     # not include in pre-circles
    if v / steps >= threshold and all((x - xc) ** 2 + (y - yc) ** 2 > rc ** 2 for xc, yc, rc in circles):
        # print(v / steps, x, y, r)
        circles.append((x, y, r))

circles.sort(key=lambda element: element[1])
selectCircles = []
eyes = []
# pixel_y in range(10)
print(circles)
for i in range(0,len(circles)-1):
    for j in range(i+1,len(circles)):
        if(circles[j][1] - circles[i][1] < 10):
            if circles[i] not in selectCircles:
                selectCircles.append(circles[i])
            if circles[j] not in selectCircles:
                selectCircles.append(circles[j])

# select pair circle // pixel_x in range (30,70)
selectCircles.sort(key=lambda element: element[0])
print(selectCircles)
for i in range(0, len(selectCircles)-1):
    for j in range(i+1, len(selectCircles)):
        if ((50 < selectCircles[j][0] - selectCircles[i][0]) and ((selectCircles[j][0] - selectCircles[i][0]) < 70)):
                if selectCircles[i] not in eyes:
                    eyes.append(selectCircles[i])
                if selectCircles[j] not in eyes:
                    eyes.append(selectCircles[j])

print(eyes)
# Draw circle on image
for x, y, r in eyes:
    draw_result.ellipse((x-r, y-r, x+r, y+r), outline=(255,0,0,0))

# Save output image
output_image.save("test1.jpg")
