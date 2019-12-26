Name:		nethack
Version:	3.6.4
Release:	1
Summary:	A roguelike dungeon exploration game

Group:		Games/Adventure
License:	Nethack GPL
URL:		http://www.nethack.org
Source0:	http://downloads.sourceforge.net/%{name}/%{name}-364-src.tgz

BuildRequires:  pkgconfig(ncurses)
BuildRequires:  bison
BuildRequires:  flex
BuildRequires:  desktop-file-utils
BuildRequires:  bdftopcf
BuildRequires:  mkfontdir
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xaw7)
BuildRequires:  pkgconfig(xext)
BuildRequires:  pkgconfig(xmu)
BuildRequires:  pkgconfig(xpm)
BuildRequires:  pkgconfig(xt)
BuildRequires:  fontpackages-devel

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

%package -n %{fontname}-fonts
Summary:        Bitmap fonts for Nethack
Group:          System/Fonts/X11 bitmap
BuildArch:      noarch
Requires:       fontpackages-filesystem

%description -n %{fontname}-fonts
Bitmap fonts for Nethack.

%package -n %{fontname}-fonts-core
Summary:         X11 core fonts configuration for %{fontname}
Group:          System/Fonts/X11 bitmap
BuildArch:      noarch
Requires:        %{fontname}-fonts
Requires:  mkfontdir
Requires:  coreutils

%description -n %{fontname}-fonts-core
X11 core fonts configuration for %{fontname}.

%prep
%setup -q -n NetHack-NetHack-%{version}_Released
#patch0 -p1 -b .makefile
#patch1 -p1 -b .config
#patch2 -p1 -b .MAK2
#patch3 -p0 -b .guidebook

perl -i -l -p -e 's{^#(PREFIX=/usr)\s*$}{$1}; s{^(PREFIX=\$\(wildcard.*)$}{# $1};' sys/unix/hints/linux-x11

cd sys/unix
sh setup.sh hints/linux-x11

%build
make all

%install
%make_install PREFIX=%{buildroot}/%{_prefix}

rm -rf $RPM_BUILD_ROOT%{nhgamedir}/save
mkdir -p %{buildroot}%{_bindir}
mv $RPM_BUILD_ROOT%{nhgamedir}/recover $RPM_BUILD_ROOT%{_bindir}/nethack-recover
mv $RPM_BUILD_ROOT/usr/games/nethack $RPM_BUILD_ROOT%{_bindir}/nethack

install -d -m 0755 $RPM_BUILD_ROOT%{_mandir}/man6
make -C doc MANDIR=$RPM_BUILD_ROOT%{_mandir}/man6 manpages

install -D -p -m 0644 win/X11/nh_icon.xpm \
        $RPM_BUILD_ROOT%{_datadir}/pixmaps/nethack.xpm

desktop-file-install \
        --dir $RPM_BUILD_ROOT%{_datadir}/applications \
        --add-category Game \
        --add-category RolePlaying \
        %{SOURCE1}

# Install the fonts for the X11 interface
cd win/X11
bdftopcf -o nh10.pcf nh10.bdf
bdftopcf -o ibm.pcf ibm.bdf
install -m 0755 -d $RPM_BUILD_ROOT%{_fontdir}
install -m 0644 -p *.pcf $RPM_BUILD_ROOT%{_fontdir}

%{__sed} -i -e 's:^!\(NetHack.tile_file.*\):\1:' \
        $RPM_BUILD_ROOT%{nhgamedir}/NetHack.ad


%post -n %{fontname}-fonts-core
mkfontdir %{_fontdir}
if [ ! -L /etc/X11/fontpath.d/nethack ] ; then
    ln -s %{_fontdir} /etc/X11/fontpath.d/nethack
fi

%preun -n %{fontname}-fonts-core
if [ $1 -eq 0 ] ; then
    rm /etc/X11/fontpath.d/nethack
    rm %{_fontdir}/fonts.dir
fi;

%files
%doc doc/*.txt README dat/license dat/history
%doc dat/opthelp dat/wizhelp
%{_mandir}/man6/*
%{_datadir}/pixmaps/nethack.xpm
%{_datadir}/applications/nethack.desktop
%{_bindir}/nethack
%{_bindir}/nethack-recover
%{nhgamedir}
%defattr(0664,root,games)
%config(noreplace) %{nhgamedir}/record
%config(noreplace) %{nhgamedir}/perm
%config(noreplace) %{nhgamedir}/logfile
%attr(2755,root,games) %{nhgamedir}/nethack

%_font_pkg -n bitmap *.pcf

%files -n %{fontname}-fonts-core


%changelog
* Mon Sep 05 2011 Eskild Hustvedt <eskild@mandriva.org> 3.4.3-2
+ Revision: 698365
- Fixed creation of ghost files

* Mon Sep 05 2011 Eskild Hustvedt <eskild@mandriva.org> 3.4.3-1
+ Revision: 698342
- Fixed save dir
- Merged back Per ?\195?\152yvind's fixes
- Various permission and build fixes. Added docs.
- imported package nethack

  + Per Øyvind Karlsen <peroyvind@mandriva.org>
    - more fixes
    - start on cleaning up and refreshing rusty/obsolete Eskild's packaging skills ;)

