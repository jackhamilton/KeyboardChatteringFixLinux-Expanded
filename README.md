This is an enhancement to finkrer's fantastic existing solution. The readme below is a mirror of the original project's. My changes are as follows:

1) Added support for virtual keyboards, e.g. KMonad. My testing has revolved mainly around this functionality, but I've tried to keep the original's intact. Please feel free to submit an issue if anything is broken.
2) Added a configuration file, at /root/.config/KeyboardChatteringFix/config. It's in TOML format, so should be fairly standard. It's at root rather than user level since the application must run at root level.
3) Added a service installer. Please note the pip3 install requirements.txt line may fail on some operating systems - if it does, and the service breaks, please manually install the contents of requirements.txt. This installer installs the program to /usr/lib/KeyboardChatteringService, creates the config, installs a systemd service to /usr/lib/systemd/system/chattering_fix.service, and starts said service.

Installation:
```shell
git clone https://github.com/jackhamilton/KeyboardChatteringFixLinux-Expanded.git
cd KeyboardChatteringFixLinux-Expanded
sudo sh setup.sh
cd ..
rm -rf KeyboardChatteringFixLinux-Expanded
```

Original readme (I've removed the sections this version makes outdated):
# __Keyboard Chattering Fix for Linux__

[![GitHub](https://img.shields.io/github/license/w2sv/KeyboardChatteringFix-Linux?)](LICENSE)

__A tool for filtering mechanical keyboard chattering on Linux__

## The problem

Switches on mechanical keyboards occasionally start to "chatter",
meaning when you press a key with a faulty switch it erroneously detects
two or even more key presses.

## The existing solutions

Apart from buying a new keyboard, there have been ways to deal
with this problem using software methods. The idea is to filter key presses
that occur faster than a certain threshold. "Keyboard Chattering Fix v 0.0.1"
is a tool I had been using on Windows for a long time, and these days you also have
[Keyboard Chatter Blocker](https://github.com/mcmonkeyprojects/KeyboardChatterBlocker),
which is a nice open source tool with some additional functionality. It's actually what
I use myself when I use Windows.

Unfortunately, all existing tools only work on Windows.
On Linux, the answer everyone seems to give is to use the Bounce Keys feature of X,
but it's not really useful in this way. For one, it resets the delay even on filtered
key presses, meaning that if you press the key fast enough,
*none* of the presses with pass through, ever. And if the key chatters,
this is bound to happen eventually and interfere with fast repeated key presses.

## This project's solution

This tool attempts to solve any such problems that may arise by having full low-level access
and control over all keyboard events.
Using `libevdev`'s Python bindings, it grabs your keyboard's event device and processes its events,
then outputs the result back to the system using `/dev/uinput`, effectively emulating a keyboard -
one that doesn't chatter, unlike your real one!

This also means it works across the system, without depending on X.

As for the filtering rule, what seems to work well is the time between the last key up event
and the current key down event. When the key chatters, that time seems to be very low - around 10 ms.
By filtering such anomalies, we can hopefully remove chatter without impeding actual fast key presses.
