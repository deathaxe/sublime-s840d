@echo off

del /q output.txt

for %%f in (*.spf) do (
	for /f "eol=^ delims=" %%r in (%%f) do (
		echo %%r >> output.txt
	)
)