import asyncio
import invent
import umock
import upytest
from invent.tools import ble


def setup():
    """Clean up any lingering BLE connections before each test."""
    for channel in list(ble.BLE_CONNECTIONS.keys()):
        invent.publish(
            message=invent.Message("close"),
            to_channel=channel,
        )
    ble.BLE_CONNECTIONS.clear()


# ── Mock helpers ──────────────────────────────────────────────────────────────


class _MockDataView:
    """Minimal Python stand-in for a JavaScript DataView."""

    def __init__(self, data):
        self._data = list(data)
        self.byteLength = len(data)

    def getUint8(self, i):
        return self._data[i]


class _MockEvent:
    """Minimal Python stand-in for a characteristicvaluechanged Event."""

    class _Target:
        def __init__(self, data_view):
            self.value = data_view

    def __init__(self, data):
        self.target = self._Target(_MockDataView(data))


class _MockCharacteristic:
    """Mock GATT characteristic."""

    def __init__(self):
        self._listeners = {}
        self.written = []

    def addEventListener(self, event, callback):
        self._listeners.setdefault(event, []).append(callback)

    def removeEventListener(self, event, callback):
        callbacks = self._listeners.get(event, [])
        try:
            callbacks.remove(callback)
        except ValueError:
            pass

    async def startNotifications(self):
        pass

    async def stopNotifications(self):
        pass

    async def writeValueWithResponse(self, data):
        self.written.append(data)

    def simulate_notification(self, data):
        """Fire a characteristicvaluechanged event with the given bytes."""
        event = _MockEvent(data)
        for cb in list(self._listeners.get("characteristicvaluechanged", [])):
            cb(event)


class _MockService:
    def __init__(self, characteristic):
        self._characteristic = characteristic

    async def getCharacteristic(self, uuid):
        return self._characteristic


class _MockServer:
    def __init__(self, service):
        self._service = service

    async def getPrimaryService(self, uuid):
        return self._service


class _MockGATT:
    def __init__(self, server):
        self._server = server
        self.connected = True

    async def connect(self):
        return self._server

    def disconnect(self):
        self.connected = False


class _MockDevice:
    def __init__(self, server):
        self.gatt = _MockGATT(server)


def _make_mock_bluetooth(device):
    """Return an async callable that resolves to *device*."""

    async def mock_request_device(options):
        return device

    return mock_request_device


# ── Tests ─────────────────────────────────────────────────────────────────────


async def test_ble_connecting_status_on_init():
    """
    Creating a BLE connection should immediately publish a 'connecting'
    status before any async work begins.
    """
    channel = "test_ble_connecting"
    got_connecting = asyncio.Event()
    got_closed = asyncio.Event()

    def on_status(message):
        if message.status == "connecting":
            got_connecting.set()
        elif message.status == "closed":
            got_closed.set()

    invent.subscribe(on_status, to_channel=channel, when_subject="status")

    mock_char = _MockCharacteristic()
    mock_device = _MockDevice(_MockServer(_MockService(mock_char)))

    with umock.patch("invent.tools.ble:window") as mock_window:
        mock_window.navigator.bluetooth.requestDevice = _make_mock_bluetooth(
            mock_device
        )
        ble.ble(channel=channel, service="180d", characteristic="2a37")
        await got_connecting.wait()

        invent.publish(
            message=invent.Message("close"),
            to_channel=channel,
        )
        await got_closed.wait()


async def test_ble_full_lifecycle():
    """
    Verify the full BLE connection lifecycle: connecting → open → closed.
    """
    channel = "test_ble_lifecycle"
    got_connecting = asyncio.Event()
    got_open = asyncio.Event()
    got_closed = asyncio.Event()

    def on_status(message):
        if message.status == "connecting":
            got_connecting.set()
        elif message.status == "open":
            got_open.set()
        elif message.status == "closed":
            got_closed.set()

    invent.subscribe(on_status, to_channel=channel, when_subject="status")

    mock_char = _MockCharacteristic()
    mock_device = _MockDevice(_MockServer(_MockService(mock_char)))

    with umock.patch("invent.tools.ble:window") as mock_window:
        mock_window.navigator.bluetooth.requestDevice = _make_mock_bluetooth(
            mock_device
        )
        ble.ble(channel=channel, service="180d", characteristic="2a37")
        await got_connecting.wait()
        await got_open.wait()

        invent.publish(
            message=invent.Message("close"),
            to_channel=channel,
        )
        await got_closed.wait()

    assert channel not in ble.BLE_CONNECTIONS, "Connection not cleaned up."


async def test_ble_receive_notification():
    """
    Incoming BLE characteristic notifications should be published to
    the channel as a 'message' with a bytes .data attribute.
    """
    channel = "test_ble_receive"
    got_open = asyncio.Event()
    got_message = asyncio.Event()
    received = {}

    def on_status(message):
        if message.status == "open":
            got_open.set()

    def on_message(message):
        received["data"] = message.data
        got_message.set()

    invent.subscribe(on_status, to_channel=channel, when_subject="status")
    invent.subscribe(on_message, to_channel=channel, when_subject="message")

    mock_char = _MockCharacteristic()
    mock_device = _MockDevice(_MockServer(_MockService(mock_char)))

    got_closed = asyncio.Event()

    def on_closed(message):
        if message.status == "closed":
            got_closed.set()

    invent.subscribe(on_closed, to_channel=channel, when_subject="status")

    with umock.patch("invent.tools.ble:window") as mock_window:
        mock_window.navigator.bluetooth.requestDevice = _make_mock_bluetooth(
            mock_device
        )
        ble.ble(channel=channel, service="180d", characteristic="2a37")
        await got_open.wait()

        mock_char.simulate_notification(b"\x48\x65\x6c\x6c\x6f")
        await got_message.wait()

        invent.publish(
            message=invent.Message("close"),
            to_channel=channel,
        )
        await got_closed.wait()

    assert received["data"] == b"\x48\x65\x6c\x6c\x6f", received["data"]


async def test_ble_send_data():
    """
    Data published to the channel with subject 'send' should be written
    to the BLE characteristic once the connection is open.
    """
    channel = "test_ble_send"
    got_open = asyncio.Event()
    write_done = asyncio.Event()
    got_closed = asyncio.Event()

    mock_char = _MockCharacteristic()
    original_write = mock_char.writeValueWithResponse

    async def patched_write(data):
        await original_write(data)
        write_done.set()

    mock_char.writeValueWithResponse = patched_write

    mock_device = _MockDevice(_MockServer(_MockService(mock_char)))

    def on_status(message):
        if message.status == "open":
            got_open.set()
        elif message.status == "closed":
            got_closed.set()

    invent.subscribe(on_status, to_channel=channel, when_subject="status")

    with umock.patch("invent.tools.ble:window") as mock_window:
        mock_window.navigator.bluetooth.requestDevice = _make_mock_bluetooth(
            mock_device
        )
        ble.ble(channel=channel, service="180d", characteristic="2a37")
        await got_open.wait()

        invent.publish(
            message=invent.Message("send", data=b"\x01\x02\x03"),
            to_channel=channel,
        )
        await write_done.wait()

        invent.publish(
            message=invent.Message("close"),
            to_channel=channel,
        )
        await got_closed.wait()

    assert mock_char.written == [b"\x01\x02\x03"], mock_char.written


async def test_ble_send_string_data():
    """
    String data sent via the channel should be encoded to bytes before
    being written to the characteristic.
    """
    channel = "test_ble_send_str"
    got_open = asyncio.Event()
    write_done = asyncio.Event()
    got_closed = asyncio.Event()

    mock_char = _MockCharacteristic()
    original_write = mock_char.writeValueWithResponse

    async def patched_write(data):
        await original_write(data)
        write_done.set()

    mock_char.writeValueWithResponse = patched_write

    mock_device = _MockDevice(_MockServer(_MockService(mock_char)))

    def on_status(message):
        if message.status == "open":
            got_open.set()
        elif message.status == "closed":
            got_closed.set()

    invent.subscribe(on_status, to_channel=channel, when_subject="status")

    with umock.patch("invent.tools.ble:window") as mock_window:
        mock_window.navigator.bluetooth.requestDevice = _make_mock_bluetooth(
            mock_device
        )
        ble.ble(channel=channel, service="180d", characteristic="2a37")
        await got_open.wait()

        invent.publish(
            message=invent.Message("send", data="hello"),
            to_channel=channel,
        )
        await write_done.wait()

        invent.publish(
            message=invent.Message("close"),
            to_channel=channel,
        )
        await got_closed.wait()

    assert mock_char.written == [b"hello"], mock_char.written


async def test_ble_send_before_open():
    """
    Data published to the channel before the connection is open should
    be queued and sent once the connection is established.
    """
    channel = "test_ble_send_queued"
    got_open = asyncio.Event()
    write_done = asyncio.Event()
    got_closed = asyncio.Event()

    mock_char = _MockCharacteristic()
    original_write = mock_char.writeValueWithResponse

    async def patched_write(data):
        await original_write(data)
        write_done.set()

    mock_char.writeValueWithResponse = patched_write

    mock_device = _MockDevice(_MockServer(_MockService(mock_char)))

    def on_status(message):
        if message.status == "open":
            got_open.set()
        elif message.status == "closed":
            got_closed.set()

    invent.subscribe(on_status, to_channel=channel, when_subject="status")

    with umock.patch("invent.tools.ble:window") as mock_window:
        mock_window.navigator.bluetooth.requestDevice = _make_mock_bluetooth(
            mock_device
        )
        ble.ble(channel=channel, service="180d", characteristic="2a37")

        # Publish before the connection is open — should be queued.
        invent.publish(
            message=invent.Message("send", data=b"\xAB\xCD"),
            to_channel=channel,
        )

        await got_open.wait()
        await write_done.wait()

        invent.publish(
            message=invent.Message("close"),
            to_channel=channel,
        )
        await got_closed.wait()

    assert mock_char.written == [b"\xAB\xCD"], mock_char.written


async def test_ble_duplicate_channel_raises():
    """
    Attempting to open a second BLE connection on the same channel should
    raise a ValueError.
    """
    channel = "test_ble_dup"
    got_open = asyncio.Event()
    got_closed = asyncio.Event()

    def on_status(message):
        if message.status == "open":
            got_open.set()
        elif message.status == "closed":
            got_closed.set()

    invent.subscribe(on_status, to_channel=channel, when_subject="status")

    mock_char = _MockCharacteristic()
    mock_device = _MockDevice(_MockServer(_MockService(mock_char)))

    with umock.patch("invent.tools.ble:window") as mock_window:
        mock_window.navigator.bluetooth.requestDevice = _make_mock_bluetooth(
            mock_device
        )
        ble.ble(channel=channel, service="180d", characteristic="2a37")

        with upytest.raises(ValueError):
            ble.ble(channel=channel, service="180d", characteristic="2a37")

        await got_open.wait()

        invent.publish(
            message=invent.Message("close"),
            to_channel=channel,
        )
        await got_closed.wait()


async def test_ble_error_on_connect_failure():
    """
    If the device picker or GATT connection fails, an 'error' status
    should be published and the connection removed from the registry.
    """
    channel = "test_ble_error"
    got_connecting = asyncio.Event()
    got_error = asyncio.Event()

    def on_status(message):
        if message.status == "connecting":
            got_connecting.set()
        elif message.status == "error":
            got_error.set()

    invent.subscribe(on_status, to_channel=channel, when_subject="status")

    with umock.patch("invent.tools.ble:window") as mock_window:

        async def failing_request_device(options):
            raise RuntimeError("User cancelled the device picker.")

        mock_window.navigator.bluetooth.requestDevice = failing_request_device

        ble.ble(channel=channel, service="180d", characteristic="2a37")
        await got_connecting.wait()
        await got_error.wait()

    assert (
        channel not in ble.BLE_CONNECTIONS
    ), "Connection not removed from registry after error."


async def test_ble_cleanup_after_close():
    """
    After closing, the connection should be removed from the registry
    and channel handlers unsubscribed.
    """
    channel = "test_ble_cleanup"
    got_open = asyncio.Event()
    got_closed = asyncio.Event()

    def on_status(message):
        if message.status == "open":
            got_open.set()
        elif message.status == "closed":
            got_closed.set()

    invent.subscribe(on_status, to_channel=channel, when_subject="status")

    mock_char = _MockCharacteristic()
    mock_device = _MockDevice(_MockServer(_MockService(mock_char)))

    with umock.patch("invent.tools.ble:window") as mock_window:
        mock_window.navigator.bluetooth.requestDevice = _make_mock_bluetooth(
            mock_device
        )
        ble.ble(channel=channel, service="180d", characteristic="2a37")
        await got_open.wait()

        invent.publish(
            message=invent.Message("close"),
            to_channel=channel,
        )
        await got_closed.wait()

    assert (
        channel not in ble.BLE_CONNECTIONS
    ), "Connection not removed from registry after close."
    assert not mock_device.gatt.connected, "GATT still connected after close."
