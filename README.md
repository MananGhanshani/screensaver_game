# screensaver_game
🖥️ screensaver_game: Interactive Physics Sandbox


Overview
This project is a 2D physics simulation built using the Pygame library. It features multiple colored balls that interact with the screen boundaries (walls) under the influence of gravity and friction. The core feature allows users to interactively pick up, drag, and launch the balls using the mouse, making it a fun, dynamic physics sandbox.

Key Features
Newtonian Gravity: Balls are subject to a constant downward acceleration (gravity = 0.5).

Inelastic Wall Collisions: Balls bounce off all four boundaries (walls) with energy loss, governed by the ball's retention (coefficient of restitution).

Friction: Horizontal movement is reduced by friction when a ball is resting on the bottom boundary.

User Interaction:

Selection: Click and hold a ball to select it (selected = True).

Movement: Drag the selected ball with the mouse, overriding its physics simulation.

Launch: Releasing the ball calculates a precise motion vector based on the mouse's trajectory and launches the ball with that velocity.

Physics & Mechanics Explained
The simulation relies on the Ball class methods, primarily check_gravity() and update_pos(), to implement physics principles:

1. Kinematics (Position Update)
The ball's new position is calculated by simply adding its velocity components (speed) to its current coordinates:

New x=Current x+x_speed
New y=Current y+y_speed
2. Gravity and Vertical Motion
Acceleration: Gravity is constantly added to the vertical speed: self.y_speed += gravity.

Floor Bounce: When the ball hits the bottom wall (self.y_pos >= HEIGHT - self.radius - ...):

The vertical speed is reversed and reduced: self.y_speed = self.y_speed * -1 * self.retention.

To prevent continuous micro-bounces, if the rebound speed is less than bounce_stop (e.g., 3 pixels/frame), the speed is set to zero, and the ball's position is fixed to the floor.

Friction: When the ball is on the floor (self.y_speed == 0), horizontal speed is gradually reduced by the self.friction value.

3. Wall Collisions
The check_gravity() method also manages collisions with the top, left, and right walls. Upon collision, the relevant speed component is reversed and scaled by self.retention to simulate energy loss:

Horizontal Bounce: Hitting the left or right wall reverses the horizontal speed: self.x_speed *= -1 * self.retention.

Coordinate Fix: Safety checks are included to ensure the ball's center never goes beyond the valid bounds of the screen, guaranteeing visual and physical accuracy.

Code Architecture
Ball Class
The core component, representing an individual object in the simulation.

Attribute	Description	Example
x_pos, y_pos	Center coordinates.	50, 50
radius, color	Visual properties.	70, 'blue'
mass	Not currently used in collision, but key for future features.	1
retention	The coefficient of restitution (bounciness). 1.0 is perfectly elastic.	0.8
friction	Rate at which horizontal speed decreases on the floor.	0.02
x_speed, y_speed	Current velocity components (pixels/frame).	27.2, -12.3

Helper Functions
Function	Purpose
draw_walls()	Draws the four white lines representing the boundaries and returns a list of wall objects for collision reference.
calc_motion_vector()	Crucial for user launch. Analyzes the mouse_trajectory list (past 20 mouse positions) to calculate the average velocity of the mouse over that period. This calculated Δx and Δy provides the initial x_push and y_push for the launched ball.

Main Game Loop
The while run: loop manages the game's flow:

Frame Rate Control: timer.tick(fps) ensures consistent physics updates.

Input Tracking: The mouse position is continuously stored in mouse_trajectory.

Simulation Step: The loop iterates over all balls:

ball.draw(): Renders the ball.

ball.update_pos(): Moves the ball based on its speed, or sets its position to the mouse if selected.

ball.check_gravity(): Applies physics (gravity, friction, wall bouncing).

Event Handling: Responds to user input (QUIT, MOUSEBUTTONDOWN for selection, MOUSEBUTTONUP for launch).

How to Run
Dependencies: Ensure you have Python and Pygame installed.

Bash

pip install pygame
Execution: Save the code as a Python file (e.g., screensaver_game.py) and run it:

Bash

python screensaver_game.py
Future Enhancements
Ball-to-Ball Collision: Implement physics for when two balls collide, using their mass and retention properties to calculate the resulting velocities.

Variable Walls: Allow users to place movable/breakable internal walls.

Customization: Add options to change gravity, wall thickness, or ball properties via a simple GUI.

🧠 Building the Physics Sandbox: A Thought Process
I. Project Setup & Core Structure
The first step in building any game or simulation with Pygame is the basic setup.

The Game Loop and Timer
Thought Process: We need a mechanism to make the simulation run smoothly and consistently, regardless of how fast the user's computer is. This is where the game loop (while run:) and the Pygame Clock (timer.tick(fps)) come in.

Logic: By setting fps = 60 and calling timer.tick(fps), we ensure that our simulation updates its state (e.g., ball position, speed, gravity) exactly 60 times every second. This consistency is critical for reliable physics.

The Wall Boundary
Thought Process: The balls need an arena. Simple lines around the screen edge will suffice for the visual and physical boundaries. We define a fixed wall_thickness for both aesthetic drawing and precise collision detection.

Function: draw_walls()

This function simply draws four lines using pygame.draw.line. The key logic is remembering that the walls are drawn on the boundary of the WIDTH and HEIGHT coordinates.

II. The Ball Class: Bringing Objects to Life
The Ball class is the heart of the project. It encapsulates everything a ball is (its attributes) and everything it does (its methods).

Initialization (__init__)
Thought Process: What characteristics make one ball different from another? We need its location (x_pos, y_pos), size (radius), appearance (color), and its core physics properties (mass, retention, friction). We also give it an initial velocity (x_speed, y_speed) to start the movement.

Drawing the Ball (draw)
Thought Process: The ball needs to appear on the screen, and we need a way to check if the user clicks on it.

Logic: self.circle = pygame.draw.circle(...) draws the visual element. Crucially, the return value of pygame.draw.circle is a Pygame Rect object (self.circle), which is a perfect hit-box for interaction.

User Selection (check_select)
Thought Process: How does the program know if the user clicked this specific ball?

Logic: This method takes the mouse coordinates (pos) from the click event and uses the built-in Rect method: self.circle.collidepoint(pos). If the click lands inside the ball's hit-box, the ball's state is changed to self.selected = True.

III. Core Physics Engine (check_gravity)
This is the most complex method, responsible for applying all forces and managing boundary collisions.

1. Applying Gravity and Friction
Gravity Logic: If the ball is not being held by the user (if not self.selected) and isn't resting on the floor, we simply increase the vertical speed: self.y_speed += gravity.

Friction Logic: Friction only applies when the ball is on the ground and moving horizontally (if self.y_speed == 0 and self.x_speed != 0). We subtract a tiny amount (self.friction) from the x_speed in the opposite direction of motion (e.g., if x_speed > 0, we subtract friction). This simulates air resistance and surface drag.

2. Wall Collision and Bounce Logic
Thought Process: A ball hits a wall when its center is exactly one radius distance away from the wall's edge (plus half the wall thickness). The response must be to reverse the speed component perpendicular to that wall and reduce its magnitude based on bounciness (retention).

Bottom Wall (Floor) Logic:

Collision Check: if self.y_pos >= HEIGHT - self.radius - (wall_thickness/2)

Bounce Response: If the speed is high enough (> bounce_stop), we reverse it and apply loss: self.y_speed *= -1 * self.retention.

Resting State: If the bounce speed is too small, the simulation stops it completely (self.y_speed = 0). This prevents the ball from jittering endlessly at the bottom, achieving a stable resting state.

Side Walls (Left/Right) Logic:

Collision Check: We check two conditions: is the center near the left wall AND is the ball moving left (self.x_speed < 0), OR is the center near the right wall AND moving right (self.x_speed > 0).

Bounce Response: self.x_speed *= -1 * self.retention. The speed is reversed and reduced.

Zero Speed Fix: If the resulting horizontal speed is below bounce_stop, it is set to zero, and the ball's coordinate is fixed firmly against the wall.

IV. Interactivity and Launch Vector
Updating Position (update_pos)
Thought Process: This method has two modes: free movement and user control.

Logic:

Free Movement: self.y_pos += self.y_speed, self.x_pos += self.x_speed. The ball moves using its calculated physics velocity.

User Control: self.x_pos = mouse[0], self.y_pos = mouse[1]. If selected, the ball ignores physics and follows the mouse exactly.

Calculating the Launch (calc_motion_vector)
Thought Process: When the user releases the ball, we want to give it momentum based on how fast the mouse was moving. A simple difference between the start and end of the drag is too abrupt. We need an average velocity over the last few frames.


Logic:We continuously track the last 20 mouse positions in mouse_trajectory.When calculating the launch vector, we find the difference between the last position (mouse_trajectory[-1]) and an older position (e.g., mouse_trajectory[0]).

We divide this position difference (distance $\Delta x$ or $\Delta y$) by the number of frames (len(mouse_trajectory)), which yields the average velocity (distance/time).This result is x_push and y_push, which are then instantly assigned to the ball's x_speed and y_speed when the mouse button is released (pygame.MOUSEBUTTONUP). 

This translates the user's quick hand movement into realistic kinetic energy.

📝 Conclusion
This Pygame project successfully implements a dynamic 2D physics sandbox where multiple balls interact with gravity, friction, and environmental boundaries.

The architecture centers around the Ball class, which encapsulates the physical state and kinematic behavior of each object. The simulation achieves realism by:

Applying Newtonian principles (constant acceleration due to gravity) to y_speed.

Handling inelastic collisions with walls by reversing velocity components and applying energy loss via the retention factor.

Implementing friction to bring horizontal motion to rest when balls settle on the floor.

Integrating user interactivity through the mouse, allowing users to temporarily override the physics engine and, crucially, to launch the balls with accurate momentum calculated from the motion vector of their mouse trajectory.

The result is a stable, visually engaging simulation that serves as a robust foundation for future enhancements, such as implementing ball-to-ball collision physics or introducing more complex interactive elements.
