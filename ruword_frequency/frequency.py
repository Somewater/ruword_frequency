import marisa_trie
from ruword_frequency.source_reader import SourceReader
import os

class Frequency(object):
    def __init__(self):
        self._max_ipm = None
        self.tree = None

    def load(self):
        filepath_tree = os.path.join(os.path.dirname(__file__), 'data', 'frequency_tree.bin')
        if not os.path.exists(filepath_tree):
            SourceReader().download_data_file('frequency_tree.bin')
        self.tree = marisa_trie.RecordTrie('<f')
        self.tree.load(filepath_tree)

    def ipm(self, word):
        if self.tree is None:
            print("Frequency loading...")
            self.load()
        text = word.lower().replace('ё', 'е') # 'ё' is not supported in some sources
        if text in self.tree:
            return self.tree[text][0][0]
        else:
            return 0.0

    def max_ipm(self):
        if self._max_ipm is None:
            self._max_ipm = 0
            for _, (ipm, ) in self.tree.iteritems():
                if self._max_ipm < ipm:
                    self._max_ipm = ipm
        return self._max_ipm

    def iterate_words(self, min_ipm=0.01):
        for w, (ipm, ) in self.tree.iteritems():
            if ipm >= min_ipm:
                yield w, ipm
