# OHSINT(THM)

OSINT refers to Open Source Intelligence so basically gathering all the information we can about something by just using open source tools.

So first of all to get metadata out of our images and stuff we can use a tool called exiftool which is normally built in Kali Linux and if its not you can download it through apt-get.

```bash
exiftool image.png
```

After we do this we get the metadata we can see the picture is registered or copyrighted by OWoodFlint and when we google search that name we find 2 of his profiles and 1 blog by him .

## Twitter →

In twitter we find out that his profile picture is cat and he lives in London and we find out that he tweeted his BSSID which we search in [wigle.net](http://wigle.net) and we find out the SSID through that

## GitHub →

On his GitHub we find out his email listed in a read.md

## WordPress Blog

In there we find out where he went for a trip to New York and then when we inspect that paragraph element we can see the password there as well .
