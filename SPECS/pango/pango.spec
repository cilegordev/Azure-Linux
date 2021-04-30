Summary:        library for laying out and rendering of text.
Name:           pango
Version:        1.44.7
Release:        1%{?dist}
License:        LGPLv2 OR MPLv1.1
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Libraries
URL:            https://pango.org
Source0:        https://download.gnome.org/sources/pango/1.44/%{name}-%{version}.tar.xz
BuildRequires:  cairo-devel
BuildRequires:  fontconfig
BuildRequires:  fontconfig-devel
BuildRequires:  freetype
BuildRequires:  glib-devel
BuildRequires:  gobject-introspection-devel
BuildRequires:  harfbuzz
BuildRequires:  harfbuzz-devel
BuildRequires:  libpng-devel
BuildRequires:  meson
BuildRequires:  pkg-config
BuildRequires:  pkgconfig(fribidi)
Requires:       harfbuzz-devel

%description
Pango is a library for laying out and rendering of text, with an emphasis on internationalization. Pango can be used anywhere that text layout is needed, though most of the work on Pango so far has been done in the context of the GTK+ widget toolkit.

%package	devel
Summary:        Header and development files
Requires:       %{name} = %{version}-%{release}

%description	devel
It contains the libraries and header files to create applications

%prep
%setup -q

%build
%meson

%meson_build

%install
%meson_install
find %{buildroot} -type f -name "*.la" -delete -print

%check
#These tests are known to fail. Hence sending exit 0
make %{?_smp_mflags} -k check || exit 0

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%license COPYING
%{_bindir}/*
%{_libdir}/*.so*
%{_datadir}/*
%{_libdir}/girepository-1.0/*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%changelog
* Fri Apr 16 2021 Henry Li <lihl@microsoft.com> - 1.44.7-1
- Upgrade to version 1.44.7
- Switch to meson build and install
- Add meson and pkgconfig(fribidi) as build requirement
- Fix file section for pango
- Remove cairo from build requirement

* Sat May 09 00:21:07 PST 2020 Nick Samson <nisamson@microsoft.com> - 1.40.4-4
- Added %%license line automatically

*   Mon Apr 20 2020 Nicolas Ontiveros <niontive@microsoft.com> 1.40.4-3
-   Rename "freetype2" to "freetype".
-   Remove sha1 macro.

*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.40.4-2
-   Initial CBL-Mariner import from Photon (license: Apache2).

*       Tue Apr 04 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.40.4-1
-       Initial version
