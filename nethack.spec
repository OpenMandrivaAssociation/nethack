%global nhgamedir /usr/games/nethack
%global nhdatadir /var/games/nethack
 
%global fontname nethack-bitmap

%bcond_with qt5

%if %{with qt5}
%global optflags %{optflags} -I%{_includedir}/qt5 -I%{_includedir}/qt5/QtCore -I%{_includedir}/qt5/QtWidgets
%endif

Name:		nethack
Version:	3.6.7
Release:	1
Summary:	A roguelike dungeon exploration game
Group:		Games/Adventure
License:	Nethack GPL
URL:		https://www.nethack.org
Source0:	https://www.nethack.org/download/%{version}/nethack-%(echo %{version}|sed -e 's,\.,,g')-src.tgz
Source1:	https://src.fedoraproject.org/rpms/nethack/raw/rawhide/f/nethack.desktop
BuildRequires:	ncurses-devel bison flex xaw-devel bdftopcf util-linux

%patchlist
https://src.fedoraproject.org/rpms/nethack/raw/rawhide/f/nethack-3.6.7-makefile.patch
https://src.fedoraproject.org/rpms/nethack/raw/rawhide/f/nethack-3.6.7-top.patch
https://src.fedoraproject.org/rpms/nethack/raw/rawhide/f/nethack-3.6.7-config.patch
https://src.fedoraproject.org/rpms/nethack/raw/rawhide/f/nethack-3.6.7-guidebook.patch
https://src.fedoraproject.org/rpms/nethack/raw/rawhide/f/hackdir.patch
https://src.fedoraproject.org/rpms/nethack/raw/rawhide/f/nethack-3.6.7-xpm.patch
https://src.fedoraproject.org/rpms/nethack/raw/rawhide/f/modern_c.patch

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
%autosetup -p0 -n NetHack-%{version}
%{__sed} -i -e "s:PREFIX=\$(wildcard ~)/nh/install:PREFIX=/usr:" sys/unix/hints/linux
%{__sed} -i -e "s:^\(HACKDIR=\).*:\1%{nhgamedir}:" sys/unix/hints/linux

%if %{with qt5}
sh sys/unix/setup.sh sys/unix/hints/linux-qt5

# Qt integration
sed -i -e 's,.*define X11_GRAPHICS.*,// #define X11_GRAPHICS,g' include/config.h
sed -i -e 's,.*define QT_GRAPHICS.*,#define QT_GRAPHICS,g' include/config.h
sed -i -e 's,^WINSRC =.*,WINSRC = $(WINTTYSRC) $(WINQTSRC) $(WINCURSESSRC),' src/Makefile
sed -i -e 's,^WINOBJ =.*,WINOBJ = $(WINTTYOBJ) $(WINQTOBJ) $(WINCURSESOBJ),' src/Makefile
sed -i -e 's,^WINLIB =.*,WINLIB = $(WINTTYLIB) $(WINQT5LIB) $(WINCURSESLIB),' src/Makefile
sed -i -e 's,^VARDATND =,VARDATND = x11tiles rip.xpm nhsplash.xpm ,' Makefile
%else
sh sys/unix/setup.sh sys/unix/hints/linux-x11
%endif
 
# Set our paths
%{__sed} -i -e "s:^\(HACKDIR=\).*:\1%{nhgamedir}:" sys/unix/nethack.sh
%{__sed} -i -e "s:FEDORA_CONFDIR:%{nhgamedir}:" sys/unix/nethack.sh
%{__sed} -i -e "s:FEDORA_STATEDIR:%{nhdatadir}:" include/unixconf.h
%{__sed} -i -e "s:FEDORA_HACKDIR:%{nhgamedir}:" include/config.h
%{__sed} -i -e "s:/usr/games/lib/nethackdir:%{nhgamedir}:" \
	doc/nethack.6 doc/nethack.txt doc/recover.6 doc/recover.txt
 
# Point the linker in the right direction
%{__sed} -i -e "s:-L/usr/X11R6/lib:-L/usr/X11R6/%{_lib}:" \
	src/Makefile util/Makefile


%build
make all

%install
%make_install \
	PREFIX=$RPM_BUILD_ROOT \
	HACKDIR=$RPM_BUILD_ROOT%{nhgamedir} \
	GAMEDIR=$RPM_BUILD_ROOT%{nhgamedir} \
	VARDIR=$RPM_BUILD_ROOT%{nhdatadir} \
	SHELLDIR=$RPM_BUILD_ROOT%{_bindir} \
	CHOWN=/bin/true \
	CHGRP=/bin/true
 
install -d -m 0755 $RPM_BUILD_ROOT%{_mandir}/man6
make -C doc MANDIR=$RPM_BUILD_ROOT%{_mandir}/man6 manpages

install -D -p -m 0644 win/X11/nh_icon.xpm \
	$RPM_BUILD_ROOT%{_datadir}/pixmaps/nethack.xpm

desktop-file-install \
	--dir $RPM_BUILD_ROOT%{_datadir}/applications \
	--add-category Game \
	--add-category RolePlaying \
	%{S:1}
 
# Install the fonts for the X11 interface
cd win/X11
bdftopcf -o nh10.pcf nh10.bdf
bdftopcf -o ibm.pcf ibm.bdf
install -m 0755 -d $RPM_BUILD_ROOT%{_fontdir}
install -m 0644 -p *.pcf $RPM_BUILD_ROOT%{_fontdir}
 
%{__sed} -i -e 's:^!\(NetHack.tile_file.*\):\1:' \
	$RPM_BUILD_ROOT%{nhgamedir}/NetHack.ad

%files
%doc doc/*.txt README dat/license dat/history
%doc dat/opthelp dat/wizhelp
%{_mandir}/man6/*
%{_datadir}/pixmaps/nethack.xpm
%{_datadir}/applications/nethack.desktop
%{_bindir}/nethack
%dir %{nhgamedir}
%defattr(0664,root,games)
%config(noreplace) %{nhdatadir}/record
%config(noreplace) %{nhdatadir}/perm
%config(noreplace) %{nhdatadir}/logfile
%config(noreplace) %{nhdatadir}/xlogfile
%attr(0775,root,games) %dir %{nhdatadir}
%attr(0775,root,games) %dir %{nhdatadir}/save
%attr(2755,root,games) %{nhgamedir}/nethack
%config(noreplace) %{nhgamedir}/nhdat
%config(noreplace) %{nhgamedir}/sysconf
%config(noreplace) %{nhgamedir}/NetHack.ad
%config(noreplace) %{nhgamedir}/license
%config(noreplace) %{nhgamedir}/pet_mark.xbm
%config(noreplace) %attr(0555,root,games) %{nhgamedir}/recover
%config(noreplace) %{nhgamedir}/rip.xpm
%config(noreplace) %{nhgamedir}/pilemark.xbm
%config(noreplace) %{nhgamedir}/symbols
%config(noreplace) %{nhgamedir}/x11tiles
%{nhgamedir}/nh10.pcf
%{nhgamedir}/fonts.dir
