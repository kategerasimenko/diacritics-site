# diacritics-site
<p>This repository stores all necessary data and scripts for diacitics restoration site.</p>
<p>The code is written in Python.</p>
<p>Contact information: Ekaterina Gerasimenko, katgerasimenko@gmail.com</p>

### GET JSONS
In the folder "get jsons" you can find a code that creates files with probabilities necessary for further work. 
There are two scripts there: get_jsons and get_bigrams.
For each script there should be an input file and both scripts require a .csv file with alphabets.

#### Alphabets (alphs.csv):
There are four cells. The first one is alphsbet with special letters and the second one is alphabet without spectial letters but wuth their equivalents. There should be one-to-one correspondence and, therefore, these two alphabets should have equal length. The third and the forth cells are special letters and their equivalents.

#### get_jsons.py:
Input is a .txt file in UTF-8 encoding. Its name should be 'input_new.txt' or you can change it in the code. It should contain words with correctly used special symbols without punctuation marks and capitalization separated by '##'. For example:
<br/>*\#\#my##name##is##kate##i##love##coding*

#### get_bigrams.py:
Input is a .txt file in UTF-8 encoding. Its name should be 'output_sent.txt' or you can change it in the code. It should contain sentences with correctly used special symbols in words. For example:
<br/>*My name is Kate. I love coding.*

<br/>If you want to add a new language and collect probabilities, you should create a folder and put alphabets and input files in it. Then you should change "for lang in langs:" in code to "for lang in ['your_folder_name']:".


### SITE
If you want to use the site, you should first install pickle module. Install pip if it is absent, open the command line and type:
<br/>**pip install flask**
<br/>Then you should change direcrory in the command line to the one where files and folders from folder 'site' in this repository are stored.
Then type:
<br/>**python run.py**
<br/>Then open in your browser 127.0.0.1:5000
<br/>The page should work :)

If you want to add languages, you should first collect probabilities (described earlier), then create a folder in "app" named as a language you want to add. The new folder should contain alphs.csv, trans_3.json, start_3.json, freqlist.json, bigram_freqlist.json. Then you should change a form in html template. Go to app\static\templates, open 'index.html' and in the part where select element is (it begins with <select name="selectlang" id="lang">), add
\<option>New_language\</option>. New_language should match exactly with the folder name that you have created. 
