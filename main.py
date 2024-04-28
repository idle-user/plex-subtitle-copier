import os
import shutil

movies_dir = None  # the movies directory goes here, else will be prompted
test_run = False  # run as test - no copying would be performed
srt_file_min_size_kb = 10  # smallest size in KB for .srt file before trying to replace with a bigger file

video_extensions = ['.mp4', '.mkv', '.avi', '.mov', '.mpeg', '.wmv', '.mpegts', '.ts', '.asf']


def find_and_copy_english_srt(movies_root, dry_run=True):
    videos_found = 0
    srt_found = 0
    srt_replaced = 0
    srt_copy_cnt = 0
    might_need_rerun = False  # flag to notify if a small .srt file found on first run through

    maybe_dry_run_text = '[DRY RUN] ' if dry_run else ''
    print(f"{maybe_dry_run_text}Process Start. Searching movies directory: '{movies_root}' ...")

    top_level_movie_dirs = [os.path.join(movies_root, filename)
                            for filename in os.listdir(movies_root)
                            if os.path.isdir(os.path.join(movies_root, filename))]

    for movie_dir in top_level_movie_dirs:
        print(f"\nSearching '{movie_dir}' ...")
        video_file = None
        srt_file = None

        # find video file
        for filename in os.listdir(movie_dir):
            file_path = os.path.join(movie_dir, filename)
            for video_ext in video_extensions:
                if file_path.endswith(video_ext):
                    video_file = file_path
                    print(f"Found video file: {video_file}")
                    videos_found = videos_found + 1
                    break
            if video_file:
                break

        # skip if no video found
        if video_file is None:
            print("No video file found. Skipping.")
            continue

        # skip if srt already exists
        root_srt_file = f"{os.path.splitext(video_file)[0]}.en.srt"
        root_srt_file_size_kb = None
        if os.path.exists(root_srt_file):
            srt_found = srt_found + 1
            print(f"Found an existing srt file in video root: {root_srt_file}")
            root_srt_file_size_kb = os.path.getsize(root_srt_file) / 1024
            # if existing is found, but under 10kb, it's bad? Try to replace
            if root_srt_file_size_kb < srt_file_min_size_kb:
                print(f"But its a small size.. will fetch larger size if possible: {root_srt_file_size_kb} KB")
            else:
                print(f"No further action needed. Skipping.")
                continue

        # find subtitles in a sub folder - usually 'subs' but we'll search 1 level deep just in case
        for filename in os.listdir(movie_dir):
            subs_dir_path = os.path.join(movie_dir, filename)
            if os.path.isdir(subs_dir_path):
                # find english srt file
                for subs_file in os.listdir(subs_dir_path):
                    if subs_file.endswith('.srt') and 'english' in subs_file.lower():
                        srt_file = os.path.join(subs_dir_path, subs_file)
                        srt_file_size_kb = os.path.getsize(srt_file) / 1024
                        # attempt to replace small srt
                        if root_srt_file_size_kb:
                            if srt_file_size_kb > root_srt_file_size_kb:
                                srt_replaced = srt_replaced + 1
                                print(f"Bigger srt file found: {srt_file_size_kb} KB - {srt_file}")
                                break
                            srt_file = None
                        else:
                            print(f"Found srt file: {srt_file}")
                            srt_found = srt_found + 1
                            if srt_file_size_kb < srt_file_min_size_kb:
                                print("...but it's a small file. Try running the script again to replace it.")
                                might_need_rerun = True
                            break
            if srt_file:
                break

        # skip if no srt found
        if srt_file is None:
            print("No srt file found. Skipping.")
            continue

        # copy srt file
        print(f"Copying found srt to '{root_srt_file}' ...")
        if not dry_run:
            shutil.copy(srt_file, root_srt_file)
        print("Copy completed.")
        srt_copy_cnt = srt_copy_cnt + 1

    print(f"\n{maybe_dry_run_text}Process Completed.\n")
    print(f"video files found: {videos_found}")
    print(f"srt files found: {srt_found}")
    print(f"srt copies made: {srt_copy_cnt}")
    print(f"srt files replaced: {srt_replaced}")

    if might_need_rerun:
        print(f"\n{maybe_dry_run_text}At least 1 small/bad .srt file found on first attempt. Rerun to try to replace.")


if __name__ == '__main__':
    if not movies_dir:
        movies_dir = input("Enter the 'Movies' full directory path: ")

    if os.path.exists(movies_dir) and os.path.isdir(movies_dir):
        find_and_copy_english_srt(movies_dir, test_run)
    else:
        print(f"The path '{movies_dir}' does not exist or is not a directory.")
