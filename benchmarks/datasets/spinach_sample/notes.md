## Spinach - [SampleI](https://spindynamics.org/documents/spinach_2_6_5625.zip) under examples/deernet_paper_kuprov.m (Matlab file) and  examples/deernet_paper_kuprov.m/sample_I_DEERNet_input.DAT

Author: Ronny Kohavi and Barry Becker  
Source: [i.kuprov](https://arxiv.org/pdf/2106.07465.pdf) - Unknown
Please cite: ake Keeley,  Tajwar Choudhury, Laura Galazzo, Enrica Bordignon, Akiva Feintuch, Daniella Goldfarb, Andrea Eggeling, Luis Fabregas Ibanez, Gunnar Jeschke, Ilya Kuprov  Neural networks in double electron-electron resonance:  a practical guide.  

### Variable description  
Field of the output structure Content 
.input_axis time grid (seconds), as received 
.input_traces DEER data, as received 
.n_networks number of neural nets in the ensemble 
.train_params neural network training parameters, described in 
.resamp_axis
.resamp_traces time grid and DEER data, resampled to 512 time points to match the input dimension of the neural networks 
.dist_ax distance grid (Angstrom) of the output 
.dist_av mean
.dist_lb 95% lower bound
.dist_ub 95% upper bound on the distance distribution(s)
.backgs_av mean
.backgs_lb 95% lower bound
.backgs_ub 95% upper bound on the back-ground signals
.retros_av mean
.retros_lb 95% lower bound
.retros_ub 95% upper bound on the back-cal-culated fit to the experimental data
.mdpths_av mean
.mdpths_st standard deviation of the modulation depths

Description from the donor of the data:   

Using neural networks in electron double resonance.  

### Relevant papers   Jake Keeley,  Tajwar Choudhury, Laura Galazzo, Enrica Bordignon, Akiva Feintuch, Daniella Goldfarb, Andrea Eggeling, Luis Fabregas Ibanez, Gunnar Jeschke, Ilya Kuprov  Neural networks in double electron-electron resonance:  a practical guide.  e-mail: i.kuprov '@' soton.ac.uk for questions. 

Code for Exporting data and arrays from Matlab into XML (SampleI) and generating graph:

`expt_data=load('<windows_directory>\spinach_2_6_5625\examples\deernet\data_paper_kuprov\sample_I_DEERNet_input.dat','-ASCII');`
`t= deernet(expt_data(:,2),1e-6*expt_data(:,1));`
`writestruct(t,'<windows_directory>\sample_I_DEERNet_input.xml','FileType','xml');`
`drawnow();`

Code in Power Query to generate resampled arrays into consolidated output using dynamix index generation and data merging:

`let`
`    Source = Table.NestedJoin(DEERNet,{"Path"},DEERNet_ReSampAxis,{"Path"},"DEERNet_ReSampAxis",JoinKind.Inner),`
`    #"Expanded DEERNet_ReSampAxis" = Table.ExpandTableColumn(Source, "DEERNet_ReSampAxis", {"resamp_axis", "resamp_axis.Element:Text.Index"}, {"DEERNet_ReSampAxis.resamp_axis", "DEERNet_ReSampAxis.resamp_axis.Element:Text.Index"}),`
`    #"Renamed Columns" = Table.RenameColumns(#"Expanded DEERNet_ReSampAxis",{{"DEERNet_ReSampAxis.resamp_axis", "resamp_axis"}}),`
`    #"Merged Queries" = Table.NestedJoin(#"Renamed Columns",{"Path", "DEERNet_ReSampAxis.resamp_axis.Element:Text.Index"},DEERNet_BackGSAv,{"Path", "backgs_av.Element:Text.Index"},"DEERNet_BackGSAv",JoinKind.LeftOuter),`
`    #"Expanded DEERNet_BackGSAv" = Table.ExpandTableColumn(#"Merged Queries", "DEERNet_BackGSAv", {"backgs_av"}, {"DEERNet_BackGSAv.backgs_av"}),`
`    #"Renamed Columns1" = Table.RenameColumns(#"Expanded DEERNet_BackGSAv",{{"DEERNet_BackGSAv.backgs_av", "backgs_av"}}),`
`    #"Merged Queries1" = Table.NestedJoin(#"Renamed Columns1",{"Path", "DEERNet_ReSampAxis.resamp_axis.Element:Text.Index"},DEERNet_BackGSLB,{"Path", "backgs_lb.Element:Text.Index"},"DEERNet_BackGSLB",JoinKind.Inner),`
`    #"Expanded DEERNet_BackGSLB" = Table.ExpandTableColumn(#"Merged Queries1", "DEERNet_BackGSLB", {"backgs_lb"}, {"DEERNet_BackGSLB.backgs_lb"}),`
`    #"Renamed Columns3" = Table.RenameColumns(#"Expanded DEERNet_BackGSLB",{{"DEERNet_BackGSLB.backgs_lb", "backgs_lb"}}),`
`    #"Merged Queries2" = Table.NestedJoin(#"Renamed Columns3",{"Path", "DEERNet_ReSampAxis.resamp_axis.Element:Text.Index"},DEERNet_BackGSUB,{"Path", "backgs_ub.Element:Text.Index"},"DEERNet_BackGSUB",JoinKind.Inner),`
`    #"Expanded DEERNet_BackGSUB" = Table.ExpandTableColumn(#"Merged Queries2", "DEERNet_BackGSUB", {"backgs_ub"}, {"DEERNet_BackGSUB.backgs_ub"}),`
`    #"Renamed Columns4" = Table.RenameColumns(#"Expanded DEERNet_BackGSUB",{{"DEERNet_BackGSUB.backgs_ub", "backgs_ub"}}),`
`    #"Merged Queries3" = Table.NestedJoin(#"Renamed Columns4",{"Path", "DEERNet_ReSampAxis.resamp_axis.Element:Text.Index"},DEERNet_RetrosAv,{"Path", "retros_av.Element:Text.Index"},"DEERNet_RetrosAv",JoinKind.Inner),`
`    #"Expanded DEERNet_RetrosAv" = Table.ExpandTableColumn(#"Merged Queries3", "DEERNet_RetrosAv", {"retros_av"}, {"retros_av"}),`
`    #"Merged Queries4" = Table.NestedJoin(#"Expanded DEERNet_RetrosAv",{"Path", "DEERNet_ReSampAxis.resamp_axis.Element:Text.Index"},DEERNet_RetrosLB,{"Path", "retros_lb.Element:Text.Index"},"DEERNet_RetrosLB",JoinKind.Inner),`
`    #"Expanded DEERNet_RetrosLB" = Table.ExpandTableColumn(#"Merged Queries4", "DEERNet_RetrosLB", {"retros_lb"}, {"retros_lb"}),`
`    #"Merged Queries5" = Table.NestedJoin(#"Expanded DEERNet_RetrosLB",{"Path", "DEERNet_ReSampAxis.resamp_axis.Element:Text.Index"},DEERNet_RetrosUB,{"Path", "retros_ub.Element:Text.Index"},"DEERNet_RetrosUB",JoinKind.Inner),`
`    #"Expanded DEERNet_RetrosUB" = Table.ExpandTableColumn(#"Merged Queries5", "DEERNet_RetrosUB", {"retros_ub"}, {"retros_ub"}),`
`    #"Reordered Columns" = Table.ReorderColumns(#"Expanded DEERNet_RetrosUB",{"Path", "n_networks", "train_params.max_time", "train_params.ndistmax", "train_params.npoints", "train_params.min_exch", "train_params.max_exch", "train_params.min_bdim", "train_params.max_bdim", "train_params.min_fwhm", "train_params.max_fwhm", "train_params.min_mdep", "train_params.max_mdep", "train_params.noise_lvl", "train_params.min_brate", "train_params.max_brate", "mdpths_av", "mdpths_st", "DEERNet_ReSampAxis.resamp_axis.Element:Text.Index", "resamp_axis", "backgs_av"}),`
`    #"Renamed Columns2" = Table.RenameColumns(#"Reordered Columns",{{"DEERNet_ReSampAxis.resamp_axis.Element:Text.Index", "rownumber"}})`
`in`
`    #"Renamed Columns2"`