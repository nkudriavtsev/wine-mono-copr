%undefine _auto_set_build_flags
%undefine _hardened_build
%{?mingw_package_header}

Name:           wine-mono
Version:        9.0.0
Release:        1%{?dist}
Summary:        Mono library required for Wine

License:        GPL-2.0-or-later AND LGPL-2.1-only AND MIT AND BSD-4-Clause-UC AND MS-PL AND MPL-1.1
URL:            http://wiki.winehq.org/Mono
# https://github.com/madewokherd/wine-mono
Source0:        https://dl.winehq.org/wine/wine-mono/%{version}/wine-mono-%{version}-src.tar.xz
Patch0:         wine-mono-7.3.0-iconv.patch
Patch1: wine-mono-configure-c99.patch

# see git://github.com/madewokherd/wine-mono

BuildArch:      noarch
ExcludeArch:    %{power64} s390x s390

# 64
BuildRequires:  mingw64-filesystem >= 95
BuildRequires:  mingw64-headers
BuildRequires:  mingw64-cpp
BuildRequires:  mingw64-gcc
BuildRequires:  mingw64-gcc-c++
BuildRequires:  mingw64-crt
BuildRequires:  mingw64-winpthreads-static
# 32
BuildRequires:  mingw32-filesystem >= 95
BuildRequires:  mingw32-headers
BuildRequires:  mingw32-cpp
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-gcc-c++
BuildRequires:  mingw32-crt
BuildRequires:  mingw32-winpthreads-static

BuildRequires:  autoconf automake
BuildRequires:  bc
BuildRequires:  cmake
BuildRequires:  dos2unix
BuildRequires:  gcc-c++
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  pkgconfig
BuildRequires:  gettext
BuildRequires:  libgdiplus
BuildRequires:  wine-core
BuildRequires:  /usr/bin/python
BuildRequires:  python3-setuptools
BuildRequires:  python3-devel

# https://bugs.winehq.org/show_bug.cgi?id=48937
# fixed in wine 5.7
BuildRequires:  dos2unix

Requires: wine-filesystem

# Bundles FAudio, libtheorafile, libmojoshader, SDL2, SDL2_image

%description
Windows Mono library required for Wine.

%global mingw_build_win32 0
%global mingw_build_win64 0
%{?mingw_debug_package}

%prep
%setup -q
%patch -P 0 -p1 -b.iconv
%patch -P 1 -p1 -b.c99

# Fix all Python shebangs
%py3_shebang_fix .
sed -i 's/GENMDESC_PRG=python/GENMDESC_PRG=python3/' mono/mono/mini/Makefile.am.in

# remove shipped compiler
rm -rf llvm-mingw-20210423-ucrt-ubuntu-18.04-x86_64/*
sed -i 's/$CPPFLAGS_FOR_BTLS $btls_cflags/$CPPFLAGS_FOR_BTLS -fPIC $btls_cflags/' mono/configure.ac

# workaround coreutils 9.2 behavior change to "cp -n" option (RHBZ#2208129)
# https://github.com/madewokherd/wine-mono/issues/164
sed -i 's~cp -n $(IMAGEDIR)/lib/mono/4.8-api/\*.dll $(IMAGEDIR)/lib/mono/4.5/~cp -n $(IMAGEDIR)/lib/mono/4.8-api/\*.dll $(IMAGEDIR)/lib/mono/4.5/ || true~' mono.make

%build
export BTLS_CFLAGS="-fPIC"
export CPPFLAGS_FOR_BTLS="-fPIC"
# Disable LLVM compiler as we do not ship a full, updated MinGW environment. Use GCC instead.
echo "AUTO_LLVM_MINGW=0" > user-config.make
# Disable WpfGfx as it requires LLVM to compile
echo "ENABLE_DOTNET_CORE_WPFGFX=0" >> user-config.make
%make_build image

%install
mkdir -p %{buildroot}%{_datadir}/wine/mono/wine-mono-%{version}/
cp -rp image/* \
    %{buildroot}%{_datadir}/wine/mono/wine-mono-%{version}/

# prep licenses
cp mono/LICENSE mono-LICENSE
cp mono/COPYING.LIB mono-COPYING.LIB
cp mono/mcs/COPYING mono-mcs-COPYING

pushd mono/mcs

for l in `ls LICENSE*`; do
echo $l
cp $l ../../mono-mcs-$l
done

popd

cp mono-basic/README mono-basic-README
cp mono-basic/LICENSE mono-basic-LICENSE

%files
%license COPYING mono-LICENSE mono-COPYING.LIB mono-basic-LICENSE mono-mcs*
%doc README mono-basic-README
%{_datadir}/wine/mono/wine-mono-%{version}/

%changelog
%autochangelog
