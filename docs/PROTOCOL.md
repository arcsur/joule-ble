# Joule Bluetooth Low Energy (BLE) Protocol Specification

This document details the reverse-engineered GATT architecture, message framing, and interaction sequence for ChefSteps and Breville Joule sous vide immersion circulators.

---

## 1. Device Profiles & GATT Services

| Model | Marketing Name | Primary Service UUID | Framing Style | Key Exchange |
|---|---|---|---|---|
| **CS10001 / J7** | ChefSteps Original Joule | `700b4321-9836-4383-a2b2-31a9098d1473` | Read/Write + Alert Notify | **None** |
| **CS20001 / J7** | ChefSteps White Joule | `700b4321-9836-4383-a2b2-31a9098d1473` | Read/Write + Alert Notify | **None** |
| **CS30001** | Breville Joule Turbo | `c6f2d9e3-49e7-4125-9014-bfc6d669ff00` | Feed Notify + App Msg Write | **Required** |

---

## 2. ChefSteps GATT Profile (`700b4321-...`)

### Characteristics

* **`700b4322-9836-4383-a2b2-31a9098d1473` (Stream Write)**
  * **Properties**: `Write` (or `Write Without Response` on some revisions)
  * **Behavior**: Receives serialized `joule.proto` `StreamMessage` frames. Must be written as an unfragmented buffer with `response=True` (`WRITE_TYPE_DEFAULT`).
* **`700b4323-9836-4383-a2b2-31a9098d1473` (Stream Read)**
  * **Properties**: `Read`
  * **Behavior**: Holds the pending response `StreamMessage` buffer (e.g. `IdentifyCirculatorReply` or telemetry `CirculatorDataPoint`).
* **`700b4325-9836-4383-a2b2-31a9098d1473` (Stream Subscribe / Alert)**
  * **Properties**: `Notify`
  * **Behavior**: Fires 4-byte alert notification packets (alert counter). The client must treat this notification as an alert trigger to perform a GATT Read on `700b4323`.
* **`700b4326-9836-4383-a2b2-31a9098d1473` (OTA File Write)**
  * **Properties**: `Write Without Response`
  * **Behavior**: Used exclusively for bulk firmware transfer blocks.

### Interaction Sequence: ChefSteps Identify Query

```
Client                                                  Joule Peripheral
  |                                                           |
  |--- Connect & Subscribe to 700b4325 ---------------------->|
  |<-- Subscription Confirmed --------------------------------|
  |    [Wait 500ms Radio Settle Delay]                        |
  |                                                           |
  |--- Write 700b4322 (StreamMessage: IdentifyCirculatorReq)->|
  |<-- GATT Write Confirmation (response=True) ---------------|
  |                                                           |
  |<-- Notification on 700b4325 (4-byte alert) ---------------|
  |--- Read 700b4323 ---------------------------------------->|
  |<-- Read 700b4323 Reply (StreamMessage: IdentifyReply) ----|
  |    [Parse Name, Serial, Hardware J7, Firmware 7.100]      |
```

---

## 3. Breville GATT Profile (`c6f2d9e3-...`)

### Characteristics

* **`c6f2d9e3-49e7-4125-9014-bfc6d669ff09` (App Message Write)**
  * **Properties**: `Write` (`WRITE_TYPE_DEFAULT`, `response=True`).
* **`c6f2d9e3-49e7-4125-9014-bfc6d669ff0b` (App Feed Notification)**
  * **Properties**: `Notify`. Continuous periodic stream of telemetry `CirculatorDataPoint` Protobuf messages.

---

## 4. Protobuf Stream Framing Rules

Every request and reply is wrapped in a top-level `StreamMessage` defined in `joule.proto`:

```protobuf
message StreamMessage {
  optional uint32 handle = 1;
  optional bytes senderAddress = 2;
  optional bytes recipientAddress = 3;
  // Payload oneof...
  optional IdentifyCirculatorRequest identifyCirculatorRequest = 10;
  optional IdentifyCirculatorReply identifyCirculatorReply = 11;
  ...
}
```

* **Handle**: Unique request counter (e.g. `2389`).
* **Sender Address**: Default `b"ABCDABCD"` (8 bytes).
* **Recipient Address**: The target circulator's 8-byte recipient hardware ID obtained from BLE Manufacturer Data (Company ID `345` / `0x0159`).
