"""
Defines tasks for BLE (Bluetooth Low Energy) connections.

Based on original pre-COVID work by [Nicholas H.Tollervey.](https://ntoll.org/)

Copyright (c) 2019-present Invent contributors.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import asyncio
import invent
from pyscript import window
from pyscript.ffi import create_proxy

try:
    window.navigator.bluetooth
    BLE_AVAILABLE = True
except AttributeError:
    BLE_AVAILABLE = False

#: Active BLE connections, keyed by channel name.
BLE_CONNECTIONS = {}


class _InventBLE:
    """
    Manage a BLE (Bluetooth Low Energy) connection bound to a channel.

    Opens a BLE connection to a device selected by the user via the
    browser's device picker, and binds it to the specified channel.

    The `channel` argument is the channel name to use for all communication.

    The `service` and `characteristic` arguments are the UUIDs of the GATT
    service and characteristic to interact with on the device. Either a full
    128-bit UUID string or a short 16-bit alias (e.g. ``"heart_rate"`` or
    ``"0x180d"``) may be used.

    The optional `filters` argument accepts a list of device-filter
    dictionaries in the same format as the Web Bluetooth API (e.g.
    ``[{"services": ["heart_rate"]}]``).  When omitted the browser picker
    shows all nearby BLE devices.

    The optional `optional_services` argument lists additional service UUIDs
    that the page needs access to beyond the primary `service`.

    All communication with the BLE device is via the channel:

    - Publish a message with subject ``"send"`` and a ``.data`` attribute
      containing ``bytes`` or ``str`` to write to the characteristic.
    - Publish a message with subject ``"close"`` to disconnect.
    - Subscribe to the channel with subject ``"message"`` to receive incoming
      characteristic notifications (arrives as ``.data`` of type ``bytes``).
    - Subscribe to the channel with subject ``"status"`` to receive connection
      state changes (arrives as ``.status``, one of: ``"connecting"``,
      ``"open"``, ``"error"``, ``"closed"``).

    .. note::

        The Web Bluetooth API requires an HTTPS origin and a user gesture to
        open the device picker.  Only Bluetooth **Low Energy** (BLE) devices
        are supported; Bluetooth Classic devices (including audio streaming)
        are not accessible via this API.

    Example usage::

        # Connect to a BLE heart-rate monitor.
        ble.ble(
            channel="heart_rate",
            service="0000180d-0000-1000-8000-00805f9b34fb",
            characteristic="00002a37-0000-1000-8000-00805f9b34fb",
        )

        # Receive heart-rate measurements.
        def on_measurement(message):
            print("Heart rate data:", message.data)

        invent.subscribe(
            handler=on_measurement,
            to_channel="heart_rate",
            when_subject="message",
        )

        # Track connection state.
        def on_status(message):
            print("Status:", message.status)

        invent.subscribe(
            handler=on_status,
            to_channel="heart_rate",
            when_subject="status",
        )

        # Write a command to the device.
        invent.publish(
            message=invent.Message("send", data=b"\\x01"),
            to_channel="heart_rate",
        )

        # Close the connection.
        invent.publish(
            message=invent.Message("close"),
            to_channel="heart_rate",
        )
    """

    def __init__(
        self,
        channel,
        service=None,
        characteristic=None,
        filters=None,
        optional_services=None,
    ):
        """
        Initialise the BLE connection and bind to the channel.

        Args:
            channel: Channel name used for all send/receive communication.
            service: UUID of the primary GATT service to connect to.
            characteristic: UUID of the GATT characteristic to read, write,
                and subscribe to notifications on.
            filters: Optional list of Web Bluetooth device-filter dicts.  When
                omitted, ``acceptAllDevices`` is used so all nearby BLE devices
                appear in the browser picker.
            optional_services: Optional list of additional service UUIDs to
                request access to alongside ``service``.
        """
        if channel in BLE_CONNECTIONS:
            raise ValueError(f"Already connected on channel '{channel}'.")
        BLE_CONNECTIONS[channel] = self
        self.channel = channel
        self.service_uuid = service
        self.characteristic_uuid = characteristic
        self._device = None
        self._server = None
        self._service_obj = None
        self._characteristic_obj = None
        self._ready = asyncio.Event()
        self._value_changed_proxy = None

        # Build the requestDevice options dict.
        options = {}
        if filters:
            options["filters"] = filters
        else:
            options["acceptAllDevices"] = True
        extra_services = list(optional_services or [])
        if service and service not in extra_services:
            extra_services.append(service)
        if extra_services:
            options["optionalServices"] = extra_services
        self._options = options

        # Subscribe to the channel for send and close commands.
        invent.subscribe(
            handler=self._handle_send,
            to_channel=channel,
            when_subject="send",
        )
        invent.subscribe(
            handler=self._handle_close,
            to_channel=channel,
            when_subject="close",
        )

        # Publish initial connecting status and begin async connection.
        self._publish_status("connecting")
        asyncio.create_task(self._connect())

    def _publish_status(self, status):
        """
        Publish a status message to the channel.
        """
        invent.publish(
            message=invent.Message("status", status=status),
            to_channel=self.channel,
        )

    def _cleanup(self):
        """
        Remove from the registry, unsubscribe handlers, and detach the
        characteristic event listener.

        Unsubscribe calls are guarded so that cleanup is always safe to call
        even if the channel has already been cleared (e.g. by the test
        framework between async tasks).
        """
        BLE_CONNECTIONS.pop(self.channel, None)
        try:
            invent.unsubscribe(
                handler=self._handle_send,
                from_channel=self.channel,
                when_subject="send",
            )
        except (ValueError, KeyError):
            pass
        try:
            invent.unsubscribe(
                handler=self._handle_close,
                from_channel=self.channel,
                when_subject="close",
            )
        except (ValueError, KeyError):
            pass
        if self._characteristic_obj and self._value_changed_proxy:
            try:
                self._characteristic_obj.removeEventListener(
                    "characteristicvaluechanged",
                    self._value_changed_proxy,
                )
            except Exception:
                pass
            self._value_changed_proxy = None

    async def _connect(self):
        """
        Request a device from the browser picker, connect to its GATT server,
        obtain the configured service and characteristic, then start
        notifications.  Any failure publishes an ``"error"`` status and cleans
        up.
        """
        try:
            self._device = await window.navigator.bluetooth.requestDevice(
                self._options
            )
            self._server = await self._device.gatt.connect()
            if self.service_uuid:
                self._service_obj = await self._server.getPrimaryService(
                    self.service_uuid
                )
                if self.characteristic_uuid:
                    self._characteristic_obj = (
                        await self._service_obj.getCharacteristic(
                            self.characteristic_uuid
                        )
                    )
                    self._value_changed_proxy = create_proxy(
                        self._on_value_changed
                    )
                    self._characteristic_obj.addEventListener(
                        "characteristicvaluechanged",
                        self._value_changed_proxy,
                    )
                    await self._characteristic_obj.startNotifications()
            self._ready.set()
            self._publish_status("open")
        except Exception:
            self._cleanup()
            self._publish_status("error")

    def _on_value_changed(self, event):
        """
        Convert the incoming JavaScript ``DataView`` to Python ``bytes`` and
        publish the data to the channel.
        """
        data_view = event.target.value
        data = bytes(
            data_view.getUint8(i) for i in range(data_view.byteLength)
        )
        invent.publish(
            message=invent.Message("message", data=data),
            to_channel=self.channel,
        )

    def _handle_send(self, message):
        """
        Write data to the characteristic.  If the connection is not yet open,
        queue the write until it is ready.
        """
        if self._ready.is_set():
            asyncio.create_task(self._write(message.data))
        else:

            async def _wait_and_write():
                """
                Wait for readiness then write.
                """
                await self._ready.wait()
                await self._write(message.data)

            asyncio.create_task(_wait_and_write())

    async def _write(self, data):
        """
        Serialise and write data to the characteristic.
        """
        if not self._characteristic_obj:
            return
        if isinstance(data, str):
            data = data.encode("utf-8")
        if isinstance(data, (bytes, bytearray)):
            await self._characteristic_obj.writeValueWithResponse(data)

    def _handle_close(self, message):
        """
        Initiate an orderly disconnection.
        """
        asyncio.create_task(self._disconnect())

    async def _disconnect(self):
        """
        Stop notifications, disconnect the GATT server, clean up, and publish
        the ``"closed"`` status.
        """
        if self._characteristic_obj:
            try:
                await self._characteristic_obj.stopNotifications()
            except Exception:
                pass
        if self._device:
            try:
                self._device.gatt.disconnect()
            except Exception:
                pass
        self._cleanup()
        self._publish_status("closed")


# Expose the class as a module-level function for ease of use.
ble = _InventBLE
