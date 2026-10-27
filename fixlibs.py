#!/usr/bin/env python3
"""Rebuild an APK's lib/ entries from the stock APK (patcher sometimes writes
corrupt copies of large .so files). Usage: fixlibs.py stock.apk patched.apk out.apk"""
import sys, zipfile, zlib
stock, patched, out = sys.argv[1:4]
zs = zipfile.ZipFile(stock)
zp = zipfile.ZipFile(patched)
bad = 0
with zipfile.ZipFile(out, "w") as zo:
    for info in zp.infolist():
        if info.filename.startswith("lib/"):
            continue
        data = zp.read(info)
        zo.writestr(info, data, compress_type=info.compress_type)
    for info in zs.infolist():
        if not info.filename.startswith("lib/"):
            continue
        try:
            data = zs.read(info)
        except Exception as e:
            print("STOCK ENTRY CORRUPT:", info.filename, e); bad += 1; continue
        ni = zipfile.ZipInfo(info.filename, date_time=info.date_time)
        ni.compress_type = zipfile.ZIP_STORED  # stored + zipalign -p = Android can mmap them
        zo.writestr(ni, data)
print("done, corrupt stock entries:", bad)
sys.exit(1 if bad else 0)
