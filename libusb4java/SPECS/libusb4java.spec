%global commit 396d642a57678a0d9663b062c980fe100cc0ea1e
%global shortcommit %(c=%{commit}; echo ${c:0:7})

# find-debuginfo can't handle JNI jars
%global debug_package %{nil}

Name:           libusb4java
Version:        1.2.0
Release:        1.20160126git%{shortcommit}%{?dist}
Summary:        JNI wrapper for libusb

License:        MIT
URL:            http://usb4java.org/
Source0:        https://github.com/usb4java/%{name}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz


#BuildRequires:  maven-local
#BuildRequires: mvn(org.apache.maven.plugins:maven-assembly-plugin)
#BuildRequires: mvn(org.apache.maven.plugins:maven-surefire-plugin)

#BuildRequires: mvn(junit:junit)
#BuildRequires: mvn(org.apache.commons:commons-lang3)
#BuildRequires: mvn(org.usb4java:libusb4java)

BuildRequires: cmake
BuildRequires: java-devel
BuildRequires: javapackages-local
BuildRequires: libusb-devel

 
%description
usb4java is a Java library to access USB devices. It is based on the
native libusb 1.0 library and uses Java NIO buffers for data exchange
between libusb and Java.

%prep
%autosetup -n %{name}-%{commit}


%build
%cmake . -DCMAKE_BUILD_TYPE=Release 
%make_build

mkdir -p classes/org/usb4java/%{platform}
cp -p src/libusb4java.so classes/org/usb4java/%{platform}
jar cvf libusb4java-%{platform}.jar -C classes org
%mvn_artifact org.usb4java:%{name}:%{version} libusb4java-%{platform}.jar

%install
%mvn_install

%files -f .mfiles
%license LICENSE.md
%doc README.md



%changelog
* Tue May 15 2018 J Szinger
- Initial package

