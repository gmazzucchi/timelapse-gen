# Generate the video from the images
# ffmpeg -framerate 20 -pattern_type glob -i '*.jpg' -c:v libx264 -pix_fmt yuv420p out.mp4

import ffmpeg, signal, shutil, time, datetime

COUNTER = 0
CONTENT_FOLDER = "./content/"
VIDEO_FOLDER = "./old-videos/"
FRAMES_PER_MINUTE = 20

input_source = "/dev/video2"
duration = 1 / 30

def generate_video(self, *args):
    current_datetime = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    command = (
        ffmpeg.input(CONTENT_FOLDER + "*.jpg", pattern_type="glob", framerate=FRAMES_PER_MINUTE)
        .output(VIDEO_FOLDER + "timelapse" + current_datetime + ".mp4", crf=17, pix_fmt="yuv420p")
        .overwrite_output()
    )
    ffmpeg.run(command)
    exit()

if __name__ == "__main__":
    _total, _used, free = shutil.disk_usage("/")
    if free < 10_000_000:
        print("Disk space is low, exiting...")
        exit()

    signal.signal(signal.SIGINT, generate_video)
    signal.signal(signal.SIGTERM, generate_video)
    while True:
        output_file = CONTENT_FOLDER +  "./i" + str(COUNTER).zfill(7) + ".jpg"
        COUNTER += 1
        command = (
            ffmpeg.input(input_source, t=duration)
            .output(output_file, vframes=1)
            .overwrite_output()
        )
        ffmpeg.run(command)
        time.sleep(60 / FRAMES_PER_MINUTE)
