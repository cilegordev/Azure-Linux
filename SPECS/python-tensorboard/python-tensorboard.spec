%global pypi_name tensorboard
%global _description %{expand:
TensorBoard is a suite of web applications for inspecting and understanding your TensorFlow runs and graphs}
%define _enable_debug_package 0
%global debug_package %{nil}

Summary:        TensorBoard is a suite of web applications for inspecting and understanding your TensorFlow runs and graphs
Name:           python-%{pypi_name}
Version:        2.16.2
Release:        6%{?dist}
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://github.com/tensorflow/tensorboard
# This source also contains the dependencies required for building tensorboard
Source0:        %{_distro_sources_url}/%{name}-%{version}.tar.gz#/%{name}-%{version}.tar.gz
Patch0:         0000-Use-system-package.patch
Patch1:         CVE-2024-43788.patch
Patch2:         CVE-2024-43796.patch
Patch3:         CVE-2024-45590.patch

BuildRequires:  bazel
BuildRequires:  build-essential
BuildRequires:  gcc
BuildRequires:  git
BuildRequires:  python3-absl-py
BuildRequires:  python3-numpy
BuildRequires:  python3-pip
BuildRequires:  python3-protobuf
BuildRequires:  python3-setuptools
BuildRequires:  python3-six
BuildRequires:  python3-virtualenv
BuildRequires:  python3-wheel
BuildRequires:  python3-werkzeug
BuildRequires:  which
BuildRequires:  zlib
ExclusiveArch:  x86_64


%description %{_description}

%package -n python3-%{pypi_name}
Summary:        %{summary}
Requires:   python3-absl-py
Requires:   python3-google-auth-oauthlib
Requires:   python3-google-auth
Requires:   python3-grpcio
Requires:   python3-markdown
Requires:   python3-numpy
Requires:   python3-protobuf
Requires:   python3-requests
Requires:   python3-setuptools
Requires:   python3-werkzeug
Requires:   python3-wheel


%description -n python3-%{pypi_name} %{_description}

%package -n python3-%{pypi_name}-data-server
Summary:        %{summary}


%description -n python3-%{pypi_name}-data-server %{_description}

%prep
%autosetup -p1 -n tensorboard-%{version}
rm -rf tensorboard-%{version}/tb_tmp/b069b9e9814ff76ffa6219506d1f1e79/external/npm

%build

ln -s %{_bindir}/python3 %{_bindir}/python
#tensorboard-data-server
pushd tensorboard/data/server/pip_package
python3 setup.py -q bdist_wheel
popd
mkdir -p pyproject-wheeldir/ && cp tensorboard/data/server/pip_package/dist/*.whl pyproject-wheeldir/

#tensorboard built using bazel
#tb_tmp contains all the dependencies for bazel build
bazel --batch --output_user_root=./tb_tmp build //tensorboard/pip_package:build_pip_package
bazel-bin/tensorboard/pip_package/build_pip_package .
mv %{pypi_name}-*.whl pyproject-wheeldir/

%install
%{pyproject_install}


%files -n python3-%{pypi_name}
%doc README.md
%license LICENSE
%{_bindir}/tensorboard
%{python3_sitelib}/tensorboard
%{python3_sitelib}/tensorboard-*

%files -n python3-%{pypi_name}-data-server
%doc README.md
%license LICENSE
%{python3_sitelib}/tensorboard_data_server*

%changelog
* Tue Nov 19 2024 Bala <balakumaran.kannan@microsoft.com> - 2.16.2-6
- Remove npm directory before building to make sure as no nodejs vulnerability is getting through
- It is done while fixing CVE-2024-21538

* Thu Sep 26 09 2024 Rohit Rawat <rohitrawat@microsoft.com> - 2.16.2-5
- Patch to fix CVE-2024-45590

* Wed Sep 25 09 2024 Rohit Rawat <rohitrawat@microsoft.com> - 2.16.2-4
- Patch to fix CVE-2024-43796

* Mon Sep 02 2024 Rohit Rawat <rohitrawat@microsoft.com> - 2.16.2-3
- Patch to fix CVE-2024-43788

* Thu May 30 2024 Neha Agarwal <nehaagarwal@microsoft.com> - 2.16.2-2
- Bump release to build with new python-werkzeug to fix CVE-2024-34069

* Thu Apr 25 2024 Riken Maharjan <rmaharjan@microsoft.com> - 2.16.2-1
- Upgrade tensorboard to 2.16.2.

* Tue Apr 23 2024 Andrew Phelps <anphel@microsoft.com> - 2.11.0-4
- Remove missing requirements `python3-tf-nightly` and `python3-tensorflow-estimator`

* Fri Feb 16 2024 Andrew Phelps <anphel@microsoft.com> - 2.11.0-3
- Relax version requirements

* Tue Aug 01 2023 Riken Maharjan <rmaharjan@microsoft.com> - 2.11.0-2
- Remove bazel version.

* Mon Dec 19 2022 Riken Maharjan <rmaharjan@microsoft.com> - 2.11.0-1
- Original version for CBL-Mariner. License Verified.
