#
# spec file for package envoy-proxy
#
# Copyright (c) 2021 SUSE LLC
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via https://bugs.opensuse.org/
#

# Some external dependencies of envoy have no build-ids and thus will cause 
# errors when performing rpm stripping, and thus disable it
%global __strip /bin/true
%define _dwz_low_mem_die_limit  20000000
%define _dwz_max_die_limit     100000000
%define src_install_dir %{_prefix}/src/%{name}
Summary:        L7 proxy and communication bus
Name:           envoy
Version:        1.21.0
Release:        1%{?dist}
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://www.envoyproxy.io/
#Source0:       https://github.com/envoyproxy/envoy/archive/refs/tags/v%{version}.tar.gz
Source0:        %{name}-%{version}.tar.gz
# Below is a manually created tarball, no download link.
# We're using pre-populated external dependencies from this tarball, since network is disabled during build time.
#   1. wget https://github.com/envoyproxy/envoy/archive/refs/tags/v%{version}.tar.gz -o %%{name}-%%{version}.tar.gz
#   2. tar -xf %%{name}-%%{version}.tar.gz
#   3. cd %%{name}-%%{version}
#   4. patch -p1 < 0001-build-Use-Go-from-host.patch
#   5. mkdir -p BAZEL_CACHE
#   6. bazel fetch --repository_cache=BAZEL_CACHE //...
#   7. tar  --sort=name \
#           --mtime="2021-04-26 00:00Z" \
#           --owner=0 --group=0 --numeric-owner \
#           --pax-option=exthdr.name=%d/PaxHeaders/%f,delete=atime,delete=ctime \
#           -cf %%{name}-%%{version}-vendor.tar.gz BAZEL_CACHE
Source1:        %{name}-%{version}-vendor.tar.gz
# Bazel fetch is not capable of prefetching and caching all external dependencies, thus
# introduce this second source to satisfy the dependency requirements. See this link for more
# detailed explanation: https://github.com/bazelbuild/bazel/issues/5175
# Below is a manually created tarball, no download link.
# We're using pre-populated external dependencies from this tarball, since network is disabled during build time.
#   1. wget https://github.com/envoyproxy/envoy/archive/refs/tags/v%{version}.tar.gz -o %%{name}-%%{version}.tar.gz
#   2. tar -xf %%{name}-%%{version}.tar.gz
#   3. cd %%{name}-%%{version}
#   4. patch -p1 < 0001-build-Use-Go-from-host.patch
#   5. mkdir -p BAZEL_CACHE
#   6. bazel fetch --repository_cache=BAZEL_CACHE //source/exe:envoy
#   7. cd $(bazel info output_base)
#   8. tar  --sort=name \
#           --mtime="2021-04-26 00:00Z" \
#           --owner=0 --group=0 --numeric-owner \
#           --pax-option=exthdr.name=%d/PaxHeaders/%f,delete=atime,delete=ctime \
#           -cf %%{name}-%%{version}-gocache.tar.gz external
Source2:        %{name}-%{version}-gocache.tar.gz
Source100:      %{name}-rpmlintrc
Patch0:         0001-build-Use-Go-from-host.patch
Patch1:         0002-disable-wee8-mismatched-new-delete-warning.patch
BuildRequires:  bazel
BuildRequires:  bazel-workspaces
BuildRequires:  c-ares-devel
BuildRequires:  cmake
BuildRequires:  fdupes
BuildRequires:  fmt-devel
BuildRequires:  gcc-c++
BuildRequires:  gcovr
BuildRequires:  git
BuildRequires:  golang >= 1.12
BuildRequires:  golang-packaging
BuildRequires:  libcurl-devel
BuildRequires:  libnghttp2-devel
BuildRequires:  libtool
BuildRequires:  nghttp2-devel
BuildRequires:  ninja-build
BuildRequires:  pkg-config
BuildRequires:  python3
BuildRequires:  python3-jinja2
BuildRequires:  python3-markupsafe
BuildRequires:  zlib-devel
BuildRequires:  pkgconfig(openssl)
ExcludeArch:    %{ix86}

%description
Envoy is an L7 proxy and communication bus designed for large modern service
oriented architectures.

%package source
Summary:        Source code of bazel-rules-cc

%description source
Envoy is an L7 proxy and communication bus designed for large modern service
oriented architectures.

This package contains source code of Envoy.

%prep
%autosetup -p1

# Prevent bundling curl, nghttp2 and zlib, don't use foreign_cc on them.
sed -i \
    -e "s|@envoy//bazel/foreign_cc:curl|@com_github_curl//:curl|" \
    -e 's|patches = \["@envoy//bazel/foreign_cc:nghttp2.patch"\]|# patches = \["@envoy//bazel/foreign_cc:nghttp2.patch"\]|g' \
    -e "s|@envoy//bazel/foreign_cc:nghttp2|@com_github_nghttp2_nghttp2//:all|" \
    -e "s|@envoy//bazel/foreign_cc:zlib|@zlib//:zlib|" \
    bazel/repositories.bzl

# Remove the script which requires /usr/bin/bash.exe and is meant to work only
# on Windows.
rm ci/windows_ci_steps.sh

# AUTOGENERATED BY obs-service-bazel_repositories
%setup -q -T -D -a 1
%setup -q -T -D -a 2
# END obs-service-bazel_repositories

%build
git config --global user.email you@example.com
git config --global user.name "Your Name"
git init
git add .
GIT_AUTHOR_DATE=2000-01-01T01:01:01 GIT_COMMITTER_DATE=2000-01-01T01:01:01 \
git commit -m "Dummy commit just to satisfy bazel" &> /dev/null

# workaround for boo#1183836
CC=gcc CXX=g++ bazel --batch build \
    --copt="-fsigned-char" \
    --cxxopt="-fsigned-char" \
    --copt="-Wno-error=old-style-cast" \
    --cxxopt="-Wno-error=old-style-cast" \
    --copt="-Wno-unused-parameter" \
    --cxxopt="-Wno-unused-parameter" \
    --copt="-Wno-implicit-fallthrough" \
    --cxxopt="-Wno-implicit-fallthrough"\
    --copt="-Wno-return-type" \
    --cxxopt="-Wno-return-type" \
    --copt="-Wno-vla-parameter" \
    --cxxopt="-Wno-vla-parameter" \
    --curses=no \
    --host_force_python=PY3 \
    --repository_cache=BAZEL_CACHE \
    --strip=never \
    --override_repository="com_github_curl=%{_datadir}/bazel-workspaces/curl" \
    --override_repository="com_github_nghttp2_nghttp2=%{_datadir}/bazel-workspaces/nghttp2" \
    --override_repository="zlib=%{_datadir}/bazel-workspaces/zlib" \
    --override_repository="org_golang_x_text=%{_builddir}/%{name}-%{version}/external/org_golang_x_text" \
    --override_repository="com_github_spf13_afero=%{_builddir}/%{name}-%{version}/external/com_github_spf13_afero" \
    --override_repository="com_github_lyft_protoc_gen_star=%{_builddir}/%{name}-%{version}/external/com_github_lyft_protoc_gen_star" \
    --override_repository="com_github_iancoleman_strcase=%{_builddir}/%{name}-%{version}/external/com_github_iancoleman_strcase" \
    --verbose_failures \
%ifarch ppc64le
    --local_cpu_resources=HOST_CPUS*.5 \
%endif
    //source/exe:envoy
bazel shutdown

%install
install -D -m0755 bazel-bin/source/exe/envoy-static %{buildroot}%{_bindir}/envoy-proxy

# Install sources
rm -rf .git bazel-*
mkdir -p %{buildroot}%{src_install_dir}
cp -r * %{buildroot}%{src_install_dir}
fdupes %{buildroot}%{src_install_dir}

%files
%license LICENSE
%doc README.md
%{_bindir}/envoy-proxy

%files source
%{src_install_dir}

%changelog
* Thu Feb 24 2022 Henry Li <lihl@microsoft.com> - 1.21.0-1
- Upgrade to version 1.21.0
- Update envoy vendor source
- Add additional pre-built vendor source that includes external go
  dependencies
- Remove unnecessary provides/comments that are imported from OpenSUSE
- Remove boringssl-source as BR
- Update 0001-build-Use-Go-from-host.patch
- Add 0002-disable-wee8-mismatched-new-delete-warning.patch to stop treating
  mismated new delete warning as error
- Remove patches that are no longer needed
- Remove -c dbg and --color=no from bazel build option which will deplete memory
  space and cause gcc compiling error
- Add bazel build option to stop treating vla-parameter warning as error
- Add --override_repository option to let bazel fetch dependencies from prebuilt 
  vendor source instead of downloading from the network 
- Disable rpm stripping

* Tue Sep 14 2021 Henry Li <lihl@microsoft.com> - 1.14.4-4
- Add patch to use newer version of bazel
- Update patch to use new version of external dependencies
- Update vendor source and file name

* Tue Jun 15 2021 Henry Li <lihl@microsoft.com> - 1.14.4-3.4
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag)
- License Verified
- Use gcc-c++ for BR
- Use ninja-build for BR
- Use golang for BR
- Change package name from envoy-proxy to envoy
- Use gcc instead of gcc10, which is not supported in CBL-Mariner
- Use bazel batch mode to build

* Wed May 19 2021 Martin Liška <mliska@suse.cz>
- Build it with GCC 10 for now (boo#1183836).

* Tue Mar 16 2021 Martin Liška <mliska@suse.cz>
- Double memory limits for dwz.

* Thu Sep 17 2020 Guillaume GARDET <guillaume.gardet@opensuse.org>
- Relax constraints on aarch64

* Tue Aug 25 2020 Michał Rostecki <mrostecki@suse.com>
- Update to 1.14.4
  * Release notes: https://www.envoyproxy.io/docs/envoy/v1.14.4/intro/version_history
- Remove patches which were either released upstream or are not
  relevant anymore:
  * 0001-server-add-getTransportSocketFactoryContext-to-Filte.patch
  * 0002-test-Fix-mocks.patch
  * 0003-test-Fix-format.patch
  * 0004-server-Add-comments-pointing-out-implementation-deta.patch
  * 0005-server-Move-setInitManager-to-TransportSocketFactory.patch
  * 0006-fix-format.patch
  * 0007-lua-Handle-the-default-case-in-scriptLog.patch
  * logger-Use-spdlog-memory_buf_t-instead-of-fmt-memory.patch
  * big-endian-support.patch
  * bazel-Fix-optional-dynamic-linking-of-OpenSSL.patch
  * compatibility-with-TLS-1.2-and-OpenSSL-1.1.0.patch
- Add patches which fix the offline build of the new version:
  * 0001-build-Use-Go-from-host.patch
  * 0002-build-update-several-go-dependencies-11581.patch
  * 0003-build-Add-explicit-requirement-on-rules_cc.patch

* Wed Jul  1 2020 Michał Rostecki <mrostecki@suse.com>
- Add patch which fixes the error occuring for spdlog 1.6.1:
  * 0007-lua-Handle-the-default-case-in-scriptLog.patch

* Wed May 20 2020 Michel Normand <normand@linux.vnet.ibm.com>
-  limit build resources for ppc64le to avoid Out of Memory error

* Wed May 20 2020 Michel Normand <normand@linux.vnet.ibm.com>
- Add ppc64/ppc64le in _constraints to use worker with max memory

* Thu Apr 16 2020 Dirk Mueller <dmueller@suse.com>
- add big-endian-support.patch to fix build on s390x:
  * backport of an already upstream patch at https://github.com/envoyproxy/envoy/pull/10250

* Mon Mar 16 2020 Michał Rostecki <mrostecki@opensuse.org>
- Fix the include dir of moonjit.

* Mon Mar  9 2020 Michał Rostecki <mrostecki@opensuse.org>
- Add bazel-rules-python as a build requirement.

* Tue Feb  4 2020 Michał Rostecki <mrostecki@opensuse.org>
- Remove nanopb from requirements.

* Thu Jan 16 2020 Michał Rostecki <mrostecki@opensuse.org>
- Add patches which allow an access to TransportSocketFactoryContext
  from a Filter context. Needed for cilium-proxy to work properly:
  * 0001-server-add-getTransportSocketFactoryContext-to-Filte.patch
  * 0002-test-Fix-mocks.patch
  * 0003-test-Fix-format.patch
  * 0004-server-Add-comments-pointing-out-implementation-deta.patch
  * 0005-server-Move-setInitManager-to-TransportSocketFactory.patch
  * 0006-fix-format.patch

* Tue Jan 14 2020 Michał Rostecki <mrostecki@opensuse.org>
- Update to version 1.12.2+git.20200109:
  * http: fixed CVE-2019-18801 by allocating sufficient memory for
    request headers.
  * http: fixed CVE-2019-18802 by implementing stricter validation
    of HTTP/1 headers.
  * http: trim LWS at the end of header keys, for correct HTTP/1.1
    header parsing.
  * http: added strict authority checking. This can be reversed
    temporarily by setting the runtime feature
    envoy.reloadable_features.strict_authority_validation to false.
  * route config: fixed CVE-2019-18838 by checking for presence of
    host/path headers.
  * listener: fixed CVE-2019-18836 by clearing accept filters
    before connection creation.
- Switch from Maistra to envoy-openssl as the way of replacing
  BoringSSL with OpenSSL.
- Add source package to build cilium-proxy separately, with
  envoy-proxy-source as a build depencency.
- Add patch which fixes dynamic linking of OpenSSL:
  * bazel-Fix-optional-dynamic-linking-of-OpenSSL.patch
- Add patch which adds backwards compatibility with TLS 1.2 and
  OpenSSL 1.1.0:
  * compatibility-with-TLS-1.2-and-OpenSSL-1.1.0.patch
- Add patch for compatibility with fmt 6.1.0 and spdlog 1.5.0:
  * logger-Use-spdlog-memory_buf_t-instead-of-fmt-memory.patch
- Remove patches which are not needed anymore:
  * 0001-bazel-Update-protobuf-and-other-needed-dependencies.patch
  * 0002-bazel-Update-grpc-to-1.23.0.patch
  * 0003-tracing-update-googleapis-use-SetName-for-operation-.patch

* Fri Dec 13 2019 Michał Rostecki <mrostecki@opensuse.org>
- Replace lua51-luajit with moonjit.

* Wed Nov  6 2019 Michał Rostecki <mrostecki@opensuse.org>
- Do not bundle any dependencies, move everything to separate
  packages.
- Add patch which makes envoy-proxy compatible with newer
  googleapis:
  * 0003-tracing-update-googleapis-use-SetName-for-operation-.patch

* Fri Nov  1 2019 Michał Rostecki <mrostecki@opensuse.org>
- Do not use global optflags (temporarily) - enabling them causes
  linker errors.

* Fri Oct 18 2019 Michał Rostecki <mrostecki@opensuse.org>
- Disable incompatible_bzl_disallow_load_after_statement check in
  Bazel - some dependencies still do not pass it.

* Thu Oct 17 2019 Richard Brown <rbrown@suse.com>
- Remove obsolete Groups tag (fate#326485)

* Wed Oct 16 2019 Michał Rostecki <mrostecki@opensuse.org>
- Remove duplicate tarball of golang-org-x-tools and unneeded
  tarballs of msgpack and http-parser.

* Tue Oct 15 2019 Michał Rostecki <mrostecki@opensuse.org>
- Update to version 1.11.1:
  * http: added mitigation of client initiated attacks that result
    in flooding of the downstream HTTP/2 connections. Those attacks
    can be logged at the “warning” level when the runtime feature
    http.connection_manager.log_flood_exception is enabled. The
    runtime setting defaults to disabled to avoid log spam when
    under attack.
  * http: added inbound_empty_frames_flood counter stat to the
    HTTP/2 codec stats, for tracking number of connections
    terminated for exceeding the limit on consecutive inbound
    frames with an empty payload and no end stream flag. The limit
    is configured by setting the
    max_consecutive_inbound_frames_with_empty_payload config
    setting.
  * http: added inbound_priority_frames_flood counter stat to the
    HTTP/2 codec stats, for tracking number of connections
    terminated for exceeding the limit on inbound PRIORITY frames.
    The limit is configured by setting the
    max_inbound_priority_frames_per_stream config setting.
  * http: added inbound_window_update_frames_flood counter stat
    to the HTTP/2 codec stats, for tracking number of connections
    terminated for exceeding the limit on inbound WINDOW_UPDATE
    frames.
  * http: added outbound_flood counter stat to the HTTP/2 codec
    stats, for tracking number of connections terminated for
    exceeding the outbound queue limit.
  * http: added outbound_control_flood counter stat to the HTTP/2
    codec stats, for tracking number of connections terminated
    for exceeding the outbound queue limit for PING, SETTINGS and
    RST_STREAM frames.
  * http: enabled strict validation of HTTP/2 messaging. Previous
    behavior can be restored using
    stream_error_on_invalid_http_messaging config setting.
- Add sources of envoy-openssl project which makes use of OpenSSL
  instead of BoringSSL.
- Add patches which makes Envoy compatible with versions of
  libraries available in openSUSE:
  * 0001-bazel-Update-protobuf-and-other-needed-dependencies.patch
  * 0002-bazel-Update-grpc-to-1.23.0.patch
- Remove patches which are not needed anymore:
  * 0001-Remove-deprecated-Blaze-PACKAGE_NAME-macro-5330.patch
  * 0001-Upgrade-gabime-spdlog-dependency-to-1.3.0-5604.patch
  * 0001-bazel-transport-sockets-Update-grpc-to-1.19.1.patch

* Thu Apr  4 2019 Jan Engelhardt <jengelh@inai.de>
- openssl-devel should be pkgconfig(openssl)

* Tue Mar 19 2019 Michal Rostecki <mrostecki@opensuse.org>
- Add patch which allows to use grpc 1.19.x.
  * 0001-bazel-transport-sockets-Update-grpc-to-1.19.1.patch
- Use source packages of grpc-httpjson-transcoding, opentracing-cpp
  and lightstep-tracer-cpp. (boo#1129568)

* Tue Mar 12 2019 Bernhard Wiedemann <bwiedemann@suse.com>
- Use fixed date for reproducible builds (boo#1047218)

* Tue Feb 26 2019 Michał Rostecki <mrostecki@opensuse.org>
- Add upstream patch which allows to use spdlog 1.3.x.
  * 0001-Upgrade-gabime-spdlog-dependency-to-1.3.0-5604.patch

* Wed Feb 20 2019 Michał Rostecki <mrostecki@opensuse.org>
- Add upstream patch which fixes build with Bazel 0.22.0.
  * 0001-Remove-deprecated-Blaze-PACKAGE_NAME-macro-5330.patch
- Fix build with the newest bazel-rules-go.

* Thu Feb 14 2019 Michał Rostecki <mrostecki@opensuse.org>
- Stop bundling libraries and dependencies, use shared libraries
  and *-source packages instead.

* Wed Oct 31 2018 Michał Rostecki <mrostecki@suse.de>
- Initial version 1.8.0+git20181105
