import asyncio
import os

import aiofiles
import nats
from watchfiles import awatch


async def watch_directory(nc, path):
    async for changes in awatch(path):
        for _, file_path in changes:
            async with aiofiles.open(file_path, mode="r") as f:
                contents = await f.read()
                device_name = os.path.splitext(os.path.basename(file_path))
                await nc.publish(f"dc1.{device_name[0]}.configure", contents.encode())


async def main():
    nc = await nats.connect("nats://localhost:4222")
    await watch_directory(nc, "deployment/intended/configs")
    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())
