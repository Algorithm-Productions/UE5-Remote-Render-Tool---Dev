def getProjectName(path):
    if not path:
        return ''

    splitPath = path.split("\\")
    if len(splitPath) == 0:
        return ''

    splitFile = splitPath[-1].split(".")
    if len(splitFile) == 0:
        return ''

    return splitFile[0]


print(getProjectName(r'D:\Projects\DingleStorageProject\DingleStorageProject.uproject'))