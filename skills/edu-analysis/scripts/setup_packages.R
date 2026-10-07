# Install the R packages the edu-analysis helpers and adapters use, into R's user library.
# Only missing packages are installed; nothing is upgraded.
# Usage: Rscript setup_packages.R            core packages
#        Rscript setup_packages.R --all      core plus the packages of the trial methods (LPA/LCA, IRT, causal, meta, ...)
#        Rscript setup_packages.R pkg ...    the named packages
wanted <- c("jsonlite", "psych", "GPArotation", "lavaan", "semTools", "seminr", "QCA", "NCA",
            "lme4", "lmerTest", "afex", "emmeans")
optional <- c("mclust", "poLCA", "mirt", "MatchIt", "cobalt", "sandwich", "fixest", "rdrobust", "metafor", "metadat",
              "ordinal", "pscl", "BayesFactor", "cluster", "igraph", "TraMineR", "stm", "car")
args <- commandArgs(trailingOnly = TRUE)
if (identical(args, "--all")) wanted <- c(wanted, optional) else if (length(args)) wanted <- args
lib <- Sys.getenv("R_LIBS_USER")
if (!nzchar(lib)) lib <- .libPaths()[1]
dir.create(lib, recursive = TRUE, showWarnings = FALSE)
.libPaths(c(lib, .libPaths()))
missing <- wanted[!vapply(wanted, requireNamespace, logical(1), quietly = TRUE)]
if (length(missing)) {
  message("Installing into ", lib, ": ", paste(missing, collapse = ", "))
  install.packages(missing, lib = lib, repos = "https://cloud.r-project.org")
}
still <- wanted[!vapply(wanted, requireNamespace, logical(1), quietly = TRUE)]
for (p in setdiff(wanted, still)) cat(sprintf("%-12s %s\n", p, as.character(utils::packageVersion(p))))
if (length(still)) { message("Still missing: ", paste(still, collapse = ", ")); quit(status = 1) }
