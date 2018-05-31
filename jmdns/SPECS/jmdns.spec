Name:           jmdns
Version:        3.5.4
Release:        1%{?dist}
Summary:        Java implementation of multi-cast DNS

# The project was originally developed under the GNU
# Lesser General Public License. It was later moved to Sourceforge
# and re-released under the Apache License, Version 2.0.
# See NOTICE.txt for more details
License:        ASL 2.0 and LGPLv2+
URL:            http://www.jmdns.org/

Source0:        https://github.com/jmdns/%{name}/archive/%{name}-%{version}.tar.gz
# faster (unclean) shutdown, used by Jenkins
# https://github.com/jenkinsci/jmdns/commit/4d56e6f0f0c230b14f1353252ae3d42ff7a5b27c
#Patch0:         0001-added-an-unclean-shut-down-that-s-a-whole-lot-faster.patch

BuildRequires:  maven-local
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:  mvn(org.codehaus.mojo:buildnumber-maven-plugin)
BuildRequires:  mvn(org.sonatype.oss:oss-parent:pom:)

BuildArch:      noarch

%description
JmDNS is a Java implementation of multi-cast DNS
and can be used for service registration and discovery
in local area networks. JmDNS is fully compatible
with Apple's Bonjour.

%package        javadoc
Summary:        Javadoc for %{name}

%description javadoc
This package contains the API documentation for %{name}.


%prep
%autosetup -n %{name}-%{name}-%{version}

# Fix FSF address
sed -i "s,59 Temple Place,51 Franklin Street,;s,Suite 330,Fifth Floor,;s,02111-1307,02110-1301," \
  src/sample/java/samples/DiscoverServiceTypes.java #LICENSE-LGPL.txt

# Remove duplicate jar execution
%pom_xpath_remove "pom:plugin[pom:artifactId='maven-jar-plugin']/pom:executions"

%mvn_alias : "org.jenkins-ci:jmdns"

%build
# Tests are disabled because they try to use network
%mvn_build -f

%install
%mvn_install


%files -f .mfiles
%license LICENSE NOTICE.txt
%doc README.md

%files javadoc -f .mfiles-javadoc
%license LICENSE NOTICE.txt


%changelog
* Fri May 18 2018 J Szinger <jszinger> - 3.5.4-1
- Update to 3.5.4

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Feb 16 2017 Mat Booth <mat.booth@redhat.com> - 3.4.1-12
- Fix failure to build from source

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Sep 01 2014 Michal Srb <msrb@redhat.com> - 3.4.1-8
- Fix BR

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.4.1-6
- Use Requires: java-headless rebuild (#1067528)

* Thu Feb 20 2014 Michal Srb <msrb@redhat.com> - 3.4.1-5
- Backport Jenkins patch: faster shutdown
- Add alias org.jenkins-ci:jmdns

* Thu Feb 20 2014 Michal Srb <msrb@redhat.com> - 3.4.1-4
- Fix directory ownership
- Add script for creating clean tarball

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri May 03 2013 Michal Srb <msrb@redhat.com> - 3.4.1-2
- Fix license tag
- Fix rpmlint warnings

* Thu May 02 2013 Michal Srb <msrb@redhat.com> - 3.4.1-1
- Initial package

