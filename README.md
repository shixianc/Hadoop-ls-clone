# Hadoop-LS-Clone
Hadoop file system Clone with file listing and search functionalities. Developed in Python and xpath. 

### 1 Usage:  Clone hdfs dfs -ls <target_path>  => 
            Python source.py <hdfs_image_file> <target_path>

### 2 Apache Hadoop ls doc =>
            Options:

            -C: Display the paths of files and directories only.
            -d: Directories are listed as plain files.
            -h: Format file sizes in a human-readable fashion (eg 64.0m instead of 67108864).
            -q: Print ? instead of non-printable characters.
            -R: Recursively list subdirectories encountered.
            -t: Sort output by modification time (most recent first).
            -S: Sort output by file size.
            -r: Reverse the sort order.
            -u: Use access time rather than modification time for display and sorting.
            -e: Display the erasure coding policy of files and directories only.
            For a file ls returns stat on the file with the following format:

            permissions number_of_replicas userid groupid filesize modification_date modification_time filename
            For a directory it returns list of its direct children as in Unix. A directory is listed as:

            permissions userid groupid modification_date modification_time dirname
            Files within a directory are order by filename by default.

            Example:

            hadoop fs -ls /user/hadoop/file1
            hadoop fs -ls -e /ecdir
            Exit Code:

            Returns 0 on success and -1 on error.

### 3 Example output:
<img src="https://github.com/shixianc/Hadoop-ls-clone/blob/master/screenshots/Screen%20Shot%202020-10-04%20at%204.08.06%20PM.png" width="500">
<img src="https://github.com/shixianc/Hadoop-ls-clone/blob/master/screenshots/Screen%20Shot%202020-10-04%20at%204.08.15%20PM.png" width="500">

### 4 XML structure illustration
ls used xpath similar DFS algorithm to traverse the xml tree element and look for target path.
<img src="https://github.com/shixianc/Hadoop-ls-clone/blob/master/screenshots/Screen%20Shot%202020-10-04%20at%204.12.36%20PM.png" width="500">
(taken from medium.com)
