# P7_sim
Simulation of drone in isaac sim. Follow the guide below on how to set it up.

## Step 0:
Clone this repo and the submodules.

## Step 1:
Install [ISAAC SIM version 6.0.1](https://docs.isaacsim.omniverse.nvidia.com/6.0.1/installation/download.html) and build it from source.

## Step 2:
In a terminal, run:

```bash
export ISAACSIM_PATH=[path to isaacsim]
```

Install pegasus in isaac sims python terminal. It would normally be located under _build/(choose your distro)/release/python.sh.

The path is used in the following command and shall be executed in the (path to pegasus)/PegasusSimulator/extensions

```bash
bash (path to isaacsim python)/python.sh -m pip install --editable pegasus.simulator
```
## Step 3:

Find the config file located under:

P7_sim/PegasusSimulator/extensions/pegasus.simulator/config.yaml

Update the location for PX4-Autopilot.

## Step 4

Now PX4 needs to be built with zenoh. Inside the PX4-Autopilot folder run:
```bash
./Tools/docker_run.sh 'make px4_sitl_zenoh' # px4_fmu-v6x_zenoh
```

Then:
```bash
./Tools/docker_run.sh 'bash'
```

Inside the container run:
```bash
build/px4_sitl_zenoh/bin/px4
```

## Step 5
Ensure that

```bash
param show
```
Where:
x +   ZENOH_DOMAIN_ID [710,1916] : 42
x +   ZENOH_ENABLE [711,1917] : 1

If not set them via:

```bash
param set (Parameter) (Value)
```

## Step 5
Now Zenoh needs to be installed for Isaac sim to access it:
```bash
sudo apt install ros-jazzy-rmw-zenoh-cpp
```




# Launching Isaac sim
Open a terminal and run:
```bash
export RMW_IMPLEMENTATION=rmw_zenoh_cpp
export ROS_DOMAIN_ID=42
```

Then try running:
```bash
bash (path to isaacsim python)/python.sh (path to P7_sim)/main.py
```

## Get PX4 docker container for simple control
Run the following inside the PX4 folder terminal:
```bash
./Tools/docker_run.sh 'bash'
```
Then:
```bash
build/px4_sitl_zenoh/bin/px4
```


# docker run --rm -it --network host -e PX4_SIM_MODEL=gazebo-classic_iris px4io/px4-sitl:latest
