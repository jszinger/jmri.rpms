# To Do
* [ ] Create GitHub issues to track this list 

## High priority
* [ ] Unbundle prebuilt binaries
* [ ] Get Jython working
* [ ] Pass self tests
* [ ] jmdns FTBS in F28
* [ ] Create startup scripts in `/usr/bin/`
* [ ] what to do about `lib/security.policy` and
  `lib/test-security.policy`?
* [ ] Are any explicit Requires needed for runtime?

## Medium priority
* [ ] Create Desktop files for GUI apps
* [ ] Verify that ECMAScript works
* [ ] Double-check JMRI BuildRequires with xmvn-depmap
* [ ] Run rpmlint on everthing

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
* [ ] Use ~/.config/JMRI as default
* [ ] AppData
  _[Fedora Packaging Guidelines for AppData Files](https://fedoraproject.org/wiki/Packaging:AppData)_
* [ ] Create a public repository once every thing is done
