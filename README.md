# HWC Notes Feed

This repository contains the code for a page that generates h-feeds of [Homebrew Website Club](https://indieweb.org/Homebrew_Website_Club) session notes.

A live version of this project is hosted at https://jamesg.blog/hwc-notes/.

This project uses Python to scrape the IndieWeb wiki for all recent events. This information is then turned into a h-feed for each individual event, as well as a h-feed for all events.

The page contains links to Granary URLs that convert the h-feeds into RSS feeds.

## Contributing

To contribute to this project, first clone the project repository:

```
git clone https://github.com/capjamesg/hwc-notes-feed
```

Then, install the required dependencies:

```
pip install -r requirements.txt
```

Then, run `hwcnotes.py` to generate the HWC notes feed page:

```
python3 hwcnotes.py
```

This script reads `template.html`, processes its contents using the data scraped from the wiki, and saves a page with h-feeds in `index.html`.

## License

This project is licensed in the public domain.