import subprocess

# Replace these URLs with the actual URLs of your video segmentsclear
segment_urls = [
    "https://eu-02.files.nextcdn.org/stream/02/16/b9d276234e046153ee7424cf59d568b339d6c061b389ca5dfc8d6f541a72777d/segment-1-v1-a1.ts"

    # Add more segment URLs as needed
]

# Use ffmpeg to concatenate the segments into a single video file
ffmpeg_cmd = ['ffmpeg'] + ['-i'] + segment_urls + ['-c', 'copy', 'output_video.ts']


# Run the ffmpeg command
subprocess.run(ffmpeg_cmd)

ffmpeg -i "https://eu-02.files.nextcdn.org/stream/02/16/b9d276234e046153ee7424cf59d568b339d6c061b389ca5dfc8d6f541a72777d/segment-1-v1-a1.ts" -c copy output_video.ts
