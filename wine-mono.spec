%undefine _hardened_build
%{?mingw_package_header}

Name:           wine-mono
Version:        4.6.4
Release:        1%{?dist}
Summary:        Mono library required for Wine

License:        GPLv2 and LGPLv2 and MIT and BSD and MS-PL and MPLv1.1
Group:          Development/Libraries
URL:            http://wiki.winehq.org/Mono
Source0:        http://dl.winehq.org/wine/wine-mono/%{version}/wine-mono-%{version}.tar.gz
Patch0:         wine-mono-build-msifilename.patch
# to statically link in winpthreads
Patch1:         wine-mono-build-static.patch

# see git://github.com/madewokherd/wine-mono

BuildArch:      noarch
ExcludeArch:    aarch64 %{power64} s390x s390

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
BuildRequires:  libtool
BuildRequires:  pkgconfig
BuildRequires:  gettext
BuildRequires:  zip
BuildRequires:  wine-core
BuildRequires:  wine-devel
BuildRequires:  mono-core
BuildRequires:  bc

Requires: wine-filesystem

%description
Windows Mono library required for Wine.

%prep
%setup -q
%patch0 -p1 -b.msifilename
%patch1 -p1 -b.static

%build
MAKEOPTS=%{_smp_mflags} MSIFILENAME=wine-mono-%{version}.msi ./build-winemono.sh.static

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

%files
%license COPYING mono-LICENSE mono-COPYING.LIB mono-basic-LICENSE mono-mcs*
%doc README mono-basic-README
%{_datadir}/wine/mono/wine-mono-%{version}.msi

%changelog
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
