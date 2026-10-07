args <- commandArgs(trailingOnly=TRUE)
if(length(args)!=4 || args[1]!='--config' || args[3]!='--out') stop('Use --config analysis_config.json --out NEW_DIRECTORY')
cfg <- jsonlite::fromJSON(args[2], simplifyVector=FALSE)
out <- args[4]
if(dir.exists(out)) stop('Output directory already exists; refusing overwrite')
dir.create(out, recursive=TRUE)
writeLines(capture.output(sessionInfo()), file.path(out,'sessionInfo.txt'))
options(digits=17)
source <- read.csv(cfg$source_results, stringsAsFactors=FALSE, check.names=FALSE)
required <- c('key','original','digits','comparison','source_location')
if(!all(required %in% names(source))) stop('source_results missing required columns')
if(nrow(source)==0) stop('No source comparisons supplied; cannot certify an empty audit')
if(anyNA(source$key) || any(!nzchar(trimws(source$key))) || anyNA(source$source_location) || any(!nzchar(trimws(source$source_location)))) stop('Source result keys and locations must be nonempty')
if(anyDuplicated(source$key)) stop('duplicate result keys')
if(any(!source$comparison %in% c('exact','rounded'))) stop('unsupported comparison semantics')
if(any(!is.finite(source$original)) || any(!is.finite(source$digits)) || any(source$digits<0) || any(source$digits%%1!=0)) stop('invalid original values or display precision')
values <- c()
if(cfg$mode=='summary_counts') {
  d <- read.csv(cfg$input, stringsAsFactors=FALSE)
  if(!identical(sort(d$group),sort(c('intervention','control')))) stop('Exactly intervention/control required')
  if(any(!is.finite(d$failed)) || any(!is.finite(d$passed)) || any(d$failed<0) || any(d$passed<0) || any(d$failed%%1!=0) || any(d$passed%%1!=0)) stop('counts must be finite nonnegative integers')
  d$total <- d$failed+d$passed
  if(any(d$total<=0)) stop('empty group')
  i <- d[d$group=='intervention',]; c <- d[d$group=='control',]
  if(c$failed==0) stop('zero control event risk; unsupported')
  values <- c(n_intervention=i$total,n_control=c$total,n_total=sum(d$total),failed_total=sum(d$failed),passed_total=sum(d$passed),failure_risk_ratio=(i$failed/i$total)/(c$failed/c$total))
  write.csv(d,file.path(out,'derived_counts.csv'),row.names=FALSE)
  grDevices::svg(file.path(out,'failure_rates.svg'),width=6,height=4)
  rates <- 100*d$failed/d$total
  upper <- min(110,max(10,max(rates)*1.2+3))
  positions <- barplot(rates,names.arg=d$group,ylab='Failure rate (%)',ylim=c(0,upper),col=c('#1b7f79','#b86b45'),main=paste('Summary counts:',cfg$case_id))
  text(positions,rates+upper*.04,labels=paste0(d$failed,' / ',d$total))
  dev.off()
} else if(cfg$mode=='descriptive_repeated') {
  required_cfg <- c('id_column','group_column','groups','variables','na_strings','scale_min','scale_max','missing_policy','collapse','sd_denominator','scoring','standardization','sample_selection','interval_algorithm')
  if(!all(required_cfg %in% names(cfg))) stop('Required descriptive settings missing')
  if(!nzchar(trimws(cfg$scoring)) || !nzchar(trimws(cfg$sample_selection))) stop('Scoring and sample selection must be documented')
  if(cfg$standardization!='none') stop('Standardization adapter unavailable')
  if(length(cfg$scale_min)!=1 || length(cfg$scale_max)!=1 || !is.finite(cfg$scale_min) || !is.finite(cfg$scale_max) || cfg$scale_min>=cfg$scale_max) stop('Invalid scale bounds')
  if(cfg$missing_policy!='available_case_per_variable' || cfg$collapse!='require_invariant_then_unique' || cfg$sd_denominator!='n-1') stop('Unsupported or missing analysis settings')
  d <- read.csv(cfg$input,stringsAsFactors=FALSE,check.names=FALSE,na.strings=unlist(cfg$na_strings))
  needed <- c(cfg$id_column,cfg$group_column,unlist(cfg$variables))
  if(!all(needed %in% names(d))) stop('input missing required columns')
  if(anyNA(d[[cfg$id_column]]) || anyNA(d[[cfg$group_column]])) stop('missing identity/group')
  if(!setequal(unique(d[[cfg$group_column]]),unlist(cfg$groups))) stop('group levels differ from configuration')
  units <- split(d,d[[cfg$id_column]])
  one <- lapply(units,function(u) {
    if(length(unique(u[[cfg$group_column]]))!=1) stop('participant assigned multiple groups')
    row <- u[1,needed,drop=FALSE]
    for(v in unlist(cfg$variables)) {
      raw <- u[[v]]; nums <- suppressWarnings(as.numeric(raw))
      if(any(!is.na(raw)&is.na(nums))) stop(paste('nonnumeric coding',v))
      z <- unique(nums[!is.na(nums)])
      if(length(z)>1) stop(paste('repeated measurements vary; aggregation setting required',v))
      if(any(!is.finite(z)) || any(z<cfg$scale_min | z>cfg$scale_max)) stop(paste('value outside documented scale',v))
      row[[v]] <- if(length(z)) z else NA_real_
    };row
  })
  one <- do.call(rbind,one);write.csv(one,file.path(out,'participant_values.csv'),row.names=FALSE)
  if(!is.null(cfg$expected_participants_by_group)) {
    if(!setequal(names(cfg$expected_participants_by_group),unlist(cfg$groups))) stop('Expected sample counts do not cover configured groups')
    for(g in unlist(cfg$groups)) if(sum(one[[cfg$group_column]]==g)!=cfg$expected_participants_by_group[[g]]) stop(paste('Participant count differs from declared source count:',g))
  }
  missingness <- list()
  for(g in unlist(cfg$groups)) for(v in unlist(cfg$variables)) {
    all_x <- one[one[[cfg$group_column]]==g,v]
    missingness[[length(missingness)+1]] <- data.frame(group=g,variable=v,n_participants=length(all_x),n_nonmissing=sum(!is.na(all_x)),n_missing=sum(is.na(all_x)))
    x <- one[one[[cfg$group_column]]==g,v]; x <- x[!is.na(x)]
    if(length(x)<2) stop('fewer than two nonmissing participants')
    values[paste(g,v,'n',sep='|')] <- length(x)
    values[paste(g,v,'mean',sep='|')] <- mean(x)
    values[paste(g,v,'sd',sep='|')] <- sd(x)
  }
  write.csv(do.call(rbind,missingness),file.path(out,'missingness.csv'),row.names=FALSE)
} else stop('Unsupported mode; no model substitution')
calc <- data.frame(key=names(values),recomputed=as.numeric(values))
write.csv(calc,file.path(out,'recomputed_results.csv'),row.names=FALSE)
comparison <- merge(source,calc,by='key',all.x=TRUE,sort=FALSE)
if(anyNA(comparison$recomputed)) stop('requested result has no calculation')
comparison$difference <- comparison$recomputed-comparison$original
comparison$tolerance <- ifelse(comparison$comparison=='exact',0,0.5*10^(-comparison$digits))
comparison$status <- ifelse(comparison$difference==0,'consistent',ifelse(abs(comparison$difference)<=comparison$tolerance+1e-12,'rounding_explains','needs_review'))
comparison$reason <- ifelse(comparison$status=='needs_review','Difference exceeds predeclared display tolerance; inspect source settings, coding, missingness and data version. Not a paper-error verdict.','Agreement within stated numeric comparison only; not data authenticity certification.')
write.csv(comparison,file.path(out,'comparison.csv'),row.names=FALSE)
writeLines('completed',file.path(out,'status.txt'))
cat('Completed',cfg$mode,'with',nrow(comparison),'comparisons\n')
