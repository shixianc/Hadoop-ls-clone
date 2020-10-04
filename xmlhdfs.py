from lxml import etree
import datetime
import sys


def main():

    ### Development ###
    # fileName = "fsimage564.xml"
    # pathName = "/user/ec2-user"
    ### Production ###
    fileName = sys.argv[1]
    pathName = sys.argv[2]
    pathIndex = 0

    # Parse the input XML file
    tree = etree.parse(fileName)
    # Process path
    path = list(filter(None, pathName.split("/")))

    # Find all inodes
    inodes = tree.findall("//inode")
    nodeMap = {}  # maps inumber to node element object
    for inode in inodes:
        nodeMap[inode.find("id").text] = inode

    # Find root node inumber
    rootINumber = None
    for inode in inodes:
        if inode.find("name").text is None:
            rootINumber = inode.find("id").text
            break

    if rootINumber is None:
        print("Error in fsimage stucture.")

    # Find all directories
    directories = tree.findall("//directory")

    # Path finding
    parentINumber = rootINumber
    isFile = False
    Found = True
    while (pathIndex < len(path)):
        children = []
        for directory in directories:
            if directory.find("parent").text == parentINumber:
                childElements = directory.findall("child")
                for childElement in childElements:
                    children.append(childElement.text)
                break
        for child in children:
            inode = nodeMap[child]
            if inode.find("name").text == path[pathIndex]:
                parentINumber = child
                isFile = True if inode.find("type").text == "FILE" else False
                if isFile and pathIndex != len(path) - 1:
                    print("ls:", "'{}'".format(pathName),
                          ": No such file or directory")
                    return
                break
        else:
            Found = False
        pathIndex += 1

    if not Found:
        print("ls:", "'{}'".format(pathName), ": No such file or directory")
        return

    # If target is not file
    if not isFile:
        children = []
        for directory in directories:
            if directory.find("parent").text == parentINumber:
                childElements = directory.findall("child")
                for childElement in childElements:
                    children.append(nodeMap[childElement.text])
                break
        print("Found", len(children), "items")

        # Sort by file size
        dict = {}
        for child in children:
            elementType = child.find("type").text
            if elementType == "FILE":
                rawSize = child.findall("blocks/block/numBytes")
                size = 0
                for rs in rawSize:
                    size += int(rs.text)
                dict[child] = size
            else:
                dict[child] = 0
        # Sort the dict list by value
        sortedChildren = sorted(dict.items(), key=lambda x: x[1])

        # Format the results and then output
        for child, size in sortedChildren:
            elementType = child.find("type").text
            name = child.find("name").text
            rawPermission = child.find("permission").text
            permission = permissionConverter(rawPermission, elementType)
            rawTime = child.find("mtime").text
            date = dateConverter(rawTime)
            pathName = "" if pathName == "/" else pathName
            if elementType == "FILE":
                totalReplica = child.find("replication").text
                print("{:>10} {:>2} {:>8} {:>8} {:>10} {:>10} {:>5} {:>8}".format(permission[2], totalReplica, permission[0], permission[1], size,
                                                                                  date[0], date[1], pathName+"/"+name))
            else:
                print("{:>10} {:>2} {:>8} {:>8} {:>10} {:>10} {:>5} {:>8}".format(permission[2], "-", permission[0], permission[1], 0,
                                                                                  date[0], date[1], pathName+"/"+name))
    # Output for single file path
    else:
        child = nodeMap[parentINumber]
        elementType = child.find("type").text
        name = child.find("name").text
        rawPermission = child.find("permission").text
        permission = permissionConverter(rawPermission, elementType)
        rawTime = child.find("mtime").text
        date = dateConverter(rawTime)
        totalReplica = child.find("replication").text
        pathName = "" if pathName == "/" else pathName
        rawSize = child.findall("blocks/block/numBytes")
        size = 0
        for rs in rawSize:
            size += int(rs.text)
        print("{:>10} {:>2} {:>8} {:>8} {:>10} {:>10} {:>5} {:>8}".format(permission[2], totalReplica, permission[0], permission[1], size,
                                                                          date[0], date[1], pathName))

# Convert the unix time to datetime


def dateConverter(rawTime):
    dt = datetime.datetime.fromtimestamp(int(rawTime)/1e3)
    result = []
    month = "0" + str(dt.month) if dt.month < 10 else str(dt.month)
    day = "0" + str(dt.day) if dt.day < 10 else str(dt.day)
    hour = "0" + str(dt.hour) if dt.hour < 10 else str(dt.hour)
    minute = "0" + str(dt.minute) if dt.minute < 10 else str(dt.minute)
    result.append("{}-{}-{}".format(dt.year, month, day))
    result.append("{}:{}".format(hour, minute))
    return result

# Format the permission data


def permissionConverter(rawPermission, elementType):

    # Format permission mode bits
    data = rawPermission.split(":")
    decimal = data[2]
    modeBits = ""
    for i in range(len(decimal)):
        digit = int(decimal[i])
        binary = int("{0:b}".format(digit))
        index = 0
        curr = ""
        while binary != 0:
            isOne = binary & 1
            if (isOne):
                if index == 0:
                    curr = "x" + curr
                elif index == 1:
                    curr = "w" + curr
                else:
                    curr = "r" + curr
            else:
                curr = "-" + curr
            binary //= 10
            index += 1
        modeBits += curr
    if (elementType == "FILE"):
        modeBits = "-" + modeBits
    else:
        modeBits = "d" + modeBits
    return data[:2] + [modeBits]


if __name__ == "__main__":
    main()
