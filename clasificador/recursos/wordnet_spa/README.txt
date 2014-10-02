MCR WordNet 3.0 database files. To be read by the NTLK WordNet reader.

These files were created from the Multilingual Central Repository 3.0.
The latest Spanish MCR 3.0 files can be downloaded from
http://adimen.si.ehu.es/web/MCR/
The latest version of the transformation process can be found in
https://github.com/pln-fing-udelar/wn-mcr-transform

For more details on the MCR 3.0 contents, including references to the
original resources, please consult the following paper:
  Gonzalez-Agirre A., Laparra E. and Rigau G. Multilingual Central
  Repository version 3.0: upgrading a very large lexical knowledge
  base. In Proceedings of the Sixth International Global WordNet
  Conference (GWC'12). Matsue, Japan. January, 2012.
which can be downloaded at:
http://adimen.si.ehu.es/~rigau/publications/gwc12-glr.pdf

The contents of the MCR package are distributed under different open licenses.
If you want to redistribute this software, part of it, or derived works based
on it or on any of its parts, make sure you are doing so under the terms stated
in the license applying to each of the involved modules.
The licenses applying to the modules contained in MCR are the following:
 - English WordNet synset and relation data, contained in folder engWN/ are
     distributed under the original WordNet license. You can find it at
     http://wordnet.princeton.edu/wordnet/license
 - Basque WordNet synset and relation data, contained in folder eusWN/ are
     distributed under CreativeCommons Attribution-NonCommercial-ShareAlike 3.0
     Unported (CC BY-NC-SA 3.0) license. You can find it at
     http://creativecommons.org/licenses/by-nc-sa/3.0
 - All other data in MCR package are distributed under Attribution 3.0 Unported
     (CC BY 3.0) license. You can find it at
     http://creativecommons.org/licenses/by/3.0/

=================================================
Usage:
1 - Extract the files into a folder.
2 - From a Python shell, import the NLTK library.
    >> import nltk
3 - Create a WordNet reader.
    >> wn = nltk.corpus.reader.wordnet.WordNetCorpusReader(<path to the extracted files>)

Now you can use the object wn to query the contents of MCR WordNet 3.0, for example in Spanish:
    >> print wn.synset("entidad.n.01").definition
