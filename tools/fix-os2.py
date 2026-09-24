#!/usr/bin/env python3
"""Post-build fix for a truncated OS/2 table (stdlib only, no fontTools).

Background: fontforge's TTF generator (run via ``tools/minify.py``) writes
an OS/2 header declaring version 5 while only storing 96 bytes (a version 4
length body, missing ``usLowerOpticalPointSize``/``usUpperOpticalPointSize``).
Any fontTools code path touching OS/2 then dies with::

    struct.error: unpack requires a buffer of 22 bytes

This script downgrades the declared version to the highest version that
fits the stored length (96 bytes -> version 4) and recalculates the
affected checksums (OS/2 directory entry + head.checkSumAdjustment).

Usage (run from ``tools/``, after ``minify.py``)::

    python3 ./fix-os2.py ./zpix.ttf

Exit code 0 = fixed or already fine. Exit code 1 = unfixable, fail the build.
"""

import struct
import sys

# Minimum OS/2 body length per version (spec + fontTools O_S_2f_2.py).
MIN_LEN_FOR_VERSION = {0: 78, 1: 86, 2: 96, 3: 96, 4: 96, 5: 100}

CHECKSUM_MAGIC = 0xB1B0AFBA


def fail(message):
    print("[fix-os2] ERROR: %s" % message)
    return 1


def table_checksum(data):
    if len(data) % 4:
        data = data + b"\0" * (4 - len(data) % 4)
    return sum(struct.unpack(">%dL" % (len(data) // 4), data)) & 0xFFFFFFFF


def file_checksum(buf):
    data = bytes(buf)
    if len(data) % 4:
        data = data + b"\0" * (4 - len(data) % 4)
    return sum(struct.unpack(">%dL" % (len(data) // 4), data)) & 0xFFFFFFFF


def read_directory(buf):
    if len(buf) < 12:
        return None
    (num_tables,) = struct.unpack(">H", buf[4:6])
    records = {}
    for i in range(num_tables):
        off = 12 + 16 * i
        if off + 16 > len(buf):
            return None
        tag, _cs, table_off, table_len = struct.unpack(">4sLLL", buf[off:off + 16])
        records[tag] = (off, table_off, table_len)
    return records


def main(path):
    with open(path, "rb") as fh:
        buf = bytearray(fh.read())

    records = read_directory(buf)
    if records is None:
        return fail("%s: not a valid sfnt file" % path)
    if b"OS/2" not in records:
        return fail("%s: no OS/2 table" % path)
    if b"head" not in records:
        return fail("%s: no head table" % path)

    rec_off, table_off, table_len = records[b"OS/2"]
    (version,) = struct.unpack(">H", buf[table_off:table_off + 2])
    print("[fix-os2] file=%s OS/2 version=%d length=%d" % (path, version, table_len))

    if version not in MIN_LEN_FOR_VERSION:
        return fail("unknown OS/2 version %d, refusing to guess" % version)

    if table_len >= MIN_LEN_FOR_VERSION[version]:
        print("[fix-os2] OK: version %d fits in %d bytes, nothing to do" % (version, table_len))
        return 0

    fitting = [v for v, need in MIN_LEN_FOR_VERSION.items() if need <= table_len]
    if not fitting:
        return fail("OS/2 length %d fits no known version" % table_len)
    target = max(fitting)
    print(
        "[fix-os2] truncated: version %d needs >= %d bytes but have %d"
        " -> downgrading to version %d"
        % (version, MIN_LEN_FOR_VERSION[version], table_len, target)
    )

    # 1. Patch the version field.
    buf[table_off:table_off + 2] = struct.pack(">H", target)

    # 2. Recompute the OS/2 directory checksum.
    new_checksum = table_checksum(bytes(buf[table_off:table_off + table_len]))
    buf[rec_off + 4:rec_off + 8] = struct.pack(">L", new_checksum)

    # 3. Recompute head.checkSumAdjustment.
    _, head_off, _head_len = records[b"head"]
    buf[head_off + 8:head_off + 12] = b"\0\0\0\0"
    adjustment = (CHECKSUM_MAGIC - file_checksum(buf)) & 0xFFFFFFFF
    buf[head_off + 8:head_off + 12] = struct.pack(">L", adjustment)

    with open(path, "wb") as fh:
        fh.write(buf)

    # 4. Verify from disk.
    with open(path, "rb") as fh:
        check = bytearray(fh.read())
    check_records = read_directory(check)
    _, check_off, check_len = check_records[b"OS/2"]
    (check_version,) = struct.unpack(">H", check[check_off:check_off + 2])
    ok_version = check_len >= MIN_LEN_FOR_VERSION.get(check_version, 10 ** 9)
    ok_checksum = file_checksum(check) == CHECKSUM_MAGIC
    print(
        "[fix-os2] verify: OS/2 version=%d length=%d version_fits=%s whole_file_checksum=%s"
        % (check_version, check_len, ok_version, "OK" if ok_checksum else "BAD")
    )
    if not (ok_version and ok_checksum):
        return fail("verification failed")

    print("[fix-os2] done: %s fixed (OS/2 v%d -> v%d)" % (path, version, target))
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: python3 fix-os2.py <font.ttf>")
        sys.exit(2)
    sys.exit(main(sys.argv[1]))
