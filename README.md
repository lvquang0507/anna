# This is Anna
Anna is a line follow robot using Pi Camera
# Launch commands
- View robot with Rviz2
```
ros2 launch anna view.launch.py
```
- Gazebo simulation 
```
ros2 launch anna rsp_gz.launch.py world:=src/anna/worlds/robot_with_track.world
```