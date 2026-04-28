# ChirpStack to Azure IoT Hub Bridge

This bridge allows you to forward messages from a ChirpStack MQTT broker to Azure IoT Hub.

## Security & Maintenance (Updated April 2026)

This project has been updated to address critical security vulnerabilities and use the latest SDKs:

- **python-dotenv (1.2.2)**: Fixed CVE-2026-28684 (Path Traversal).
- **paho-mqtt (2.1.0)**: Fixed CVE-2025-10543 (Integer Truncation).
- **azure-iot-device (3.1.0)**: Upgraded to the latest major version for MQTT 5.0 support and security patches.

## Requirements

- Python 3.9+
- ChirpStack Network Server
- Azure IoT Hub

## Installation

1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure your environment variables in a `.env` file (see `.env-sample`).

## Implementation Details

The bridge uses the `paho-mqtt` 2.x client with `CallbackAPIVersion.VERSION1` for compatibility. Messages sent to Azure IoT Hub are now explicitly configured with `application/json` content type and `utf-8` encoding to ensure proper routing and processing.

## Running the Bridge

```bash
python bridge_chirpstack_iothub.py
```

Or using Docker:

```bash
docker build -t chirpstack-iothub-bridge .
docker run --env-file .env chirpstack-iothub-bridge
```
