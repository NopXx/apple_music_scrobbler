#!/usr/bin/env python3
"""Desktop app — menu bar icon + background server + optional native window."""
import os
import sys
import threading
import time
import webbrowser
from pathlib import Path


def _resolve_resource_dir() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent.parent / "Resources"
    return Path(__file__).parent.resolve()


def _resolve_data_dir() -> Path:
    if getattr(sys, "frozen", False):
        return Path.home() / "Library" / "Application Support" / "AppleMusicScrobbler"
    return Path(__file__).parent.resolve()


RESOURCE_DIR = _resolve_resource_dir()
DATA_DIR = _resolve_data_dir()
DATA_DIR.mkdir(parents=True, exist_ok=True)

# py2app flatten DATA_FILES ลง Resources/ ตรง ๆ — สำหรับ dev ไฟล์จะอยู่ใน ./web
# ถ้า dir "web" ไม่มี (bundled) fallback ใช้ RESOURCE_DIR
_web_candidate = RESOURCE_DIR / "web"
WEB_DIR = _web_candidate if _web_candidate.is_dir() else RESOURCE_DIR

os.environ["AMS_DATA_DIR"] = str(DATA_DIR)
os.environ["AMS_WEB_DIR"] = str(WEB_DIR)
os.chdir(RESOURCE_DIR)

import server  # noqa: E402
import rumps  # noqa: E402


_tracker = None
_httpd = None


def _run_server():
    global _tracker, _httpd
    server.db_init()
    _tracker = server.Tracker()
    server.TRACKER_REF["t"] = _tracker
    threading.Thread(target=_tracker.run, daemon=True).start()
    _httpd = server.ReusableServer(("127.0.0.1", server.PORT), server.Handler)
    print(f"[app] server ready on http://127.0.0.1:{server.PORT}")
    _httpd.serve_forever()


# ============================================================
# Native notifications via pyobjc (fallback: rumps -> osascript)
# ============================================================
def _load_nsimage_from_url(url: str):
    """ดาวน์โหลดรูปภาพจาก URL → คืน NSImage (คืน None ถ้าโหลดไม่ได้)"""
    if not url:
        return None
    try:
        from Foundation import NSData, NSURL  # type: ignore
        from AppKit import NSImage  # type: ignore
        ns_url = NSURL.URLWithString_(url)
        if ns_url is None:
            return None
        data = NSData.dataWithContentsOfURL_(ns_url)
        if data is None:
            return None
        img = NSImage.alloc().initWithData_(data)
        return img
    except Exception:
        return None


def _pyobjc_notify(title: str, subtitle: str, body: str, image_url: str = ""):
    try:
        from Foundation import NSUserNotification, NSUserNotificationCenter  # type: ignore
        n = NSUserNotification.alloc().init()
        n.setTitle_(title)
        if subtitle:
            n.setSubtitle_(subtitle)
        if body:
            n.setInformativeText_(body)
        # แนบรูป artwork — NSUserNotification แสดง thumbnail ทางขวาของ notification
        img = _load_nsimage_from_url(image_url)
        if img is not None:
            try:
                n.setContentImage_(img)
            except Exception:
                pass
        NSUserNotificationCenter.defaultUserNotificationCenter().deliverNotification_(n)
    except Exception:
        try:
            rumps.notification(title, subtitle, body, sound=False)
        except Exception:
            # rumps/pyobjc unavailable → fall through to osascript
            raise


# ============================================================
# Menu bar app
# ============================================================
URL_HOME = f"http://127.0.0.1:{server.PORT}"
URL_SETTINGS = f"http://127.0.0.1:{server.PORT}/settings.html"

# i18n strings ที่ใช้ใน menu bar — sync กับ i18n.js
MENU_I18N = {
    "th": {
        "track.empty": "—",
        "not_playing": "ยังไม่ได้เล่นเพลง",
        "scrobble.empty": "Scrobble: —",
        "scrobble.done": "Scrobble: ✓ Scrobbled แล้ว",
        "scrobble.too_short": "Scrobble: — (เพลงสั้นเกินไป)",
        "scrobble.progress": "Scrobble: {pct}%",
        "open_window": "เปิดหน้าต่าง",
        "open_settings": "ตั้งค่า",
        "enable_notifications": "เปิดการแจ้งเตือน",
        "quit": "ออก",
    },
    "en": {
        "track.empty": "—",
        "not_playing": "Not playing",
        "scrobble.empty": "Scrobble: —",
        "scrobble.done": "Scrobble: ✓ Scrobbled",
        "scrobble.too_short": "Scrobble: — (track too short)",
        "scrobble.progress": "Scrobble: {pct}%",
        "open_window": "Open Window",
        "open_settings": "Open Settings",
        "enable_notifications": "Enable Notifications",
        "quit": "Quit",
    },
}


def _menu_t(key: str, **vars) -> str:
    lang = (server.load_settings().get("language") or "th").lower()
    table = MENU_I18N.get(lang) or MENU_I18N["en"]
    s = table.get(key) or MENU_I18N["en"].get(key) or key
    return s.format(**vars) if vars else s


class ScrobblerApp(rumps.App):
    def __init__(self):
        super().__init__("♪", quit_button=None)
        # สร้าง items โดยใช้ placeholder title — จะ set ผ่าน _refresh_menu_labels() ทีเดียว
        self._track_item = rumps.MenuItem("—", callback=None)
        self._artist_item = rumps.MenuItem("not_playing", callback=None)
        self._scrobble_item = rumps.MenuItem("scrobble.empty", callback=None)
        self._open_window_item = rumps.MenuItem("open_window", callback=self.open_window, key="o")
        self._open_settings_item = rumps.MenuItem("open_settings", callback=self.open_settings, key=",")
        self._notif_item = rumps.MenuItem("enable_notifications", callback=self.toggle_notif)
        self._quit_item = rumps.MenuItem("quit", callback=self.quit_app, key="q")
        self._version_item = rumps.MenuItem(f"v{getattr(server, '__version__', '?')}", callback=None)

        self.menu = [
            self._track_item,
            self._artist_item,
            self._scrobble_item,
            None,
            self._open_window_item,
            self._open_settings_item,
            None,
            self._notif_item,
            None,
            self._quit_item,
            None,
            self._version_item,
        ]
        # disable the info lines (grey text, no click)
        self._track_item.set_callback(None)
        self._artist_item.set_callback(None)
        self._scrobble_item.set_callback(None)
        self._version_item.set_callback(None)

        self._last_title = ""
        self._last_lang = None
        self._refresh_menu_labels()
        self._refresh_notif_check()

    def _refresh_menu_labels(self):
        """อัปเดต title ของ menu items ตามภาษาปัจจุบัน"""
        lang = (server.load_settings().get("language") or "th").lower()
        self._last_lang = lang
        self._open_window_item.title = _menu_t("open_window")
        self._open_settings_item.title = _menu_t("open_settings")
        self._notif_item.title = _menu_t("enable_notifications")
        self._quit_item.title = _menu_t("quit")

    # --- menu item handlers ---
    def open_window(self, _):
        webbrowser.open(URL_HOME)

    def open_settings(self, _):
        webbrowser.open(URL_SETTINGS)

    def toggle_notif(self, sender):
        s = server.load_settings().get("notifications", {})
        new_val = not s.get("enabled", True)
        server.save_settings({"notifications": {"enabled": new_val}})
        sender.state = new_val
        self._refresh_notif_check()

    def _refresh_notif_check(self):
        s = server.load_settings().get("notifications", {})
        self._notif_item.state = bool(s.get("enabled", True))

    def quit_app(self, _):
        try:
            if _tracker:
                _tracker.stop()
        except Exception:
            pass
        try:
            if _httpd:
                threading.Thread(target=_httpd.shutdown, daemon=True).start()
        except Exception:
            pass
        rumps.quit_application()

    def _build_menubar_title(self, data, playing):
        """ประกอบ title ของ menu bar จาก settings.menubar"""
        mb = server.load_settings().get("menubar", {}) or {}
        show_icon = mb.get("show_icon", True)
        show_track = mb.get("show_track", True)
        show_artist = mb.get("show_artist", False)
        show_state = mb.get("show_state", True)
        max_len = int(mb.get("max_length", 28) or 28)

        name = data.get("name") or ""
        artist = data.get("artist") or ""

        # ไม่เล่นอะไรอยู่ — แสดงแค่ icon (ถ้าเปิด) หรือ "♪" ขั้นต่ำ
        if not name:
            return "♪" if show_icon else "♪"

        parts = []
        if show_icon:
            parts.append("♪")
        if show_state:
            parts.append("▶" if playing else "⏸")

        text_parts = []
        if show_track and name:
            text_parts.append(name)
        if show_artist and artist:
            text_parts.append(artist)
        text = " — ".join(text_parts)

        if text:
            if max_len > 0 and len(text) > max_len:
                text = text[:max_len - 1] + "…"
            parts.append(text)

        return " ".join(parts) if parts else "♪"

    # --- periodic refresh of the info lines ---
    @rumps.timer(3)
    def _refresh_status(self, _):
        try:
            # ถ้าภาษาถูกเปลี่ยนผ่าน settings → อัปเดต label ของ menu items ทั้งหมด
            cur_lang = (server.load_settings().get("language") or "th").lower()
            if cur_lang != self._last_lang:
                self._refresh_menu_labels()

            data = server.CURRENT_NOW_PLAYING.get("data", {}) or {}
            name = data.get("name") or ""
            artist = data.get("artist") or ""
            playing = bool(data.get("playing"))

            if not name:
                self.title = self._build_menubar_title(data, playing)
                self._track_item.title = _menu_t("track.empty")
                self._artist_item.title = _menu_t("not_playing")
                self._scrobble_item.title = _menu_t("scrobble.empty")
                return

            self.title = self._build_menubar_title(data, playing)
            self._track_item.title = name
            self._artist_item.title = artist or _menu_t("track.empty")

            # Scrobble progress
            pct = data.get("scrobble_percent", 0) or 0
            has_scrobbled = bool(data.get("has_scrobbled"))
            duration = data.get("duration", 0) or 0
            if has_scrobbled:
                self._scrobble_item.title = _menu_t("scrobble.done")
            elif duration <= 30:
                self._scrobble_item.title = _menu_t("scrobble.too_short")
            else:
                self._scrobble_item.title = _menu_t("scrobble.progress", pct=int(pct))
        except Exception as e:
            print(f"[menu] refresh error: {e}")


def main():
    # Hook notifications through pyobjc (ไม่ต้อง spawn osascript subprocess)
    server.NOTIFY_CALLBACK["fn"] = _pyobjc_notify

    threading.Thread(target=_run_server, daemon=True).start()
    time.sleep(0.4)

    ScrobblerApp().run()


if __name__ == "__main__":
    main()
