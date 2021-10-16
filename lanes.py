"""
Lanes module for Froggit

This module contains the lane classes for the Frogger game. The lanes are the vertical
slice that the frog goes through: grass, roads, water, and the exit hedge.

Each lane is like its own level. It has hazards (e.g. cars) that the frog has to make
it past.  Therefore, it is a lot easier to program frogger by breaking each level into
a bunch of lane objects (and this is exactly how the level files are organized).

You should think of each lane as a secondary subcontroller.  The level is a subcontroller
to app, but then that subcontroller is broken up into several other subcontrollers, one
for each lane.  That means that lanes need to have a traditional subcontroller set-up.
They need their own initializer, update, and draw methods.

There are potentially a lot of classes here -- one for each type of lane.  But this is
another place where using subclasses is going to help us A LOT.  Most of your code will
go into the Lane class.  All of the other classes will inherit from this class, and
you will only need to add a few additional methods.

If you are working on extra credit, you might want to add additional lanes (a beach lane?
a snow lane?). Any of those classes should go in this file.  However, if you need additional
obstacles for an existing lane, those go in models.py instead.  If you are going to write
extra classes and are now sure where they would go, ask on Piazza and we will answer.

# YOUR NAME AND NETID HERE
# DATE COMPLETED HERE
"""
from game2d import *
from consts import *
from models import *

# PRIMARY RULE: Lanes are not allowed to access anything in any level.py or app.py.
# They can only access models.py and const.py. If you need extra information from the
# level object (or the app), then it should be a parameter in your method.

class Lane(object):         # You are permitted to change the parent class if you wish
    """
    Parent class for an arbitrary lane.

    Lanes include grass, road, water, and the exit hedge.  We could write a class for
    each one of these four (and we will have classes for THREE of them).  But when you
    write the classes, you will discover a lot of repeated code.  That is the point of
    a subclass.  So this class will contain all of the code that lanes have in common,
    while the other classes will contain specialized code.

    Lanes should use the GTile class and to draw their background.  Each lane should be
    GRID_SIZE high and the length of the window wide.  You COULD make this class a
    subclass of GTile if you want.  This will make collisions easier.  However, it can
    make drawing really confusing because the Lane not only includes the tile but also
    all of the objects in the lane (cars, logs, etc.)
    """
    # LIST ALL HIDDEN ATTRIBUTES HERE
    # Attribute _tile: A GTile object, the background image of the lane
    # Invariant: _tile is a GTile object

    # Attribute _objs: A list of lane obstacles if lane has obstacles
    # Invariant: _objs a list containing GImage objects or is empty

    # Attribute _speed: The speed (#pixels/sec) obstacles are moving in the lane
    # Invariat: _speed is set equal to zero if speed is specified in lane

    # Attribute _width: The width of a lane in grid squares
    # Invariant: _width is an int > 0

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getTile(self):
        """
        Returns tile object of the lane.
        """
        return self._tile


    # INITIALIZER TO SET LANE POSITION, BACKGROUND,AND OBJECTS
    def __init__(self,dict,lnnum,hbdict):
        """
        Initializes a Lane object.

        Parameter dict: A JSON dictionary containing information about the level
        Precondition: dict is a dictionary

        Parameter lnnum: A int representing the lane number, bottom/first = 0
        Precondition: lnnum is an int >= 0

        Parameter hbdict: A JSON dictionary with hitbox sizes for obstacles
        Precondition: hbdict is a dictionary
        """
        listlanes = dict['lanes']
        self._width = dict['size'][0]
        lane = dict['lanes'][lnnum]
        self._tile = GTile(source=listlanes[lnnum]['type']+'.png',\
        width=self._width*GRID_SIZE,height=GRID_SIZE)
        self._tile.bottom = lnnum*GRID_SIZE
        self._tile.left = 0
        self._speed = 0

        if 'objects' in lane:
            self._objs = []
            for pos in range(len(lane['objects'])):
                obst = GImage(source=lane['objects'][pos]['type']+'.png')
                obst.x = lane['objects'][pos]['position']*GRID_SIZE+GRID_SIZE/2
                obst.y = lnnum*GRID_SIZE + GRID_SIZE/2
                hitbox =hbdict['images'][lane['objects'][pos]['type']]['hitbox']
                obst.hitbox = hitbox
                if 'speed' in lane:
                    if lane['speed'] < 0:
                        obst.angle = 180
                    self._speed = lane['speed']
                self._objs.append(obst)
        else:
            self._objs = []

    # ADDITIONAL METHODS (DRAWING, COLLISIONS, MOVEMENT, ETC)
    def update(self,dt,buffer):
        """
        Updates and animates the obstacles within the lane.

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float) >= 0

        Parameter buffer: The distance that obstacles can move offscreen
        Precondition: buffer is a number > 0
        """
        dx = self._speed*dt
        buffer = buffer*GRID_SIZE

        for pos in range(len(self._objs)):
            self._objs[pos].x += dx
            x = self._objs[pos].x

            if self._speed < 0 and x < -buffer:
                d = -x - buffer
                self._objs[pos].x = self._width*GRID_SIZE+buffer-d
            elif self._speed >= 0 and x > self._width*GRID_SIZE+buffer:
                d = x - (self._width*GRID_SIZE+buffer)
                self._objs[pos].x = -buffer+d

    def draw(self, view):
        """
        Draws the GTile and obstacles within the lane.
        """
        self._tile.draw(view)

        if not self._objs is None:
           for obst in self._objs:
                obst.draw(view)


class Grass(Lane):                           # We recommend AGAINST changing this one
    """
    A class representing a 'safe' grass area.

    You will NOT need to actually do anything in this class.  You will only do anything
    with this class if you are adding additional features like a snake in the grass
    (which the original Frogger does on higher difficulties).
    """
    pass

    # ONLY ADD CODE IF YOU ARE WORKING ON EXTRA CREDIT EXTENSIONS.


class Road(Lane):                           # We recommend AGAINST changing this one
    """
    A class representing a roadway with cars.

    If you implement Lane correctly, you do really need many methods here (not even an
    initializer) as this class will inherit everything.  However, roads are different
    than other lanes as they have cars that can kill the frog. Therefore, this class
    does need a method to tell whether or not the frog is safe.
    """
    # DEFINE ANY NEW METHODS HERE
    def collide_car(self,frog):
        """
        Returns True if Frog collides with car.

        Parameter frog: A Frog object representing the frog in the game
        Precondition: frog is a Frog object
        """
        for objs in self._objs:
            if frog.getFrog().collides(objs):
                return True
        return False


class Water(Lane):
    """
    A class representing a waterway with logs.

    If you implement Lane correctly, you do really need many methods here (not even an
    initializer) as this class will inherit everything.  However, water is very different
    because it is quite hazardous. The frog will die in water unless the (x,y) position
    of the frog (its center) is contained inside of a log. Therefore, this class needs a
    method to tell whether or not the frog is safe.

    In addition, the logs move the frog. If the frog is currently in this lane, then the
    frog moves at the same rate as all of the logs.
    """
    # DEFINE ANY NEW METHODS HERE
    def on_log(self, frog):
        """
        Returns True if a log in the lane contains the frog.

        Parameter frog: A Frog object representing the frog in the game
        Precondition: frog is a Frog object
        """
        for obst in self._objs:
            if obst.contains((frog.getX(),frog.getY())):
                return True
        return False

    def move_frog_log(self,frog,dt):
        """
        Moves the frog along with the log.

        Method moves the frog the same distance (dx) that the log moves.

        Parameter frog: A Frog object representing the frog in the game
        Precondition: frog is a Frog object

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float) >= 0
        """
        dx = self._speed*dt
        frog.setX(frog.getX() + dx)


class Hedge(Lane):
    """
    A class representing the exit hedge.

    This class is a subclass of lane because it does want to use a lot of the features
    of that class. But there is a lot more going on with this class, and so it needs
    several more methods.  First of all, hedges are the win condition. They contain exit
    objects (which the frog is trying to reach). When a frog reaches the exit, it needs
    to be replaced by the blue frog image and that exit is now "taken", never to be used
    again.

    That means this class needs methods to determine whether or not an exit is taken.
    It also need to take the (x,y) position of the frog and use that to determine which
    exit (if any) the frog has reached. Finally, it needs a method to determine if there
    are any available exits at all; once they are taken the game is over.

    These exit methods will require several additional attributes. That means this class
    (unlike Road and Water) will need an initializer. Remember to user super() to combine
    it with the initializer for the Lane.
    """
    # LIST ALL HIDDEN ATTRIBUTES HERE
    # Attribute _usedexits: A list GImage exit objects that have been used.
    # Invariant: _usedexits is a list of GImage object

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getObjs(self):
        """
        Returns the list of obstacles in a Hedge lane.
        """
        return self._objs

    # INITIALIZER TO SET ADDITIONAL EXIT INFORMATION
    def __init__(self,dict,lnnum,hbdict):
        """
        Initializes a Hedge object, sublass of Lane.

        Parameter dict: A JSON dictionary containing information about the level
        Precondition: dict is a dictionary

        Parameter lnnum: A int representing the lane number, bottom/first = 0
        Precondition: lnnum is an int >= 0

        Parameter hbdict: A JSON dictionary with hitbox sizes for obstacles
        Precondition: hbdict is a dictionary
        """
        self._usedexits = []
        super().__init__(dict,lnnum,hbdict)

    # ANY ADDITIONAL METHODS
    def collide_hedge(self,frog):
        """
        Returns True if Frog collides with Hedge.

        Parameter frog: A Frog object representing the frog in the game
        Precondition: frog is a Frog object
        """
        if frog.getFrog().collides(self._tile):
            return True

        return False

    def is_open_hedge(self,frog):
        """
        Returns True if frog is an exit or opening in the Hedge lane.

        Parameter frog: A Frog object representing the frog in the game
        Precondition: frog is a Frog object
        """
        cood = (frog.getX(),frog.getY())

        for obst in self._objs:
            if obst.contains(cood):
                return True
        return False

    def type_hedge_obst(self,frog):
        """
        Returns the type of obstacle which contains the frog.

        Method returns the type as a string. If no obstacle contains the
        coordinates provided, the method returns an empty string.

        Parameter frog: A Frog object representing the frog in the game
        Precondition: frog is a Frog object
        """
        cood = (frog.getX(),frog.getY())
        for obst in self._objs:
            if obst.contains((frog.getX(),frog.getY())):
                return obst.source[:-4]
        return ''

    def allow_in_exit(self,frog):
        """
        Returns True if the Frog can move into the exit within the Hedge.

        Method will return False when the exit is already occupied.

        Parameter frog: A Frog object representing the frog in the game
        Precondition: frog is a Frog object
        """
        for obst in self._objs:
            if obst.contains((frog.getX(),frog.getY())) and\
            not obst in self._usedexits:
                return True
        return False

    def add_used_exit(self,frog):
        """
        Adds used exit to the list _usedexits.

        Parameter frog: A Frog object representing the frog in the game
        Precondition: frog is a Frog object
        """
        cood = (frog.getX(),frog.getY())

        for exit in self._objs:
            if exit.contains(cood):
                self._usedexits.append(exit)

    def which_exit(self,frog):
        """
        Returns the exit which contains the frog.

        If no exit contains the frog, method returns None.

        Parameter frog: A Frog object representing the frog in the game
        Precondition: frog is a Frog object
        """
        cood = (frog.getX(),frog.getY())
        for exit in self._objs:
            if exit.contains(cood):
                return exit

        return None

    def exits_filled(self):
        """
        Returns True if all exits in Hedge lane are filled.
        """
        result = False
        for exit in self._objs:
            if exit in self._usedexits:
                result = True
            else:
                return False

        return result

# IF YOU NEED ADDITIONAL LANE CLASSES, THEY GO HERE
