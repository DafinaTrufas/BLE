import asyncio
from bleak import BleakScanner, BleakClient

SERVICE_UUID = "00005678-0000-1000-8000-00805f9b34fb"
CHAR_UUID = "00002345-0000-1000-8000-00805f9b34fb"

def handle_notify(sender, data):
    print(data)

async def main():
    print("Scanning for BLE devices...")
    devices = await BleakScanner.discover()
    for i, d in enumerate(devices):
        print(f"{i}: {d.name} [{d.address}]")

    address = input("Enter the MAC address of the (simulated) peripheral: ")

    async with BleakClient(address) as client:
        print("Connected:", client.is_connected)

        services = await client.get_services()
        for service in services:
            print(f"[Service] {service.uuid}")
            for char in service.characteristics:
                print(f"  [Characteristic] {char.uuid} — {char.properties}")

        print("Subscribing to notifications...")
        await client.start_notify(CHAR_UUID, handle_notify)
        #value = await client.read_gatt_char(CHAR_UUID)
        #print(value)

        print("Waiting for updates... Press Ctrl+C to stop.")
        await asyncio.sleep(480)

asyncio.run(main())