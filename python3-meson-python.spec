# Conditional build:
%bcond_without	doc	# API documentation
%bcond_without	tests	# unit tests

%define		module	meson-python
Summary:	Meson PEP 517 Python build backend
# Name must match the python module/package name (as on pypi or in 'import' statement)
Name:		python3-%{module}
Version:	0.17.1
Release:	0.1
License:	MIT
Group:		Libraries/Python
Source0:	https://files.pythonhosted.org/packages/source/m/meson-python/meson_python-%{version}.tar.gz
# Source0-md5:	bf1299782f02e4bb590a437bd140fd12
URL:		https://github.com/mesonbuild/meson-python
BuildRequires:	patchelf >= 0.11.0
BuildRequires:	python3-modules >= 1:3.2
BuildRequires:	python3-build
BuildRequires:	python3-installer
BuildRequires:	python3-pyproject_metadata
%if %{with tests}
BuildRequires:	python3-Cython
BuildRequires:	python3-wheel
BuildRequires:	python3-virtualenv >= 20.29
BuildRequires:	python3-requests-mock
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	python3-tox
%endif
Requires:	python3-modules >= 1:3.2
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
meson-python is a Python build back-end built on top of the Meson
build system. It enables using Meson for the configuration and build
steps of Python packages.

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
# use explicit plugins list for reliable builds (delete PYTEST_PLUGINS if empty)
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS= \
%{__python3} -m pytest tests
%endif

%if %{with doc}
%{_bindir}/tox -e docs
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install_pyproject

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGELOG.rst README.rst
%dir %{py3_sitescriptdir}/mesonpy
%{py3_sitescriptdir}/mesonpy/*.py
%{py3_sitescriptdir}/mesonpy/__pycache__
%{py3_sitescriptdir}/meson_python-%{version}.dist-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/*
%endif
