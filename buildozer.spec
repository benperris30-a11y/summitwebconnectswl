[app]
title = Summit WebViewer
package.name = summitwebview
package.domain = org.soundworkslakes
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json
version = 0.1
requirements = python3, kivy, requests, urllib3, chardet, idna, certifi, pyjnius, android
orientation = portrait
fullscreen = 1
android.permissions = INTERNET
android.uses_cleartext_traffic = True
android.api = 33
android.minapi = 21
android.ndk_api = 21
android.archs = arm64-v8a, armeabi-v7a

[buildozer]
log_level = 2
warn_on_root = 1