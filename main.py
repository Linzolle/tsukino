import asyncio
import gc

from tsukino import Tsukino

Tsukino().run()

asyncio.set_event_loop(asyncio.new_event_loop())

print("Cleaning up... ", end='')
gc.collect()
print("Done.")