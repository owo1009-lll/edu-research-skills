# edu_methods_patterns.R — pattern-finding methods: cluster analysis, social network analysis,
# lag sequential analysis and sequence analysis of learning logs, and structural topic models.
# Source edu_methods.R first (edu_need, edu_num, edu_save). Packages are loaded only by the
# function that needs them: cluster, igraph, TraMineR, stm. Every function returns a list of
# data frames plus `notes` so edu_save() works.

# ---------------------------------------------------------------- shared helper
edu_adjusted_rand <- function(a, b) {
  # Adjusted Rand index (Hubert & Arabie, 1985):
  # ARI = (sum_ij C(n_ij,2) - E) / (0.5 * (sum_i C(a_i,2) + sum_j C(b_j,2)) - E),
  # E = sum_i C(a_i,2) * sum_j C(b_j,2) / C(n,2). 1 = identical partitions, about 0 = chance.
  ok <- !is.na(a) & !is.na(b); tab <- table(a[ok], b[ok])
  c2 <- function(x) x * (x - 1) / 2
  idx <- sum(c2(tab)); ra <- sum(c2(rowSums(tab))); cb <- sum(c2(colSums(tab))); ex <- ra * cb / c2(sum(tab))
  mx <- (ra + cb) / 2
  if (mx == ex) return(1)
  (idx - ex) / (mx - ex)
}

edu_relabel_by_size <- function(cl) {
  # Cluster labels 1..k in decreasing size (ties by first appearance) so tables are stable across methods.
  tab <- table(factor(cl, levels = unique(cl)))
  map <- stats::setNames(seq_along(tab), names(tab)[order(-tab, seq_along(tab))])
  unname(map[as.character(cl)])
}

# ---------------------------------------------------------------- cluster analysis
edu_cluster <- function(d, vars, k = 2:8, method = c("kmeans", "ward", "pam"), scale = TRUE, seed = 123,
                        k_final = NULL, gap_B = 100, nstart = 25) {
  edu_need("cluster")
  method <- match.arg(method, c("kmeans", "ward", "pam"), several.ok = TRUE)
  x <- edu_num(d, vars); keep <- stats::complete.cases(x); x <- x[keep, , drop = FALSE]
  if (nrow(x) <= max(k)) stop("Fewer complete cases than the largest k")
  z <- if (scale) base::scale(x) else as.matrix(x)
  dz <- stats::dist(z); hc <- NULL
  part <- function(m, kk) {
    set.seed(seed)
    switch(m,
           kmeans = stats::kmeans(z, kk, nstart = nstart, iter.max = 100)$cluster,
           ward = { if (is.null(hc)) hc <<- stats::hclust(dz, method = "ward.D2"); stats::cutree(hc, kk) },
           pam = cluster::pam(dz, kk, diss = TRUE, cluster.only = TRUE))
  }
  gap_fun <- list(
    kmeans = function(xx, kk) list(cluster = stats::kmeans(xx, kk, nstart = nstart, iter.max = 100)$cluster),
    ward = function(xx, kk) list(cluster = stats::cutree(stats::hclust(stats::dist(xx), method = "ward.D2"), kk)),
    pam = function(xx, kk) list(cluster = cluster::pam(xx, kk, cluster.only = TRUE)))
  wss <- function(cl) sum(vapply(split(seq_len(nrow(z)), cl), function(i) sum(sweep(z[i, , drop = FALSE], 2, colMeans(z[i, , drop = FALSE]))^2), 0))
  fit <- list(); sel <- list(); parts <- list()
  for (m in method) {
    set.seed(seed)
    gp <- if (gap_B > 0) cluster::clusGap(z, gap_fun[[m]], K.max = max(k), B = gap_B, verbose = FALSE)$Tab else NULL
    rows <- lapply(k, function(kk) {
      cl <- part(m, kk); parts[[paste(m, kk)]] <<- cl
      data.frame(method = m, k = kk, within_ss = wss(cl),
                 avg_silhouette = summary(cluster::silhouette(cl, dz))$avg.width,
                 gap = if (is.null(gp)) NA else gp[kk, "gap"], gap_se = if (is.null(gp)) NA else gp[kk, "SE.sim"])
    })
    f <- do.call(rbind, rows); fit[[m]] <- f
    k_gap <- if (is.null(gp)) NA else cluster::maxSE(gp[, "gap"], gp[, "SE.sim"], method = "Tibs2001SEmax")
    sel[[m]] <- data.frame(method = m, k_max_silhouette = f$k[which.max(f$avg_silhouette)], k_gap_rule = k_gap)
  }
  fit <- do.call(rbind, fit); sel <- do.call(rbind, sel)
  kf <- if (is.null(k_final)) sel$k_max_silhouette[1] else k_final
  mem <- data.frame(row = which(keep))
  cr <- list(); cz <- list()
  for (m in method) {
    cl <- edu_relabel_by_size(if (!is.null(parts[[paste(m, kf)]])) parts[[paste(m, kf)]] else part(m, kf))
    mem[[m]] <- cl
    n <- as.vector(table(factor(cl, levels = seq_len(kf))))
    cr[[m]] <- data.frame(method = m, cluster = seq_len(kf), n = n, pct = 100 * n / length(cl),
                          stats::aggregate(x, list(cl = cl), mean)[, -1, drop = FALSE], check.names = FALSE)
    cz[[m]] <- data.frame(method = m, cluster = seq_len(kf), n = n,
                          stats::aggregate(as.data.frame(base::scale(x)), list(cl = cl), mean)[, -1, drop = FALSE], check.names = FALSE)
  }
  out <- list(fit = fit, selection = cbind(sel, k_used = kf), centroids_raw = do.call(rbind, cr),
              centroids_z = do.call(rbind, cz))
  if (length(method) > 1) {
    pr <- utils::combn(method, 2)
    out$agreement <- data.frame(method_a = pr[1, ], method_b = pr[2, ], k = kf,
                                ARI = apply(pr, 2, function(p) edu_adjusted_rand(mem[[p[1]]], mem[[p[2]]])))
  }
  out$membership <- mem
  out$notes <- c(sprintf("n = %d complete cases (%d dropped); %s; distances are Euclidean.", nrow(x), sum(!keep),
                         if (scale) "variables were z-standardized before clustering" else "variables were used in raw units"),
                 sprintf("k-means: %d random starts (seed %d); Ward: ward.D2 on Euclidean distances; PAM: medoids on the same distances. Clusters are numbered by size.", nstart, seed),
                 sprintf("Elbow = within-cluster SS on the clustering scale; silhouette = mean silhouette width (> .50 reasonable, > .70 strong structure; Kaufman & Rousseeuw, 1990); gap statistic with %d reference sets and the Tibshirani et al. (2001) rule (smallest k with gap(k) >= gap(k+1) - SE).", gap_B),
                 sprintf("k used = %d (%s). Confirm k with interpretability and cluster sizes (avoid clusters below about 5%% of the sample); indices often disagree.", kf, if (is.null(k_final)) "largest average silhouette of the first method" else "set by the analyst"),
                 "Adjusted Rand index (Hubert & Arabie, 1985) compares methods: 1 = identical partitions, about 0 = chance agreement; low agreement means the cluster solution is not robust.",
                 "Clustering is descriptive: it always returns k groups, even in data without groups, and gives no test of k. k-means favours spherical, similar-sized clusters; every case gets a hard assignment.",
                 "Prefer latent profile analysis (latent-group functions) when you need model-based class enumeration (BIC, entropy, BLRT), posterior membership probabilities, class-specific variances, or covariates and distal outcomes (three-step).")
  out
}

# ---------------------------------------------------------------- social network analysis
edu_network <- function(edges, directed = TRUE, weight = NULL, nodes = NULL, community = c("louvain", "walktrap"), seed = 123) {
  edu_need("igraph")
  community <- match.arg(community)
  el <- data.frame(from = as.character(edges[[1]]), to = as.character(edges[[2]]), stringsAsFactors = FALSE)
  el$weight <- if (is.null(weight)) 1 else suppressWarnings(as.numeric(edges[[weight]]))
  el <- el[!is.na(el$from) & !is.na(el$to) & el$from != "" & el$to != "" & !is.na(el$weight), ]
  vx <- NULL
  if (!is.null(nodes)) {
    vx <- if (is.data.frame(nodes)) nodes else data.frame(name = nodes)
    names(vx)[1] <- "name"; vx$name <- as.character(vx$name)
    extra <- setdiff(unique(c(el$from, el$to)), vx$name)
    if (length(extra)) stop("Edges name nodes missing from `nodes`: ", paste(utils::head(extra, 5), collapse = ", "))
  }
  g0 <- igraph::graph_from_data_frame(el, directed = directed, vertices = vx)
  loops <- sum(igraph::which_loop(g0)); multi <- sum(igraph::which_multiple(g0))
  g <- igraph::simplify(g0, remove.multiple = TRUE, remove.loops = TRUE, edge.attr.comb = list(weight = "sum", "ignore"))
  w <- if (is.null(weight)) NULL else igraph::E(g)$weight
  if (is.null(weight)) g <- igraph::delete_edge_attr(g, "weight")
  gu <- if (directed) igraph::as_undirected(g, mode = "collapse", edge.attr.comb = list(weight = "sum", "ignore")) else g
  wu <- if (is.null(weight)) NULL else igraph::E(gu)$weight
  n <- igraph::vcount(g); mode_d <- if (directed) "in" else "all"
  comp <- igraph::components(g, mode = "weak")
  set.seed(seed)
  cm <- if (community == "louvain") igraph::cluster_louvain(gu, weights = wu) else igraph::cluster_walktrap(gu, weights = wu)
  ev <- igraph::eigen_centrality(gu, weights = wu)$vector
  net <- data.frame(measure = c("nodes", "edges", "density", if (directed) "reciprocity", "transitivity (global)",
                                "mean distance", "diameter", "weak components", "largest component share",
                                if (directed) c("in-degree centralization", "out-degree centralization") else "degree centralization",
                                "betweenness centralization", "closeness centralization", "eigenvector centralization",
                                "communities", "modularity"),
                    value = c(n, igraph::ecount(g), igraph::edge_density(g), if (directed) igraph::reciprocity(g),
                              igraph::transitivity(gu, type = "global"),
                              igraph::mean_distance(g, weights = NA, directed = directed, unconnected = TRUE),
                              igraph::diameter(g, directed = directed, unconnected = TRUE, weights = NA),
                              comp$no, max(comp$csize) / n,
                              if (directed) c(igraph::centr_degree(g, mode = "in", loops = FALSE)$centralization,
                                              igraph::centr_degree(g, mode = "out", loops = FALSE)$centralization)
                              else igraph::centr_degree(g, mode = "all", loops = FALSE)$centralization,
                              igraph::centr_betw(g, directed = directed)$centralization,
                              if (igraph::is_connected(g, mode = "strong")) igraph::centr_clo(g, mode = if (directed) "out" else "all")$centralization else NA,
                              igraph::centr_eigen(gu)$centralization,
                              length(igraph::sizes(cm)), igraph::modularity(gu, igraph::membership(cm), weights = wu)))
  nd <- data.frame(node = igraph::V(g)$name, stringsAsFactors = FALSE)
  if (directed) {
    nd$in_degree <- igraph::degree(g, mode = "in"); nd$out_degree <- igraph::degree(g, mode = "out")
    if (!is.null(weight)) { nd$in_strength <- igraph::strength(g, mode = "in"); nd$out_strength <- igraph::strength(g, mode = "out") }
  } else {
    nd$degree <- igraph::degree(g)
    if (!is.null(weight)) nd$strength <- igraph::strength(g)
  }
  nd$betweenness <- igraph::betweenness(g, directed = directed, weights = NA)
  nd$betweenness_norm <- igraph::betweenness(g, directed = directed, weights = NA, normalized = TRUE)
  if (directed) {
    nd$closeness_in <- igraph::closeness(g, mode = "in", weights = NA, normalized = TRUE)
    nd$closeness_out <- igraph::closeness(g, mode = "out", weights = NA, normalized = TRUE)
  } else nd$closeness <- igraph::closeness(g, mode = "all", weights = NA, normalized = TRUE)
  nd$eigenvector <- unname(ev); nd$community <- as.integer(igraph::membership(cm))
  if (!is.null(vx) && ncol(vx) > 1) nd <- merge(nd, vx, by.x = "node", by.y = "name", all.x = TRUE, sort = FALSE)
  sz <- igraph::sizes(cm)
  list(network = net, nodes = nd,
       communities = data.frame(community = as.integer(names(sz)), size = as.vector(sz)),
       graph = igraph::set_vertex_attr(g, "community", value = as.integer(igraph::membership(cm))),
       notes = c(sprintf("%s network: %d nodes, %d ties%s; %d self-loops and %d duplicate ties were removed (duplicate weights summed).",
                         if (directed) "Directed" else "Undirected", n, igraph::ecount(g),
                         if (is.null(weight)) "" else sprintf(" weighted by '%s'", weight), loops, multi),
                 "Density, reciprocity and centralization use the binary ties. Transitivity, eigenvector centrality and communities use the undirected (symmetrized) network; tie weights are used for strength, eigenvector and communities.",
                 "Betweenness, closeness, mean distance and diameter count steps (weights ignored; igraph would read weights as distances, but education tie weights usually mean strength). Mean distance averages reachable pairs only; closeness uses reachable nodes only, and closeness centralization is reported only for connected networks.",
                 sprintf("Communities: %s (seed %d) on the symmetrized network; modularity Q > .30 is the usual mark of clear community structure (Newman & Girvan, 2004). Louvain results can vary slightly with the seed.",
                         if (community == "louvain") "Louvain (Blondel et al., 2008)" else "walktrap (Pons & Latapy, 2005)", seed),
                 "Network measures describe this bounded network; missing respondents remove their ties and bias degree and centrality downward. Significance of differences between nodes needs permutation tests (e.g., QAP), not ordinary p values."))
}

edu_network_plot <- function(x, file = "output/network.png", label = TRUE, seed = 123, ...) {
  # x: an edu_network() result or an edge list (passed to edu_network with ...). Node size = in-degree
  # (degree when undirected), colour = community, Fruchterman-Reingold layout with a fixed seed.
  edu_need("igraph")
  res <- if (is.data.frame(x)) edu_network(x, ...) else x
  g <- res$graph; dirn <- igraph::is_directed(g)
  deg <- igraph::degree(g, mode = if (dirn) "in" else "all")
  pal <- c("#59788E", "#C07A50", "#6B9A6B", "#A05C7B", "#8C8C3E", "#4E8C8C", "#9E6B4E", "#6F6FA6")
  com <- igraph::V(g)$community
  dir.create(dirname(file), showWarnings = FALSE, recursive = TRUE)
  set.seed(seed); lay <- igraph::layout_with_fr(g)
  grDevices::png(file, width = 1800, height = 1600, res = 300)
  on.exit(grDevices::dev.off())
  graphics::par(mar = c(0, 0, 0, 0))
  plot(g, layout = lay, vertex.size = 4 + 10 * sqrt(deg / max(1, max(deg))),
       vertex.color = pal[(com - 1) %% length(pal) + 1], vertex.frame.color = "white",
       vertex.label = if (label) igraph::V(g)$name else NA, vertex.label.cex = 0.45, vertex.label.color = "grey10",
       edge.color = grDevices::adjustcolor("grey40", .5), edge.arrow.size = 0.25, edge.width = 0.6)
  invisible(file)
}

# ---------------------------------------------------------------- lag sequential analysis
edu_lsa <- function(d, actor, order, code, lag = 1, self_transitions = TRUE, z_crit = 1.96) {
  # Transitions are formed within each actor's sequence (sorted by `order`), never across actors.
  dd <- d[!is.na(d[[actor]]), c(actor, order, code)]
  dd <- dd[base::order(as.character(dd[[actor]]), dd[[order]]), ]
  codes <- if (is.factor(d[[code]])) levels(droplevels(d[[code]])) else sort(unique(as.character(stats::na.omit(dd[[code]]))))
  pairs <- do.call(rbind, lapply(split(as.character(dd[[code]]), as.character(dd[[actor]])), function(v) {
    if (length(v) <= lag) return(NULL)
    data.frame(given = v[seq_len(length(v) - lag)], target = v[(lag + 1):length(v)], stringsAsFactors = FALSE)
  }))
  pairs <- pairs[!is.na(pairs$given) & !is.na(pairs$target), ]
  O <- table(factor(pairs$given, levels = codes), factor(pairs$target, levels = codes))
  N <- sum(O); r <- rowSums(O); cc <- colSums(O); K <- length(codes)
  if (!self_transitions && sum(diag(O)) > 0) stop("self_transitions = FALSE but ", sum(diag(O)), " repeated codes occur; merge repeats first or keep self_transitions = TRUE")
  cells <- data.frame(given = rep(codes, times = K), target = rep(codes, each = K), observed = as.vector(O), stringsAsFactors = FALSE)
  if (self_transitions) {
    # Independence: e_ij = f_i+ f_+j / N; adjusted residual (Allison & Liker, 1982; Bakeman & Quera, 2011)
    # z_ij = (f_ij - e_ij) / sqrt(e_ij (1 - f_i+/N) (1 - f_+j/N)).
    E <- outer(r, cc) / N
    Z <- (O - E) / sqrt(E * outer(1 - r / N, 1 - cc / N))
    cells$expected <- as.vector(E); cells$z <- as.vector(Z)
    df <- (K - 1)^2
  } else {
    # Quasi-independence with structural zeros on the diagonal: expected counts from the Poisson log-linear model
    # given + target fitted to the off-diagonal cells (iterative proportional fitting gives the same fit);
    # z = standardized Pearson (adjusted) residual (Bakeman & Quera, 2011, ch. 10).
    off <- cells$given != cells$target & r[cells$given] > 0 & cc[cells$target] > 0
    fit <- stats::glm(observed ~ factor(given) + factor(target), family = stats::poisson, data = cells[off, ])
    cells$expected <- NA; cells$z <- NA
    cells$expected[off] <- stats::fitted(fit); cells$z[off] <- stats::rstandard(fit, type = "pearson")
    df <- fit$df.residual
  }
  cells$cond_prob <- ifelse(r[cells$given] > 0, cells$observed / r[cells$given], NA)
  a <- cells$observed; b <- r[cells$given] - a; c2 <- cc[cells$target] - a; dd2 <- N - r[cells$given] - cc[cells$target] + a
  cells$yule_q <- ifelse(a * dd2 + b * c2 > 0, (a * dd2 - b * c2) / (a * dd2 + b * c2), NA)
  cells$p <- 2 * stats::pnorm(-abs(cells$z))
  cells$sig <- ifelse(is.na(cells$z), "", ifelse(cells$z > z_crit, "+", ifelse(cells$z < -z_crit, "-", "")))
  ok <- !is.na(cells$expected) & cells$expected > 0
  x2 <- sum((cells$observed[ok] - cells$expected[ok])^2 / cells$expected[ok])
  wide <- function(v) { m <- matrix(v, K, K, dimnames = list(codes, codes)); data.frame(given = codes, m, check.names = FALSE, row.names = NULL) }
  sig <- cells[cells$sig == "+", ]; sig <- sig[base::order(-sig$z), ]
  list(summary = data.frame(actors = length(unique(dd[[actor]])), events = nrow(dd), transitions = N, codes = K, lag = lag,
                            chisq = x2, df = df, p = stats::pchisq(x2, df, lower.tail = FALSE),
                            cells_expected_below_5 = sum(cells$expected[ok] < 5)),
       transitions = cells, observed = wide(as.vector(O)), z = wide(cells$z), significant = sig,
       notes = c(sprintf("Lag-%d transitions within actors (%d transitions from %d actors); %s.", lag, N, length(unique(dd[[actor]])),
                         if (self_transitions) "repeats of the same code are allowed (independence model)" else "repeats are structural zeros (quasi-independence model)"),
                 sprintf("Adjusted residual z (Allison & Liker, 1982; Bakeman & Quera, 2011): z > %.2f marks a transition that occurs more often than chance ('+'), z < -%.2f less often ('-'). Yule's Q (-1 to 1) is the effect size, comparable across studies; cond_prob = P(target | given).", z_crit, z_crit),
                 "The overall chi-square tests independence of given and target codes. Many cells are tested at once, so treat single significant cells with care (Bonferroni or a stricter z when the table is large).",
                 sprintf("%d cells have expected counts below 5; z is unreliable there (Bakeman & Quera recommend enough transitions that expected counts are at least about 5).", sum(cells$expected[ok] < 5)),
                 "Transitions from all actors are pooled, so the table assumes actors follow the same transition pattern; frequent actors weigh more. Lag sequential analysis shows sequential association, not cause.",
                 "If consecutive identical codes were merged during coding, set self_transitions = FALSE; otherwise the diagonal is a structural zero and the independence model is wrong."))
}

# ---------------------------------------------------------------- sequence analysis (TraMineR)
edu_seq_string <- function(v) {
  v <- v[!is.na(v)]; r <- rle(v)
  paste0(r$values, "(", r$lengths, ")", collapse = "-")
}

edu_sequence <- function(d, id, time, state, k = 2:6, k_final = NULL, sm = "TRATE", indel = "auto", seed = 123) {
  edu_need(c("TraMineR", "cluster"))
  dd <- d[!is.na(d[[id]]) & !is.na(d[[time]]), c(id, time, state)]
  if (any(duplicated(dd[c(id, time)]))) stop("Each id must have at most one state per time point")
  ids <- unique(as.character(dd[[id]])); tms <- sort(unique(dd[[time]]))
  alph <- if (is.factor(d[[state]])) levels(droplevels(d[[state]])) else sort(unique(as.character(stats::na.omit(dd[[state]]))))
  W <- matrix(NA_character_, length(ids), length(tms), dimnames = list(ids, as.character(tms)))
  W[cbind(match(as.character(dd[[id]]), ids), match(dd[[time]], tms))] <- as.character(dd[[state]])
  utils::capture.output(sq <- suppressMessages(TraMineR::seqdef(as.data.frame(W, stringsAsFactors = FALSE), alphabet = alph,
                                                                 id = ids, cnames = as.character(tms))))
  miss <- any(as.matrix(sq) == attr(sq, "nr"))
  sd <- TraMineR::seqstatd(sq)
  dist_t <- data.frame(time = tms, t(sd$Frequencies), n_valid = as.vector(sd$ValidStates), entropy = as.vector(sd$Entropy),
                       check.names = FALSE, row.names = NULL)
  tr <- suppressMessages(TraMineR::seqtrate(sq))
  trt <- data.frame(from = alph, matrix(tr, length(alph), dimnames = list(NULL, alph)), check.names = FALSE)
  mt <- TraMineR::seqmeant(sq)
  utils::capture.output(D <- suppressMessages(TraMineR::seqdist(sq, method = "OM", sm = sm, indel = indel, with.missing = miss)))
  hc <- stats::hclust(stats::as.dist(D), method = "ward.D2")
  k <- k[k < length(ids)]
  sil <- data.frame(k = k, avg_silhouette = vapply(k, function(kk) summary(cluster::silhouette(stats::cutree(hc, kk), dmatrix = D))$avg.width, 0))
  kf <- if (is.null(k_final)) sil$k[which.max(sil$avg_silhouette)] else k_final
  cl <- edu_relabel_by_size(stats::cutree(hc, kf))
  M <- as.matrix(sq); M[M == attr(sq, "nr") | M == attr(sq, "void")] <- NA
  types <- do.call(rbind, lapply(seq_len(kf), function(j) {
    i <- which(cl == j); med <- i[which.min(rowSums(D[i, i, drop = FALSE]))]
    share <- vapply(alph, function(s) mean(M[i, ] == s, na.rm = TRUE), 0)
    data.frame(type = j, n = length(i), pct = 100 * length(i) / length(cl), medoid_id = ids[med],
               medoid_sequence = edu_seq_string(M[med, ]), t(share), check.names = FALSE)
  }))
  list(states = data.frame(state = alph, mean_time = as.vector(mt[, "Mean"]), share = as.vector(mt[, "Mean"]) / sum(mt[, "Mean"])),
       distribution = dist_t, transition_rates = trt, cluster_fit = sil, types = types,
       membership = data.frame(id = ids, type = cl),
       notes = c(sprintf("%d sequences, %d time points, %d states%s.", length(ids), length(tms), length(alph),
                         if (miss) "; gaps inside sequences are kept as missing and treated as an extra state in OM" else ""),
                 "distribution = cross-sectional state proportions at each time point (the data behind a state distribution plot); entropy = Shannon entropy of that distribution. transition_rates = P(state at t+1 | state at t), pooled over time.",
                 sprintf("Optimal matching distances: substitution costs %s, indel %s (Gabadinho et al., 2011). Cost choices change the typology; report them and check robustness with another cost setting (Studer & Ritschard, 2016).",
                         if (identical(sm, "TRATE")) "2 - p(i->j) - p(j->i) from the observed transition rates" else as.character(sm), as.character(indel)),
                 sprintf("Sequence types: Ward (ward.D2) clustering of the OM distances; k = %d (%s). Types are numbered by size; medoid = the most central sequence, written as state(duration).",
                         kf, if (is.null(k_final)) "largest average silhouette" else "set by the analyst"),
                 "Sequence types are a descriptive typology, not latent classes; with weak structure (silhouette < .25) say so and interpret types with caution. Sequences should share one time grid (sessions, weeks)."))
}

# ---------------------------------------------------------------- structural topic model (stm)
edu_topics <- function(d, text_col, k = 3:10, segmented = TRUE, covariates = NULL, id_col = NULL, k_final = NULL,
                       stopwords = NULL, lower_thresh = 1, n_words = 10, n_docs = 3, seed = 123) {
  edu_need("stm")
  text <- as.character(d[[text_col]]); ids <- if (is.null(id_col)) as.character(seq_len(nrow(d))) else as.character(d[[id_col]])
  text[is.na(text)] <- ""
  if (segmented) toks <- strsplit(trimws(text), "\\s+")
  else {
    if (any(grepl("[一-鿿]", text))) stop("Chinese text must be segmented first: run scripts/segment_zh.py, then call edu_topics(segmented = TRUE)")
    toks <- strsplit(trimws(gsub("[[:punct:][:digit:][:space:]]+", " ", tolower(text))), " ")
  }
  toks <- lapply(toks, function(t) t[nzchar(t) & !t %in% stopwords])
  meta <- if (is.null(covariates)) data.frame(.doc = seq_along(text)) else d[covariates]
  meta[] <- lapply(meta, function(v) if (is.character(v)) factor(v) else v)
  keep <- lengths(toks) > 0 & stats::complete.cases(meta)
  vocab <- sort(unique(unlist(toks[keep])))
  docs <- lapply(toks[keep], function(t) { tb <- table(match(t, vocab)); rbind(as.integer(names(tb)), as.integer(tb)) })
  utils::capture.output(pp <- stm::prepDocuments(docs, vocab, meta[keep, , drop = FALSE], lower.thresh = lower_thresh, verbose = FALSE))
  used <- ids[keep]; if (length(pp$docs.removed)) used <- used[-pp$docs.removed]
  prev <- if (is.null(covariates)) NULL else stats::as.formula(paste("~", paste(covariates, collapse = " + ")))
  utils::capture.output(sk <- stm::searchK(pp$documents, pp$vocab, K = k, prevalence = prev, data = pp$meta,
                                           init.type = "Spectral", heldout.seed = seed, verbose = FALSE))
  sr <- as.data.frame(lapply(sk$results, function(v) as.numeric(unlist(v))))
  search <- data.frame(k = sr$K, semantic_coherence = sr$semcoh, exclusivity = sr$exclus, heldout_likelihood = sr$heldout,
                       residual = sr$residual, lower_bound = sr$lbound)
  if (is.null(k_final)) {
    zs <- function(v) if (length(v) > 1 && stats::sd(v) > 0) (v - mean(v)) / stats::sd(v) else 0 * v
    kf <- search$k[which.max(zs(search$semantic_coherence) + zs(search$exclusivity))]
  } else kf <- k_final
  utils::capture.output(fit <- stm::stm(pp$documents, pp$vocab, K = kf, prevalence = prev, data = pp$meta,
                                        init.type = "Spectral", seed = seed, verbose = FALSE))
  lt <- stm::labelTopics(fit, n = n_words); th <- fit$theta
  dom <- max.col(th, ties.method = "first")
  topics <- data.frame(topic = seq_len(kf), mean_proportion = colMeans(th),
                       docs_dominant = tabulate(dom, kf),
                       semantic_coherence = stm::semanticCoherence(fit, pp$documents), exclusivity = stm::exclusivity(fit),
                       prob_words = apply(lt$prob, 1, paste, collapse = ", "), frex_words = apply(lt$frex, 1, paste, collapse = ", "))
  rep_docs <- do.call(rbind, lapply(seq_len(kf), function(j) {
    o <- utils::head(order(-th[, j]), n_docs); data.frame(topic = j, rank = seq_along(o), doc_id = used[o], theta = th[o, j])
  }))
  out <- list(corpus = data.frame(documents_input = length(text), documents_used = length(used), vocabulary = length(pp$vocab),
                                  tokens = sum(vapply(pp$documents, function(m) sum(m[2, ]), 0))),
              search = search, topics = topics, representative_docs = rep_docs,
              theta = data.frame(doc_id = used, round(th, 4), check.names = FALSE))
  names(out$theta)[-1] <- paste0("topic", seq_len(kf))
  if (!is.null(covariates)) {
    set.seed(seed)
    ef <- stm::estimateEffect(stats::as.formula(paste("1:", kf, " ~ ", paste(covariates, collapse = " + "))), fit,
                              metadata = pp$meta, uncertainty = "Global")
    se <- summary(ef)
    out$effects <- do.call(rbind, lapply(seq_along(se$tables), function(j) {
      tb <- se$tables[[j]]
      data.frame(topic = se$topics[j], term = rownames(tb), estimate = tb[, 1], se = tb[, 2], t = tb[, 3], p = tb[, 4], row.names = NULL)
    }))
  }
  out$model <- fit
  out$notes <- c(sprintf("%d of %d documents used (empty documents%s dropped); words in %d or fewer documents removed; vocabulary %d.",
                         length(used), length(text), if (is.null(covariates)) "" else " and documents with missing covariates", lower_thresh, length(pp$vocab)),
                 if (segmented) "Text was used as given (space-separated tokens). Chinese text must be segmented with scripts/segment_zh.py (jieba, user dictionary, stop words) before this step." else "English text: lower-cased, punctuation and digits removed; no stemming; stop words only if supplied.",
                 sprintf("Structural topic model (Roberts et al., 2014, 2019), spectral initialization (deterministic), seed %d%s.", seed,
                         if (is.null(covariates)) "" else paste0("; topic prevalence ~ ", paste(covariates, collapse = " + "))),
                 sprintf("k = %d (%s). searchK compares semantic coherence (Mimno et al., 2011) and exclusivity (higher is better for both, and they trade off), held-out likelihood and residuals; no index fixes k, so read the topics of neighbouring k before deciding.",
                         kf, if (is.null(k_final)) "best sum of standardized coherence and exclusivity" else "set by the analyst"),
                 "prob_words = highest probability words; frex_words = frequent and exclusive words (FREX), usually better for naming topics. representative_docs lists document IDs only: read those texts to name and validate each topic.",
                 if (!is.null(covariates)) "effects: estimateEffect regression of topic proportions on the covariates with global uncertainty (composition method); estimates are differences in expected topic proportion, associations not causal effects.",
                 "Topics are a statistical summary of word co-occurrence; validate them by reading documents and do not treat topic proportions as measured constructs without validation.")
  out
}
