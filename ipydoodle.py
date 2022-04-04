import ipycanvas
import time
import threading
import numpy as np
import sys
import time
import threading

FREQUENCY = 30
DEFAULT = {
            "Box" : {"width":100, "height":100},
            "Line" : {"x1":100, "y1":100, "x2":-100, "y2":-100},
            "Circle" : {"radius" : 50},
          }

CURRENT_WORLD = None


class Canvas(ipycanvas.Canvas):
    def clear(self):
        super().clear()
        self.fill_styled_rects([0],[0],[self.size[0]],[self.size[1]], color = [256,256,256])
        
        # axis
        self.stroke_styled_line_segments([[(-self.size[0],0),(self.size[0],0)],[(0,self.size[1]),(0,-self.size[1])]], color=[100,100,100])
    
    def move_coor(self, x, y):
        try : 
            if type(x) == int and type(y) == int :
                moved_x = x + self.size[0]/2
                moved_y = self.size[1]/2 - y
            else:
                moved_x = [xx + self.size[0]/2 for xx in x]
                moved_y = [self.size[1]/2 - yy for yy in y]
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
        
class World:
    def __init__(self):
        self.canvas = Canvas()
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
    
    def move_coor(self, x, y):
        moved_x = x + self.canvas.size[0]/2
        moved_y = self.canvas.size[1]/2 - y
        return moved_x, moved_y

            
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
    def __init__(self, world=None, x=None , y=None , width=None , height=None , color=[0,0,0], alpha=1):
        super(Box,self).__init__(world)
        
        if not x:
            x = 0
        if not y:
            y = 0
        if not width:
            width = DEFAULT["Box"]["width"]
        if not height:
            height = DEFAULT["Box"]["height"]
        
        self.__x = x
        self.__y = y
        self.__width = width
        self.__height = height
        self.__color = color
        self.__alpha = alpha
        
        self.dirty()
        
    def draw(self):
        self.canvas().fill_styled_rects([self.__x], [self.__y], [self.__width], [self.__height], [self.__color], alpha=self.__alpha)
    
    @property
    def color(self):
        return self.__color
    
    @property
    def alpha(self):
        return self.__alpha
        
    @color.setter
    def color(self, val):
        self.__color = val
        self.dirty()

    @alpha.setter
    def alpha(self, val):
        self.__alpha = val
        self.dirty()
        
    @property
    def x(self):
        return self.__x
    
    @property
    def y(self):
        return self.__y
    
    @property
    def width(self):
        return self.__width
    
    @property
    def height(self):
        return self.__height
        
    @x.setter
    def x(self, val):
        self.__x = val
        self.dirty()

    @y.setter
    def y(self, val):
        self.__y = val
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
    def __init__(self, world=None, x1=None , y1=None , x2=None , y2=None , color=[0,0,0], alpha=1):
        super().__init__(world)
        
        if x1 is None and y1 is None and x2 is None and y2 is None:
            x1 = DEFAULT["Line"]["x1"]
            y1 = DEFAULT["Line"]["y1"]
            x2 = DEFAULT["Line"]["x2"]
            y2 = DEFAULT["Line"]["y2"]
        elif x1 is None and y1 is None:
            x1 = 0
            y1 = 0
        elif x2 is None and y2 is None:
            x2 = 0
            y2 = 0

        self.__x1 = x1
        self.__y1 = y1
        self.__x2 = x2
        self.__y2 = y2
        self.__color = color
        self.__alpha = alpha
        
        self.dirty()
        
    def draw(self):
        self.canvas().stroke_styled_line_segments([[(self.__x1,self.__y1),(self.__x2,self.__y2)]], color=self.__color)
    
    @property
    def color(self):
        return self.__color
    
    @property
    def alpha(self):
        return self.__alpha
        
    @color.setter
    def color(self, val):
        self.__color = val
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
    def __init__(self, world=None, x=None , y=None , radius=None, color=[0,0,0], alpha=1):
        super().__init__(world)
        
        if x is None and y is None:
            x = 0
            y = 0
        if radius is None:
            radius = DEFAULT["Circle"]["radius"]
            
        self.__x = x
        self.__y = y
        self.__radius = radius
        self.__color = color
        self.__alpha = alpha
        
        self.dirty()
        
    def draw(self):
        self.canvas().fill_styled_circles([self.__x], [self.__y], [self.__radius], color=self.__color)
    
    @property
    def color(self):
        return self.__color
    
    @property
    def alpha(self):
        return self.__alpha
        
    @color.setter
    def color(self, val):
        self.__color = val
        self.dirty()

    @alpha.setter
    def alpha(self, val):
        self.__alpha = val
        self.dirty()
        
    @property
    def x(self):
        return self.__x
    
    @property
    def y(self):
        return self.__y
    
    @property
    def radius(self):
        return self.__radius
        
    @x.setter
    def x(self, val):
        self.__x = val
        self.dirty()

    @y.setter
    def y(self, val):
        self.__y = val
        self.dirty()
        
    @radius.setter
    def radius(self, val):
        self.__radius = val
        self.dirty()