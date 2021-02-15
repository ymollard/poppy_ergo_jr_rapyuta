# Poppy Ergo Jr with rapyuta.io
This repository is intendend to control a tangible [Popppy Ergo Jr](https://www.poppy-project.org/en/robots/poppy-ergo-jr/) robot from the cloud through [rapyuta.io](https://rapyuta.io/).

## Scenario
The robot runs a pre-installed [ROS Kinetic controller](https://github.com/poppy-project/poppy_controllers) on top of the 16.04 Rapyta image for Raspberry Pi. The robot will infinitely move beetwen 2 poses, driven by [a node running in the cloud](https://github.com/ymollard/poppy_ergo_jr_rapyuta/blob/main/poppy_ergo_jr_move_example/src/move.py#L14-L20). 

## Quickstart
### 1. Create the new SD image for the robot
Start from a [16.04 ROS Kinetic rapyuta.io reference Board Support Package (BSP) image](https://storage.googleapis.com/io-reference-bsp-images/up/ubuntu/2018-08-23-rapyuta-robotics-xenial-ros-up-board-amd64.iso), connect you robot to the wifi using e.g. `wpa_supplicant.conf` or `nmcli device disconnect wlan0; nmcli d wifi connect <ESSID> password <WPA_KEY>` and then install former Poppy software for Ubuntu 16.04:

```bash
pip install pip==9.0.1
sudo apt install python-matplotlib python-scipy
sudo -H pip install ikpy==2.3.3
sudo -H pip install pypot==3.0.0
sudo -H pip install poppy-ergo-jr==2.0.0
sudo apt install ros-kinetic-control-msgs
cd catkin_ws/src && git clone https://github.com/poppy-project/poppy_controllers.git
cd .. && catkin_make_isolated
Delete the marker detector sensor from /usr/local/lib/python2.7/dist-packages/poppy_ergo_jr/configuration/*.json    # Old version of pypot buggy with the detector
sudo usermod -a -G dialout rapyuta
sudo usermod -a -G tty rapyuta
sudo nano /boot/cmdline.txt   # Drop the AMA0 console, it is needed for the motos
```

Reboot and make sure you can then start the controllers:
```bash
source ~/catkin_ws/devel/setup.bash
roslaunch poppy_controllers control.launch
```

#### 2. Onboard the robot in rapyuta.io
[Onboarding here](https://userdocs.rapyuta.io/developer-guide/manage-machines/onboarding/).
This is a pre-installed device, so **do not** select Use docker compose as default runtime option.
Click the created device and make sure rapyuta.io packages are fully installed and that the device appears to be connected before pursuing.

#### 3. Add builds and packages to rapyuta.io
Add 2 new builds of:
* **poppy_controllers** (for the device: Default build, for Kinetic)
* **poppy_ergo_jr_rapyuta** (for the cloud: catkin build, for Kinetic)

Add a new **poppy_move_2_poses** package with 3 components:
* **poppy_controllers** (Default build) in the device `roslaunch poppy_controllers control.launch` with:
  * Topic `/joint_states` QoS Maximum
  * Action `/follow_joint_trajectory`
* **moveit** (Catkin build) in the cloud `roslaunch poppy_ergo_jr_moveit_config demo.launch fake_execution:=true gripper:=true use_rviz:=false` with:
  * TODO: requires additional topics (see *To be continued* here under)
* **move_example** (Catkin build) in the cloud `roslaunch poppy_ergo_jr_move_example move.launch`
  * TODO: requires additional topics (see *To be continued* here under)

Reboot the device, ssh to the robot, `source ~/catkin_ws/devel/setup.bash` and start `roscore`.

#### 4. Deploy the package
Deploy **poppy_move_2_poses**: 2 components will start in the cloud and 1 on the robot, if connected.

## To be continued...
This is not fully working. MoveIt requires more topics and parameters to be opened through the network. Currently failing with the regular "MoveIt-not-started error":

```
[ERROR] [1613397758.592146652]: Robot model parameter not found! Did you remap 'robot_description'?
[FATAL] [1613397758.593794454]: Unable to construct robot model. Please make sure all needed information is on the parameter server.
Traceback (most recent call last):
  File "/opt/catkin_ws/src/poppy_ergo_jr_move_example/src/move.py", line 10, in <module>
    commander = moveit_commander.MoveGroupCommander("arm_and_finger")
  File "/opt/ros/melodic/lib/python2.7/dist-packages/moveit_commander/move_group.py", line 52, in __init__
    self._g = _moveit_move_group_interface.MoveGroupInterface(name, robot_description, ns, wait_for_servers)
RuntimeError: Unable to construct robot model. Please make sure all needed information is on the parameter server.
```
