# big-little-matching
Modified implementation of stable marriage algorithm to assist in big-little matching for sororities. The script prioritizes the preferences of the littles. 

## How to Use
The script is based on the following forms used to take top 8 preferences for bigs and littles: 
* [Form for bigs](https://goo.gl/forms/abo56E0KQgYZOTFB2)
* [Form for littles](https://goo.gl/forms/CeJJjnMirwitrF1q1) 

1. Create a Google Spreadsheets for each of the forms and download each spreadsheet as a csv file. Place each of these  downloaded files in the same directory as the script. 

2. Run the script in via the command line by `python biglittle.py [littlePrefSheet].csv [bigPrefSheet].csv`

## How to Read Output 
The script creates a csv file, _preferences.csv_, which has 5 columns: 
1. `Big`: the name of the big
2. `Suggested Little`: the suggested little to match with the big 
3. `Big Rank`: the rank of the big for the little 
4. `Little Rank`: the rank of the little for the big
5. `Rematch?`: `TRUE` if the suggested match is one where the little ranked the big lower than their top 4 

If `Rematch?` equals `TRUE`, matching committee should review pair and match by hand.

The script randomly selects from the bigs who said they wanted more than one little and matches them with littles. In the `Big` column, these bigs's names are listed as `{name}2`. The preferences of littles for these 'duplicate' bigs and of the 'duplicate' bigs for the littles is accounted for. However for matches where bigs are taking more than one little, and littles are suggested as twins, the matches should be reviewed by hand. 

## Areas of Improvement 
1. The script does not optimize when assigning bigs who will take multiple littles -- these bigs are assigned randomly out of the bigs who say the prefer more than one little. Matches might be more successful if different bigs are selected to take more than one little. As such, these matches should be reviewed by hand. 
2. Because bigs and littles only list their top 8 preferences, if a little is not mutually ranked by other bigs or there are more successful matches for all the bigs on a little's list, it is possible her match will be with a big she did not list in her top 8. These matches will be flagged in the `Rematch?` column of _preferences.csv_. 

## 
This script was based on an implementation of the [stable marriage algorithm](https://gist.github.com/joyrexus/9967709). 
