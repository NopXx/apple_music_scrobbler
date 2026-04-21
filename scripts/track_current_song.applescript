-- ติดตามเพลงที่กำลังฟังใน Apple Music
-- บันทึกทุกครั้งที่เพลงเริ่มเล่น (รวมถึงเล่นเพลงเดิมซ้ำ)

property logFile : (POSIX path of (path to home folder)) & "Desktop/vibe-code/apple-music/played_songs.log"
property lastTrackID : ""
property lastPosition : 0

on run
	repeat
		try
			if application "Music" is running then
				tell application "Music"
					if player state is playing then
						set currentTrack to current track
						set trackName to name of currentTrack
						set trackArtist to artist of currentTrack
						set trackAlbum to album of currentTrack
						set trackDuration to duration of currentTrack
						set currentPosition to player position
						set trackID to (trackName & " - " & trackArtist) as string

						-- log เมื่อ:
						-- 1) เปลี่ยนเพลงใหม่
						-- 2) เพลงเดิมแต่ position ย้อนกลับมาต้น (replay / กด prev / seek ไปต้น)
						set isNewTrack to (trackID is not equal to lastTrackID)
						set isReplay to (trackID is equal to lastTrackID) and (currentPosition < 3) and (lastPosition > 5)

						if isNewTrack or isReplay then
							my logTrack(trackName, trackArtist, trackAlbum, trackDuration, isReplay)
							my displayInfo(trackName, trackArtist, trackAlbum, isReplay)
							set lastTrackID to trackID
						end if

						set lastPosition to currentPosition
					end if
				end tell
			end if
		on error errMsg
			log "Error: " & errMsg
		end try

		delay 2
	end repeat
end run

on logTrack(trackName, trackArtist, trackAlbum, trackDuration, isReplay)
	set timeStamp to (do shell script "date '+%Y-%m-%d %H:%M:%S'")
	if isReplay then
		set tag to "REPLAY"
	else
		set tag to "PLAY  "
	end if
	set logLine to timeStamp & " | " & tag & " | " & trackName & " | " & trackArtist & " | " & trackAlbum & " | " & (trackDuration as string) & "s"

	do shell script "echo " & quoted form of logLine & " >> " & quoted form of logFile
end logTrack

on displayInfo(trackName, trackArtist, trackAlbum, isReplay)
	if isReplay then
		set notifTitle to "🔁 Replaying"
	else
		set notifTitle to "♪ Now Playing"
	end if
	set notifBody to trackName & " — " & trackArtist
	display notification notifBody with title notifTitle subtitle trackAlbum
end displayInfo
