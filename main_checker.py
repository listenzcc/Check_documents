# %%
import os
import time
import threading

from local_tools import FileManager, Recorder, get_text
from local_profile import FOLDER, WORDS

# %%

# Init file manager
manager = FileManager(root=FOLDER)
manager.walker()
manager.display()


# %%
class Pool():
    def __init__(self, num_max=0):
        self.threads = []
        self.num_max = num_max

    def append(self, thread):
        self.threads.append(thread)

    def report(self):
        s = [t.is_alive() for t in self.threads]
        num_threads = len(self.threads)
        num_alive = s.count(True)
        return f'| {num_alive} | {num_threads} | {self.num_max} |'

    def is_done(self):
        return not any(t.is_alive() for t in self.threads)


pool = Pool(num_max=len(manager.paths))


def check_suspect(path, recorder, j=0):
    t = time.time()
    # print(f'Checking {j} {path}')
    try:
        text = get_text(path)
    except:
        return 1

    for word in recorder.words:
        if word in text:
            j = text.index(word)
            surrounding = text[j-20: j+20]
            recorder.append(dict(Name=os.path.basename(path),
                                 Offence=word,
                                 Folder=os.path.dirname(path),
                                 Surrounding=surrounding))

    print(f'')
    d = time.time() - t
    print(f'{pool.report()}, Done {j}, {path}, {d} seconds passed.')


# %%
if __name__ == '__main__':
    print('Hi there.')
    while True:
        mode = input(
            'Choose a mode, [c] for autocheck mode, others for interface mode:\n')
        if mode == 'c':
            MODE = 'Check'
        else:
            MODE = 'Interface'
        break

    if MODE == 'Check':
        # Check files in file manager,
        # the wrong files will be recorded.

        # Init recorder
        recorder = Recorder(words=WORDS)

        # Check files using multi-threads
        for j, path in enumerate(manager.paths):
            # print(j, path)
            t = threading.Thread(target=check_suspect,
                                 args=(path, recorder, j))
            t.start()
            # t.run()
            pool.append(t)

        # Wait threads to finish
        while True:
            if pool.is_done():
                break
            time.sleep(1)
        # for t in threads:
        #     t.join()

        # Display
        recorder.display()

        # Save
        recorder.save(browser=True)

    if MODE == 'Interface':
        # Interface mode,
        # select idx of the file,
        # the contents will be printed
        while True:
            print(f'File idx from 0 to {len(manager.paths)}')
            inp = input('>> ')

            # Enter 'q' to escape
            if inp == 'q':
                break

            if inp == 'l':
                manager.display()

            # Legal check for input,
            # convert it into int if it is legal
            try:
                idx = int(inp)
            except ValueError:
                print(f'Wrong input: {inp}')
                continue

            # Get path
            path = manager.paths[idx]

            # Print contents
            print(f'-- {path} --')
            print(get_text(path))
            print(f'-- {path} --')
            print('')

    # Stop,
    # have a good luck
    print('Bye Bye')
