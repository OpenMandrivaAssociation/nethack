Name:           nethack
Version:        3.4.3
Release:        %mkrel 1
Summary:        A roguelike dungeon exploration game

Group:          Games/Adventure
License:        Nethack GPL
URL:            http://www.nethack.org
Source:         http://downloads.sourceforge.net/%{name}/%{name}-343-src.tgz
# Nethack Linux settings/defines
Patch0:         nethack-settings.patch
# HP monitor, patch from http://www.netsonic.fi/~walker/nh/hpmon.diff 
# Some parts adapted from Debian's patch
Patch1: 		nethack-enh-hpmon.patch
# "Paranoid hit" patch by Joshua Kwan <joshk@triplehelix.org>
# heavily edited from http://www.netsonic.fi/~walker/nh/paranoid-343.diff
# originally by  David Damerell, Jonathan Nieder, Jukka Lahtinen, Stanislav
# Traykov
#
# Adapted from its Debian version
Patch2:         nethack-enh-paranoid-hit.patch

BuildRoot: 		%{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires:  ncurses-devel
BuildRequires:  bison, flex


%description
NetHack is a single player dungeon exploration game that runs on a
wide variety of computer systems, with a variety of graphical and text
interfaces all using the same game engine.

Unlike many other Dungeons & Dragons-inspired games, the emphasis in
NetHack is on discovering the detail of the dungeon and not simply
killing everything in sight - in fact, killing everything in sight is
a good way to die quickly.

Each game presents a different landscape - the random number generator
provides an essentially unlimited number of variations of the dungeon
and its denizens to be discovered by the player in one of a number of
characters: you can pick your race, your role, and your gender.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
# Generates makefiles
(source sys/unix/setup.sh)

%build
# Patch in our paths with RPM macros.
perl -pi -e 's{MDV_HACKDIR}{%{_gamesdatadir}/games/nethack}' include/config.h
perl -pi -e 's{MDV_VAR_PLAYGROUND}{%{_var}/games/nethack}' include/unixconf.h
%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall \
        GAMEDIR=$RPM_BUILD_ROOT%{_gamesdatadir}/games/nethack \
        VARDIR=$RPM_BUILD_ROOT%{_var}/games/nethack \
        SHELLDIR=$RPM_BUILD_ROOT%{_gamesbindir} \
        CHOWN=/bin/true \
        CHGRP=/bin/true
rm -f $RPM_BUILD_ROOT%{_gamesbindir}/nethack
mv $RPM_BUILD_ROOT%{_gamesdatadir}/games/nethack/nethack $RPM_BUILD_ROOT%{_gamesbindir}/nethack
mv $RPM_BUILD_ROOT%{_gamesdatadir}/games/nethack/recover $RPM_BUILD_ROOT%{_gamesbindir}/nethack-recover
install -D -m644 doc/nethack.6 $RPM_BUILD_ROOT%{_mandir}/man6/nethack.6

%clean
rm -rf $RPM_BUILD_ROOT

%files
%_gamesdatadir/games/nethack
%_mandir/man6/*
%attr(0775,root,games) %{_var}/games/nethack
%attr(2755,root,games) %_gamesbindir/nethack
%attr(0755,root,games) %_gamesbindir/nethack-recover
%attr(664,root,games) %config(noreplace) %{_var}/games/nethack/record
%attr(664,root,games) %config(noreplace) %{_var}/games/nethack/perm
%attr(664,root,games) %config(noreplace) %{_var}/games/nethack/logfile
