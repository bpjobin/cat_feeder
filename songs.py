# https://github.com/onebeartoe/media-players/blob/master/pi-ezo/src/main/java/org/onebeartoe/media/piezo/ports/rtttl/BuiltInSongs.java
# The following RTTTL tunes were extracted from the following:
# most of which originated from here:
# http://www.picaxe.com/RTTTL-Ringtones-for-Tune-Command/
#

SONGS = [
    'Canada-O:d=16,o=5,b=180:2g,4a#,8p,8a#,2d#,4p,4f,4g,4g#,4a#,4c6,2f,2g,4a,8p,8a,2a#,4p,8c.,p,4d6,4d6,4c6,4c6,2a#.,f,8p,g,4g#,8p,g,8f.,p,g,8p,g#,4a#,8p,g#,8g.,p,8g#,p,a#,4c6,4a#,4g#,4g,2f',
    'Canada(O:d=4,o=5,b=100:2g,a#,8p,8a#,2d#,p,f,g,g#,a#,c6,2f,2p,2g,a,8p,8a,2a#,p,c6,2d6,2c6,1a#',
    'TakeOnMe:d=4,o=4,b=160:8f#5,8f#5,8f#5,8d5,8p,8b,8p,8e5,8p,8e5,8p,8e5,8g#5,8g#5,8a5,8b5,8a5,8a5,8a5,8e5,8p,8d5,8p,8f#5,8p,8f#5,8p,8f#5,8e5,8e5,8f#5,8e5,8f#5,8f#5,8f#5,8d5,8p,8b,8p,8e5,8p,8e5,8p,8e5,8g#5,8g#5,8a5,8b5,8a5,8a5,8a5,8e5,8p,8d5,8p,8f#5,8p,8f#5,8p,8f#5,8e5,8e5',
    'HockeyNi:d=4,o=5,b=200:8c,8c,8c,f,d,1c6,8c,8c,8c,f,d,8d6,1c6,8f,8f,8f,a,c6,d6.,d#6,8d6,a#,c6.,c#6,8c6,g#,1c6,8c,8c,8c,f,d,1c6,8c,8c,8c,f,d6,8d6,1c6,8f,8f,8f,a,c6,d6.,d#6,8d6,a#,c6.,c#6,8c6,g#,1c6',
    'InDaClub:d=4,o=5,b=160:d#6,16d,16p,8d6,p,16d,16p,16d,16p,p,16d,16p,16d,16p,p,16d,16p,16d,16p,d6,16d#,16p,8d#6,p,16d#,16p,16d#,16p,c6,16c,16p,8d6,p,16c,16p,16c,16p,d#6,16d,16p,8d6,p,16d,16p,16d,16p,p,16d,16p,16d,16p,p,16d,16p,16d,16p,d6,16d#,16p,8d#6,p,16d#,16p,16d#,16p,c6,16c,16p,8d6,p,16c,16p,16c,16p',
]

def find(name):
    for song in SONGS:
        song_name = song.split(':')[0]
        if song_name == name:
            return song
