#!/usr/bin/env python
"""
| File: 1_px4_single_vehicle.py
| Author: Marcelo Jacinto (marcelo.jacinto@tecnico.ulisboa.pt)
| License: BSD-3-Clause. Copyright (c) 2023, Marcelo Jacinto. All rights reserved.
| Description: This files serves as an example on how to build an app that makes use of the Pegasus API to run a simulation with a single vehicle, controlled using the MAVLink control backend.
"""

# Imports to start Isaac Sim from this script
import carb
from isaacsim import SimulationApp

# Start Isaac Sim's simulation environment
# Note: this simulation app must be instantiated right after the SimulationApp import, otherwise the simulator will crash
# as this is the object that will load all the extensions and load the actual simulator.
simulation_app = SimulationApp({"headless": False})

# -----------------------------------
# The actual script should start here
# -----------------------------------
import omni.timeline
from isaacsim.core.api.world import World
from isaacsim.core.utils.extensions import enable_extension

enable_extension("isaacsim.ros2.bridge")

# Import the Pegasus API for simulating drones
from pegasus.simulator.params import ROBOTS, SIMULATION_ENVIRONMENTS
from pegasus.simulator.logic.state import State
from pegasus.simulator.logic.backends.px4_mavlink_backend import PX4MavlinkBackend, PX4MavlinkBackendConfig
from pegasus.simulator.logic.vehicles.multirotor import Multirotor, MultirotorConfig
from pegasus.simulator.logic.interface.pegasus_interface import PegasusInterface
from pegasus.simulator.logic.sensors import Barometer, IMU, Magnetometer, GPS
from pegasus.simulator.logic.thrusters import QuadraticThrustCurve
from pegasus.simulator.logic.dynamics import LinearDrag
from pegasus.simulator.logic.graphs import ROS2CameraGraph

# Auxiliary scipy and numpy modules
from pathlib import Path
from scipy.spatial.transform import Rotation

PROJECT_ROOT = Path(__file__).resolve().parent
PEGASUS_ROOT = PROJECT_ROOT / "PegasusSimulator"

class PegasusApp:
    """
    A Template class that serves as an example on how to build a simple Isaac Sim standalone App.
    """

    def __init__(self):
        """
        Method that initializes the PegasusApp and is used to setup the simulation environment.
        """

        # Acquire the timeline that will be used to start/stop the simulation
        self.timeline = omni.timeline.get_timeline_interface()

        # Start the Pegasus Interface
        self.pg = PegasusInterface()

        # Acquire the World, .i.e, the singleton that controls that is a one stop shop for setting up physics, 
        # spawning asset primitives, etc.
        self.pg._world = World(**self.pg._world_settings)
        self.world = self.pg.world

        # Launch one of the worlds provided by NVIDIA

        print("Loading environment...")
        print(str(PROJECT_ROOT / "forest_world.usd"))
        self.pg.load_environment(str(PROJECT_ROOT / "forest_world.usd"))

        # Create the vehicle
        # Try to spawn the selected robot in the world to the specified namespace
        config_multirotor = MultirotorConfig()
        # Create the multirotor configuration
        mavlink_config = PX4MavlinkBackendConfig({
            "vehicle_id": 0,
            "px4_autolaunch": True,
            "px4_dir": self.pg.px4_path,
            "px4_vehicle_model": self.pg.px4_default_airframe # CHANGE this line to 'iris' if using PX4 version bellow v1.14
        })
        config_multirotor.backends = [PX4MavlinkBackend(mavlink_config)]

        config_multirotor.stage_prefix = "quadrotor"
        config_multirotor.usd_file = str(
            PEGASUS_ROOT
            / "extensions/pegasus.simulator/pegasus/simulator/assets/Robots/x500v2/x500v2.usd"
        )

        # The default thrust curve for a quadrotor and dynamics relating to drag
        config_multirotor.thrust_curve = QuadraticThrustCurve()
        config_multirotor.drag = LinearDrag([0.50, 0.30, 0.0])

        # Set the sensors for a quadrotor
        # For each sensor we are using the default parameters, but you can also pass in a dictionary
        # to configure them. Check the Sensors API documentation for more information.
        config_multirotor.sensors = [Barometer(), IMU(), Magnetometer(), GPS()]

        # The backends for actually sending commands to the vehicle.
        # By default use mavlink (with default mavlink configurations).
        # It can also be your own custom Control Backend implementation!
        #
        # Note: you can have multiple backends (this is usefull for creating backends
        # for logging purposes) but only the first backend in the list will be used
        # to send commands to the vehicles. The others will just be used to receive the
        # current state of the vehicle and the data produced by the sensors


        # Create and spawn the multirotor object in the scene
        Multirotor(
                stage_prefix="/World/quadrotor",
                # The path to the multirotor USD file
                usd_file=config_multirotor.usd_file,
                vehicle_id=0,
                init_pos=[0.0, 0.0, 0.07],
                init_orientation=Rotation.from_euler("XYZ", [0.0, 0.0, 0.0], degrees=True).as_quat(),
                config=config_multirotor,
            )
        # Reset the simulation environment so that all articulations (aka robots) are initialized
        self.world.reset()

        # Auxiliar variable for the timeline callback example
        self.stop_sim = False

    def run(self):
        """
        Method that implements the application main loop, where the physics steps are executed.
        """

        # Start the simulation
        self.timeline.play()

        # The "infinite" loop
        while simulation_app.is_running() and not self.stop_sim:

            # Update the UI of the app and perform the physics step
            self.world.step(render=True)
        
        # Cleanup and stop
        carb.log_warn("PegasusApp Simulation App is closing.")
        self.timeline.stop()
        simulation_app.close()

def main():

    # Instantiate the template app
    pg_app = PegasusApp()

    # Run the application loop
    pg_app.run()

if __name__ == "__main__":
    main()
