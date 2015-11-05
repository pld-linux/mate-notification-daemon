# NOTE:
# - we could reuse gnome notification daemon if there is added xdg/autostart file with NotShowIn=GNOME:
#   http://git.gnome.org/browse/notification-daemon/commit/data?id=1ad20d22098bc7718614a8a87744a2c22d5438d0
#
# Conditional build:
%bcond_with	gtk3	# use GTK+ 3.x instead of 2.x

Summary:	Notification daemon for MATE Desktop
Summary(pl.UTF-8):	Demon powiadomień dla środowiska MATE Desktop
Name:		mate-notification-daemon
Version:	1.12.0
Release:	1
License:	GPL v2+
Group:		Applications/System
Source0:	http://pub.mate-desktop.org/releases/1.12/%{name}-%{version}.tar.xz
# Source0-md5:	0cfb2fd81c7b7370fb6af5eed952acbc
URL:		http://wiki.mate-desktop.org/mate-notification-daemon
BuildRequires:	autoconf >= 2.63
BuildRequires:	automake >= 1:1.10
BuildRequires:	dbus-devel >= 0.78
BuildRequires:	dbus-glib-devel >= 0.78
BuildRequires:	desktop-file-utils
BuildRequires:	gdk-pixbuf2-devel >= 2.22.0
BuildRequires:	gettext-tools >= 0.11
BuildRequires:	glib2-devel >= 1:2.36.0
%{!?with_gtk3:BuildRequires:	gtk+2-devel >= 2:2.24.0}
%{?with_gtk3:BuildRequires:	gtk+3-devel >= 3.0.0}
BuildRequires:	intltool >= 0.50.1
BuildRequires:	libcanberra-devel
%{!?with_gtk3:BuildRequires:	libcanberra-gtk-devel >= 0.4}
%{?with_gtk3:BuildRequires:	libcanberra-gtk3-devel >= 0.4}
BuildRequires:	libnotify-devel
BuildRequires:	libtool >= 2:2.2.6
%{!?with_gtk3:BuildRequires:	libwnck2-devel}
%{?with_gtk3:BuildRequires:	libwnck-devel >= 3.0.0}
BuildRequires:	mate-common
BuildRequires:	pkgconfig
BuildRequires:	tar >= 1:1.22
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xz
Requires:	dbus >= 0.78
Requires:	dbus-glib >= 0.78
Requires:	glib2 >= 1:2.36.0
Requires:	gdk-pixbuf2 >= 2.22.0
Requires:	gsettings-desktop-schemas
%{!?with_gtk3:Requires:	gtk+2 >= 2:2.24.0}
%{?with_gtk3:Requires:	gtk+3 >= 3.0.0}
Requires:	gtk-update-icon-cache
Requires:	hicolor-icon-theme
%{!?with_gtk3:Requires:	libcanberra-gtk >= 0.4}
%{?with_gtk3:Requires:	libcanberra-gtk3 >= 0.4}
Provides:	dbus(org.freedesktop.Notifications)
Requires(post,postun):	/sbin/ldconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# NOTE: we must move %{_libexecdir}/mate-notification-daemon out of %{_libdir},
# because it conflicts with %{_libdir}/mate-notification-daemon plugin dir
# (unlike in mate-settings-daemon, we can use %{_libdir}/%{name} here - plugins exist in subdir)
%define		_libexecdir %{_libdir}/%{name}

%description
Notification daemon for MATE Desktop.

%description -l pl.UTF-8
Demon powiadomień dla środowiska MATE Desktop.

%prep
%setup -q

%build
%{__intltoolize}
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-icon-update \
	--disable-silent-rules \
	--disable-static \
	%{?with_gtk3:--with-gtk=3.0}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
#install -d $RPM_BUILD_ROOT%{_libdir}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# mate < 1.5 did not exist in pld, avoid dependency on mate-conf
%{__rm} $RPM_BUILD_ROOT%{_datadir}/MateConf/gsettings/mate-notification-daemon.convert

%{__rm} $RPM_BUILD_ROOT%{_libdir}/%{name}/engines/lib*.la

desktop-file-install \
	--remove-category="MATE" \
	--add-category="X-Mate" \
	--delete-original \
	--dir=$RPM_BUILD_ROOT%{_desktopdir} \
	$RPM_BUILD_ROOT%{_desktopdir}/mate-notification-properties.desktop

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_icon_cache hicolor
%glib_compile_schemas

%postun
%update_icon_cache hicolor
%glib_compile_schemas

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS README
%attr(755,root,root) %{_bindir}/mate-notification-properties
%dir %{_libdir}/%{name}
%attr(755,root,root) %{_libexecdir}/mate-notification-daemon
%dir %{_libdir}/%{name}/engines
%attr(755,root,root) %{_libdir}/%{name}/engines/libcoco.so
%attr(755,root,root) %{_libdir}/%{name}/engines/libnodoka.so
%attr(755,root,root) %{_libdir}/%{name}/engines/libslider.so
%attr(755,root,root) %{_libdir}/%{name}/engines/libstandard.so
%{_datadir}/dbus-1/services/org.freedesktop.mate.Notifications.service
%{_datadir}/glib-2.0/schemas/org.mate.NotificationDaemon.gschema.xml
%{_datadir}/%{name}
%{_desktopdir}/mate-notification-properties.desktop
%{_iconsdir}/hicolor/*/apps/mate-notification-properties.*
%{_mandir}/man1/mate-notification-properties.1*
