Name:           purejavacomm
Version:        1.0.1
Release:        1%{?dist}
Summary:        PureJavaComm is an Application Programming Interface (API) for accessing serial ports from Java

License:        BSD
URL:            https://github.com/nyholku/purejavacomm
Source0:        https://github.com/nyholku/%{name}/archive/v%{version}.tar.gz   

BuildArch:      noarch

BuildRequires:  maven-local
BuildRequires:  mvn(org.apache.maven.wagon:wagon-ssh)
BuildRequires:  mvn(org.apache.maven.wagon:wagon-ftp)

#Requires:      

%description
PureJavaComm is an Application Programmin Interface (API) for
accessing serial ports from Java, so this is a library aimed at
programmers, not end users.

PureJavaComm aims to be a drop-in replacement for Sun's (now Oracle)
abandoned JavaComm and an easier to deploy alternative to RXTX.

PJC is written 100% in Java so it is easy for Java programmers to
develop and debug and it requires no native libraries. Native access
to the underlaying operating system's serial port programming
interface is provided by the wonderful JNA library which takes away
all the pain of compiling and deploying native code.

PJC is BSD licensed but please note it depends on JNA which is
LGPL/ASL dual licensed.

%package        javadoc
Summary:        Javadoc for %{name}

%description javadoc
This package contains the API documentation for %{name}.


%prep
%autosetup
rm -rf lib/

%build
%mvn_build


%install
%mvn_install

%files -f .mfiles
#license LICENSE.txt
%doc README.md ChangeLog doc/DE9-pinout.txt

%files javadoc -f .mfiles-javadoc




%changelog
* Wed Mar 28 2018 J Szinger
- Initial package
