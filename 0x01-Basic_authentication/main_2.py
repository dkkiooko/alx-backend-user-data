#!/usr/bin/env python3
"""Main 2
"""
from api.v1.auth.basic_auth import BasicAuth

a = BasicAuth()

print(a.extract_base64_authorization_header(None))
print(a.extract_base64_authorization_header(89))
print(a.extract_base64_authorization_header("Holberton School"))
print(a.extract_base64_authorization_header("Basic Holberton"))
print(a.extract_base64_authorization_header("Basic SG8sYmVydG9u"))
print(a.extract_base64_authorization_header("Basic SG9sYmVydGpuIFNjaGpvbA=="))
print(a.extract_base64_authorization_header("Basic1234"))