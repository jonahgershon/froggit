"""
Subcontroller module for Froggit

This module contains the subcontroller to manage a single level in the Froggit game.
Instances of Level represent a single game, read from a JSON.  Whenever you load a new
level, you are expected to make a new instance of this class.

The subcontroller Level manages the frog and all of the obstacles. However, those are
all defined in models.py.  The only thing in this class is the level class and all of
the individual lanes.

This module should not contain any more classes than Levels. If you need a new class,
it should either go in the lanes.py module or the models.py module.

# YOUR NAME AND NETID HERE
# DATE COMPLETED HERE
"""
from game2d import *
from consts import *
from lanes  import *
from models import *

# PRIMARY RULE: Level can only access attributes in models.py or lanes.py using getters
# and setters. Level is NOT allowed to access anything in app.py (Subcontrollers are not
# permitted to access anything in their parent. To see why, take CS 3152)


class Level(object):
    """
    This class controls a single level of Froggit.

    This subcontroller has a reference to the frog and the individual lanes.  However,
    it does not directly store any information about the contents of a lane (e.g. the
    cars, logs, or other items in each lane). That information is stored inside of the
    individual lane objects.

    If you want to pause the game, tell this controller to draw, but do not update.  See
    subcontrollers.py from Lesson 27 for an example.  This class will be similar to that
    one in many ways.

    All attributes of this class are to be hidden.  No attribute should be accessed
    without going through a getter/setter first.  However, just because you have an
    attribute does not mean that you have to have a getter for it.  For example, the
    Froggit app probably never needs to access the attribute for the Frog object, so
    there is no need for a getter.

    The one thing you DO need a getter for is the width and height.  The width and height
    of a level is different than the default width and height and the window needs to
    resize to match.  That resizing is done in the Froggit app, and so it needs to access
    these values in the level.  The height value should include one extra grid square
    to suppose the number of lives meter.
    """

    # LIST ALL HIDDEN ATTRIBUTES HERE
    # Attribute _height: The height of the level by number of grid squares
    # Invariant: _height is an int > 0

    # Attribute _width: The width of the level by number of grid squares
    # Invariant: _width is an int > 0

    # Attribute _lanes: A list of the lanes in a level extracted fron JSON dict
    # Invariant: _lanes is a list containing Lane objects

    # Attribute _currlane: The current lane where the frog is located
    # Invariant: _currlane is a Lane object

    # Attribute _frog: A Frog object representing the frog in the game
    # Invariant: _frog is a Frog object or None

    # Attribute _lives: A list record of lives left in the game
    # Invariant: _lives is a list of GImage objects

    # Attribute _livlabel: A label indicating the frog head images are lives
    # Invariant: _livlabel is a GLabel object

    # Attribute _buffer: The distance that obstacles can move offscreen
    # Invariant: _buffer is a number > 0

    # Attribute _state: The current state of the game
    # Invariant: _state is an 0 <= int <= 5

    # Attribute _startx: The starting x-coordinate of the frog
    # Invariant: _starty is a number >= 0 and < width of game in pixels

    # Attribute _starty: The starting y-coordinate of the frog
    # Invariant: _starty is a number >= 0 and < height of game in pixels

    # Attribute _donefrogs: A list of images representing frogs that finished
    # Invariant: _donefrogs is list of GImage objects

    # Attribute _animator: A coroutine for performing an animation
    # Invariant: _animator is a generator-based coroutine or None

    # Attribute _alive: A bool stating if frog is alive or dying
    # Invariant: _alive is a bool, False while in dying animation

    # Attribute _croakS: The sound for when the frog jumps
    # Invariant: _croakS is Sound object

    # Attribute _splatS: The sound for when the frog dies
    # Invariant: _splatS is Sound object

    # Attribute _trillS: The sound for when the frog reaches an exit
    # Invariant: _trillS is Sound object

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getWidth(self):
        """
        Returns the width of level.
        """
        return self._width

    def getHeight(self):
        """
        Returns the height of level.
        """
        return self._height

    def getState(self):
        """
        Returns the current state of the game-level.
        """
        return self._state

    def getDonefrogs(self):
        """
        Returns the list (_donefrogs) of images representing frogs that finished.
        """
        return self._donefrogs

    def getDonefrogs(self):
        """
        Returns the list (_donefrogs) of images representing frogs that finished.
        """
        return self._donefrogs

    # INITIALIZER (standard form) TO CREATE THE FROG AND LANES
    def __init__(self,dict,hbdict):
        """
        Initializes a level object from a level JSON dictionary.

        Parameter dict: A JSON dictionary containing information about the level
        Precondition: dict is a dictionary

        Parameter hbdict: A JSON dictionary with hitbox sizes for obstacles
        Precondition: hbdict is a dictionary
        """
        self._width = dict['size'][0]
        self._height = dict['size'][1]+1
        self._state = STATE_ACTIVE

        self._init_lanes(dict,hbdict)
        self._init_lives()

        self._startx = dict['start'][0]*GRID_SIZE+GRID_SIZE/2
        self._starty = dict['start'][1]*GRID_SIZE+GRID_SIZE/2
        self._frog = Frog(self._startx,self._starty,hbdict)
        self._buffer = dict['offscreen']
        self._donefrogs = []
        self._animator = None
        self._alive = True

        self._croakS = Sound(source=CROAK_SOUND)
        self._splatS = Sound(source=SPLAT_SOUND)
        self._trillS = Sound(source=TRILL_SOUND)

    # UPDATE METHOD TO MOVE THE FROG AND UPDATE ALL OF THE LANES
    def update(self,input,dt):
        """
        Animated the frog's movements and animation and updates all the
        lanes' obstacles.

        Parameter input: The user's input
        Precondition: input is an instance of GInput

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float) >= 0
        """
        if self._alive:
            self._special_cases(dt)

        if not self._animator is None:
            try:
                self._animator.send(dt)
            except:
                self._animator = None
                if not self._alive:
                    self._frog_died()
        elif not self._frog is None:
            if input.is_key_down('right'):
                self._to_right()
            elif input.is_key_down('left'):
                self._to_left()
            elif input.is_key_down('up'):
                self._to_up()
            elif input.is_key_down('down'):
                self._to_down()

        for lane in self._lanes:
            lane.update(dt,self._buffer)

    # DRAW METHOD TO DRAW THE FROG AND THE INDIVIDUAL LANES
    def draw(self,view):
        """
        Draws the all the aspects of the level, including the frog, lanes,
        lives and finished frogs, to the view.

        Parameter view: The view to draw to
        Precondition: view is a GView obect
        """
        for lane in self._lanes:
            lane.draw(view)

        for life in self._lives:
            life.draw(view)

        self._livlabel.draw(view)

        if not self._frog is None:
            self._frog.draw(view)

        if len(self._donefrogs) > 0:
            for frog in self._donefrogs:
                frog.draw(view)

    # ANY NECESSARY HELPERS (SHOULD BE HIDDEN)
    def exits_full(self):
        """
        Returns True if all exits in the level are full.
        """
        result = False

        for lane in self._lanes:
            if lane.getTile().source == 'hedge.png':
                result = lane.exits_filled()

        return result

    def start_over(self,dict):
        """
        Generates a new frog and positions it in the starting position.

        Uses the attributes startx and starty to return the frog back
        to the intial starting position provided by the level JSON. Also
        resets _alive attribute to True.

        Parameter dict: A JSON dictionary with hitbox sizes for obstacles
        Precondition: dict is a dictionary
        """
        self._frog = Frog(self._startx,self._starty,dict)
        self._alive = True
        self._state = STATE_ACTIVE

    def _init_lanes(self,dict,hbdict):
        """
        Helper method to __init__ to initate _lanes attribute.

        Parameter dict: A JSON dictionary containing information about the level
        Precondition: dict is a dictionary

        Parameter hbdict: A JSON dictionary with hitbox sizes for obstacles
        Precondition: hbdict is a dictionary
        """
        self._lanes = []
        lstlanes = dict['lanes']

        for pos in range(len(lstlanes)):
            if lstlanes[pos]['type'] == 'grass':
                lane = Grass(dict,pos,hbdict)
            elif lstlanes[pos]['type'] == 'road':
                lane = Road(dict,pos,hbdict)
            elif lstlanes[pos]['type'] == 'water':
                lane = Water(dict,pos,hbdict)
            elif lstlanes[pos]['type'] == 'hedge':
                lane = Hedge(dict,pos,hbdict)

            self._lanes.append(lane)

    def _init_lives(self):
        """
        Helper method to __init__ to initate _lives and _livlabel attributes.
        """
        self._lives = []
        for pos in range(3):
            life = GImage(source=FROG_HEAD,width=GRID_SIZE,height=GRID_SIZE)
            life.left = (self._width-(3-pos))*GRID_SIZE
            life.top = (self._height)*GRID_SIZE
            self._lives.append(life)

        self._livlabel = GLabel(text='Lives:')
        self._livlabel.right = self._lives[0].left
        self._livlabel.bottom = (self._height-.9)*GRID_SIZE
        self._livlabel.font_name = ALLOY_FONT
        self._livlabel.font_size = ALLOY_SMALL
        self._livlabel.linecolor = 'dark green'

    def _special_cases(self,dt):
        """
        Method checks for special cases when frog moves, including if frog
        collides and dies, safely exits, or drowns.

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float) >= 0
        """
        lane = self._lanes[round((self._frog.getY()-GRID_SIZE/2)/GRID_SIZE)]
        if isinstance(lane, Road) and lane.collide_car(self._frog):
            self._initiate_death()
        elif isinstance(lane, Water) and not lane.on_log(self._frog) and \
        self._animator is None:
            self._initiate_death()
        elif isinstance(lane, Water) and lane.on_log(self._frog):
            if self._animator is None:
                lane.move_frog_log(self._frog,dt)
            if self._frog.getX()< 0 or self._frog.getX()> self._width*GRID_SIZE:
                self._initiate_death()
        elif isinstance(lane,Hedge):
            if lane.collide_hedge(self._frog):
                if lane.type_hedge_obst(self._frog) == 'exit':
                    if lane.allow_in_exit(self._frog):
                        self._frog_to_exit()

    def _to_right(self):
        """
        Initiates a right moving animation of the Frog if Frog can move into
        new x position. Frog does not move out of level grid and into hedges.
        """
        self._croakS.play()
        oldx = self._frog.getX()
        newx = self._frog.getX()+GRID_SIZE
        y = self._frog.getY()
        self._frog.getFrog().angle = FROG_EAST

        if newx < self._width*GRID_SIZE:
            self._animator = self._frog.animate_horizontal('right')
            next(self._animator)
            lane = self._lanes[round((self._frog.getY()-GRID_SIZE/2)/GRID_SIZE)]
            if isinstance(lane,Hedge):
                self._animator = None

    def _to_left(self):
        """
        Initiates a left moving animation of the Frog if Frog can move into
        new x position. Frog does not move out of level grid and into hedges.
        """
        self._croakS.play()
        oldx = self._frog.getX()
        newx = self._frog.getX()-GRID_SIZE
        y = self._frog.getY()
        self._frog.getFrog().angle = FROG_WEST

        if newx > 0:
            self._animator = self._frog.animate_horizontal('left')
            next(self._animator)
            lane = self._lanes[round((self._frog.getY()-GRID_SIZE/2)/GRID_SIZE)]
            if isinstance(lane,Hedge):
                self._animator = None

    def _to_up(self):
        """
        Initiates an upward moving animation of the Frog if Frog can move into
        new y position. Frog does not move out of level grid, into hedges or
        used exits.
        """
        self._croakS.play()
        oldy = self._frog.getY()
        newy = self._frog.getY()+GRID_SIZE
        x = self._frog.getX()
        self._frog.getFrog().angle = FROG_NORTH

        if newy < (self._height-1)*GRID_SIZE:
            self._animator = self._frog.animate_vertical('up')
            next(self._animator)
            lane = self._lanes[round((newy-GRID_SIZE/2)/GRID_SIZE)]
            if isinstance(lane,Hedge):
                self._frog.setY(newy)
                if lane.collide_hedge(self._frog):
                    if lane.type_hedge_obst(self._frog) == 'exit':
                        if not lane.allow_in_exit(self._frog):
                            self._frog.setY(oldy)
                            self._animator = None
                        elif lane.allow_in_exit(self._frog):
                            self._frog.setY(oldy)
                    elif not lane.is_open_hedge(self._frog):
                        self._frog.setY(oldy)
                        self._animator = None
                    elif lane.is_open_hedge(self._frog):
                        self._frog.setY(oldy)

    def _to_down(self):
        """
        Initiates a downward moving animation of the Frog if Frog can move into
        new y position. Frog does not move out of level grid, into hedges,
        used exits, or open exits from above.
        """
        self._croakS.play()
        oldy = self._frog.getY()
        newy = self._frog.getY()-GRID_SIZE
        x = self._frog.getX()
        self._frog.getFrog().angle = FROG_SOUTH

        if newy > 0:
            self._animator = self._frog.animate_vertical('down')
            next(self._animator)
            lane = self._lanes[round((newy-GRID_SIZE/2)/GRID_SIZE)]
            if isinstance(lane,Hedge):
                self._frog.setY(newy)
                if lane.collide_hedge(self._frog):
                    if not lane.is_open_hedge(self._frog) or \
                        lane.type_hedge_obst(self._frog) == 'exit':
                            self._frog.setY(oldy)
                            self._animator = None
                    elif lane.is_open_hedge(self._frog):
                        self._frog.setY(oldy)

    def _initiate_death(self):
        """
        Changes the attribute _alive to False and initiates death animation
        coroutine.
        """
        self._alive = False
        self._splatS.play()
        self._animator = self._frog.animate_death()
        next(self._animator)

    def _frog_died(self):
        """
        Alters _state, _animator, _frog and _lives attributes once frog dies
        and adjusts according to how many lives are left.
        """
        self._animator = None
        if len(self._lives) > 1:
            self._state = STATE_PAUSED
            self._frog = None
            self._lives = self._lives[:-1]
        else:
            self._state = STATE_COMPLETE
            self._frog = None
            self._lives = self._lives[:-1]

    def _frog_to_exit(self):
        """
        Creates finished frog image over exit and adjusts state based on how
        many open exits are left. Adds the used exit to _donefrogs attribute.
        """
        self._trillS.play()
        lane = self._lanes[round((self._frog.getY()-GRID_SIZE/2)/GRID_SIZE)]
        exit = lane.which_exit(self._frog)
        image = GImage(source=FROG_SAFE,x=exit.x,y=exit.y)
        lane.add_used_exit(self._frog)
        self._donefrogs.append(image)
        self._frog = None
        if self.exits_full():
            self._state = STATE_COMPLETE
        else:
            self._state = STATE_PAUSED
