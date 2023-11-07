# Movie Subtitle Copier Script (for Plex)

## Purpose
This script was created to find, copy, and rename .srt files found inside movie subdirectories, 
in order for Plex to easily find and use them.

*Note: This script is currently written to handle English subtitles only, but can easily be modified to handle other languages if needed.*


## Requirement

* Python3
* Existing /movies/ directory in Plex readable format (see below)
* .srt files existing inside a movie's subdirectory 


## Expected Directory Structure

```commandline
/PATH-TO-MEDIA/
.
└── video
    └── Movies
        ├── Sample.Movie.A.2023.1080p.BluRay.x265-ABC
        │   ├── Sample.Movie.A.2023.1080p.BluRay.x265-ABC.mp4
        │   └── Subs
        │       └── 2_English.srt
        └── Sample.Movie.B.2023.1080p.BluRay.x265-ABC
            ├── Sample.Movie.B.2023.1080p.BluRay.x265-ABC.mp4
            └── Subs
                └── 2_English.srt
```

## Expected Output Structure

```commandline
/PATH-TO-MEDIA/
.
└── video
    └── Movies
        ├── Sample.Movie.A.2023.1080p.BluRay.x265-ABC
        │   ├── Sample.Movie.A.2023.1080p.BluRay.x265-ABC.mp4
        │   ├── Sample.Movie.A.2023.1080p.BluRay.x265-ABC.en.srt    <----- COPIED FROM 2_English.srt
        │   └── Subs
        │       └── 2_English.srt
        └── Sample.Movie.B.2023.1080p.BluRay.x265-ABC
            ├── Sample.Movie.B.2023.1080p.BluRay.x265-ABC.mp4
            ├── Sample.Movie.B.2023.1080p.BluRay.x265-ABC.en.srt    <----- COPIED FROM 2_English.srt
            └── Subs
                └── 2_English.srt
```


## Sample Terminal Outputs

If you do not define the `movies_dir` path in the script, it will prompt you to enter it. 
```
python \path\to\script\subtitleCopier.py 
Enter the 'Movies' full directory path: \\plex-server\media\video\Movies
Process Start. Searching movies directory: '\\plex-server\media\video\Movies' ...
```

If an existing subtitles file already exists, it will skip that movie folder. 
```
Searching '\\plex-server\media\video\Movies\Sample.Movie.A.2023.1080p.BluRay.x265-ABC' ...
Found video file: \\plex-server\media\video\Movies\Sample.Movie.A.2023.1080p.BluRay.x265-ABC\Sample.Movie.A.2023.1080p.BluRay.x265-ABC.mp4
Found an existing srt file in video root: \\plex-server\media\video\Movies\Sample.Movie.A.2023.1080p.BluRay.x265-ABC\Sample.Movie.A.2023.1080p.BluRay.x265-ABC.en.srt
No further action needed. Skipping.
```

When a subtitles file is found, it will be copied next to the movie file and renamed appropriately.
```
Searching '\\plex-server\media\video\Movies\Sample.Movie.B.2023.1080p.BluRay.x265-ABC' ...
Found video file: \\plex-server\media\video\Movies\Sample.Movie.B.2023.1080p.BluRay.x265-ABC\Sample.Movie.B.2023.1080p.BluRay.x265-ABC.mp4
Found srt file: \\plex-server\media\video\Movies\Sample.Movie.B.2023.1080p.BluRay.x265-ABC\Subs\2_English.srt
Copying found srt to '\\plex-server\media\video\Movies\Sample.Movie.B.2023.1080p.BluRay.x265-ABC\Sample.Movie.B.2023.1080p.BluRay.x265-ABC.en.srt' ...
Copy completed.
```

When no subtitles file is found, it will skip that movie folder.
```
Searching '\\plex-server\media\video\Movies\Sample.Movie.C.2023.1080p.BluRay.x265-ABC' ...
Found video file: \\plex-server\media\video\Movies\Sample.Movie.C.2023.1080p.BluRay.x265-ABC\Sample.Movie.C.2023.1080p.BluRay.x265-ABC.mkv
No srt file found. Skipping.
```

When the process is complete, it will display quick stats of what was found and performed.
```
Process Completed.

video files found: 282
srt files found: 223
srt copies made: 1
```

