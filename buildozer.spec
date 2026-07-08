[app]

title = Summit WebViewer
package.name = summitwebview
package.domain = org.soundworkslakes

source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,json,xml

version = 0.1

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

# Fallback cleartext toggle
android.uses_cleartext_traffic = True

# Map and inject the custom Network Security Config into the compiled Android manifest structure
android.manifest_application_arguments = android:networkSecurityConfig="@xml/network_security_config"
android.add_resources = network_security_config.xml:res/xml/network_security_config.xml

log_level = 2

[buildozer]
warn_on_root = 1
