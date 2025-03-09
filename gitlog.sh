# Extract commit history with hashes, dates, and messages
git log --pretty=format:"%H | %ad | %s" --date=short > history_raw.txt
