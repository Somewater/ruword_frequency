import os
from typing import Dict
from collections import Counter, defaultdict
import marisa_trie

class SourceReader:
    def build_tree_from_dictionaries(self):
        wc_lists = defaultdict(list)
        for need_lemmatization, generator, source_name in [(False, self.read_freq_2011, '2011'),
                                                           (False, self.read_freq_hagen, 'hagen'),
                                                           (True, self.read_freq_litc_win, 'litc_win'),
                                                           (False, self.read_freq_wikipedia, 'wikipedia'),
                                                           (True, self.read_freq_flibusta, 'flibusta'),
                                                           (True, self.read_freq_puhlyi, 'puhlyi')]:
            print('read %s' % source_name)
            wc = generator()

            wc2 = Counter()
            for w, ipm in wc.items():
                wc2[w.lower()] += ipm
            wc = wc2

            del wc2
            for w, ipm in wc.items():
                wc_lists[w].append(ipm)
        wc = dict()
        for w, cs in wc_lists.items():
            wc[w] = sum(cs) / len(cs)
        return marisa_trie.RecordTrie('<f', [(w, (ipm,)) for w, ipm in wc.items()])

    def load_word_count(self, filepath: str = 'data/word_count_union.csv') -> Dict[str, int]:
        wc = dict()
        with open(filepath) as file:
            for line in file:
                cnt = int(line[:10])
                text = line[11:].strip()
                wc[text] = cnt
        return wc

        # http://speakrus.ru/dict/index.htm
    def read_freq_hagen(self) -> Dict[str, float]:
        wc = dict()
        with open(os.path.join('data', 'freq', 'hagen_freq_alph.txt'), encoding='windows-1251') as f:
            for line in f:
                r = line.split(' | ')
                wc[r[1]] = float(r[3])
        return wc

        # http://dict.ruslang.ru/freq.php
    def read_freq_2011(self) -> Dict[str, float]:
        wc = dict()
        header_readed = False
        with open(os.path.join('data', 'freq', 'freqrnc2011.csv')) as f:
            for line in f:
                if header_readed:
                    r = line.split('\t')
                    wc[r[0]] = float(r[2])
                else:
                    header_readed = True
        return wc

        # http://speakrus.ru/dict/index.htm
    def read_freq_litc_win(self) -> Dict[str, float]:
        words_all = 2.390000
        wc = dict()
        with open(os.path.join('data', 'freq', 'litc-win.txt'), encoding='windows-1251') as f:
            for line in f:
                r = line.split(' | ')
                wc[line[8:]] = int(line[:7]) / words_all
        return wc

    def read_freq_wikipedia(self) -> Dict[str, float]:
        return self._read_word_count(os.path.join('data', 'freq', 'wikipedia_freq.txt'), 17118.429422, 100)

    def read_freq_flibusta(self) -> Dict[str, float]:
        return self._read_word_count(os.path.join('data', 'freq', 'word_frequency_flibusta_0.txt'))

    def read_freq_puhlyi(self) -> Dict[str, float]:
        return self._read_word_count(os.path.join('data', 'freq', 'word_frequency_by_puhlyi.txt'))

    def _read_word_count(self, filepath: str, words_all: float = None, min_count: int = 5):
        if words_all is None:
            words_all = 0
            with open(filepath) as f:
                for line in f:
                    cnt = int(line[:10])
                    words_all += cnt
            words_all = words_all / 1000000
        wc0 = Counter()
        with open(filepath) as f:
            for line in f:
                cnt = int(line[:10])
                text = line[11:].strip().lower()
                wc0[text] += cnt
        wc = dict()
        skipped = 0
        for w,c in wc0.items():
            if c >= min_count:
                wc[w] = c / words_all
            else:
                skipped += 1
        print('Skipped %d words (%.2f %%) by min_count=%d' % (skipped, 100 * skipped / len(wc0), min_count))
        return wc