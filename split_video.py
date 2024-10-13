from moviepy.video.io.VideoFileClip import VideoFileClip # type: ignore

def split_video(input_file, num_segments):
    # Load video file
    video = VideoFileClip(input_file)
    duration = video.duration # Duration of the video in seconds
    segment_duration = duration / num_segments #duration of each segment
    
    # Split the video into segments
    for i in range(num_segments):
        start_time = i * segment_duration
        end_time = (i + 1) * segment_duration
        segment = video.subclip(start_time, end_time)
        output_file = f"segment_{i+1}.mp4"
        segment.write_videofile(output_file, codec="libx264")
        
    print(f"Video split into {num_segments} segments successfully!")
    

# Example usage
input_file = "/Users/jordanjones/Movies/Police Surprise Man at His Doorstep Just After He Escapes Them.mp4"
num_segments = 4
split_video(input_file, num_segments)
