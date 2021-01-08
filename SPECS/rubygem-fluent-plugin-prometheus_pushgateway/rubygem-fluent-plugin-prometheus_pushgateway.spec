%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name fluent-plugin-prometheus_pushgateway
Summary:        A fluent plugin for prometheus pushgateway
Name:           rubygem-fluent-plugin-prometheus_pushgateway
Version:        0.0.2
Release:        1%{?dist}
License:        Apache 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
BuildRequires:  ruby >= 2.3.0
Requires:       rubygem-fluent-plugin-prometheus < 2.0.0
Requires:       rubygem-fluent-plugin-prometheus >= 1.7.0

%description
This is Fluentd's plugin for sending data collected by
fluent-plugin-prometheus plugin to Pushgateway.

%prep
%setup -q -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%license %{gemdir}/gems/%{gem_name}-%{version}/LICENSE
%{gemdir}

%changelog
