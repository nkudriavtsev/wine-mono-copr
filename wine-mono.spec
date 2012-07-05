%{?mingw_package_header}

Name:           wine-mono
Version:        0.0.4
Release:        7%{?dist}
Summary:        Mono library required for Wine

License:        GPLv2 and LGPLv2 and MIT and BSD and MS-PL and MPLv1.1
Group:          Development/Libraries
URL:            http://wiki.winehq.org/Mono
Source0:        http://sourceforge.net/projects/wine/files/Wine%20Mono/0.0.4/wine-mono-0.0.4.tar.gz
Patch0:         wine-mono-build-msifilename.patch
Patch1:         wine-mono-build-fixidtgeneration.patch

# see git://github.com/madewokherd/wine-mono
Patch100:       0052-Add-a-script-for-making-a-source-tarball.patch
Patch101:       0053-Rewrite-source-tarball-script.patch
Patch102:       0054-build-winemono.sh-unset-CC-when-cross-compiling-othe.patch
Patch103:       0055-Ship-MonoPosixHelper.dll.patch

BuildArch:      noarch

# 64
BuildRequires:  mingw64-filesystem >= 95
BuildRequires:  mingw64-binutils
BuildRequires:  mingw64-headers
BuildRequires:  mingw64-cpp
BuildRequires:  mingw64-gcc
BuildRequires:  mingw64-gcc-c++
BuildRequires:  mingw64-crt
# 32
BuildRequires:  mingw32-filesystem >= 95
BuildRequires:  mingw32-binutils
BuildRequires:  mingw32-headers
BuildRequires:  mingw32-cpp
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-gcc-c++
BuildRequires:  mingw32-crt

BuildRequires:  autoconf automake
BuildRequires:  libtool
BuildRequires:  pkgconfig
BuildRequires:  gettext
BuildRequires:  zip
BuildRequires:  wine-core wine-wow
BuildRequires:  wine-devel
BuildRequires:  mono-core

Requires: wine-filesystem

%description
Windows Mono library required for Wine.

%prep
%setup -q
%patch0 -b.msifilename
%patch1 -b.fixidtgen
%patch100 -p1
%patch101 -p1
%patch102 -p1
%patch103 -p1

%build
# make sure this builds on x86-64
if [ -x %{_bindir}/wine ] ; then
   MAKEOPTS=%{_smp_mflags} MSIFILENAME=wine-mono-%{version}.msi ./build-winemono.sh
else
   MAKEOPTS=%{_smp_mflags} WINE=%{_bindir}/wine64 MSIFILENAME=wine-mono-%{version}.msi ./build-winemono.sh
fi

%install
mkdir -p %{buildroot}%{_datadir}/wine/mono
install -p -m 0644 wine-mono-%{version}.msi \
    %{buildroot}%{_datadir}/wine/mono/wine-mono-%{version}.msi

# prep licenses
cp mono/LICENSE mono-LICENSE
cp mono/COPYING.LIB mono-COPYING.LIB

pushd mono/mcs

sed -i 's/\r//' LICENSE.MSPL

iconv -f iso8859-1 -t utf-8 LICENSE.MSPL > LICENSE.MSPL.conv && mv -f LICENSE.MSPL.conv LICENSE.MSPL

for l in `ls LICENSE*`; do
echo $l
cp $l ../../mono-mcs-$l
done

popd

cp mono-basic/README mono-basic-README
cp mono-basic/LICENSE mono-basic-LICENSE
cp MonoGame/LICENSE.txt MonoGame-LICENSE.txt

%files
%doc COPYING README
%doc mono-LICENSE mono-COPYING.LIB mono-mcs*
%doc mono-basic-README mono-basic-LICENSE
%doc MonoGame-LICENSE.txt
%{_datadir}/wine/mono/wine-mono-%{version}.msi

%changelog
* Wed Jul 04 2012 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.0.4-7
- add mingw-filesystem BR
- fix header macro

* Fri Jun 29 2012 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.0.4-6
- rename to wine-mono

* Wed Jun 27 2012 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.0.4-5
- add conditional so package builds on x86-64 builders as well

* Tue Jun 26 2012 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.0.4-4
- add -e option to echo in build script to fix idt files generation

* Sun Jun 24 2012 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.0.4-3
- pull some upstream patches from git

* Tue Jun 12 2012 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.0.4-2
- rename msi according to what wine expects

* Mon May 28 2012 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.0.4-1
- Initial release
