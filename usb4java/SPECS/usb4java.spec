Name:           usb4java
Version:        1.2.0
Release:        1%{?dist}
Summary:        USB library for Java based on libusb

License:        MIT
URL:            http://usb4java.org/
Source0:        https://github.com/usb4java/%{name}/archive/%{name}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  maven-local

BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(org.apache.commons:commons-lang3)
BuildRequires:  mvn(org.usb4java:libusb4java)

 
%description
usb4java is a Java library to access USB devices. It is based on the
native libusb 1.0 library and uses Java NIO buffers for data exchange
between libusb and Java.

%package        javadoc
Summary:        Javadoc for %{name}

%description javadoc
This package contains the API documentation for %{name}.

%prep
%autosetup -n usb4java-usb4java-%{version}

%pom_remove_plugin :maven-assembly-plugin

%pom_remove_dep org.usb4java:libusb4java
%pom_add_dep  org.usb4java:libusb4java:%{version}

%build
%mvn_build -f

%install
%mvn_install

%files -f .mfiles
%license LICENSE.md
%doc README.md

%files javadoc -f .mfiles-javadoc


%changelog
* Tue May 15 2018 J Szinger
- Initial package
