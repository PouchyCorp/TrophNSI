# Extract commit history with hashes, dates, and messages
git log --pretty=format:"%H | %ad | %s" --date=short > history_raw.txt

# Anonymize authors and emails (replace with placeholders)
git log --pretty=format:"%H | %ad | Anonymous | %s" --date=short > history_anonymized.txt

# Save the output in a final .txt file
mv history_anonymized.txt commit_history.txt

# Verify the output
cat commit_history.txt

