# NOTE:
# - we could reuse gnome notification daemon if there is added xdg/autostart file with NotShowIn=GNOME:
#   http://git.gnome.org/browse/notification-daemon/commit/data?id=1ad20d22098bc7718614a8a87744a2c22d5438d0
Summary:	Notification daemon for MATE Desktop
Name:		mate-notification-daemon
Version:	1.6.0
Release:	1
License:	GPL v2+
Group:		Applications/System
Source0:	http://pub.mate-desktop.org/releases/1.6/%{name}-%{version}.tar.xz
# Source0-md5:	15a90379dc551f4858c9176758c7388f
Patch1:		use-libwnck.patch
URL:		http://wiki.mate-desktop.org/mate-notification-daemon
BuildRequires:	dbus-devel >= 0.78
BuildRequires:	dbus-glib-devel >= 0.78
BuildRequires:	desktop-file-utils
BuildRequires:	glib2-devel >= 1:2.18.0
BuildRequires:	gtk+2-devel > 2:2.18
BuildRequires:	intltool >= 0.40.0
BuildRequires:	libcanberra-devel
BuildRequires:	libcanberra-gtk-devel >= 0.4
BuildRequires:	libnotify-devel
BuildRequires:	libwnck2-devel
BuildRequires:	mate-common
BuildRequires:	mate-doc-utils
BuildRequires:	tar >= 1:1.22
BuildRequires:	xorg-lib-libX11-devel
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
%patch1 -p1

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
/sbin/ldconfig
%update_icon_cache hicolor
%glib_compile_schemas

%postun
/sbin/ldconfig
%update_icon_cache hicolor
%glib_compile_schemas

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS README
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
