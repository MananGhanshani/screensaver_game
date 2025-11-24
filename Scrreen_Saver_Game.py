import pygame

pygame.init()

WIDTH = 1000
HEIGHT = 800
screen = pygame.display.set_mode([WIDTH,HEIGHT])

fps = 60
timer = pygame.time.Clock()

#game variables

wall_thickness = 10
gravity = 0.5
bounce_stop = 3

#trackposition of mouse to get movemt  vector
mouse_trajectory = []

class Ball:
        # methods
        def __init__(self,x_pos,y_pos, radius , color, mass, retention,y_speed,x_speed,id,friction):
                # self is an parameter here it is an instance refrence/ handler
                # x,y,color,mass,retention these are attributes / variables for instances
                # self is an parameter when objects / instances 
                # are passed through  it becomes a argument
                # these all are attributes from arguments
                self.x_pos = x_pos
                self.y_pos = y_pos
                self.radius = radius
                self.color = color
                self.mass = mass
                self.retention = retention
                self.y_speed = y_speed
                self.x_speed = x_speed
                self.id = id
                self.friction = friction
                # these are attributes set internally (default state )
                self.circle = ''
                self.selected = False
                              
        def draw(self):
                # takes no in put just type .draw()
                # makes an visual and actual object that is interactable with inputs
                self.circle = pygame.draw.circle(screen , self.color, (self.x_pos, self.y_pos) ,self.radius)
        
        def check_gravity(self):
                # in this snippet returns y_speed and modifies x_speed
                
                if not self.selected:
                        
                        # apply gravity if not resting or selected 
                        if self.y_speed != 0 or self.y_pos < HEIGHT - self.radius - (wall_thickness/2):
                                self.y_speed += gravity
                                
                        # apply friction 
                        if self.y_speed == 0 and self.x_speed != 0:
                                if self.x_speed > 0:
                                        self.x_speed -= self.friction
                                elif self.x_speed <0:
                                        self.x_speed += self.friction
                                
                        # bottom wall logic
                        if self.y_pos >= HEIGHT - self.radius - (wall_thickness/2):
                                # if y coords are greater than it should be
                                # to check if certer has moved farther 
                                # below accesisable region or touches it  
                                if self.y_speed > bounce_stop:
                                        self.y_speed = self.y_speed * -1 * self.retention
                                        # negates the speed with some loss
                                else:
                                        if abs(self.y_speed) <= bounce_stop:
                                        # less than negligible make it stop and fix coords
                                                self.y_speed = 0
                                self.y_pos = HEIGHT - self.radius - (wall_thickness/2) # <-- Safety
                        
                        # top wall logic
                        elif self.y_pos <= self.radius + (wall_thickness/2):
                                # if y coords are less that they should be 
                                # to check if ball has moved farther
                                # above the top boundary or touching it
                                if self.y_speed < -bounce_stop: 
                                        # Check if it's moving *up* fast enough to bounce
                                        self.y_speed *= -1 * self.retention
                                        #  negates the value with some reduction
                                else:
                                        if abs(self.y_speed) <= bounce_stop:
                                        # less than negligible make it stop and fix coords
                                                self.y_speed = 0
                                
                        # side wall logics
                        if (self.x_pos < self.radius + (wall_thickness/2) and self.x_speed < 0) or \
                                (self.x_pos > WIDTH - self.radius - (wall_thickness/2) and self.x_speed > 0):
                                #is the ball is touching left wall and if so it its speed towards left wall        
                                #is the ball is touching right wall and if so it its speed towards right wall   
                                        self.x_speed *= -1 * self.retention
                                        # change speed in opposite direction with some reduction 
                                        if abs(self.x_speed) < bounce_stop:
                                        # less than negligiable then make x speeed zero and fix coords 
                                                self.x_speed = 0
                                                if (self.x_pos < self.radius + (wall_thickness/2) and self.x_speed < 0):
                                                        # still at left wall fix coords 
                                                        self.x_pos = self.radius + (wall_thickness/2)
                                                elif (self.x_pos > WIDTH - self.radius - (wall_thickness/2) and self.x_speed > 0):
                                                        # still at right wall fix coords
                                                        self.x_pos = WIDTH - self.radius - (wall_thickness/2)

                else:
                        self.x_speed = x_push
                        self.y_speed = y_push
                return self.y_speed
        
        def check_select(self, pos): 
                # takes input as coords
                self.selected = False
                # original assumption that ball is not selected
                if self.circle.collidepoint(pos):
                        self.selected = True
                # as circle is an object on display
                # it checks if the input coords collide with circle
                # if yes then the circle is selected selected = True
                return self.selected
        
        def update_pos(self,mouse) :
                # takes input as coords
                if not self.selected:
                        self.y_pos += self.y_speed
                        self.x_pos += self.x_speed
                        # if ball is not selected by the user then
                        # the coords og ball will be based of velocity 
                else:
                        self.x_pos = mouse[0]
                        self.y_pos = mouse[1]
                        # if ball is selcted by the user then
                        # the coords of the ball will be (center) mouse position        
    
# functions
def draw_walls():
        # creates both visual and physical objects in form of boundries
        left    = pygame.draw.line(screen ,'white' , (0,0) , (0,HEIGHT), wall_thickness)
        right   = pygame.draw.line(screen ,'white' , (WIDTH,0) , (WIDTH,HEIGHT), wall_thickness)
        top     = pygame.draw.line(screen ,'white' , (0,0) , (WIDTH,0), wall_thickness)
        bottom  = pygame.draw.line(screen ,'white' , (0,HEIGHT) , (WIDTH,HEIGHT), wall_thickness)
        wall_list = [left,right, top , bottom]
        return wall_list

def calc_motion_vector():
        # if the ball is selected fiirst make velocity zero
        x_speed = 0
        y_speed = 0
        if len(mouse_trajectory) > 10:
                # if trajectory has enough frame data to perform reliable action
                # what mouse did with ball in min 1/6 sec would be the mment
                x_speed = (mouse_trajectory[-1][0] - mouse_trajectory[0][0]) / len(mouse_trajectory)
                # the latest x component of speed becomes new initial value x speed
                y_speed = (mouse_trajectory[-1][1] - mouse_trajectory[0][1]) / len(mouse_trajectory)
                # the latest y component of speed becomes new initial value of y speed
        return x_speed , y_speed

# these balls are objects/ instances of class ball  
ball1 = Ball(50, 50, 70, 'blue', 1, 0.8, 27.2, -12.3, 1,0.02)
ball2 = Ball(500, 500, 50, 'green', 3, 0.6, -30.3, 11.6, 2, 0.03)
ball3 = Ball(200, 200, 40, 'gold', 2, 0.8, 22.5, 22.7, 3, 0.04)
ball4 = Ball(700, 100, 60, 'red', 5, 1.000001, -14.6, -19.6, 4, 0.1)
ball5 = Ball(300, 700, 100, 'white', 6 , 0.4, 15.0,20.1, 5, 0.01)
ball6 = Ball(850, 400, 80, 'cyan', 7, 0.9, -5.0, -8.0, 6, 0.15)
balls = [ball1,ball2,ball3,ball4,ball5,ball6] 

#main game loop
run = True
while run:
        timer.tick(fps)
        screen.fill('black')
        walls =  draw_walls()
        
        # mouse tracking
        mouse_coords = pygame.mouse.get_pos()
        mouse_trajectory.append(mouse_coords)
        if len(mouse_trajectory) > 20:
                mouse_trajectory.pop(0)
        x_push, y_push = calc_motion_vector()
        
        for ball in balls:
                ball.draw()                 
                ball.update_pos(mouse_coords)
                ball.check_gravity()        
         
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        run = False
                # selecting ball by mouse down
                if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                                if ball1.check_select(event.pos) or ball2.check_select(event.pos) \
                                        or ball3.check_select(event.pos) or ball4.check_select(event.pos) \
                                                or ball5.check_select(event.pos) or ball6.check_select(event.pos):
                                                active_select = True
                # leaving it by mouse up
                if event.type == pygame.MOUSEBUTTONUP:
                        if event.button ==1:
                                active_select = False
                                for ball in balls:
                                        ball.selected = False
        pygame.display.flip()
        
pygame.quit()
