Name:     ngdevkit-gngeo
Version:  0.8.1+202501101116
Release:  1%{?dist}
Summary:  Portable Neo-Geo emulator customized for ngdevkit
License:  GPLv3+
URL:      https://github.com/dciabrin/gngeo

%define headrev %(echo %{version} | cut -d+ -f2)

Source0:  https://github.com/dciabrin/gngeo/archive/nightly-%{headrev}.tar.gz

BuildRequires: autoconf autoconf-archive automake libtool make pkg-config SDL2-devel zlib-devel glew-devel
Requires: emudbg-static libGLEW SDL2 zlib

%description
SDL2 fork of GnGeo, the portable Neo-Geo emulator. It provides a
couple of additional features compared to the original GnGeo like
GLSL blitter, libretro pixel shader, source-level debugging.  It also
targets additional platforms like macOS, raspberry PI and native
Windows 10.

# Disable stripping of m68k libraries
%global __os_install_post %{nil}

# Disable debuginfo for now
%global debug_package %{nil}

ExclusiveArch: x86_64

%prep
%autosetup -n gngeo-nightly-%{headrev}

%build
autoreconf -iv
%configure --program-prefix=ngdevkit- CFLAGS="-fPIE -Wno-implicit-function-declaration -DGNGEORC=\\\"ngdevkit-gngeorc\\\""
make -j1 pkgdatadir=%{_datadir}/ngdevkit-gngeo

%install
%make_install pkgdatadir=%{_datadir}/ngdevkit-gngeo

# %check

%files
%{_bindir}/ngdevkit-gngeo
%{_datadir}/man/man1/ngdevkit-gngeo.1
%{_datadir}/ngdevkit-gngeo/gngeo_data.zip
%{_datadir}/ngdevkit-gngeo/noop.glsl
%{_datadir}/ngdevkit-gngeo/noop.glslp

# %doc
%license COPYING


%changelog
* Fri Jan 10 2025 CI Build Bot <> - 0.8.1+202501101116-1
- Nightly build for tag nightly-202501101116
