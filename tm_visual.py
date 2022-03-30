import ipycanvas

# class poly():
#     def __init__(self, points, color, line, alpha):
#         self.color = color
#         self.line = line
#         self.alpha = alpha
    
#         self.width = max([p[0] for p in points]) = min([p[0] for p in points])
#         self.height = max([p[1] for p in points]) = min([p[0] for p in points])
        
#         self.center_x = min([p[0] for p in points]) + width/2
#         self.center_y = min([p[1] for p in points]) + height/2
    
#     def render(self):
    
    
class Canvas(ipycanvas.Canvas):
    
    def __init__(self, *args, **kwargs):
        super(Canvas, self).__init__()
        
        # set canvas to white
        self.fill_styled_rects([0],[0],[self.size[0]],[self.size[1]], color = [256,256,256])
        print("muyaho2")
        
    def box(self, x = None , y = None , width = None , height = None , color = [0,0,0], alpha=1):
        
        if x is None:
            x = self.size[0]/2
        
        if y is None:
            y = self.size[1]/2
        
        if width is None:
            width = self.size[0]/10
        
        if height is None:
            height =width
            
        
        coor_x = x - width /2
        coor_y = y - height /2
        self.fill_styled_rects([coor_x], [coor_y], [width], [height], [color], alpha=1)
    
    def ball(self, x = None , y = None , radius = None , color = [0,0,0], alpha=1):
        
        if x is None:
            x = self.size[0]/2
        
        if y is None:
            y = self.size[1]/2
        
        if radius is None:
            radius = self.size[0]/10
            
        self.fill_styled_circles([x], [y], [radius], [color], alpha=1)

                          
                          
# import time

# class World:
#   PERIOD = 10 # 10ms
#   def render(self) :
#     now = time.time()
#     if now - self.rendered_at < PERIOD :
#       return
#     # do render
#     self.rendered_at = now

# class Box:
#   def __init__(self, world):
#     self.world = world
  
#   @property
#   def x(self):
#     return self.__x

#   @x.setter
#   def x(self, val):
#     self.__x = val
#     self.world.render()