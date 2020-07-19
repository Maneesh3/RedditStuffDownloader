# RedditStuffDownloader
>Download any subreddit posts/media/content - along with comments

## Requirements
* `Python 3.8`
* `Reddit account` - _with Script app activated (for API requests)_
  * fill the `config.json` file with the required configuration
* `FFMPEG` download from website, keep in parent directory _(only used for reddit video & audio combination)_

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

[#] Reddit Stuff Downloader [#]

positional arguments:
  _postIdUrl           value of PostID/postUrl

optional arguments:
  -h, --help           show this help message and exit
  -l, --subredditList  predefines subreddits list
  -i, --postID         single Post ID; -i <PostID>
  -u, --postUrl        single Post URL; -u <PostUrl>
 
 
Each subreddit content is saaved in a seperate directory 
along with posts links saved in json file
```
## TODO:
- [x] Download Reddit videos along with audio
- [ ] Command line arguments **_[currently working on]_**
- [ ] Verify Windows OS support !??
- [ ] Cannot downlaod some URL's content
- [ ] Unknown URL must be properly notified (logs)
- [ ] Reconstruct the source code using classes and with proper documentation


Copyright (c) 2020 Maneesh
