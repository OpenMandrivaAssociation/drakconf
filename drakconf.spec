Summary:	The %{vendor} Linux Control Center
Name:		drakconf
Version:	13.1
Release:	2
License:	GPLv2+
Group:		System/Configuration/Other
Url:		https://abf.io/omv_software/drakconf
Source0:	%{name}-%{version}.tar.xz
BuildArch:	noarch
BuildRequires:	gettext
BuildRequires:	intltool
BuildRequires:	perl-MDK-Common-devel
BuildRequires:	drakxtools-backend
BuildRequires:	perl-Locale-gettext
Requires:	distro-release
Requires:	drakconf-icons = %{version}
Requires:	drakxtools >= 11.64
Requires:	drakx-kbd-mouse-x11
Requires:	harddrake-ui
Requires:	perl-MDK-Common
Requires:	userdrake
Requires:	termcap
Requires:	vte2.91
#Suggests:	mdkonline >=2.77.19
Suggests:	drakmenustyle
#Suggests:	drakbackup
#Suggests:	drakvirt
Suggests:	msec-gui
Suggests:	drakfax
#Suggests:	drakguard
#Suggests:	draksnapshot
Suggests:	rpmdrake
Suggests:	system-config-printer
Suggests:	transfugdrake
# Replacing drakboot -- kdebase4-runtime is for kcmshell4
#Suggests:	kdebase4-runtime
#Suggests:	kcm-grub2
Suggests:	firewall-config

%description
drakconf includes the %{vendor} Linux Control Center
which is an interface to multiple utilities from DrakXtools.

%package	icons
Summary:	Icons of the %{vendor} Linux Control Center
Group:		Graphical desktop/Other

%description icons
This package hold icons of the %{vendor}
Linux Control Center used in tools' banners.

%prep
%setup -q
%apply_patches

%build

%install
%makeinstall_std

#install lang
%find_lang %{name}

#install menu
mkdir -p %{buildroot}%{_datadir}/applications
install -m644 drakconf.desktop %{buildroot}%{_datadir}/applications/%{_vendor}-drakconf.desktop

#install menu icon
mkdir -p %{buildroot}/{%{_iconsdir},%{_miconsdir},%{_liconsdir}}
install -m644 drakconf20.png %{buildroot}/%{_miconsdir}/drakconf.png
install -m644 drakconf36.png %{buildroot}/%{_iconsdir}/drakconf.png
install -m644 drakconf52.png %{buildroot}/%{_liconsdir}/drakconf.png

install -d %{buildroot}/etc
touch %{buildroot}/etc/mcc.conf

for i in %{buildroot}{%{_sbindir},%{_bindir}}/mcc; do ln -s {drakconf,$i}; done

(cd %{buildroot} ; find usr -type f -name "*.png"  -printf "/%%p\n") > images-big.list
perl -ni -e '/128/ ? print : print STDERR $_ ' images-big.list 2> images.list
cat images-big.list >> %{name}.lang

%files icons -f images.list

%files -f %{name}.lang
%config(noreplace) %ghost %{_sysconfdir}/mcc.conf
%config(noreplace) %{_sysconfdir}/sysconfig/mcc.conf
%{_bindir}/*
%{_sbindir}/*
%{_libexecdir}/drakconf
%{_libexecdir}/drakxconf
%{_datadir}/applications/%{_vendor}-drakconf.desktop
%{perl_vendorlib}/MDV
%dir %{_datadir}/mcc
%{_datadir}/mcc/progs.conf
%{_datadir}/polkit-1/actions/*
%dir %{_datadir}/mcc/themes/
%dir %{_datadir}/mcc/themes/default
%{_datadir}/mcc/themes/default/mcc.css

%post
mkdir -p %{_localstatedir}/log
touch %{_localstatedir}/log/explanations
