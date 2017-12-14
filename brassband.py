"""
brassband.py

Tools for modelling and analysis of UK brass band grading tables.

(c) copyright Aleksander J Dubas 2017
See LICENCE for details.
"""
import numpy as np
from random import sample


def read_csv(filename):
    """
    Read in a csv file.

    The format of the file should be:
    Band Name, Result Two Years Ago, Result Last Year

    Parameters
    ----------
    filename: string
        Name of the file to be read in.

    Returns
    -------
    names: list of strings
        A list of the names of each band.
    twoYearsAgo: array of numbers
        An array of results from two years ago.
    lastYear: list of numbers
        An array of results from last year.
    """
    # create lists first
    names = []
    twoY = []
    lastY = []
    with open(filename, "r") as fin:
        for line in fin.readlines():
            cells = line.split(",")
            try:
                names.append(cells[0])
                twoY.append(float(cells[1]))
                lastY.append(float(cells[2]))
            except IndexError:
                pass
    return names, np.array(twoY), np.array(lastY)


def analyse(filename, nPromoted, nRelegated, nSamplesPerBand=1000):
    """
    Analyses the table in <filename>.

    Estimates probability of promotion, retention or relegation
    depending on finishing position.
    Assumes all bands in the section have an equal chance
    of finishing in all positions.
    Output is written to console.

    Parameters
    ----------
    filename: string
        Name of the file containing the section data.
    nPromoted: integer
        Number of bands promoted in the section.
    nRelegated: integer
        Number of bands relegated in the section.
    nSamplesPerBand: integer (default 1000)
        Number of times to sample finishing position.
        The larger this is, the greater the accuracy,
        but the longer the calculation time.

    Returns
    -------
    None
    """
    # read in the file
    names, twoYearsAgo, lastYear = read_csv(filename)
    # calculate number of bands in the section
    nBands = len(lastYear)
    # calculate the number of samples
    nSamples = nSamplesPerBand*nBands
    # calculate the starting total
    start = twoYearsAgo + lastYear

    # iterate over every band in the section
    for i in range(nBands):
        # create empty arrays
        promoted = np.zeros(nBands)
        stay = np.zeros(nBands)
        relegated = np.zeros(nBands)

        for j in range(nSamples):
            # generate a random result
            result = sample(range(1, nBands+1), nBands)
            # index of finishing position of band i
            iResult = result[i]-1
            # calculate final score
            final = start + np.array(result)
            # get total for band i
            iTotal = final[i]
            # sort the final scores (in place)
            final.sort()
            # calculate if band i is promoted or relegated
            if iTotal < final[nPromoted]:
                promoted[iResult] += 1
            elif iTotal < final[nBands-nRelegated]:
                stay[iResult] += 1
            else:
                relegated[iResult] += 1

        # calculate total number of samples
        # for each finishing position
        totals = promoted + stay + relegated
        # convert results into percentages
        promotedPercent = 100*promoted/totals
        stayPercent = 100*stay/totals
        relegatedPercent = 100*relegated/totals

        # output results
        print("\n{}".format(names[i]))
        print("-"*len(names[i]))
        print("Place\tPromote\t Stay\tRelegate")
        print("-"*32)
        for j in range(nBands):
            print(" {:2d}\t{: 5.1f}\t{: 5.1f}\t{:5.1f}".format(j+1,
                promotedPercent[j], stayPercent[j], relegatedPercent[j]))
    return
