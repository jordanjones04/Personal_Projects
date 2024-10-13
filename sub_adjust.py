import re

def parse_srt_file(file_path):
    subtitles = []
    with open(file_path, 'r', encoding='utf-8-sig') as file:  # Use utf-8-sig to handle BOM
        lines = file.readlines()

    # Initialize variables to store subtitle data
    index = None
    start_time = None
    end_time = None
    text_lines = []

    for line in lines:
        line = line.strip()
        if not line:
            if index is not None and start_time and end_time and text_lines:
                subtitle = {
                    'index': index,
                    'start_time': start_time,
                    'end_time': end_time,
                    'text': '\n'.join(text_lines)
                }
                subtitles.append(subtitle)
            # Reset variables for the next subtitle
            index = None
            start_time = None
            end_time = None
            text_lines = []
        elif index is None:
            index = int(line.lstrip('\ufeff'))  # Remove BOM and convert to int
        elif re.match(r'\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}', line):
            start, end = line.split(' --> ')
            start_time = start.strip()
            end_time = end.strip()
        else:
            text_lines.append(line)

    return subtitles

def adjust_timing(subtitles, seconds_to_adjust):
    adjusted_subtitles = []
    for subtitle in subtitles:
        start_time = subtitle['start_time']
        end_time = subtitle['end_time']

        # Convert start and end times to seconds with milliseconds
        start_seconds = time_to_seconds_with_ms(start_time)
        end_seconds = time_to_seconds_with_ms(end_time)

        # Adjust timing
        start_seconds -= seconds_to_adjust
        end_seconds -= seconds_to_adjust

        # Convert back to the srt format with milliseconds
        adjusted_start_time = seconds_to_time_with_ms(start_seconds)
        adjusted_end_time = seconds_to_time_with_ms(end_seconds)

        # Create the adjusted subtitle entry
        adjusted_subtitle = {
            'index': subtitle['index'],
            'start_time': adjusted_start_time,
            'end_time': adjusted_end_time,
            'text': subtitle['text']
        }
        adjusted_subtitles.append(adjusted_subtitle)

    return adjusted_subtitles

def time_to_seconds_with_ms(time_str):
    parts = re.split(r'[:,]', time_str)
    
    # Handle variations in timestamp format
    if len(parts) == 4:
        h = int(parts[0])
        m = int(parts[1])
        s = int(parts[2])
        ms = int(parts[3])
    elif len(parts) == 3:
        h = int(parts[0])
        m = int(parts[1])
        s_and_ms = parts[2].split('.')
        s = int(s_and_ms[0])
        ms = int(s_and_ms[1])
    else:
        raise ValueError(f"Invalid timestamp format: {time_str}")
    
    return h * 3600 + m * 60 + s + ms / 1000

def seconds_to_time_with_ms(seconds):
    h = int(seconds) // 3600
    m = (int(seconds) % 3600) // 60
    s = int(seconds) % 60
    ms = int((seconds - int(seconds)) * 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


# Specify the path to your subtitle file
srt_file_path = '/Users/jordanjones/Library/Mobile Documents/3L68KQB4HG~com~readdle~CommonDocuments/Documents/Anime/AJATT Shows/Crayon Shin-Chan/Show/2.srt'

# Parse the subtitle file
subtitles = parse_srt_file(srt_file_path)

# Adjust the timing by 46 seconds (or your desired value)
adjusted_subtitles = adjust_timing(subtitles, 45)

# Specify the path for the new adjusted subtitle file
adjusted_srt_file_path = '/Users/jordanjones/Library/Mobile Documents/3L68KQB4HG~com~readdle~CommonDocuments/Documents/Anime/AJATT Shows/Crayon Shin-Chan/Show/2 copy.srt'

# Write the adjusted subtitles to the new .srt file
with open(adjusted_srt_file_path, 'w', encoding='utf-8') as file:
    for subtitle in adjusted_subtitles:
        file.write(str(subtitle['index']) + '\n')
        file.write(subtitle['start_time'] + ' --> ' + subtitle['end_time'] + '\n')
        file.write(subtitle['text'] + '\n\n')
