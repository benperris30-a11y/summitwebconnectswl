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

# master's current commit pins Kivy's build-time Cython requirement to
# <=3.0.0, which resolves to a known-broken Cython 3.0.0 release (generates
# malformed OpenGL calls, e.g. glVertexAttribPointer). develop has since
# loosened this pin, avoiding the broken exact version.
p4a.branch = develop

android.accept_sdk_license = True

android.enable_androidx = True

android.allow_backup = False

# Copy network_security_config.xml into src/main/res/xml/ so it's actually
# packaged into the APK (it was previously unused, sitting on disk).
android.res_xml = network_security_config.xml

# Point the <application> tag at the network security config, plus a
# belt-and-braces cleartext flag. NOTE: this key expects a FILE PATH
# containing the XML attributes, not an inline string.
android.extra_manifest_application_arguments = manifest_app_args.xml

log_level = 2

[buildozer]

warn_on_root = 1
