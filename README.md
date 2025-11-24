# screensaver_game
Game made with ball physics and GUI 
Overview
This is a Pygame application that simulates multiple colored balls bouncing within a rectangular screen area, treating the edges as walls.

Key Features:

Gravity: Balls are subject to a constant downward acceleration.
Bouncing/Collisions: Balls bounce off the four walls with a reduction in speed (inelastic collision), determined by their retention attribute.
Friction: When resting on the bottom wall (y_speed == 0), horizontal movement is reduced by friction.
User Interaction: Users can click and drag a ball to select it, move it with the mouse, and release it to launch it with a velocity based on the mouse's motion trajectory.
Resources
Pygame: The simulation uses the Pygame library for graphics, input handling, and game loop management.
Concepts: The physics is based on basic Newtonian mechanics, including velocity, acceleration (gravity), momentum (implicitly handled by speed changes after collision), and friction.
Code Explanation
The simulation is built around the main game loop, a Ball class, and a few helper functions.

1. Global Setup and Variables
   
Pygame Initialization: pygame.init(), screen setup (WIDTH, HEIGHT), and game timer (fps, timer).
Game Variables:
wall_thickness = 10: Defines the visual and functional thickness of the screen boundaries.
gravity = 0.5: The constant acceleration applied to the balls' y_speed.
bounce_stop = 3: If a ball's bounce speed is less than this value, it's considered to have stopped bouncing and its speed is set to zero (to prevent perpetual micro-bounces).
mouse_trajectory: A list used to store the mouse's past positions to calculate the launch vector when a ball is released.

2. The Ball Class
   
Each ball is an instance of the Ball class, carrying its unique properties:
Physical Properties: radius, mass, retention (for elasticity), and friction.
Kinematic Properties: x_pos, y_pos (position), x_speed, and y_speed (velocity).
State: The selected boolean tracks if the user is currently holding the ball.
The core physics logic is encapsulated in two methods:
check_gravity(): This method updates the ball's velocity (y_speed increases due to gravity). It is primarily responsible for Wall Collision Detection and Response. It checks if the ball's edges are touching any of the four boundaries and, if so, reverses the corresponding speed component while multiplying it by the retention value (e.g., self.y_speed *= -1 * self.retention). It also applies friction when the ball is on the floor.
update_pos(): This method updates the ball's position.
If not selected, it adds x_speed and y_speed to the current position.
If selected, it forces the ball's position to match the current mouse coordinates, preparing for user launch.

2. Game Loop (while run:)
   
The main loop continuously performs these steps at a rate defined by fps:
Drawing: Clears the screen to black and draws the static walls using draw_walls().
Mouse Tracking: Updates the mouse_trajectory and calculates the potential launch speed (x_push, y_push) using calc_motion_vector().
Ball Update: Loops through every ball, calling its draw(), update_pos(), and check_gravity() methods to advance the simulation one frame.
Event Handling: Listens for mouse clicks (MOUSEBUTTONDOWN) to select a ball and mouse releases (MOUSEBUTTONUP) to unselect a ball and launch it using the calculated x_push and y_push speeds.
The calc_motion_vector() function is crucial for interactivity. It determines the launch velocity by finding the difference between the most recent mouse position and an older mouse position within the trajectory list, dividing by the number of frames between them to get a velocity:















































































