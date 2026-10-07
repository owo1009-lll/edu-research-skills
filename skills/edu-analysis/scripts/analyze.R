# Task-selected participant-level analyses. Base R + project-local jsonlite.
.libPaths(c(Sys.getenv('R_LIBS_USER'), file.path(R.home(), 'library')), include.site=FALSE)
args <- commandArgs(trailingOnly=TRUE)
if(length(args)!=2) stop('Use analyze.R PLAN_JSON NEW_OUTPUT_DIRECTORY')
cfg <- jsonlite::fromJSON(args[1], simplifyVector=FALSE)
out <- args[2]
if(dir.exists(out)) stop('Refusing to overwrite outputs')
dir.create(out, recursive=TRUE)
writeLines(capture.output(sessionInfo()), file.path(out,'sessionInfo.txt'))
writeLines(.libPaths(), file.path(out,'library_paths.txt'))
options(digits=17)
need <- function(x, keys, where) {
  if(!all(keys %in% names(x))) stop(paste('Missing explicit settings in',where,':',paste(setdiff(keys,names(x)),collapse=',')))
}
need(cfg,c('data','question','design','variables','scales','analyses','na_strings','seed','bootstrap_replicates','confidence'),'plan')
if(!nzchar(cfg$question)) stop('Research question required')
if(!is.numeric(cfg$confidence) || cfg$confidence<=0 || cfg$confidence>=1) stop('Invalid confidence level')
if(cfg$bootstrap_replicates<200 || cfg$bootstrap_replicates%%1!=0) stop('At least 200 bootstrap replicates required')
set.seed(cfg$seed)
need(cfg$design,c('unit','id','row_structure','cluster_columns','independence_basis'),'design')
if(!nzchar(cfg$design$independence_basis)) stop('Document the independence assumption, not a default')
if(!cfg$design$row_structure %in% c('one_per_unit','paired_wide')) stop('Long/repeated rows need a later longitudinal adapter')
d <- read.csv(cfg$data,sep=if(is.null(cfg$separator)) ',' else cfg$separator,
              na.strings=unlist(cfg$na_strings),check.names=FALSE,stringsAsFactors=FALSE,
              fileEncoding='UTF-8',colClasses='character')
if(!cfg$design$id %in% names(d)) stop('Unit ID column required; a documented generated row ID is permitted')
if(anyNA(d[[cfg$design$id]]) || any(!nzchar(d[[cfg$design$id]])) || anyDuplicated(d[[cfg$design$id]])) stop('Missing/duplicate unit IDs: no silent row deduplication')
if(anyDuplicated(names(d))) stop('Duplicate column names')
dict <- cfg$variables
if(!all(names(dict) %in% names(d))) stop('Dictionary includes absent columns')
used <- character()
checks <- list()
for(v in names(dict)) {
  spec <- dict[[v]]
  need(spec,c('type','meaning','source'),'variable dictionary')
  if(!nzchar(spec$meaning) || !nzchar(spec$source)) stop('Variable meaning and source required')
  if(spec$type=='numeric') {
    old <- d[[v]]; x <- suppressWarnings(as.numeric(old))
    if(any(!is.na(old)&is.na(x)) || any(!is.finite(x)&!is.na(x))) stop(paste('Invalid numeric coding',v))
    if(!is.null(spec$min) && any(x<spec$min,na.rm=TRUE)) stop(paste('Below range',v))
    if(!is.null(spec$max) && any(x>spec$max,na.rm=TRUE)) stop(paste('Above range',v))
    if(!is.null(spec$allowed) && any(!is.na(x)&!x %in% unlist(spec$allowed))) stop(paste('Unexpected numeric values',v))
    d[[v]] <- x
  } else if(spec$type=='categorical') {
    need(spec,c('levels','labels','reference'),'factor dictionary')
    levels <- unlist(spec$levels); labels <- unlist(spec$labels)
    if(length(levels)!=length(labels) || anyDuplicated(levels) || anyDuplicated(labels) || !spec$reference %in% labels) stop('Invalid factor specification')
    if(any(!is.na(d[[v]])&!d[[v]] %in% as.character(levels))) stop(paste('Unexpected category',v))
    d[[v]] <- relevel(factor(d[[v]],levels=as.character(levels),labels=labels),ref=spec$reference)
  } else stop('Variable type must be numeric or categorical')
  checks[[length(checks)+1]] <- data.frame(variable=v,type=spec$type,n=nrow(d),missing=sum(is.na(d[[v]])),distinct=length(unique(d[[v]][!is.na(d[[v]])])))
}
write.csv(do.call(rbind,checks),file.path(out,'variable_checks.csv'),row.names=FALSE)
clusters <- unlist(cfg$design$cluster_columns)
if(length(clusters) && !all(clusters %in% names(d))) stop('Declared cluster columns absent')
suspects <- grep('(^|_)(class|classroom|school|teacher|cluster|session)(_|$)',names(d),value=TRUE,ignore.case=TRUE)
undeclared <- setdiff(suspects,clusters)
if(length(undeclared)) stop(paste('Potential nesting columns need explicit design handling:',paste(undeclared,collapse=',')))
observed_clusters <- clusters[vapply(clusters,function(v)length(unique(na.omit(d[[v]])))>1,logical(1))]
inferential <- any(vapply(cfg$analyses,function(a)a$method!='descriptive',logical(1)))
if(length(observed_clusters) && inferential) stop('Observed nesting: independent-sample inference refused; clustered/multilevel models not implemented')
warnings <- character()
if(length(clusters)) warnings <- c(warnings,'Only one observed cluster: population-level generalization still restricted')
if(length(cfg$design$possible_unmeasured_clusters)) warnings <- c(warnings,paste('Unmeasured clustering:',paste(unlist(cfg$design$possible_unmeasured_clusters),collapse=','),'Inference is explicitly conditional on independence'))
score_log <- list()
scale_items <- list()
for(s in cfg$scales) {
  need(s,c('name','items','min','max','reverse','aggregation','min_items','source','missing_rule'),'scoring rule')
  items <- unlist(s$items); reverse <- unlist(s$reverse)
  if(length(items)<1 || anyDuplicated(items) || !all(items %in% names(dict)) || !all(reverse %in% items)) stop('Invalid scoring items')
  if(s$name %in% names(d)) stop('Scoring would overwrite a source column')
  if(!nzchar(s$source) || !nzchar(s$missing_rule) || s$min>=s$max || s$min_items<1 || s$min_items>length(items)) stop('Invalid explicit scoring settings')
  if(!all(vapply(d[items],is.numeric,logical(1)))) stop('Scoring items must be numeric')
  x <- as.matrix(d[items])
  if(any(x<s$min|x>s$max,na.rm=TRUE)) stop('Scoring values outside documented range')
  if(length(reverse)) x[,reverse] <- s$min+s$max-x[,reverse,drop=FALSE]
  count <- rowSums(!is.na(x)); mean_x <- rowMeans(x,na.rm=TRUE)
  score <- switch(s$aggregation,mean=mean_x,sum={
    if(s$min_items<length(items) && !identical(s$sum_method,'prorated')) stop('Partial-item sums require explicitly declared prorating')
    mean_x*length(items)
  },stop('Only mean/sum scoring implemented'))
  score[count<s$min_items] <- NA_real_
  d[[s$name]] <- score
  scale_items[[s$name]] <- x
  score_log[[length(score_log)+1]] <- data.frame(scale=s$name,items=length(items),reverse=paste(reverse,collapse='|'),aggregation=s$aggregation,min_items=s$min_items,n_scored=sum(!is.na(score)),n_unscored=sum(is.na(score)),source=s$source,missing_rule=s$missing_rule)
}
if(length(score_log)) write.csv(do.call(rbind,score_log),file.path(out,'scoring.csv'),row.names=FALSE)
write.csv(d,file.path(out,'scored_data.csv'),row.names=FALSE,na='') # sensitive: retained only in the private run
rows <- list(); diagnostics <- list(); samples <- list()
emit <- function(id,method,term,n,estimate=NA_real_,low=NA_real_,high=NA_real_,statistic=NA_real_,df=NA_real_,p=NA_real_,detail='') {
  rows[[length(rows)+1]] <<- data.frame(analysis=id,method=method,term=term,n=n,estimate=estimate,ci_low=low,ci_high=high,statistic=statistic,df=df,p=p,detail=detail)
}
record_diagnostic <- function(id,check,value=NA_real_,p=NA_real_,note='') {
  diagnostics[[length(diagnostics)+1]] <<- data.frame(analysis=id,check=check,value=value,p=p,note=note)
}
normality <- function(id,x,label) {
  if(length(x)>=3 && length(x)<=5000 && sd(x)>0) {
    t <- shapiro.test(x); record_diagnostic(id,paste0('Shapiro_',label),unname(t$statistic),t$p.value,'Diagnostic, not automatic accept/reject; inspect QQ plot and design')
  } else record_diagnostic(id,paste0('Shapiro_',label),note='Unavailable at this sample size or constant values')
}
boot_ci <- function(values) {
  finite <- values[is.finite(values)]
  if(length(finite)<.8*cfg$bootstrap_replicates) stop('Too many degenerate bootstrap resamples; CI unavailable')
  record_diagnostic(id, 'valid_bootstrap_replicates', length(finite), note=paste('requested=', cfg$bootstrap_replicates))
  as.numeric(quantile(finite,c((1-cfg$confidence)/2,(1+cfg$confidence)/2),names=FALSE,type=7))
}
alpha_raw <- function(x) {
  if(ncol(x)<2 || nrow(x)<3) return(NA_real_)
  total <- var(rowSums(x)); if(total<=0)return(NA_real_)
  ncol(x)/(ncol(x)-1)*(1-sum(apply(x,2,var))/total)
}
standard_effect <- function(x,y=NULL,paired=FALSE) {
  if(paired) return(mean(x-y)/sd(x-y))
  nu <- length(x)+length(y)-2
  pooled <- sqrt(((length(x)-1)*var(x)+(length(y)-1)*var(y))/nu)
  correction <- exp(lgamma(nu/2)-.5*log(nu/2)-lgamma((nu-1)/2))
  correction*(mean(x)-mean(y))/pooled
}
select_sample <- function(a,vars) {
  if(!all(vars %in% names(d))) stop('Analysis refers to absent variables')
  if(!a$missing %in% c('complete_case','available_case')) stop('Missing rule must be explicit; no automatic imputation')
  z <- d; eligibility <- rep(TRUE,nrow(z))
  for(f in a$filters) {
    if(!f$variable %in% names(d) || !identical(f$operator,'in')) stop('Only explicit in-list filters implemented')
    eligibility <- eligibility & !is.na(z[[f$variable]]) & as.character(z[[f$variable]]) %in% as.character(unlist(f$values))
  }
  ok <- eligibility & complete.cases(z[vars])
  samples[[length(samples)+1]] <<- data.frame(analysis=a$id,n_input=nrow(d),n_eligible=sum(eligibility),n_complete=sum(ok),n_missing=sum(eligibility & !complete.cases(z[vars])),missing_rule=a$missing)
  write.csv(data.frame(unit_id=z[[cfg$design$id]][ok]),file.path(out,paste0(a$id,'_sample.csv')),row.names=FALSE)
  z[ok,,drop=FALSE]
}

# Observed-variable, one-row-per-independent-unit extensions. No ordered-model search.
path_fit <- function(response, predictors, z) {
  f <- lm(reformulate(predictors, response=response), data=z, na.action=na.fail)
  if(f$rank!=ncol(model.matrix(f)) || df.residual(f)<3 || any(!is.finite(coef(f))))
    stop('Path model rank deficient or insufficient degrees of freedom')
  f
}
path_vcov <- function(f, inference) {
  if(inference=='OLS') return(vcov(f))
  X<-model.matrix(f);h<-hatvalues(f)
  if(any(h>=1-1e-10)) stop('HC3 leverage denominator unavailable')
  inv<-solve(crossprod(X))
  inv%*%crossprod(X,X*as.numeric(residuals(f)^2/(1-h)^2))%*%inv
}
path_coefficients <- function(f, label, inference) {
  b<-coef(f);se<-sqrt(diag(path_vcov(f,inference)));nu<-df.residual(f);crit<-qt((1+cfg$confidence)/2,nu)
  for(j in seq_along(b)) emit(id,paste0('path_',inference),paste(label,names(b)[j],sep=':'),nobs(f),
    b[j],b[j]-crit*se[j],b[j]+crit*se[j],b[j]/se[j],nu,2*pt(-abs(b[j]/se[j]),nu),
    if(inference=='HC3') 'Unstandardized coefficient; HC3 t reference approximate; interpret using recorded design' else 'Unstandardized coefficient; OLS t reference with residual df; interpret using recorded design')
  normality(id,residuals(f),paste0(label,'_residuals'))
  record_diagnostic(id,paste0(label,'_max_leverage'),max(hatvalues(f)))
  record_diagnostic(id,paste0(label,'_max_Cooks_distance'),max(cooks.distance(f)))
  record_diagnostic(id,paste0(label,'_predicted_outcome_min'),min(fitted(f)))
  record_diagnostic(id,paste0(label,'_predicted_outcome_max'),max(fitted(f)))
  pdf(file.path(out,paste0(id,'_',label,'_diagnostics.pdf')));par(mfrow=c(2,2));plot(f);dev.off()
}
run_path_analysis <- function(a) {
  need(a,c('x','outcome','covariates','center','inference','time_order','path_rationale'),'path analysis')
  if(!identical(cfg$design$row_structure,'one_per_unit')) stop('Path extensions require one row per independent unit; repeated/paired designs unsupported')
  if(!a$inference %in% c('OLS','HC3')) stop('Choose OLS or HC3 inference')
  if(!nzchar(a$time_order) || !nzchar(a$path_rationale)) stop('Document time order and substantive path rationale')
  covs<-unlist(a$covariates);meds<-unlist(a$mediators)
  if(a$method=='moderation') {need(a,c('w','moderator_values'),'moderation');extra<-a$w}
  else {if(length(meds)!=if(a$method=='simple_mediation')1L else 2L)stop('Declare one or two mediators in the intended order');extra<-meds}
  vars<-c(a$x,a$outcome,extra,covs)
  if(anyDuplicated(vars) || any(!grepl('^[A-Za-z][A-Za-z0-9_]*$',vars)))stop('Roles require distinct safe column names')
  z<-select_sample(a,vars);n<-nrow(z)
  if(n<8 || !is.numeric(z[[a$outcome]]) || sd(z[[a$outcome]])==0)stop('Numeric nonconstant outcome and >=8 complete units required')
  z2<-data.frame(.Y=z[[a$outcome]],.X=z[[a$x]])
  if(!is.numeric(z2$.X) && !is.factor(z2$.X))stop('Predictor must be numeric or explicitly coded factor')
  if(is.factor(z2$.X)) {
    if(any(table(z2$.X)==0))stop('An X level has no complete cases; no silent level or reference change')
    if(a$method!='moderation') {
      if(nlevels(z2$.X)!=2)stop('Mediation currently supports numeric or binary X')
      z2$.X<-as.numeric(z2$.X==levels(z2$.X)[2])
    }
  }
  cn<-if(length(covs))paste0('.C',seq_along(covs)) else character()
  for(j in seq_along(covs)) z2[[cn[j]]]<-z[[covs[j]]]
  centers<-unlist(a$center);allowed<-if(a$method=='moderation')c(a$x,a$w) else a$x
  if(anyDuplicated(centers) || !all(centers %in% allowed))stop('Center only explicitly named numeric X/W; not mediators or covariates')
  offsets<-list()
  for(v in centers) {
    if(!is.numeric(z[[v]]))stop('Do not center categorical variables')
    offsets[[v]]<-mean(z[[v]])
  }
  if(a$x %in% centers)z2$.X<-z2$.X-offsets[[a$x]]
  coding<-list(x=a$x,x_type=if(is.factor(z[[a$x]]))'factor' else 'numeric',
    x_levels=if(is.factor(z[[a$x]]))levels(z[[a$x]]) else NULL,
    mediation_binary_coding=if(a$method!='moderation' && is.factor(z[[a$x]]))'first declared reference=0, other=1' else NULL,
    covariates=if(length(covs))as.list(setNames(covs,cn)) else list(),centering_offsets=offsets,n_complete=n,
    time_order=a$time_order,path_rationale=a$path_rationale,
    limits='Observed-variable additive linear paths; complete cases for all paths; no causal identification, clustering, repeated-measure, SEM or model-order search')
  if(a$method=='moderation') {
    z2$.W<-z[[a$w]]
    if(is.factor(z2$.W)) {if(nlevels(z2$.W)!=2 || any(table(z2$.W)==0))stop('W supports numeric or complete binary factor')}
    else if(!is.numeric(z2$.W) || sd(z2$.W)==0)stop('W must be nonconstant numeric or binary factor')
    if(a$w %in% centers)z2$.W<-z2$.W-offsets[[a$w]]
    f<-path_fit('.Y',c('.X*.W',cn),z2);path_coefficients(f,'outcome',a$inference)
    V<-path_vcov(f,a$inference);b<-coef(f);nu<-df.residual(f);crit<-qt((1+cfg$confidence)/2,nu)
    wvals<-unlist(a$moderator_values)
    if(!length(wvals) || anyDuplicated(wvals))stop('Specify unique moderator values on original scale/labels')
    if(is.numeric(z2$.W)) {
      if(!is.numeric(wvals) || any(!is.finite(wvals)))stop('Numeric moderator values required')
      if(any(wvals<min(z[[a$w]]) | wvals>max(z[[a$w]])))stop('Conditional effects outside observed moderator range not supported')
      wencoded<-wvals-if(a$w %in% centers)offsets[[a$w]] else 0
    } else {if(!all(wvals %in% levels(z2$.W)))stop('Moderator labels absent');wencoded<-wvals}
    base<-z2[1,,drop=FALSE]
    for(v in cn)base[[v]]<-if(is.factor(z2[[v]]))factor(levels(z2[[v]])[1],levels=levels(z2[[v]])) else mean(z2[[v]])
    mm<-function(nd)model.matrix(delete.response(terms(f)),nd,contrasts.arg=f$contrasts,xlev=f$xlevels)
    contrasts_x<-if(is.factor(z2$.X))levels(z2$.X)[-1] else 'one_unit'
    for(k in seq_along(wvals)) for(xlabel in contrasts_x) {
      nd<-base[rep(1,2),,drop=FALSE]
      nd$.W<-if(is.factor(z2$.W))factor(rep(wencoded[k],2),levels=levels(z2$.W)) else rep(wencoded[k],2)
      nd$.X<-if(is.factor(z2$.X))factor(c(levels(z2$.X)[1],xlabel),levels=levels(z2$.X)) else c(0,1)
      L<-mm(nd)[2,]-mm(nd)[1,];est<-sum(L*b);se<-sqrt(as.numeric(t(L)%*%V%*%L))
      emit(id,paste0('conditional_effect_',a$inference),paste0(xlabel,'|',a$w,'=',wvals[k]),n,est,est-crit*se,est+crit*se,est/se,nu,2*pt(-abs(est/se),nu),
        if(is.factor(z2$.X))paste('Contrast against',levels(z2$.X)[1],';original W scale') else 'X simple slope; original W scale; no multiplicity adjustment')
    }
    grid_w<-if(is.numeric(z2$.W))seq(min(z2$.W),max(z2$.W),length.out=80) else levels(z2$.W)
    if(is.factor(z2$.X))grid_x<-levels(z2$.X) else {
      need(a,'plot_x_values','numeric X moderation plot');grid_x<-unlist(a$plot_x_values)
      if(!is.numeric(grid_x) || !length(grid_x) || any(!is.finite(grid_x)) || any(grid_x<min(z[[a$x]]) | grid_x>max(z[[a$x]])))stop('Plot X values must be in observed original scale')
      grid_x<-grid_x-if(a$x %in% centers)offsets[[a$x]] else 0
    }
    g<-expand.grid(.W=grid_w,.X=grid_x,stringsAsFactors=FALSE)
    if(is.factor(z2$.X))g$.X<-factor(g$.X,levels=levels(z2$.X))
    if(is.factor(z2$.W))g$.W<-factor(g$.W,levels=levels(z2$.W))
    for(v in cn)g[[v]]<-base[[v]][rep(1,nrow(g))]
    GX<-mm(g);g$fit<-as.numeric(GX%*%b);g$se<-sqrt(rowSums((GX%*%V)*GX));g$low<-g$fit-crit*g$se;g$high<-g$fit+crit*g$se
    g$W_original<-if(is.numeric(z2$.W))g$.W+if(a$w %in% centers)offsets[[a$w]] else 0 else as.character(g$.W)
    g$X_original<-if(is.numeric(z2$.X))g$.X+if(a$x %in% centers)offsets[[a$x]] else 0 else as.character(g$.X)
    write.csv(g,file.path(out,paste0(id,'_prediction_grid.csv')),row.names=FALSE)
    pdf(file.path(out,paste0(id,'_moderation.pdf')))
    wx<-if(is.numeric(z2$.W))g$W_original else match(g$W_original,levels(z2$.W));plot(wx,g$fit,type='n',xlab=a$w,ylab=paste(a$outcome,'conditional mean'),ylim=range(g$low,g$high))
    groups<-unique(g$X_original)
    for(j in seq_along(groups)){keep<-g$X_original==groups[j];lines(wx[keep],g$fit[keep],type='b',col=j);lines(wx[keep],g$low[keep],lty=2,col=j);lines(wx[keep],g$high[keep],lty=2,col=j)}
    legend('topleft',legend=paste(a$x,groups,sep='='),col=seq_along(groups),lty=1,bty='n');dev.off()
    coding$w<-a$w;coding$w_levels<-if(is.factor(z2$.W))levels(z2$.W) else NULL
    coding$plot_covariates<-'Numeric at complete-case means, factors at declared reference; pointwise mean confidence bands, not prediction intervals'
  } else {
    for(j in seq_along(meds)) {if(!is.numeric(z[[meds[j]]]) || sd(z[[meds[j]]])==0)stop('Mediators must be nonconstant numeric observed variables');z2[[paste0('.M',j)]]<-z[[meds[j]]]}
    serial<-a$method=='serial_mediation'
    fit_all<-function(dat) {
      m1<-path_fit('.M1',c('.X',cn),dat)
      total<-path_fit('.Y',c('.X',cn),dat)
      if(serial){m2<-path_fit('.M2',c('.X','.M1',cn),dat);y<-path_fit('.Y',c('.X','.M1','.M2',cn),dat)}
      else y<-path_fit('.Y',c('.X','.M1',cn),dat)
      c1<-coef(m1);cy<-coef(y);ct<-coef(total)
      specific<-if(serial)c(via_M1=c1[['.X']]*cy[['.M1']],via_M2=coef(m2)[['.X']]*cy[['.M2']],via_M1_M2=c1[['.X']]*coef(m2)[['.M1']]*cy[['.M2']]) else c(via_M1=c1[['.X']]*cy[['.M1']])
      effects<-c(direct=cy[['.X']],total=ct[['.X']],specific,total_indirect=sum(specific))
      if(abs(effects[['total']]-effects[['direct']]-effects[['total_indirect']])>1e-8*max(1,abs(effects[['total']])))stop('Total/direct/indirect decomposition failed')
      list(effects=effects,models=if(serial)list(M1=m1,M2=m2,outcome=y,total=total) else list(M1=m1,outcome=y,total=total))
    }
    point<-fit_all(z2)
    for(label in names(point$models))path_coefficients(point$models[[label]],label,a$inference)
    B<-cfg$bootstrap_replicates;indices<-matrix(NA_integer_,B,n);draws<-matrix(NA_real_,B,length(point$effects),dimnames=list(NULL,names(point$effects)))
    failures<-character(B)
    for(k in seq_len(B)){
      indices[k,]<-sample.int(n,n,replace=TRUE)
      value<-tryCatch(fit_all(z2[indices[k,],,drop=FALSE])$effects,error=function(e){failures[k]<<-conditionMessage(e);NULL})
      if(!is.null(value))draws[k,]<-value
    }
    valid<-apply(draws,1,function(v)all(is.finite(v)))
    write.csv(indices,file.path(out,paste0(id,'_bootstrap_indices.csv')),row.names=FALSE)
    write.csv(data.frame(replicate=seq_len(B),draws,check.names=FALSE),file.path(out,paste0(id,'_bootstrap_draws.csv')),row.names=FALSE,na='')
    write.csv(data.frame(replicate=which(!valid),reason=failures[!valid]),file.path(out,paste0(id,'_bootstrap_failures.csv')),row.names=FALSE)
    record_diagnostic(id,'path_bootstrap_valid',sum(valid),note=paste('requested=',B,';whole independent units; all paths jointly refit; same complete-case sample'))
    if(sum(valid)<.8*B)stop('Fewer than 80% jointly valid full-path bootstrap replicates; no effect CI')
    for(term in names(point$effects)){
      ci<-as.numeric(quantile(draws[valid,term],c((1-cfg$confidence)/2,(1+cfg$confidence)/2),names=FALSE,type=7))
      emit(id,'indirect_association_bootstrap',term,n,point$effects[[term]],ci[1],ci[2],detail='Percentile type7; full path refit in each row resample; total indirect summed within each draw; no causal interpretation or total-effect significance gate')
    }
    coding$mediators_in_declared_order<-meds;coding$bootstrap_valid<-sum(valid);coding$bootstrap_failed<-sum(!valid)
  }
  jsonlite::write_json(coding,file.path(out,paste0(id,'_encoding.json')),auto_unbox=TRUE,pretty=TRUE,null='null')
}

ids <- vapply(cfg$analyses,function(a)a$id,character(1))
if(anyDuplicated(ids) || any(!grepl('^[A-Za-z][A-Za-z0-9_-]{0,63}$',ids))) stop('Unique safe analysis IDs required')
for(a in cfg$analyses) {
  need(a,c('id','method','purpose','missing'),'analysis')
  if(!nzchar(a$purpose)) stop('Each analysis needs a question-linked purpose')
  id <- a$id
  if(a$method!='descriptive' && !identical(a$missing,'complete_case')) stop('Inferential analyses require complete-case handling for their selected variables')
  if(a$method=='descriptive') {
    if(!identical(a$missing,'available_case'))stop('Descriptives use explicitly declared available cases per variable')
    for(v in unlist(a$variables)) {
      z <- select_sample(modifyList(a,list(id=paste0(id,'_',v))),c(v,unlist(a$group)))
      if(!is.numeric(z[[v]])) stop('Descriptive mean requires numeric variable')
      groups <- if(is.null(a$group))list(all=z[[v]]) else split(z[[v]],z[[a$group]],drop=TRUE)
      for(g in names(groups)) {
        x <- groups[[g]]; n <- length(x); if(n<2)stop('Fewer than two observations for descriptive CI')
        se <- sd(x)/sqrt(n); margin <- qt((1+cfg$confidence)/2,n-1)*se
        emit(id,'descriptive',paste(v,g,sep='|'),n,mean(x),mean(x)-margin,mean(x)+margin,detail=paste('sd=',sd(x),';median=',median(x),';range=',min(x),max(x),';mean CI=Student t'))
      }
    }
  } else if(a$method=='alpha') {
    if(!identical(a$missing,'complete_case') || is.null(scale_items[[a$scale]]))stop('Alpha requires a configured scale and complete items')
    x <- scale_items[[a$scale]]; eligible <- select_sample(a,colnames(x)); x <- x[match(eligible[[cfg$design$id]],d[[cfg$design$id]]),,drop=FALSE]
    n <- nrow(x); estimate <- alpha_raw(x);if(!is.finite(estimate))stop('Alpha unavailable for insufficient/constant data')
    vals <- replicate(cfg$bootstrap_replicates,alpha_raw(x[sample.int(n,n,replace=TRUE),,drop=FALSE])); ci <- boot_ci(vals)
    emit(id,'raw_Cronbach_alpha',a$scale,n,estimate,ci[1],ci[2],detail='Row bootstrap percentile CI; item reversal precedes covariance; alpha does not establish unidimensionality or validity')
    record_diagnostic(id,'minimum_item_variance',min(apply(x,2,var)),note='Do not silently remove constant items or maximize alpha')
  } else if(a$method %in% c('pearson','spearman')) {
    z <- select_sample(a,c(a$x,a$y)); x <- z[[a$x]];y <- z[[a$y]];n <- length(x)
    if(n<4 || !is.numeric(x) || !is.numeric(y) || sd(x)==0 || sd(y)==0)stop('Correlation needs at least four nonconstant numeric pairs')
    t <- if(a$method=='pearson') cor.test(x,y,method='pearson',conf.level=cfg$confidence) else cor.test(x,y,method='spearman',exact=FALSE,continuity=FALSE)
    if(a$method=='pearson') ci <- unname(t$conf.int) else {
      vals <- replicate(cfg$bootstrap_replicates,{i<-sample.int(n,n,replace=TRUE);suppressWarnings(cor(x[i],y[i],method='spearman'))});ci<-boot_ci(vals)
    }
    emit(id,a$method,paste(a$x,a$y,sep='~'),n,unname(t$estimate),ci[1],ci[2],unname(t$statistic),if(length(t$parameter))unname(t$parameter) else NA_real_,t$p.value,if(a$method=='pearson')'Fisher z CI; association, not causal effect' else 'Asymptotic t p-value with ties; row-bootstrap percentile CI')
    record_diagnostic(id,'ties_x',n-length(unique(x)));record_diagnostic(id,'ties_y',n-length(unique(y)))
    pdf(file.path(out,paste0(id,'_scatter.pdf')));plot(x,y,xlab=a$x,ylab=a$y);lines(lowess(x,y),col='red');dev.off()
  } else if(a$method %in% c('independent_t','paired_t')) {
    if(a$method=='paired_t') {
      if(!identical(cfg$design$row_structure,'paired_wide'))stop('Paired t requires explicitly aligned wide pairs')
      z <- select_sample(a,c(a$x,a$y));x <- z[[a$x]]; y <- z[[a$y]]; n <- nrow(z)
      if(n<3 || !is.numeric(x) || !is.numeric(y))stop('Paired t needs at least three numeric pairs')
      t <- t.test(x,y,paired=TRUE,conf.level=cfg$confidence); effect <- standard_effect(x,y,TRUE)
      vals <- replicate(cfg$bootstrap_replicates,{i<-sample.int(n,n,replace=TRUE);standard_effect(x[i],y[i],TRUE)})
      emit(id,'paired_t','mean_difference_x_minus_y',n,mean(x-y),t$conf.int[1],t$conf.int[2],unname(t$statistic),unname(t$parameter),t$p.value,'Pairs matched by unique unit ID; missing pairs excluded together')
      normality(id,x-y,'differences'); effect_name <- 'Cohen_dz'
    } else {
      if(!cfg$design$row_structure %in% c('one_per_unit','paired_wide'))stop('Independent t design unsupported')
      need(a,c('groups','variance'),'independent t')
      z <- select_sample(a,c(a$outcome,a$group));g <- as.character(z[[a$group]]);levels <- unlist(a$groups)
      if(length(levels)!=2 || !setequal(unique(g),levels))stop('Exactly the two declared groups must be selected')
      x <- z[[a$outcome]][g==levels[1]];y <- z[[a$outcome]][g==levels[2]]
      if(min(length(x),length(y))<3 || !is.numeric(x) || !is.numeric(y))stop('At least three numeric observations per group')
      if(!a$variance %in% c('welch','pooled'))stop('Declare Welch or pooled variance')
      t <- t.test(x,y,var.equal=a$variance=='pooled',conf.level=cfg$confidence); n <- length(x)+length(y)
      effect <- standard_effect(x,y);vals<-replicate(cfg$bootstrap_replicates,standard_effect(sample(x,length(x),replace=TRUE),sample(y,length(y),replace=TRUE)))
      emit(id,paste0(a$variance,'_t'),paste0(levels[1],'-',levels[2]),n,mean(x)-mean(y),t$conf.int[1],t$conf.int[2],unname(t$statistic),unname(t$parameter),t$p.value,paste('n1=',length(x),';n2=',length(y)))
      normality(id,x,'group1');normality(id,y,'group2');record_diagnostic(id,'variance_ratio',var(x)/var(y));effect_name<-'Hedges_g_pooled_SD'
    }
    ci <- boot_ci(vals);emit(id,effect_name,'standardized_difference',n,effect,ci[1],ci[2],detail='Bootstrap percentile CI; independent Hedges g uses pooled SD even when mean test is Welch')
  } else if(a$method=='anova') {
    need(a,c('outcome','group','variance'),'ANOVA')
    z <- select_sample(a,c(a$outcome,a$group)); y <- z[[a$outcome]]; g <- droplevels(factor(z[[a$group]]));n<-length(y)
    if(!is.numeric(y) || nlevels(g)<2 || any(table(g)<3))stop('ANOVA requires numeric outcome and >=3 observations in each group')
    fit <- lm(y~g);tab<-anova(fit);ss<-tab$'Sum Sq';eta<-ss[1]/sum(ss)
    if(a$variance=='classical') { statistic<-tab$'F value'[1];df<-tab$Df[1];p<-tab$'Pr(>F)'[1];df2<-tab$Df[2] }
    else if(a$variance=='welch') { test<-oneway.test(y~g,var.equal=FALSE);statistic<-unname(test$statistic);df<-unname(test$parameter[1]);df2<-unname(test$parameter[2]);p<-test$p.value }
    else stop('Declare classical or Welch ANOVA')
    emit(id,paste0(a$variance,'_anova'),'omnibus_F',n,statistic=statistic,df=df,p=p,detail=paste('denominator_df=',df2,';no automatic post-hoc search'))
    vals<-replicate(cfg$bootstrap_replicates,{i<-unlist(lapply(split(seq_len(n),g),function(k)sample(k,length(k),replace=TRUE)));aovtab<-anova(lm(y[i]~g[i]));aovtab$'Sum Sq'[1]/sum(aovtab$'Sum Sq')})
    ci<-boot_ci(vals);emit(id,'eta_squared','between_group_variation',n,eta,ci[1],ci[2],detail='Classical SS-based descriptive effect, stratified row-bootstrap CI; also reported alongside Welch test')
    dev<-abs(y-ave(y,g,FUN=median)); bf<-anova(lm(dev~g));record_diagnostic(id,'Brown_Forsythe',bf$'F value'[1],bf$'Pr(>F)'[1],'Median-centered variance diagnostic; no result-driven test switching')
    normality(id,residuals(fit),'residuals')
    pdf(file.path(out,paste0(id,'_diagnostics.pdf')));par(mfrow=c(1,2));plot(g,y);qqnorm(residuals(fit));qqline(residuals(fit));dev.off()
  } else if(a$method=='regression') {
    need(a,c('outcome','predictors','inference'),'regression')
    predictors<-unlist(a$predictors);if(!length(predictors) || anyDuplicated(predictors))stop('At least one unique predictor required')
    if(!a$inference %in% c('OLS','HC3'))stop('Declare OLS or HC3 intervals')
    vars<-c(a$outcome,predictors);if(any(!grepl('^[A-Za-z][A-Za-z0-9_]*$',vars)))stop('Formula accepts column names only, not expressions or interactions')
    z<-select_sample(a,vars);if(!is.numeric(z[[a$outcome]]))stop('Regression outcome must be numeric')
    form<-reformulate(predictors,response=a$outcome);fit<-lm(form,data=z,na.action=na.fail);X<-model.matrix(fit);n<-nrow(X);pdim<-ncol(X);nu<-df.residual(fit)
    if(fit$rank!=pdim || nu<3)stop('Rank deficiency/insufficient residual degrees of freedom')
    b<-coef(fit);e<-residuals(fit);hat<-hatvalues(fit);if(any(hat>=1-1e-10))stop('HC3 leverage denominator unavailable')
    inv<-solve(crossprod(X));hc3<-inv%*%crossprod(X, X*as.numeric(e^2/(1-hat)^2))%*%inv
    for(kind in c('OLS','HC3')) {
      se<-sqrt(diag(if(kind=='OLS')vcov(fit) else hc3));crit<-qt((1+cfg$confidence)/2,nu)
      for(j in seq_along(b)) emit(id,paste0('linear_regression_',kind),names(b)[j],n,b[j],b[j]-crit*se[j],b[j]+crit*se[j],b[j]/se[j],nu,2*pt(-abs(b[j]/se[j]),nu),paste('Chosen inference=',a$inference,';unstandardized coefficient;t reference for HC3 is an approximation'))
    }
    fit_summary<-summary(fit); f<-fit_summary$fstatistic
    emit(id,'linear_regression','R_squared',n,fit_summary$r.squared,detail=paste('adjusted_R_squared=',fit_summary$adj.r.squared,';OLS_F=',f[1],';df=',f[2],f[3],';p=',pf(f[1],f[2],f[3],lower.tail=FALSE)))
    normality(id,e,'residuals')
    aux<-lm(e^2~X[,-1,drop=FALSE]); bp<-n*summary(aux)$r.squared;record_diagnostic(id,'Breusch_Pagan_auxiliary',bp,pchisq(bp,pdim-1,lower.tail=FALSE),'Auxiliary squared-residual n*R2 diagnostic; HC3 does not fix clustering, nonlinearity or confounding')
    record_diagnostic(id,'max_Cooks_distance',max(cooks.distance(fit)));record_diagnostic(id,'max_leverage',max(hat));record_diagnostic(id,'condition_number',kappa(X))
    if(pdim>2) for(j in 2:pdim) {
      r2<-summary(lm(X[,j]~X[,-c(1,j),drop=FALSE]))$r.squared
      record_diagnostic(id,paste0('design_column_VIF:',colnames(X)[j]),1/(1-r2),note='Dummy-column VIF, not factor-level GVIF')
    }
    write.csv(data.frame(unit_id=z[[cfg$design$id]],fitted=fitted(fit),residual=e,leverage=hat,cooks_distance=cooks.distance(fit)),file.path(out,paste0(id,'_residuals.csv')),row.names=FALSE)
    pdf(file.path(out,paste0(id,'_diagnostics.pdf')));par(mfrow=c(2,2));plot(fit);dev.off()
  } else if(a$method %in% c('moderation','simple_mediation','serial_mediation')) {
    run_path_analysis(a)
  } else stop(paste('Unsupported method:',a$method))
}
write.csv(do.call(rbind,rows),file.path(out,'results.csv'),row.names=FALSE,na='')
if(length(diagnostics))write.csv(do.call(rbind,diagnostics),file.path(out,'diagnostics.csv'),row.names=FALSE,na='')
write.csv(do.call(rbind,samples),file.path(out,'analysis_samples.csv'),row.names=FALSE)
jsonlite::write_json(list(question=cfg$question,design=cfg$design,confidence=cfg$confidence,bootstrap=list(seed=cfg$seed,rng_kind=RNGkind(),replicates=cfg$bootstrap_replicates,algorithm='percentile, quantile type 7, degenerate replicates omitted only when >=80% valid'),warnings=warnings,analyses=cfg$analyses),file.path(out,'analysis_notes.json'),auto_unbox=TRUE,pretty=TRUE,null='null')
writeLines(warnings,file.path(out,'warnings.txt'))
writeLines('completed',file.path(out,'status.txt'))
cat('Completed',length(cfg$analyses),'preselected analyses for',nrow(d),'input units\n')
