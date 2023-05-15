Name:     emudbg
Version:  0.2+202305151016
Release:  1%{?dist}
Summary:  emulator-agnostic source-level debugging API
License:  GPLv3+
URL:      https://github.com/dciabrin/emudbg

%define headrev %(echo %{version} | cut -d+ -f2)

Source0: https://github.com/dciabrin/emudbg/archive/nightly-%{headrev}.tar.gz

BuildRequires: automake autoconf libtool pkgconfig

%description
emudbg defines a simple debugging API that can be implemented by
emulators to expose simple step-by-step execution and memory
inspection capabilities over a standard GDB remote serial protocol

%global debug_package %{nil}

%package devel
Summary:  emulator-agnostic source-level debugging API (development files)
Provides: emudbg-static = %{version}-%{release}
ExclusiveArch: x86_64
%description devel
emudbg defines a simple debugging API that can be implemented by
emulators to expose simple step-by-step execution and memory
inspection capabilities over a standard GDB remote serial protocol


%prep
%autosetup -n %{name}-nightly-%{headrev}

%build
autoreconf -iv
%configure
make %{?_smp_mflags}

%install
%make_install


%files devel
%{_includedir}/emudbg.h
%{_libdir}/libemudbg.a
%{_libdir}/pkgconfig/emudbg.pc
%doc AUTHORS NEWS README
%license COPYING


%changelog
* Mon May 15 2023 CI Build Bot <> - 0.2+202305151016-1
- Nightly build for tag nightly-202305151016
