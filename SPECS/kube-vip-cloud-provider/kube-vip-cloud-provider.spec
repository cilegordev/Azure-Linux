Summary:        The Kube-Vip cloud provider functions as a general-purpose cloud provider for on-premises bare-metal or virtualized setups
Name:           kube-vip-cloud-provider
Version:        0.0.2
Release:        2%{?dist}
License:        ASL 2.0
URL:            https://github.com/kube-vip/kube-vip-cloud-provider
Group:          Applications/Text
Vendor:         Microsoft
Distribution:   Mariner
Source0:        https://github.com/kube-vip/%{name}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
#Note that the source file should be renamed to the format {name}-%{version}.tar.gz

# Steps to manually create the vendor tarball, no download link.
# We're using pre-populated Go modules from this tarball, since network is disabled during build time.
# Adding the vendor folder and creating a tarball
# How to re-build this file:
# 1. wget https://github.com/kube-vip/%%{name}/archive/refs/tags/v%%{version}tar.gz -O %%{name}-%%{version}.tar.gz
# 2. tar -xf %%{name}-%%{version}.tar.gz
# 3. cd %%{name}-%%{version}
# 4. go mod vendor
# 5. tar -cf %%{name}-%%{version}-vendor.tar.gz vendor

Source1: %{name}-%{version}-vendor.tar.gz

BuildRequires: golang

%description
The Kube-Vip cloud provider functions as a general-purpose cloud provider for on-premises bare-metal or virtualized setups. 

%prep
%setup -q
tar -xvf %{SOURCE1}

%build 
go build -mod=vendor

%install
install -d %{buildroot}%{_bindir}
install kube-vip-cloud-provider %{buildroot}%{_bindir}/kube-vip-cloud-provider

%files
%{_bindir}/kube-vip-cloud-provider

%changelog
* Tue Nov 01 2022 Olivia Crain <oliviacrain@microsoft.com> - 0.0.2-2
- Bump release to rebuild with go 1.18.8

* Tue Sep 06 2022 Vinayak Gupta <guptavinayak@microsoft.com> - 0.0.2-1
- Original version for CBL-Mariner
- License Verified
