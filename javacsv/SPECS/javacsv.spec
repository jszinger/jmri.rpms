Name:           javacsv
Version:        2.1
Release:        1%{?dist}
Summary:        Java library for reading and writing CSV and plain delimited text files

License:        LGPLv2
URL:            https://www.csvreader.com/java_csv.php
Source0:        http://downloads.sourceforge.net/%{name}/JavaCsv/JavaCsv%%202.1/%{name}%{version}.zip
Source1:        https://www.gnu.org/licenses/old-licenses/lgpl-2.1.txt
BuildArch:      noarch

BuildRequires: ant
BuildRequires: javapackages-local

%description
Java CSV is a small fast open source Java library for reading and
writing CSV and plain delimited text files. All kinds of CSV files can
be handled, text qualified, Excel formatted, etc.

Features:
    * Handles column delimiters within data using quoted text qualifiers.
    * Handles record delimiters within data using quoted text qualifiers.


%package        javadoc
Summary:        Javadoc for %{name}

%description javadoc
This package contains the API documentation for %{name}.

%prep
%autosetup -c
cp -p %{SOURCE1} .
# Delete prebuild content
rm javacsv.jar
rm -rf doc

%build
ant -buildfile build.xml
ant -buildfile javadoc.xml

%install
%mvn_artifact net.sourceforge.%{name}:%{name}:%{version} %{name}.jar

%mvn_install -J doc/


%files -f .mfiles
%dir %{_javadir}/%{name}
%license lgpl-2.1.txt

%files javadoc -f .mfiles-javadoc
%license lgpl-2.1.txt

%changelog
* Fri May 18 2018 J Szinger <szinger>
- Inital package
