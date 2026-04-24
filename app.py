#!/usr/bin/env python3
"""Desktop app — menu bar icon + background server + custom NSPopover mini player."""
import os
import sys
import threading
import time
import webbrowser
import subprocess
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

_web_candidate = RESOURCE_DIR / "web"
WEB_DIR = _web_candidate if _web_candidate.is_dir() else RESOURCE_DIR

os.environ["AMS_DATA_DIR"] = str(DATA_DIR)
os.environ["AMS_WEB_DIR"] = str(WEB_DIR)
os.chdir(RESOURCE_DIR)

import server  # noqa: E402
import objc
from AppKit import (
    NSApp, NSApplication, NSStatusBar, NSVariableStatusItemLength,
    NSPopover, NSPopoverBehaviorTransient, NSViewController,
    NSMenu, NSMenuItem
)
from Foundation import NSURL, NSRect, NSPoint, NSSize, NSObject, NSURLRequest
from WebKit import WKWebView, WKWebViewConfiguration


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
# Native notifications via pyobjc
# ============================================================
def _load_nsimage_from_url(url: str):
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
        img = _load_nsimage_from_url(image_url)
        if img is not None:
            try:
                n.setContentImage_(img)
            except Exception:
                pass
        NSUserNotificationCenter.defaultUserNotificationCenter().deliverNotification_(n)
    except Exception:
        try:
            def esc(x):
                return str(x).replace("\\", "\\\\").replace('"', '\\"')
            script = (
                f'display notification "{esc(body)}" '
                f'with title "{esc(title)}" '
                f'subtitle "{esc(subtitle)}"'
            )
            subprocess.Popen(
                ["osascript", "-e", script],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
        except Exception:
            pass


# ============================================================
# Menu bar app (NSStatusItem + NSPopover)
# ============================================================
URL_HOME = f"http://127.0.0.1:{server.PORT}"
URL_SETTINGS = f"http://127.0.0.1:{server.PORT}/settings.html"
URL_MINI_PLAYER = f"http://127.0.0.1:{server.PORT}/miniplayer.html"

class StatusItemController(NSObject):
    def init(self):
        self = objc.super(StatusItemController, self).init()
        if self is None: return None
        
        # 1. Create Status Item
        self.statusItem = NSStatusBar.systemStatusBar().statusItemWithLength_(NSVariableStatusItemLength)
        self.button = self.statusItem.button()
        self.button.setTitle_("♪")
        self.button.setTarget_(self)
        self.button.setAction_(objc.selector(self.togglePopover_, signature=b"v@:@"))
        
        # 2. Create Popover
        self.popover = NSPopover.alloc().init()
        self.popover.setBehavior_(NSPopoverBehaviorTransient)
        
        # 3. Create WebView
        config = WKWebViewConfiguration.alloc().init()
        
        # Size for mini player: matches miniplayer.html (320x480)
        frame = NSRect(NSPoint(0, 0), NSSize(320, 520))
        self.webView = WKWebView.alloc().initWithFrame_configuration_(frame, config)
        
        # 4. Create View Controller to host WebView
        self.vc = NSViewController.alloc().init()
        self.vc.setView_(self.webView)
        self.popover.setContentViewController_(self.vc)
        
        # Load the mini player
        url = NSURL.URLWithString_(URL_MINI_PLAYER)
        self.webView.loadRequest_(NSURLRequest.requestWithURL_(url))
        
        # Timer for updating status bar title
        self.timer = threading.Thread(target=self._update_loop, daemon=True)
        self.timer.start()
        
        return self

    def togglePopover_(self, sender):
        if self.popover.isShown():
            self.popover.performClose_(sender)
        else:
            # Refresh content on open to ensure fresh data
            self.webView.reload_(None)
            self.popover.showRelativeToRect_ofView_preferredEdge_(
                self.button.bounds(),
                self.button,
                1 # NSMinYEdge (bottom)
            )
            # Make sure it becomes key to receive events if needed
            self.popover.contentViewController().view().window().makeKeyWindow()

    def _update_loop(self):
        while True:
            try:
                data = server.CURRENT_NOW_PLAYING.get("data", {}) or {}
                playing = bool(data.get("playing"))
                title = self._build_menubar_title(data, playing)
                
                # Perform UI update on main thread
                # Note: setTitle_ expects an NSString. In PyObjC, str is automatically converted.
                self.button.performSelectorOnMainThread_withObject_waitUntilDone_(
                    objc.selector(self.button.setTitle_, signature=b"v@:@"), 
                    title, 
                    False
                )
            except Exception as e:
                print(f"[menu] update error: {e}")
            time.sleep(3)

    def _build_menubar_title(self, data, playing):
        mb = server.load_settings().get("menubar", {}) or {}
        show_icon = mb.get("show_icon", True)
        show_track = mb.get("show_track", True)
        show_artist = mb.get("show_artist", False)
        show_state = mb.get("show_state", True)
        max_len = int(mb.get("max_length", 28) or 28)

        name = data.get("name") or ""
        artist = data.get("artist") or ""

        if not name:
            return "♪"

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


def main():
    # Hook notifications
    server.NOTIFY_CALLBACK["fn"] = _pyobjc_notify
    
    # Hook app callbacks from server
    server.APP_CALLBACKS["quit"] = lambda: NSApp.performSelectorOnMainThread_withObject_waitUntilDone_(
        NSApp.terminate_, None, False
    )
    server.APP_CALLBACKS["open_window"] = lambda: webbrowser.open(URL_HOME)
    server.APP_CALLBACKS["open_settings"] = lambda: webbrowser.open(URL_SETTINGS)

    threading.Thread(target=_run_server, daemon=True).start()
    time.sleep(0.4)

    app = NSApplication.sharedApplication()
    controller = StatusItemController.alloc().init()
    
    # Keep controller alive
    app.setDelegate_(controller)
    
    app.run()


if __name__ == "__main__":
    main()
