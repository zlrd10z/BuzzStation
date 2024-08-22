import asyncio
from libs.keypad import Keypad
from gui import gui_playlist
from core.data_storage import DataStorage
from core.playlist import playlist_loop
from core.potentiometers_operations import potentiometersOperations
import time


async def main():
    # Create objects:
    keys = Keypad()
    data_storage = DataStorage()
    await asyncio.gather(
        potentiometersOperations(data_storage),
        playlist_loop(keys, data_storage)
    )

if __name__ == "__main__":
    asyncio.run(main())
