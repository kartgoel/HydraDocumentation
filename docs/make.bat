@REM @ECHO OFF

@REM pushd %~dp0

@REM REM Command file for Sphinx documentation

@REM if "%SPHINXBUILD%" == "" (
@REM 	set SPHINXBUILD=sphinx-build
@REM )
@REM set SOURCEDIR=source
@REM set BUILDDIR=build

@REM if "%1" == "" goto help

@REM %SPHINXBUILD% >NUL 2>NUL
@REM if errorlevel 9009 (
@REM 	echo.
@REM 	echo.The 'sphinx-build' command was not found. Make sure you have Sphinx
@REM 	echo.installed, then set the SPHINXBUILD environment variable to point
@REM 	echo.to the full path of the 'sphinx-build' executable. Alternatively you
@REM 	echo.may add the Sphinx directory to PATH.
@REM 	echo.
@REM 	echo.If you don't have Sphinx installed, grab it from
@REM 	echo.http://sphinx-doc.org/
@REM 	exit /b 1
@REM )

@REM %SPHINXBUILD% -M %1 %SOURCEDIR% %BUILDDIR% %SPHINXOPTS% %O%
@REM goto end

@REM :help
@REM %SPHINXBUILD% -M help %SOURCEDIR% %BUILDDIR% %SPHINXOPTS% %O%

@REM :end
@REM popd


@ECHO OFF

pushd %~dp0

REM Command file for Sphinx documentation

if "%SPHINXBUILD%" == "" (
	set SPHINXBUILD=sphinx-build
)
set SOURCEDIR=source
set BUILDDIR=build
set SPHINXOPTS=-W --keep-going

if "%1" == "" goto help

%SPHINXBUILD% >NUL 2>NUL
if errorlevel 9009 (
	echo.
	echo.The 'sphinx-build' command was not found. Make sure you have Sphinx
	echo.installed, then set the SPHINXBUILD environment variable to point
	echo.to the full path of the 'sphinx-build' executable. Alternatively you
	echo.may add the Sphinx directory to PATH.
	echo.
	echo.If you don't have Sphinx installed, grab it from
	echo.http://sphinx-doc.org/
	exit /b 1
)

%SPHINXBUILD% -M %1 %SOURCEDIR% %BUILDDIR% %SPHINXOPTS%
goto end

:help
%SPHINXBUILD% -M help %SOURCEDIR% %BUILDDIR% %SPHINXOPTS%

:end
popd
