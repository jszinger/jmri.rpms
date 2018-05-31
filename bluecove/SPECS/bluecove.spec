%define gitdate  20140321
%define snapshot 64
Name:           bluecove
Version:        2.1.1
Release:        1.%{gitdate}snap%{snapshot}%{?dist}
Summary:        Implementation of JSR-82 Java Bluetooth API

License:        ASL 2.0 and LGPLv2+ and GPLv3+
URL:            https://github.com/hcarver/bluecove
Source0:        https://github.com/hcarver/bluecove/archive/master.zip

BuildRequires:  ant
BuildRequires:  maven-local
BuildRequires:  mvn(org.apache.maven.plugins:maven-source-plugin)
BuildRequires:  mvn(org.codehaus.mojo:native-maven-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-antrun-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-assembly-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-dependency-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-clean-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-install-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-deploy-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-site-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-release-plugin)

BuildRequires:  mvn(net.sf.jour:jour-instrument)

BuildRequires:  bluez-libs-devel
BuildRequires:  libmatthew-java
BuildRequires:  dbus-java >= 2.5.1

Requires:       dbus-java
Requires:       libmatthew-java

%description
BlueCove is a JSR-82 implementation on Java Standard Edition (J2SE) that 
currently interfaces with the Mac OS X, WIDCOMM, BlueSoleil and Microsoft 
Bluetooth stack. Originally developed by Intel Research and currently 
maintained by volunteers.

This package adds additional support for:
- Linux with BlueZ (bluecove-gpl)
- Linux with BlueZ using DBUS for device discovery (bluecove-bluez)
- Emulator for use with MicroEmulator (bluecove-emu)

%package        javadoc
Summary:        Javadoc for %{name}

%description javadoc
This package contains the API documentation for %{name}.


%prep
%autosetup -n bluecove-master

%pom_disable_module bluecove-emu-gui
%pom_disable_module bluecove-tests
%pom_disable_module bluecove-android2
%pom_disable_module bluecove-examples

xmvn --offline install:install-file \
    -Dfile=%{_javadir}/dbus-java/dbus.jar \
    -DgroupId=org.freedesktop.dbus \
    -DartifactId=dbus \
    -Dversion=2.7 \
    -Dpackaging=jar

%pom_remove_dep org.freedesktop.dbus:dbus:2.5.1-SNAPSHOT bluecove-bluez
%pom_add_dep org.freedesktop.dbus:dbus:2.7 bluecove-bluez "<scope>provided</scope>"

xmvn --offline install:install-file \
    -Dfile=%{_jnidir}/unix-0.5.jar \
    -DgroupId=cx.ath.matthew \
    -DartifactId=unix \
    -Dversion=0.5.0 \
    -Dpackaging=jar

%pom_add_dep cx.ath.matthew:unix:0.5.0 bluecove-bluez "<scope>provided</scope>"

%build
cd bluecove
%mvn_build
cd ..

# build bluecove-gpl
cd bluecove-gpl
ant jar -Dproduct_version=%{version}-SNAPSHOT \
        -Dbluecove_main_dist_dir=../bluecove/target \
        -Dbluecove.native.resources.skip=true \
        -Dbluecove.native.linker.options="" \
        -DCC_compiler_options="%{optflags} -fPIC -fno-stack-protector"
cd ..

# build bluecove-bluez
cd bluecove-bluez
ant jar -Dproduct_version=%{version}-SNAPSHOT \
        -Dbluecove_main_dist_dir=../bluecove/target \
        -Ddbus_java_jar=%{_javadir}/dbus-java/dbus.jar \
        -Dlibmatthew_java_debug_jar=%{_jnidir}/unix.jar \
        -Dbluecove.native.resources.skip=true \
        -Dbluecove.native.linker.options="" \
        -DCC_compiler_options="%{optflags} -fPIC -fno-stack-protector"
cd ..

%mvn_build

%install
%mvn_install

mkdir -p %{buildroot}%{_libdir}/%{name}/%{version}-SNAPSHOT
cp -p bluecove-gpl/target/*.so %{buildroot}%{_libdir}/%{name}/%{version}-SNAPSHOT
cp -p bluecove-bluez/target/*.so %{buildroot}%{_libdir}/%{name}/%{version}-SNAPSHOT

cp -p bluecove/LICENSE.txt bluecove/README.txt bluecove/stacks.txt bluecove/todo.txt .
cp -p bluecove-gpl/LICENSE.txt LICENSE-gpl.txt
cp -p bluecove-gpl/AUTHORS.txt AUTHORS-gpl.txt

%files -f .mfiles
%{_libdir}/%{name}
%license LICENSE.txt LICENSE-gpl.txt
%doc AUTHORS.txt README.txt stacks.txt todo.txt AUTHORS-gpl.txt

%files javadoc -f .mfiles-javadoc
%license LICENSE.txt LICENSE-gpl.txt

%changelog
* Tue Mar 27 2018 J Szinger
- Repackage with maven
