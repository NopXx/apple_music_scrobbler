// Shared i18n for index.html + settings.html
// Pages use data-i18n / data-i18n-html / data-i18n-placeholder / data-i18n-title.
// JS uses window.t(key, vars) for dynamic strings.
(function () {
  const DICTS = {
    th: {
      // --- nav / common ---
      "nav.settings": "Settings",
      "nav.back": "Back",
      "common.save": "บันทึก",
      "common.cancel": "ยกเลิก",
      "common.close": "ปิด",
      "common.search": "Search",
      "common.delete_all": "ลบทั้งหมด",
      "common.original_prefix": "Original: ",
      "common.searching": "กำลังค้นหา...",
      "common.error_searching": "ค้นหาผิดพลาด",

      // --- index / player ---
      "player.idle": "ยังไม่ได้เล่นเพลง — เปิด Apple Music แล้วกด play",
      "player.now_playing": "Now Playing",
      "player.paused": "Paused",
      "player.playing_badge": "Playing",
      "player.paused_badge": "Paused",
      "player.wait_scrobble": "รอ Scrobble",
      "player.scrobbled": "Scrobbled",
      "player.change_artwork": "Change artwork",
      "player.change_artwork_tip": "ดึงรูปปกใหม่",
      "player.edit_info": "Edit info",
      "player.edit_info_tip": "แก้ข้อมูลเพลง",
      "player.no_history": "ยังไม่มีประวัติ",
      "player.recent": "Recent Activity",
      "player.items_suffix": " items",

      "modal.edit_title": "Edit Track Info",
      "modal.artist": "Artist",
      "modal.track": "Track",
      "modal.album": "Album",
      "modal.select_artwork": "Select Artwork",
      "modal.search_placeholder": "Search song or artist...",
      "modal.enter_song": "กรอกชื่อเพลงเพื่อค้นหา...",
      "modal.no_results": "ไม่พบผลลัพธ์",
      "modal.save_artwork_failed": "Failed to save artwork",

      "event.play": "Play",
      "event.replay": "Replay",
      "event.scrobbled": "Scrobbled",

      // --- settings ---
      "settings.title": "Settings",
      "settings.subtitle": "ตั้งค่าการเชื่อมต่อ scrobble, webhook, และจัดการข้อมูล",

      "lang.card_title": "Language / ภาษา",
      "lang.card_desc": "เลือกภาษาที่ใช้แสดงผลในแอป",
      "lang.th": "ไทย",
      "lang.en": "English",

      "lastfm.title": "Last.fm Scrobbling",
      "lastfm.desc": "เชื่อมบัญชี Last.fm เพื่อ scrobble เพลงที่เล่นอัตโนมัติ",
      "lastfm.connected_as": "Connected as",
      "lastfm.disconnect": "Disconnect",
      "lastfm.enable_scrobbling": "เปิดใช้งาน Scrobbling",
      "lastfm.connect": "Connect with Last.fm",
      "lastfm.setup_title": "ต้องใส่ API Keys ของคุณก่อน",
      "lastfm.setup_desc": "Last.fm ให้ฟรี ใช้เวลาไม่ถึงนาที:",
      "lastfm.step1": "กดปุ่มด้านล่างเพื่อเปิดหน้าสมัคร",
      "lastfm.step2": "กรอกชื่อ application (อะไรก็ได้) แล้ว Submit",
      "lastfm.step3_html": "Copy ค่า <b>API key</b> และ <b>Shared secret</b> มาวางในช่องด้านล่าง",
      "lastfm.step4_html": "กด \"Connect with Last.fm\" อีกครั้ง",
      "lastfm.open_register": "เปิดหน้าสมัคร API Keys",
      "lastfm.api_keys": "API Keys",
      "lastfm.save_keys": "Save Keys",
      "lastfm.waiting_title": "รอการอนุมัติบน Last.fm...",
      "lastfm.waiting_desc": "อนุมัติในหน้าเว็บที่เพิ่งเปิดขึ้น — จะเชื่อมต่อให้อัตโนมัติ",
      "lastfm.reopen_html": "หากหน้าไม่เปิด: <a href=\"#\" id=\"lf-reopen-auth\" style=\"color:var(--accent-blue);\">คลิกที่นี่เพื่อเปิดใหม่</a>",
      "lastfm.cancel": "Cancel",
      "lastfm.toast_saved_keys": "บันทึก Keys แล้ว",
      "lastfm.toast_need_keys": "ต้องกรอก API Key และ Shared Secret ก่อน",
      "lastfm.toast_connected": "✓ เชื่อมต่อสำเร็จ: {name}",
      "lastfm.toast_cancelled": "ยกเลิกแล้ว",
      "lastfm.toast_on": "เปิด Scrobbling แล้ว",
      "lastfm.toast_off": "ปิด Scrobbling แล้ว",
      "lastfm.confirm_disconnect": "ยกเลิกการเชื่อมต่อ Last.fm?",

      "webhook.title": "Webhook",
      "webhook.desc": "ส่ง POST JSON เมื่อเกิด event: play, replay, pause, resume, scrobble",
      "webhook.url": "Webhook URL",
      "webhook.heartbeat": "Heartbeat Interval",
      "webhook.heartbeat_hint": "วินาที — ส่งข้อมูลซ้ำทุกๆกี่วินาที, 0 = ปิด",
      "webhook.enable": "เปิดใช้งาน Webhook",
      "webhook.test": "ทดสอบส่ง",
      "webhook.save": "Save",
      "webhook.saved": "บันทึก Webhook แล้ว",
      "webhook.example_title": "ตัวอย่าง payload",
      "webhook.example_note": "eventName: <b>nowplaying</b> (play/replay/resume) · <b>paused</b> (pause/stopped) · <b>scrobble</b>",
      "webhook.need_url": "กรอก URL ก่อน",
      "webhook.sent_ok": "ส่งสำเร็จ (HTTP {status})",

      "scrobble.title": "Scrobble Threshold",
      "scrobble.desc": "กำหนดเงื่อนไขก่อนส่ง scrobble ไปยัง Last.fm",
      "scrobble.percent": "เล่นผ่านกี่ % ถึงจะ scrobble (หรือ 240 วิขึ้นไป)",
      "scrobble.min": "ข้ามเพลงที่สั้นกว่ากี่วินาที",
      "scrobble.saved": "บันทึก Threshold แล้ว",

      "notif.title": "Notifications",
      "notif.desc": "แจ้งเตือนบนเดสก์ท็อปเมื่อเล่นเพลงใหม่ / scrobble (ใช้ได้เฉพาะโหมด menu bar app)",
      "notif.enable": "เปิดใช้งาน notifications",
      "notif.on_play": "เมื่อเล่นเพลงใหม่",
      "notif.on_scrobble": "เมื่อ scrobble สำเร็จ",

      "menubar.title": "Menu Bar",
      "menubar.desc": "เลือกข้อมูลที่จะแสดงบน menu bar ด้านบนสุด (ใช้ได้เฉพาะโหมด menu bar app)",
      "menubar.show_icon": "แสดงไอคอน ♪",
      "menubar.show_state": "แสดงสถานะเล่น/หยุด (▶ / ⏸)",
      "menubar.show_track": "แสดงชื่อเพลง",
      "menubar.show_artist": "แสดงชื่อศิลปิน",
      "menubar.max_length": "ความยาวข้อความสูงสุด (ตัวอักษร)",

      "data.title": "Play History",
      "data.desc": "Export, Import รองรับ JSON (play history), CSV, และ JSON edit history (auto-detect)",
      "data.export_json": "Export JSON",
      "data.export_csv": "Export CSV",
      "data.import": "Import",
      "data.clear": "ลบประวัติทั้งหมด",
      "data.confirm_clear": "ลบประวัติทั้งหมด? ไม่สามารถเรียกคืนได้",
      "data.cleared": "ลบแล้ว",
      "data.imported": "Import สำเร็จ {n} records",

      "edits.title": "Edit History",
      "edits.desc": "แก้ชื่อเพลงที่ Apple Music ให้ข้อมูลผิด — ระบบจะใช้ชื่อที่แก้ไว้ก่อน scrobble/ส่ง webhook ทุกครั้ง",
      "edits.export": "Export",
      "edits.import": "Import",
      "edits.search_placeholder": "ค้นหา artist / track / album...",
      "edits.no_results": "ไม่พบผลลัพธ์",
      "edits.empty": "ยังไม่มีรายการแก้ไข",
      "edits.delete": "ลบ",
      "edits.confirm_clear": "ลบ edit history ทั้งหมด?",
      "edits.imported": "Import สำเร็จ {n} edits",
      "edits.not_edit_format": "ไฟล์ไม่ใช่ edit history (import เป็น {type} แทน)",
      "edits.count": "{start}–{end} จาก {total}",
      "edits.count_filtered": "{start}–{end} จาก {total} (กรองจาก {all})",
      "edits.page_size_suffix": " / page",
    },
    en: {
      // --- nav / common ---
      "nav.settings": "Settings",
      "nav.back": "Back",
      "common.save": "Save",
      "common.cancel": "Cancel",
      "common.close": "Close",
      "common.search": "Search",
      "common.delete_all": "Delete all",
      "common.original_prefix": "Original: ",
      "common.searching": "Searching...",
      "common.error_searching": "Error searching",

      // --- index / player ---
      "player.idle": "Nothing playing — open Apple Music and hit play",
      "player.now_playing": "Now Playing",
      "player.paused": "Paused",
      "player.playing_badge": "Playing",
      "player.paused_badge": "Paused",
      "player.wait_scrobble": "Waiting to scrobble",
      "player.scrobbled": "Scrobbled",
      "player.change_artwork": "Change artwork",
      "player.change_artwork_tip": "Fetch new artwork",
      "player.edit_info": "Edit info",
      "player.edit_info_tip": "Edit track info",
      "player.no_history": "No history yet",
      "player.recent": "Recent Activity",
      "player.items_suffix": " items",

      "modal.edit_title": "Edit Track Info",
      "modal.artist": "Artist",
      "modal.track": "Track",
      "modal.album": "Album",
      "modal.select_artwork": "Select Artwork",
      "modal.search_placeholder": "Search song or artist...",
      "modal.enter_song": "Enter a song name to search...",
      "modal.no_results": "No results",
      "modal.save_artwork_failed": "Failed to save artwork",

      "event.play": "Play",
      "event.replay": "Replay",
      "event.scrobbled": "Scrobbled",

      // --- settings ---
      "settings.title": "Settings",
      "settings.subtitle": "Configure scrobbling, webhooks, and data management",

      "lang.card_title": "Language / ภาษา",
      "lang.card_desc": "Pick the display language",
      "lang.th": "ไทย",
      "lang.en": "English",

      "lastfm.title": "Last.fm Scrobbling",
      "lastfm.desc": "Link your Last.fm account to scrobble plays automatically",
      "lastfm.connected_as": "Connected as",
      "lastfm.disconnect": "Disconnect",
      "lastfm.enable_scrobbling": "Enable scrobbling",
      "lastfm.connect": "Connect with Last.fm",
      "lastfm.setup_title": "You need your own API keys first",
      "lastfm.setup_desc": "Last.fm gives them away free — under a minute:",
      "lastfm.step1": "Click the button below to open the signup page",
      "lastfm.step2": "Enter any application name then Submit",
      "lastfm.step3_html": "Copy the <b>API key</b> and <b>Shared secret</b> into the fields below",
      "lastfm.step4_html": "Click \"Connect with Last.fm\" again",
      "lastfm.open_register": "Open API Keys signup",
      "lastfm.api_keys": "API Keys",
      "lastfm.save_keys": "Save keys",
      "lastfm.waiting_title": "Waiting for Last.fm approval...",
      "lastfm.waiting_desc": "Approve on the page that just opened — we'll connect automatically",
      "lastfm.reopen_html": "Didn't open? <a href=\"#\" id=\"lf-reopen-auth\" style=\"color:var(--accent-blue);\">click here to reopen</a>",
      "lastfm.cancel": "Cancel",
      "lastfm.toast_saved_keys": "Keys saved",
      "lastfm.toast_need_keys": "API Key and Shared Secret are required",
      "lastfm.toast_connected": "✓ Connected: {name}",
      "lastfm.toast_cancelled": "Cancelled",
      "lastfm.toast_on": "Scrobbling on",
      "lastfm.toast_off": "Scrobbling off",
      "lastfm.confirm_disconnect": "Disconnect Last.fm?",

      "webhook.title": "Webhook",
      "webhook.desc": "POST JSON on events: play, replay, pause, resume, scrobble",
      "webhook.url": "Webhook URL",
      "webhook.heartbeat": "Heartbeat interval",
      "webhook.heartbeat_hint": "seconds — repeat payload every N seconds, 0 = off",
      "webhook.enable": "Enable webhook",
      "webhook.test": "Send test",
      "webhook.save": "Save",
      "webhook.saved": "Webhook saved",
      "webhook.example_title": "Example payload",
      "webhook.example_note": "eventName: <b>nowplaying</b> (play/replay/resume) · <b>paused</b> (pause/stopped) · <b>scrobble</b>",
      "webhook.need_url": "URL required",
      "webhook.sent_ok": "Sent (HTTP {status})",

      "scrobble.title": "Scrobble threshold",
      "scrobble.desc": "Conditions before scrobbling to Last.fm",
      "scrobble.percent": "Scrobble after what % played (or 240s+)",
      "scrobble.min": "Skip tracks shorter than (seconds)",
      "scrobble.saved": "Threshold saved",

      "notif.title": "Notifications",
      "notif.desc": "Desktop notifications on new play / scrobble (menu bar app only)",
      "notif.enable": "Enable notifications",
      "notif.on_play": "On new play",
      "notif.on_scrobble": "On scrobble",

      "menubar.title": "Menu Bar",
      "menubar.desc": "Choose what to show in the top menu bar (menu bar app only)",
      "menubar.show_icon": "Show icon ♪",
      "menubar.show_state": "Show play/pause state (▶ / ⏸)",
      "menubar.show_track": "Show track name",
      "menubar.show_artist": "Show artist name",
      "menubar.max_length": "Max text length (chars)",

      "data.title": "Play history",
      "data.desc": "Export / import — JSON (play history), CSV, or JSON edit history (auto-detect)",
      "data.export_json": "Export JSON",
      "data.export_csv": "Export CSV",
      "data.import": "Import",
      "data.clear": "Delete all history",
      "data.confirm_clear": "Delete all history? This can't be undone.",
      "data.cleared": "Deleted",
      "data.imported": "Imported {n} records",

      "edits.title": "Edit history",
      "edits.desc": "Fix track names Apple Music gets wrong — edits are applied before every scrobble / webhook",
      "edits.export": "Export",
      "edits.import": "Import",
      "edits.search_placeholder": "Search artist / track / album...",
      "edits.no_results": "No results",
      "edits.empty": "No edits yet",
      "edits.delete": "Delete",
      "edits.confirm_clear": "Delete all edit history?",
      "edits.imported": "Imported {n} edits",
      "edits.not_edit_format": "Not an edit-history file (imported as {type} instead)",
      "edits.count": "{start}–{end} of {total}",
      "edits.count_filtered": "{start}–{end} of {total} (filtered from {all})",
      "edits.page_size_suffix": " / page",
    },
  };

  let LANG = localStorage.getItem("ams_lang") || "th";
  if (LANG !== "th" && LANG !== "en") LANG = "th";

  function t(key, vars) {
    const d = DICTS[LANG] || DICTS.th;
    let s = d[key];
    if (s == null) s = DICTS.th[key];
    if (s == null) s = key;
    if (vars) {
      for (const k in vars) {
        s = s.split("{" + k + "}").join(vars[k]);
      }
    }
    return s;
  }

  function applyI18n(root) {
    root = root || document;
    root.querySelectorAll("[data-i18n]").forEach((el) => {
      el.textContent = t(el.getAttribute("data-i18n"));
    });
    root.querySelectorAll("[data-i18n-html]").forEach((el) => {
      el.innerHTML = t(el.getAttribute("data-i18n-html"));
    });
    root.querySelectorAll("[data-i18n-placeholder]").forEach((el) => {
      el.setAttribute("placeholder", t(el.getAttribute("data-i18n-placeholder")));
    });
    root.querySelectorAll("[data-i18n-title]").forEach((el) => {
      el.setAttribute("title", t(el.getAttribute("data-i18n-title")));
    });
    document.documentElement.setAttribute("lang", LANG);
    if (window.lucide && typeof window.lucide.createIcons === "function") {
      try { window.lucide.createIcons(); } catch (e) {}
    }
  }

  function setLang(lang, opts) {
    opts = opts || {};
    if (lang !== "th" && lang !== "en") return;
    LANG = lang;
    localStorage.setItem("ams_lang", lang);
    applyI18n();
    if (opts.persist !== false) {
      try {
        fetch("/api/settings", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ language: lang }),
        }).catch(() => {});
      } catch (e) {}
    }
    window.dispatchEvent(new CustomEvent("ams:lang", { detail: lang }));
  }

  async function initFromServer() {
    try {
      const r = await fetch("/api/settings");
      const s = await r.json();
      if (s.language && (s.language === "th" || s.language === "en") && s.language !== LANG) {
        setLang(s.language, { persist: false });
      }
    } catch (e) {}
  }

  window.ams_i18n = { t, applyI18n, setLang, initFromServer, getLang: () => LANG };
  window.t = t;

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", () => {
      applyI18n();
      initFromServer();
    });
  } else {
    applyI18n();
    initFromServer();
  }
})();
