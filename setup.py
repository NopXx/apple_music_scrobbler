"""py2app build script.

Usage:
    pip install pywebview pyobjc py2app
    python3 setup.py py2app           # release .app in ./dist
    python3 setup.py py2app -A        # development build (symlinked, faster)
"""
from setuptools import setup
import re
from pathlib import Path

# อ่าน __version__ จาก server.py ให้เป็น single source of truth
_server_src = (Path(__file__).parent / "server.py").read_text()
_m = re.search(r'__version__\s*=\s*"([^"]+)"', _server_src)
VERSION = _m.group(1) if _m else "0.0.0"

APP = ["app.py"]
# แพ็คไฟล์ frontend ลง Resources/web/ ใน .app bundle (คง subdir ให้ตรงกับ dev)
DATA_FILES = [
    ("web", ["web/index.html", "web/settings.html", "web/i18n.js", "web/miniplayer.html"]),
]

OPTIONS = {
    "argv_emulation": False,
    "packages": ["AppKit", "WebKit"],
    "includes": ["server", "_credentials"],
    "iconfile": "assets/icon.icns",
    "plist": {
        "CFBundleName": "Apple Music Scrobbler",
        "CFBundleDisplayName": "Apple Music Scrobbler",
        "CFBundleIdentifier": "com.nopxx.applemusicscrobbler",
        "CFBundleVersion": VERSION,
        "CFBundleShortVersionString": VERSION,
        "LSMinimumSystemVersion": "11.0",
        "LSUIElement": True,  # เป็น menu bar app ไม่โชว์ใน Dock
        "NSHighResolutionCapable": True,
        "NSAppleEventsUsageDescription":
            "ใช้ AppleScript เพื่ออ่านเพลงที่กำลังเล่นใน Apple Music",
        "NSAppleMusicUsageDescription":
            "เข้าถึงข้อมูลเพลงที่กำลังเล่นใน Apple Music",
        "NSUserNotificationsUsageDescription":
            "แสดงการแจ้งเตือนเมื่อเล่นเพลงใหม่หรือ scrobble",
    },
}

setup(
    app=APP,
    name="Apple Music Scrobbler",
    data_files=DATA_FILES,
    options={"py2app": OPTIONS},
    setup_requires=["py2app"],
)
