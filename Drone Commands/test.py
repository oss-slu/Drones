import asyncio
from mavsdk import System

async def run():
    # Connect to the drone
    drone = System()
    print('connecting')
    await drone.connect(system_address="serial:///dev/serial0:57600")
    print('connected')

    print("arming")
    await drone.action.arm()

    print("take off")
    await drone.param.set_param_float("MIS_TAKEOFF_ALT", 1.0)
    await drone.action.takeoff()

    await asyncio.sleep(5)

    print("landing")
    await drone.action.land()

    await drone.action.disarm()



# Run the asyncio loop
asyncio.run(run())
