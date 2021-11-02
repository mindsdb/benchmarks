## [Comparative DEER Analyzer](https://ethz.ch/content/dam/ethz/special-interest/chab/physical-chemistry/epr-dam/documents/software/deer-15-on/CDA_Installer.zip) - [deer_bi_50_50K](https://ethz.ch/content/dam/ethz/special-interest/chab/physical-chemistry/epr-dam/documents/software/deer-15-on/DeerAnalysis2021b.zip) under consensus_deer_analysis.m (Matlab file) and  deernet_standalone/examples/data_deeran/deer_bi_50_50K.DTA 

Author: G. Jeschke 
Source: [i.kuprov](https://arxiv.org/pdf/2106.07465.pdf) - Unknown
Please cite: ake Keeley,  Tajwar Choudhury, Laura Galazzo, Enrica Bordignon, Akiva Feintuch, Daniella Goldfarb, Andrea Eggeling, Luis Fabregas Ibanez, Gunnar Jeschke, Ilya Kuprov  Neural networks in double electron-electron resonance:  a practical guide.  

### Variable description  
Field of the output structure (Content )
Zero-corrected time axis
Real part (phase corrected)
Imaginary part (phase corrected)
DEERNet background
DEERNet fit
Tihonov regularization fit
DEERNet fit lower bound
DEERNet fit upper bound
DEERNet bckg. lower bound
DEERNet bckg. upper bound
Exponential background
Exponential backg. lower bound
Exponential backg. upper bound
row_number

Description from the donor of the data:   

Using neural networks in electron double resonance.  

### Relevant papers   Jake Keeley,  Tajwar Choudhury, Laura Galazzo, Enrica Bordignon, Akiva Feintuch, Daniella Goldfarb, Andrea Eggeling, Luis Fabregas Ibanez, Gunnar Jeschke, Ilya Kuprov  Neural networks in double electron-electron resonance:  a practical guide.  e-mail: i.kuprov '@' soton.ac.uk for questions. 

Required Running Comparative DEER Analyzer for inputting data (DTA and DSC files) and outputting two different DAT files.

Code in Power Query to import DAT files, add column names based on CDA documentation and assign dynamic index generation:

`(path as text) =>`
`let`
 `   Source = Csv.Document(File.Contents(path),null,"",null,1252),`
 `   #"Change Type" = Table.TransformColumnTypes(Source,{{"Column1", type text}, {"Column2", type number}, {"Column3", type number}, {"Column4", type number}, {"Column5", type number}, {"Column6", type number}, {"Column7", type number}, {"Column8", type number}, {"Column9", type number}, {"Column10", type number}, {"Column11", type number}}),`
 `   #"Removed Columns" = Table.RemoveColumns(#"Change Type",{"Column1"}),`
 `   #"Renamed Columns" = Table.RenameColumns(#"Removed Columns",{{"Column2", "Zero-corrected time axis"}, {"Column3", "Real part (phase corrected)"}, {"Column4", "Imaginary part (phase corrected)"}, {"Column5", "DEERNet background"}, {"Column6", "DEERNet fit"}, {"Column7", "Tihonov regularization fit"}, {"Column8", "DEERNet fit lower bound"}, {"Column9", "DEERNet fit upper bound"}, {"Column10", "DEERNet bckg. lower bound"}, {"Column11", "DEERNet bckg. upper bound"}, {"Column12", "Exponential background"}, {"Column13", "Exponential backg. lower bound"}, ``{"Column14", "Exponential backg. upper bound"}}),`
 `   #"Changed Type" = Table.TransformColumnTypes(#"Renamed Columns",{{"Exponential background", type number}, {"Exponential backg. lower bound", type number}, {"Exponential backg. upper bound", type number}}),`
 `   #"Added Index" = Table.AddIndexColumn(#"Renamed Columns", "row_number", 0, 1)`

`in`
 `   #"Added Index"`