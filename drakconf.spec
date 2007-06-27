# Changed by Makefile of cvs.
# do not edit here, but in cvs/soft/control-center

# needed to properly rebuild for 10.0
%define _requires_exceptions perl(lang)

Summary:  The Mandriva Linux Control Center 
Name:     drakconf
Version:  10.4.20
Release:  %mkrel 1
# get the source from our cvs repository (see
# http://www.mandrivalinux.com/en/cvs.php3)
Source0:  %name-%version.tar.bz2
Source1:  drakconf16.png
Source2:  drakconf32.png
Source3:  drakconf48.png
License:  GPL
Group:    System/Configuration/Other
Url:      http://www.mandrivalinux.com/en/cvs.php3
Obsoletes: DrakConf
Provides: DrakConf
BuildRequires: gettext intltool
BuildRequires: perl-MDK-Common-devel
Requires: mandriva-release, drakxtools > 10.4.29-1mdv2007.0
Requires: harddrake-ui > 10-12mdk, popt >= 1.6.4-24mdk, usermode
Requires: perl-Gtk2 >= 1.023-1mdk, perl-Gnome2-Vte
Requires: gtk+2.0 >= 2.2.0-3mdk, perl-MDK-Common => 1.0.4-16mdk
#Requires: drakcronat >= 0.1.3-1mdk # currenly broken, actually waiting for gtk+-2.x port completion
Requires: drakmenustyle, userdrake => 1.2-1mdk
Requires: drakconf-icons = %version
Requires: drakx-net, printerdrake, drakbackup, drak3d, drakx-kbd-mouse-x11
BuildRoot: %_tmppath/%name-%version-buildroot
Conflicts: rpmdrake < 2.4-5mdk
# workaround rpm issues on updates (bad ordering relating to virtual packages?):
Requires: perl-Gtk2-Html2
%define _requires_exceptions perl(Gtk2::Html2)

%description
drakconf includes the Mandriva Linux Control Center which is an interface to 
multiple utilities from DrakXtools.

%package icons
Summary: Icons of the Mandriva Linux Control Center
Group:   Graphical desktop/Other
Conflicts: drakconf < 10.2-4mdk

%description icons
This package hold icons of the Mandriva Linux Control Center used in
tools' banners.

%prep
%setup -q

%build

%install
rm -fr $RPM_BUILD_ROOT
%makeinstall_std

#install lang
%find_lang %name

#install menu
mkdir -p %buildroot/%_menudir
cat > %buildroot/%_menudir/drakconf << EOF
?package(%{name}): needs="x11" icon="drakconf.png" section="System/Configuration" title="Configure Your Computer" longtitle="System configuration tool" command="%_sbindir/%name" \
xdg="true"
EOF

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-drakconf.desktop << EOF
[Desktop Entry]
Name=Configure Your Computer
Comment=Configure Your Computer
Exec=%{_sbindir}/%name
Icon=drakconf.png
Terminal=false
Type=Application
StartupNotify=false
Categories=GTK;X-MandrivaLinux-System-Configuration;Settings;
EOF

#install menu icon
mkdir -p %buildroot/{%_miconsdir,%_liconsdir}
install -m644 %SOURCE1 %buildroot/%_miconsdir/drakconf.png
install -m644 %SOURCE2 %buildroot/%_iconsdir/drakconf.png
install -m644 %SOURCE3 %buildroot/%_liconsdir/drakconf.png

#this allow user to use drakconf
ln -sf %_bindir/drakconf %buildroot/%_sbindir/drakconf

install -d %buildroot/etc
touch %buildroot/etc/mcc.conf

for i in %buildroot{%_sbindir,%_bindir}/mcc; do ln -s {drakconf,$i}; done

(cd $RPM_BUILD_ROOT ; find usr -type f -name "*.png"  -printf "/%%p\n") > images-big.list
perl -ni -e '/128/ ? print : print STDERR $_ ' images-big.list 2> images.list
cat images-big.list >> %name.lang

%post
%update_menus

%postun
%clean_menus

%triggerun -- %name < 9.0-0.6mdk
[[ -s /root/.mcc ]] && cp -af /root/.mcc /etc/mcc.conf; :

%clean
rm -rf $RPM_BUILD_ROOT

%files icons -f images.list
%defattr(-,root,root)

%files -f %{name}.lang
%defattr(-,root,root)
%doc COPYING 
%config(noreplace) %ghost %{_sysconfdir}/mcc.conf
%config(noreplace) %{_sysconfdir}/gnome-vfs-2.0/vfolders/*
%_bindir/*
%_sbindir/*
%_menudir/drakconf
%{_datadir}/applications/mandriva-drakconf.desktop
%_miconsdir/*.png
%_iconsdir/*.png
%_liconsdir/*.png
%dir %_datadir/mcc
%_datadir/mcc/desktop
%dir %_datadir/mcc/themes/
%dir %_datadir/mcc/themes/default
%_datadir/mcc/themes/default/gtkrc


