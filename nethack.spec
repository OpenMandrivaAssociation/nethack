Name:		nethack
Version:	3.4.3
Release:	2
Summary:	A roguelike dungeon exploration game

Group:		Games/Adventure
License:	Nethack GPL
URL:		http://www.nethack.org
Source0:	http://downloads.sourceforge.net/%{name}/%{name}-343-src.tgz
# Nethack Linux settings/defines
Patch0:		nethack-settings.patch
# HP monitor, patch from http://www.netsonic.fi/~walker/nh/hpmon.diff 
# Some parts adapted from Debian's patch
Patch1: 	nethack-enh-hpmon.patch
# "Paranoid hit" patch by Joshua Kwan <joshk@triplehelix.org>
# heavily edited from http://www.netsonic.fi/~walker/nh/paranoid-343.diff
# originally by  David Damerell, Jonathan Nieder, Jukka Lahtinen, Stanislav
# Traykov
#
# Adapted from its Debian version
Patch2:		nethack-enh-paranoid-hit.patch
#TODO: unfinished
Patch3:		nethack-3.4.3-makefile-destdir.patch
BuildRequires:	ncurses-devel bison flex


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
%patch0 -p1 -b .settings~
%patch1 -p1 -b .hpmon~
%patch2 -p1 -b .paranoid~
#%patch3 -p1 -b .destdir~
# Generates makefiles
(source sys/unix/setup.sh)

%build
# Patch in our paths with RPM macros.
perl -pi -e 's{MDV_HACKDIR}{%{_gamesdatadir}/nethack}' include/config.h
perl -pi -e 's{MDV_VAR_PLAYGROUND}{%{_localstatedir}/lib/games/nethack}' include/unixconf.h
%make CFLAGS="%{optflags} -I../include -Wno-error=format-security" LDFLAGS="%{ldflags}"

%install
%makeinstall_std \
        GAMEDIR=%{buildroot}%{_gamesdatadir}/nethack \
        VARDIR=%{buildroot}%{_localstatedir}/lib/games/nethack \
        SHELLDIR=%{buildroot}%{_gamesbindir} \
        CHOWN=/bin/true \
        CHGRP=/bin/true
rm -f %{buildroot}%{_gamesbindir}/nethack                                                                                                                     
mv %{buildroot}%{_gamesdatadir}/nethack/nethack %{buildroot}%{_gamesbindir}/nethack                                                                           
mv %{buildroot}%{_gamesdatadir}/nethack/recover %{buildroot}%{_gamesbindir}/nethack-recover                                                                   
install -m644 doc/nethack.6 -D %{buildroot}%{_mandir}/man6/nethack.6

%post
%create_ghostfile %{_localstatedir}/lib/games/nethack/record root games 664
%create_ghostfile %{_localstatedir}/lib/games/nethack/perm root games 664
%create_ghostfile %{_localstatedir}/lib/games/nethack/logfile root games 664

%files
%doc doc/*txt README dat/license
%{_gamesdatadir}/nethack
%{_mandir}/man6/*
%defattr(755,root,games)
%{_gamesbindir}/nethack-recover
%attr(2755,root,games) %{_gamesbindir}/nethack
%defattr(644,root,games,775)
%dir %{_localstatedir}/lib/games/nethack/
%dir %{_localstatedir}/lib/games/nethack/save
%ghost %verify(not md5 size mtime) %{_localstatedir}/lib/games/nethack/record
%ghost %verify(not md5 size mtime) %{_localstatedir}/lib/games/nethack/perm
%ghost %verify(not md5 size mtime) %{_localstatedir}/lib/games/nethack/logfile
