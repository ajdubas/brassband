"""
Brassband.

Tools for modelling and analysis of UK brass band grading tables.

(c) copyright Aleksander J Dubas 2017
See LICENCE for details.
"""
import numpy as np
from random import randrange


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


def analyse(filename, nPromoted, nRelegated, nSamplesPerBand=1000,
            absentBands=[]):
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
    absentBands: list of strings
        List of absent bands.

    Returns
    -------
    None
    """
    # read in the file
    names, twoYearsAgo, lastYear = read_csv(filename)
    # calculate number of bands in the section
    nBands = len(lastYear)
    nPlayed = nBands - len(absentBands)
    # calculate the number of samples
    nSamples = nSamplesPerBand*nBands
    # calculate the starting total
    start = twoYearsAgo + lastYear

    # create absence array
    absent = np.zeros(nBands)
    for i in range(nBands):
        if names[i] in absentBands:
            absent[i] = 1

    # iterate over every band in the section
    for i in range(nBands):
        if absent[i]:
            # absent band logic
            promoted = 0
            stay = 0
            relegated = 0

            result = np.zeros(nBands, int)
            for j in range(nSamplesPerBand):
                # generate a random result
                placings = list(range(1, nPlayed+1))
                for k in range(len(result)):
                    if absent[k]:
                        result[k] = nPlayed+1
                    else:
                        result[k] = placings.pop(randrange(len(placings)))
                # calculate final score
                final = start + result
                # get total for band i
                iTotal = final[i]
                # sort the final scores (in place)
                final.sort()
                # calculate if band i is promoted or relegated
                if iTotal < final[nPromoted]:
                    promoted += 1
                elif iTotal < final[nBands-nRelegated]:
                    stay += 1
                else:
                    relegated += 1

            # calculate total number of samples
            # for each finishing position
            total = promoted + stay + relegated
            # convert results into percentages
            promotedPercent = 100*promoted/total
            stayPercent = 100*stay/total
            relegatedPercent = 100*relegated/total

            # output results
            print("\n{}".format(names[i]))
            print("-"*len(names[i]))
            print("Place\tPromote\t Stay\tRelegate")
            print("-"*32)
            print(" {:2d}a\t".format(nPlayed+1) +
                  "{: 5.1f}\t".format(promotedPercent) +
                  "{: 5.1f}\t".format(stayPercent) +
                  "{:5.1f}".format(relegatedPercent))
            continue

        # create empty arrays
        promoted = np.zeros(nPlayed)
        stay = np.zeros(nPlayed)
        relegated = np.zeros(nPlayed)

        result = np.zeros(nBands, int)
        for j in range(nSamples):
            # generate a random result
            placings = list(range(1, nPlayed+1))
            for k in range(len(result)):
                if absent[k]:
                    result[k] = nPlayed+1
                else:
                    result[k] = placings.pop(randrange(len(placings)))
            # index of finishing position of band i
            iResult = result[i]-1
            # calculate final score
            final = start + result
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
        for j in range(nPlayed):
            print(" {:2d}\t{: 5.1f}\t{: 5.1f}\t{:5.1f}".format(j+1,
                  promotedPercent[j], stayPercent[j], relegatedPercent[j]))
    return
