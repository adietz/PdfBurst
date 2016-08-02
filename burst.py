#!/usr/bin/env python
#
#

import sys, argparse, logging, re, ntpath
from PyPDF2 import PdfFileWriter, PdfFileReader
from collections import defaultdict


# Gather our code in a main() function
def main(args):

    burstTag = '{(.+?)}'

    if args.tag is not None:
        burstTag = args.tag

    print "Using Burst Tag: ", burstTag, ' on ', args.inputpdf
    outputpath = ntpath.dirname(args.inputpdf)
    if args.output is not None:
        outputpath = args.output
    filename = ntpath.basename(args.inputpdf)
    input1 = PdfFileReader(open(args.inputpdf, 'rb'))
    previousTag = "TAGNOTFOUND"
    currentTag = ""
    output = PdfFileWriter()
    outputpages = defaultdict(list)
    for page in input1.pages:
        pagecontent = page.extractText()
        tagSearch = re.search(burstTag, pagecontent)
        if tagSearch:
            currentTag = str(tagSearch.group(1))
            previousTag = currentTag
        else: #no tag was found, reuse the previous page's tag
            currentTag = previousTag
        outputpages[currentTag].append(page)
    for tag,pg in outputpages.iteritems():
        print tag
        output = PdfFileWriter()
        for outpage in pg:
            output.addPage(outpage)
        outputStream = file(outputpath + '\\' + tag + '-' + filename, "wb")
        output.write(outputStream)

# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Bursts a PDF File to multiple files, appending the burst tag to the front of the filename.",
        epilog="As an alternative to the commandline, params can be placed in a file, one per line, and specified on the commandline like '%(prog)s @params.conf'.",
        fromfile_prefix_chars='@')
    # TODO Specify your real parameters here.
    parser.add_argument(
        "inputpdf",
        help="PDF file you want to burst",
        metavar="Input.pdf")
    parser.add_argument(
        "-t",
        "--tag",
        help='regex representation, including a match group, to use as burst tag.  default will be {(.+?)}',
        metavar='bursttag')

    parser.add_argument(
        "-o",
        "--output",
        help='location to place output',
        metavar='outputpath')
    args = parser.parse_args()
    main(args)
