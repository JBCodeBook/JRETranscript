import os.path
import regex
import tkinter as tk
from tkinter import filedialog as fd


def processFile(oldFile, newFile):
    if not os.path.exists(newFile):
        print("Creating file: " + newFile)
        with open(newFile, 'w') as outfile, open(oldFile, 'r', encoding='utf-8') as infile:
            for line in infile:
                outfile.write(line)
    else:
        print("File Already exists")


def replace_timestamp(matchobj):
    times = ['00:15:00', '00:30:00', '00:45:00', '01:00:00', '01:15:00''01:30:00', '01:45:00', '02:00:00',
             '02:15:00' '02:30:00', '02:45:00', ]

    if matchobj.group(0) in times:
        print(f"Found time: {matchobj.group(0)}")
        new_time = f"<p> {matchobj.group(0)} </p>"
        return new_time
    else:
        return ''


# create the root window
root = tk.Tk()
root.title('Tkinter Open File Dialog')
root.resizable(False, False)
root.geometry('300x150')


def main():
    filename = fd.askopenfilename()

    pattern2 = regex.compile("(?<=\d\d:\d\d:\d\d(\s))(.*)" + "\s{0,2}")
    speaker_set = set()
    speaker_list = []

    with open(filename, 'r') as input_file:
        x = input_file.readlines()

        for line in x:
            if regex.search(pattern2, line):
                speaker_set.add(regex.search(pattern2, line)[0])

        for speaker in speaker_set:
            speaker_list.append(speaker.strip("\n"))


    pattern_remove_newline = regex.compile("\n\n")

    pattern_non_character_line_endings = regex.compile("(?<=\?\s{0,1})\n", regex.MULTILINE)
    pattern_start_p_tag = regex.compile("(?=^[A-Z])", regex.MULTILINE)
    pattern_end_p_tag = regex.compile("\.\s{0,1}\n", regex.MULTILINE)
    pattern_final_clean_up = regex.compile("(?<=\w)\n", regex.MULTILINE)
    pattern_timestamps = regex.compile("\d\d:\d\d:\d\d ", regex.MULTILINE)


    out_file = filename + "_finished.txt"

    with open(filename, 'r') as newfile:
        doc = newfile.read()

        edit = regex.sub(pattern_remove_newline, "\n", doc)


        for speaker in speaker_list:
            edit = regex.sub(
                f"(?<=\d\d:\d\d:\d\d(\s)({speaker}" + "\s{0,2}" + f"\n)(.*)\n)((\d\d:\d\d:\d\d)(\s)({speaker})" + "\s{0,2}\n)",
                "", edit)


        for speaker in speaker_list:
            edit = regex.sub(speaker, f"<h4 class=\"speaker\"> {speaker} </h4>", edit)


        edit = regex.sub(pattern_start_p_tag, "<p class=\"body\">", edit)
        edit = regex.sub(pattern_end_p_tag, "</p>\n", edit)
        edit = regex.sub(pattern_non_character_line_endings, "</p>\n", edit)
        edit = regex.sub(pattern_final_clean_up, "</p class=\"body\">\n", edit)
        edit = regex.sub(pattern_timestamps, replace_timestamp, edit)

        with open(out_file, 'w') as outfile:
            for line in edit:
                outfile.write(line)
            print("Complete")


if __name__ == '__main__':
    main()
