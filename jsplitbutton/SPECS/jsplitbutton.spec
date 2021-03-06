# Should unit tests be run?  Defaults to off.  Enable using
# '--with tests'.
%global with_tests   0%{?_with_tests:1}

Name:           jsplitbutton
Version:        1.3.1
Release:        1%{?dist}
Summary:        A split button control for Java Swing.

License:        Apache
URL:            https://github.com/rhwood/%{name}
Source0:        https://github.com/rhwood/%{name}/archive/v%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  maven-local
BuildRequires:  mvn(junit:junit)

BuildRequires:  mvn(org.apache.maven.plugins:maven-source-plugin)
BuildRequires:  mvn(org.jacoco:jacoco-maven-plugin)

%if %{with_tests}
BuildRequires:  xorg-x11-server-Xvfb
%endif


%description
A simple implementation of the split button control for Java Swing.

%package        javadoc
Summary:        Javadoc for %{name}

%description javadoc
This package contains the API documentation for %{name}.

%prep
%autosetup

%build
%if %{with_tests}
  xvfb-run %mvn_build
%else
  %mvn_build -f
%endif


%install
%mvn_install

%files -f .mfiles
%license LICENSE.txt
%doc README.md

%files javadoc -f .mfiles-javadoc
%license LICENSE.txt

%changelog
* Fri Jul 13 2018 J Szinger <jszinger> - 1.3.1-1
- Initial package
