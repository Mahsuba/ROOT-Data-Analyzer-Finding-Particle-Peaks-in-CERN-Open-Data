import ROOT


# PROJECT: ROOT Data Analyzer – Finding Particle Peaks in CERN Data
# FILE: analyze_dimuon_mass.py

# Our goal is:
#   - Open CERN DoubleMuon data (NanoAOD_DoubleMuon.root)
#   - Build dimuon invariant mass histogram
#   - Look for peaks (especially Z boson around 91 GeV)
#   - Fit a Gaussian to the Z peak region
#   - Save a nice plot as PNG




root_file_name = "NanoAOD_DoubleMuon.root"

print(f"Opening ROOT file: {root_file_name}")
root_file = ROOT.TFile(root_file_name)


event_tree = root_file.Events
print("Loaded TTree named 'Events'")



number_of_bins   = 100
minimum_mass_GeV = 0.0
maximum_mass_GeV = 200.0

dimuon_mass_histogram = ROOT.TH1F(
    "dimuon_mass_histogram",
    "Dimuon invariant mass; m_{#mu#mu} (GeV); Number of pairs",
    number_of_bins,
    minimum_mass_GeV,
    maximum_mass_GeV
)



max_events_to_process = 200000

print("Looping over events and building dimuon mass...")

for event_index, event in enumerate(event_tree):


    if max_events_to_process > 0 and event_index >= max_events_to_process:
        break

    # ok we will see how many muons are in this event?
    number_of_muons = event.nMuon

    # but we need at least 2 muons to make a pair
    if number_of_muons < 2:
        continue

    # lets loop over all unique muon pairs (first_muon_index < second_muon_index)
    for first_muon_index in range(number_of_muons):
        for second_muon_index in range(first_muon_index + 1, number_of_muons):

            # now we need to get kinematic information for the first muon
            muon1_pt   = event.Muon_pt[first_muon_index]
            muon1_eta  = event.Muon_eta[first_muon_index]
            muon1_phi  = event.Muon_phi[first_muon_index]
            muon1_mass = event.Muon_mass[first_muon_index]

            # and for the 2nd muon's kinematic information
            muon2_pt   = event.Muon_pt[second_muon_index]
            muon2_eta  = event.Muon_eta[second_muon_index]
            muon2_phi  = event.Muon_phi[second_muon_index]
            muon2_mass = event.Muon_mass[second_muon_index]

            # lets build 4-vectors for each muon
            
            muon1_four_vector = ROOT.TLorentzVector()
            muon2_four_vector = ROOT.TLorentzVector()

            muon1_four_vector.SetPtEtaPhiM(
                muon1_pt, muon1_eta, muon1_phi, muon1_mass
            )

            muon2_four_vector.SetPtEtaPhiM(
                muon2_pt, muon2_eta, muon2_phi, muon2_mass
            )


            dimuon_four_vector = muon1_four_vector + muon2_four_vector
            dimuon_invariant_mass = dimuon_four_vector.M()

            
            dimuon_mass_histogram.Fill(dimuon_invariant_mass)

print("Finished looping over events.")
print(f"Total dimuon pairs (histogram entries): {dimuon_mass_histogram.GetEntries()}")


# we need to draw full mass spectrum (0–200 GeV)

canvas_full = ROOT.TCanvas(
    "canvas_full",
    "Dimuon invariant mass – full range",
    800,
    600
)

dimuon_mass_histogram.SetLineColor(ROOT.kMagenta)
dimuon_mass_histogram.SetFillColor(ROOT.kMagenta - 9)
dimuon_mass_histogram.SetFillStyle(3004)

# lets set a clear title 
dimuon_mass_histogram.SetTitle("Dimuon invariant mass; m_{#mu#mu} (GeV); Number of pairs")

dimuon_mass_histogram.Draw()

canvas_full.SaveAs("dimuon_mass_full.png")
print("Saved full-range plot as dimuon_mass_full.png")


# we need to zoom in around the Z boson peak and fit a gaussian

# make a new canvas for the zoomed-in Z peak
canvas_zoom = ROOT.TCanvas(
    "canvas_zoom",
    "Dimuon invariant mass – Z peak",
    800,
    600
)

# we want to see roughly from 60 to 120 GeV to focus on the Z
z_peak_min = 60.0
z_peak_max = 120.0

# so, set X-axis display range to zoom in
dimuon_mass_histogram.GetXaxis().SetRangeUser(z_peak_min, z_peak_max)

# now, create a Gaussian function for fitting in this range
gaussian_fit = ROOT.TF1(
    "gaussian_fit",
    "gaus",          # its already built-in Gaussian,dont get confused haha
    z_peak_min,
    z_peak_max
)

print("Fitting Gaussian to Z peak region (60–120 GeV)...")
dimuon_mass_histogram.Fit(gaussian_fit, "R")  # "R" = respect function range

# little style the histogram and fit line
dimuon_mass_histogram.SetLineColor(ROOT.kMagenta)
dimuon_mass_histogram.SetFillColor(ROOT.kMagenta - 9)
dimuon_mass_histogram.SetFillStyle(3004)

gaussian_fit.SetLineColor(ROOT.kBlue)
gaussian_fit.SetLineStyle(2)

# draw histogram and fit on same canvas
dimuon_mass_histogram.Draw()
gaussian_fit.Draw("same")

# lets add legend
legend = ROOT.TLegend(0.60, 0.55, 0.82, 0.68)
legend.SetTextSize(0.025)
legend.SetBorderSize(0)
legend.SetFillStyle(0)
legend.AddEntry(dimuon_mass_histogram, "Dimuon data", "f")
legend.AddEntry(gaussian_fit, "Gaussian fit (Z peak)", "l")
legend.Draw()

# save zoomed-in plot
canvas_zoom.SaveAs("dimuon_mass_Zpeak.png")
print(" Saved Z-peak plot as dimuon_mass_Zpeak.png")

# Print Gaussian fit parameters (mean ≈ Z mass)
fit_mean  = gaussian_fit.GetParameter(1)
fit_sigma = gaussian_fit.GetParameter(2)
print(f"Gaussian mean (peak position): {fit_mean:.2f} GeV")
print(f"📌Gaussian sigma (width):        {fit_sigma:.2f} GeV")

print("Analysis complete! You can now use the plots in your report.")
