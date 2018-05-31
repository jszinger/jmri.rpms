Name:           jour
Version:        2.0.3
Release:        1%{?dist}
Summary:        An open source suite of java bytecode instrumentation.

License:        LGPL
URL:            http://jour.sourceforge.net/index.html
Source0:        http://downloads.sourceforge.net/%{name}/%{version}/%{name}-%{version}-src.zip

BuildArch:      noarch

BuildRequires:  maven-local
BuildRequires:  mvn(org.apache.maven.plugins:maven-dependency-plugin)
BuildRequires:  mvn(javassist:javassist)
BuildRequires:  mvn(org.apache.maven.plugins:maven-plugin-plugin)

# all require should be automatic
#Requires:      

%description
The Jour library is an open source suite of java bytecode
instrumentation base on Javassist.  Jour is designed to simplify the
use of Javassist for processing multiple classes. In short Jour is
simple Aspect Oriented Programming AOP framework on top of Javassist.

%package        javadoc
Summary:        Javadoc for %{name}

%description javadoc
This package contains the API documentation for %{name}.

%prep
%autosetup -c

%pom_disable_module jour-maven-plugin
%pom_disable_module jour-examples

%build
%mvn_build -f

%install
%mvn_install

%files -f .mfiles

%files javadoc -f .mfiles-javadoc

%changelog
* Tue Mar 27 2018 J Szinger
- Initial package
