Name:           json-schema-validator
Version:        0.1.19
Release:        1%{?dist}
Summary:        Java JSON schema validator

License:        Apache
URL:            https://github.com/networknt/json-schema-validator
Source0:        https://github.com/networknt/%{name}/archive/%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  maven-local
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:  mvn(org.jacoco:jacoco-maven-plugin)

BuildRequires:  mvn(ch.qos.logback:logback-classic)
BuildRequires:  mvn(com.fasterxml.jackson.core:jackson-databind)
BuildRequires:  mvn(io.undertow:undertow-core)
BuildRequires:  mvn(org.slf4j:slf4j-ext)

# Testing
BuildRequires:  mvn(org.mockito:mockito-core)


%description
A Java JSON schema validator that supports JSON schema draft v4.

%package        javadoc
Summary:        Javadoc for %{name}

%description javadoc
This package contains the API documentation for %{name}.

%prep
%autosetup -n %{name}-%{version}

%pom_remove_plugin :maven-source-plugin
%pom_remove_plugin :nexus-staging-maven-plugin

%build
%mvn_build

%install
%mvn_install


%files -f .mfiles
%license LICENSE
%doc README.md CHANGELOG.md

%files javadoc -f .mfiles-javadoc


%changelog
* Fri May 25 2018 J Szinger <jszinger> - 0.1.19-1
- Initial package
