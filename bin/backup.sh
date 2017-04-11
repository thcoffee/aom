cd /home/deployuser/aom
echo `date`
git add bin
git add conf
git add .gitignore
git add README.md
git commit -m "`date +%Y-%m-%d`-01 backup"
git push piter master
