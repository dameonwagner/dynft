Name: dynft
Version: 0.9.2
Release: 1
Source0: %{name}_%{version}.tar.gz
License: GNU GPL
Group: Development/Libraries
BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: python3-docutils
BuildRequires: systemd-rpm-macros
Requires: python3-pyyaml
Requires: python3-click
Requires: python3-netaddr
Requires: python3-dns
Requires: python3-nftables
Requires: python3-jsonschema
BuildArch: noarch
Vendor: Dameon Wagner <dameon.wagner@it.ox.ac.uk>
Summary: Dynamic ruleset object management for nftables

%description
dynft is a command-line tool that can be used to dynamically update
nftables ruleset objects.

%prep
%autosetup

%build
python3 setup.py build
rst2man docs/%{name}.rst | gzip > %{name}.1.gz

%install
python3 setup.py install --single-version-externally-managed -O1 --root=%{buildroot} --record=INSTALLED_FILES

%{__mkdir} -m0755 -p %{buildroot}%{_mandir}/man1
%{__mkdir} -m0755 -p %{buildroot}%{_unitdir}
%{__mkdir} -m0755 -p %{buildroot}%{_docdir}/%{name}/docs
%{__mkdir} -m0755 -p %{buildroot}%{_docdir}/%{name}/examples

%{__install} -m0644 -p %{name}.1.gz %{buildroot}%{_mandir}/man1/
%{__install} -m0644 -p debian/%{name}.service %{buildroot}%{_unitdir}/
%{__install} -m0644 -p debian/%{name}.timer %{buildroot}%{_unitdir}/
%{__install} -m0644 -p README.md %{buildroot}%{_docdir}/%{name}/
%{__install} -m0644 -p docs/%{name}.rst %{buildroot}%{_docdir}/%{name}/docs/
%{__install} -m0644 -p examples/nftables_dynamic.yml %{buildroot}%{_docdir}/%{name}/examples/


%clean
rm -rf %{buildroot}

%files -f INSTALLED_FILES
%defattr(-,root,root)
%{_mandir}/man1/%{name}.1.gz
%{_unitdir}/%{name}.service
%{_unitdir}/%{name}.timer
%doc %{_docdir}/%{name}/*

%changelog
* Thu May 07 2026 Dameon Wagner <dameon.wagner@it.ox.ac.uk> - 0.9.2
- Add dynft.spec for building RPM package too.
* Fri Nov 01 2024 Dameon Wagner <dameon.wagner@it.ox.ac.uk> - 0.9.1
- lib/dynft/sets.py:
  - Refactor back to support older versions of python, removing the use
    of both the walrus operator (introduced in python 3.8) and the match
    statement (introduced in python 3.10).  This is necessary as we'll
    need to be supporting both RHEL8 (which provides 3.6.8) and RHEL9
    (which provides 3.9.18, at the time of commiting).
Fri Nov 01 2024 Dameon Wagner <dameon.wagner@it.ox.ac.uk> - 0.9.0
- Initial release
