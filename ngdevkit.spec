Name:     ngdevkit
Version:  0.4+202403182012
Release:  1%{?dist}
Summary:  Open source development for Neo-Geo
License:  GPLv3+
URL:      https://github.com/dciabrin/ngdevkit

%define headrev %(echo %{version} | cut -d+ -f2)

Source0:  https://github.com/dciabrin/ngdevkit/archive/nightly-%{headrev}.tar.gz

BuildRequires: autoconf automake make zip python ngdevkit-toolchain pkg-config
Requires: ngdevkit-toolchain pkg-config
Requires: python >= 3.0
Requires: python3-pyyaml

%description
ngdevkit is a ASM/C/C++ software development kit for
the Neo-Geo AES or MVS hardware. It provides a complete
toolchain for cross compiling to the m68k and z80 CPUs,
a C library for easy hardware access, and a set of tools
for managing character and sprite ROMs. It also comes with
an open-source BIOS replacement for running your ROM under
your favorite emulator, and a m68k-enabled GDB for
source-level-debugging.

# Disable stripping of m68k libraries
%global __os_install_post %{nil}

# Disable debuginfo for now
%global debug_package %{nil}

ExclusiveArch: x86_64

%prep
%autosetup -n %{name}-nightly-%{headrev}

%build
autoreconf -iv
%configure --enable-external-toolchain --enable-external-emudbg --enable-external-gngeo --enable-examples=no
make -j1 #%{?_smp_mflags}

%install
%make_install

# %check

%files
%{_bindir}/*.py
/usr/m68k-neogeo-elf/include/*
/usr/m68k-neogeo-elf/lib/*
%{_datadir}/ngdevkit/neogeo.zip
%{_datadir}/ngdevkit/nullsound.ihx
%{_datadir}/ngdevkit/nullsound/*
%{_datadir}/pkgconfig/ngdevkit.pc
# %doc
%license COPYING COPYING.LESSER


%changelog
* Mon Mar 18 2024 CI Build Bot <> - 0.4+202403182012-1
- Nightly build for tag nightly-202403182012
