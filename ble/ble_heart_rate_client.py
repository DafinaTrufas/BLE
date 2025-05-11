import asyncio
from bleak import BleakScanner, BleakClient

HR_SERVICE_UUID = "0000180d-0000-1000-8000-00805f9b34fb"
HR_MEASUREMENT_CHAR_UUID = "00002a37-0000-1000-8000-00805f9b34fb"

def handle_hr_notify(sender, data):
    print(f"Heart Rate: {data[1]} bpm")

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

        print("Subscribing to Heart Rate notifications...")
        await client.start_notify(HR_MEASUREMENT_CHAR_UUID, handle_hr_notify)

        print("Waiting for heart rate updates... Press Ctrl+C to stop.")
        await asyncio.sleep(60)

        await client.stop_notify(HR_MEASUREMENT_CHAR_UUID)

asyncio.run(main())
