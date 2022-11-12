# Reference(part from):
# 1. https://github.com/pratibha1708/Point-in-Polygon-App/blob/main/Report_PiP.pdf
# 2. Lecture 5 exercise 7
# 3. Week 5 practice notebook

# define point, lines and polygon from Lecture 5 exercise 7 solution[1]:

class point:
    def _init_(self,name,x,y):
        self._name = name
        self._x = x
        self._y = y
    def get_x(self):
        return self._x
    def get_y(self):
        return self._y
    def get_name(self):
        return self._name

class line(point):
    def _init_(self,name,point1,point2):
        super()._init_(name)
        self._point1 = point1
        self._point2 = point2
    def slop(self):
        if point.get_x(self._point2) != point.get_y(self._point1):
            slop = (point.get_y(self._point2) - point.get_y(self._point1)) / (point.get_x(self._point2) - point.get_y(self._point1))
        else: slop = 'This line is parallel to the x-axis'
        return slop
    def yinterept(self):
        b = point.get_y(self._point1) - line.slop(self) * point.get_y(self._point1)
        return b

class polygon(point):
    def _init_(self, name,points):
        super()._init_(name)
        self._points = points
    def get_points(self):
        return self._points
    def get_xs(self):
        x = []
        for point in self._points:
            x = x.append(point.get_x())
        return x
    def get_ys(self):
        y = []
        for point in self._points:
            y = y.append(point.get_y())
        return y
    def get_xmax(self):
        x = polygon.get_xs(self)
        xmax = x[0]
        for i in x:
            if x[i] > xmax:
               xmax = x[i]
            else: xmax = xmax
        return xmax
    def get_ymax(self):
        y = polygon.get_ys(self)
        ymax = y[0]
        for i in y:
            if y[i] > ymax:
                ymax = y[i]
            else: ymax = ymax
        return ymax
    def get_xmin(self):
        x = polygon.get_xs(self)
        xmin = x[0]
        for i in x:
            if x[i] < xmin:
               xmin = x[i]
            else: xmin = xmin
        return xmin
    def get_ymin(self):
        y = polygon.get_ys(self)
        ymin = y[0]
        for i in y:
            if y[i] > ymin:
                ymin = y[i]
            else: ymin = ymin
        return ymin
    def get_npoints(self):
        points = polygon.get_points(self)
        number = len(points)
        return number

# 1. Read a list of x, y coordinates from a comma-separated values (CSV) file and create a polygon object from them. The points are provided in clock-wise order[2];

print('Point in Polygon Test')
input_path = str(input('please insert the path of your points for testing file'))
def polygon_create(path):
    points = []
    with open(path,'r') as f:
        for lines in f.readlines():
            lines = lines.replace('\n','')
            name = lines[0]
            x = lines[1]
            y = lines[2]
            point = point(name,x,y)
            points.append(point)
    points = points[1:]
    return polygon('polygon',points)
polygon_test = polygon_create(input_path)

# 2. Read a list of x, y coordinates from a file and create a list of points objects for testing[2];

test_path = str(input('please insert the path of your points for testing file'))
def points_read(path):
    test_point = []
    with open(path, 'r') as f:
        for lines in f.readlines():
            lines = lines.replace('\n', '')
            name = lines[0]
            x = lines[1]
            y = lines[2]
            point = point(name, x, y)
            test_point.append(point)
    test_points = test_point[1:]
    return test_points
point_test = points_read(test_path)

# 3. Categorise these points and write into a file whether they are: “inside”,“outside”, or “boundary”;

# MBR:

def mbr(testpoints,polygon1):
    xmax = polygon.get_xmax(polygon1)
    ymax = polygon.get_ymax(polygon1)
    xmin = polygon.get_xmin(polygon1)
    ymin = polygon.get_ymin(polygon1)
    result = {}
    for testpoint in testpoints:
        if (point.get_x(testpoint) < xmin or point.get_x(testpoint) > xmax) and (point.get_y(testpoint) < ymin or point.get_x(testpoint) > ymax):
           test = 'outside'
        else: test = 'not know'
        a = (point.get_x(testpoint),point.get_y(testpoint))
        result['{a}'] = test
    return result
mbr_result = mbr(point_test,polygon_test)

# RCAA:

def rcaa(testpoints,polygon1):
    points = polygon.get_points(polygon1)
    n = polygon.get_npoints(polygon1)
    result = {}
    for testpoint in testpoints:
        count = 0
        x = point.get_x(testpoint)
        y = point.get_y(testpoint)
        K = []
        for i in range(n-2):
            a = line(i,points[i],points[i+1])
            k = line.slop(a)
            K[i] = k
            if k != 'This line is parallel to the x-axis':
                b = line.yinterept(a)
                test_y = k*x + b
                if point.get_y(points[i]) > point.get_y(points[i+1]):
                    ymax = point.get_y(points[i])
                    ymin = point.get_y(points[i+1])
                else:
                    ymax = point.get_y(points[i+1])
                    ymin = point.get_y(points[i])
                if test_y == y:
                    location = 'on the boundary'
                else:
                    if ymin < test_y < ymax:
                        count = count +1
                    elif ymin == test_y:
                        if (k > 0 and (K[i-1] < 0 or k == 'This line is parallel to the x-axis')) or (k < 0 and (K[i-1] > 0 or k == 'This line is parallel to the x-axis')):
                            count = count
                        else: count = count +1
                    else: count = count
            else:
                if ymin <= test_y <= ymax:
                    count = count + 1
                else: count = count
            if count%2 != 0:
                location = "inside"
            else: location = "outside"
        a = (point.get_x(testpoint), point.get_y(testpoint))
        result['{a}'] = location
    return result
rcaa_result = rcaa(point_test,polygon_test)

# 4. Plot the points and polygon in a plot window[3]

import matplotlib.pyplot as plt
from collections import OrderedDict

class Plotter:
    def __init__(self):
        plt.figure()
    def add_polygon(self, xs, ys):
        plt.fill(xs, ys, 'lightgray', label='Polygon')
    def add_point(self, x, y, kind=None):
        if kind == 'outside':
            plt.plot(x, y, 'ro', label='Outside')
        elif kind == 'boundary':
            plt.plot(x, y, 'bo', label='Boundary')
        elif kind == 'inside':
            plt.plot(x, y, 'go', label='Inside')
        else:
            plt.plot(x, y, 'ko', label='Unclassified')
    def show(self,type):
        handles, labels = plt.gca().get_legend_handles_labels()
        by_label = OrderedDict(zip(labels, handles))
        plt.legend(by_label.values(), by_label.keys())
        if type == 'mbr':
            plt.title('Points in Polygon MBR Result')
        elif type == 'racc':
            plt.title('Points in Polygon RCAA Result')
        else:
            print('Wrong Test type')
        plt.show()

plotter = Plotter()
plotter.add_polygon(polygon.get_xs(polygon_test), polygon.get_ys(polygon_test))
for key,value in mbr_result:
    (a,b) = key
    plotter.add_point(a, b, value)
plotter.show('mbr')

plotter = Plotter()
plotter.add_polygon(polygon.get_xs(polygon_test), polygon.get_ys(polygon_test))
for key,value in rcaa_result:
    (a,b) = key
    plotter.add_point(a, b, value)
plotter.show('racc')

# 5. Write the result of each point in a CSV file;

def output(path, test_result):
    with open(path, 'w') as f:
        f.write('(X,Y), test_result\n')
        for key, value in test_result():
            f.write('{key},{value}\n')


answer = input('Do you want to save your result?(y/n)')
if answer == 'y':
    mbr_output_path = str(input('please insert the path of your points MBR testing output'))
    rcaa_output_path = str(input('please insert the path of your points RCAA testing output'))
    output(mbr_output_path, mbr_result)
    output(rcaa_output_path, rcaa_result)
else:
    print('Thanks for using.')