import csv
from pydub import AudioSegment
import os


def create_output_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def load_audio(file_path, format="m4a"):
    return AudioSegment.from_file(file_path, format=format)


def read_labels(file_path):
    with open(file_path, "r") as file:
        reader = csv.DictReader(file)
        return [row for row in reader]


def read_performers(file_path):
    performers = {}
    with open(file_path, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            performers[row["Role"]] = row["Performer"]
    return performers


def read_songs(file_path):
    songs = {}
    with open(file_path, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            song = row["Song"]
            roles = row["Role"].split(" | ")
            songs[song] = roles
    return songs


def convert_time_to_milliseconds(time_str):
    return float(time_str)


def export_segment(segment, output_dir, index, label, artist, bitrate="192k"):
    segment.export(
        os.path.join(output_dir, f"{index+1}_{label}.m4a"),
        format="mp4",
        codec="aac",
        bitrate=bitrate,
        tags={
            "title": label,
            "artist": artist,
            "track": str(index + 1),
        },
    )


def main():

    output_dir = "output"
    create_output_directory(output_dir)

    input_audio_path = "input.m4a"
    audio = load_audio(input_audio_path)

    labels_path = "info/label.csv"
    labels = read_labels(labels_path)

    performers_path = "info/performers.csv"
    cast = read_performers(performers_path)

    songs_path = "info/songs.csv"
    songs = read_songs(songs_path)

    for i, row in enumerate(labels):
        start_time_ms = convert_time_to_milliseconds(row["Start"])
        end_str = row.get("End", "").strip()
        if end_str:
            end_time_ms = convert_time_to_milliseconds(end_str)
        elif i + 1 < len(labels):
            end_time_ms = convert_time_to_milliseconds(labels[i + 1]["Start"])
        else:
            end_time_ms = len(
                audio
            )  # If it's the last row and no end time, use full audio duration

        label = row["Song"]
        performers = songs.get(label, [])
        artist = ", ".join([cast.get(character, "Unknown") for character in performers])
        segment = audio[start_time_ms:end_time_ms]
        print(
            f"🎧 Segment {i+1}: '{label}' from {start_time_ms} ms to {end_time_ms} ms"
        )
        export_segment(segment, output_dir, i, label, artist)


if __name__ == "__main__":
    main()
