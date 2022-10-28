%global gnu_mirror https://ftpmirror.gnu.org
%global newlib_mirror https://sourceware.org/ftp

Name:     ngdevkit-toolchain
Version:  0.1+202210281551
Release:  1%{?dist}
Summary:  Open source development for Neo-Geo
License:  GPLv3+
URL:      https://github.com/dciabrin/ngdevkit-toolchain

%global headrev %(echo %{version} | cut -d+ -f2)

Source0:  https://github.com/dciabrin/ngdevkit-toolchain/archive/nightly-%{headrev}.tar.gz
Source1:  %{gnu_mirror}/binutils/binutils-2.35.2.tar.bz2
Source2:  %{gnu_mirror}/gcc/gcc-5.5.0/gcc-5.5.0.tar.xz
Source3:  %{gnu_mirror}/gdb/gdb-9.2.tar.xz
Source4:  %{newlib_mirror}/newlib/newlib-4.0.0.tar.gz
Source5:  http://sourceforge.net/projects/sdcc/files/sdcc/3.7.0/sdcc-src-3.7.0.tar.bz2


BuildRequires: autoconf automake bison gawk make texinfo flex gcc-c++
BuildRequires: libtool pkgconfig
BuildRequires: boost-devel bzip2-devel readline-devel
BuildRequires: expat-devel gmp-devel libmpc-devel mpfr-devel ncurses-devel xz-devel zlib-devel
Requires: expat flex gettext gmp libmpc mpfr ncurses sed xz zlib

%description
ngdevkit is a C/C++ software development kit for the Neo-Geo AES or
MVS hardware. This package provides the toolchain of the toolkit.

# Disable stripping of m68k libraries
%global __os_install_post %{nil}

# Disable debuginfo for now
%global debug_package %{nil}

ExclusiveArch: x86_64

%prep
%autosetup -n %{name}-nightly-%{headrev}

%build
make %{?_smp_mflags} -- prefix=/usr LOCAL_PACKAGE_DIR=%{_sourcedir}

%install
%make_install -- prefix=/usr

# %check

%files
%{_bindir}/m68k-neogeo-elf-*
/usr/m68k-neogeo-elf/include/*
/usr/m68k-neogeo-elf/bin/*
/usr/m68k-neogeo-elf/info/*
/usr/m68k-neogeo-elf/lib/*
/usr/m68k-neogeo-elf/locale/*
/usr/m68k-neogeo-elf/man/*
/usr/m68k-neogeo-elf/lib64/*
%{_bindir}/z80-neogeo-ihx-*
/usr/z80-neogeo-ihx/include/*
/usr/z80-neogeo-ihx/lib/*
/usr/z80-neogeo-ihx/doc/*
# %doc
%license COPYING COPYING.LESSER


%changelog
* Fri Oct 28 2022 CI Build Bot <> - 0.1+202210281551-1
- Nightly build for tag nightly-202210281551
