#!/usr/bin/python
print("Content-type: text/plain\r\n\r\n", end='')

import rfc822
import time

print("Current time:\n")
print("  RFC 2822: " + rfc822.formatdate())
print("  RFC 3339: " + time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
