# This is the last version without android support, which requires
# non-free software to build.

Name:           XBeeJavaLibrary
Version:        1.1.1
Release:        1%{?dist}
Summary:        XBee Java Library

License:        MPL 2
URL:            https://github.com/digidotcom/XBeeJavaLibrary
Source0:        https://github.com/digidotcom/%{name}/archive/v%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  maven-local

BuildRequires:  mvn(org.rxtx:rxtx)
BuildRequires:  mvn(org.slf4j:slf4j-api)
BuildRequires:  mvn(org.slf4j:slf4j-jdk14)

# Testing
BuildRequires:  mvn(org.mockito:mockito-all)
BuildRequires:  mvn(org.powermock:powermock-module-junit4)
BuildRequires:  mvn(org.powermock:powermock-api-mockito)


%description
This project contains the source code of the XBee Java Library, an
easy-to-use API developed in Java that allows you to interact with
Digi International's XBee radio frequency (RF) modules. This source
has been contributed by Digi International.

%package        javadoc
Summary:        Javadoc for %{name}

%description javadoc
This package contains the API documentation for %{name}.


%prep 
%autosetup -n %{name}-%{version}

%pom_remove_plugin :maven-dependency-plugin library/pom.xml
%pom_remove_plugin :maven-source-plugin library/pom.xml

%pom_disable_module distribution
%pom_disable_module examples/communication/ReceiveModemStatusSample
%pom_disable_module examples/communication/ReceiveDataSample
%pom_disable_module examples/communication/ReceiveDataPollingSample
%pom_disable_module examples/communication/SendBroadcastDataSample
%pom_disable_module examples/communication/SendDataAsyncSample
%pom_disable_module examples/communication/SendDataSample
%pom_disable_module examples/communication/explicit/ReceiveExplicitDataPollingSample
%pom_disable_module examples/communication/explicit/ReceiveExplicitDataSample
%pom_disable_module examples/communication/explicit/SendBroadcastExplicitDataSample
%pom_disable_module examples/communication/explicit/SendExplicitDataAsyncSample
%pom_disable_module examples/communication/explicit/SendExplicitDataSample
%pom_disable_module examples/configuration/ManageCommonParametersSample
%pom_disable_module examples/configuration/ResetModuleSample
%pom_disable_module examples/configuration/SetAndGetParametersSample
%pom_disable_module examples/io/IOSamplingSample
%pom_disable_module examples/io/LocalADCSample
%pom_disable_module examples/io/LocalDIOSample
%pom_disable_module examples/io/RemoteADCSample
%pom_disable_module examples/io/RemoteDIOSample
%pom_disable_module examples/network/DiscoverDevicesSample

# Included in rxtx
%pom_remove_dep org.rxtx:rxtx-native


%build
%mvn_build

%install
%mvn_install

%files -f .mfiles
%license LICENSE.txt
%doc README.md release_notes.txt

%files javadoc -f .mfiles-javadoc
%license LICENSE.txt


%changelog
* Thu May 24 2018 J Szinger <szinger@lanl.gov> - 1.1.1-1
- Initial package
