import asyncio
import gc
import time

loops = 0
max_wait_time = 60

while True:
    from tsukino import Tsukino
    print("Connecting...")
    Tsukino().run()

    asyncio.set_event_loop(asyncio.new_event_loop())
    loops += 1

    print("Cleaning up... ", end='')
    gc.collect()
    print("Done.")

    sleeptime = min(loops * 2, max_wait_time)
    if sleeptime:
        print("Restarting in {} seconds...".format(loops*2))
        time.sleep(sleeptime)