# coding=utf-8
from __future__ import absolute_import, unicode_literals

import unittest

from nltk.corpus import WordNetCorpusReader
from pkg_resources import resource_filename


class TestWordNet(unittest.TestCase):
    def setUp(self):
        self.wncr = WordNetCorpusReader(resource_filename('clasificador.recursos', 'wordnet_spa'), None)

    # Habría que actualizar el offset ya que cambió y el test deja de servir.
    # def test_invalid_literal_for_int_16(self):
    #     self.wncr._synset_from_pos_and_line('n',
    #                                         "04122387 00 n 0a agudeza 0 broma 0 chiste 0 chufleta 0 comentario_burlón 0 cuchufleta 0 idea 0 ocurrencia 0 pulla 0 salida 0 04 @ 04120601 n 0000 + 00620096 v 0000 + 00499330 v 0000 + 00558467 v 0000 | comentario ingenioso para hacer reír  \n")

    def test_key_error(self):
        self.wncr.lemma("menor.a.09.menor").antonyms()


if __name__ == '__main__':
    unittest.main()
