# RedditStuffDownloader
>Download any subreddit posts/media/content

## Requirements
* `Python 3.8`
* `Reddit account` - _with Script app activated (for API requests)_
  * fill the `config.json` file with the required configuration
* `FFMPEG` download from website, keep in parent directory

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
python Reddit-Stuff-Downloader/reddit-dwn.py 

Each subreddit content is saaved in a seperate directory along with posts likst saved in json file
```
## TODO:
- [x] Download Reddit videos along with audio
- [ ] Cannot downlaod some URL's content
- [ ] Unknown URL must be properly notified (logs)
- [ ] Reconstruct the source code using classes and with proper documentation


Copyright (c) 2020 Maneesh
