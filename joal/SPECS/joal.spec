Name:           joal
Version:        2.3.2
Release:        1%{?dist}
%global src_name %{name}-v%{version}
Summary:        Java bindings for OpenAL API

License:        BSD
URL:            http://jogamp.org/
Source0:        http://jogamp.org/deployment/v%{version}/archive/Sources/%{src_name}.tar.xz
Source1:        http://central.maven.org/maven2/org/jogamp/%{name}/%{name}/%{version}/%{name}-%{version}.pom

%global debug_package %{nil}

BuildRequires:  ant
BuildRequires:  javapackages-local
BuildRequires:  openal-soft-devel
BuildRequires:  gluegen2-devel = %{version}

Requires:       gluegen2 = %{version}

%description
The JOAL Project hosts a reference implementation of the Java bindings
for OpenAL API, and is designed to provide hardware-supported 3D
spatialized audio for games written in Java.

%package        javadoc
Summary:        Javadoc for %{name}

%description javadoc
This package contains the API documentation for %{name}.


%prep
%autosetup -n %{src_name}

# Remove bundled dependencies
rm -fr make/lib

# Restore the gluegen2 source code from gluegen2-devel
rm -fr ../gluegen
cp -rdf %{_datadir}/gluegen2 ../gluegen

# Fix wrong-script-end-of-line-encoding
rm make/scripts/*.bat

# Fix spurious-executable-perm
chmod -x LICENSE.txt

# Fix non-executable-script
find make/scripts -type f -name "*.sh" -exec chmod +x {} +

# Fix script-without-shebang
find make/scripts -type f -name "*.sh" -exec sed -i -e '1i#!/bin/sh' {} +

# git executable should not be used, use true (to avoid checkout) instead
sed -i 's/executable="git"/executable="true"/' make/build.xml


%build
cd make

# As we never cross-compile this package, the SDK root is always /
export TARGET_PLATFORM_ROOT=/

xargs -t ant <<EOF
 -verbose
 -Dc.compiler.debug=true
 -Djavacdebug=true
 -Djavac.memorymax=512m
 -Dcommon.gluegen.build.done=true
 
 -Dantlr.jar=%{_javadir}/antlr.jar 
 -Djunit.jar=%{_javadir}/junit.jar 
 -Dant.jar=%{_javadir}/ant.jar 
 -Dant-junit.jar=%{_javadir}/ant/ant-junit.jar 
 -Dgluegen.jar=%{_javadir}/gluegen2.jar 
 -Dgluegen-rt.jar=%{_jnidir}/gluegen2-rt.jar 
 -Dswt.jar=%{_jnidir}/swt.jar 
 -Djavadoc.link=%{_javadocdir}/java 
 -Dgluegen.link=%{_javadocdir}/gluegen2 

 joal.build tag.build javadoc.public
EOF


%install
%mvn_artifact %{SOURCE1} build/jar/%{name}.jar
%mvn_install -J build/javadoc

mkdir -p  %{buildroot}%{_jnidir}
cp -a build/jar/%{name}-natives-*.jar %{buildroot}%{_jnidir}/


%files -f .mfiles
%license LICENSE.txt
%doc README.txt
%{_jnidir}/*.jar

%files javadoc -f .mfiles-javadoc
%license LICENSE.txt


%changelog
* Wed May 23 2018 J Szinger <jszinger>
- initial package
