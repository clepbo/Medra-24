#!/usr/bin/env python3
"""Minimal reader for Figma's .fig container (fig-kiwi).

A .fig is a zip; canvas.fig inside it is Kiwi-encoded:
    "fig-kiwi" | uint32 version | (uint32 len + raw-deflate block)*
The first block is the Kiwi schema, the second is the document. Kiwi is self-describing,
so the schema in the file is enough to decode the document without Figma's source.

Used here for one purpose: reading a designer's corrections back out of an exported file
so they can be folded into the generator instead of guessed at.
"""
import struct, zlib, sys, json


class Reader:
    def __init__(self, buf):
        self.b = buf; self.i = 0
    def byte(self):
        v = self.b[self.i]; self.i += 1; return v
    def bool(self): return self.byte() != 0
    def varuint(self):
        v = 0; shift = 0
        while True:
            c = self.byte()
            v |= (c & 0x7F) << shift
            if not (c & 0x80): break
            shift += 7
        return v & 0xFFFFFFFF
    def varint(self):
        v = self.varuint()
        return ~(v >> 1) if (v & 1) else (v >> 1)
    def varuint64(self):
        v = 0; shift = 0
        while True:
            c = self.byte()
            v |= (c & 0x7F) << shift
            if not (c & 0x80): break
            shift += 7
        return v
    def varint64(self):
        v = self.varuint64()
        return ~(v >> 1) if (v & 1) else (v >> 1)
    def float(self):
        first = self.byte()
        if first == 0: return 0.0
        bits = first | (self.byte() << 8) | (self.byte() << 16) | (self.byte() << 24)
        bits = (bits << 23) | (bits >> 9)          # kiwi's rotate
        bits &= 0xFFFFFFFF
        return struct.unpack("<f", struct.pack("<I", bits))[0]
    def string(self):
        out = bytearray()
        while True:
            c = self.byte()
            if c == 0: break
            out.append(c)
        return out.decode("utf-8", "replace")


TYPE_BOOL, TYPE_BYTE, TYPE_INT, TYPE_UINT = -1, -2, -3, -4
TYPE_FLOAT, TYPE_STRING, TYPE_INT64, TYPE_UINT64 = -5, -6, -7, -8
KIND_ENUM, KIND_STRUCT, KIND_MESSAGE = 0, 1, 2


def read_schema(buf):
    r = Reader(buf)
    defs = []
    for _ in range(r.varuint()):
        name = r.string(); kind = r.byte()
        fields = []
        for _f in range(r.varuint()):
            fname = r.string(); ftype = r.varint(); is_array = r.bool(); value = r.varuint()
            fields.append({"name": fname, "type": ftype, "array": is_array, "value": value})
        defs.append({"name": name, "kind": kind, "fields": fields})
    return defs


class Decoder:
    def __init__(self, defs):
        self.defs = defs
        self.by_name = {d["name"]: i for i, d in enumerate(defs)}

    def value(self, r, t):
        if t == TYPE_BOOL:   return r.bool()
        if t == TYPE_BYTE:   return r.byte()
        if t == TYPE_INT:    return r.varint()
        if t == TYPE_UINT:   return r.varuint()
        if t == TYPE_FLOAT:  return r.float()
        if t == TYPE_STRING: return r.string()
        if t == TYPE_INT64:  return r.varint64()
        if t == TYPE_UINT64: return r.varuint64()
        return self.compound(r, self.defs[t])

    def compound(self, r, d):
        if d["kind"] == KIND_ENUM:
            v = r.varuint()
            for f in d["fields"]:
                if f["value"] == v: return f["name"]
            return v
        out = {}
        if d["kind"] == KIND_STRUCT:
            for f in d["fields"]:
                out[f["name"]] = self.field(r, f)
            return out
        while True:
            fid = r.varuint()
            if fid == 0: return out
            f = next((x for x in d["fields"] if x["value"] == fid), None)
            if f is None: raise ValueError(f"unknown field {fid} in {d['name']}")
            out[f["name"]] = self.field(r, f)

    def field(self, r, f):
        if f["array"]:
            return [self.value(r, f["type"]) for _ in range(r.varuint())]
        return self.value(r, f["type"])


def load(path):
    raw = open(path, "rb").read()
    assert raw[:8] == b"fig-kiwi", "not a fig-kiwi payload"
    i = 12
    blocks = []
    while i + 4 <= len(raw) and len(blocks) < 2:
        (n,) = struct.unpack_from("<I", raw, i); i += 4
        if n == 0 or i + n > len(raw): break
        chunk = raw[i:i + n]
        if chunk[:4] == b"\x28\xb5\x2f\xfd":      # newer files zstd the data block
            import zstandard
            blocks.append(zstandard.ZstdDecompressor().decompress(chunk, max_output_size=1 << 31))
        else:
            try:
                blocks.append(zlib.decompressobj(-15).decompress(chunk))
            except zlib.error:
                break
        i += n
    defs = read_schema(blocks[0])
    dec = Decoder(defs)
    r = Reader(blocks[1])
    root = dec.compound(r, defs[dec.by_name["Message"]])
    return defs, root


if __name__ == "__main__":
    defs, root = load(sys.argv[1])
    print("schema defs:", len(defs))
    print("top-level keys:", list(root.keys()))
    nc = root.get("nodeChanges") or []
    print("nodeChanges:", len(nc))
