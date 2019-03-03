# Create COMMIT
mv .gitattributes gitattributes-backup.bk
mv .git/hooks/pre-push pre-push-backup.bk
git add .
git commit -m "Temporary Deploy Commit (created by deploy.sh)"

# Push to heroku
git push heroku master -f

# Revert
git reset HEAD~1
mv gitattributes-backup.bk .gitattributes
mv pre-push-backup.bk .git/hooks/pre-push
