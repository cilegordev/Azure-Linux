%global debug_package %{nil}
%ifarch x86_64
%define archname amd64
%endif
%ifarch aarch64
%define archname arm64
%endif
%define kubeproxy_n_1 1.16.13
%define coredns_n_1 1.6.2
Summary:        Microsoft Kubernetes
Name:           kubernetes
Version:        1.17.11
Release:        3%{?dist}
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Microsoft Kubernetes
URL:            https://mcr.microsoft.com/oss
#               Download URL https://kubernetesartifacts.azureedge.net/kubernetes/v1.17.11-hotfix.20200901/binaries/kubernetes-node-linux-amd64.tar.gz
Source0:        kubernetes-node-linux-%{archname}-%{version}-hotfix.20200901.tar.gz
Source1:        kubelet.service
BuildRequires:  systemd-devel
Requires:       cni
Requires:       cri-tools
Requires:       ebtables
Requires:       ethtool
Requires:       iproute
Requires:       iptables
Requires:       moby-engine
Requires:       socat
Requires:       util-linux
Requires(postun): %{_sbindir}/groupdel
Requires(postun): %{_sbindir}/userdel
Requires(pre):  %{_sbindir}/groupadd
Requires(pre):  %{_sbindir}/useradd
ExclusiveArch:  x86_64

%description
Microsoft Kubernetes %{version}.

%package        client
Summary:        Client utilities

%description    client
Client utilities for Microsoft Kubernetes %{version}.

%package        kubeadm
Summary:        Bootstrap utilities
Requires:       %{name} = %{version}
Requires:       moby-cli

%description    kubeadm
Bootstrap utilities for Microsoft Kubernetes %{version}.

%prep
%setup -q -D -T -b 0 -n kubernetes

%build
echo "Nothing to build. Picking up binaries."

%install
# install binaries
install -m 755 -d %{buildroot}%{_bindir}
cd %{_builddir}
binaries=(kubelet kubectl kubeadm)
for bin in "${binaries[@]}"; do
  echo "+++ INSTALLING ${bin}"
  install -p -m 755 -t %{buildroot}%{_bindir} kubernetes/node/bin/${bin}
done

# install service files
install -d -m 0755 %{buildroot}/%{_lib}/systemd/system
install -p -m 644 -t %{buildroot}%{_lib}/systemd/system %{SOURCE1}

# install config files
install -d -m 0755 %{buildroot}%{_sysconfdir}/kubernetes
install -d -m 644 %{buildroot}%{_sysconfdir}/kubernetes/manifests

# install the place the kubelet defaults to put volumes
install -dm755 %{buildroot}%{_sharedstatedir}/kubelet
install -dm755 %{buildroot}%{_var}/run/kubernetes

install -d -m 0755 %{buildroot}/%{_lib}/tmpfiles.d
cat << EOF >> %{buildroot}/%{_lib}/tmpfiles.d/kubernetes.conf
d %{_var}/run/kubernetes 0755 kube kube -
EOF

%clean
rm -rf %{buildroot}/*


%pre
if [ $1 -eq 1 ]; then
    # Initial installation.
    getent group kube >/dev/null || groupadd -r kube
    getent passwd kube >/dev/null || useradd -r -g kube -d / -s /sbin/nologin \
            -c "Kubernetes user" kube
fi

%post
chown -R kube:kube %{_sharedstatedir}/kubelet
chown -R kube:kube %{_var}/run/kubernetes
systemctl daemon-reload

%post kubeadm
systemctl daemon-reload
systemctl stop kubelet
systemctl enable kubelet

%postun
if [ $1 -eq 0 ]; then
    # Package deletion
    userdel kube
    groupdel kube
    systemctl daemon-reload
fi

%files
%defattr(-,root,root)
%license LICENSES
%{_bindir}/kubelet
%{_lib}/tmpfiles.d/kubernetes.conf
%dir %{_sysconfdir}/kubernetes
%dir %{_sysconfdir}/kubernetes/manifests
%dir %{_sharedstatedir}/kubelet
%dir %{_var}/run/kubernetes
%{_lib}/systemd/system/kubelet.service

%files client
%defattr(-,root,root)
%{_bindir}/kubectl

%files kubeadm
%defattr(-,root,root)
%{_bindir}/kubeadm

%changelog
* Wed Dec 02 2020 Nicolas Guibourge <nicolasg@microsoft.com> - 1.17.11-3
- Rename ms-kubernetes-1.17.11 into kubernetes and lint spec

* Wed Nov 18 2020 George Mileka <gmileka@microsoft.com> 1.17.11-2
- Added license file and macro.

* Fri Oct 2 2020 George Mileka <gmileka@microsoft.com 1.17.11-1
- Moved k8s to 1.17.11.

* Mon Aug 17 2020 Jiri Appl <jiria@microsoft.com> 1.17.7-4
- Clean up the spec.

* Thu Aug 6 2020 George Mileka <gmileka@microsoft.com> 1.17.7-3
- Create /etc/kubernetes/manifests.

* Wed Jul 30 2020 Jiri Appl <jiria@microsoft.com> 1.17.7-2
- Removed container images.

* Fri Jul 24 2020 George Mileka <gmileka@microsoft.com> 1.17.7
- Moved to 1.17.7.

* Tue Jun 30 2020 George Mileka <gmileka@microsoft.com> 1.17.3-2
- Adding the 1.16 kubeproxy and coredns for downgrade scenarios.

* Thu Jun 03 2020 Nicolas Guibourge <nicolasg@microsoft.com> 1.17.3-2
- Renaming iproute2 to iproute.

* Fri May 29 2020 George Mileka <gmileka@microsoft.com> 1.17.3.
- Switched to ecpacr.

* Tue Apr 14 2020 George Mileka <gmileka@microsoft.com> 1.17.3-hotfix.20200408
- Initial version of K8s 1.17.3-hotfix.20200408.
