cd /home/deployuser/aom
echo `date`
git add bin
git add conf
git add _modules
git add sls
git add web
git add templates
git add .gitignore
git add README.md
git commit -m "`date +%Y-%m-%d` backup"
git push piter master
