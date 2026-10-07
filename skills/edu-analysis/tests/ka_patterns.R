# Known-answer checks for edu_methods_patterns.R (cluster, network, lag sequential analysis,
# sequence analysis, topic models). Relies on check(), safely(), edu_methods.R and edu_methods_patterns.R.
if (!exists("edu_cluster")) {
  pf <- file.path(here, "..", "scripts", "edu_methods_patterns.R")
  if (file.exists(pf)) source(pf, encoding = "UTF-8")
}
pkgs_ok <- function(p) all(vapply(p, requireNamespace, logical(1), quietly = TRUE))

if (pkgs_ok("cluster")) safely("cluster analysis", {
  # Adjusted Rand index by hand: a = 111222, b = 112233. sum C(n_ij,2) = 2; row pairs 3+3 = 6;
  # column pairs 1+1+1 = 3; C(6,2) = 15; expected = 6*3/15 = 1.2; max = (6+3)/2 = 4.5;
  # ARI = (2 - 1.2) / (4.5 - 1.2) = 0.8 / 3.3 (Hubert & Arabie, 1985).
  check("ARI hand example", edu_adjusted_rand(c(1, 1, 1, 2, 2, 2), c(1, 1, 2, 2, 3, 3)), 0.8 / 3.3, 1e-12)
  check("ARI invariant to label names", edu_adjusted_rand(c(1, 1, 2, 2), c("b", "b", "a", "a")), 1, 1e-12)
  # iris, raw units, k-means k = 3: the widely reproduced optimum, total within SS = 78.851
  # (between_SS / total_SS = 88.4%), cluster sizes 50 / 62 / 38.
  r <- edu_cluster(datasets::iris, names(datasets::iris)[1:4], k = 3, method = "kmeans", scale = FALSE, gap_B = 0)
  check("k-means iris within SS = 78.851", r$fit$within_ss, 78.85144, 1e-3)
  check("k-means iris sizes 62/50/38", r$centroids_raw$n, c(62, 50, 38), 0)
  # ruspini, PAM k = 4: average silhouette width 0.74 (Kaufman & Rousseeuw, 1990; cluster ?silhouette example),
  # and k = 4 is the best k by silhouette among 2..6.
  r <- edu_cluster(cluster::ruspini, c("x", "y"), k = 2:6, method = "pam", scale = FALSE, gap_B = 0)
  check("PAM ruspini k = 4 average silhouette 0.74", r$fit$avg_silhouette[r$fit$k == 4], 0.74, 0.005)
  check("silhouette picks k = 4 for ruspini", r$selection$k_max_silhouette, 4, 0)
  # Simulated well-separated clusters (centres 10 SD apart): every method recovers the truth (ARI = 1),
  # silhouette and the gap rule both select k = 3, and the methods agree perfectly.
  set.seed(42); truth <- rep(1:3, c(60, 50, 40))
  sim <- data.frame(a = c(0, 10, 0)[truth] + stats::rnorm(150), b = c(0, 0, 10)[truth] + stats::rnorm(150))
  r <- edu_cluster(sim, c("a", "b"), k = 2:5, gap_B = 20)
  check("recovered k (silhouette, gap) = 3", c(r$selection$k_max_silhouette, r$selection$k_gap_rule), rep(3, 6), 0)
  check("ARI with planted clusters = 1 (kmeans, ward, pam)",
        vapply(c("kmeans", "ward", "pam"), function(m) edu_adjusted_rand(r$membership[[m]], truth), 0), c(1, 1, 1), 1e-12)
  check("ARI between methods = 1", r$agreement$ARI, c(1, 1, 1), 1e-12)
  check("centroids in z units have mean 0 (weighted by size)", sum(r$centroids_z$n[1:3] * r$centroids_z$a[1:3]) / 150, 0, 1e-10)
}) else message("skipped: cluster analysis (package cluster missing)")

if (pkgs_ok("igraph")) safely("social network analysis", {
  # Zachary (1977) karate club: 34 nodes, 78 ties; density 78/561 = .1390; global transitivity .2557;
  # mean distance 2.408; degree of the instructor (1) = 16 and the administrator (34) = 17;
  # betweenness of node 1 = 231.07 (Newman, 2010); Louvain modularity .42 (Blondel et al., 2008).
  kc <- igraph::as_data_frame(igraph::make_graph("Zachary"))
  r <- edu_network(kc, directed = FALSE)
  v <- function(m) r$network$value[r$network$measure == m]
  check("karate density, transitivity, mean distance", c(v("density"), v("transitivity (global)"), v("mean distance")),
        c(78 / 561, 0.2557, 2.408), c(1e-10, 1e-4, 1e-3))
  check("karate degree of nodes 1 and 34", r$nodes$degree[match(c("1", "34"), r$nodes$node)], c(16, 17), 0)
  check("karate betweenness of node 1", r$nodes$betweenness[r$nodes$node == "1"], 231.07, 0.01)
  check("karate Louvain modularity about .42", v("modularity"), 0.42, 0.005)
  # Hand-computable directed graph a->b, b->a, b->c plus isolate d (listed in nodes) and a duplicate tie:
  # reciprocity = 2 of 3 ties reciprocated; density = 3 / (4*3) = .25; in-degree of b = 1, out-degree of b = 2.
  e <- data.frame(from = c("a", "b", "b", "b"), to = c("b", "a", "c", "c"))
  r <- edu_network(e, directed = TRUE, nodes = data.frame(id = c("a", "b", "c", "d"), grade = c(7, 7, 8, 8)))
  check("directed reciprocity, density, nodes", c(v("reciprocity"), v("density"), v("nodes")), c(2 / 3, 0.25, 4), 1e-12)
  check("in/out degree of b", c(r$nodes$in_degree[r$nodes$node == "b"], r$nodes$out_degree[r$nodes$node == "b"]), c(1, 2), 0)
  # Same graph with tie weights 5 (duplicate b->c summed to 10): reachable directed pairs a->b 1, a->c 2,
  # b->a 1, b->c 1, so mean distance = 5/4 in steps whatever the weights; out-strength of b = 5 + 10 = 15.
  e$w <- 5
  r <- edu_network(e, directed = TRUE, weight = "w", nodes = c("a", "b", "c", "d"))
  check("weighted: mean distance in steps, out-strength of b", c(v("mean distance"), r$nodes$out_strength[r$nodes$node == "b"]), c(1.25, 15), 1e-12)
  f <- edu_network_plot(kc, file.path(tempdir(), "network_test.png"), directed = FALSE)
  check("network plot file written", as.numeric(file.exists(f) && file.size(f) > 1000), 1, 0)
}) else message("skipped: social network analysis (package igraph missing)")

safely("lag sequential analysis", {
  # Two actors: actor 1 codes A B A B B A, actor 2 codes B A (rows shuffled; order column restores time).
  # Lag-1 transitions within actors: AB = 2, BA = 3, BB = 1, AA = 0 (N = 6; the boundary A -> B between
  # actors must not be counted). Margins: given A = 2, B = 4; target A = 3, B = 3.
  # Expected (Bakeman & Quera, 2011): e_AB = 2*3/6 = 1, e_BB = 4*3/6 = 2.
  # Adjusted residual z = (f - e) / sqrt(e (1 - f_i+/N)(1 - f_+j/N)):
  #   z_AB = (2 - 1) / sqrt(1 * (2/3) * (1/2)) = sqrt(3);  z_BB = (1 - 2) / sqrt(2 * (1/3) * (1/2)) = -sqrt(3).
  # Yule's Q for A -> B: a = 2, b = 0, c = 1, d = 3, Q = (6 - 0) / (6 + 0) = 1. Pearson chi-square = 1 + 1 + .5 + .5 = 3.
  d <- data.frame(who = c(rep("s1", 6), rep("s2", 2)), t = c(1:6, 1:2), act = c("A", "B", "A", "B", "B", "A", "B", "A"))
  d <- d[c(8, 3, 1, 6, 2, 7, 5, 4), ]
  r <- edu_lsa(d, "who", "t", "act")
  cell <- function(g, t) r$transitions[r$transitions$given == g & r$transitions$target == t, ]
  check("observed AB, BA (no cross-actor transition)", c(cell("A", "B")$observed, cell("B", "A")$observed), c(2, 3), 0)
  check("expected AB, BB", c(cell("A", "B")$expected, cell("B", "B")$expected), c(1, 2), 1e-12)
  check("adjusted residuals AB, BB = +-sqrt(3)", c(cell("A", "B")$z, cell("B", "B")$z), c(sqrt(3), -sqrt(3)), 1e-12)
  check("Yule's Q AB = 1; P(B|A) = 1; chi-square = 3", c(cell("A", "B")$yule_q, cell("A", "B")$cond_prob, r$summary$chisq), c(1, 1, 3), 1e-12)
  # Identity: under independence the adjusted residuals equal the standardized Pearson residuals of the
  # Poisson log-linear model given + target (Haberman, 1973).
  set.seed(7); sim <- data.frame(id = rep(1:20, each = 30), t = rep(1:30, 20), code = sample(c("Q", "R", "E", "F"), 600, TRUE, c(.4, .3, .2, .1)))
  r <- edu_lsa(sim, "id", "t", "code")
  g <- stats::glm(observed ~ given + target, family = stats::poisson, data = r$transitions, control = stats::glm.control(epsilon = 1e-14, maxit = 100))
  check("adjusted residuals equal Haberman residuals", r$transitions$z, unname(stats::rstandard(g, type = "pearson")), 1e-8)
  # Quasi-independence (repeats impossible): fitted expected counts reproduce the observed margins.
  nr <- do.call(rbind, lapply(1:20, function(i) { v <- character(30); v[1] <- "Q"
    for (j in 2:30) v[j] <- sample(setdiff(c("Q", "R", "E", "F"), v[j - 1]), 1); data.frame(id = i, t = 1:30, code = v) }))
  r <- edu_lsa(nr, "id", "t", "code", self_transitions = FALSE)
  tt <- r$transitions; tt$expected[is.na(tt$expected)] <- 0
  check("quasi-independence expected margins = observed margins",
        c(tapply(tt$expected, tt$given, sum) - tapply(tt$observed, tt$given, sum), tapply(tt$expected, tt$target, sum) - tapply(tt$observed, tt$target, sum)),
        rep(0, 8), 1e-6)
})

if (pkgs_ok(c("TraMineR", "cluster"))) safely("sequence analysis", {
  # mvad (TraMineR documentation example, seqdef(mvad, 17:86)): 712 school leavers, 70 monthly states, 6 states.
  # Transition rates and the first-month state distribution are recomputed by direct counting.
  data(mvad, package = "TraMineR", envir = environment())
  W <- as.matrix(data.frame(lapply(mvad[, 17:86], as.character)))
  long <- data.frame(id = rep(mvad$id, 70), month = rep(1:70, each = 712), state = as.vector(W))
  r <- edu_sequence(long, "id", "month", "state", k = 2:4)
  check("mvad 712 sequences, 70 months, 6 states", c(nrow(r$membership), nrow(r$distribution), nrow(r$states)), c(712, 70, 6), 0)
  from <- as.vector(W[, -70]); to <- as.vector(W[, -1]); hand <- prop.table(table(from, to), 1)
  got <- as.matrix(r$transition_rates[, -1]); rownames(got) <- r$transition_rates$from
  check("transition rates equal direct counts", got[rownames(hand), colnames(hand)], unclass(hand), 1e-10)
  first <- prop.table(table(W[, 1]))
  check("first-month state distribution equals direct counts", unlist(r$distribution[1, names(first)]), as.vector(first), 1e-10)
  # Planted typology: three trajectories (school -> HE, school -> employment, training -> joblessness),
  # with timing jitter; OM + Ward must find k = 3 and recover the planted types (ARI = 1).
  set.seed(3); typ <- rep(1:3, each = 20)
  pl <- do.call(rbind, lapply(seq_along(typ), function(i) {
    cut <- sample(4:8, 1)
    s <- switch(typ[i], c(rep("school", cut), rep("HE", 12 - cut)), c(rep("school", cut), rep("employment", 12 - cut)),
                c(rep("training", cut), rep("joblessness", 12 - cut)))
    data.frame(id = i, month = 1:12, state = s)
  }))
  r <- edu_sequence(pl, "id", "month", "state", k = 2:5)
  check("planted sequence types: k = 3, ARI = 1", c(r$types$type[nrow(r$types)], edu_adjusted_rand(r$membership$type, typ)), c(3, 1), 1e-12)
}) else message("skipped: sequence analysis (TraMineR or cluster missing)")

if (pkgs_ok("stm")) safely("topic model", {
  # Planted topics: two disjoint (segmented Chinese) vocabularies; documents draw only from one of them.
  # A two-topic STM must put each vocabulary in its own topic and assign every document to its source (ARI = 1).
  va <- c("函数", "方程", "几何", "证明", "代数", "概率", "统计", "图形", "公式", "计算")
  vb <- c("旋律", "节奏", "和声", "音色", "乐谱", "演奏", "合唱", "音阶", "调式", "乐器")
  set.seed(11); grp <- rep(1:2, each = 20)
  txt <- vapply(grp, function(g) paste(sample(if (g == 1) va else vb, 30, TRUE), collapse = " "), "")
  r <- edu_topics(data.frame(id = paste0("d", 1:40), text = txt), "text", k = 2:3, id_col = "id", k_final = 2, n_words = 5)
  w <- strsplit(r$topics$prob_words, ", ")
  src <- vapply(w, function(x) if (all(x %in% va)) 1 else if (all(x %in% vb)) 2 else 0, 0)
  check("each topic's top words come from one planted vocabulary", sort(src), c(1, 2), 0)
  check("documents recovered (ARI = 1)", edu_adjusted_rand(max.col(as.matrix(r$theta[, -1])), grp), 1, 1e-12)
  check("searchK rows and topic proportions sum to 1", c(nrow(r$search), sum(r$topics$mean_proportion)), c(2, 1), 1e-8)
  # gadarian (stm documentation example: 341 open-ended answers, treatment and pid_rep covariates): output shape.
  gd <- stm::gadarian
  r <- edu_topics(gd, "open.ended.response", k = 3, segmented = FALSE, covariates = c("treatment", "pid_rep"), n_docs = 2)
  check("gadarian shape: 341 documents, 3 topics, 6 representative docs, 3 x 3 effect rows",
        c(r$corpus$documents_input, nrow(r$topics), nrow(r$representative_docs), nrow(r$effects)), c(341, 3, 6, 9), 0)
  check("gadarian theta rows sum to 1", range(rowSums(as.matrix(r$theta[, -1]))), c(1, 1), 1e-3)
}) else message("skipped: topic model (package stm missing)")
