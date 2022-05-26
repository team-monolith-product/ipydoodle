import ipycanvas
import time
import threading
import sys
import time
import threading
from IPython.display import display
import numpy # Installed by ipycanvas package

FREQUENCY = 30
DEFAULT = {
            "Box" : {"width":100, "height":100},
            "Line" : {"x1":100, "y1":100, "x2":-100, "y2":-100},
            "Circle" : {"radius" : 50},
          }

CURRENT_WORLD = None


class Canvas(ipycanvas.Canvas):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__color = kwargs['color']
        self.__axis = kwargs['axis']
        self.__axis_color = kwargs['axis_color']
    def clear(self):
        super().clear()
        self.fill_styled_rects([0],[0],[self.width],[self.height], color = self.__color.color)
        
        # axis
        if self.__axis:
            self.stroke_styled_line_segments([[(-self.width,0),(self.width,0)],[(0,self.height),(0,-self.height)]], color=self.__axis_color.color)

    def move_coor(self, x, y):
        try :
            if (type(x) == int or type(x) == float) and (type(y) == int or type(y) == float) :
                moved_x = x + self.width/2
                moved_y = self.height/2 - y
            else:
                moved_x = [xx + self.width/2 for xx in x]
                moved_y = [self.height/2 - yy for yy in y]
        except :
            sys.stderr.write("x, y must be same type : int, arr")
        
        return moved_x, moved_y
    
    def moved_coor_rect_center(self, x, y, width, height):
        try : 
            if type(x) == int and type(y) == int and type(width) == int and type(height) == int :
                moved_x = x - width/2
                moved_y = y + height/2
            else:
                moved_x = [xx - width[i]/2 for i, xx in enumerate(x)]
                moved_y = [yy + height[i]/2 for i, yy in enumerate(y)]
        except :
            sys.stderr.write("x, y, width, height must be same type : int, arr")
        
        return moved_x, moved_y
    
    def fill_styled_rects(self, x, y, width, height, color, alpha=1):
        x,y = self.move_coor(*self.moved_coor_rect_center(x,y,width,height))
        super().fill_styled_rects(x, y, width, height, color, alpha)

    def fill_styled_circles(self, x, y, radius, color, alpha=1):
        x,y = self.move_coor(x, y)
        super().fill_styled_circles(x, y, radius, color, alpha)
        
    def stroke_styled_line_segments(self, points, color, alpha=1, points_per_line_segment=None):
        for l_idx in range(len(points)):
            for p_idx in range(len(points[l_idx])):
                points[l_idx][p_idx] = self.move_coor(*points[l_idx][p_idx])
        
        super().stroke_styled_line_segments(points, color, alpha, points_per_line_segment)
    
    @property
    def color(self):
        return self.__color
    
    @color.setter
    def color(self, val):
        self.__color = val
    
    @property
    def axis(self):
        return self.__axis
    
    @axis.setter
    def axis(self, val):
        self.__axis = self.val
    
    @property
    def axis_color(self):
        return self.__axis_color
    
    @axis_color.setter
    def axis_color(self, val):
        self.__axis_color = self.val

class Color:
    def __init__(self, val):
        self.__color = self.__change_color_type(val)

    def __repr__(self):
        return str(self.__color)
        
    def __change_color_type(self,val):
        if type(val) is str:
            if val[0] == '#' and len(val) == 7:
                retval = [int(val[1:3],16),int(val[3:5],16),int(val[5:7],16)]
            else:
                retval = self.__str2list(val.lower())
        elif type(val) is list:
            retval = val
        elif type(val) is numpy.ndarray:
            retval = list(val)
        elif type(val) is tuple:
            retval = list(val)
        else:
            raise TypeError(f'Color does not support {type(val)} parameter')
            
        return retval
    
    def __str2list(self,val):
        color_dict = {
            'black' : (0,0,0),
            'white' : (255,255,255),
            'red' : (255,0,0),
            'lime' : (0,255,0),
            'blue' : (0,0,255),
            'yellow' : (255,255,0),
            'cyan' : (0,255,255),
            'magenta' : (255,0,255),
            'silver' : (192,192,192),
            'gray' : (128,128,128),
            'maroon' : (128,0,0),
            'olive' : (128,128,0),
            'green' : (0,128,0),
            'purple' : (128,0,128),
            'teal' : (0,128,128),
            'navy' : (0,0,128),
            '검정색' : (0,0,0),
            '흰색' : (255,255,255),
            '빨강색' : (255,0,0),
            '연두색' : (0,255,0),
            '파란색' : (0,0,255),
            '노란색' : (255,255,0),
            '옥색' : (0,255,255),
            '분홍색' : (255,0,255),
            '은색' : (192,192,192),
            '회색' : (128,128,128),
            '적갈색' : (128,0,0),
            '올리브색' : (128,128,0),
            '초록색' : (0,128,0),
            '보라색' : (128,0,128),
            '암청색' : (0,128,128),
            '남색' : (0,0,128)
        }
        
        try:
            return list(color_dict[val])
        except:
            raise ValueError(f'Wrong name for color : {val}')
            
    @property
    def color(self):
        return self.__color
    
    @color.setter
    def color(self, val):
        self.__color = self.__change_color_type(val)


class World:
    def __init__(self, width = 700, height = 500, color = 'white', axis = True, axis_color = 'black'):
        self.__width = width
        self.__height = height
        self.__color = Color(color)
        self.__axis = axis
        self.__axis_color = Color(axis_color)
        self.canvas = Canvas(width = self.__width, height = self.__height, color = self.__color, axis = self.__axis, axis_color = self.__axis_color)
        self.objects = []
        self.rendered_at = None


        global CURRENT_WORLD
        CURRENT_WORLD = self
        
        # set canvas to white
        self.canvas.clear()
        
        display(self.canvas)
    
    def render(self):
        self.rendered_at = time.time()

        with ipycanvas.hold_canvas(self.canvas):
            self.canvas.clear()
            for obj in self.objects:
                obj.draw()

    def dirty(self):
        now = time.time()
        if self.rendered_at:
            if now - self.rendered_at >= (1/FREQUENCY):
                self.render()
            else:
                old_rendered_at = self.rendered_at
                def func():
                    time.sleep((1/FREQUENCY) - (now - self.rendered_at))
                    if old_rendered_at == self.rendered_at:
                        self.render()
                t = threading.Thread(target = func)
                t.start()
        else:
            self.render()
    
    def clear(self):
        self.objects = []
        self.canvas.clear()

    @property
    def width(self):
        return self.__width
    
    @property
    def height(self):
        return self.__height
        
    @width.setter
    def width(self, val):
        self.__width = val
        self.canvas.width = self.__width
        self.canvas.clear()

    @height.setter
    def height(self, val):
        self.__height = val
        self.canvas.height = self.__height
        self.canvas.clear()

    @property
    def color(self):
        return self.__color
    
    @color.setter
    def color(self, val):
        self.__color = Color(val)
        self.canvas.color = self.__color

        self.canvas.clear()    
    
    @property
    def axis(self):
        return self.__axis

    @axis.setter
    def axis(self, val):
        self.__axis = self.val
        self.canvas.clear()

    @property
    def axis_color(self):
        return self.__axis_color
    
    @axis_color.setter
    def axis_color(self, val):
        self.__axis_color = self.val
        self.canvas.clear()

class WorldObject:
    def __init__(self, world=None):
        if not world:
            global CURRENT_WORLD
            if not CURRENT_WORLD:
                CURRENT_WORLD = World()
            self.__world = CURRENT_WORLD
        else:
            self.__world = world

        self.__world.objects.append(self)
    
    def dirty(self):
        return self.__world.dirty()

    def canvas(self):
        return self.__world.canvas
        
 
class Box(WorldObject):
    def __init__(self, world=None, x=None , y=None , width=None , height=None , color='black', alpha=1, trail = False):
        super(Box,self).__init__(world)
        
        if not x:
            x = 0
        if not y:
            y = 0
        if not width:
            width = DEFAULT["Box"]["width"]
        if not height:
            height = DEFAULT["Box"]["height"]
        
        self.__pos = x,y
        self.__width = width
        self.__height = height
        self.__color = Color(color)
        self.__alpha = alpha
        self.__pos_history = [(x,y)]
        self.__trail = trail

        self.dirty()
        
    def draw(self):
        self.canvas().fill_styled_rects([self.pos[0]], [self.pos[1]], [self.__width], [self.__height], [self.__color.color], alpha=self.__alpha)

        if self.__trail:
            self.canvas().stroke_styled_line_segments([[pos for pos in self.__pos_history]], color=self.__color.color, alpha = self.__alpha)

    @property
    def color(self):
        return self.__color.color
    
    @property
    def alpha(self):
        return self.__alpha
        
    @color.setter
    def color(self, val):
        self.__color.color = val                                              
        self.dirty()

    @alpha.setter
    def alpha(self, val):
        self.__alpha = val
        self.dirty()
        
    @property
    def pos(self):
        return self.__pos

    @property
    def x(self):
        return self.__pos[0]
    
    @property
    def y(self):
        return self.__pos[1]
    
    @property
    def width(self):
        return self.__width
    
    @property
    def height(self):
        return self.__height
        
    @x.setter
    def x(self, val):
        self.pos = val, self.__pos[1]

    @y.setter
    def y(self, val):
        self.pos = self.__pos[0], val 
    
    @pos.setter
    def pos(self, val):
        self.__pos = tuple(val)
        self.__pos_history.append(self.__pos)
        self.dirty()
        
    @width.setter
    def width(self, val):
        self.__width = val
        self.dirty()

    @height.setter
    def height(self, val):
        self.__height = val
        self.dirty()
        

class Line(WorldObject):
    def __init__(self, world=None, x1=None , y1=None , x2=None , y2=None , color='black', alpha=1):
        super().__init__(world)

        if x1 is None and y1 is None and x2 is None and y2 is None:
            x1 = DEFAULT["Line"]["x1"]
            y1 = DEFAULT["Line"]["y1"]
            x2 = DEFAULT["Line"]["x2"]
            y2 = DEFAULT["Line"]["y2"]
        elif (x1 is None) or (y1 is None):
            raise SyntaxError(f'x1 and y1 must be given together : {"x1"if x1 is None else "y1"}')
        elif (x2 is None) or (y2 is None):
            raise SyntaxError(f'x2 and y2 must be given together : {"x2"if x2 is None else "y2"}')
        elif (x1 is None) and (y1 is None):
            x1 = 0
            y1 = 0
        elif (x2 is None) and (y2 is None):
            x2 = 0
            y2 = 0

        self.__x1 = x1
        self.__y1 = y1
        self.__x2 = x2
        self.__y2 = y2
        self.__color = Color(color)
        self.__alpha = alpha
        
        self.dirty()
        
    def draw(self):
        self.canvas().stroke_styled_line_segments([[(self.__x1,self.__y1),(self.__x2,self.__y2)]], color=self.__color.color, alpha = self.__alpha)
    
    @property
    def color(self):
        return self.__color.color
    
    @property
    def alpha(self):
        return self.__alpha
        
    @color.setter
    def color(self, val):
        self.__color.color = val
        self.dirty()

    @alpha.setter
    def alpha(self, val):
        self.__alpha = val
        self.dirty()
        
    @property
    def x1(self):
        return self.__x1
    
    @property
    def y1(self):
        return self.__y1
    
    @property
    def x2(self):
        return self.__x2
    
    @property
    def y2(self):
        return self.__y2
        
    @x1.setter
    def x1(self, val):
        self.__x1 = val
        self.dirty()

    @y1.setter
    def y1(self, val):
        self.__y1 = val
        self.dirty()
        
    @x2.setter
    def x2(self, val):
        self.__x2 = val
        self.dirty()

    @y2.setter
    def y2(self, val):
        self.__y2 = val
        self.dirty()
        

class Circle(WorldObject):
    def __init__(self, world=None, x=None , y=None , radius=None, color='black', alpha=1, trail = False):
        super().__init__(world)
        
        if not x:
            x = 0
        if not y:
            y = 0

        if radius is None:
            radius = DEFAULT["Circle"]["radius"]
            
        self.__pos = (x,y)
        self.__radius = radius
        self.__color = Color(color)
        self.__alpha = alpha
        self.__pos_history = [(x,y)]
        self.__trail = trail

        self.dirty()
        
    def draw(self):
        self.canvas().fill_styled_circles([self.__pos[0]], [self.__pos[1]], [self.__radius], color=self.__color.color, alpha = self.__alpha)

        if self.__trail:
            self.canvas().stroke_styled_line_segments([[pos for pos in self.__pos_history]], color=self.__color.color, alpha = self.__alpha)
    
    @property
    def color(self):
        return self.__color.color
    
    @property
    def alpha(self):
        return self.__alpha
        
    @color.setter
    def color(self, val):
        self.__color.color = val
        self.dirty()

    @alpha.setter
    def alpha(self, val):
        self.__alpha = val
        self.dirty()

    @property
    def pos(self):
        return self.__pos

    @property
    def x(self):
        return self.__pos[0]
    
    @property
    def y(self):
        return self.__pos[1]
    
    @property
    def radius(self):
        return self.__radius
        
    @x.setter
    def x(self, val):
        self.pos = val, self.__pos[1]

    @y.setter
    def y(self, val):
        self.pos = self.__pos[0], val 
    
    @pos.setter
    def pos(self, val):
        self.__pos = tuple(val)
        self.__pos_history.append(self.__pos)
        self.dirty()
        
    @radius.setter
    def radius(self, val):
        self.__radius = val
        self.dirty()