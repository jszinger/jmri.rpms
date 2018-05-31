# Netbeans platform is too hard to package, so let's just pull the
# modules we need.
Name:           openide-util-lookup
Version:        8.2
Release:        1%{?dist}
Summary:        Support for the Registration and Lookup extension mechanism.

License:        GPLv2 with exceptions or CDDL
URL:            http://platform.netbeans.org

Source0:        http://download.netbeans.org/netbeans/%{version}/final/zip/netbeans-%{version}-201609300101-platform-src.zip
Source1:        org-openide-util-lookup.pom
BuildArch:      noarch


BuildRequires:  maven-local

#BuildRequires:  mvn(javax.annotation:javax.annotation-api)
#BuildRequires:  mvn(org.netbeans.api:org-openide-filesystems)

%description
Support classes for the Registration and Lookup extension mechanism.

%package        javadoc
Summary:        Javadoc for %{name}

%description javadoc
This package contains the API documentation for %{name}.

%prep
%autosetup -c
cd openide.util.lookup
cp %{SOURCE1} pom.xml

#ln -s ../../../../openide.filesystems/src/org/openide/filesystems src/org/openide/

%build
cd openide.util.lookup
# Tests need org.netbeans.junit
%mvn_build -f

%install
cd openide.util.lookup
%mvn_install

%files -f openide.util.lookup/.mfiles
%license nbbuild/licenses/CDDL-GPL-2-CP

%files javadoc -f openide.util.lookup/.mfiles-javadoc


%changelog
* Thu May 31 2018 J Szinger <jszinger> - 8.2-1
- Initial package
