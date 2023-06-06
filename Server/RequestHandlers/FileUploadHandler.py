"""
GPL 3 file header
"""

from Server.ServerDataManager import ServerDataManager


class FileUploadHandler:
    # noinspection SpellCheckingInspection
    """
    Handle the FILEUPLOAD request.
    This will handle multipart file uploads
    """

    # noinspection PyUnusedLocal
    # noinspection PyMethodMayBeStatic
    def handleRequest(self, server, parameters: dict, data):
        filePath = parameters.get('filePath')[0]
        fullPath = ServerDataManager.getPathToDirectory(server, filePath)
        self.parseDataToFile(server, fullPath)
        return ''

    # noinspection PyMethodMayBeStatic
    def parseDataToFile(self, server, filePath):
        """
        Take all the file parts in the POST request and save them to a file
        """
        content_type = server.headers['content-type']
        assert content_type, "Content-Type header doesn't contain boundary"
        boundary = content_type.split("=")[1].encode()
        remainingBytes = int(server.headers['content-length'])
        line = server.rfile.readline()
        remainingBytes -= len(line)
        assert (boundary in line), "Content NOT begin with boundary"
        line = server.rfile.readline()
        remainingBytes -= len(line)
        line = server.rfile.readline()
        remainingBytes -= len(line)
        line = server.rfile.readline()
        remainingBytes -= len(line)
        out = open(filePath, 'wb')
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
                return
            else:
                out.write(nextLine)
                nextLine = line
        raise Exception("Unexpected Ends of data")
