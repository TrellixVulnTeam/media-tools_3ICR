# -*- coding: utf-8 -*-

import math
import numpy as np
import random
import scipy
from scipy import signal
import time
import sys

def addNormalizedValues(arr, key, nkey):
    if len(arr) < 1:
        return arr
    values = [v[key] for v in arr]
    range = (min(values), max(values))
    for i, entry in enumerate(arr):
        arr[i][nkey] = norm(entry[key], range)
    return arr

def angleBetween(x1, y1, x2, y2):
    deltaX = x2 - x1
    deltaY = y2 - y1
    return math.degrees(math.atan2(deltaY, deltaX))

def bboxFromPoints(points):
    x_coordinates, y_coordinates = zip(*points)
    return (min(x_coordinates), min(y_coordinates), max(x_coordinates), max(y_coordinates))

# return the bounding box of a rotated rectangle
def bboxRotate(x, y, w, h, angle=45.0):
    cx, cy = (x + w * 0.5, y + h * 0.5)
    distanceToCorner = distance(cx, cy, cx-w*0.5, cy-h*0.5)
    tlX, tlY = translatePoint(cx, cy, distanceToCorner, 225+angle) # top left corner
    trX, trY = translatePoint(cx, cy, distanceToCorner, 315+angle) # top right corner
    brX, brY = translatePoint(cx, cy, distanceToCorner, 45+angle) # bottom right corner
    blX, blY = translatePoint(cx, cy, distanceToCorner, 135+angle) # bottom left corner
    xs = [tlX, trX, brX, blX]
    ys = [tlY, trY, brY, blY]
    minX = min(xs)
    minY = min(ys)
    maxX = max(xs)
    maxY = max(ys)
    return (minX, minY, maxX-minX, maxY-minY)

def ceilInt(n):
    return int(math.ceil(n))

def ceilToNearest(n, nearest):
    return 1.0 * math.ceil(1.0*n/nearest) * nearest

def distance(x1, y1, x2, y2):
    return math.hypot(x2 - x1, y2 - y1)

def ease(n, easingFunction="sin", exp=6, invert=False):

    if easingFunction.endswith("Invert"):
        easingFunction = easingFunction[:-6]
        invert = True

    if "^" in easingFunction:
        easingFunction, exp = easingFunction.split("^")
        exp = int(exp)

    if easingFunction == "sin":
        n = easeSinInOut(n)
    elif easingFunction == "quadIn":
        n = n ** 2
    elif easingFunction == "quadOut":
        n = n * (2.0 - n)
    elif easingFunction == "quadInOut":
        n = 2.0 * n * n if n < 0.5 else -1.0 + (4 - 2.0*n)*n
    elif easingFunction == "cubicIn":
        n = n ** 3
    elif easingFunction == "cubicOut":
        n = (n - 1.0)**3 + 1.0
    elif easingFunction == "cubicInOut":
        n = 4.0 * (n ** 3) if n < 0.5 else (n-1.0)*(2*n-2)*(2*n-2)+1
    elif easingFunction == "quartIn":
        n = n ** 4
    elif easingFunction == "quartOut":
        n = 1.0 - (n-1.0)**4
    elif easingFunction == "quartInOut":
        n = 8.0 * n**4 if n < 0.5 else 1.0 - 8.0 * (n-1.0)**4
    elif easingFunction == "quintIn":
        n = n ** 5
    elif easingFunction == "quintOut":
        n = 1.0 + (n - 1.0) ** 5
    elif easingFunction == "quintInOut":
        n = 16.0 * n**5 if n < 0.5 else 1.0 + 16.0 * (n-1.0)**5
    elif easingFunction == "expIn":
        n = n ** exp
    elif easingFunction == "expOut":
        n = 1.0 - (n-1.0)**exp if exp % 2 <= 0 else 1.0 + (n-1.0)**exp
    elif easingFunction == "expInOut":
        if exp % 2 <= 0:
            n = 2**(exp-1) * n**exp if n < 0.5 else 1.0 - 2**(exp-1) * (n-1.0)**exp
        else:
            n = 2**(exp-1) * n**exp if n < 0.5 else 1.0 + 2**(exp-1) * (n-1.0)**exp

    return n if invert is not True else 1.0-n

def easeSinInOut(n):
    return (math.sin((n+1.5)*math.pi)+1.0) / 2.0

def easeSinInOutBell(n):
    return (math.sin((2.0*n+1.5)*math.pi)+1.0) / 2.0

def findNextValue(arr, value, isSorted=True):
    nvalue = None
    if not isSorted:
        arr.sort()
    for v in arr:
        if v > value:
            nvalue = v
            break
    return nvalue

def findPeaks(data, distance=None, height=None, findMinima=True):
    values = np.array(data)
    maxima, _ = signal.find_peaks(values, distance=distance, height=height)
    if findMinima:
        ivaluses = np.negative(values) # invert values to get minima
        minima, _ = signal.find_peaks(ivaluses, distance=distance, height=height)
    # import matplotlib.pyplot as plt
    # plt.plot(values, color="blue")
    # plt.plot(maxima, values[maxima], "x", color="green")
    # plt.plot(minima, values[minima], "x", color="red")
    # plt.show()
    if findMinima:
        return (list(minima), list(maxima))
    else:
        return list(maxima)

def floorInt(n):
    return int(math.floor(n))

def formatClockTime(s):
    tString = time.strftime('%H:%M', time.gmtime(s))
    if tString.startswith("0"):
        tString = tString[1:]
    return tString

def formatDecimal(n, precision=1):
    return "{0}".format(str(round(n, precision) if n % 1 else int(n)))

def formatNumber(n):
    return "{:,}".format(n)

def formatSeconds(s, separator=":", retainHours=False, showDays=False):
    dayString = ''
    if showDays:
        secondsInADay = 24.0 * 60 * 60
        if s > secondsInADay:
            dayString = '%s%s' % (int(s / secondsInADay), separator)
            s = s % secondsInADay
            retainHours = True
    tString = time.strftime('%H:%M:%S', time.gmtime(s))
    if tString.startswith("00:") and not retainHours:
        tString = tString[3:]
    if separator != ":":
        tString = tString.replace(":", separator)
    return dayString + tString

def getRandomColor(seed=None):
    c = []
    for i in range(3):
        if seed is not None:
            random.seed(seed+i)
        c.append(random.randint(0, 255))
    return tuple(c)

def getScaledValue(originalValue, scaleAmount, anchor):
    distance = originalValue - anchor
    sdistance = distance * scaleAmount
    return (anchor + sdistance)

def getValue(d, key, default):
    return d[key] if key in d else default

def hex2rgb(hex):
  # "#FFFFFF" -> [255,255,255]
  return [int(hex[i:i+2], 16) for i in range(1,6,2)]

def isInt(string):
    answer = False
    try:
        if "." not in str(string) and "e" not in str(string):
            num = int(string)
            answer = True
    except ValueError:
        answer = False
    return answer

def isNumber(n):
    return isinstance(n, (int, float))

def lerp(ab, amount):
    a, b = ab
    return (b-a) * amount + a

def lerpEase(ab, amount, easingFunction="sinIn"):
    if easingFunction != "linear":
        amount = ease(amount, easingFunction)
    return lerp(ab, amount)

def lim(value, ab=(0, 1)):
    a, b = ab
    return max(a, min(b, value))

def logTime(startTime=None, label="Elapsed time"):
    if startTime is False:
        return False
    now = time.time()
    if startTime is not None:
        secondsElapsed = now - startTime
        timeStr = formatSeconds(secondsElapsed)
        print("%s: %s" % (label, timeStr))
    return now

def norm(value, ab, limit=False):
    a, b = ab
    n = 0.0
    if (b - a) != 0:
        n = 1.0 * (value - a) / (b - a)
    if limit:
        n = lim(n)
    return n

# normalize angle between -360 to 360
def normalizeAngle(degrees):
    # return degrees % 360.0 if degrees >= 0.0 else degrees % -360.0
    return degrees % 360.0

def parseFloat(string):
    return parseNumber(string, alwaysFloat=True)

def parseNumber(string, alwaysFloat=False):
    try:
        num = float(string)
        if "." not in str(string) and "e" not in str(string) and not alwaysFloat:
            num = int(string)
        return num
    except ValueError:
        return string

def parseNumbers(arr, keyExceptions=['id', 'identifier', 'uid']):
    for i, item in enumerate(arr):
        if isinstance(item, (list,)):
            for j, v in enumerate(item):
                arr[i][j] = parseNumber(v)
        else:
            for key in item:
                if key not in keyExceptions:
                    arr[i][key] = parseNumber(item[key])
    return arr

def parseTimeMs(string):
    t = timecodeToMs(string) if isinstance(string, str) else string
    return t

def piDigits():
    return [3,1,4,1,5,9,2,6,5,3,5,8,9,7,9,3,2,3,8,4,6,2,6,4,3,3,8,3,2,7,9,5,0,2,8,8,4,1,9,7,1,6,9,3,9,9,3,7,5,1,0,5,8,2,0,9,7,4,9,4,4,5,9,2,3,0,7,8,1,6,4,0,6,2,8,6,2,0,8,9,9,8,6,2,8,0,3,4,8,2,5,3,4,2,1,1,7,0,6,7,9,8,2,1,4,8,0,8,6,5,1,3,2,8,2,3,0,6,6,4,7,0,9,3,8,4,4,6,0,9,5,5,0,5,8,2,2,3,1,7,2,5,3,5,9,4,0,8,1,2,8,4,8,1,1,1,7,4,5,0,2,8,4,1,0,2,7,0,1,9,3,8,5,2,1,1,0,5,5,5,9,6,4,4,6,2,2,9,4,8,9,5,4,9,3,0,3,8,1,9,6,4,4,2,8,8,1,0,9,7,5,6,6,5,9,3,3,4,4,6,1,2,8,4,7,5,6,4,8,2,3,3,7,8,6,7,8,3,1,6,5,2,7,1,2,0,1,9,0,9,1,4,5,6,4,8,5,6,6,9,2,3,4,6,0,3,4,8,6,1,0,4,5,4,3,2,6,6,4,8,2,1,3,3,9,3,6,0,7,2,6,0,2,4,9,1,4,1,2,7,3,7,2,4,5,8,7,0,0,6,6,0,6,3,1,5,5,8,8,1,7,4,8,8,1,5,2,0,9,2,0,9,6,2,8,2,9,2,5,4,0,9,1,7,1,5,3,6,4,3,6,7,8,9,2,5,9,0,3,6,0,0,1,1,3,3,0,5,3,0,5,4,8,8,2,0,4,6,6,5,2,1,3,8,4,1,4,6,9,5,1,9,4,1,5,1,1,6,0,9,4,3,3,0,5,7,2,7,0,3,6,5,7,5,9,5,9,1,9,5,3,0,9,2,1,8,6,1,1,7,3,8,1,9,3,2,6,1,1,7,9,3,1,0,5,1,1,8,5,4,8,0,7,4,4,6,2,3,7,9,9,6,2,7,4,9,5,6,7,3,5,1,8,8,5,7,5,2,7,2,4,8,9,1,2,2,7,9,3,8,1,8,3,0,1,1,9,4,9,1,2,9,8,3,3,6,7,3,3,6,2,4,4,0,6,5,6,6,4,3,0,8,6,0,2,1,3,9,4,9,4,6,3,9,5,2,2,4,7,3,7,1,9,0,7,0,2,1,7,9,8,6,0,9,4,3,7,0,2,7,7,0,5,3,9,2,1,7,1,7,6,2,9,3,1,7,6,7,5,2,3,8,4,6,7,4,8,1,8,4,6,7,6,6,9,4,0,5,1,3,2,0,0,0,5,6,8,1,2,7,1,4,5,2,6,3,5,6,0,8,2,7,7,8,5,7,7,1,3,4,2,7,5,7,7,8,9,6,0,9,1,7,3,6,3,7,1,7,8,7,2,1,4,6,8,4,4,0,9,0,1,2,2,4,9,5,3,4,3,0,1,4,6,5,4,9,5,8,5,3,7,1,0,5,0,7,9,2,2,7,9,6,8,9,2,5,8,9,2,3,5,4,2,0,1,9,9,5,6,1,1,2,1,2,9,0,2,1,9,6,0,8,6,4,0,3,4,4,1,8,1,5,9,8,1,3,6,2,9,7,7,4,7,7,1,3,0,9,9,6,0,5,1,8,7,0,7,2,1,1,3,4,9,9,9,9,9,9,8,3,7,2,9,7,8,0,4,9,9,5,1,0,5,9,7,3,1,7,3,2,8,1,6,0,9,6,3,1,8,5,9,5,0,2,4,4,5,9,4,5,5,3,4,6,9,0,8,3,0,2,6,4,2,5,2,2,3,0,8,2,5,3,3,4,4,6,8,5,0,3,5,2,6,1,9,3,1,1,8,8,1,7,1,0,1,0,0,0,3,1,3,7,8,3,8,7,5,2,8,8,6,5,8,7,5,3,3,2,0,8,3,8,1,4,2,0,6,1,7,1,7,7,6,6,9,1,4,7,3,0,3,5,9,8,2,5,3,4,9,0,4,2,8,7,5,5,4,6,8,7,3,1,1,5,9,5,6,2,8,6,3,8,8,2,3,5,3,7,8,7,5,9,3,7,5,1,9,5,7,7,8,1,8,5,7,7,8,0,5,3,2,1,7,1,2,2,6,8,0,6,6,1,3,0,0,1,9,2,7,8,7,6,6,1,1,1,9,5,9,0,9,2,1,6,4,2,0,1,9,8]

def plotList(arr, keyX, keyY, highlight=None, size=4):
    from matplotlib import pyplot as plt
    x = [item[keyX] for item in arr]
    y = [item[keyY] for item in arr]
    if highlight is not None:
        values = unique([item[highlight] for item in arr])
        colors = [values.index(item[highlight]) for item in arr]
        plt.scatter(x, y, c=colors, s=size)
    else:
        plt.scatter(x, y, s=size)
    plt.show()

def pseudoRandom(seed, range=(0, 1), isInt=False):
    random.seed(seed)
    value = random.random()
    value = lerp(range, value)
    if isInt:
        value = roundInt(value)
    return value

def resizeMatrix(mat, shape):
    mh = mat.shape[0]
    mw = mat.shape[1]
    resizedFp = np.zeros(shape, dtype=mat.dtype)
    h = shape[0]
    w = shape[1]
    for y in range(h):
        for x in range(w):
            ny = 1.0 * y / (h-1.0)
            nx = 1.0 * x / (w-1.0)
            i = roundInt(ny * (mh-1))
            j = roundInt(nx * (mw-1))
            resizedFp[y, x] = mat[i, j]
    return resizedFp

def roundToNearest(n, nearest):
    return 1.0 * round(1.0*n/nearest) * nearest

def roundInt(n):
    return int(round(n))

def timecodeToMs(tc):
    t = tuple([float(v) for v in tc.split(":")])
    hours = minutes = seconds = 0
    if len(t)==3:
        hours, minutes, seconds = t
    elif len(t)==2:
        minutes, seconds = t
    seconds = seconds + minutes * 60 + hours * 3600
    return roundInt(seconds*1000)

# East = 0 degrees
def translatePoint(x, y, distance, angle, radians=False):
    rad = angle if radians else math.radians(angle)
    x2 = x + distance * math.cos(rad)
    y2 = y + distance * math.sin(rad)
    return (x2, y2)

def unique(arr):
    return list(set(arr))

def weightedMean(values, weights=None):
    count = len(values)
    if count <= 0:
        return 0
    if weights is None:
        weights = [w**2 for w in range(count, 0, -1)]
    return np.average(values, weights=weights)

def weightedShuffle(arr, weights, count=None, seed=3):
    np.random.seed(seed)
    weightsSum = sum(weights)
    weights = [1.0*w/weightsSum for w in weights]
    return np.random.choice(arr, count, p=weights)
