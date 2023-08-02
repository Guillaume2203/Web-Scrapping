library(netstat)
library(RSelenium)
library(wdman)
library(stringr)
library(readr)
library(jsonlite)
library(lubridate)

#remDr$closeWindow()

#rs_driver_object <- rsDriver(
#  browser = "firefox",
#  verbose = F,port = 4445L,
#  extraCapabilities = list("moz:firefoxOptions" = list(args = list('--headless')))
#)
last_execution_time <- Sys.time()-7201


while (TRUE) {
current_time <- Sys.time()

if (as.numeric(current_time)-as.numeric(last_execution_time) >= 7200){
# Run docker ps command and capture the output
docker_ps <- system('docker ps', intern = TRUE)
# Extract the container ID from the output using regex
container_id <- regmatches(docker_ps, regexpr('[0-9a-fA-F]{12}', docker_ps))
for (id in container_id) {
  cmd <- paste("docker stop", id)
  system(cmd)
}
Sys.sleep(15)
shell('docker run -d -p 4445:4444 selenium/standalone-firefox:4.0.0')
remDr<-remoteDriver(remoteServerAddr = "localhost", port = 4445L, browserName = "firefox")
Sys.sleep(10)
#remDr<- rs_driver_object$client

remDr$open()
remDr$navigate("https://www.strava.com/login")
Sys.sleep(15)

wxbox <- remDr$findElement(using = 'css selector', "#email")
wxbox$sendKeysToElement(list("email"))
wxbox <- remDr$findElement(using = 'css selector', "#password")
wxbox$sendKeysToElement(list("password"))
webElem <- remDr$findElement(using = 'css', "#remember_me")
webElem$clickElement()
connect <-remDr$findElement(using = 'css', "#login-button")
connect$clickElement()
Sys.sleep(15)

last_execution_time <- current_time}



activities=read_rds("dir/Activities.rds")

act=as.numeric(as.matrix(activities))
Sys.sleep(10) # give the page time to fully load
remDr$navigate("https://www.strava.com/dashboard/feed?feed_type=following&num_entries=200")
Sys.sleep(15)
webElem <- remDr$findElement(using = 'css', "#rawdata-tab")
webElem$clickElement()
raw <- remDr$getPageSource()[[1]]


df=as.data.frame(strsplit(raw, split =","))
df <- df[str_detect(df[,1], "www.strava.com%2Factivities%2F"), ]
df=strsplit(df, split ="%2F")
id=as.data.frame(0)
#for (g in 1:length(df)) {if(df[[g]][1]=="\"activity_id\""){id[g,1]=df[[g]][2]}else{id[g,1]=NA} }
for (g in 1:length(df)) {id[g,1]=as.character(df[[g]][5])}
id=strsplit(id[[1]], split ="%")
df=as.data.frame(0)
for (g in 1:length(id)) {df[g,1]=as.character(id[[g]][1])}
df <- df[complete.cases(df), ] 
df=unique(as.numeric(df))

#id=as.data.frame(0)
#tod=strsplit(list, split ="_")
#for (y in 1:length(list)) { id[y,1]=tod[[y]][4]}
#id=as.numeric(unlist(id))
df=setdiff(df, act)

#Do the loop
if(length(df)!=0){
for (i in 1:length(df)) {
  Sys.sleep(5)
  remDr$navigate(paste("https://www.strava.com/activities/", df[i], sep=""))
  Sys.sleep(15)
  
  #Extract Name & Date & link & weight
  raw2=remDr$getPageSource()[[1]]
  #Extract Name
  df2=as.data.frame(strsplit(raw2, split =",\n"))
  Name <- df2[str_detect(df2[,1], "athlete_name:"), ]
  Name=as.data.frame(strsplit(Name, split =":"))
  Name=as.character(Name[2,])
  Name <- gsub('\"',"",Name)
  Name <- sub(' ',"",Name)
  
  #Extract Date
  df2=as.data.frame(strsplit(raw2, split =":"))
  Date <- df2[str_detect(df2[,1], "2023-"), ]
  Date=as.data.frame(strsplit(Date, split =c(";:")))[1,1]
  if (is.null(Date)==TRUE){
    Date=as.Date(Sys.time())
  } else {
    Date=as.character(parse_number(Date, locale=locale(grouping_mark = "-")))
    Date=as.Date(parse_datetime(Date))
    if (is.na(Date)==TRUE){
      Date=as.Date(Sys.time())
    }
  }
  
  
  #Extract link
  Link=df[i]
  

  remDr$navigate(paste("https://www.strava.com/activities/", df[i] , "/streams", sep=""))
  Sys.sleep(10)

  webElem <- tryCatch(
    expr = {remDr$findElement(using = 'css', "#rawdata-tab")},
    error = function(e) {NULL}
  )
  if (!is.null(webElem)) {
    webElem$clickElement()
    f1<-remDr$findElement(using="xpath", value="//*[@class='data']")
    f2<-f1$getElementAttribute('innerHTML')[[1]]  
    f2 <- gsub("=>", ":", f2)
    f2 <- gsub("[{}]", "", f2)
    f2 <- paste0("{",f2,"}")
    act2<-fromJSON(f2, simplifyVector = TRUE)
  } else {
    act2=as.data.frame(0)
  }

  #webElem <- remDr$findElement(using = 'css', "#rawdata-tab")
  #webElem$clickElement()
  #f1<-remDr$findElement(using="xpath", value="//*[@class='data']")
  #f2<-f1$getElementAttribute('innerHTML')[[1]]  
  #f2 <- gsub("=>", ":", f2)
  #f2 <- gsub("[{}]", "", f2)
  #f2 <- paste0("{",f2,"}")
  #act2<-fromJSON(f2, simplifyVector = TRUE)
  
  DF=list(act2$time)
  DF=c(DF, list(act2$cadence))
  DF=c(DF,list(act2$heartrate))
  DF=c(DF, list(as.numeric(act2$distance)/1000))
  DF=c(DF, list(as.numeric(act2$velocity_smooth)*3.6))
  DF=c(DF, list(act2$nm))
  DF=c(DF, list(act2$watts))
  DF=c(DF, list(act2$altitude))
  if (length(act2$latlng)==0){
  DF=c(DF, list(act2$altitude))
  DF=c(DF, list(act2$altitude))} else {
  DF=c(DF, list(act2$latlng[,2]))
  DF=c(DF, list(act2$latlng[,1]))
  }
  DF=c(DF, list(act2$headwind))
  DF=c(DF, list(act2$grade_smooth))
  DF=c(DF, list(act2$temp))
  DF=c(DF, list(act2$interval))
  DF=c(DF, list(act2$lrbalance))
  DF=c(DF, list(act2$lte))
  DF=c(DF, list(act2$rte))
  DF=c(DF, list(act2$lps))
  DF=c(DF, list(act2$rps))
  DF=c(DF, list(act2$smo2))
  DF=c(DF, list(act2$thb))
  DF=c(DF, list(act2$o2hb))
  DF=c(DF, list(act2$hhb))
  
  names(DF) <- c("secs", "cad", "hr", "km", "kph", "nm", "watts", "alt", "lon", "lat", "headwind",
                 "slope","temp", "interval", "lrbalance", "lte",
                 "rte", "lps", "rps", "smo2", "thb", "o2hb", "hhb")
  
  for (z in (1:23)) {
    if (length(DF[[z]]) == 0) {
      DF[[z]]=numeric(length(DF$secs))
    }
  }
  
  if (sum(as.numeric(DF$watts), na.rm = TRUE)==0){
    DF=0
    activities[nrow(activities)+1,1]=Link
    saveRDS(activities, "dir/Activities.rds")
  }  else {
    write.table(DF, file = paste("dir/",Name, Date, Link ,sep="_",".csv"), row.names = FALSE, dec = ".", sep = ",",
                quote = FALSE)
    activities[nrow(activities)+1,1]=Link
    saveRDS(activities, "dir/Activities.rds")
    cat("File:", paste(Name, Date, Link ,sep="_"), "\n")
  }
}
  cat("Sleep 2 min :", as.character(Sys.time()), "\n")
  Sys.sleep(120)}
else{
  cat("Sleep 3 min :", as.character(Sys.time()), "\n")
  Sys.sleep(180)}
}


# Run docker ps command and capture the output
docker_ps <- system('docker ps', intern = TRUE)
# Extract the container ID from the output using regex
container_id <- regmatches(docker_ps, regexpr('[0-9a-fA-F]{12}', docker_ps))
system(paste("docker stop ", container_id,sep=""))
