# -*- coding: utf-8 -*-

import Pyjo.Test


class NoseTest(Pyjo.Test.NoseTest):
    script = __file__
    srcdir = '../..'


class UnitTest(Pyjo.Test.UnitTest):
    script = __file__


if __name__ == '__main__':

    from Pyjo.Test import *  # @UnusedWildImport

    import Pyjo.Transaction.WebSocket

    # Simple text frame roundtrip
    ws = Pyjo.Transaction.WebSocket.new()
    chunk = ws.build_frame(1, 0, 0, 0, 1, b'whatever')
    is_ok(chunk, b"\x81\x08\x77\x68\x61\x74\x65\x76\x65\x72", 'right frame')
    dummy = bytearray(chunk)
    frame = ws.parse_frame(dummy)
    is_ok(frame[0], 1, 'fin flag is set')
    is_ok(frame[1], 0, 'rsv1 flag is not set')
    is_ok(frame[2], 0, 'rsv2 flag is not set')
    is_ok(frame[3], 0, 'rsv3 flag is not set')
    is_ok(frame[4], 1, 'text frame')
    is_ok(frame[5], b'whatever', 'right payload')
    is_ok(ws.build_frame(1, 0, 0, 0, 1, b'whatever'), chunk, 'frames are equal')

    # Simple text frame roundtrip with all flags set
    ws = Pyjo.Transaction.WebSocket.new()
    chunk = ws.build_frame(1, 1, 1, 1, 1, b'whatever')
    is_ok(chunk, b"\xf1\x08\x77\x68\x61\x74\x65\x76\x65\x72", 'right frame')
    dummy = bytearray(chunk)
    frame = ws.parse_frame(dummy)
    is_ok(frame[0], 1, 'fin flag is set')
    is_ok(frame[1], 1, 'rsv1 flag is set')
    is_ok(frame[2], 1, 'rsv2 flag is set')
    is_ok(frame[3], 1, 'rsv3 flag is set')
    is_ok(frame[4], 1, 'text frame')
    is_ok(frame[5], b'whatever', 'right payload')
    is_ok(ws.build_frame(1, 1, 1, 1, 1, b'whatever'), chunk, 'frames are equal')

    # Simple text frame roundtrip without FIN bit
    ws = Pyjo.Transaction.WebSocket.new()
    chunk = ws.build_frame(0, 0, 0, 0, 1, b'whatever')
    is_ok(chunk, b"\x01\x08\x77\x68\x61\x74\x65\x76\x65\x72", 'right frame')
    dummy = bytearray(chunk)
    frame = ws.parse_frame(dummy)
    is_ok(frame[0], 0, 'fin flag is not set')
    is_ok(frame[1], 0, 'rsv1 flag is not set')
    is_ok(frame[2], 0, 'rsv2 flag is not set')
    is_ok(frame[3], 0, 'rsv3 flag is not set')
    is_ok(frame[4], 1, 'text frame')
    is_ok(frame[5], b'whatever', 'right payload')
    is_ok(ws.build_frame(0, 0, 0, 0, 1, b'whatever'), chunk, 'frames are equal')

    # Simple text frame roundtrip with RSV1 flags set
    ws = Pyjo.Transaction.WebSocket.new()
    chunk = ws.build_frame(1, 1, 0, 0, 1, b'whatever')
    is_ok(chunk, b"\xc1\x08\x77\x68\x61\x74\x65\x76\x65\x72", 'right frame')
    dummy = bytearray(chunk)
    frame = ws.parse_frame(dummy)
    is_ok(frame[0], 1, 'fin flag is set')
    is_ok(frame[1], 1, 'rsv1 flag is set')
    is_ok(frame[2], 0, 'rsv2 flag is not set')
    is_ok(frame[3], 0, 'rsv3 flag is not set')
    is_ok(frame[4], 1, 'text frame')
    is_ok(frame[5], b'whatever', 'right payload')
    is_ok(ws.build_frame(1, 1, 0, 0, 1, b'whatever'), chunk, 'frames are equal')

    # Simple text frame roundtrip with RSV2 flags set
    ws = Pyjo.Transaction.WebSocket.new()
    chunk = ws.build_frame(1, 0, 1, 0, 1, b'whatever')
    is_ok(chunk, b"\xa1\x08\x77\x68\x61\x74\x65\x76\x65\x72", 'right frame')
    dummy = bytearray(chunk)
    frame = ws.parse_frame(dummy)
    is_ok(frame[0], 1, 'fin flag is set')
    is_ok(frame[1], 0, 'rsv1 flag is not set')
    is_ok(frame[2], 1, 'rsv2 flag is set')
    is_ok(frame[3], 0, 'rsv3 flag is not set')
    is_ok(frame[4], 1, 'text frame')
    is_ok(frame[5], b'whatever', 'right payload')
    is_ok(ws.build_frame(1, 0, 1, 0, 1, b'whatever'), chunk, 'frames are equal')

    # Simple text frame roundtrip with RSV3 flags set
    ws = Pyjo.Transaction.WebSocket.new()
    chunk = ws.build_frame(1, 0, 0, 1, 1, b'whatever')
    is_ok(chunk, b"\x91\x08\x77\x68\x61\x74\x65\x76\x65\x72", 'right frame')
    dummy = bytearray(chunk)
    frame = ws.parse_frame(dummy)
    is_ok(frame[0], 1, 'fin flag is set')
    is_ok(frame[1], 0, 'rsv1 flag is not set')
    is_ok(frame[2], 0, 'rsv2 flag is not set')
    is_ok(frame[3], 1, 'rsv3 flag is set')
    is_ok(frame[4], 1, 'text frame')
    is_ok(frame[5], b'whatever', 'right payload')
    is_ok(ws.build_frame(1, 0, 0, 1, 1, b'whatever'), chunk, 'frames are equal')

    # Simple binary frame roundtrip
    ws = Pyjo.Transaction.WebSocket.new()
    chunk = ws.build_frame(1, 0, 0, 0, 2, b'works')
    is_ok(chunk, b"\x82\x05\x77\x6f\x72\x6b\x73", 'right frame')
    dummy = bytearray(chunk)
    frame = ws.parse_frame(dummy)
    is_ok(frame[0], 1, 'fin flag is set')
    is_ok(frame[1], 0, 'rsv1 flag is not set')
    is_ok(frame[2], 0, 'rsv2 flag is not set')
    is_ok(frame[3], 0, 'rsv3 flag is not set')
    is_ok(frame[4], 2, 'binary frame')
    is_ok(frame[5], b'works', 'right payload')
    is_ok(ws.build_frame(1, 0, 0, 0, 2, b'works'), chunk, 'frames are equal')

    # Masked text frame roundtrip
    ws = Pyjo.Transaction.WebSocket.new(masked=True)
    chunk = ws.build_frame(1, 0, 0, 0, 1, b'also works')
    dummy = bytearray(chunk)
    frame = ws.parse_frame(dummy)
    is_ok(frame[0], 1, 'fin flag is set')
    is_ok(frame[1], 0, 'rsv1 flag is not set')
    is_ok(frame[2], 0, 'rsv2 flag is not set')
    is_ok(frame[3], 0, 'rsv3 flag is not set')
    is_ok(frame[4], 1, 'text frame')
    is_ok(frame[5], b'also works', 'right payload')
    isnt_ok(Pyjo.Transaction.WebSocket.new().build_frame(1, 0, 0, 0, 2, b'also works'), chunk, 'frames are not equal')

    # Masked binary frame roundtrip
    ws = Pyjo.Transaction.WebSocket.new(masked=True)
    chunk = ws.build_frame(1, 0, 0, 0, 2, b'just works')
    dummy = bytearray(chunk)
    frame = ws.parse_frame(dummy)
    is_ok(frame[0], 1, 'fin flag is set')
    is_ok(frame[1], 0, 'rsv1 flag is not set')
    is_ok(frame[2], 0, 'rsv2 flag is not set')
    is_ok(frame[3], 0, 'rsv3 flag is not set')
    is_ok(frame[4], 2, 'binary frame')
    is_ok(frame[5], b'just works', 'right payload')
    isnt_ok(Pyjo.Transaction.WebSocket.new().build_frame(1, 0, 0, 0, 2, b'just works'), chunk, 'frames are not equal')

    # One-character text frame roundtrip
    ws = Pyjo.Transaction.WebSocket.new()
    chunk = ws.build_frame(1, 0, 0, 0, 1, b'a')
    is_ok(chunk, b"\x81\x01\x61", 'right frame')
    dummy = bytearray(chunk)
    frame = ws.parse_frame(dummy)
    is_ok(frame[0], 1, 'fin flag is set')
    is_ok(frame[1], 0, 'rsv1 flag is not set')
    is_ok(frame[2], 0, 'rsv2 flag is not set')
    is_ok(frame[3], 0, 'rsv3 flag is not set')
    is_ok(frame[4], 1, 'text frame')
    is_ok(frame[5], b'a', 'right payload')
    is_ok(ws.build_frame(1, 0, 0, 0, 1, b'a'), chunk, 'frames are equal')

    # One-byte binary frame roundtrip
    ws = Pyjo.Transaction.WebSocket.new()
    chunk = ws.build_frame(1, 0, 0, 0, 2, b'a')
    is_ok(chunk, b"\x82\x01\x61", 'right frame')
    dummy = bytearray(chunk)
    frame = ws.parse_frame(dummy)
    is_ok(frame[0], 1, 'fin flag is set')
    is_ok(frame[1], 0, 'rsv1 flag is not set')
    is_ok(frame[2], 0, 'rsv2 flag is not set')
    is_ok(frame[3], 0, 'rsv3 flag is not set')
    is_ok(frame[4], 2, 'binary frame')
    is_ok(frame[5], b'a', 'right payload')
    is_ok(ws.build_frame(1, 0, 0, 0, 2, b'a'), chunk, 'frames are equal')

    # 16-bit text frame roundtrip
    ws = Pyjo.Transaction.WebSocket.new()
    chunk = ws.build_frame(1, 0, 0, 0, 1, b'hi' * 10000)
    is_ok(chunk, b"\x81\x7e\x4e\x20" + (b"\x68\x69" * 10000), 'right frame')
    dummy = bytearray(chunk)
    frame = ws.parse_frame(dummy)
    is_ok(frame[0], 1, 'fin flag is set')
    is_ok(frame[1], 0, 'rsv1 flag is not set')
    is_ok(frame[2], 0, 'rsv2 flag is not set')
    is_ok(frame[3], 0, 'rsv3 flag is not set')
    is_ok(frame[4], 1, 'text frame')
    is_ok(frame[5], b'hi' * 10000, 'right payload')
    is_ok(ws.build_frame(1, 0, 0, 0, 1, b'hi' * 10000), chunk, 'frames are equal')

    # 64-bit text frame roundtrip
    ws = Pyjo.Transaction.WebSocket.new(max_websocket_size=500000)
    chunk = ws.build_frame(1, 0, 0, 0, 1, b'hi' * 200000)
    is_ok(chunk, b"\x81\x7f\x00\x00\x00\x00\x00\x06\x1a\x80" + (b"\x68\x69" * 200000), 'right frame')
    dummy = bytearray(chunk)
    frame = ws.parse_frame(dummy)
    is_ok(frame[0], 1, 'fin flag is set')
    is_ok(frame[1], 0, 'rsv1 flag is not set')
    is_ok(frame[2], 0, 'rsv2 flag is not set')
    is_ok(frame[3], 0, 'rsv3 flag is not set')
    is_ok(frame[4], 1, 'text frame')
    is_ok(frame[5], b'hi' * 200000, 'right payload')
    is_ok(ws.build_frame(1, 0, 0, 0, 1, b'hi' * 200000), chunk, 'frames are equal')

    # Empty text frame roundtrip
    ws = Pyjo.Transaction.WebSocket.new()
    chunk = ws.build_frame(1, 0, 0, 0, 1, b'')
    is_ok(chunk, b"\x81\x00", 'right frame')
    dummy = bytearray(chunk)
    frame = ws.parse_frame(dummy)
    is_ok(frame[0], 1, 'fin flag is set')
    is_ok(frame[1], 0, 'rsv1 flag is not set')
    is_ok(frame[2], 0, 'rsv2 flag is not set')
    is_ok(frame[3], 0, 'rsv3 flag is not set')
    is_ok(frame[4], 1, 'text frame')
    is_ok(frame[5], b'', 'no payload')
    is_ok(ws.build_frame(1, 0, 0, 0, 1, b''), chunk, 'frames are equal')

    # Empty close frame roundtrip
    ws = Pyjo.Transaction.WebSocket.new()
    chunk = ws.build_frame(1, 0, 0, 0, 8, b'')
    is_ok(chunk, b"\x88\x00", 'right frame')
    dummy = bytearray(chunk)
    frame = ws.parse_frame(dummy)
    is_ok(frame[0], 1, 'fin flag is set')
    is_ok(frame[1], 0, 'rsv1 flag is not set')
    is_ok(frame[2], 0, 'rsv2 flag is not set')
    is_ok(frame[3], 0, 'rsv3 flag is not set')
    is_ok(frame[4], 8, 'close frame')
    is_ok(frame[5], b'', 'no payload')
    is_ok(ws.build_frame(1, 0, 0, 0, 8, b''), chunk, 'frames are equal')

    # Masked empty binary frame roundtrip
    ws = Pyjo.Transaction.WebSocket.new(masked=True)
    chunk = ws.build_frame(1, 0, 0, 0, 2, b'')
    dummy = bytearray(chunk)
    frame = ws.parse_frame(dummy)
    is_ok(frame[0], 1, 'fin flag is set')
    is_ok(frame[1], 0, 'rsv1 flag is not set')
    is_ok(frame[2], 0, 'rsv2 flag is not set')
    is_ok(frame[3], 0, 'rsv3 flag is not set')
    is_ok(frame[4], 2, 'binary frame')
    is_ok(frame[5], b'', 'no payload')
    isnt_ok(Pyjo.Transaction.WebSocket.new().build_frame(1, 0, 0, 0, 2, b''), chunk, 'frames are not equal')

    # Compressed binary message roundtrip
    ws = Pyjo.Transaction.WebSocket.new(compressed=True)
    chunk = ws.build_message(binary=b'just works')
    dummy = bytearray(chunk)
    frame = ws.parse_frame(dummy)
    is_ok(frame[0], 1, 'fin flag is set')
    is_ok(frame[1], 1, 'rsv1 flag is set')
    is_ok(frame[2], 0, 'rsv2 flag is not set')
    is_ok(frame[3], 0, 'rsv3 flag is not set')
    is_ok(frame[4], 2, 'binary frame')
    ok(frame[5], b'has payload')
    isnt_ok(Pyjo.Transaction.WebSocket.new().build_message(binary=b'just works'), chunk, 'messages are not equal')

    done_testing()
