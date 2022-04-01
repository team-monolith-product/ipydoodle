import ipycanvas
import time
import threading

FREQUENCY = 30
DEFAULT = {
            "Box" : {"width":100,
                    "height":100},
            "Ball" : {"radius":50}
          }

CURRENT_WORLD = None


class Canvas(ipycanvas.Canvas):
    def clear(self):
        super().clear()
        self.fill_styled_rects([0],[0],[self.size[0]],[self.size[1]], color = [256,256,256])
    
    def move_coor(self, x, y):
        moved_x = [xx + self.size[0]/2 for xx in x]
        moved_y = [self.size[1]/2 - yy for yy in y]
        return moved_x, moved_y
    
    def moved_coor_rect_center(self, x, y, width, height):
        moved_x = [xx - width[i]/2 for i, xx in enumerate(x)]
        moved_y = [yy + height[i]/2 for i, yy in enumerate(y)]
        return moved_x, moved_y
    
    def fill_styled_rects(self, x, y, width, height, color, alpha=1):
        x,y = self.move_coor(*self.moved_coor_rect_center(x,y,width,height))
        super().fill_styled_rects(x, y, width, height, color, alpha)
        
        
class World:
    def __init__(self):
        self.canvas = Canvas()
        self.objects = []
        
        global CURRENT_WORLD
        CURRENT_WORLD = self
        
        # set canvas to white
        self.canvas.clear()
        
        display(self.canvas)
    
    def render(self):
        with ipycanvas.hold_canvas(self.canvas):
            self.canvas.clear()
            for obj in self.objects:
                obj.draw()
                
    # with condition -> 하위 obj 가 변경되었을때 호출 
    def dirty(self):
        self.render()
    
    def move_coor(self, x, y):
        moved_x = x + self.canvas.size[0]/2
        moved_y = self.canvas.size[1]/2 - y
        return moved_x, moved_y

            
class Object:
    def __init__(self, world=None, color=[0,0,0], alpha=1):
        if not world:
            global CURRENT_WORLD
            if not CURRENT_WORLD:
                CURRENT_WORLD = World()
            self.world = CURRENT_WORLD
        else:
            self.world = world

        self.world.objects.append(self)

        
class Box(Object):
    def __init__(self, world=None, x=None , y=None , width=None , height=None , color=[0,0,0], alpha=1):
        super(Box,self).__init__(world, color, alpha)
        
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
        
        self.world.dirty()
        
    def draw(self):
        self.world.canvas.fill_styled_rects([self.__x], [self.__y], [self.__width], [self.__height], [self.__color], alpha=self.__alpha)
    
    @property
    def color(self):
        return self.__color
    
    @property
    def alpha(self):
        return self.__alpha
        
    @color.setter
    def color(self, val):
        self.__color = val
        self.world.dirty()

    @alpha.setter
    def alpha(self, val):
        self.__alpha = val
        self.world.dirty()
        
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
        self.world.dirty()

    @y.setter
    def y(self, val):
        self.__y = val
        self.world.dirty()
        
    @width.setter
    def width(self, val):
        self.__width = val
        self.world.dirty()

    @height.setter
    def height(self, val):
        self.__height = val
        self.world.dirty()