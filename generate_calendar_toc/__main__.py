"""
WIP and repurposed from https://github.com/yyolk/leetcode_dailies/blob/7ab1429b952a8f10db9bdc5643201f5a9d9e7f2d/generate_calendar_toc/__main__.py

Generate a table of contents per solution directory.

The TOC in this case is a calendar with hyperlinked days.

This also serves as a way to track which days weren't completed,
as it will not link to a file that doesn't exist for the given day.
"""
import calendar
import os
import re

from datetime import datetime, date
from pathlib import Path

from bs4 import BeautifulSoup


SOLUTIONS_DIR_PATTERN = re.compile(r"\d{4}")
FILE_PATTERN = re.compile(r"\d{1,}.py")
DAYS_PATTERN = re.compile(r"\d")
TOC_INSERT_MARKER = "<!-- START_TOC -->"
README = Path("README.md")


matching_directories = []
matching_files = {}

# Loop at the base of the repository for matching solution directories
for root, dirs, files in os.walk("."):
    for dir_name in dirs:
        if SOLUTIONS_DIR_PATTERN.match(dir_name):
            matching_directories.append(Path(os.path.join(root, dir_name)))

# Loop over our directories to get the files within
for dir_ in matching_directories:
    for root, dirs, files in os.walk(dir_):
        for file_name in files:
            # Does this file_name match our FILE_PATTERN
            if FILE_PATTERN.match(file_name):
                # Our file is at dir/file_name
                file_ = dir_ / file_name
                # Extract the date from the filename, we only care about the date part.
                extracted_date = (
                    datetime.strptime(file_.stem, "%d")
                    .replace(year=int(str(dir_)), month=12)
                    .date()
                )
                # Set the Path(file) to it's datetime index, for easy lookup
                matching_files[extracted_date] = file_


cal = calendar.HTMLCalendar(calendar.SUNDAY)
readme_text = README.read_text()
readme_frontmatter = readme_text[: readme_text.find(TOC_INSERT_MARKER)].strip()
readme_toc = []
for year in matching_directories:
    year = int(str(year))
    soup = BeautifulSoup(cal.formatmonth(year, 12), "html.parser")
    dir_date = date(year, 12, 1)
    for el in soup.find_all("td", string=DAYS_PATTERN):
        # Extract the day from the <td>
        day = int(el.get_text())
        # Our lookup index is our current position in the calendar
        idx = dir_date.replace(day=day)
        # Does this day have a file to match?
        if idx in matching_files:
            path_ = matching_files[idx]
            el.string.wrap(soup.new_tag("a", href=str(path_)))
            # Add code and input emoji qualifiers.
            el.string = el.string + "🐍"
            # Create puzzle_input link (eg, "<day>.txt").
            puzzle_input_el = soup.new_tag("a", href=f"{path_.stem}.txt")
            puzzle_input_el.string = "🗒"
            el.append(soup.new_tag("br"))
            el.append(puzzle_input_el)
    # Set the align attribute to center, which works on markdown rendering for the <table />
    soup.table["align"] = "center"
    # The only content in the file will be the output of the HTMLCalendar
    year_toc = soup.prettify()
    readme_toc.append(year_toc)

readme_toc = "\n\n".join(readme_toc)
readme_content = "\n\n\n".join([readme_frontmatter, TOC_INSERT_MARKER, readme_toc])
README.write_text(readme_content)
