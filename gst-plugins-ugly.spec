%define _disable_ld_no_undefined 1
%define major 1.0
%define majorminor 1.0
%define bname gstreamer1.0
%define name %{bname}-plugins-ugly

%define build_experimental 0
%{?_with_experimental: %{expand: %%global build_experimental 1}}
%define build_lame 0
%define build_amrnb 0
%define build_amrwbdec 0
%define build_x264 0

##########################
# Hardcode PLF build
%define build_plf 1
##########################

%if %{build_plf}
%define distsuffix plf
# make EVR of plf build higher than regular to allow update, needed with rpm5 mkrel
%define extrarelsuffix plf
%define build_lame 1
%define build_x264 1
%define build_amrnb 1
%define build_amrwbdec 1
%endif

Summary: GStreamer Streaming-media framework plug-ins
Name: %{name}
Version: 1.6.2
Release: 1%{?extrarelsuffix}
License: LGPLv2+
Group: Sound
Source0: http://gstreamer.freedesktop.org/src/gst-plugins-ugly/gst-plugins-ugly-%{version}.tar.xz
URL: http://gstreamer.freedesktop.org/
#gw for the pixbuf plugin
BuildRequires: pkgconfig(gtk+-2.0)
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(orc-0.4)
BuildRequires: gstreamer-plugins-base-devel
BuildRequires: pkgconfig(glu)
BuildRequires: pkgconfig(id3tag)
BuildRequires: pkgconfig(mad)
BuildRequires: pkgconfig(dvdread)
%ifnarch %mips %arm
BuildRequires: pkgconfig(valgrind)
%endif
BuildRequires: pkgconfig(check)
Provides: %{bname}-audiosrc
Provides: %{bname}-audiosink

%description
GStreamer is a streaming-media framework, based on graphs of filters which
operate on media data. Applications using this library can do anything
from real-time sound processing to playing videos, and just about anything
else media-related. Its plugin-based architecture means that new data
types or processing capabilities can be added simply by installing new
plug-ins.

This package contains a set of plug-ins that have good quality and
correct functionality, but distributing them might pose problems. The
license on either the plug-ins or the supporting libraries might not
be how the GStreamer authors like. The code might be widely known to
present patent problems.

%if %{build_plf}
This package is in restricted repository as it violates some patents.
%endif

%prep
%setup -q -n gst-plugins-ugly-%{version}

%build
%configure2_5x --disable-dependency-tracking --disable-static \
--with-package-name='OpenMandriva %{name} package' \
--with-package-origin='http://www.openmandriva.org/' \
%if ! %{build_lame}
--disable-lame \
%endif
%if %{build_experimental}
--enable-experimental
%endif

%make

%check
cd tests/check
make check VERBOSE=1

%install
GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1 %makeinstall_std

%find_lang gst-plugins-ugly-%{majorminor}

rm -fr %{buildroot}%{_datadir}/gtk-doc

# Clean out files that should not be part of the rpm.
# This is the recommended way of dealing with it for RH8
find %{buildroot} -name '*.la' -delete

%files -f gst-plugins-ugly-%{majorminor}.lang
%doc AUTHORS COPYING README NEWS
%{_libdir}/gstreamer-%{majorminor}/libgstasf.so
%{_libdir}/gstreamer-%{majorminor}/libgstdvdlpcmdec.so
%{_libdir}/gstreamer-%{majorminor}/libgstdvdread.so
%{_libdir}/gstreamer-%{majorminor}/libgstdvdsub.so
%{_libdir}/gstreamer-%{majorminor}/libgstmad.so
%{_libdir}/gstreamer-%{majorminor}/libgstrmdemux.so
%if %{build_experimental}
%{_libdir}/gstreamer-%{majorminor}/libgstsynaesthesia.so
%endif
%{_libdir}/gstreamer-%{majorminor}/libgstxingmux.so

%if %{build_lame}
### LAME ###
%package -n %{bname}-lame
Summary: GStreamer plug-in for encoding mp3 songs using lame
Group: Sound
Requires: %{bname}-plugins-base
BuildRequires: %{bname}-plugins-base
BuildRequires:	%{bname}-tools
BuildRequires: lame-devel >= 3.89

%description -n %{bname}-lame
Plug-in for encoding mp3 with lame under GStreamer.

This package is in the restricted repository as it violates some patents.

%files -n %{bname}-lame
%{_libdir}/gstreamer-%{majorminor}/libgstlame.so
%endif

%if %{build_x264}
%package -n %{bname}-x264
Summary: GStreamer plug-in for H264/AVC video encoding
Group: Video
BuildRequires: pkgconfig(x264)

%description -n %{bname}-x264
Plug-in for encoding H264/AVC video.

This package is in restricted repository as it violates some patents.

%files -n %{bname}-x264
%{_libdir}/gstreamer-%{majorminor}/libgstx264.so
%{_datadir}/gstreamer-%{majorminor}/presets/GstX264Enc.prs
%endif

%if %{build_amrnb}
%package -n %{bname}-amrnb
Summary: GStreamer plug-in for AMR-NB support
Group: Sound
Requires: %{bname}-plugins-base
BuildRequires: pkgconfig(opencore-amrnb)

%description -n %{bname}-amrnb
Plug-in for decoding AMR-NB under GStreamer.

This package is in restricted repository as it violates some patents.

%files -n %{bname}-amrnb
%{_libdir}/gstreamer-%{majorminor}/libgstamrnb.so
%{_datadir}/gstreamer-%{majorminor}/presets/GstAmrnbEnc.prs
%endif

%if %{build_amrwbdec}
%package -n %{bname}-amrwbdec
Summary: GStreamer plug-in for AMR-WB decoding support
Group: Sound
Requires: %{bname}-plugins-base
BuildRequires: pkgconfig(opencore-amrwb)

%description -n %{bname}-amrwbdec
Plug-in for decoding AMR-Wb under GStreamer.

This package is in restricted repository as it violates some patents.

%files -n %{bname}-amrwbdec
%{_libdir}/gstreamer-%{majorminor}/libgstamrwbdec.so
%endif

### SIDPLAY ###
%package -n %{bname}-sid
Summary: GStreamer Sid C64 music plugin
Group: Sound
Requires: %{bname}-plugins-base
BuildRequires: sidplay-devel

%description -n %{bname}-sid
Plugin for playback of C64 SID format music files

%files -n %{bname}-sid
%{_libdir}/gstreamer-%{majorminor}/libgstsid.so

### A52DEC ###
%package -n %{bname}-a52dec
Summary: GStreamer VOB decoder plugin
Group: Sound
Requires: %{bname}-plugins-base
BuildRequires: a52dec-devel >= 0.7.3

%description -n %{bname}-a52dec
Plugin for decoding of VOB files.

%files -n %{bname}-a52dec
%{_libdir}/gstreamer-%{majorminor}/libgsta52dec.so

%package -n %{bname}-mpeg
Summary: GStreamer plug-ins for MPEG video playback and encoding
Group: Video
Requires: %{bname}-plugins-base
BuildRequires: pkgconfig(libmpeg2)

%description -n %{bname}-mpeg
Plug-ins for playing and encoding MPEG video.

%files -n %{bname}-mpeg
%{_libdir}/gstreamer-%{majorminor}/libgstmpeg2dec.so

%package -n %{bname}-cdio
Summary: GStreamer plug-in for audio CD playback
Group: Sound
Requires: %{bname}-plugins-base
BuildRequires: pkgconfig(libcdio)
Conflicts: %{bname}-plugins-good < 0.10.10

%description -n %{bname}-cdio
Plug-in for audio CD playback.

%files -n %{bname}-cdio
%{_libdir}/gstreamer-%{majorminor}/libgstcdio.so

%package -n %{bname}-twolame
Summary: GStreamer plug-in for MP2 encoding support
Group: Sound
Requires: %{bname}-plugins-base
BuildRequires: pkgconfig(twolame)

%description -n %{bname}-twolame
Plug-in for encoding MP2 under GStreamer.

%files -n %{bname}-twolame
%{_libdir}/gstreamer-%{majorminor}/libgsttwolame.so
