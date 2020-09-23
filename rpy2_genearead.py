'''
/// @file rpy2_genearead.ipynb
/// @author Austin Vandegriffe
/// @date 2020-09-23
/// @brief We will use RPy2 as an interface to R where we will use the user-friendly GENEAread library
/// @pre You will need a bin file from GENEActiv and R installed
/// @style K&R, "one true brace style" (OTBS), and '_' variable naming
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/// @references
/// ## [1] https://www.activinsights.com/wp-content/uploads/2014/03/geneactiv_instruction_manual_v1.2.pdf
/// ###### in particular, page 27
/// ## [2] https://cran.r-project.org/web/packages/GENEAread/index.html
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/// @notes
/// ## You will need to have R installed on your computer
/// ## You will need the following libraries
/// #### > pip install tzlocal
/// #### > pip install rpy2
'''


########################################################################################################################
##### Imports ##########################################################################################################
########################################################################################################################
import os
os.chdir(".")

import pandas as pd
import numpy as np
import rpy2.robjects as robjects
import rpy2.robjects.packages as rpackages
from rpy2.robjects import pandas2ri
pandas2ri.activate()

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-i', help='input')
parser.add_argument('-o', help='output')
args = parser.parse_args()

fin_name = "demo.bin"
fout_name = "demo.csv"
if args.i != None:
    fin_name = args.i
if args.o != None:
    fout_name = args.o


########################################################################################################################
##### RPy2 interfacing and Processing ##################################################################################
########################################################################################################################

#"""
utils = rpackages.importr('utils')
utils.chooseCRANmirror(ind=1)
utils.install_packages("GENEAread")
#"""

R = robjects.r
# importr("GENEAread")

R('library("GENEAread")')
# From the GENEAread library we will use read.bin to process the *.bin file.
R(f'x = read.bin( "{fin_name}" )')
# We can choose to directly save the generated table from R but I have chosen to
## process it further using pandas' dataframe.
#R(f'write.table( x$data.out[,c("timestamp","x","y","z")], file="{out_file}", sep=",", row.names=FALSE )')


########################################################################################################################
##### RPy2 Conversion and Pandas Processing ############################################################################
########################################################################################################################

# We only care about the timestamp and x,y,z
df = pd.DataFrame(pandas2ri.ri2py(R.x[0])[:,:4])
# Rename the columns, they are defaulted to 0,1,2,3,...
df.columns = ["timestamp","x","y","z"]
# The converted timestamp if in a decimal seconds; hence, by multiplying the time stamp by
## 1000 we obtain milliseconds which we can then convert using numpy
df["timestamp"] = df["timestamp"].apply( lambda x: np.datetime64( np.int(x*1000), "ms" ) )

# Save the dataframe to a file for processing by another program
df.to_csv(fout_name, header=True, index=False, sep=',')