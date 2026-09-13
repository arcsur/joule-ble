# joule-ble

Asynchronous Python library for interfacing with ChefSteps and Breville Joule sous vide devices over Bluetooth Low Energy (BLE).

Designed following Home Assistant standards for Bluetooth integration libraries, supporting both passive advertisement discovery and active appliance control.

---

## Features

- **Hardware Generation Support**:
  - **Original ChefSteps Joule** (`CS10001` / `CS20001`): ChefSteps Stream GATT Service (`700b4321-9836-4383-a2b2-31a9098d1473`).
  - **Breville Joule Turbo** (`CS30001`): Breville FreeRTOS GATT Service (`c6f2d9e3-49e7-4125-9014-bfc6d669ff00`).
- **Complete Sous Vide Operations**:
  - Start cook program (setpoint temperature in °C, optional cook time, delayed start, holding temperature).
  - Adjust target temperature setpoint dynamically during cooking.
  - Stop heating and circulation.
  - Clear errors and faults.
  - Identify device (flashes indicator LED).
  - Authenticated session pairing and key exchange support.
- **Rich Live Telemetry**:
  - Bath water temperature (°C).
  - Heater temperature (°C).
  - Upper and lower control board temperatures (°C).
  - Motor RPM and motor current / PWM.
  - Program step (Idle, Preheating, Waiting for food, Cooking, Complete, Error).
  - Low water level and safety fault detection.
- **Home Assistant Standards**:
  - Modern `bleak` and `bleak-retry-connector` connection management with auto-reconnect handling.
  - Built-in `JouleBluetoothDeviceData` for BLE advertisement decoding and device discovery in config flows.
  - Fully typed dataclasses with native Celsius float representation.

---

## Installation

```bash
pip install joule-ble
```

---

## Quickstart

### 1. Advertisement Discovery (Config Flow)

```python
from bleak.backends.scanner import AdvertisementData
from bleak.backends.device import BLEDevice
from joule_ble import JouleBluetoothDeviceData

scanner_parser = JouleBluetoothDeviceData()

# Called from Home Assistant bluetooth scanner callback:
device_info = scanner_parser.update(ble_device, advertisement_data)
if device_info:
    print(f"Discovered {device_info.name} ({device_info.model}) at {device_info.mac_address}")
```

### 2. Controlling the Joule & Live Telemetry

```python
import asyncio
from bleak import BleakScanner
from joule_ble import JouleClient, JouleState, MIN_TEMP_C, MAX_TEMP_C

async def main():
    # Discover device
    device = await BleakScanner.find_device_by_filter(
        lambda d, adv: "joule" in (adv.local_name or "").lower()
    )
    if not device:
        print("No Joule found!")
        return

    client = JouleClient(device)

    # Listen for live status updates
    def state_updated(state: JouleState):
        print(
            f"Bath: {state.bath_temp_c}°C | Target: {state.target_temp_c}°C | "
            f"Step: {state.program_step} | RPM: {state.motor_rpm} | Low Water: {state.low_water}"
        )

    client.register_callback(state_updated)

    await client.connect()
    print("Connected! Device:", client.device_info)

    # Start heating to 54.0°C with a 1 hour timer (3600s)
    await client.start_cook(target_temp_c=54.0, cook_time_seconds=3600)
    await asyncio.sleep(10)

    # Change temperature setpoint to 55.0°C
    await client.set_temperature(55.0)
    await asyncio.sleep(10)

    # Stop cooking
    await client.stop_cook()
    await client.disconnect()

asyncio.run(main())
```

---

## Architecture & Protocols

The Joule uses Google Protocol Buffers (`StreamMessage`) transmitted across BLE GATT characteristics:
- **ChefSteps Stream Service**: `700b4321-9836-4383-a2b2-31a9098d1473`
  - Write: `700b4322-9836-4383-a2b2-31a9098d1473`
  - Subscribe: `700b4325-9836-4383-a2b2-31a9098d1473`
- **Breville Service**: `c6f2d9e3-49e7-4125-9014-bfc6d669ff00`
  - App Message (Write): `c6f2d9e3-49e7-4125-9014-bfc6d669ff09`
  - Appliance Message (Notify): `c6f2d9e3-49e7-4125-9014-bfc6d669ff08`

Messages exceeding the negotiated ATT MTU are automatically fragmented into chunks on transmission and reassembled upon reception.

---

## License

Apache 2.0
