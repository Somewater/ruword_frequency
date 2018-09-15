# Description 
Python library `ruword_frequency` returns frequency (ipm - items per million) of russian words, case insensitive.
It based on huge collection of russian documents and prepared word frequency sources. Full list:
- [Wikipedia dump, russian segment](https://dumps.wikimedia.org/ruwiki/latest)
- [Flibusta dump](https://rutracker.org/forum/viewtopic.php?t=5385741), more then 200 Gb of texts
- [Pyhlyi's library](https://rutracker.org/forum/viewtopic.php?t=1874223)
- [Новый частотный словарь русской лексики](http://dict.ruslang.ru/freq.php)
- [Словарь русской литературы](http://www.artint.ru/projects/frqlist.php) from http://speakrus.ru/dict/index.htm
- [Частотный словарь Марка фон Хагена](http://speakrus.ru/dict/index.htm) see [description](http://speakrus.ru/dict/hagen_freq_desc.txt)

Word's ipm from all enumerated sources was extracted and mean values used. 
Full index contains more them 7 billions word forms including mistakes from raw data sources (unfortunately).

# Requirements:
- Python 3
- Word index occupies near 50 Mb on hard disk and will be downloaded first time you invoke `frequency.load()` method

# Installation
```
pip install ruword_frequency
```

# Usage
```
from ruword_frequency import Frequency
freq = Frequency()
freq.load()

freq.ipm('привет')
>>> 53.51823806762695

freq.ipm('неттакогослова')
>>> 0.0

# get max ipm value. For weights normalization, for example
freq.max_ipm()
>>> 42329.2890625

# get list of most used words  with ipm more then 10000
for w in freq.iterate_words(10000):
    print(w)
```

For other useful methods see [marisa-trie](https://marisa-trie.readthedocs.io/en/latest/tutorial.html) documentations.
Tree index available as `freq.tree`

# Rebuild tree by yourself
```
from ruword_frequency.source_reader import SourceReader
reader = SourceReader()

# increase socket timeout, sometimes helpful for huge file downloading:
import socket
socket.setdefaulttimeout(60)

reader.download_all_sources()
tree = reader.build_tree_from_dictionaries()
reader.save_tree(tree)

# use it 
freq = Frequency()
freq.ipm('привет')
```