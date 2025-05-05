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
            performers = row["Perfomer"].split(" | ")
            songs[song] = performers
    return songs


def convert_time_to_milliseconds(time_str):
    return float(time_str) * 1000


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

    labels_path = "show-info/label.csv"
    labels = read_labels(labels_path)

    performers_path = "show-info/performers.csv"
    cast = read_performers(performers_path)

    songs_path = "show-info/songs.csv"
    songs = read_songs(songs_path)

    for i, row in enumerate(labels):
        start_time_ms = convert_time_to_milliseconds(row["Start"])
        end_time_ms = convert_time_to_milliseconds(row["End"])
        label = row["Song"]
        performers = songs.get(label, [])
        artist = ", ".join([cast.get(character, "Unknown") for character in performers])
        segment = audio[start_time_ms:end_time_ms]
        export_segment(segment, output_dir, i, label, artist)


if __name__ == "__main__":
    main()
