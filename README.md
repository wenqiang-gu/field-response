# field-response
Here are some field response files for LArTPC in json format, and a python script for converting json format to ROOT TH2 histogram

* garfield-icarus-fnal-commissioning.[json.bz2/root]

Garfield simulation for ICARUS: -240V, +10V, +260V for Y,U,V planes

Note that in ICARUS, Y is the first induction, U is the second induction, and V is the collection

The normalization is determined from the Garfield simulation. In a full transparency condition,
if you take integral of the central electron path, the integral should be close to 0.01 e/ns.
As the time binning is 100ns in the histogram, it's equivalent to 1 electron.

* Garfield simulation condition for SBND (in progress):

1st induction: -210V

2nd induction: 0V

collection:    430V 

This setting is suggested by Michelle as it provides full transparency

