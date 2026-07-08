[app]

title = Summit WebViewer

package.name = summitwebview
package.domain = org.soundworkslakes

source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,json

version = 0.1

requirements = python3,kivy==2.3.0,requests,pyjnius

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

android.uses_cleartext_traffic = True

log_level = 2

[buildozer]

warn_on_root = 1
