Name:           beansbinding
Version:        1.2.1
Release:        18.1%{?dist}
Summary:        Beans Binding (JSR 295) reference implementation

Group:          Development/Libraries
License:        LGPLv2+
URL:            https://beansbinding.dev.java.net/
Source0:        https://beansbinding.dev.java.net/files/documents/6779/73673/beansbinding-1.2.1-src.zip
Source1:        http://central.maven.org/maven2/org/jdesktop/beansbinding/1.2.1/beansbinding-1.2.1.pom
Patch0:         disable-doclint.patch

BuildRequires:  ant
BuildRequires:  javapackages-local
BuildRequires:  ant-junit
BuildRequires:  java-devel

Requires:       java >= 1:1.6.0
Requires:       javapackages-tools

BuildArch:      noarch

%description
In essence, Beans Binding (JSR 295) is about keeping two properties 
(typically of two objects) in sync. An additional emphasis is placed 
on the ability to bind to Swing components, and easy integration with 
IDEs such as NetBeans. This project provides the reference implementation.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Documentation

%description javadoc
Javadoc for %{name}.

%prep
%setup -q -c -n %{name}-%{version}
%patch0 -p1
# remove all binary libs
find . -type f \( -iname "*.jar" -o -iname "*.zip" \) -print0 | xargs -t -0 %{__rm} -f

%build
%{ant} dist

%install
%mvn_artifact %{SOURCE1} dist/%{name}.jar
%mvn_install -J dist/javadoc

%files -f .mfiles
%license license.txt
%doc releaseNotes.txt

%files javadoc -f .mfiles-javadoc


%changelog
* Fri May 25 2018 J Szinger <szinger@lanl.gov> - 1.2.1-18.1
- Include pom.xml

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Mar 24 2017 Omair Majid <omajid@redhat.com> - 1.2.1-16
- Add BuildRequires on java-devel
- Resolves RHBZ 1423272

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jun 22 2015 Omair Majid <omajid@redhat.com> - 1.2.1-14
- Update to comply with latest packaging guidelines
- Require javapackges-tools

* Mon Jun 22 2015 Omair Majid <omajid@redhat.com> - 1.2.1-13
- Disable doclint

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Aug 05 2013 Omair Majid <omajid@redhat.com> - 1.2.1-11
- Update to work with latest guidelines
- Fix build dependencies

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Aug 20 2008 Victor G. Vasilyev <victor.vasilyev@sun.com> 1.2.1-3
- Canonical using of %%{__rm}
- The %%{ant} macro is used instead of the ant command
- Redundant export of the $JAVA_HOME environment variable is removed
  in the %%build script

* Wed Aug 13 2008 Victor G. Vasilyev <victor.vasilyev@sun.com> 1.2.1-2
- java-devel & jpackage-utils are added as the build requirements
- jpackage-utils is added as the run-time requirement
- Appropriate values of Group Tags are chosen from the official list
- Redundant run-time requirements for /bin/* utilities are removed
- A ghost symlink for javadoc package is removed
- Documentation added

* Tue Jul 08 2008 Victor G. Vasilyev <victor.vasilyev@sun.com> 1.2.1-1
- Changing for Fedora

* Thu Dec 13 2007 Jaroslav Tulach <jtulach@mandriva.org> 0:1.2.1-1mdv2008.1
+ Revision: 119152
- First package of beansbinding library
- create beansbinding
