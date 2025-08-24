#
# Conditional build:
%bcond_without	doc	# API documentation
%bcond_without	tests	# unit tests

%define		module	meson-python
Summary:	Meson PEP 517 Python build backend
Summary(pl.UTF-8):	Backend budowania Meson zgodny z PEP 517 dla Pythona
Name:		python3-%{module}
Version:	0.18.0
Release:	1
License:	MIT
Group:		Libraries/Python
Source0:	https://files.pythonhosted.org/packages/source/m/meson-python/meson_python-%{version}.tar.gz
# Source0-md5:	b4d7f9ef6f09deb8dc8a7e5cbf16778e
URL:		https://github.com/mesonbuild/meson-python
BuildRequires:	meson >= 1.2.3
BuildRequires:	patchelf >= 0.11.0
BuildRequires:	python3-modules >= 1:3.8
BuildRequires:	python3-build
BuildRequires:	python3-installer
BuildRequires:	python3-packaging >= 23.2
BuildRequires:	python3-pyproject_metadata >= 0.9.1
%if "%{_ver_lt %{py3_ver} 3.11}" == "1"
BuildRequires:	python3-tomli >= 1.0.0
%endif
%if %{with tests}
BuildRequires:	python3-Cython >= 3.0.3
BuildRequires:	python3-pytest >= 6.0
BuildRequires:	python3-pytest-cov
BuildRequires:	python3-pytest-mock
%if "%{_ver_lt %{py3_ver} 3.11}" == "1"
BuildRequires:	python3-typing-extensions >= 3.7.4
%endif
BuildRequires:	python3-wheel
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 2.044
%if %{with doc}
BuildRequires:	python3-furo >= 2024.8.6
BuildRequires:	python3-sphinx_copybutton >= 0.5.0
BuildRequires:	python3-sphinx_design >= 0.1.0
BuildRequires:	python3-sphinxext.opengraph >= 0.7.0
BuildRequires:	sphinx-pdg-3 >= 8.1
%endif
Requires:	patchelf >= 0.11.0
Requires:	python3-modules >= 1:3.8
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
meson-python is a Python build back-end built on top of the Meson
build system. It enables using Meson for the configuration and build
steps of Python packages.

%description -l pl.UTF-8
meson-python to backend budowania Pythona, zbudowany w oparciu o
system budowania Meson. Pozwala na używanie Mesona do kroków
konfiguracji i budowania pakietów pythonowych.

%package apidocs
Summary:	API documentation for Python %{module} module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona %{module}
Group:		Documentation

%description apidocs
API documentation for Python %{module} module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona %{module}.

%prep
%setup -q -n meson_python-%{version}

%build
%py3_build_pyproject

%if %{with tests}
# preset flags break test_ndebug
unset CFLAGS CPPFLAGS
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS=pytest_cov.plugin,pytest_mock.plugin \
%{__python3} -m pytest tests
%endif

%if %{with doc}
sphinx-build-3 -b html docs docs/_build/html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install_pyproject

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGELOG.rst LICENSE README.rst
%dir %{py3_sitescriptdir}/mesonpy
%{py3_sitescriptdir}/mesonpy/*.py
%{py3_sitescriptdir}/mesonpy/__pycache__
%{py3_sitescriptdir}/meson_python-%{version}.dist-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_sphinx_design_static,_static,explanations,how-to-guides,reference,tutorials,*.html,*.js}
%endif
