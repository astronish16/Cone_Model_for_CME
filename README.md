# Cone Model for CME
A python-3 implementation of cone model [Xie et al.,2004](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2003JA010226#) for Solar Coronal Mass Ejection.

The file `Xie's_cone_v1.py` provides a python programme to get necessary CME parameters as discussed in the model. Folder `Data` consist of the datafiles used in the programme, while folder `img` consist of the output iamges.

## Steps to obtain CME parameters
1) Dowload processed images of SOHO/LASCO observation from [Helioviewer.org](https://helioviewer.ias.u-psud.fr/) or [SunPy](https://docs.sunpy.org/en/stable/guide/acquiring_data/helioviewer.html).
2) Read those data files using (data,header) variables with sequential number (In order to get running difference image; see line number 39 to 54).
3) Select particular data file to infer CME parameters. (See line number 60 to 64)
4) Compile the code.
5) After compilation a popup window will appear in which difference image of CME is shown. Select 30 to 35 points on CME leading edge and press Esc key. (To fit ellipse we require only 5 points; but we select as many as points to minimize variation in parameters obtained from sequential frames)
6) Programme will return CME paramters with fitted halo on top of SOHO/LASCO image.









# Note
Currently this python program is in early stage. It only works with the SOHO/LASCO coronagraph data. So if you find any bug or have some suggestions for improvement, please notify me with Github [Issues](https://github.com/astronish16/Cone_Model_for_CME/issues) or [Pull requests](https://github.com/astronish16/Cone_Model_for_CME/pulls).
