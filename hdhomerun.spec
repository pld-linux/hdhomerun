# TODO
# - fix icons
Summary:	Silicon Dust HDHomeRun configuration utility
Name:		hdhomerun
Version:	20141210
Release:	1
License:	LGPL v3 and GPL v3
Group:		Applications/System
Source0:	http://download.silicondust.com/hdhomerun/lib%{name}_%{version}.tgz
# Source0-md5:	c3bf11ecfa3b1ceeedc54ec67e7f25b4
Source1:	http://download.silicondust.com/hdhomerun/%{name}_config_gui_%{version}.tgz
# Source1-md5:	b4bf62b088fb58c5b0e85ed7e30294a2
Source2:	%{name}_config_gui.desktop
URL:		http://www.silicondust.com/
BuildRequires:	desktop-file-utils
BuildRequires:	gtk+2-devel
BuildRequires:	libicns
Requires:	gtk-update-icon-cache
Requires:	hicolor-icon-theme
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The configuration and firmware upgrade utility for Silicon Dust's
networked HDTV dual-tuner HDHomeRun device.

%description
The configuration and firmware upgrade utility for Silicon Dust's
networked HDTV dual-tuner HDHomeRun device.

%package devel
Summary:	Developer tools for the hdhomerun library
Group:		Development
Requires:	%{name} = %{version}-%{release}

%description devel
The hdhumerun-devel package provides developer tools for the hdhomerun
library.

%prep
%setup -qc -a 1

# Fix up linefeeds, drop execute bit and don't strip binaries
%{__sed} -i 's/\r//' libhdhomerun/*
%{__chmod} -x libhdhomerun/*
%{__sed} -i -e '/$(STRIP).*/d' -e 's/C\(PP\)\?FLAGS .=/C\1FLAGS ?=/' libhdhomerun/Makefile

# Convert files to utf8
for f in libhdhomerun/*; do
	iconv -f iso-8859-1 -t utf-8 --output $f.new $f && mv $f.new $f
done

cat << __EOF__ > README.firmware
The HDHomeRun Firmwares are not redistributable, but the latest versions of
both the US ATSC and European DVB-T firmwares can always be obtained from
the Silicon Dust web site:

http://www.silicondust.com/downloads/linux

__EOF__

%build
cd hdhomerun_config_gui
%configure
%{__make}
cd ..

%if 0
# fails with assertion:
#+ icns2png -x hdhr.icns
#icns2png: jpc_dec.c:1072: jpc_dec_tiledecode: Assertion `dec->numcomps == 3' failed.
cd hdhomerun_config_gui/OSX
icns2png -x hdhr.icns
cd -
%endif

%install
rm -rf $RPM_BUILD_ROOT
%{__make} -C hdhomerun_config_gui install \
	DESTDIR=$RPM_BUILD_ROOT

install -p libhdhomerun/hdhomerun_config $RPM_BUILD_ROOT%{_bindir}
rm -rf include
install -d include
cp -a libhdhomerun/*.h include
sed -r 's|(^#include +["])(.*)(["] *$)|#include <hdhomerun/\2>|' \
    libhdhomerun/hdhomerun.h > include/hdhomerun.h
install -d $RPM_BUILD_ROOT%{_includedir}/hdhomerun
cp -p include/*.h $RPM_BUILD_ROOT%{_includedir}/hdhomerun
desktop-file-install --dir=${RPM_BUILD_ROOT}%{_desktopdir} %{SOURCE2}

%if 0
for size in 16x16 32x32 128x128 256x256 512x512; do
	install -d $RPM_BUILD_ROOT%{_iconsdir}/hicolor/${size}
	cp -p hdhomerun_config_gui/OSX/hdhr_${size}x32.png $RPM_BUILD_ROOT%{_iconsdir}/hicolor/${size}/hdhr.png
done
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if 0
%post
%update_icon_cache hicolor

%postun
%update_icon_cache hicolor
%endif

%files
%defattr(644,root,root,755)
%doc libhdhomerun/lgpl.txt libhdhomerun/README hdhomerun_config_gui/COPYING README.firmware
# lib and cli are LGPLv3
%{_libdir}/libhdhomerun.so
%attr(755,root,root) %{_bindir}/hdhomerun_config
# gui is GPLv3
%attr(755,root,root) %{_bindir}/hdhomerun_config_gui
%{_desktopdir}/hdhomerun_config_gui.desktop
#%{_iconsdir}/hicolor/*/hdhr.png

%files devel
%defattr(644,root,root,755)
%dir %{_includedir}/hdhomerun
%{_includedir}/hdhomerun/*.h
