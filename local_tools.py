import os
import sys
import docx
import webbrowser
import pandas as pd

from pprint import pprint

from io import StringIO
from io import open
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, process_pdf

import PyPDF2


def read_pdf(pdf):
    # Read contents of [pdf]

    # Resource manager
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    laparams = LAParams()

    # Device
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)
    process_pdf(rsrcmgr, device, pdf)
    device.close()
    content = retstr.getvalue()
    retstr.close()

    # Require all lines
    lines = str(content).split("\n")

    # Return
    return '\n'.join(lines)


def get_text(path):
    # Get text from path

    # Get text of .docx file
    if path.endswith('.docx'):
        texts = []

        doc = docx.Document(path)
        all_paras = doc.paragraphs
        for para in all_paras:
            texts.append(para.text)

        return '\n'.join(texts)

    # Get text of .pdf file
    if path.endswith('.pdf'):
        texts = []

        with open(path, 'rb') as f:
            return read_pdf(f)
            pdf_reader = PyPDF2.PdfFileReader(f)
            for j in range(pdf_reader.numPages):
                page = pdf_reader.getPage(j)
                texts.append(page.extractText())

        return '\n'.join(texts)

    # Get nothing
    return ''


class Recorder():
    def __init__(self, words):
        self.suspects = pd.DataFrame(columns=['Name',
                                              'Offence',
                                              'Surrounding',
                                              'Folder'])

        self.words = words
        self.fname = 'suspect'

    def append(self, dct):
        series = pd.Series(dct)
        self.suspects = self.suspects.append(series,
                                             ignore_index=True)
        pass

    def display(self):
        print('--------------------')
        pprint(self.suspects)

    def save(self, name='suspects', browser=False):
        self.suspects.to_json(f'{name}.json')
        self.suspects.to_html(f'{name}.html')
        if browser:
            webbrowser.open(f'{name}.html')


class FileManager():
    """FileManager

    Find all .docx files in root recursively.
    """

    def __init__(self, root, exts=['.docx', '.pdf']):
        self.root = root
        self.exts = exts
        self.paths = []

    def append(self, path):
        # Append new [path] to paths
        # path: full path of the .docx file

        # Path should be a file
        assert(os.path.isfile(path))

        # Ignore temporal file
        if os.path.basename(path).startswith('~'):
            return

        # Record legal .docx file
        if any([path.endswith(ext) for ext in self.exts]):
            self.paths.append(path)

    def walker(self, root=None):
        # Walk through [root] recursively

        # Start with self.root
        if root is None:
            root = self.root

        # Use try wrapper to deal with PermissionError
        try:
            for node in os.listdir(root):
                # If meet a file, try to append it
                if os.path.isfile(os.path.join(root, node)):
                    self.append(os.path.join(root, node))

                # if meet a folder, dig in
                if os.path.isdir(os.path.join(root, node)):
                    self.walker(root=os.path.join(root, node))
        except PermissionError:
            pass

    def display(self):
        # Display recorded paths
        print('-' * 80)
        for j, path in enumerate(self.paths):
            print(j, path)
        print('')


if __name__ == '__main__':
    manager = FileManager()
    manager.walker()
    manager.display()

# %%
