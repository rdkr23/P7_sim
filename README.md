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

## Step 4:
Try running the script:
```bash
bash (path to isaacsim python)/python.sh (path to P7_sim)/main.py
```


## Get PX4 docker container for simple control
Run the following inside the PX4 folder terminal:
```bash
docker run --rm -it --network host -e PX4_SIM_MODEL=gazebo-classic_iris px4io/px4-sitl:latest
```


