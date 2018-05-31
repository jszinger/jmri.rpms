Name:           javax-usb
Version:        1.0.2
Release:        1%{?dist}
Summary:        Java API that allows direct USB-level access to the system's USB devices

License:        CPL
URL:            http://javax-usb.sourceforge.net/
Source0:        https://sourceforge.net/projects/javax-usb/files/javax.usb%%20API/1.0.2/javax-usb_1.0.2.tar.bz2

BuildArch:      noarch

BuildRequires:  ant
BuildRequires:  javapackages-local

%description
This project allows access to USB devices from Java. It was created
under the JCP process and is assigned JSR 080. The official Java
package name is 'javax.usb'.

%package        javadoc
Summary:        Javadoc for %{name}

%description javadoc
This package contains the API documentation for %{name}.

%prep
%autosetup -n %{name}

%build
ant all

%install
%mvn_artifact javax.usb:usb-api:%{version} lib/jsr80.jar
%mvn_install -J docs/jdoc

%files -f .mfiles
%license LICENSE
%doc README

%files javadoc -f .mfiles-javadoc

%changelog
* Tue May 15 2018 J Szinger
- initial package
