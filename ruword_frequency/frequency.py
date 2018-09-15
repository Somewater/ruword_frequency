import marisa_trie
from ruword_frequency.source_reader import SourceReader


class Frequency(object):
    def __init__(self):
        self.word_count = None
        self._max_ipm = None
        self.filepath_tree = 'data/frequency_tree_lemms.bin'
        self.tree = None

    def load(self):
        self.tree = marisa_trie.RecordTrie('<f')
        self.tree.load(self.filepath_tree)

    def save(self):
        if self.tree is None:
            raise RuntimeError("Dictionaries not loaded yet")
        self.tree.save(self.filepath_tree)

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
