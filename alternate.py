import asyncio
import aiofiles
from watchfiles import awatch
import nats
import os


asyncio.set_event_loop(asyncio.new_event_loop())


async def watch_directory(path):
    # while True:
    async for changes in awatch(path):
        for _, file_path in changes:
            async with aiofiles.open(file_path, mode="r") as f:
                contents = await f.read()
                device_name = os.path.splitext(os.path.basename(file_path))
                return contents, device_name[0]


async def main():
    nc = await nats.connect("nats://localhost:4222")
    message, device_name = await watch_directory("configs")
    await nc.publish(f"dc1.{device_name}.configure", message.encode())
    await nc.close()
    await main()


if __name__ == "__main__":
    asyncio.run(main())
