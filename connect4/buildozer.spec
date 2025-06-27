[app]
title = Connect 4 Game
package.name = connect4game
package.domain = org.yourname.connect4
source.dir = .
version = 0.1
requirements = python3,kivy==2.1.0,pyjnius==1.6.1
orientation = portrait

[android]
android.api = 31
android.minapi = 21
android.ndk = 25b
android.ndk_api = 21
android.accept_sdk_license = True
android.archs = armeabi-v7a

[buildozer]
log_level = 2