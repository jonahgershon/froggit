"""
Models module for Froggit

This module contains the model classes for the Frogger game. Anything that you
interact with on the screen is model: the frog, the cars, the logs, and so on.

Just because something is a model does not mean there has to be a special class for
it. Unless you need something special for your extra gameplay features, cars and logs
could just be an instance of GImage that you move across the screen. You only need a new
class when you add extra features to an object.

That is why this module contains the Frog class.  There is A LOT going on with the
frog, particularly once you start creating the animation coroutines.

If you are just working on the main assignment, you should not need any other classes
in this module. However, you might find yourself adding extra classes to add new
features.  For example, turtles that can submerge underneath the frog would probably
need a custom model for the same reason that the frog does.

If you are unsure about  whether to make a new class or not, please ask on Piazza. We
will answer.

# YOUR NAME AND NETID HERE
# DATE COMPLETED HERE
"""
from consts import *
from game2d import *

# PRIMARY RULE: Models are not allowed to access anything in any module other than
# consts.py.  If you need extra information from a lane or level object, then it
# should be a parameter in your method.


class Frog(GSprite):         # You will need to change this by Task 3
    """
    A class representing the frog

    The frog is represented as an image (or sprite if you are doing timed animation).
    However, unlike the obstacles, we cannot use a simple GImage class for the frog.
    The frog has to have additional attributes (which you will add).  That is why we
    make it a subclass of GImage.

    When you reach Task 3, you will discover that Frog needs to be a composite object,
    tracking both the frog animation and the death animation.  That will like caused
    major modifications to this class.
    """

    # LIST ALL HIDDEN ATTRIBUTES HERE
    # Attribute _x: the x coordinate of the composite frog object
    # Invariant: _x is a number >= 0

    # Attribute _y: the y coordinate of the composite frog object
    # Invariant: _y is a number >= 0

    # Attribute _frog: A sprite which illustrates the frog
    # Invariant: _frog is a GSprite object

    # Attribute _death: A sprite which illustrates the frog's death
    # Invariant: _death is a GSprite object

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getFrog(self):
        """
        Returns the _frog GSprite attribute of the composite object.
        """
        return self._frog

    def getDeath(self):
        """
        Returns the _death GSprite attribute of the composite object.
        """
        return self._death

    def getY(self):
        """
        Returns the y coordinate of the composite frog object.
        """
        return self._y

    def getX(self):
        """
        Returns the x coordinate of the composite frog object.
        """
        return self._x

    def setX(self,value):
        """
        Sets x coordinate of composite object equal to value.

        Parameter value: The new x coordinate.
        Precondition: value is a number >= 0
        """
        self._x = value
        self._frog.x = value
        self._death.x = value

    def setY(self,value):
        """
        Sets y coordinate of composite object equal to value.

        Parameter value: The new y coordinate.
        Precondition: value is a number >= 0
        """
        self._y = value
        self._frog.y = value
        self._death.y = value

    # INITIALIZER TO SET FROG POSITION
    def __init__(self,x,y,dict):
        """
        Initializes Frog object.

        Parameter x: The starting x coordinate value of the frog
        Precondition: x is a number

        Parameter y: The starting y coordinate value of the frog
        Precondition: y is a number

        Parameter dict: A JSON dictionary with hitbox sizes for obstacles
        Precondition: dict is a dictionary
        """
        frogformat = dict['sprites']['frog']['format']
        frogsize = (frogformat[0],frogformat[1])
        hitboxes = dict['sprites']['frog']['hitboxes']
        deathformat = dict['sprites']['skulls']['format']
        deathsize = (deathformat[0],deathformat[1])

        self._frog = GSprite(x=x,y=y,source=FROG_SPRITE+'.png',angle=FROG_NORTH,\
            format=frogsize,frame=0,hitboxes=hitboxes)

        self._death = GSprite(x=x,y=y,source=DEATH_SPRITE+'.png',\
            format=deathsize,frame=0)

        self._x = x
        self._y = y

    # ADDITIONAL METHODS (DRAWING, COLLISIONS, MOVEMENT, ETC)
    def draw(self,view):
        """
        Draws the frog object (_frog and _death when appropriate).

        Parameter view: the view to draw to
        Precondition: view is a GView obect
        """
        if not self._frog is None:
            self._frog.draw(view)

        else:
            self._death.draw(view)

    def animate_vertical(self,direction):
        """
        Animates the frog up or down over FROG_SPEED seconds.

        Parameter dt: The time since the last animation frame.
        Precondition: dt is a float.

        Parameter direction: The direction to move
        Precondition: direction is a string, either 'up' or 'down'
        """
        start = self._y
        if direction == 'up':
            end = start + GRID_SIZE
        elif direction == 'down':
            end = start - GRID_SIZE

        step = GRID_SIZE/FROG_SPEED
        time = 0
        split = FROG_SPEED/8
        counttime = 0
        frame = [0,1,2,3,4,3,2,1,0]
        count = 0

        while time <= FROG_SPEED:
            dt = (yield)
            if direction == 'up':
                self.setY(self._y + step*dt)
            elif direction == 'down':
                self.setY(self._y - step*dt)

            time += dt
            counttime += dt
            if counttime >= split:
                count += 1
                counttime = 0
                self._frog.frame = frame[count]

            if direction == 'up' and self._y > end:
                self.setY(end)
            elif direction == 'down' and self._y < end:
                self.setY(end)

        self._frog.frame = 0

    def animate_horizontal(self,direction):
        """
        Animates the frog left or right over FROG_SPEED seconds.

        Parameter dt: The time since the last animation frame.
        Precondition: dt is a float.

        Parameter direction: The direction to move
        Precondition: direction is a string, either 'left' or 'right'
        """
        start = self._x
        if direction == 'right':
            end = start + GRID_SIZE
        elif direction == 'left':
            end = start - GRID_SIZE

        step = GRID_SIZE/FROG_SPEED
        time = 0
        split = FROG_SPEED/8
        counttime = 0
        frame = [0,1,2,3,4,3,2,1,0]
        count = 0

        while time < FROG_SPEED:
            dt = (yield)
            if direction == 'right':
                self.setX(self._x + step*dt)
            elif direction == 'left':
                self.setX(self._x - step*dt)
            if abs(self._x-start) > GRID_SIZE:
                self.setX(end)

            time += dt
            counttime += dt

            if counttime >= split:
                count += 1
                counttime = 0
                self._frog.frame = frame[count]

        if abs(self._x-start) > GRID_SIZE:
            self.setX(end)

        self._frog.frame = 0

    def animate_death(self):
        """
        Animates the frogs death over DEATH_SPEED seconds.

        Sets the _frog attribute to None.

        Parameter dt: The time since the last animation frame.
        Precondition: dt is a float.
        """
        self._frog = None
        split = DEATH_SPEED/7
        counttime = 0
        count = 0
        time = 0

        while time <= DEATH_SPEED:
            dt = (yield)
            time += dt

            counttime += dt
            if counttime >= split:
                count += 1
                counttime = 0
                self._death.frame = count

        self._death.frame = 0

# IF YOU NEED ADDITIONAL LANE CLASSES, THEY GO HERE
