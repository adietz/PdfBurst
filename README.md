# PdfBurst
PdfBurst is a python script that can burst a pdf file into multiple pdfs based on the presence of a burst tag ({....} by default) on each page.

In the event that no burst tag exists on a page, the previously found burst tag is reused.  This allows you to put a burst tag on the
first page of a report and then burst the report out by, for instance, client.

Multiple, non-linear burst tags are combined into one file, so a sequence of pages like 
{tag1}, {tag2}, {tag3}, {tag2} would only generate 3 separate files, not 4.
