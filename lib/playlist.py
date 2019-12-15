#!/usr/bin/python3
import os
import shutil
import re


class Playlist(object):
    def __init__(self, title=""):
        self.title = title
        self.song_list = []
        self.__metadata_regex_strings = {
            "title": r"^#PLAYLIST:\s(.*)$"
        }

    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, new_title):
        if isinstance(new_title, str):
            self.__title = new_title
        else:
            raise ValueError

    # m3u format: https://en.wikipedia.org/wiki/M3U
    def export(self, filepath, filename, overwrite=False, force_title=None, skip_all_songs_playlist=False, write_playlist_only=False):
        if not os.path.isdir(filepath):
            # invalid filepath given
            print(f"Error: Could not find path {filepath}")
            raise FileNotFoundError
        
        music_dir = os.path.join(filepath, "Music")
        playlist_dir = os.path.join(filepath, "Playlists")
        playlist_path = os.path.join(playlist_dir, filename)

        if not write_playlist_only:
            # make dirs if they don't exist yet
            if not os.path.isdir(music_dir):
                os.mkdir(music_dir)
            if not os.path.isdir(playlist_dir):
                os.mkdir(playlist_dir)

            # check if file exists already in playlists
            if os.path.isfile(playlist_path) and overwrite == False:
                # error because file already exists
                print("Error: Playlist already exists.")
                raise FileExistsError

            # copy music to music directory on flash drive
            for song in self.song_list:
                try:
                    shutil.copyfile(song, os.path.join(music_dir, os.path.basename(song)))
                except shutil.SameFileError:
                    print("File already exists, skipping")
                except IsADirectoryError:
                    print("Destination is a directory.")
                except PermissionError:
                    print(f"Error: Permission Denied. Unable to copy {song} to {music_dir}")
                except:
                    print("Error occurred while copying file.")
        else:  # write_playlist_only is True
            playlist_path = os.path.join(filepath, filename)

        # write data to a playlist file using the M3U format
        try:
            with open(playlist_path, "w") as playlist:
                # extended M3U header
                playlist.write("#EXTM3U\n")

                # write gloabal metadata
                if self.title != '' or force_title is not None:
                    playlist.write(f"#PLAYLIST: {self.title if self.title != '' else force_title}\n")

                # copy songs to playlist file
                for song in self.song_list:
                    # TODO: write song metadata?
                    playlist.write(f"../Music/{os.path.basename(song)}\n")

            if not skip_all_songs_playlist:
                # update the list of playlists in the Playlist directory
                all_playlists = [x for x in os.listdir(playlist_dir) if x[-4:] == ".m3u"]
                with open(os.path.join(playlist_dir, "__playlists.txt"), 'w') as list_file:
                    list_file.writelines(sorted([x + '\n' for x in all_playlists], key=str.casefold))
                    

                self.create_all_songs_playlist(music_dir)

        except PermissionError:
            print(f"Error: Permission Denied. Unable to write playlist at {playlist_path}")

    def import_existing(self, filepath):
        print(f"IMPORTING {filepath}")
        if not os.path.isfile(filepath):
            # invalid filepath given
            print(f"Error: Could not find file {filepath}")
            raise FileNotFoundError

        song_list = list()
        title = ""

        try:
            with open(filepath, "r") as playlist:
                # extended M3U header
                for line in playlist.readlines():
                    if line[0] == "#":
                        # comment in m3u file, extract metadata if possible
                        comment_data = self.__parse_comment(line)
                        if "title" in comment_data:
                            title = comment_data["title"]
                    else:
                        # path to a song, try to find it
                        translated_dir = os.path.normpath(os.path.join(os.path.dirname(filepath), "..", "Music"))
                        translated_dir += (os.path.sep)
                        print(filepath)
                        print(translated_dir)
                        # replace the VSOS path ("D:Music/") with the system's path to the actual files
                        line = line.replace("D:Music/", translated_dir, 1)
                        line = line.replace("../Music/", translated_dir, 1)
                        line = line.strip()  # strip the trailing newline

                        if not os.path.isfile(line):
                            print(f"Error: Unable to find song {line}. Skipping...")
                        else:
                            song_list.append(line)

        except PermissionError:
            print(f"Error: Permission Denied. Unable to read playlist at {filepath}")
        finally:
            self.title = title
            self.song_list = song_list

    @staticmethod
    def create_all_songs_playlist(music_dir):
        all_songs_playlist = Playlist(title="All Music")
        all_songs_playlist.song_list.extend(x for x in os.listdir(music_dir) if x[-4:] == ".mp3")
        all_songs_playlist.song_list.sort(key=str.casefold)
        all_songs_playlist.export(music_dir, "__all_songs.m3u", skip_all_songs_playlist=True, write_playlist_only=True)

    def __parse_comment(self, comment_string):
        data = dict()
        for value_name, regex in self.__metadata_regex_strings.items():
            match = re.match(regex, comment_string)
            if match:
                data[value_name] = match[1]
                break
        return data

    def __str__(self):
        lines = list()
        if self.title:
            lines.append(f'Playlist "{self.title}"\n')
        else:
            lines.append("Untitled Playlist\n")
        if self.song_list:
            lines.append("Songs:\n")
            for i, song in enumerate(self.song_list):
                lines.append(f"   {str(i+1) + '.':<4} {os.path.basename(song)}\n")
        else:
            lines.append("No songs added.\n")

        return ''.join(lines)


# test code
if __name__ == "__main__":
    my_playlist = Playlist(title="My Playlist")
    # add music
    my_playlist.song_list.append("/Users/david/Music/Music/Aerosmith Dream On Lyrics.mp3")
    my_playlist.song_list.append("/Users/david/Music/Music/Jeff Buckley - Hallelujah.mp3")
    my_playlist.song_list.append("/Users/david/Music/Music/Blue Oyster Cult.mp3")
    my_playlist.song_list.append("/Users/david/Music/Music/Louis Armstrong - What a Wonderful World.mp3")
    my_playlist.song_list.append("/Users/david/Music/Music/Coldplay - The Scientist.mp3")
    my_playlist.song_list.append("/Users/david/Music/Music/Matchbox 20 - Bent.mp3")
    my_playlist.song_list.append("/Users/david/Music/Music/Counting Crows - Mr. Jones.mp3")
    my_playlist.song_list.append("/Users/david/Music/Music/Creedence Clearwater Revival - Have You Ever Seen the Rain_.mp3")
    my_playlist.song_list.append("/Users/david/Music/Music/Tom Petty & the Heartbreakers - Mary Jane's Last Dance.mp3")
    my_playlist.song_list.append("/Users/david/Music/Music/Earth ,Wind & Fire - September.mp3")
    my_playlist.song_list.append("/Users/david/Music/Music/U2 - New Year's Day.mp3")
    my_playlist.song_list.append("/Users/david/Music/Music/Elton John - Daniel.mp3")
    my_playlist.song_list.append("/Users/david/Music/Music/Will Smith - Gettin' Jiggy Wit It.mp3")
    my_playlist.song_list.append("/Users/david/Music/Music/Hootie & the Blowfish - Let Her Cry.mp3")
    # Export playlist
    my_playlist.export("/Volumes/FLASH DRIVE", "My_Playlist.m3u", overwrite=True)
    print(my_playlist)

    print("Importing playlist...")
    imported = Playlist()
    imported.import_existing("/Volumes/FLASH DRIVE/Playlists/My_Playlist.m3u")
    print(imported)
