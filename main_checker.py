# %%
import os
import traceback
import threading
import multiprocessing
from list_files import FileManager
from win32com.client import Dispatch, DispatchEx
import docx
from shutil import rename

FOLDER = os.path.join('F:\何晖光组项目')
# FOLDER = os.path.join('F:\\')

# %%
manager = FileManager(root=FOLDER)
manager.walker()
manager.display()


# %%
# for path in manager.paths:
#     doc = word.Documents.Open(FileName=path, Encoding=encoding)

# %%

MODE = 'Check'
# MODE = 'Interface'

suspects = []

words = ['秘密']

suspects_file_name = 'suspects.txt'
with open(suspects_file_name, 'w') as f:
    f.writelines([''])


def get_text(path):
    texts = []
    doc = docx.Document(path)
    all_paras = doc.paragraphs
    for para in all_paras:
        texts.append(para.text)
    return '\n'.join(texts)


def check_suspect(path, j=0, words=words):
    print(f'Checking {j} {path}')
    text = get_text(path)

    # with open(txt_file_name, 'ab') as f:
    #     f.writelines([path.encode(), text.encode()])

    for word in words:
        if word in text:
            j = text.index(word)
            surrounding = text[j-20: j+20]
            with open(suspects_file_name, 'ab') as f:
                f.writelines(['\n-------\n'.encode(),
                              path.encode(),
                              '\n'.encode(),
                              surrounding.encode(),
                              '\n'.encode(), ])
                suspects.append((path, surrounding))


# %%
if __name__ == '__main__':
    if MODE == 'Check':
        threads = []
        for j, path in enumerate(manager.paths):
            print(j, path)
            # t = multiprocessing.Process(target=check_suspect, args=(path, j))

            t = threading.Thread(target=check_suspect, args=(path, j))
            t.start()
            threads.append(t)
            # if j > 10:
            #     break
        for t in threads:
            t.join()

        print('--------------------')
        for j, cell in enumerate(suspects):
            print(j, cell[0])
            print(cell[1])
            print()

    if MODE == 'Interface':
        while True:
            print(f'File idx from 0 to {len(manager.paths)}')
            inp = input('>> ')
            if inp == 'q':
                break

            try:
                idx = int(inp)
            except ValueError:
                print(f'Wrong input: {inp}')
                continue

            path = manager.paths[idx]

            print(f'-- {path} --')
            print(get_text(path))
            print(f'-- {path} --')
            print('')

    print('Bye Bye')
