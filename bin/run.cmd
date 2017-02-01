if %time:~0,2% LSS 10 (
    set hour=0%time:~1,1%
) else (
    set hour=%time:~0,2%
)

set year=%date:~0,4%
set month=%date:~5,2%
set day=%date:~8,2%

set name=humblebundlespider
set logdir=%workdir%\log\%year%\%month%\%day%
set filename=%name%.%year%%month%%day%%hour%%time:~3,2%%time:~6,2%

mkdir %logdir%

set console=%logdir%\%filename%.CONSOLE.log
set item=%logdir%\%filename%.ITEM.csv
set log=%logdir%\%filename%.LOG.log

echo %date% %time% > %console%
echo ================================================================================ >> %console%

::scrapy crawl %name% -o %item% -t csv
::scrapy crawl %name% -o %item% -t csv -s LOG_FILE=%log%
scrapy crawl %name% -o %item% -t csv -s LOG_FILE=%log% >> %console%

echo ================================================================================ >> %console%
echo %date% %time% >> %console%