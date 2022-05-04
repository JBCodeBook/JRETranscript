import os.path
import regex
import tkinter as tk
from tkinter import filedialog as fd
"""
This script will take a text document that is produced by Words audio transcription service and format it. 
It will find the speaker names and squash consecutive lines where the speaker is the same down into a single paragraph.
It will remove the timestamps in each line, if certain times are needed to be left in the document 
then the replace_timestampe method can be used
"""

def processFile(oldFile, newFile):
    """
    If the new file does not exist, create this file else print that the file already
    exists and nothing needs to be done

    :param oldFile: original text document that needs formating
    :param newFile: the new file that will be created and writen to
    """
    if not os.path.exists(newFile):
        print("Creating file: " + newFile)
        with open(newFile, 'w') as outfile, open(oldFile, 'r', encoding='utf-8') as infile:
            for line in infile:
                outfile.write(line)
    else:
        print("File Already exists")


def replace_timestamp(matchobj):
    """
    helper function that keep any times that are in "times" list

    :param matchobj: Is used to compare to the timestamps in times to select which timestamps to remove
    :return: returns empty line if timestamp not found. If found returns the timestamp to be included in document
    """

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
    # Used to locate the file name of text document using file explorer
    filename = fd.askopenfilename()

    # Store the names of each speaker in the document
    speaker_set = set()
    speaker_list = []

    remove_timestamp = regex.compile("(?<=\d\d:\d\d:\d\d(\s))(.*)" + "\s{0,2}")

    # Remove the timestamps in the document and find all speakers
    with open(filename, 'r') as input_file:
        x = input_file.readlines()

        for line in x:
            if regex.search(remove_timestamp, line):
                speaker_set.add(regex.search(remove_timestamp, line)[0])

        for speaker in speaker_set:
            speaker_list.append(speaker.strip("\n"))

    # Formats the document using regex
    pattern_remove_newline = regex.compile("\n\n")
    pattern_non_character_line_endings = regex.compile("(?<=\?\s{0,1})\n", regex.MULTILINE)
    pattern_start_p_tag = regex.compile("(?=^[A-Z])", regex.MULTILINE)
    pattern_end_p_tag = regex.compile("\.\s{0,1}\n", regex.MULTILINE)
    pattern_final_clean_up = regex.compile("(?<=\w)\n", regex.MULTILINE)
    pattern_timestamps = regex.compile("\d\d:\d\d:\d\d ", regex.MULTILINE)

    out_file = filename + "_finished.txt"

    # Formats the document by removing timestamps and squashing consecutive speakers into single paragraph.
    # Finishes off by adding HTML to document
    with open(filename, 'r') as newfile:
        doc = newfile.read()
        edit = regex.sub(pattern_remove_newline, "\n", doc)

        # Backtrack removes the lines where the speaker is the same for consecutive lines
        for speaker in speaker_list:
            edit = regex.sub(
                f"(?<=\d\d:\d\d:\d\d(\s)({speaker}" + "\s{0,2}" + f"\n)(.*)\n)((\d\d:\d\d:\d\d)(\s)({speaker})" + "\s{0,2}\n)",
                "", edit)

        # Adds HTML tags to each speakers name to make them a header
        for speaker in speaker_list:
            edit = regex.sub(speaker, f"<h4 class=\"speaker\"> {speaker} </h4>", edit)

        # Adds HTML to the main body of text and formats it using <p> tag
        edit = regex.sub(pattern_start_p_tag, "<p class=\"body\">", edit)
        edit = regex.sub(pattern_end_p_tag, "</p>\n", edit)
        edit = regex.sub(pattern_non_character_line_endings, "</p>\n", edit)
        edit = regex.sub(pattern_final_clean_up, "</p class=\"body\">\n", edit)
        edit = regex.sub(pattern_timestamps, replace_timestamp, edit)

        # Writes the formated document to a new file with suffix "_finished.txt"
        with open(out_file, 'w') as outfile:
            for line in edit:
                outfile.write(line)
            print("Complete")


if __name__ == '__main__':
    main()
