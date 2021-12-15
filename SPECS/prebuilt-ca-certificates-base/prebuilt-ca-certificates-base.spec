# When updating, "Version" AND "Release" tags must be updated in the "ca-certificates" package as well.
Summary:        Prebuilt version of ca-certificates-base package.
Name:           prebuilt-ca-certificates-base
Version:        20200720
Release:        20%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Security
URL:            https://hg.mozilla.org
BuildArch:      noarch

BuildRequires:  ca-certificates-base = %{version}-%{release}

Conflicts:      prebuilt-ca-certificates

%description
Prebuilt version of the ca-certificates-base package with no runtime dependencies.

%prep -q

# Remove 'ca-certificates', if present. We don't want them
# to get mixed into the bundle provided by 'ca-certificates-base'.
if rpm -q ca-certificates &>/dev/null; then rpm -e --nodeps ca-certificates; fi

%build

%install

mkdir -p %{buildroot}%{_sysconfdir}/pki/{tls/certs,ca-trust/extracted,java}

cp %{_sysconfdir}/pki/tls/cert.pem %{buildroot}%{_sysconfdir}/pki/tls/
cp -r %{_sysconfdir}/pki/tls/certs/* %{buildroot}%{_sysconfdir}/pki/tls/certs/
cp -r %{_sysconfdir}/pki/ca-trust/extracted/* %{buildroot}%{_sysconfdir}/pki/ca-trust/extracted/
cp %{_sysconfdir}/pki/java/cacerts %{buildroot}%{_sysconfdir}/pki/java/

find %{buildroot} -name README -delete

%files
# Base certs bundle file with trust
%{_sysconfdir}/pki/tls/cert.pem
%{_sysconfdir}/pki/tls/certs/*
%{_sysconfdir}/pki/ca-trust/extracted/*
%{_sysconfdir}/pki/java/cacerts

%changelog
* Tue Oct 12 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 20200720-20
- Removing conflicts with 'ca-certificates-shared'.
- License verified.

* Thu Sep 23 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 20200720-19
- Making 'Release' match with 'ca-certificates'.
- Removing legacy components.
- Adding a conflict with a new prebuilt set of certs.

* Mon Sep 13 2021 CBL-Mariner Service Account <cblmargh@microsoft.com> - 20200720-18
- Making 'Release' match with 'ca-certificates'.

* Fri Aug 20 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 20200720-17
- Making 'Release' match with 'ca-certificates'.

* Fri Aug 20 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 20200720-16
- Making 'Release' match with 'ca-certificates'.
- No longer have to remove 'ca-bundle.legacy.crt' and 'ca-legacy.conf' - gone from 'ca-certificates'.

* Wed Jul 07 2021 CBL-Mariner Service Account <cblmargh@microsoft.com> - 20200720-15
- Making 'Release' match with 'ca-certificates'.

* Thu Jun 03 2021 CBL-Mariner Service Account <cblmargh@microsoft.com> - 20200720-14
- Making 'Release' match with 'ca-certificates'.

* Fri Mar 12 2021 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 20200720-13
- Making 'Release' match with 'ca-certificates'.

* Sat Mar 06 2021 CBL-Mariner Servicing Account <clbmargh@microsoft.com> - 20200720-12
- Making 'Release' match with 'ca-certificates'.

* Mon Feb 08 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 20200720-11
- Making 'Release' match with 'ca-certificates'.

* Tue Jan 12 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 20200720-10
- Making 'Release' match with 'ca-certificates'.

* Wed Dec 2 2020 Mateusz Malisz <mamalisz@microsoft.com> - 20200720-1
- Original version for CBL-Mariner
