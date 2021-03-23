# NOTE:
# - we could reuse gnome notification daemon if there is added xdg/autostart file with NotShowIn=GNOME:
#   http://git.gnome.org/browse/notification-daemon/commit/data?id=1ad20d22098bc7718614a8a87744a2c22d5438d0
#

Summary:	Notification daemon for MATE Desktop
Summary(pl.UTF-8):	Demon powiadomień dla środowiska MATE Desktop
Name:		mate-notification-daemon
Version:	1.24.2
Release:	1
License:	GPL v2+
Group:		Applications/System
Source0:	https://pub.mate-desktop.org/releases/1.24/%{name}-%{version}.tar.xz
# Source0-md5:	a4fe071c5337e88c27b7991679dca425
URL:		http://wiki.mate-desktop.org/mate-notification-daemon
BuildRequires:	autoconf >= 2.63
BuildRequires:	automake >= 1:1.10
BuildRequires:	dbus-devel >= 0.78
BuildRequires:	desktop-file-utils
BuildRequires:	gdk-pixbuf2-devel >= 2.22.0
BuildRequires:	gettext-tools >= 0.19.8
BuildRequires:	glib2-devel >= 1:2.50.0
BuildRequires:	gtk+3-devel >= 3.22.0
BuildRequires:	libcanberra-devel
BuildRequires:	libcanberra-gtk3-devel >= 0.4
BuildRequires:	libnotify-devel
BuildRequires:	libtool >= 2:2.2.6
BuildRequires:	libwnck-devel >= 3.0.0
BuildRequires:	mate-common
BuildRequires:	pkgconfig
BuildRequires:	tar >= 1:1.22
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xz
Requires:	dbus >= 0.78
Requires:	gdk-pixbuf2 >= 2.22.0
Requires:	glib2 >= 1:2.50.0
Requires:	gsettings-desktop-schemas
Requires:	gtk+3 >= 3.22.0
Requires:	gtk-update-icon-cache
Requires:	hicolor-icon-theme
Requires:	libcanberra-gtk3 >= 0.4
Provides:	dbus(org.freedesktop.Notifications)
Requires(post,postun):	/sbin/ldconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%if "%{_libexecdir}" == "%{_libdir}"
# NOTE: we must move %{_libexecdir}/mate-notification-daemon out of %{_libdir},
# because it conflicts with %{_libdir}/mate-notification-daemon plugin dir
# (unlike in mate-settings-daemon, we can use %{_libdir}/%{name} here - plugins exist in subdir)
%define		_libexecdir %{_libdir}/%{name}
%endif

%description
Notification daemon for MATE Desktop.

%description -l pl.UTF-8
Demon powiadomień dla środowiska MATE Desktop.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-icon-update \
	--disable-silent-rules \
	--disable-static

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/%{name}/engines/lib*.la
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/{frp,ie,ku_IQ}

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
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/mate-notification-properties
%attr(755,root,root) %{_libexecdir}/mate-notification-daemon
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/engines
%attr(755,root,root) %{_libdir}/%{name}/engines/libcoco.so
%attr(755,root,root) %{_libdir}/%{name}/engines/libnodoka.so
%attr(755,root,root) %{_libdir}/%{name}/engines/libslider.so
%attr(755,root,root) %{_libdir}/%{name}/engines/libstandard.so
%{_datadir}/dbus-1/services/org.freedesktop.mate.Notifications.service
%{_datadir}/glib-2.0/schemas/org.mate.NotificationDaemon.gschema.xml
%{_desktopdir}/mate-notification-properties.desktop
%{_iconsdir}/hicolor/*/apps/mate-notification-properties.*
%{_mandir}/man1/mate-notification-properties.1*
