
import collections
import itertools
from operator import itemgetter
from pprint import pprint
from lib.math_utils import *

def addIndices(arr, keyName="index", startIndex=0):
    for i, item in enumerate(arr):
        arr[i][keyName] = startIndex + i
    return arr

def createLookup(arr, key):
    return dict([(str(item[key]), item) for item in arr])

def containsList(bucketList, needleList):
    return set(needleList).issubset(set(bucketList))

def dequeue(arr, count):
    if count >= len(arr):
        return (arr, [])
    returnArr = arr[:count]
    remainder = arr[count:]
    return (returnArr, remainder)

def filterByQueryString(arr, queryString):
    return filterWhere(arr, parseFilterString(queryString))

def filterWhere(arr, filters):
    if isinstance(filters, tuple):
        filters = [filters]

    if len(arr) <= 0:
        return arr

    # Filter array
    for f in filters:
        mode = '='
        if len(f) == 2:
            key, value = f
        else:
            key, value, mode = f
        value = parseNumber(value)
        if mode == "<=":
            arr = [a for a in arr if key not in a or a[key] <= value]
        elif mode == ">=":
            arr = [a for a in arr if key not in a or a[key] >= value]
        elif mode == "<":
            arr = [a for a in arr if key not in a or a[key] < value]
        elif mode == ">":
            arr = [a for a in arr if key not in a or a[key] > value]
        elif mode == "~=":
            arr = [a for a in arr if key not in a or value in a[key]]
        elif mode == "!=":
            arr = [a for a in arr if key not in a or a[key] != value]
        elif mode == "!~=":
            arr = [a for a in arr if key not in a or value not in a[key]]
        else:
            arr = [a for a in arr if key not in a or a[key] == value]

    return arr

def findWhere(arr, filters):
    results = filterWhere(arr, filters)
    if len(results) < 1:
        return None
    else:
        return results[0]

def flattenList(arr):
    return [item for sublist in arr for item in sublist]

def getCounts(arr, key):
    counter = collections.Counter([v[key] for v in arr])
    return counter.most_common()

def getDuplicates(arr):
    return [item for item, count in collections.Counter(arr).items() if count > 1]

def groupList(arr, groupBy, sort=False, desc=True):
    groups = []
    arr = sorted(arr, key=itemgetter(groupBy))
    for key, items in itertools.groupby(arr, key=itemgetter(groupBy)):
        group = {}
        litems = list(items)
        count = len(litems)
        group[groupBy] = key
        group["items"] = litems
        group["count"] = count
        groups.append(group)
    if sort:
        reversed = desc
        groups = sorted(groups, key=lambda k: k["count"], reverse=reversed)
    return groups

def listToHumanString(arr):
    arr = [str(value).strip() for value in arr]
    arrLen = len(arr);
    if arrLen < 1:
        return "Unknown";
    if arrLen < 2:
        return arr[0]
    if arrLen < 3:
        return ' and '.join(arr)

    string = ''
    for i, value in enumerate(arr):
        if i == arrLen-1:
            string += value
        elif i == arrLen-2:
            string += (value + ', and ')
        else:
            string += (value + ', ')
    return string

def listToTupleList(arr):
    it = iter(arr)
    return zip(it, it)

def parseFilterString(str):
    if len(str) <= 0:
        return []
    conditionStrings = str.split("&")
    conditions = []
    modes = ["<=", ">=", "~=", "!=", "!~=", ">", "<", "="]
    for cs in conditionStrings:
        for mode in modes:
            if mode in cs:
                parts = cs.split(mode)
                parts.append(mode)
                conditions.append(tuple(parts))
                break
    return conditions

def parseQueryString(str, doParseNumbers=False):
    if len(str) <= 0:
        return {}
    conditionStrings = str.split("&")
    conditions = {}
    for cs in conditionStrings:
        key, value = tuple(cs.split("="))
        if doParseNumbers:
            value = parseNumber(value)
        conditions[key] = value
    return conditions

def parseSortString(str):
    if len(str) <= 0:
        return []
    conditionStrings = str.split("&")
    conditions = []
    for cs in conditionStrings:
        if "=" in cs:
            parts = cs.split("=")
            conditions.append(tuple(parts))
        else:
            conditions.append((cs, "asc"))
    return conditions

def prependAll(arr, prepends):
    if isinstance(prepends, tuple):
        prepends = [prepends]

    for i, item in enumerate(arr):
        for p in prepends:
            newKey = None
            if len(p) == 3:
                key, value, newKey = p
            else:
                key, value = p
                newKey = key
            arr[i][newKey] = value + item[key]

    return arr

def sortBy(arr, sorters, targetLen=None):
    if isinstance(sorters, tuple):
        sorters = [sorters]

    if len(arr) <= 0:
        return arr

    # Sort array
    for s in sorters:
        trim = 1.0
        if len(s) > 2:
            key, direction, trim = s
            trim = float(trim)
        else:
            key, direction = s
        reversed = (direction == "desc")

        arr = sorted(arr, key=lambda k: k[key], reverse=reversed)

        if 0.0 < trim < 1.0:
            count = int(round(len(arr) * trim))
            if targetLen is not None:
                count = max(count, targetLen)
            arr = arr[:count]

    if targetLen is not None and len(arr) > targetLen:
        arr = arr[:targetLen]

    return arr

def sortByQueryString(arr, sortString, targetLen=None):
    sorters = parseSortString(sortString)

    if len(sorters) <= 0:
        return arr

    return sortBy(arr, sorters, targetLen)

def sortMatrix(arr, sortY, sortX, rowCount):
    count = len(arr)
    cols = ceilInt(1.0 * count / rowCount)
    arr = sortBy(arr, sortY)
    arrSorted = []
    for col in range(cols):
        i0 = col * rowCount
        i1 = min(i0 + rowCount, count)
        row = sortBy(arr[i0:i1], sortX)
        arrSorted += row
    return arrSorted

def updateAll(arr, updates):
    if isinstance(updates, tuple):
        updates = [updates]

    for i, item in enumerate(arr):
        for u in updates:
            key, value = u
            arr[i][key] = value

    return arr

def unionLists(arr1, arr2):
    if containsList(arr1, arr2):
        return arr1

    elif containsList(arr2, arr1):
        return arr2

    else:
        set1 = set(arr1)
        for v in arr2:
            if v not in set1:
                arr1.append(v)
        return arr1
