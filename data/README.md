## Cases and Transcripts
Cases and transcripts from Oyez's API and [[Walker Boyle's repo](https://github.com/walkerdb)] with the following additional steps:
* Removed cases prior to 1991, the first year that the most senior justice, Clarence Thomas, was on the bench.
* Updated cases & transcript to extend to the end of the 2024-2025 SCOTUS term.
* Removed cases without corresponding transcripts. This involved regrabbing 12 cases from 2017 where the case history suggested there was no transcript at the time the history was grabbed, but where the transcripts are currently available via the Oyez API.
* Removed all transcripts with "unavailable" set to `True` and their corresponding case briefs.
* Manually removed incomplete advocate data in around ~30 cases briefs.
* Remove all transcripts with transcript parameter set to null

In total, this gives us 2488 SCOTUS oral arguments transcripts with 6772 separate attorney argument sections.

## Cleaned Transcripts
Cleaned transcripts are run with the file "create_cleaned_transcripts.ipynb" Please refer to documentation in the file itself for how to use. THIS CODE WILL NOT WORK ON DIRECTLY DOWNLOADED OYEZ DATA. Please follow the data cleaning steps above to clean your Oyez data first (there will likely be a small number edge cases that you will need to manually clean as well, so be on the look out)!

Cleaned transcripts differ from Oyez transcripts in two main ways:
1. Each section of a cleaned transcript starts with an advocate opening statement and ends at the end of questioning. The Chief Justice's case introduction turn and a petitioner's rebuttal argument turns are all removed.
2. Text blocks are consolidated, speaker information is pared down, but petitioner/respondent sides are added (integrated with information from the case briefs). Adjacent speaker turns are merged.
The folder "cleaned_transcripts/restructed_text_unchanged" stores transcripts processed with the above two steps. The folder "cleaned_transcripts/restructered_overlaps_removed" includes an additional three post-processing steps to remove text overlap. This uses a heuristic approach that passes spot-check, but depending on your use case, it can be good to dig into the code to make sure that the heuristic satisfies what you need.

Note: we use |year|.|docket| as a unique id because some dockets are not unique across years.

## SQLite DB
Run "create_sql_db.ipynb" to create database for automated metrics. It's too large to be processed easily by Git, so just make sure to process wherever you're running your jobs.

## TODOs
A few of the other justices besides Roberts have argued in front of the Court before they were sworn in. Have a year filter (similar to the one we have for Roberts) that classifies them properly into "petitioner" or "respondent" instead of "scotus_justice" in their earlier cases. 07/16/2025 IMPLEMENTED! NEED TO RERUN TO REGEN

Some of the briefs for the 2024 cases have also been updated with a conclusion. We want to regrab those cases with the Oyez API.

There are cases where a speaker exists but their side/role is null. We want to set that to "inferred" or advocate as a default.