
%define plugin	azupnpav

Name:		vuze-plugin-%plugin
Version:	0.2.23
Release:	%mkrel 1
Summary:	Vuze plugin: Media Server
Group:		Networking/File transfer
License:	GPLv2+
URL:		http://azureus.sourceforge.net/
Source0:	http://azureus.sourceforge.net/plugins/%{plugin}_%{version}.zip
Patch0:		azupnpav-remove-win32.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	vuze
BuildRequires:	java-rpmbuild
Requires:	vuze
BuildArch:      noarch

%description
The Media Server Plugin provides a simple UPnP Media Server interface.
This allows conformant media renderers to stream content present in
Azureus.

Note that if this package is not installed, the plugin will be
automatically downloaded from sourceforge servers on Vuze startup.

%prep
%setup -q -c
unzip %{plugin}_%{version}.jar
rm %{plugin}_%{version}.jar
find -name '*.class' -delete
%patch0 -p1
ln -s %{_datadir}/azureus/build.plugins.xml build.xml
[ -e plugin.properties ] && ! grep -q plugin.version plugin.properties

%build
CLASSPATH=%{_datadir}/azureus/Azureus2.jar %ant makejar -Dsource.dir=. -Dplugin.version=%{version}

%install
rm -rf %{buildroot}

install -d -m755 %{buildroot}%{_datadir}/azureus/plugins/%plugin
install -m644 %{plugin}_%{version}.jar %{buildroot}%{_datadir}/azureus/plugins/%plugin
install -m644 plugin.properties %{buildroot}%{_datadir}/azureus/plugins/%plugin

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%dir %{_datadir}/azureus/plugins/%plugin
%{_datadir}/azureus/plugins/%plugin/%{plugin}_%{version}.jar
%{_datadir}/azureus/plugins/%plugin/plugin.properties
