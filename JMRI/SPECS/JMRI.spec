# Should unit tests be run?  Defaults to off.  Enable using
# '--with tests'.  Useful to test packaging, but expect failures.
%global with_tests   0%{?_with_tests:1}
%global with_X11tests   0%{?_with_X11tests:1}

# Turn off the brp-python-bytecompile script for jython
%undefine __brp_python_bytecompile

Name:           JMRI
Version:        4.11.7
Release:        1%{?dist}
Summary:        Java Model Railroad Interface

License:        GPLv2
URL:            http://jmri.org/
Source0:        https://github.com/JMRI/JMRI/archive/v%{version}.tar.gz
Source1:        http://rhwood.github.com/paducah/devices/70-jmri.rules
Patch0:         jmri-rm-applejavaextensions.patch
#Patch1:         jmri-debug-scriptengine.patch

BuildArch:      noarch

# Maven and utils
BuildRequires:  maven-local
BuildRequires:  xmvn

BuildRequires:  mvn(org.apache.maven.plugins:maven-install-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-antrun-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-clean-plugin)

# Plugins from pom.xml
BuildRequires:  mvn(org.codehaus.mojo:javacc-maven-plugin)
BuildRequires:  mvn(org.jacoco:jacoco-maven-plugin)
BuildRequires:  mvn(org.codehaus.mojo:build-helper-maven-plugin)
BuildRequires:  mvn(org.codehaus.mojo:buildnumber-maven-plugin) >= 1.4

# TODO: double-check with xmvn-builddep
# Dependencies from pom.xml
BuildRequires:  mvn(com.digi.xbee:xbjlib)
BuildRequires:  mvn(com.fasterxml.jackson.core:jackson-annotations)
BuildRequires:  mvn(com.fasterxml.jackson.core:jackson-core)
BuildRequires:  mvn(com.fasterxml.jackson.core:jackson-databind)
BuildRequires:  mvn(com.google.code.findbugs:annotations)
BuildRequires:  mvn(com.google.code.findbugs:jsr305)
BuildRequires:  mvn(com.networknt:json-schema-validator)
BuildRequires:  mvn(com.sparetimelabs:purejavacomm)
BuildRequires:  mvn(javax.help:javahelp)
BuildRequires:  mvn(javax.vecmath:vecmath)
BuildRequires:  mvn(net.java.dev.jna:jna-platform)
BuildRequires:  mvn(net.java.jinput:jinput)
BuildRequires:  mvn(net.jcip:jcip-annotations)
BuildRequires:  mvn(net.sf.bluecove:bluecove)
BuildRequires:  mvn(net.sourceforge.javacsv:javacsv)
BuildRequires:  mvn(org.apache.commons:commons-text)
BuildRequires:  mvn(org.eclipse.paho:org.eclipse.paho.client.mqttv3)
BuildRequires:  mvn(org.eclipse.jetty.websocket:websocket-api)
BuildRequires:  mvn(org.eclipse.jetty.websocket:websocket-server)
BuildRequires:  mvn(org.eclipse.jetty.websocket:websocket-servlet)
BuildRequires:  mvn(org.hid4java:hid4java) >= 0.5.0
BuildRequires:  mvn(org.jdesktop:beansbinding)
BuildRequires:  mvn(org.jdom:jdom2)
BuildRequires:  mvn(org.jmdns:jmdns) >= 3.5.1
BuildRequires:  mvn(org.jogamp.gluegen:gluegen-rt)
BuildRequires:  mvn(org.jogamp.joal:joal)
BuildRequires:  mvn(org.netbeans.api:org-openide-util-lookup)
BuildRequires:  mvn(org.openlcb:openlcb)
BuildRequires:  mvn(org.python:jython-standalone)
BuildRequires:  mvn(org.slf4j:jul-to-slf4j)
BuildRequires:  mvn(org.slf4j:slf4j-log4j12)
BuildRequires:  mvn(org.usb4java:usb4java-javax)

BuildRequires:  openal-soft-devel

%if %{with_tests}
BuildRequires:  mvn(org.antlr:antlr-runtime)
BuildRequires:  mvn(org.objenesis:objenesis)
%if %{with_X11tests}
BuildRequires:  xorg-x11-server-Xvfb
%endif
# For tests:
#BuildRequires:  mvn(io.cucumber:cucumber-java)
#BuildRequires:  mvn(io.cucumber:cucumber-java8)
#BuildRequires:  mvn(io.cucumber:cucumber-junit)
#BuildRequires:  mvn(io.cucumber:cucumber-picocontainer)
#BuildRequires:  mvn(io.github.bonigarcia:webdrivermanager)
#BuildRequires:  mvn(net.sf.jfcunit:jfcunit)
#BuildRequires:  mvn(org.mockito:mockito-core) >= 2.13.0
#BuildRequires:  mvn(org.netbeans:jemmy) >= 2.3.1.1
#BuildRequires:  mvn(org.seleniumhq.selenium:selenium-java)
%endif


%description
The JMRI project is building tools for model railroad computer
control. We want it to be usable to as many people as possible, so
we're building it in Java to run anywhere, and we're trying to make it
independent of specific hardware systems.

JMRI is intended as a jumping-off point for hobbyists who want to
control their layouts with a computer without having to create an
entire system from scratch.

%package javadoc
Summary:       Javadoc for %{name}

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q
%patch0
#patch1

# Tell jython where to look for its files 
echo 'python.home = %{_datadir}/jython' >> python.properties

# Dependencies not available; testing only
%pom_remove_dep  com.github.spotbugs:spotbugs-annotations
%pom_remove_dep  io.cucumber:cucumber-java
%pom_remove_dep  io.cucumber:cucumber-java8
%pom_remove_dep  io.cucumber:cucumber-junit
%pom_remove_dep  io.cucumber:cucumber-picocontainer
%pom_remove_dep  io.github.bonigarcia:webdrivermanager
%pom_remove_dep  org.seleniumhq.selenium:selenium-java

%pom_add_dep com.google.code.findbugs:annotations:3.0.1
%pom_add_dep com.google.guava:guava:18.0

%if %{with_tests}
%pom_add_dep jakarta-regexp:jakarta-regexp:1.5:test
%pom_add_dep jline:jline:2.13:test
%pom_add_dep net.bytebuddy:byte-buddy:1.7.10:test
%pom_add_dep org.objenesis:objenesis:2.6:test
%pom_add_dep org.antlr:antlr-runtime:3.2:test
%pom_add_dep xerces:xercesImpl:2.11.0:test
%pom_add_dep com.github.jnr:jnr-posix:3.0.41:test
%endif

# Remove Pi4J; needs armhfp (32 bit)
%pom_remove_dep com.pi4j:pi4j-core
rm -rf java/src/jmri/jmrix/pi/
rm -rf java/test/jmri/jmrix/pi/
sed -ipi_bak 's/jmri.jmrix.pi.PackageTest.class,//' \
    java/test/jmri/jmrix/PackageTest.java

# Remove AppleJavaExtensions; MacOS only
%pom_remove_dep com.apple:AppleJavaExtensions
rm -rf java/src/jmri/plaf
rm -rf java/test/jmri/plaf
sed -iplaf.bak 's/jmri.plaf.PackageTest.class,//' \
    java/test/jmri/PackageTest.java

# Known by other names
%pom_change_dep com.digi.xbee:xbee-java-library \
    com.digi.xbee:xbjlib:1.1.1

%pom_change_dep com.github.purejavacomm:purejavacomm \
    com.sparetimelabs:purejavacomm:1.0.1

%pom_change_dep org.eclipse.paho:mqtt-client:0.4.0 \
    org.eclipse.paho:org.eclipse.paho.client.mqttv3:1.0.2

%pom_change_dep org.jogamp.gluegen:gluegen-rt-main \
    org.jogamp.gluegen:gluegen-rt:2.3.2

%pom_change_dep org.jogamp.joal:joal-main org.jogamp.joal:joal:2.3.2


%if %{with_tests}
# TODO: Unbundle these
# Make bundled JARs known to maven
# Violates packaging guidelines, but they aren't available otherwise
xmvn --offline install:install-file -Dfile=lib/byte-buddy-1.7.10.jar

xmvn --offline install:install-file -Dfile=lib/jakarta-regexp-1.5.jar \
    -DgroupId=jakarta-regexp -DartifactId=jakarta-regexp -Dversion=1.5 \
    -Dpackaging=jar

xmvn --offline install:install-file -Dfile=lib/jemmy-2.3.1.1-RELEASE802.jar \
    -DgroupId=org.netbeans.external -DartifactId=jemmy-2.3.1.1 \
    -Dversion=RELEASE802 -Dpackaging=jar

xmvn --offline install:install-file -Dfile=lib/jfcunit.jar \
    -DgroupId=net.sf.jfcunit -DartifactId=jfcunit -Dversion=2.08 \
    -Dpackaging=jar

xmvn --offline install:install-file -Dfile=lib/mockito-core-2.13.0.jar \
    -DgroupId=org.mockito -DartifactId=mockito-core -Dversion=2.13.0 \
    -Dpackaging=jar

#xmvn --offline install:install-file -Dfile=lib/objenesis-2.2.jar \
#    -DgroupId=org.objenesis -DartifactId=objenesis -Dversion=2.2 \
#    -Dpackaging=jar
%endif

# Use guava
sed -i.guava_bak \
    's/org.python.google.common.io.Files/com.google.common.io.Files/' \
    java/src/jmri/jmrit/jython/InputWindow.java 

# Use jline
sed -i.jline_bak 's/org.python.jline.internal.Log/jline.internal.Log/' \
    java/test/jmri/util/JUnitAppender.java

# HidRawEnvironmentPlugin is Windows only
%pom_xpath_remove "pom:properties/pom:jinput.plugins" 
%pom_xpath_remove "pom:systemPropertyVariables/pom:jinput.plugins" 

%if %{with_tests}
# Disable selenium web browser tests
rm -rf java/acceptancetest/
rm -f java/test/jmri/util/web/BrowserFactory.java
rm -f java/test/jmri/RunCucumberTest.java
sed -i.s_bak 's/RunCucumberTest.class,//' java/test/jmri/PackageTest.java

# Disable network tests
rm java/test/jmri/util/zeroconf/ZeroConfServiceEventTest.java
sed -i.jmdns_bak 's/ZeroConfServiceEventTest.class,//' \
    java/test/jmri/util/zeroconf/PackageTest.java

rm java/test/jmri/server/json/schema/JsonSchemaSocketServiceTest.java
sed -i.jssst_bak \
    -e 's/JsonSchemaSocketServiceTest.class//' \
    java/test/jmri/server/json/schema/PackageTest.java
#    -e 's/JsonSchemaHttpServiceTest.class,/JsonSchemaHttpServiceTest.class/' \

%endif

# TODO: unbundle and remove
# What to do about lib/security.policy and lib/test-security.policy?
# rm -rf lib
pushd lib
  # unbundle the stuff we know we've dealt with
  rm antlr-3.4-complete.jar
  rm AppleJavaExtensions.jar
  rm beansbinding-1.2.1.jar
  rm bluecove*.jar
  rm byte-buddy-1.7.10.jar
  #cglib-nodep-2.2.2.jar
  rm -rf checker-framework/
  rm -rf com/ # com/apple...
  rm commons-io-2.6.jar
  rm commons-lang3-3.7.jar
  rm commons-text-1.2.jar
  rm cucumber-*.jar
  #ecj.jar
  #gherkin-4.1.3.jar
  #gherkin-jvm-deps-1.0.4.jar
  rm gluegen-rt.jar
  rm hamcrest-core-1.3.jar
  rm hid4java-0.5.0.jar
  #i18nchecker.jar
  rm jackson-*.jar
  #jacocoant.jar
  rm jakarta-regexp-1.5.jar
  #javacc.jar
  rm javacsv.jar
  #javassist-3.20.0-GA.jar
  #javax.servlet-api-3.1.0.jar
  #jcip-annotations-1.0.jar
  rm jdom*.jar
  rm jemmy-2.3.1.1-RELEASE802.jar
  rm jetty-*.jar
  rm jfcunit.jar
  rm jhall.jar
  rm jhidrawplugin.jar
  rm jinput.jar
  #jlfgr-1_0.jar
  rm jmdns-3.5.1.jar
  rm jna-*.jar
  rm joal.jar
  rm json-schema-validator-0.1.19.jar
  rm jsr305.jar
  rm jul-to-slf4j-1.7.25.jar
  rm junit-4.12.jar
  rm jython-standalone-2.7.0.jar
  rm libusb4java-*.jar
  rm log4j-1.2.17.jar
  #mailapi.jar
  rm mockito-core-2.13.0.jar
  rm mqtt-client-0.4.0.jar
  rm -rf net/
  rm objenesis-2.2.jar
  rm openlcb.jar
  rm -rf org/
  rm org-openide-util-lookup-RELEASE82.jar
  rm pi4j*.jar
  rm picocontainer-2.15.jar
  #plantuml.jar
  rm purejavacomm-1.0.1.jar
  rm README.md
  #rscbundlecheck.jar
  #security.policy
  rm selenium-server-standalone-3.6.0.jar
  rm slf4j-api-1.7.25.jar
  rm slf4j-log4j12-1.7.25.jar
  # smtp.jar
  rm spotbugs-annotations-3.1.1.jar
  #system-rules-1.16.0.jar
  #tag-expressions-1.0.1.jar
  #test-security.policy
  #typetools-0.5.0.jar
  #UmlGraph-5.7.jar
  rm usb4java-1.2.0.jar
  rm usb4java-javax-1.2.0.jar
  rm usb-api-1.0.2.jar
  #vecmath-1.5.2.jar
  rm webdrivermanager-2.0.1.jar
  rm websocket-*.jar
  #xAPlib.jar
  rm xbee-java-library-1.2.0.jar
  rm xercesImpl.jar
rm *.jar

  # Prebuilt shared libraries
  rm -rf linux
  rm -rf macosx
  rm -rf windows
popd

%build
%if %{with_tests}
  echo 'log4j.category.jmri.jmrit.operations.trains.TrainSwitchListsTest=DEBUG' \    >> tests.lcf
  %if %{with_X11tests}
    xvfb-run %mvn_build
  %else
    # run headless tests; need xvfb-run for virtual GUI tests
    export JMRI_OPTIONS=-Djava.awt.headless=true
    %mvn_build
  %endif
%else
  # Skip tests
  %mvn_build -f
%endif


%install
%mvn_install

# TODO: unbundle these
#mkdir -p %{buildroot}%{_jnidir}/%{name}
#cp -a lib/       %{buildroot}%{_jnidir}/%{name}

#TODO: make the installed program find these
mkdir -p %{buildroot}%{_datadir}/%{name}
cp -a help/      %{buildroot}%{_datadir}/%{name}
cp -a jython/    %{buildroot}%{_datadir}/%{name}
cp -a resources/ %{buildroot}%{_datadir}/%{name}
cp -a web/       %{buildroot}%{_datadir}/%{name}
cp -a xml/       %{buildroot}%{_datadir}/%{name}
install -p -m 644 lib/security.policy %{buildroot}%{_datadir}/%{name}/

mkdir -p %{buildroot}%{_udevrulesdir}
install -p -m 644 %{SOURCE1} %{buildroot}%{_udevrulesdir}/


%files -f .mfiles
%license LICENSE.txt
%doc README.md
%{_datadir}/%{name}
#{_jnidir}/#{name}
%{_udevrulesdir}/70-jmri.rules

%files javadoc -f .mfiles-javadoc
%license LICENSE.txt

%changelog
* Sat Jun 23 2018 James Szinger <jszinger@gmail.com> - 4.11.7-1
- Initial package
