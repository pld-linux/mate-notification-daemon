# NOTE:
# - we could reuse gnome notification daemon if there is added xdg/autostart file with NotShowIn=GNOME:
#   http://git.gnome.org/browse/notification-daemon/commit/data?id=1ad20d22098bc7718614a8a87744a2c22d5438d0
Summary:	Notification daemon for MATE Desktop
Name:		mate-notification-daemon
Version:	1.5.0
Release:	0.2
License:	GPL v2+
Source0:	http://pub.mate-desktop.org/releases/1.5/%{name}-%{version}.tar.xz
# Source0-md5:	393a7832e71aa8cfd28793750f88de50
Group:		Applications/System
URL:		http://mate-desktop.org/
BuildRequires:	desktop-file-utils
BuildRequires:	icon-naming-utils
BuildRequires:	mate-common
BuildRequires:	pkgconfig(MateCORBA-2.0)
BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires:	pkgconfig(gsettings-desktop-schemas)
BuildRequires:	pkgconfig(libcanberra)
BuildRequires:	pkgconfig(libmatenotify)
BuildRequires:	pkgconfig(libmatewnck)
BuildRequires:	pkgconfig(mate-desktop-2.0)
BuildRequires:	pkgconfig(mate-doc-utils)
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	glib2 >= 1:2.26.0
Requires:	gsettings-desktop-schemas
Requires:	gtk-update-icon-cache
Requires:	hicolor-icon-theme
Provides:	dbus(org.freedesktop.Notifications)
Requires(post,postun):	/sbin/ldconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# makefiles and this spec gets confused if %{_libdir} == %{_libexecdir}
# so we setup separate --libexecdir=%{_libdir}/mnd
%define		_libexecdir %{_libdir}/mnd

%description
Notification daemon for MATE Desktop.

%prep
%setup -q

%build
NOCONFIGURE=1 ./autogen.sh
%configure \
	--disable-static

%{__make} \
	V=1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}
%{__make} install \
	LIBTOOL="%{_bindir}/libtool" \
	DESTDIR=$RPM_BUILD_ROOT

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
/sbin/ldconfig
%update_icon_cache hicolor
%glib_compile_schemas

%postun
/sbin/ldconfig
%update_icon_cache hicolor
%glib_compile_schemas

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS COPYING README
%attr(755,root,root) %{_bindir}/mate-notification-properties
%{_desktopdir}/mate-notification-properties.desktop
%{_datadir}/dbus-1/services/org.freedesktop.mate.Notifications.service
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/mate-notification-properties.ui
%dir %{_libexecdir}
%attr(755,root,root) %{_libexecdir}/mate-notification-daemon
%{_iconsdir}/hicolor/*/apps/mate-notification-properties.*
%{_datadir}/glib-2.0/schemas/org.mate.NotificationDaemon.gschema.xml
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/engines
%attr(755,root,root) %{_libdir}/%{name}/engines/libcoco.so
%attr(755,root,root) %{_libdir}/%{name}/engines/libnodoka.so
%attr(755,root,root) %{_libdir}/%{name}/engines/libslider.so
%attr(755,root,root) %{_libdir}/%{name}/engines/libstandard.so
