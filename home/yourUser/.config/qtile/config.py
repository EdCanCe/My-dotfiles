# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
from libqtile import bar, layout, qtile, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from datetime import datetime

mod = "mod4"

# Apps to open
terminal = "kitty"
browser = "firefox"
textEditor = "flatpak run com.visualstudio.code"
fileManager = "nautilus"
normalScreenShot = "Scripts/fullscreenshot.sh"
areaScreenShot = "Scripts/screenshot.sh"
startScript = "Scripts/atstartonce.sh" #Everytime the system boots
git ="flatpak run io.github.shiftey.Desktop"
apps = "rofi -show drun"

# Bar font
textFont="Montserrat, Bold"

# Colors of the bar
color1="#F9E400"
color2="#FFAF00"
color3="#F5004F"
color4="#7C00FE"

black="#000814"
white="#ffffff"
gray="#2f3b4d"

# Separator between widgets
leftSep="\ue0be"
rightSep="\ue0bc"

margins=6
barText=14
barSize=barText+20

# NerdFonts Icons
consoleTag="\uf30a" #fedora
codeTag="\ue70c" #vscode
browserTag="\ue745" #firefox
gitTag="\uf09b"
musicTag="\uf1bc" #spotify
databaseTag="\uf1c0"
shellTag="\ue795"

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),

    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),

    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key(
        [mod],
        "f",
        lazy.window.toggle_fullscreen(),
        desc="Toggle fullscreen on the focused window",
    ),
    Key([mod], "t", lazy.window.toggle_floating(), desc="Toggle floating on the focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
    
    # Brightness, media and colume
    Key([], "XF86MonBrightnessUp", lazy.spawn("brightnessctl set +10%")),
    Key([], "XF86MonBrightnessDown", lazy.spawn("brightnessctl set 10%-")),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ +5%")), #Este funciona con pulseaudio
    Key([], "XF86AudioPlay", lazy.spawn("playerctl play-pause")),
    Key([], "XF86AudioNext", lazy.spawn("playerctl next")),
    Key([], "XF86AudioPrev", lazy.spawn("playerctl previous")),
    Key([], "XF86AudioLowerVolume", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ -5%")),
    Key([], "XF86AudioMute", lazy.spawn("pactl set-sink-mute @DEFAULT_SINK@ toggle")),
    
    # Launch apps
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod], "b", lazy.spawn(browser), desc="Launch browser"),
    Key([mod], "c", lazy.spawn(textEditor), desc="Launch text editor"),
    Key([mod], "m", lazy.spawn(fileManager), desc="Launch file manager"),
    Key([mod], "s", lazy.spawn(normalScreenShot), desc="Take screenshot"),
    Key([mod], "g", lazy.spawn(git), desc="Launch Git"),
    Key([mod, "shift"], "s", lazy.spawn(areaScreenShot), desc="Take screenshot in selected area"),
    Key([mod, "shift"], "r", lazy.spawn(apps), desc="Select a program to run"),
]

# Add key bindings to switch VTs in Wayland.
# We can't check qtile.core.name in default config as it is loaded before qtile is started
# We therefore defer the check until the key binding is run by using .when(func=...)
for vt in range(1, 8):
    keys.append(
        Key(
            ["control", "mod1"],
            f"f{vt}",
            lazy.core.change_vt(vt).when(func=lambda: qtile.core.name == "wayland"),
            desc=f"Switch to VT{vt}",
        )
    )

# The order of icons in the bar
groups = [Group(i) for i in [
    consoleTag, browserTag, codeTag, shellTag, gitTag, musicTag, databaseTag,
]]

for i, group in enumerate(groups):
    desktopNumber=str(i+1)
    keys.extend(
        [
            # mod + group number = switch to group
            Key(
                [mod],
                desktopNumber,
                lazy.group[group.name].toscreen(),
                desc="Switch to group {}".format(group.name),
            ),
            # mod + shift + group number = switch to & move focused window to group
            Key(
                [mod, "shift"],
                desktopNumber,
                lazy.window.togroup(group.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(group.name),
            ),
        ]
    )

# Used layouts
layouts = [
    layout.Columns(border_width=3, margin=margins, border_normal=black, border_focus=color1),
    layout.Zoomy(columnwidth=250, margin=margins)
]

# Screen config
screens = [
    Screen(
    	wallpaper="~/.config/qtile/bg.jpg",
        top=bar.Bar(
            [
                widget.GroupBox(
                	margin_y=3,
                    	margin_x=0,
                    	padding_y=5,
                    	padding_x=6,
                    	borderwidth=3,
                    	active=color4,
                    	inactive=gray,
                    	this_current_screen_border=color2,
                    	block_highlight_text_color=white,
                        urgent_border=color3,
                    	rounded=False,
                    	highlight_method='block',
                    	fontsize=barSize-5,
                    	background=black),
                widget.Prompt(background=black, font=textFont, foreground=white),
                widget.WindowName(background=black, font=textFont, foreground=white),
                widget.Systray(font=textFont),
                widget.TextBox(leftSep, background=black, foreground=color4, fontsize=barSize, font="FiraCode", margin=0, padding=0),
                widget.Net(format="{down:.0f}{down_suffix} ↓↑ {up:.0f}{up_suffix}", background=color4, foreground=black, font=textFont),
                widget.TextBox(leftSep, foreground=color3, background=color4, fontsize=barSize, font="FiraCode", margin=0, padding=0),
                widget.Volume(background=color3, foreground=black, fmt='Vol: {}', font=textFont),
                widget.TextBox(leftSep, foreground=color2, background=color3, fontsize=barSize, font="FiraCode", margin=0, padding=0),
                widget.Battery(discharge_char="", update_interval=10, format="{char}{percent: 2.0%}", background=color2, foreground=black, font=textFont),
                widget.TextBox(leftSep, foreground=color1, background=color2, fontsize=barSize, font="FiraCode", margin=0, padding=0),
                widget.Clock(format='%d/%m/%y  %H:%M    ', background=color1, foreground=black, font=textFont, fontsize=barText-2),
            ],
            barSize,
            margin=[margins, margins, 0, margins],
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),
        Match(wm_class="makebranch"),  
        Match(wm_class="maketag"),
        Match(wm_class="ssh-askpass"),
        Match(title="branchdialog"),
        Match(title="pinentry")
    ],
    border_width=0
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# xcursor theme (string or None) and size (integer) for Wayland backend
wl_xcursor_theme = None
wl_xcursor_size = 24

wmname = "LG3D"

# Do a script every startup
@hook.subscribe.startup_once
def autostart():
    os.system(startScript)