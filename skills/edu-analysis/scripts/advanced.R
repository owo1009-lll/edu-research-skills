# Mature estimators, explicit design/estimation choices, recorded diagnostics.
.libPaths(c(Sys.getenv('R_LIBS_USER'),file.path(R.home(),'library')),include.site=FALSE)
args <- commandArgs(trailingOnly=TRUE)
if(length(args)!=2)stop('Use advanced.R PLAN_JSON NEW_OUTPUT_DIRECTORY')
cfg <- jsonlite::fromJSON(args[1],simplifyVector=FALSE)
out <- args[2]
if(dir.exists(out))stop('Refusing overwrite')
dir.create(out,recursive=TRUE)
options(digits=17)
options(error=function(){traceback(12);quit(status=1)})
writeLines(capture.output(sessionInfo()),file.path(out,'sessionInfo.txt'))
writeLines(.libPaths(),file.path(out,'library_paths.txt'))
need <- function(x,k,where)if(!all(k%in%names(x)))stop(paste('Missing',where,paste(setdiff(k,names(x)),collapse=',')))
csv <- function(x,name)write.csv(x,file.path(out,paste0(name,'.csv')),row.names=FALSE,na='')
js <- function(x,name)jsonlite::write_json(x,file.path(out,paste0(name,'.json')),auto_unbox=TRUE,pretty=TRUE,na='null',digits=16)
txt <- function(x,name)writeLines(x,file.path(out,paste0(name,'.txt')))
need(cfg,c('data','question','selection_reason','design','variables','analysis','na_strings','seed','confidence'),'plan')
if(!nzchar(cfg$question)||!nzchar(cfg$selection_reason))stop('Real question and method-selection reason required')
if(cfg$confidence<=0||cfg$confidence>=1)stop('Invalid confidence')
need(cfg$design,c('unit','id','row_structure','cluster_columns','independence_basis'),'design')
set.seed(cfg$seed)
d <- read.csv(cfg$data,na.strings=unlist(cfg$na_strings),check.names=FALSE,colClasses='character',fileEncoding='UTF-8')
if(anyDuplicated(names(d)))stop('Duplicate columns')
if(!cfg$design$id%in%names(d)||anyNA(d[[cfg$design$id]])||any(!nzchar(d[[cfg$design$id]])))stop('Valid unit ID required')
if(cfg$design$row_structure!='long'&&anyDuplicated(d[[cfg$design$id]]))stop('Duplicate units in wide/independent design')
checks <- list()
for(v in names(cfg$variables)) {
  if(!v%in%names(d))stop(paste('Absent declared variable',v))
  s <- cfg$variables[[v]];need(s,c('type','meaning','source'),'variable')
  if(!nzchar(s$meaning)||!nzchar(s$source))stop('Variable meaning/source must come from materials')
  if(s$type%in%c('continuous','ordinal')) {
    z <- suppressWarnings(as.numeric(d[[v]]))
    if(any(!is.na(d[[v]])&is.na(z))||any(!is.finite(z)&!is.na(z)))stop(paste('Unexplained numeric coding',v))
    if(!is.null(s$min)&&any(z<s$min,na.rm=TRUE))stop(paste('Below range',v))
    if(!is.null(s$max)&&any(z>s$max,na.rm=TRUE))stop(paste('Above range',v))
    if(s$type=='ordinal') {
      need(s,'levels','ordinal variable');levels <- unlist(s$levels)
      if(any(!is.na(z)&!z%in%levels))stop(paste('Undeclared ordinal category',v))
      if(any(!levels%in%z))stop(paste('Declared but absent ordinal category',v,'review coding and identification'))
    }
    d[[v]] <- z
  } else if(s$type=='categorical') {
    need(s,c('levels','reference'),'categorical variable')
    if(any(!is.na(d[[v]])&!d[[v]]%in%unlist(s$levels)))stop(paste('Unknown group value',v))
    d[[v]] <- factor(d[[v]],levels=unlist(s$levels))
    if(!s$reference%in%levels(d[[v]]))stop('Unspecified reference')
    d[[v]] <- relevel(d[[v]],s$reference)
  } else stop('Use explicit continuous/ordinal/categorical variable types')
  checks[[v]] <- data.frame(variable=v,type=s$type,n=nrow(d),missing=sum(is.na(d[[v]])),distinct=length(unique(na.omit(d[[v]]))))
}
csv(do.call(rbind,checks),'variable_checks')
a <- cfg$analysis;need(a,c('method','missing','missing_assumption'),'analysis')
if(!nzchar(a$missing_assumption))stop('Missing-data strategy/assumption required')
declared_clusters <- unlist(cfg$design$cluster_columns)
if(length(declared_clusters)&&!all(declared_clusters%in%names(d)))stop('Cluster column absent')
if(a$method%in%c('efa','cfa','sem','invariance','clpm','ri_clpm','growth') && length(declared_clusters)) {
  if(any(vapply(declared_clusters,function(v)length(unique(na.omit(d[[v]])))>1,logical(1))))stop('Nested sampling needs an appropriate clustered estimator; not independent lavaan/psych')
}
if(a$method%in%c('efa','cfa','sem','invariance','clpm','ri_clpm','growth')&&cfg$design$row_structure=='long')stop('Measurement/panel SEM needs one row per unit; prepare documented wide data')
record <- list(method=a$method,n_input=nrow(d),question=cfg$question,selection_reason=cfg$selection_reason,
               missing=a$missing,missing_assumption=a$missing_assumption,confidence=cfg$confidence,seed=cfg$seed)
warn <- character()
capture_warn <- function(expr,stage='analysis')withCallingHandlers(expr,warning=function(w){warn<<-c(warn,paste0(stage,': ',conditionMessage(w)));invokeRestart('muffleWarning')})
complete_sample <- function(vars) {
  if(!all(vars%in%names(d)))stop('Missing analysis columns')
  ok <- complete.cases(d[vars]);record$n_used <<- sum(ok);record$n_excluded <<-sum(!ok)
  csv(data.frame(id=d[[cfg$design$id]][ok]),'sample_ids_private')
  d[ok,,drop=FALSE]
}
sem_diagnostics <- function(fit) {
  converged <- isTRUE(lavaan::lavInspect(fit,'converged'))
  estimates <- lavaan::parameterEstimates(fit,standardized=TRUE,ci=TRUE,level=cfg$confidence)
  negative <- estimates[estimates$op=='~~' & estimates$lhs==estimates$rhs & estimates$est < -1e-8,]
  gradients <- tryCatch(lavaan::lavInspect(fit,'gradient'),error=function(e)NA_real_)
  covariance <- tryCatch(lavaan::lavInspect(fit,'cov.lv'),error=function(e)NULL)
  mats <- if(is.matrix(covariance))list(covariance) else covariance
  mats <- Filter(function(z)is.matrix(z)&&nrow(z)>0,mats)
  min_eigen <- if(length(mats))min(vapply(mats,function(z)min(eigen(z,symmetric=TRUE,only.values=TRUE)$values),numeric(1))) else NA_real_
  variance <- tryCatch(lavaan::lavInspect(fit,'vcov'),error=function(e)NULL)
  se_problem <- any(!is.finite(estimates$se[estimates$op%in%c('=~','~',':=')]))
  condition <- if(!is.null(variance)&&all(is.finite(variance)))kappa(variance,exact=TRUE) else NA_real_
  post_check <- isTRUE(capture_warn(lavaan::lavInspect(fit,'post.check')))
  pt <- lavaan::parTable(fit)
  constrained <- any(pt$op=='==')
  valid <- converged && post_check && nrow(negative)==0 && !se_problem && (is.na(min_eigen)||min_eigen>=-1e-7)
  list(converged=converged,post_check=post_check,
       negative_variances=negative,nonfinite_parameter_se=se_problem,latent_covariance_min_eigen=min_eigen,
       maximum_gradient=if(all(is.na(gradients)))NA_real_ else max(abs(gradients),na.rm=TRUE),
       parameter_covariance_condition=condition,equality_constraints=constrained,
       stability_note=if(constrained)'Raw gradient is not the constrained projected gradient; equality constraints make the full parameter covariance singular. Review constrained optimization and SEs rather than misclassifying these raw diagnostics.' else 'Review gradient and covariance conditioning together with warnings and substantive identification.',
       npar=lavaan::lavInspect(fit,'npar'),n_used=lavaan::lavInspect(fit,'nobs'),
       admissible_for_interpretation=valid,scope='Diagnostic information, not a fit-threshold certification or proof of causal identification')
}
save_sem <- function(fit,name) {
  # Keep the actual model object private; structured public exports are separately reviewed.
  saveRDS(fit,file.path(out,paste0(name,'.rds')))
  txt(capture.output(summary(fit,fit.measures=TRUE,standardized=TRUE,rsquare=TRUE)),paste0(name,'_summary'))
  pe <- lavaan::parameterEstimates(fit,standardized=TRUE,ci=TRUE,level=cfg$confidence,
                                 boot.ci.type=if(is.null(a$bootstrap_ci))'perc' else a$bootstrap_ci)
  csv(pe,paste0(name,'_parameters'))
  # The first table's CI belongs to est, not std.all. Standardized CIs are a separate delta-method export.
  ss <- tryCatch(lavaan::standardizedSolution(fit,level=cfg$confidence),error=function(e)data.frame(error=conditionMessage(e)))
  csv(ss,paste0(name,'_standardized'))
  measures <- capture_warn(lavaan::fitMeasures(fit))
  csv(data.frame(measure=names(measures),value=unname(measures)),paste0(name,'_fit'))
  diag <- sem_diagnostics(fit);js(diag,paste0(name,'_diagnostics'))
  boot <- tryCatch(lavaan::lavInspect(fit,'boot'),error=function(e)NULL)
  if(!is.null(boot))js(list(requested=nrow(boot),failed_indices=attr(boot,'error.idx'),
      nonadmissible_indices=attr(boot,'nonadmissible'),finite_replicates=sum(apply(boot,1,function(z)all(is.finite(z)))),
      ci='Percentile intervals for unstandardized estimates; standardizedSolution remains delta-method'),paste0(name,'_bootstrap_diagnostics'))
  diag
}
lavaan_args <- function(model) {
  need(a,c('estimator','parameterization','identification','interval_method','model_rationale'),'SEM specification')
  if(!a$estimator%in%c('ML','MLR','WLSMV'))stop('Estimator not adapted')
  if(!a$parameterization%in%c('delta','theta')||!a$identification%in%c('marker','std.lv'))stop('Explicit identification/parameterization required')
  if(!a$missing%in%c('listwise','fiml','pairwise'))stop('Missing method not adapted')
  ordered <- names(cfg$variables)[vapply(cfg$variables,function(s)s$type=='ordinal',logical(1))]
  ngroups <- if(is.null(a$group))1L else length(unique(na.omit(d[[a$group]])))
  used <- unique(unlist(lavaan::lavNames(lavaan::lavaanify(model,auto=TRUE,ngroups=ngroups),'ov')))
  ordered <- intersect(ordered,used)
  if(length(ordered)&&a$estimator!='WLSMV')stop('Ordered indicators require the adapted WLSMV model; explicitly reconsider measurement types instead of overriding')
  if(a$estimator=='WLSMV'&&a$missing=='fiml')stop('WLSMV cannot use FIML in lavaan')
  if(a$estimator!='WLSMV'&&a$missing=='pairwise')stop('Pairwise adapted only for WLSMV')
  if(!all(used%in%names(d))||!all(used%in%names(cfg$variables)))stop('Model uses undeclared/absent observed variables')
  observed <- d[used];record$n_complete <<- sum(complete.cases(observed));record$missing_by_model_variable <<-as.list(colSums(is.na(observed)))
  csv(as.data.frame(table(apply(is.na(observed),1,paste,collapse=''))),'missing_patterns')
  options <- list(model=model,data=d,estimator=a$estimator,missing=a$missing,
                  meanstructure=TRUE,std.lv=a$identification=='std.lv',parameterization=a$parameterization)
  if(length(ordered))options$ordered <- ordered
  if(a$interval_method=='bootstrap_percentile') {
    if(a$estimator!='ML')stop('Percentile bootstrap currently adapted for ML only; do not silently change estimator')
    need(a,'bootstrap_replicates','bootstrap');if(a$bootstrap_replicates<200)stop('At least 200 bootstrap replicates')
    options$se <- 'bootstrap';options$bootstrap <- a$bootstrap_replicates
  } else if(a$interval_method!='delta')stop('Interval method not adapted')
  options
}
result_status <- 'completed'
if(a$method%in%c('clpm','ri_clpm','growth')) {
  need(a,c('waves','times','comparability_basis','constraint_reason'),'longitudinal design')
  times <- unlist(a$times);waves <- unlist(a$waves)
  if(length(times)<3||any(diff(times)<=0))stop('At least three explicitly ordered occasions with increasing elapsed times required')
  if(!nzchar(a$comparability_basis)||!nzchar(a$constraint_reason))stop('Measurement comparability and cross-wave constraint decisions need evidence')
  record$times <- times;record$comparability_basis <- a$comparability_basis
  record$constraint_reason <- a$constraint_reason
  if(a$method=='growth') {
    if(length(waves)!=length(times)||any(vapply(cfg$variables[waves],function(v)is.null(v)||v$type!='continuous',logical(1))))stop('Continuous growth outcome at each occasion required')
    need(a,'origin_reason','growth time origin')
    a$model <- paste(paste('intercept =~',paste(paste0('1*',waves),collapse=' + ')),
                     paste('slope =~',paste(paste0(times,'*',waves),collapse=' + ')),sep='\n')
    record$estimand <- paste('Latent intercept at elapsed time zero and linear change per declared time unit;',a$origin_reason)
  } else {
    need(a,c('x','y','lag_constraints','ri_measurement_assumption'),'panel variables')
    x <- unlist(a$x);y <- unlist(a$y);n <- length(times)
    if(length(x)!=n||length(y)!=n||anyDuplicated(c(x,y))||!all(c(x,y)%in%names(cfg$variables)))stop('Two distinct documented series at every occasion required')
    if(any(vapply(cfg$variables[c(x,y)],function(v)v$type!='continuous',logical(1))))stop('Panel adapter currently continuous observed composites only')
    if(!a$lag_constraints%in%c('free','equal'))stop('Explicit free/equal lag decision required')
    if(a$lag_constraints=='equal'&&length(unique(diff(times)))!=1)stop('Unequal elapsed intervals do not justify equal discrete lag coefficients')
    prefix <- if(a$method=='ri_clpm')'w' else ''
    xx <- if(nzchar(prefix))paste0('wx',seq_len(n)) else x
    yy <- if(nzchar(prefix))paste0('wy',seq_len(n)) else y
    model <- character()
    if(a$method=='ri_clpm') {
      model <- c(paste('RIx =~',paste(paste0('1*',x),collapse=' + ')),paste('RIy =~',paste(paste0('1*',y),collapse=' + ')),
                 'RIx ~~ RIx','RIy ~~ RIy','RIx ~~ RIy', 'RIx ~ 0*1','RIy ~ 0*1')
      for(i in seq_len(n))model <- c(model,paste0(xx[i],' =~ 1*',x[i]),paste0(yy[i],' =~ 1*',y[i]),
        paste0(x[i],' ~~ 0*',x[i]),paste0(y[i],' ~~ 0*',y[i]),paste0(x[i],' ~ 1'),paste0(y[i],' ~ 1'),
        paste0(xx[i],' ~ 0*1'),paste0(yy[i],' ~ 0*1'),
        paste0('RIx ~~ 0*',xx[i],' + 0*',yy[i]),paste0('RIy ~~ 0*',xx[i],' + 0*',yy[i]))
      record$estimand <- 'Stable random intercept covariance and lagged within-person deviations, not causal intervention effects'
      record$measurement_assumption <- a$ri_measurement_assumption
    } else record$estimand <- 'Cross-lagged observed-score associations confounding stable between-person and within-person variation'
    for(i in seq_len(n))model <- c(model,paste0(xx[i],' ~~ ',xx[i]),paste0(yy[i],' ~~ ',yy[i]),paste0(xx[i],' ~~ ',yy[i]))
    for(i in 2:n) {
      lab <- if(a$lag_constraints=='equal')'' else as.character(i)
      model <- c(model,paste0(xx[i],' ~ ax',lab,'*',xx[i-1],' + cyx',lab,'*',yy[i-1]),
                       paste0(yy[i],' ~ ay',lab,'*',yy[i-1],' + cxy',lab,'*',xx[i-1]))
    }
    a$model <- paste(model,collapse='\n')
  }
}
if(a$method=='efa') {
  need(a,c('items','factors','factor_number_reason','extraction','rotation','correlation','parallel_replicates'),'EFA')
  items <- unlist(a$items);if(length(items)<3||!all(items%in%names(cfg$variables)))stop('Declare at least three EFA indicators')
  if(!a$missing%in%c('listwise','pairwise'))stop('EFA only explicit listwise/pairwise')
  z <- if(a$missing=='listwise')complete_sample(items) else d
  z <- z[items];if(any(vapply(z,function(x)length(unique(na.omit(x)))<2,logical(1))))stop('Constant EFA item')
  if(!a$correlation%in%c('pearson','polychoric'))stop('Explicit EFA correlation required')
  if(a$correlation=='pearson'&&any(vapply(cfg$variables[items],function(v)v$type=='ordinal',logical(1))))stop('Ordinal declarations require polychoric EFA in this adapter')
  if(!a$extraction%in%c('minres','ml','pa')||!a$rotation%in%c('oblimin','promax','varimax','none'))stop('EFA extraction/rotation not adapted')
  if(a$factors<1||a$factors>=length(items)||a$factors%%1!=0)stop('Invalid factor number')
  if(!nzchar(a$factor_number_reason)||a$parallel_replicates<100)stop('Factor-selection reason and adequate PA replicates required')
  correlation <- if(a$correlation=='polychoric')capture_warn(psych::polychoric(z,correct=0,smooth=FALSE,global=FALSE)$rho) else cor(z,use=if(a$missing=='pairwise')'pairwise.complete.obs' else 'complete.obs')
  if(min(eigen(correlation,symmetric=TRUE)$values)<=0)stop('Non-positive definite correlation: no automatic smoothing')
  pairs <- crossprod(!is.na(as.matrix(z)));csv(data.frame(item=rownames(pairs),pairs,check.names=FALSE),'pairwise_n')
  if(a$correlation=='polychoric') {
    need(a,'parallel_design','ordinal parallel analysis')
    if(a$parallel_design!='permutation_without_replacement'||a$missing!='listwise')stop('Ordinal permutation PA currently requires declared listwise sample and no-replacement independent column permutations')
    observed <- capture_warn(psych::fa(correlation,nfactors=1,fm=a$extraction,rotate='none',SMC=FALSE),'parallel observed reference')$values
    null <- replicate(a$parallel_replicates,{
      randomized <- as.data.frame(lapply(z,function(column)sample(column,replace=FALSE)))
      rr <- capture_warn(psych::polychoric(randomized,correct=0,smooth=FALSE,global=FALSE),'parallel null reference')$rho
      if(any(!is.finite(rr))||min(eigen(rr,symmetric=TRUE)$values)<=0)stop('Ordinal null correlation invalid; preserve failed PA rather than smoothing or silently changing categories')
      capture_warn(psych::fa(rr,nfactors=1,fm=a$extraction,rotate='none',SMC=FALSE),'parallel null reference')$values
    })
    reference <- apply(null,1,quantile,probs=.95)
    pa <- list(fa.values=observed,fa.sim=reference,nfact=sum(observed>reference))
    csv(data.frame(replicate=seq_len(ncol(null)),t(null)),'efa_parallel_null')
    record$parallel_design <- 'Independent column permutations without replacement, preserving observed ordinal marginals; psych polychoric(global=FALSE,correct=0,smooth=FALSE), psych fa one-factor reduced eigenvalues and 95th null quantile'
  } else {
    pa <- capture_warn(psych::fa.parallel(z,fa='fa',fm=a$extraction,n.iter=a$parallel_replicates,
                         cor='cor',use=if(a$missing=='pairwise')'pairwise' else 'complete',plot=FALSE,quant=.95),'parallel reference generation')
    record$parallel_design <- 'psych fa.parallel simulated Gaussian and randomized empirical reference, 95th percentile'
  }
  fit <- capture_warn(psych::fa(correlation,nfactors=a$factors,n.obs=nrow(z),fm=a$extraction,rotate=a$rotation),'selected EFA model')
  saveRDS(fit,file.path(out,'efa.rds'));txt(capture.output(print(fit)),'efa_summary')
  csv(data.frame(item=rownames(fit$loadings),unclass(fit$loadings),communality=fit$communality,uniqueness=fit$uniquenesses,check.names=FALSE),'efa_loadings')
  if(!is.null(fit$Phi))csv(data.frame(factor=rownames(fit$Phi),fit$Phi,check.names=FALSE),'efa_factor_correlations')
  csv(data.frame(index=seq_along(pa$fa.values),observed=pa$fa.values,reference=pa$fa.sim),'efa_parallel')
  js(list(parallel_suggested_factors=pa$nfact,chosen_factors=a$factors,choice_reason=a$factor_number_reason,
          correlation=a$correlation,extraction=a$extraction,rotation=a$rotation,parallel_replicates=a$parallel_replicates,
          KMO=psych::KMO(correlation)$MSA,bartlett=psych::cortest.bartlett(correlation,n=nrow(z)),
          improper_communalities=any(fit$communality<0|fit$communality>1),convergence=if(is.null(fit$converged))NA else fit$converged,
          convergence_note='psych fa does not expose a universal optimizer convergence flag for every extraction. Preserve warnings and finite loading/uniqueness checks; a missing flag is not a pass.',
          limitation='Parallel analysis is evidence for dimensionality, not automatic theory/validity verification; pairwise sample sizes may differ'),'efa_diagnostics')
  if(any(fit$communality<0|fit$communality>1))result_status <- 'inadmissible_fit'
} else if(a$method%in%c('cfa','sem','clpm','ri_clpm','growth')) {
  need(a,'model','measurement/path model');options <- lavaan_args(a$model)
  txt(a$model,'model')
  options$fixed.x <- FALSE
  estimator <- if(a$method=='cfa')lavaan::cfa else if(a$method=='growth')lavaan::growth else if(a$method=='ri_clpm')lavaan::lavaan else lavaan::sem
  if(a$method=='growth') {options$std.lv <- FALSE;options$int.ov.free <- FALSE;options$int.lv.free <- TRUE}
  if(a$method=='ri_clpm') {
    options$std.lv <- FALSE;options$int.ov.free <- FALSE;options$int.lv.free <- FALSE
    options$auto.fix.first <- FALSE;options$auto.fix.single <- FALSE;options$auto.var <- FALSE
    options$auto.cov.lv.x <- FALSE;options$auto.cov.y <- FALSE
  }
  if(!is.null(a$group)) {
    need(a,c('group_reason','measurement_comparability'),'multigroup SEM')
    if(!nzchar(a$group_reason)||!nzchar(a$measurement_comparability))stop('Substantive groups and measurement comparability review required')
    options$group <- a$group
    if(length(a$group_equal))options$group.equal <- unlist(a$group_equal)
    if(length(a$group_partial))options$group.partial <- unlist(a$group_partial)
    record$group_reason <- a$group_reason;record$measurement_comparability <- a$measurement_comparability
  }
  fit <- capture_warn(do.call(estimator,options))
  diag <- save_sem(fit,a$method)
  record$n_used <- diag$n_used
  if(!diag$admissible_for_interpretation)result_status <- 'inadmissible_fit'
  if(a$method=='growth'&&diag$admissible_for_interpretation) {
    pt <- lavaan::parTable(fit);ix <- pt$free[pt$lhs=='intercept'&pt$op=='~1'];sx <- pt$free[pt$lhs=='slope'&pt$op=='~1']
    coefficients <- pt$est[match(c(ix,sx),pt$free)];variance <- lavaan::lavInspect(fit,'vcov')[c(ix,sx),c(ix,sx),drop=FALSE]
    X <- cbind(1,times);average <- as.vector(X%*%coefficients)
    se <- sqrt(diag(X%*%variance%*%t(X)));critical <- qnorm((1+cfg$confidence)/2)
    csv(data.frame(time=times,mean=average,se=se,ci_lower=average-critical*se,ci_upper=average+critical*se),'growth_average_trajectory')
    record$trajectory_interval <- 'Model-implied population mean with pointwise estimator-specific delta/Wald confidence intervals; not observed wave means, individual trajectories or individual prediction intervals'
  }
  if(!is.null(a$hypotheses)&&diag$admissible_for_interpretation) {
    for(h in a$hypotheses) {
      need(h,c('name','constraints','reason'),'planned Wald hypothesis')
      if(!nzchar(h$reason)||!grepl('^[A-Za-z0-9_]+$',h$name))stop('Documented hypothesis and safe output name required')
      test <- capture_warn(lavaan::lavTestWald(fit,constraints=h$constraints))
      js(list(hypothesis=h,test=test),paste0('wald_',h$name))
    }
  }
  if(isTRUE(a$reliability)) {
    if(a$method!='cfa')stop('Model-based composite reliability requires an actual CFA; do not use SEM regressions as CFA')
    if(!diag$admissible_for_interpretation)stop('No reliability interpretation from inadmissible measurement model')
    need(a,'reliability_denominator','composite reliability')
    if(!a$reliability_denominator%in%c('observed','model_implied'))stop('Explicit reliability denominator required')
    rel <- semTools::compRelSEM(fit,tau.eq=FALSE,ord.scale=TRUE,obs.var=a$reliability_denominator=='observed',simplify=TRUE)
    if(is.atomic(rel)&&is.null(dim(rel))) {
      factors <- names(rel)
      if(is.null(factors)) {
        factors <- lavaan::lavNames(fit,'lv')
        if(length(factors)!=length(rel))stop('Composite label unavailable; do not assign by guessed order')
      }
      rel <- data.frame(composite=factors,reliability=as.numeric(rel))
    }
    else rel <- data.frame(composite=rownames(rel),as.data.frame(rel),check.names=FALSE)
    csv(rel,'composite_reliability')
    record$reliability <- 'Congeneric CFA-based composite reliability; observed ordinal scale for ordered indicators; not validity'
    record$reliability_denominator <- a$reliability_denominator
  }
} else if(a$method=='invariance') {
  need(a,c('model','steps','comparison_basis'),'invariance')
  if(!nzchar(a$comparison_basis))stop('Substantive group/occasion comparison rationale required')
  if(is.null(a$group)&&is.null(a$long_factors))stop('Actual group or repeated measurement map required')
  if(!is.null(a$group)&&(!a$group%in%names(d)||length(unique(na.omit(d[[a$group]])))<2))stop('Need actual multiple groups')
  options <- lavaan_args(a$model);ordered <- options$ordered
  long_names <- if(is.null(a$long_factors))NULL else lapply(a$long_factors,unlist)
  fits <- list();comparisons <- list()
  for(step in a$steps) {
    need(step,c('name','equal','reason'),'invariance step')
    if(!nzchar(step$reason))stop('Document each planned constraint/release')
    equal <- unlist(step$equal);if(is.null(equal))equal <- character()
    partial <- unlist(step$partial)
    generator <- list(configural.model=a$model,data=d,parameterization=a$parameterization,
                      ID.fac=a$identification,meanstructure=TRUE)
    if(!is.null(a$group))generator$group <- a$group
    if(length(long_names))generator$longFacNames <- long_names
    if(length(equal)&&!is.null(a$group))generator$group.equal <- equal
    if(length(equal)&&length(long_names))generator$long.equal <- equal
    if(length(partial)&&!is.null(a$group))generator$group.partial <- partial
    if(length(partial)&&!is.null(long_names))generator$long.partial <- partial
    if(length(ordered)){generator$ordered <- ordered;generator$ID.cat <- 'Wu.Estabrook.2016'}
    syntax <- capture_warn(do.call(semTools::measEq.syntax,generator))
    model <- as.character(syntax);txt(model,paste0('invariance_',step$name,'_model'))
    current <- options;current$model <- model;current$std.lv <- FALSE;current$group <- a$group
    fit <- capture_warn(do.call(lavaan::cfa,current));fits[[step$name]] <- fit
    diag <- save_sem(fit,paste0('invariance_',step$name))
    if(!diag$admissible_for_interpretation){result_status <- 'inadmissible_fit';break}
    if(length(fits)>1) {
      previous <- fits[[length(fits)-1]]
      # lavaan selects the estimator-appropriate scaled difference test; never subtract robust chi-square values.
      comparison <- capture_warn(lavaan::lavTestLRT(previous,fit))
      csv(data.frame(model=rownames(comparison),comparison,check.names=FALSE),paste0('invariance_',step$name,'_comparison'))
      if(!isTRUE(step$continue_after_review)&&length(fits)<length(a$steps)) {
        record$stopped_after <- step$name;record$reason <- 'Constraint comparison awaits substantive diagnostic review; no automatic progression based on fit thresholds'
        result_status <- 'awaiting_constraint_review';break
      }
    }
  }
  record$constraints <- a$steps;record$group <- a$group;record$long_factors <- a$long_factors
} else if(a$method=='lmm') {
  need(a,c('formula','estimation','df_method','centering','random_structure_reason','cluster','residual_assumption'),'mixed model')
  if(!a$estimation%in%c('REML','ML')||!a$df_method%in%c('Satterthwaite','Kenward-Roger'))stop('Explicit ML/REML and supported small-sample df method required')
  clusters <- unlist(a$cluster)
  if(!length(clusters)||!all(clusters%in%names(d)))stop('Known grouping units required')
  record$centering <- a$centering;record$random_structure_reason <- a$random_structure_reason
  for(cn in a$centering) {
    need(cn,c('variable','mode','output','reason'),'centering')
    if(!cn$variable%in%names(cfg$variables)||!nzchar(cn$reason))stop('Center only documented numerical predictors')
    if(cn$mode=='grand')d[[cn$output]] <- d[[cn$variable]]-mean(d[[cn$variable]],na.rm=TRUE)
    else if(cn$mode=='within') {
      need(cn,c('group','between_output'),'within-between centering')
      means <- ave(d[[cn$variable]],d[[cn$group]],FUN=function(x)mean(x,na.rm=TRUE))
      d[[cn$output]] <- d[[cn$variable]]-means;d[[cn$between_output]] <- means
    } else stop('Centering must be explicitly grand or within')
  }
  formula <- as.formula(a$formula);vars <- all.vars(formula)
  if(!all(vars%in%names(d)))stop('Mixed-model variable absent')
  if(a$missing!='listwise')stop('LMM adapter excludes missing model rows explicitly; dedicated workflow needed for multiple imputation')
  z <- complete_sample(vars)
  cluster_counts <- lapply(clusters,function(g)data.frame(cluster=g,n_clusters=length(unique(z[[g]])),min_rows=min(table(z[[g]])),max_rows=max(table(z[[g]]))))
  csv(do.call(rbind,cluster_counts),'cluster_counts')
  if(any(vapply(cluster_counts,function(x)x$n_clusters<2,logical(1))))stop('At least two actual clusters needed')
  fit <- capture_warn(lmerTest::lmer(formula,data=z,REML=a$estimation=='REML'))
  saveRDS(fit,file.path(out,'lmm.rds'));txt(capture.output(summary(fit,ddf=a$df_method)),'lmm_summary')
  coeff <- as.data.frame(coef(summary(fit,ddf=a$df_method)));coeff$term <- rownames(coeff)
  critical <- qt((1+cfg$confidence)/2,df=coeff$df)
  coeff$ci_lower <- coeff$Estimate-critical*coeff[['Std. Error']];coeff$ci_upper <- coeff$Estimate+critical*coeff[['Std. Error']]
  csv(coeff,'lmm_fixed');csv(as.data.frame(lme4::VarCorr(fit)),'lmm_random')
  if(length(a$planned_contrasts)) {
    contrasts <- list()
    for(h in a$planned_contrasts) {
      need(h,c('name','weights','reason'),'mixed-model planned contrast')
      if(!nzchar(h$reason)||!all(names(h$weights)%in%names(lme4::fixef(fit))))stop('Located reason and estimable named fixed-effect contrast required')
      weights <- setNames(rep(0,length(lme4::fixef(fit))),names(lme4::fixef(fit)))
      weights[names(h$weights)] <- unlist(h$weights)
      result <- lmerTest::contest1D(fit,L=weights,ddf=a$df_method,confint=TRUE,level=cfg$confidence)
      result$contrast <- h$name;result$reason <- h$reason
      contrasts[[length(contrasts)+1]] <- result
    }
    csv(do.call(rbind,contrasts),'lmm_planned_contrasts')
    record$contrast_multiplicity <- 'Prespecified term contrasts; intervals/tests unadjusted, no automated search. Save any further family adjustment separately.'
  }
  csv(as.data.frame(capture_warn(anova(fit,ddf=a$df_method,type=3))),'lmm_anova')
  diag <- list(singular=lme4::isSingular(fit),convergence_messages=fit@optinfo$conv,
     nonfinite_fixed_inference=any(!is.finite(as.matrix(coeff[c('Estimate','Std. Error','df')]))),
     gradient=fit@optinfo$derivs$gradient,hessian_eigenvalues=eigen(fit@optinfo$derivs$Hessian,symmetric=TRUE)$values,
     estimation=a$estimation,df_method=a$df_method,conditional_residual_assumption=a$residual_assumption,
     note='Singular fits and few clusters constrain inference; no automatic random-term deletion or population generalization')
  js(diag,'lmm_diagnostics')
  if(length(fit@optinfo$conv$lme4$messages))result_status <- 'requires_diagnostic_review'
  if(any(!is.finite(diag$hessian_eigenvalues))||min(diag$hessian_eigenvalues)<=0)result_status <- 'hessian_requires_review'
  if(isTRUE(diag$singular))result_status <- 'singular_fit_requires_review'
  if(isTRUE(diag$nonfinite_fixed_inference))result_status <- 'nonfinite_inference_requires_review'
  csv(data.frame(id=z[[cfg$design$id]],fitted=fitted(fit),residual=residuals(fit)),'lmm_residuals_private')
  if(!is.null(a$prediction)) {
    need(a$prediction,c('rows','meaning'),'prediction')
    grid <- as.data.frame(lapply(a$prediction$rows,unlist),stringsAsFactors=FALSE)
    for(g in names(z)[vapply(z,is.factor,logical(1))])if(g%in%names(grid))grid[[g]] <- factor(grid[[g]],levels=levels(z[[g]]))
    fixedformula <- reformulas::nobars(formula);X <- model.matrix(delete.response(terms(fixedformula)),grid)
    b <- lme4::fixef(fit);X <- X[,names(b),drop=FALSE]
    mu <- as.vector(X%*%b);se <- sqrt(diag(X%*%as.matrix(vcov(fit))%*%t(X)))
    ci <- qnorm((1+cfg$confidence)/2)*se
    csv(data.frame(grid,predicted_mean=mu,se=se,ci_lower=mu-ci,ci_upper=mu+ci),'lmm_predictions')
    record$prediction_interval <- 'Pointwise asymptotic Wald confidence interval of the population fixed-effect mean, not individual prediction interval'
    record$prediction_meaning <- a$prediction$meaning
  }
} else if(a$method=='rm_anova') {
  need(a,c('outcome','within','between','factor_levels','cell_handling','contrasts','correction','comparison'),'repeated ANOVA')
  if(cfg$design$row_structure!='long'||!length(a$within))stop('Repeated ANOVA needs explicitly long within-person design')
  if(!a$correction%in%c('GG','HF','none')||a$cell_handling!='mean')stop('Explicit cell mean handling and sphericity correction required')
  within <- unlist(a$within);between <- unlist(a$between);factors <- c(within,between)
  for(v in factors) {if(!v%in%names(d)||is.null(a$factor_levels[[v]]))stop('Declared ordered factor levels required');d[[v]] <- factor(d[[v]],levels=unlist(a$factor_levels[[v]]))}
  if(a$missing!='listwise')stop('ANOVA complete cells only; use LMM or dedicated missing workflow otherwise')
  if(!all(a$contrasts==c('contr.sum','contr.poly')))stop('Type-III ANOVA uses explicitly declared sum/poly contrasts')
  options(contrasts=unlist(a$contrasts))
  for(g in between)if(any(tapply(as.character(d[[g]]),d[[cfg$design$id]],function(x)length(unique(x)))!=1))stop('Between factor varies within person')
  keys <- c(cfg$design$id,factors)
  selected <- complete.cases(d[c(keys,a$outcome)])
  z <- aggregate(d[[a$outcome]][selected],d[selected,keys,drop=FALSE],mean);names(z)[ncol(z)] <- a$outcome
  cells <- prod(vapply(a$factor_levels[within],length,integer(1)))
  ncell <- table(z[[cfg$design$id]]);keep <- names(ncell)[ncell==cells]
  if(anyDuplicated(z[c(cfg$design$id,within)]))stop('Duplicate repeated cells after declared aggregation')
  z <- z[z[[cfg$design$id]]%in%keep,,drop=FALSE]
  if(length(keep)<3)stop('Insufficient complete repeated designs')
  record$n_persons <- length(keep);record$n_excluded_persons <- length(unique(d[[cfg$design$id]]))-length(keep)
  record$cell_handling <- 'Explicit equal-weight mean per person/within cell; estimand is participant cell mean, not raw trial-weighted mean'
  csv(z,'anova_cells_private')
  fit <- capture_warn(afex::aov_ez(id=cfg$design$id,dv=a$outcome,data=z,within=within,
     between=if(length(between))between else NULL,type=3,return='afex_aov',anova_table=list(correction=a$correction,es='ges')))
  saveRDS(fit,file.path(out,'rm_anova.rds'));txt(capture.output(summary(fit)),'rm_anova_summary')
  table <- as.data.frame(afex::nice(fit,correction=a$correction,es='ges'));csv(table,'rm_anova_display')
  num <- as.data.frame(fit$anova_table);num$effect <- rownames(num);csv(num,'rm_anova_numeric')
  js(list(correction=a$correction,contrasts=unlist(a$contrasts),n_persons=length(keep),
     warning='Sphericity applies to within effects with more than two levels; exact tests/corrections are saved in summary. Complete-cell exclusion has assumptions.'),'rm_anova_diagnostics')
  if(!is.null(a$comparison)) {
    need(a$comparison,c('formula','adjust','reason'),'planned comparisons')
    if(!nzchar(a$comparison$reason)||!a$comparison$adjust%in%c('holm','tukey','bonferroni','none'))stop('Planned contrast reason and multiplicity rule required')
    emm <- capture_warn(emmeans::emmeans(fit,as.formula(a$comparison$formula)))
    csv(as.data.frame(summary(emm,infer=c(TRUE,FALSE),level=cfg$confidence)),'rm_anova_marginal_means')
    csv(as.data.frame(summary(pairs(emm,adjust=a$comparison$adjust),infer=c(TRUE,TRUE),level=cfg$confidence)),'rm_anova_comparisons')
  }
} else stop(paste('Method adapter not yet implemented:',a$method))
record$status <- result_status
record$warnings <- unique(warn)
record$packages <- as.list(vapply(c('jsonlite','reformulas','psych','lavaan','semTools','lme4','lmerTest','afex','emmeans'),function(p)as.character(packageVersion(p)),character(1)))
js(record,'analysis_record');txt(unique(warn),'warnings');txt(result_status,'status')
if(result_status=='inadmissible_fit')quit(status=3)
