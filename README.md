<h1> Walking in the light </h1>

<p>
For this project, we propose the design of a dynamic lighting system for handrails or corridors.
Instead of having an always-on lighting system, our design makes use of a light strand attached to a kinect via a raspberry pi. 
When a person is detected the corresponding lights in the strand will be turned on, then switched off again as the person passes.
The persons movement speed will be calculated to allow for a system of lights that guides people to their destinations.
The final system will light the area in front of and behind a person and provide a traveling light moving at the same speed as the person walking.
</p>


<h2> Scientific Goals: </h2>
<p>
The main scientific goals of this project are to detect a person from RGB images and a density point cloud, predict their future movement speed and automate a corridor\hallway lighting to match the individuals speed.
In this case the input to the system would consist of an RGB image and point cloud.
The system will then determine whether or not an individual is present in the scene.
The output of the system will be a traveling light that matches the individuals traveling speed.
The persons continued movement speed could be estimated and their future speed\position can be calculated using a Kalman filter.
This predicted speed would then be used to light the hallway for the person.
</p>

<h2> Engineering Goals: </h2>
<p>
The main engineering goals for this project are to provide the campus with a more environmentally friendly lighting system.
Here lights will only be used in areas that are being occupied.
This is in contrast to having lights turned on in an area that isn't being utilized.
</p>

