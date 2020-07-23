# %%
import os


# %%


class FileManager():
    def __init__(self, root):
        self.root = root
        self.paths = []

    def append(self, path):
        assert(os.path.isfile(path))

        if os.path.basename(path).startswith('~'):
            return

        if any([path.endswith('.docx'),
                path.endswith('.docx')]):
            self.paths.append(path)

    def walker(self, root=None):
        if root is None:
            root = self.root

        try:
            for node in os.listdir(root):
                if os.path.isfile(os.path.join(root, node)):
                    self.append(os.path.join(root, node))

                if os.path.isdir(os.path.join(root, node)):
                    self.walker(root=os.path.join(root, node))
        except PermissionError:
            pass

    def display(self):
        print('-' * 80)
        for j, path in enumerate(self.paths):
            print(j, path)
        print('')


# %%
if __name__ == '__main__':
    manager = FileManager()
    manager.walker()
    manager.display()

# %%
