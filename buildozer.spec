[app]
title = G-BEPC
package.name = gbepc
package.domain = org.gsociety
source.dir = .
source.include_exts = py,kv,png,jpg,pdf
source.exclude_dirs = .github,bin,.buildozer,__pycache__
version = 1.0
p4a.branch = v2024.01.21
requirements = python3,kivy==2.3.0,kivymd==1.2.0,pillow,pymupdf,plyer
icon.filename = %(source.dir)s/assets/icon.png
orientation = portrait
fullscreen = 0
android.archs = arm64-v8a, armeabi-v7a
android.api = 33
android.minapi = 21
android.accept_sdk_license = True
android.permissions = READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,MANAGE_EXTERNAL_STORAGE,VIBRATE

[buildozer]
log_level = 2
warn_on_root = 1
