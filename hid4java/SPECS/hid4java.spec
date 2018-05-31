Name: hid4java
Version: 0.5.0
Release: 1%{?dist}
Summary: Java wrapper for the hidapi library

License: MIT
URL: http://github.com/gary-rowe/hid4java
Source0: https://github.com/gary-rowe/%{name}/archive/%{name}-%{version}.tar.gz
BuildArch: noarch

BuildRequires: maven-local
BuildRequires: mvn(org.apache.maven.plugins:maven-source-plugin)
BuildRequires: mvn(net.java.dev.jna:jna)

Requires: hidapi

%description
hid4java supports USB HID devices through a common API. The API is very simple
but provides great flexibility such as support for feature reports and blocking
reads with timeouts. Attach/detach events are provided to allow applications to
respond instantly to device availability.


%package javadoc
Summary: Javadoc for %{name}

%description javadoc
This package contains the API documentation for %{name}.

%prep
%autosetup -n %{name}-%{name}-%{version}

sed -i 's/Native.loadLibrary("hidapi",/Native.loadLibrary("hidapi-libusb",/' \
src/main/java/org/hid4java/jna/HidApiLibrary.java

find -name '*.so' -print -delete
find -name '*.dylib' -print -delete
find -name '*.dll' -print -delete

%build
%mvn_build

%install
%mvn_install

%files -f .mfiles
%doc AUTHORS README.md
%license LICENSE

%files javadoc -f .mfiles-javadoc
%doc AUTHORS README.md
%license LICENSE

%changelog
* Fri May 18 2018 J Szinger <jszinger> - 0.5.0-1
- update to 0.5.0

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Aug 27 2015 Jonny Heggheim <hegjon@gmail.com> - 0.4.0-2
- Fixed the dependency for hidapi

* Mon Aug 24 2015 Jonny Heggheim <hegjon@gmail.com> - 0.4.0-1
- Update to upstream version 0.4.0

* Fri Aug 07 2015 Jonny Heggheim <hegjon@gmail.com> - 0.4.0-0.1.gitb010cee
- Inital packaging
