import asyncio
import os

import nats
from napalm import get_network_driver

# Load DEVICE environment variable to build device construct
DEVICE = os.environ["DEVICE"]

device = {
    "hostname": DEVICE,
    "username": "admin",
    "password": "admin",
}


async def send_config_replace(data):
    driver = get_network_driver("eos")
    conn = driver(**device)
    try:
        print(f"Connecting to {device['hostname']}...")
        conn.open()  # Open the connection to the device
        print("Connection established.")

        # Load and preview the replacement configuration
        print("Loading configuration...")
        conn.load_replace_candidate(config=data)
        print("Configuration changes preview:")
        print(conn.compare_config())

        # Commit the changes
        if conn.compare_config():
            print("Applying configuration...")
            conn.commit_config()
            print("Configuration replaced successfully.")
        else:
            print("No changes detected. Skipping commit.")

    except Exception as e:
        print(f"An error occurred: {e}")
        # Rollback in case of any failure
        print("Rolling back configuration...")
        conn.rollback()
    finally:
        # Close the connection
        conn.close()
        print(f"Disconnected from {device['hostname']}.")


async def main():
    nc = await nats.connect("nats://nats:4222")

    async def message_handler(msg):
        subject = msg.subject
        data = msg.data.decode()
        print(f"Received message on subject '{subject}':\n{data}")
        await send_config_replace(data)

    await nc.subscribe(f"dc1.{DEVICE}.configure", cb=message_handler)
    # Wait indefinitely until the program is interrupted
    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())
