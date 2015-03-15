srtmerge
========

Merge and clean up multi-line and multi-language subtitle files.

<br><b>Purpose</b>

Some closed caption subtitle files contain multiple lines of subtitle in a single subtitle timing block.

This script merges multiple lines into a single line. If Non-English translation lines are also present, they will be seperately merged into another line, on top of the English line.

We use Chinese as the intended translated language. This script may not apply to some languages with the same charset to English.<br><br>

<b>Usage</b>
<h5>To merge a subtitle file containing multiple lines of English and/or translated lines:</h5>
<pre>
python merge.py /path/to/original/subtitle.srt /path/to/output/subtitle.srt
</pre>
<h5>To split a subtitle file containing multiple lines of English and/or translated lines, into two separate subtitle files -- one for English, and one for translated:</h5>
<pre>
python split.py /path/to/original/subtitle.srt /path/to/output/subtitle
</pre>
Note that <b>/path/to/output/subtitle.en.srt</b> and <b>/path/to/output/subtitle.ch.srt</b> will be created.<br><br>

<b>用途</b>

<b>merge.py</b> 将带有多行英文的SRT字幕合并成单行。如果同时有中文翻译行，中文翻译单独合并成单行，并置于对应的英文行上方。
<b>split.py</b> 将带有多行英文的SRT字幕合并成单行。如果同时有中文翻译行，中文翻译单独合并成单行放进一个文件，英文行放在另外一个文件里。<br>

用法如上方。</b><br><br>

<b>License</b><br>
Copyright (c) sundaymouse 2014<br>
License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.<br>
For full license details, see: http://www.gnu.org/copyleft/gpl.html<br>
