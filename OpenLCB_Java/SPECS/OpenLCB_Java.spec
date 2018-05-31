%global commit f471067d6c60e4e0854ed607fd41d68282708c30
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           OpenLCB_Java
Version:        0.7.18
Release:        1.20180513git%{shortcommit}%{?dist}
Summary:        OpenLCB Java Prototype

License:        GPLv2+
URL:            https://github.com/openlcb/%{name}OpenLCB_Java
Source0:        https://github.com/openlcb/%{name}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
Source1:        https://www.gnu.org/licenses/old-licenses/gpl-2.0.txt
BuildArch:      noarch

#https://github.com/openlcb/OpenLCB_Java/archive/master.zip

BuildRequires:  maven-local

BuildRequires:  mvn(net.jcip:jcip-annotations)
BuildRequires:  mvn(org.jdom:jdom2)
BuildRequires:  mvn(com.google.code.findbugs:annotations)
BuildRequires:  mvn(com.google.code.findbugs:jsr305)
BuildRequires:  mvn(net.jcip:jcip-annotations)
BuildRequires:  mvn(org.jacoco:jacoco-maven-plugin)
BuildRequires:  mvn(org.umlgraph:umlgraph)

# Testing
#BuildRequires:  mvn(junit:junit)
#BuildRequires:  mvn(org.mockito:mockito-core)
#BuildRequires:  mvn(org.hamcrest:hamcrest-library)

%description
OpenLCB Java Prototype

%package        javadoc
Summary:        Javadoc for %{name}

%description javadoc
This package contains the API documentation for %{name}.

%prep
%autosetup -n %{name}-%{commit}
cp -p %{SOURCE1} .

rm -rf lib/
rm *.jar

%pom_remove_dep com.github.spotbugs:spotbugs-annotations
%pom_remove_dep net.java.linoleum:jlfgr
%pom_remove_plugin :maven-source-plugin 

%pom_add_dep com.google.code.findbugs:annotations:3.0.1


%build
%mvn_build -f


%install
%mvn_install

%files -f .mfiles
%license gpl-2.0.txt
%doc README.md

%files javadoc -f .mfiles-javadoc


%changelog
* Thu May 24 2018 J Szinger <jszinger> - 0.7.18-1.20180513gitf471067d6
- Initial package
