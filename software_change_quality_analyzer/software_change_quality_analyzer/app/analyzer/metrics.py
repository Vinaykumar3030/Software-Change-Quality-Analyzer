from pathlib import Path
from git import Repo

def get_commit_metrics(repo_path: str, commit_ref: str = "HEAD"):
    repo = Repo(repo_path)
    commit = repo.commit(commit_ref)

    if not commit.parents:
        files_changed = len(commit.stats.files)
        lines_added = commit.stats.total["insertions"]
        lines_deleted = commit.stats.total["deletions"]
    else:
        stats = commit.stats.total
        files_changed = len(commit.stats.files)
        lines_added = stats["insertions"]
        lines_deleted = stats["deletions"]

    return {
        "lines_added": int(lines_added),
        "lines_deleted": int(lines_deleted),
        "files_changed": int(files_changed),
    }
