Name:           apache-commons-text
Version:        1.3
Release:        1%{?dist}
Summary:        Apache Commons Text is a library focused on algorithms working on strings

License:        ASL 2.0
URL:            https://commons.apache.org/proper/commons-text/project-summary.html
Source0:        https://archive.apache.org/dist/commons/text/source/commons-text-%{version}-src.tar.gz

BuildArch:      noarch

BuildRequires:  maven-local
BuildRequires:  mvn(org.apache.commons:commons-lang3)
BuildRequires:  mvn(org.apache.commons:commons-parent:pom:)

# Testing only; not available
#BuildRequires: mvn(org.junit.jupiter:junit-jupiter-engine:5.2.0)
#BuildRequires: mvn(org.junit.jupiter:junit-jupiter-params5.2.0)
#BuildRequires: mvn(org.junit.platform:junit-platform-launcher:1.2.0)
#BuildRequires: mvn(org.assertj:assertj-core:3.10.0)

#Requires:       

%description
Apache Commons Text is a library focused on algorithms working on strings


%package        javadoc
Summary:        Javadoc for %{name}

%description javadoc
This package contains the API documentation for %{name}.


%prep
%autosetup -n commons-text-%{version}-src

%build
%mvn_build -f

%install
%mvn_install

%files -f .mfiles
%license LICENSE.txt NOTICE.txt
%doc README.md RELEASE-NOTES.txt

%files javadoc -f .mfiles-javadoc
%license LICENSE.txt NOTICE.txt



%changelog
* Tue May 22 2018 J Szinger <jszinger>
- Initial package
