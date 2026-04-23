-- เขียนสถานะเพลงปัจจุบันเป็น JSON ทุก 2 วินาที + บันทึก log

property baseDir : (POSIX path of (path to home folder)) & "Desktop/vibe-code/apple-music/"
property jsonFile : baseDir & "now_playing.json"
property logFile : baseDir & "played_songs.log"
property lastTrackID : ""
property lastPosition : 0
property lastState : "stopped"

on run
	repeat
		try
			set jsonText to "{\"playing\": false}"

			if application "Music" is running then
				tell application "Music"
					set ps to player state as string
					if ps is "playing" or ps is "paused" then
						set trackName to ""
						set trackArtist to ""
						set trackAlbum to ""
						set trackDuration to 0
						set currentPosition to 0
						
						try
							set currentPosition to player position
						end try

						try
							set t to current track
							try
								set trackName to name of t
							end try
							try
								set trackArtist to artist of t
							end try
							try
								set trackAlbum to album of t
							end try
							try
								set trackDuration to duration of t
							end try
							
							-- Fallback for stream title
							if trackName is "" or trackName is missing value then
								try
									set trackName to current stream title
								end try
							end if
						end try

						if trackName is not "" and trackArtist is not "" then
							set isPlaying to (ps is "playing")
							set trackID to trackName & " - " & trackArtist
							set isNewTrack to (trackID is not equal to lastTrackID)
							set isReplay to (trackID is equal to lastTrackID) and (currentPosition < 3) and (lastPosition > 5)

							if isPlaying and (isNewTrack or isReplay) then
								set eventTag to "PLAY  "
								if isReplay then set eventTag to "REPLAY"
								my logEvent(eventTag, trackName, trackArtist, trackAlbum, trackDuration)
								set lastTrackID to trackID
							else if isPlaying and lastState is "paused" then
								my logEvent("RESUME", trackName, trackArtist, trackAlbum, trackDuration)
							else if (not isPlaying) and lastState is "playing" then
								my logEvent("PAUSE ", trackName, trackArtist, trackAlbum, trackDuration)
							end if

							set lastState to ps
							set lastPosition to currentPosition

							set jsonText to "{" & ¬
								"\"playing\": " & (isPlaying as string) & "," & ¬
								"\"name\": " & my jsonEscape(trackName) & "," & ¬
								"\"artist\": " & my jsonEscape(trackArtist) & "," & ¬
								"\"album\": " & my jsonEscape(trackAlbum) & "," & ¬
								"\"duration\": " & trackDuration & "," & ¬
								"\"position\": " & currentPosition & ¬
								"}"
						end if
					end if
				end tell
			end if

			my writeFile(jsonFile, jsonText)
		on error errMsg
			log "Error: " & errMsg
		end try

		delay 2
	end repeat
end run

on jsonEscape(s)
	set s to my replaceText(s, "\\", "\\\\")
	set s to my replaceText(s, "\"", "\\\"")
	return "\"" & s & "\""
end jsonEscape

on replaceText(srcText, findText, replaceWith)
	set AppleScript's text item delimiters to findText
	set parts to text items of srcText
	set AppleScript's text item delimiters to replaceWith
	set result to parts as string
	set AppleScript's text item delimiters to ""
	return result
end replaceText

on writeFile(fp, txt)
	do shell script "cat > " & quoted form of fp & " <<'JSONEOF'
" & txt & "
JSONEOF"
end writeFile

on logEvent(tag, trackName, trackArtist, trackAlbum, trackDuration)
	set timeStamp to (do shell script "date '+%Y-%m-%d %H:%M:%S'")
	set logLine to timeStamp & " | " & tag & " | " & trackName & " | " & trackArtist & " | " & trackAlbum & " | " & (trackDuration as string) & "s"
	do shell script "echo " & quoted form of logLine & " >> " & quoted form of logFile
end logEvent
