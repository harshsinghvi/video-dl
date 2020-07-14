from concurrent.futures import ProcessPoolExecutor
from pathlib import Path as p
from os import cpu_count
import ffmpeg

class FFConcat:

    def __init__(self, path, check_files=False):

        self.check_files = check_files
        self.path = p(path)
        self.cores = cpu_count()
        self.batches = []

    def file_check(self):
        '''
        Optional:
        Iterates over folders in path, renames with leading zero for sorting if missing.
        '''
        for folder in sorted(self.path.iterdir()):
            # Folder names were originally "Folder Name - [Disk 1]"
            disk_number = folder.stem.split()[-1].strip(']')
            if len(disk_number) == 1:
                folder.rename('{}/Folder Name - Disk 0{}'.format(self.path, disk_number))
            elif len(disk_number) == 2:
                folder.rename('{}/Folder Name - Disk {}'.format(self.path, disk_number))

    def file_batch(self):
        '''
        Iterates over folders in path creating a list. Converts list into string format
        which is combined with resulting output filename in a dict and added to
        batch list.
        '''
        print('Batching audio files by folder.')
        for folder in sorted(self.path.iterdir()):
            # Use folder names as concat output name for final file.
            outfile = (self.path/'{}.mp3'.format(folder.stem)).as_posix()
            tracks = []
            # Create a list of sorted tracks in folder.
            for track in sorted(folder.iterdir()):
                tracks.append(track.as_posix())
            print('Located {} audio files in \"{}\"'.format(len(tracks), folder.stem))
            # Format file list in string format which ffmpeg will accept via input.
            file_list = '|'.join(_ for _ in tracks)
            # Generate list of dictionaries containing the file list and output filemame
            self.batches.append({
                                'file_list': file_list,
                                'outfile': outfile
                                })

    def combine_audio(self, batch):
        '''
        Input: single dictionary containing a string formatted file list for each folder
        and output filename. Converts list into ffmpeg input concat object. Runs object
        with audio codec copy concatenating files within folder into single file.
        '''
        print('Starting concat for: {}'.format(batch['outfile']))
        tracks = ffmpeg.input('concat:{}'.format(batch['file_list']))
        tracks.output(batch['outfile'], acodec='copy').run()
        print('Completed concat for: {}'.format(batch['outfile']))

    def mp(self, function, iterable):
        '''
        Input: combine_audio function and batch list.
        Sets max workers depending on iterable length and core count.
        '''
        if len(iterable) >= self.cores:
            workers = self.cores
        elif len(iterable) < self.cores:
            workers = len(iterable)
        with ProcessPoolExecutor(max_workers=workers) as p:
            p.map(function, iterable)

    def run(self):

        if self.check_files:
            self.file_check()

        self.file_batch()

        if len(self.batches) == 1:
            print('One batch found. Sending directly to concatenator.')
            self.combine_audio(self.batches[0])
        elif len(self.batches) > 1:
            print('Sending {} batches to multi-processing.'.format(len(self.batches)))
            self.mp(self.combine_audio, self.batches)

concat = FFConcat(path='downloads')
concat.run()