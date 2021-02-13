%undefine _hardened_build
%{?mingw_package_header}

Name:           wine-mono
Version:        6.0.0
Release:        1%{?dist}
Summary:        Mono library required for Wine

License:        GPLv2 and LGPLv2 and MIT and BSD and MS-PL and MPLv1.1
URL:            http://wiki.winehq.org/Mono
# https://github.com/madewokherd/wine-mono
Source0:        https://dl.winehq.org/wine/wine-mono/%{version}/wine-mono-%{version}-src.tar.xz
# to statically link in winpthreads
Patch0:         wine-mono-build-static.patch

# https://bugs.winehq.org/show_bug.cgi?id=48937
# fixed in wine 5.7
Patch1:         wine-mono-crlf.patch

# see git://github.com/madewokherd/wine-mono

BuildArch:      noarch
ExcludeArch:    %{power64} s390x s390

# 64
BuildRequires: make
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
BuildRequires:  pkgconfig
BuildRequires:  gettext
BuildRequires:  libgdiplus
BuildRequires:  wine-core
BuildRequires:  /usr/bin/python
BuildRequires:  /usr/bin/pathfix.py

# https://bugs.winehq.org/show_bug.cgi?id=48937
# fixed in wine 5.7
BuildRequires:  dos2unix

Requires: wine-filesystem

# Bundles FAudio, libtheorafile, libmojoshader, SDL2, SDL2_image

%description
Windows Mono library required for Wine.

%global mingw_build_win32 0
%{?mingw_debug_package}

%prep
%setup -q
%patch0 -p1 -b.static
%patch1 -p1 -b.crlf

# Fix all Python shebangs
pathfix.py -pni "%{__python3} %{py3_shbang_opts}" .
sed -i 's/GENMDESC_PRG=python/GENMDESC_PRG=python3/' mono/mono/mini/Makefile.am.in

# remove shipped compiler
rm -rf llvm-mingw-20200325-ubuntu-18.04/*
sed -i 's/$CPPFLAGS_FOR_BTLS $btls_cflags/$CPPFLAGS_FOR_BTLS -fPIC $btls_cflags/' mono/configure.ac

%build
export BTLS_CFLAGS="-fPIC"
export CPPFLAGS_FOR_BTLS="-fPIC"
# Disable LLVM compiler as we do not ship a full, updated MinGW environment. Use GCC instead.
echo "AUTO_LLVM_MINGW=0" > user-config.make
# Disable WpfGfx as it requires LLVM to compile
echo "ENABLE_DOTNET_CORE_WPFGFX=0" >> user-config.make
make %{_smp_mflags} image

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
* Sat Feb 13 2021 Michael Cronenworth <mike@cchtml.com> - 6.0.0-1
- version upgrade

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Oct 10 2020 Michael Cronenworth <mike@cchtml.com> - 5.1.1-1
- version upgrade

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jun 24 2020 Michael Cronenworth <mike@cchtml.com> - 5.1.0-1
- version upgrade

* Sun Apr 26 2020 Michael Cronenworth <mike@cchtml.com> - 5.0.0-1
- version upgrade

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.9.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Nov 16 2019 Michael Cronenworth <mike@cchtml.com> - 4.9.4-1
- version upgrade

* Sun Sep 29 2019 Michael Cronenworth <mike@cchtml.com> - 4.9.3-1
- version upgrade

* Mon Aug 19 2019 Michael Cronenworth <mike@cchtml.com> - 4.9.2-1
- version upgrade

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Jun 23 2019 Michael Cronenworth <mike@cchtml.com> - 4.9.0-1
- version upgrade

* Sun Apr 28 2019 Michael Cronenworth <mike@cchtml.com> - 4.8.3-1
- version upgrade

* Sun Apr 14 2019 Michael Cronenworth <mike@cchtml.com> - 4.8.1-1
- version upgrade
- switch from MSI to new shared filesystem format

* Fri Mar 01 2019 Michael Cronenworth <mike@cchtml.com> - 4.8.0-1
- version upgrade

* Mon Feb 18 2019 Michael Cronenworth <mike@cchtml.com> - 4.7.5-1
- version upgrade

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.7.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Aug 23 2018 Peter Robinson <pbrobinson@fedoraproject.org> 4.7.3-2
- Don't exclude aarch64

* Sat Jul 21 2018 Michael Cronenworth <mike@cchtml.com> - 4.7.3-1
- version upgrade

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.7.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Aug 08 2017 Michael Cronenworth <mike@cchtml.com> - 4.7.1-1
- version upgrade

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Mar 23 2017 Michael Cronenworth <mike@cchtml.com> - 4.7.0-1
- version upgrade

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.6.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Dec 15 2016 Michael Cronenworth <mike@cchtml.com> - 4.6.4-1
- version upgrade

* Thu Oct 13 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.6.3-2
- mono rebuild for aarch64 support

* Wed Jun 15 2016 Michael Cronenworth <mike@cchtml.com> - 4.6.3-1
- version upgrade

* Sun Apr 17 2016 Michael Cronenworth <mike@cchtml.com> - 4.6.2-1
- version upgrade

* Sun Mar 13 2016 Peter Robinson <pbrobinson@fedoraproject.org> 4.6.0-2
- Fix up the Wine / mono supported arch cross section

* Tue Mar 08 2016 Michael Cronenworth <mike@cchtml.com> - 4.6.0-1
- version upgrade

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 4.5.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.5.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Apr 23 2015 Michael Cronenworth <mike@cchtml.com> - 4.5.6-4
- enable optimizations, tls patch

* Mon Apr 20 2015 Michael Cronenworth <mike@cchtml.com> - 4.5.6-3
- statically link DLLs (#1213427)

* Sun Mar 08 2015 Michael Cronenworth <mike@cchtml.com> - 4.5.6-2
- disable optimizations in CLI, workaround for gcc5

* Fri Mar 06 2015 Michael Cronenworth <mike@cchtml.com> - 4.5.6-1
- version upgrade

* Thu Feb 05 2015 Michael Cronenworth <mike@cchtml.com> - 4.5.4-2
- Update bundled valgrind headers (#1141584)

* Fri Nov 14 2014 Andreas Bierfert <andreas.bierfert@lowlatency.de>
- 4.5.4-1
- version upgrade

* Tue Jun 24 2014 Michael Cronenworth <mike@cchtml.com> - 4.5.2-4
- Rebuilt to use static libgcc (#1056436)

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.5.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Dec 14 2013 Michael Cronenworth <mike@cchtml.com>
- 4.5.2-2
- Add ExcludeArch as Mono requires an x86 builder host

* Sun Dec 08 2013 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 4.5.2-1
- version upgrade

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Apr  4 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 0.0.8-3
- Fix FTBFS against latest automake
- Added BR: bc

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Oct 29 2012 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.0.8-1
- version upgrade

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

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
