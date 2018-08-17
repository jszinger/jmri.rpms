# To Do
* [ ] Create GitHub issues to track this list 

## High priority
* [x] Unbundle prebuilt binaries
* [x] jmdns FTBS in F28
* [x] Get Jython working
  - update python.properties python.home
* [ ] Pass self tests
```
[ERROR] Failures: 
[ERROR]   TrainSwitchListsTest.testSwitchListTrainTurn:235 confirm number of lines in switch list expected:<32> but was:<31>
```
* [x] Create startup scripts in `/usr/bin/`
* [x] what to do about `lib/security.policy` and
  `lib/test-security.policy`?
  - `./scripts/AppScriptTemplate:OPTIONS="${OPTIONS} -Djava.security.policy=${LIBDIR}/security.policy"`
  - install to %{_datadir}

* [x] Are any explicit Requires needed for runtime?
  - antlr32-java for jython?
  - openal-soft

## Medium priority
* [ ] Create Desktop files for GUI apps
  - See [Pi_Icons.tar.gz](http://jmri.org/install/support/Pi_Icons.tar.gz)
* [ ] Verify that ECMAScript works
* [x] Double-check JMRI BuildRequires with xmvn-depmap
* [ ] Run rpmlint on everthing
* [ ] Unbundle Node.js (NPM) packages: rm -rf web/app/node_modules

## Low priority
* [ ] Create an unbundled branch of JMRI
* [ ] Does
  _[Packaging:Web Assets](https://fedoraproject.org/wiki/Packaging:Web_Assets)_
  apply? 
* [ ] Pi4J: Can it be built for x86 even it it doesn't run? Or can it
  be built for arm and included as a weak dependency?
  ```
  BuildArch: noarch
  # List the arches that the dependent package builds on below
  ExclusiveArch: %{ix86} %{arm} x86_64 noarch
  ```
  - I think it uses the deprecates syssf GPIO interface not available
  in Fedora/CentOS.
  
* [ ] Use ~/.config/JMRI as default
* [ ] AppData
  _[Fedora Packaging Guidelines for AppData Files](https://fedoraproject.org/wiki/Packaging:AppData)_
* [ ] Create a public repository once every thing is done

