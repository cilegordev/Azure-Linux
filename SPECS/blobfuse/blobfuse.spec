Summary:        FUSE adapter - Azure Storage Blobs
Name:           blobfuse
Version:        1.4.2
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications/Tools
URL:            https://github.com/Azure/azure-storage-fuse/
Source0:        https://github.com/Azure/azure-storage-fuse/archive/%{name}-%{version}.tar.gz
BuildRequires:  boost-devel
BuildRequires:  boost-static
BuildRequires:  cmake
BuildRequires:  curl-devel
BuildRequires:  fuse-devel
BuildRequires:  gcc
BuildRequires:  gnutls
BuildRequires:  gnutls-devel
BuildRequires:  golang
BuildRequires:  libgcrypt-devel
BuildRequires:  make
BuildRequires:  pkg-config
BuildRequires:  util-linux-devel
Requires:       fuse

%description
FUSE adapter - Azure Storage Blobs

%prep
%autosetup -n azure-storage-fuse-blobfuse-%{version}

%build
./build.sh

%install
mkdir -p %{buildroot}%{_bindir}
install -p -m 755 build/blobfuse %{buildroot}%{_bindir}/

%files
%defattr(-,root,root,-)
%license LICENSE
%{_bindir}/blobfuse

%changelog
* Mon Nov 29 2021 Thomas Crain <thcrain@microsoft.com> - 1.4.2-1
- Upgrade to latest upstream version
- Remove %%clean section

* Fri Nov 13 2021 Andrew Phelps <anphel@microsoft.com> - 1.3.6-5
- Fix gcc11 compilation errors

* Tue Sep 21 2021 Henry Li <lihl@microsoft.com> - 1.3.6-4
- Remove util-linux-libs from BR 

* Tue Jun 08 2021 Henry Beberman <henry.beberman@microsoft.com> - 1.3.6-3
- Increment release to force republishing using golang 1.15.13.

* Mon Apr 26 2021 Nicolas Guibourge <nicolasg@microsoft.com> - 1.3.6-2
- Increment release to force republishing using golang 1.15.11.

* Tue Feb 02 2021 Henry Beberman <henry.beberman@microsoft.com> - 1.3.6-1
- Add blobfuse spec
- License verified
- Original version for CBL-Mariner
