if %time:~0,2% LSS 10 (
    set hour=0%time:~1,1%
) else (
    set hour=%time:~0,2%
)

set year=%date:~0,4%
set month=%date:~5,2%
set day=%date:~8,2%

set name=pymodule.py
set logdir=%PROJECT_HOME%\log\%year%\%month%\%day%
set filename=%name%.%year%%month%%day%%hour%%time:~3,2%%time:~6,2%
set console=%logdir%\%filename%.CONSOLE.log

mkdir %logdir%

echo %date% %time% > %console%
echo ================================================================================ >> %console%

echo python %name%

echo ================================================================================ >> %console%
echo %date% %time% >> %console%