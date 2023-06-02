"""
GPL 3 file header
"""

from Server.ServerDataManager import ServerDataManager


class FileUploadHandler:
    # noinspection PyUnusedLocal
    # noinspection PyMethodMayBeStatic
    def handleRequest(self, server, parameters: dict, data):
        filePath = parameters.get('filePath')[0]
        fullPath = ServerDataManager.getPathToDirectory(server, filePath)
        self.parseDataToFile(server, fullPath)
        return ''

    # noinspection PyMethodMayBeStatic
    def parseDataToFile(self, server, filePath):
        content_type = server.headers['content-type']
        if not content_type:
            return False, "Content-Type header doesn't contain boundary"
        boundary = content_type.split("=")[1].encode()
        remainingBytes = int(server.headers['content-length'])
        line = server.rfile.readline()
        remainingBytes -= len(line)
        if boundary not in line:
            return False, "Content NOT begin with boundary"
        line = server.rfile.readline()
        remainingBytes -= len(line)
        line = server.rfile.readline()
        remainingBytes -= len(line)
        line = server.rfile.readline()
        remainingBytes -= len(line)
        try:
            out = open(filePath, 'wb')
        except IOError:
            return False, "Can't create file to write, do you have permission to write?"

        nextLine = server.rfile.readline()
        remainingBytes -= len(nextLine)
        while remainingBytes > 0:
            line = server.rfile.readline()
            remainingBytes -= len(line)
            if boundary in line:
                nextLine = nextLine[0:-1]
                if nextLine.endswith(b'\r'):
                    nextLine = nextLine[0:-1]
                out.write(nextLine)
                out.close()
                return True, "File '%s' upload success!" % filePath
            else:
                out.write(nextLine)
                nextLine = line
        return False, "Unexpected Ends of data."
