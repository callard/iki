# Default Filetype support #

Several media format exists in the computer world, and several for each type of media (sound : mp3, vorbis, .., .. ; videos : mpeg{1.4..}, theora). We have to make a choice of the default filetype we support. Basically, it should be simpler to support Open Format over Proprietary format, so here is a list of the format we should support :

  * Container
    * Ogg - http://xiph.org/
  * Audio
    * Vorbis - http://www.vorbis.com/ - lossy
    * Flac - http://flac.sourceforge.net/ - lossless
  * Video
    * Theora - http://www.theora.org/
  * Images
    * PNG - http://en.wikipedia.org/wiki/PNG
    * JPEG - http://en.wikipedia.org/wiki/JPEG
    * DNG - http://www.adobe.com/products/dng/ - raw
  * Miscellaneous
    * XSPF - http://www.xspf.org/ - playlist
    * M3U - http://en.wikipedia.org/wiki/M3U - playlist
    * PLS - http://en.wikipedia.org/wiki/PLS_(file_format) - playlist

This list is what **iki** should handle by default, but it's not the case for the moment.

Anyway, other media format could be support, with extension. The _filetype support system_ will be extensible, and it should be easy to add any type of filetype to the default ones.