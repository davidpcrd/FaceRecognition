git ls-files | grep -E '.js|.py|.md|.txt|.bat' | grep -v '.json' | xargs wc -l

git log --shortstat --author "davidpcrd" | grep "files changed" | awk '{files+=$1; inserted+=$4; deleted+=$6} END {print "files changed", files, "lines inserted:", inserted, "lines deleted:", deleted}'