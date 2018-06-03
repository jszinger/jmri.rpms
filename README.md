# RPM Packaging of [JMRI](http://jmri.org/)

The goal of this project is to package JMRI in rpm format.  This
includes JMRI itself along with the dependencies that are not
currently packaged.  A couple of dependencies are updates or patches of
existing packages.

Targets [Fedora](https://start.fedoraproject.org/) 27/28.  Maven is
used for the build since Fedora has good packaging support for maven
projects.  See the
_[Java Packaging HOWTO](https://fedora-java.github.io/howto/latest/)_.

My intent is to comply with the
_[Fedora Packaging Guidelines](https://fedoraproject.org/wiki/Packaging:Guidelines#Packages_which_are_not_useful_without_external_bits)_
and the
_[Fedora Packaging Guidelines for Java](https://fedoraproject.org/wiki/Packaging:Java)_.
Much of the effort, not yet complete, is the unbundling of prebuilt
content.

Each package is in its own directory with an RPM build hierarchy.

## Status
Work in progress. Highly experimental and currently broken.

Should compile and pass most unit tests.

See [ToDo.md](ToDo.md).

## Get Sources
spectool -g to download the SOURCES
```shell
spectool -g -C ../SOURCES/ usb4java.spec 
```

get all SOURCES
```shell
for d in *; do mkdir $d/SOURCES; popd; done
for d in *; do
    pushd $d/SPECS
    spectool -g -C ../SOURCES/ *.spec
    popd
done
```

## Create SRPMS
rpmbuild -bs to create src.rpms
```shell
rpmbuild -D'_topdir ..' -bs usb4java.spec 
```

build all SRPMS
```shell
for d in * ;do
    pushd $d/SPECS
    rpmbuild -D'_topdir ..' -bs *.spec
    popd
done
```

## Build RPMS
mockchain to build everything
```shell
mockchain -r fedora-27-x86_64 -l /usr/local/mockchain/ --recurse \
    */SRPMS/*.src.rpm
mockchain -r fedora-28-x86_64 -l /usr/local/mockchain/ --recurse \
    */SRPMS/*.src.rpm
```

after initial build, save the build order from `mockchain` output and
```shell
mockchain -r fedora-27-x86_64 -l /usr/local/mockchain/ --recurse \
    `cat buildorder`
```

The JMRI unit tests are flakey.
