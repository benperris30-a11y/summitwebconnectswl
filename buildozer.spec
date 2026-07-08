[app]

title = Summit WebViewer
package.name = summitwebview
package.domain = org.soundworkslakes

source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,json,xml

version = 0.1

# Strict environment locks remain intact
requirements = python3==3.11.9,hostpython3==3.11.9,kivy==2.3.0,requests,pyjnius

orientation = portrait
fullscreen = 1

android.permissions = INTERNET

android.api = 34
android.minapi = 24
android.ndk = 25b
android.ndk_api = 24

android.archs = arm64-v8a,armeabi-v7a
android.accept_sdk_license = True
android.enable_androidx = True
android.allow_backup = False

# Natively toggle cleartext at application layer
android.uses_cleartext_traffic = True

# Map and inject the custom Network Security Config into the compiled Android manifest structure
android.manifest_application_arguments = android:networkSecurityConfig="@xml/network_security_config"

# This forces Buildozer to completely merge our local res directory into the native Gradle layout
android.add_resources = %(source.dir)s/res

log_level = 2

[buildozer]
warn_on_root = 1
