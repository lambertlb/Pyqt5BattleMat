# BattleMat

Make an electronic battle mat using python and PySide2

I did this as a learning experiment to learn Python and QT

This is basically a conversion of the ElectronicBattleMat project done in GWT

## Items to run
    BattleMatServer.py will start a web service in your local network. It will print the ip and host in console window
    BattleMat.py will start the python client.
    You can also use a browser as a client by choosing your address and port I.E. http://192.168.109.2:8080


## Dependencies
    Beside python 10 or later you will need the following items.
        I used these instead of newer ones because PyCharm gave fewer erroneous warnings
    pip install PySide2
    pip install event-bus

## Things of interest
I learned many things about Python and Qt while doing this project. Some of them were very painful.
So I thought I would enumerate them here to help others over the pain.

###  Asynchronous tasks
I wanted to centralize the handling of tasks
that take a while such as loading json data from a server or getting
images from the web. To do this I create a series of classes services/AsyncTasks.py.
They also manage a cache of images, so they ever have to be loaded just once from the web.
### How to handle Posts in a Python server
My web service is mostly driven be POST requests from my application.
For each request type I created a handler. These can be found under Server/RequestHandlers.
FileUploadHandler is the most complicated and deals with multipart uploads.
### Handling zooming sub images in a scene
QGraphicsScene has a lot of nice things for handling panning and zooming, but I have a lot of
issues with overlay images getting pixelated when zoomed. I solved this sub-classing QGraphicsItem
and doing al the painting by myself. You can find this under views/PogCanvas.
### Using mouse wheel to zoom image
view/BattleMatCanvas is a subclass of QGraphicsView and shows how I use the mouse wheel to zoom an image.

## Issues
### Hand Cursor
I have not figured out how to use a different cursor other than the hand when over the QGraphicsView.
if you do setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag) so that you can use the mouse
to pan the image you are stuck with the hand cursor. To not use this means you have to manually pan
the image and that becomes very complicated. Would be nice if I could just tell it what cursor to use.

## Software License
GPL 3
