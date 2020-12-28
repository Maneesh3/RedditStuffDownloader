# RedditStuffDownloader
>Download any subreddit posts/media/content - along with comments

## Requirements
* `Python 3.8`
* `Reddit account` - _with Script app activated (for API requests)_
  * fill the `config.json` file with the required configuration
* `FFmpeg` download from website- [FFmpeg](https://ffmpeg.org/), keep in parent directory _(only used for reddit video & audio combination)_

## Installation

```bash
# clone the repo
$ git clone https://github.com/Maneesh3/RedditStuffDownloader.git

# install the requirements
$ pip3 install -r requirements.txt
```

## Usage
```
usage: 
$ python Reddit-Stuff-Downloader/reddit-dwn.py 
 _____          _     _ _ _      _____ _          __  __ 
|  __ \        | |   | (_) |    / ____| |        / _|/ _|
| |__) |___  __| | __| |_| |_  | (___ | |_ _   _| |_| |_ 
|  _  // _ \/ _` |/ _` | | __|  \___ \| __| | | |  _|  _|
| | \ \  __/ (_| | (_| | | |_   ____) | |_| |_| | | | |  
|_|  \_\___|\__,_|\__,_|_|\__| |_____/ \__|\__,_|_| |_|  
 _____                      _                 _           
|  __ \                    | |               | |          
| |  | | _____      ___ __ | | ___   __ _  __| | ___ _ __ 
| |  | |/ _ \ \ /\ / / '_ \| |/ _ \ / _` |/ _` |/ _ \ '__|
| |__| | (_) \ V  V /| | | | | (_) | (_| | (_| |  __/ |   
|_____/ \___/ \_/\_/ |_| |_|_|\___/ \__,_|\__,_|\___|_|   
 
usage: reddit1.py [-h] [-l] [-f FPATH] [-c CNT] [-t TYP] [-i PID] [-u PURL]

[#] Reddit Stuff Downloader [#]

optional arguments:
  -h, --help                 show this help message and exit
  -l, --subredditList        predefined subreddits list
  -s SUBNAME, --sub SUBNAME  single subreddit; -s <sub name>
  -f FPATH, --file FPATH     text file; -f <File path>
  -c CNT, --count CNT        posts count; -c <number>
  -t TYP, --type TYP         filter type(hot,top,new); -t <type>
  -i PID, --pid PID          single Post ID; -i <PostID>
  -u PURL, --purl PURL       single Post URL; -u <PostUrl>
 
 
Each subreddit content is saved in a seperate directory 
along with posts links saved in json file
```
## TODO:
- [x] Download Reddit videos along with audio
- [x] Command line arguments   **_[currently working on]_**
- [x] Verify Windows OS support !??   **_[currently working on] Bugs listed in issues page_**
- [ ] Cannot download some URL's content, Unknown URL must be properly notified (logs)
- [x] add inputs like list of subs in txt, subreddit name input, etc.. **_[currently working on] Bugs listed in issues page_**
- [ ] Reconstruct the source code using classes and with proper documentation


Copyright (c) 2020 Maneesh
