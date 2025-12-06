# ROOT Data Analyzer – Finding Particle Peaks in CERN Open Data

## Dataset
The dataset used in this analysis is `NanoAOD_DoubleMuon.root`, obtained from the CERN Open Data portal.
It contains proton–proton collision events recorded at the LHC, with reconstructed muons stored in a TTree
named `Events`.

## Analysis Method
For each event, all unique pairs of reconstructed muons were selected.
The four-momentum of each muon was built using its transverse momentum (pT), pseudorapidity (η),
azimuthal angle (φ), and mass.
The invariant mass of each muon pair was calculated using four-vector addition and filled into a histogram.

## Observed Distribution
The full dimuon invariant mass spectrum shows a large background at low masses and a clear resonance
around 90–92 GeV.
To study this resonance, the mass range was restricted to 60–120 GeV, where a Gaussian function
was fitted to the peak region.

## Interpretation
The Gaussian fit yields a mean value close to 91 GeV.
This value is consistent with the known mass of the Z boson.
The observed peak therefore corresponds to Z → μ⁺ μ⁻ decays in real LHC data.

## Conclusion
This project demonstrates a complete ROOT/PyROOT analysis workflow using real CERN Open Data,
including event looping, histogramming, fitting, visualization, and physics interpretation.
